from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from baseline.serializers.user_serializer import UserSerializer

User = get_user_model()


class AccountViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for getting logged in account details
    """

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        if pk == "self":
            pk = self.request.user.pk
            self.kwargs.update(dict(pk=pk))

        return super().get_object()
