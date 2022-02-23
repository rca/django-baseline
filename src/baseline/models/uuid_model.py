import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    This abstract base class provides id field on any model that inherits from it
    which will be the primary key.

    This is 99% ripped from model_utils, however, rather than specifying a version
    this sets a default value, which plays nicely with history records
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True

    @property
    def pk_s(self) -> str:
        """
        Return a string version of the UUID pk
        """
        return str(self.id)
