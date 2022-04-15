import time

from contextlib import AbstractContextManager
from types import TracebackType
from typing import Type


class TimeContext(AbstractContextManager):
    """
    Context manager for timing blocks of code
    """

    def __init__(
        self,
        message: str = None,
        extra_newline: bool = False,
    ) -> None:
        """

        Args:
            message: when a message is given, it will be printed when the context block ends
            extra_newline: whether to print a newline after the message
        """
        super().__init__()

        self.message = message
        self.extra_newline = extra_newline

        self.start = time.time()
        self.end = None
        self.delta = None

    def __enter__(self):
        return self

    def __exit__(
        self,
        __exc_type: Type[BaseException],
        __exc_value: BaseException,
        __traceback: TracebackType,
    ) -> bool:
        self.end = time.time()
        self.delta = self.end - self.start

        if self.message:
            print(f"{self.message}: {self.delta}")
            if self.extra_newline:
                print()

        return False
