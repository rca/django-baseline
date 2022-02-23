import pytest

from unittest import mock

from django_fsm import FSMField, TransitionNotAllowed
from model_utils import Choices

from baseline.fsm import transition


def get_thing(*args, **kwargs):
    thing = Thing(*args, **kwargs)

    return thing


def test_set_transition_state():
    """
    Ensures a transition state is set when using the custom transition decorator
    """

    def assert_state(instance):
        """
        ensure the running state is set
        """
        assert instance.state == "do_thing_running"

    x = get_thing()
    x.do_thing(assert_state)

    # ensure the target transition is set when the process is done
    assert x.state == x.CHOICES.done


def test_custom_name():
    """
    Ensures a transition state is set to the custom name
    """

    def assert_state(instance):
        """
        ensure the custom state is used
        """
        assert instance.state == "WEEE"

    x = get_thing()
    x.do_another_thing(assert_state)

    # ensure the target transition is set when the process is done
    assert x.state == x.CHOICES.done


def test_cant_call_while_running():
    """
    Ensures the transition cannot be called when already in a running state
    """

    def rerun(instance):
        """
        call the transition again
        """
        instance.do_thing(None)

    x = get_thing()

    with pytest.raises(TransitionNotAllowed):
        x.do_thing(rerun)

    # ensure the target transition is set when the process is done
    assert x.state == x.CHOICES.error


def test_disable_running_transition():
    """
    Ensures the running transition can be disabled
    """

    def assert_new(instance):
        """
        ensure the state is still the original state
        """
        assert instance.state == "new"

    x = get_thing()
    x.disable_running_state(assert_new)
