import datetime
import uuid

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from two_factor import utils

from baseline.serializers.auth import LoginSerializer, MFASerializer
from baseline.utils import get_user_serializer, set_cookie

from ..utils import get_mfa_cache_key

User = get_user_model()
UserSerializer = get_user_serializer()


def get_logged_in_response(user: "User", mfa_verified: bool = None):
    """
    Returns response when user is logged in properly

    Args:
        user: the user that is logged in
        mfa_verified: whether mfa was verified
    """
    auth_token, _ = Token.objects.get_or_create(user=user)
    key = auth_token.key

    user_serializer = UserSerializer(instance=user)

    response = Response(user_serializer.data)
    set_cookie(response, "auth_token", key)

    message = f"login, user={user}, user.pk={user.pk}"
    if mfa_verified:
        message = f"{message}, mfa_verified={mfa_verified}"

    print(message)

    return response


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

        cache_uuid = str(uuid.uuid4())
        cache_key = get_mfa_cache_key(cache_uuid)

        cache.set(cache_key, {"user_id": user.pk}, 300)

        # check to see if this user has a MFA device setup and enabled
        mfa_device = utils.default_device(user)
        if mfa_device and mfa_device.confirmed:
            response_body = {
                "mfa_required": True,
                "mfa_devices": [mfa_device._meta.object_name],
                "mfa_state": cache_uuid,
            }

            # use status 202 in order to distinguish between fully-authenticated,
            # "here's your auth token," and, "your username/password was good,
            # but we still need to bug you for an MFA challenge response."
            return Response(response_body, status=status.HTTP_202_ACCEPTED)

        return get_logged_in_response(user)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def logout(self, request, *args, **kwargs):
        response = Response({"message": "ok"})

        soon = timezone.now() + datetime.timedelta(seconds=1)
        set_cookie(response, "auth_token", "", expires=soon)

        return response

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[AllowAny],
        url_name="verify-mfa",
    )
    def verify_mfa(self, request, *args, **kwargs):
        """
        verify the MFA response
        """

        serializer = MFASerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return get_logged_in_response(serializer.user, mfa_verified=True)
