from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from baseline.serializers.auth import LoginSerializer
from baseline.utils import set_cookie

User = get_user_model()


class LoginViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for logging in a user
    """

    permission_classes = [AllowAny]

    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override the create endpoint
        """

        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # get or create the user's auth token
        user = serializer.user

        auth_token, _ = Token.objects.get_or_create(user=user)
        key = auth_token.key

        response = Response({"message": "okay"})
        set_cookie(response, "auth", key)

        return response
