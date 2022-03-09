"""
Module defining logic to dynamically select fields to return
"""
import functools
import typing

from rest_framework import serializers


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

        self._setup_fields(fields, **kwargs)

    def _setup_fields(self, fields=None, **kwargs):
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
            ), "fields listed in `dynamic_fields` must be in `fields`"

            output_fields = dynamic_fields

        # look for fields in the request context when fields is not passed in as kwargs
        if fields is None:
            request = kwargs.get("context", {}).get("request")
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

        # now pop any fields that are not in the `output_fields` var
        for name in original_field_names - output_fields:
            self.fields.pop(name)

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
