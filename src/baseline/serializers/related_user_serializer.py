from .user_serializer import UserSerializer as BaseUserSerializer, User


class RelatedUserSerializer(BaseUserSerializer):
    """
    Serializer to represent a FK to a user that already exists
    """

    def to_internal_value(self, data):
        """
        Gets the user object from the database

        By doing this, the user will not be created, but instead an existing user will be referenced
        """
        return User.objects.get(username=data)
