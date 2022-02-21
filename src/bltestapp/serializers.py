from rest_framework import serializers

from dynamic_fields.serializers import DynamicFieldSerializer

from bltestapp.models import Widget


class WidgetSerializer(DynamicFieldSerializer, serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ["id", "name", "created", "modified", "quantity"]
        dynamic_fields = ["id", "name"]
