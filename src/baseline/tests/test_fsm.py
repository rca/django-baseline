import pytest
from django.db import models
from django_fsm import FSMField, TransitionNotAllowed
from model_utils import Choices

from baseline.fsm import transition


def assert_state(instance):
    """
    Callable to be passed into a transition method to inspect the running state
    """
    assert instance.state == "do_thing_running"


class Thing(models.Model):
    """
    A class to test the transition running state
    """

    CHOICES = Choices("new", "done", "error")
    state = FSMField(choices=CHOICES, default=CHOICES.new)

    def save(self, *args, **kwargs):
        """
        Overrides the default state to make this a no-op
        """

    @transition(state, source=CHOICES.new, target=CHOICES.done, on_error=CHOICES.error)
    def do_thing(self, callable):
        """
        Call the callable with the instance object

        Args:
            callable: the callable to run
        """
        callable(self)


def test_set_transition_state():
    """
    Ensures a transition state is set when using the custom transition decorator
    """
    x = Thing()
    x.do_thing(assert_state)

    # ensure the target transition is set when the process is done
    assert x.state == x.CHOICES.done


def test_cant_call_while_running():
    """
    Ensures the transition cannot be called when already in a running state
    """

    def rerun(instance):
        instance.do_thing(rerun)

    x = Thing()

    with pytest.raises(TransitionNotAllowed):
        x.do_thing(rerun)

    # ensure the target transition is set when the process is done
    assert x.state == x.CHOICES.error
