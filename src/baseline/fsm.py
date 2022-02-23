import functools
import typing

Callable = typing.Callable
Iterable = typing.Iterable

from django_fsm import transition as fsm_transition

if typing.TYPE_CHECKING:
    from django.db import models


def get_running_state_name(func: "Callable") -> str:
    """
    Returns the name of the running state
    Args:
        func: the transition function being wrapped

    Returns:
        str: the running state name
    """
    func_name = func.__name__

    return f"{func_name}_running"


def set_transition_state(self: "models.Model", func: "Callable") -> None:
    """
    Sets the state to the running state for the given transition function

    This is used to switch the state to an intermediate value while a transition is running

    NOTE: this is used internally and should not be used otherwise; it sort of sidesteps
    transitions being in control of the state field.
    Args:
        self: the model instance
        func: the function to derive the running state from
    """
    self.state = get_running_state_name(func)
    self.save()


def transition(
    field,
    source="*",
    target=None,
    on_error=None,
    conditions=None,
    permission=None,
    custom=None,
):
    """
    Wrapper around Django FSM's transition() decorator

    This implementation will set the state to an intermediary *_running state,
    where the name of the function is used as the name of the state.

    Going to an intermediate state has 2 side effects:

    - when the state field is being used to interactively display the object's state,
      the UI will show that processing is happening.

    - the transition function can only be called once, since the intermediate
      state is not in the source list.  it's a weak'ish way to mitigate a
      race condition where the transition is called multiple times from multiple
      processes.  NOTE: a more dedicated locking mechanism should be used to
      mitigate race conditions.

    Args: all the same args as Django FSM's transition
    """
    conditions = conditions or []
    custom = custom or {}

    def decorator(fn):
        fsm_transition_result = fsm_transition(
            field,
            source=source,
            target=target,
            on_error=on_error,
            conditions=conditions,
            permission=permission,
            custom=custom,
        )

        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            set_transition_state(self, fn)
            return fn(self, *args, **kwargs)

        wrapped = fsm_transition_result(wrapper)

        return wrapped

    return decorator
