from django.db import models
from django_fsm import FSMField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from baseline.fsm import transition
from baseline.models.named_model import NamedModel
from baseline.models.uuid_model import UUIDModel


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

    @transition(
        state,
        source=CHOICES.new,
        target=CHOICES.done,
        on_error=CHOICES.error,
        running_state="WEEE",
    )
    def do_another_thing(self, callable):
        """
        Call the callable with the instance object

        Args:
            callable: the callable to run
        """
        callable(self)

    @transition(
        state,
        source=CHOICES.new,
        target=CHOICES.done,
        on_error=CHOICES.error,
        set_running_state=False,
    )
    def disable_running_state(self, callable):
        """
        Call the callable with the instance object

        Args:
            callable: the callable to run
        """
        callable(self)


class Widget(UUIDModel, NamedModel, TimeStampedModel, models.Model):
    """
    A widget
    """

    quantity = models.PositiveIntegerField()
