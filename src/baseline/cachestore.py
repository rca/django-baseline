"""
helpers for dealing with temporary storage in cache
"""
import typing
import uuid

from django.core.cache import cache

Nonce = typing.AnyStr


def get_nonce() -> Nonce:
    """
    Returns a one-time use token
    """
    return str(uuid.uuid4())


class CacheStore:
    """
    Class to store and retrieve data in cache using a nonce
    """

    @staticmethod
    def get(nonce: Nonce) -> typing.Any:
        """
        Returns the item stored at the nonce address
        """
        return cache.get(nonce)

    @staticmethod
    def set(data: typing.Any) -> Nonce:
        """
        Places the given data into cache using a unique nonce

        Args:
            data: the data to store

        Returns:
            Nonce: the key where the data is stored
        """
        nonce = get_nonce()

        cache.set(nonce, data)

        return nonce
