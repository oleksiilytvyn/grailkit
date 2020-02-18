# -*- coding: UTF-8 -*-
"""Core types and widely used components.

:copyright: (c) 2017-2020 by Oleksii Lytvyn (http://alexlitvin.name).
:license: MIT, see LICENSE for more details.
"""
from typing import Union, Callable, Any, List, Dict, Tuple, Type

import weakref
import logging

from grailkit.util import object_type

logging.getLogger(__name__).addHandler(logging.NullHandler())

_Callable = Union[Callable, Type]


class Signal(object):
    """Callback mechanism for DNA objects.

    This class uses weak references to callbacks, so methods can be deleted
    if no references exists
    """

    def __init__(self, *args):
        """Create signal.

        Args:
            *args: list of types, used as template of arguments
        """
        self._args: List[type] = [object_type(x) for x in args]
        self._fns: Dict[str, Tuple[Any, Any]] = {}
        self._flush_keys: List[str] = []

    def __len__(self):
        """Return number of connected slots."""
        return len(self._fns)

    def __bool__(self):
        """Return True and prevent from converting to False when number of slots is 0."""
        return True

    @property
    def template(self) -> str:
        """Return string template of types of signal."""
        return ", ".join("<%s>" % str(x.__name__) for x in self._args)

    def connect(self, fn: _Callable, name: str = "") -> None:
        """Add function to list of callbacks.

        Args:
            fn (callable): function to call on emit
            name (str): give name to slot
        """
        if not callable(fn):
            raise ValueError("Given object is not callable")

        ref = self._wrap(fn)

        if len(name) == 0:
            name = str(len(self._fns))

        self._fns[name] = ref

    def disconnect(self, fn: _Callable):
        """Remove function from list, if it previously added to it.

        Args:
            fn (callable): function to remove
        """
        found_key = None

        for key, value in self._fns.items():
            if value[0] and fn == value[1]():
                found_key = key

                break

        if found_key:
            del self._fns[found_key]

    def emit(self, *args, name: str = "", **kwargs):
        """Emit signal.

        If `name` argument was given, only slot with this name will be called
        otherwise all slots will be called

        Args:
            *args: arguments to pass to callbacks
            name (str): give name of slot to be called
            **kwargs: keyword arguments to pass to callbacks
        """
        if name and name in self._fns:
            return self._call(name, *args, **kwargs)

        for key in self._fns:
            self._call(key, *args, **kwargs)

        # remove dead references
        self._flush()

    def _call(self, name: str, *args, **kwargs):
        """Call method, if reference is dead then flush.

        Args:
            name (str): slot name
            *args (list): list of argument to be passed
            **kwargs (dict): dict of arguments to be passed
        """
        ref = self._fns[name]
        obj = ref[0]
        fun = ref[1]

        try:
            # bound
            if callable(obj) and obj() and callable(fun):
                callback = getattr(obj(), fun().__name__)
                callback(*args, **kwargs)
            # unbound
            elif obj is None and fun:
                fun(*args, **kwargs)
            # non exists
            else:
                self._flush_keys.append(name)
        # Error caused by callback
        except RuntimeError as e:
            logging.warning("Slot %s removed because of exception raised.\n "
                            "Original exception was: %s" %
                            (str(fun), str(e)))

            self._flush_keys.append(name)

    def _flush(self):
        """Delete dead references."""
        for key in set(self._flush_keys):
            if key in self._fns:
                del self._fns[key]

        self._flush_keys = []

    @classmethod
    def _wrap(cls, fn: _Callable) -> Tuple[Any, Any]:
        """Return tuple with parent object and method.

        Args:
            fn (callable): callable to wrap with weakref
        """
        if hasattr(fn, '__self__') and hasattr(fn, '__func__'):
            return weakref.ref(getattr(fn, '__self__')), weakref.ref(getattr(fn, '__func__'))
        else:
            return None, fn


class Signalable(object):
    """Like a Signal but with messages and bundles."""

    def __init__(self):
        """Create object that can connect Signals."""
        self.__slots = {}
        self.__bundle_slots = Signal()

    def __bool__(self):
        """Return True."""
        return True

    def __len__(self):
        """Return number of registered callbacks."""
        return self.callbacks_length

    @property
    def callbacks_length(self) -> int:
        """Return number of registered callbacks."""
        return sum(len(v) for k, v in self.__slots.items()) + len(self.__bundle_slots)

    def connect(self, message: str, fn: _Callable) -> None:
        """Connect listener `fn` to slot `message`.

        Args:
            message (str): slot name
            fn (callable): function to call
        Raises:
            ValueError if at least one of arguments is not supported
        """
        if not isinstance(message, str):
            raise ValueError("Can't connect to slot '%s', given value is not of type string"
                             % message)

        if not callable(fn):
            raise ValueError("Given function is not callable.")

        if message not in self.__slots:
            self.__slots[message] = Signal()

        self.__slots[message].connect(fn)

    def disconnect(self, message: str, fn: _Callable) -> None:
        """Disconnect listener from slot.

        Args:
            message (str): slot name
            fn (callable): function to call
        """
        if message in self.__slots:
            self.__slots[message].disconnect(fn)

    def emit(self, message: str, *args) -> None:
        """Trigger all listeners of message.

        Args:
            message (str): slot name
            *args: list of arguments
        """
        if message in self.__slots:
            self.__slots[message].emit(*args)

    def connect_bundle(self, fn: _Callable) -> None:
        """Connect a bundle listener.

        Args:
            fn (callable): callback listener
        """
        self.__bundle_slots.connect(fn)

    def disconnect_bundle(self, fn: _Callable) -> None:
        """Remove bundle listener.

        Args:
            fn (callable): callback listener
        """
        self.__bundle_slots.disconnect(fn)

    def emit_bundle(self, bundle: List[str]) -> None:
        """Emit bundle of messages.

        Args:
            bundle (list): bundle of messages
        """
        self.__bundle_slots.emit(bundle)
