from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Widget
from .serializers import WidgetSerializer


class WidgetFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Widget
        fields = ("name", "quantity")


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = [AllowAny]

    filterset_class = WidgetFilter
    search_fields = ["name"]
