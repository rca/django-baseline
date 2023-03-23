import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from baseline.serializers.auth import LoginSerializer
from baseline.serializers.user_serializer import UserSerializer
from baseline.utils import set_cookie

User = get_user_model()


class AuthViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for logging in a user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        """
        Override the create endpoint
        """

        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # get or create the user's auth token
        user = serializer.user

        auth_token, _ = Token.objects.get_or_create(user=user)
        key = auth_token.key

        user_serializer = UserSerializer(instance=user)

        response = Response(user_serializer.data)
        set_cookie(response, "auth_token", key)

        return response

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def logout(self, request, *args, **kwargs):
        response = Response({"message": "ok"})

        soon = timezone.now() + datetime.timedelta(seconds=1)
        set_cookie(response, "auth_token", "", expires=soon)

        return response
