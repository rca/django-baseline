from unittest import mock

from rest_framework import serializers, status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from bltestapp.models import Widget
from bltestapp.serializers import WidgetSerializer
from dynamic_fields.serializers import DynamicFieldSerializer


class TestExplicitPrefixSerializer(DynamicFieldSerializer, serializers.Serializer):
    first = serializers.CharField()
    last = serializers.CharField()

    class Meta:
        field_prefix = "ExplicitName"


class TestSerializer(DynamicFieldSerializer, serializers.Serializer):
    first = serializers.CharField()
    last = serializers.CharField()


class NestedTestSerializer(DynamicFieldSerializer):
    widget = WidgetSerializer()
    owner_name = serializers.CharField()


def test_nested_dynamic_fields():
    """
    ensure dynamic fields in nested serializers can be selected
    """
    widget = Widget(name="test widget", quantity=11)
    serializer = NestedTestSerializer(
        instance={
            "widget": widget,
            "owner_name": "test_name",
        },
        fields="widget_created,widget_name,widget_quantity",
    )

    assert sorted(list(serializer.data.keys())) == [
        "owner_name",
        "widget",
    ], serializer.data

    assert sorted(list(serializer.data["widget"].keys())) == [
        "created",
        "id",
        "name",
        "quantity",
    ], serializer.data


def test_serializer_prefix():
    """
    ensure the default prefix is created from the class name
    """
    serializer = TestSerializer()
    assert "test" == serializer.field_prefix


def test_explicit_serializer_prefix():
    """
    ensure the prefix is grabbed from the meta block
    """
    serializer = TestExplicitPrefixSerializer()
    assert "explicitname" == serializer.field_prefix


def test_existing_field_in_request_param():
    """
    ensure a field in the fields param that's already in the fields list does nothing
    """
    request_mock = mock.Mock(query_params=dict(fields="test_last"))

    serializer = TestSerializer(
        instance={"first": "test_first", "last": "test_last"},
        context={"request": request_mock},
    )

    data = serializer.data

    assert list(data.keys()) == ["first", "last"]


def test_no_request_param():
    """
    ensure fields specified in the request are honored
    """
    request_mock = mock.Mock(query_params=dict())

    serializer = TestSerializer(
        instance={"first": "test_first", "last": "test_last"},
        context={"request": request_mock},
    )

    data = serializer.data

    assert list(data.keys()) == ["first", "last"]


def test_dynamic_model_serializer_prefix():
    """
    Ensure the name comes from the model
    """
    serializer = WidgetSerializer()
    assert "widget" == serializer.field_prefix


def test_dynamic_model_fields():
    """
    ensure fields kwarg filters fields
    """
    widget = Widget(name="test widget", quantity=11)
    serializer = WidgetSerializer(widget, fields="widget_id,widget_name")

    assert sorted(list(serializer.data.keys())) == ["id", "name"], serializer.data


def test_default_model_fields():
    """
    ensure fields kwarg filters fields
    """
    widget = Widget(name="test widget", quantity=11)
    serializer = WidgetSerializer(widget)

    assert sorted(list(serializer.data.keys())) == ["id", "name"]


def test_api_request(db):
    widget = Widget.objects.create(name="test widget", quantity=11)

    client = APIClient()

    url = reverse("widgets-list")
    response = client.get(url, data={"fields": "widget_created,widget_name"})

    assert 200 == response.status_code

    assert sorted(list(response.data["results"][0].keys())) == ["created", "id", "name"]


def test_post_dynamic_field(db):
    client = APIClient()

    data = {
        "name": "test widget",
        "quantity": 100,
    }

    url = reverse("widgets-list")
    response = client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
