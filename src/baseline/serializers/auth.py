from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
