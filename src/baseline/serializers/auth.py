from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..utils import get_mfa_cache_key

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    Serializer to validate incoming login data
    """

    user = None

    username = serializers.CharField()
    password = serializers.CharField()

    def is_valid(self, *, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)

        # if the required fields were passed in, check to see if the password is correct
        if is_valid:
            request = self.context["request"]
            try:
                user = authenticate(
                    request,
                    username=self.validated_data["username"],
                    password=self.validated_data["password"],
                )
            except Exception as exc:
                raise exc

            if not user:
                errors = dict(login_error="bad username or password")

                if not raise_exception:
                    self._errors.update(errors)
                else:
                    raise ValidationError(errors)

        self.user = user

        return is_valid


class MFASerializer(serializers.Serializer):
    """
    Serializer to validate incoming MFA response
    """

    user = None

    challenge_response = serializers.CharField()
    mfa_state = serializers.CharField()

    def is_valid(self, *, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)

        errors = []
        user = None

        # if the required fields were passed in, check to see if the password is correct
        if is_valid:
            cache_key = get_mfa_cache_key(self.validated_data["mfa_state"])
            cache_data = cache.get(cache_key)
            if cache_data:
                user = User.objects.get(pk=cache_data["user_id"])
                device = TOTPDevice.objects.get(user=user, name="default")
                verified = device.verify_token(
                    self.validated_data["challenge_response"]
                )

                if not verified:
                    errors.append("incorrect challenge response")
            else:
                errors.append("state not found")

            if errors:
                if raise_exception:
                    raise ValidationError(errors)

        if is_valid:
            self.user = user

        return is_valid
