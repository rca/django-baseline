"""
Module defining logic to dynamically select fields to return
"""
import functools
import typing

from rest_framework import serializers

if typing.TYPE_CHECKING:
    from baseline.types import StringList


# noinspection PyAbstractClass
class DynamicFieldSerializer(serializers.Serializer):
    """
    Class that dynamically selects fields based on a `fields` param

    This serializer looks for a `fields` parameter and will select
    the fields that are returned.

    This serializer works by look for field names prefixed by the serializer's
    model name (for model serializers) or the name of the serializer itself
    (for example, a serializer named TestSerializer would have a prefix of
    `test`, which is the lowercased name of the class with `serializer` removed).
    """

    def __init__(self, *args, fields=None, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        self.dynamic_fields = fields

    @property
    @functools.lru_cache()
    def field_prefix(self) -> str:
        """
        Returns the string that fields for this serializer are prefixed with
        """
        field_prefix = self.get_meta_attr("field_prefix")
        if field_prefix is None:
            field_prefix = self.__class__.__name__.replace("Serializer", "").lower()
        else:
            field_prefix = field_prefix.lower()

        return field_prefix

    def get_dynamic_fields(self, fields: str) -> set:
        """
        Returns the fields in the given list corresponding to this serializer
        Args:
            fields: the full list of fields requested

        Returns:
            set: the fields corresponding to this serializer
        """
        fields_list = fields.split(",")

        dynamic_fields = []
        for field in fields_list:
            field_split = field.split("_", 1)
            if len(field_split) != 2:
                continue

            serializer_name, field_name = field_split
            if serializer_name != self.field_prefix:
                continue

            dynamic_fields.append(field_name)

        return set(dynamic_fields)

    def get_excluded_fields(self, fields: "StringList" = None, **kwargs) -> list:
        # the original set of field names
        original_field_names = set(self.fields)

        # keep track of the fields that will be output
        output_fields = set(self.fields)

        # check to see if `dynamic_fields` is defined in the Meta block
        # when found, this becomes the set of fields that will be output
        dynamic_fields = set(self.get_meta_attr("dynamic_fields") or [])
        if dynamic_fields:
            # make sure that any field listed in the default fields is
            # actually defined in the fields list; otherwise blow up
            assert (
                len(dynamic_fields - output_fields) == 0
            ), f"fields listed in `dynamic_fields` must be in `fields`, dynamic_fields={dynamic_fields}, output_fields={output_fields}"

            output_fields = dynamic_fields

        # look for fields in the request context when fields are not passed in as kwargs
        fields = fields or self.get_requested_fields()
        if fields is None:
            request = self.context.get("request")
            if request:
                fields = request.query_params.get("fields", "")

        if fields:
            dynamic_fields = self.get_dynamic_fields(fields)

            # ensure that all the fields requested are in the original set of fields
            assert (
                len(dynamic_fields - original_field_names) == 0
            ), "requested fields must be defined in `fields`"

            # re-add any fields that have been requested
            output_fields = output_fields.union(dynamic_fields)

        # create a list of the fields that are excluded in this request
        excluded_fields = list(original_field_names - output_fields)

        return excluded_fields

    def get_meta_attr(self, name: str) -> typing.Any:
        """
        Returns the requested attribute from the Meta block, if it exists

        Args:
            name: the name of the desired attribute

        Returns:
            the attribute's value
        """
        meta = getattr(self, "Meta", None)
        if meta:
            return getattr(meta, name, None)

    def get_requested_fields(self):
        """
        Returns the fields that have been requested

        This looks up the serializer stack in case it's a nested serializer
        """
        requested_fields = self.dynamic_fields
        if not requested_fields:
            if self.parent and hasattr(self.parent, "get_requested_fields"):
                requested_fields = self.parent.get_requested_fields()

        return requested_fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        excluded_fields = self.get_excluded_fields()

        for name in excluded_fields:
            representation.pop(name)

        return representation
