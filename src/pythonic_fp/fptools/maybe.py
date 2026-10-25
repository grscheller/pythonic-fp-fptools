# Copyright 2023-2026 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Callable, Iterable, Iterator
from typing import Final, cast, final, overload

from pythonic_fp.gadgets.sentinels.flavored import Sentinel

from ._recoverable import RECOVERABLE

__all__ = ['MayBe']

type _Sentinel = Sentinel[str]
_sentinel: Final[_Sentinel] = Sentinel('_MayBe_sentinel')


@final
class MayBe[D]:
    """
    .. admonition:: Maybe Monad

        Data structure wrapping a potentially missing item.

        - immutable semantics
        - can store any item of any type, including ``None``
        - hashable when contents are hashable

    """

    __slots__ = '_data', '_hash'
    __match_args__ = ('_data',)

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, data: D) -> None: ...

    def __init__(self, data: D | _Sentinel = _sentinel) -> None:
        """
        .. admonition:: init

            Initialize MayBe with 1 or 0 data items.

            :param data: Optional data item for the MayBe instance.

            .. important::

                - a ``MayBe`` is immutable once initialized
                - MayBe() is not a singleton

        """
        self._data: D | _Sentinel = data
        self._hash: int | _Sentinel = _sentinel

    def __hash__(self) -> int:
        """
        .. admonition:: hash

            :returns: The integer hash for the MayBe instance.
            :raises TypeError: When contained object is not hashable. 

            .. note::

                If contained item hashable, use its hash value in
                the hash calculation, otherwise the MayBe will be
                unhashable.

                - should be safe, the MayBe holds a reference to the item
                - only calculates its hash value when necessary
                - if contained value unhashable, MayBe will be unhashable

                .. tip::

                    Use MayBe instances as dict keys or set members
                    only when the type of contained data is hashable.

        """
        if self._hash is _sentinel:
            self._hash = hash((self._data,))
        return cast(int, self._hash)

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: equality comparison

            Compare MayBe instance to another object. Compare first
            by identity, then value.

            :returns: True only if other object is a MayBe with
                      a corresponding item, or both empty.

        """
        if not isinstance(other, type(self)):
            return False
        if self._data is other._data:
            return True
        return self._data == other._data

    def __getstate__(self) -> dict[str, object]:
        """
        .. admonition:: getstate

           Don't carry the hash value across pickling and spawn-based
           multiprocessing (the default on Windows and Mac-OS).

        """
        return {'_data': self._data, '_hash': _sentinel}

    def __setstate__(self, state: dict[str, object]) -> None:
        """
        .. admonition:: setstate

           Don't carry the hash value across pickling and spawn-based
           multiprocessing (the default on Windows and Mac-OS).

        """
        self._data = cast(D, state['_data'])
        self._hash = _sentinel

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            Truthy when not empty.

            :returns: True if not empty, False if empty.

        """
        return self._data is not _sentinel

    def __len__(self) -> int:
        """
        .. admonition:: len

            Zero or one items.

        """
        return 1 if self else 0

    def __iter__(self) -> Iterator[D]:
        """
        .. admonition:: iterate

           :yields: The contained item.

        """
        if self:
            yield cast(D, self._data)

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            :returns: A string to reproduce the MayBe.

            .. note::

                Return the strings

                - 'MayBe()' if empty
                - 'MayBe(repr_item)' if not empty

                Where ``repr_item = repr(item)``.

        """
        if self:
            return 'MayBe(' + repr(self._data) + ')'
        return 'MayBe()'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            :returns: A string meaningful to an end user.

            .. note::

                Return the strings

                - 'MayBe(str_item)' when not empty
                - 'MayBe()' when empty

                Where ``str_item = str(item)``.

        """
        if self:
            return 'MayBe(' + str(self._data) + ')'
        return 'MayBe()'

    @overload
    def get(self) -> D: ...
    @overload
    def get(self, alt: D) -> D: ...

    def get(self, alt: D | _Sentinel = _sentinel) -> D:
        """
        .. admonition:: get

            Return the item if it exists, otherwise an optional
            alternate item.

            :param alt: Optional alternative item to return if MayBe empty.
            :returns: The item if it exists.
            :raises ValueError: When an alternate item is not provided but needed.

            .. warning::

                Unsafe method get will raise ValueError() if the MayBe
                is empty and an alternate return item not provided.

                .. tip::

                    Best practice is to first check the MayBe in
                    a boolean context. Threadsafe since a MayBe
                    is immutable once created.

        """
        if self._data is not _sentinel:
            return cast(D, self._data)

        if alt is _sentinel:
            msg = 'MayBe: an alternate return item not provided to get method'
            raise ValueError(msg)
        return cast(D, alt)

    def map[U](self, f: Callable[[D], U]) -> MayBe[U]:
        """
        .. admonition:: map

            Map function f over the MayBe.

            :param f: Mapping function.
            :returns: A new MayBe instance if not empty,
                      otherwise itself.

        """
        if self:
            return MayBe(f(cast(D, self._data)))
        return cast(MayBe[U], self)

    def map_except[U](self, f: Callable[[D], U]) -> MayBe[U]:
        """
        .. admonition:: map_except

            Map function f over the MayBe.

            :param f: Mapping function.
            :returns: New MayBe instance if not empty and exception is
                      not thrown, an empty Maybe if exception is thrown,
                      otherwise itself.

            .. note::

                Swallows exceptions of types

                - LookupError
                - ValueError
                - ArithmeticError
                - RuntimeError

                Does not attempt to stop exceptions

                - TypeError
                - AttributeError
                - KeyboardInterrupt

        """
        if self:
            try:
                return MayBe(f(cast(D, self._data)))
            except RECOVERABLE:
                return MayBe()

        return cast(MayBe[U], self)

    def bind[U](self, f: Callable[[D], MayBe[U]]) -> MayBe[U]:
        """
        .. admonition:: bind

            Flatmap function f over the MayBe.

            :param f: Function to bind.
            :returns: A new MayBe instance if not empty,
                      otherwise itself.

        """
        if self:
            return f(cast(D, self._data))

        return cast(MayBe[U], self)

    def bind_except[U](self, f: Callable[[D], MayBe[U]]) -> MayBe[U]:
        """
        .. admonition:: bind_except

            Flatmap function f over the MayBe.

            :param f: Function to bind over contained values.
            :returns: A successfully bound MayBe[U], a propagated
            empty MayBe[U], or an empty MayBe[U] if an exception
            is raised.

            .. note::

                Swallows exceptions of types

                - LookupError
                - ValueError
                - ArithmeticError
                - RuntimeError

                Does not attempt to stop exceptions

                - TypeError
                - AttributeError
                - KeyboardInterrupt

        """
        if self:
            try:
                return f(cast(D, self._data))
            except RECOVERABLE:
                return MayBe()

        return cast(MayBe[U], self)

    @staticmethod
    def sequence[U](iterable_mb_u: Iterable[MayBe[U]]) -> MayBe[Iterable[U]]:
        """
        .. admonition:: MayBe.sequence

            Iterable[MayBe[U]] -> MayBe[Iterable[U]]

            :param sequence_mb_u: An Iterable of MayBe[U] values.
            :returns: Empty MayBe if one of the MayBe is empty,
                      otherwise a MayBe of an Iterable of the
                      contained values.

            .. note::

                A sequenced empty Iterable[MayBe[U]] would produce
                a MayBe of an empty Iterable, not an empty MayBe.

        """
        sequenced_list: list[U] = []

        for mb_u in iterable_mb_u:
            if mb_u:
                sequenced_list.append(mb_u.get())
            else:
                return MayBe()

        return MayBe(type(iterable_mb_u)(sequenced_list))
