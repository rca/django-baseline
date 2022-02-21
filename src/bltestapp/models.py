from django.db import models

from model_utils.models import TimeStampedModel

from baseline.models.named_model import NamedModel
from baseline.models.uuid_model import UUIDModel


class Widget(UUIDModel, NamedModel, TimeStampedModel, models.Model):
    """
    A widget
    """

    quantity = models.PositiveIntegerField()
