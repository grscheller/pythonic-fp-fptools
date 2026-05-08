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

__all__ = ['MayBe']

from collections.abc import Callable, Iterator, Sequence
from typing import cast, Final, final, overload
from pythonic_fp.gadgets.sentinels.flavored import Sentinel

type _Sentinel = Sentinel[str]
_sentinel: Final[_Sentinel] = Sentinel('_MayBe_sentinel')

@final
class MayBe[D]:
    """
    .. admonition:: Maybe Monad

        Data structure wrapping a potentially missing item.

        - immutable semantics
        - can store any item of any type, including ``None``
        - hashable

        .. note::

            If contained item not hashable, item's identity is
            used for hash calculation.

        .. warning::

            ``MayBe()`` is not a singleton.

    """

    __slots__ = ('_item', '_hash')
    __match_args__ = ('_item',)

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, item: D) -> None: ...

    def __init__(self, item: D | _Sentinel = _sentinel) -> None:
        """
        .. admonition:: initialize

            Setup ``MayBe`` with 1 or 0 items.

        """
        self._item: D | _Sentinel = item
        self._hash: int | None = None

    def __hash__(self) -> int:
        """
        .. admonition:: hashability

            If contained item hashable, use its hash value in
            the hash calculation, otherwise use item's identity.

            - should be safe, the ``MayBe`` holds a reference to the item
            - lazily calculates hash value, then caches it

        """
        if self._hash is None:
            try:
                self._hash = hash((self._item, type(self._item), _Sentinel))
            except TypeError:
                self._hash = hash((id(self._item), type(self._item), _Sentinel))

        return self._hash

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            Truthy when not empty.

        """
        return self._item is not _sentinel

    def __len__(self) -> int:
        """
        .. admonition:: len

            Zero or one items.

        """
        return 1 if self else 0

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: equality comparison

            Compare ``MayBe`` to another object.

            - compare first by identity, then value

        """
        if not isinstance(other, type(self)):
            return False
        if self._item is other._item:
            return True
        if self._item == other._item:
            return True
        return False

    def __iter__(self) -> Iterator[D]:
        """
        .. admonition:: iterate

            Iterate ``item`` if present.

        """
        if self:
            yield cast(D, self._item)

    def __repr__(self) -> str:
        """
        .. admonition:: representation string

            Return the strings

            - 'MayBe(repr_item)' if not empty
            - 'MayBe()' if empty

            Where ``repr_item = repr(item)``.

        """
        if self:
            return 'MayBe(' + repr(self._item) + ')'
        return 'MayBe()'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Return the strings

            - 'MayBe(str_item)' when not empty
            - 'MayBe()' when empty

            Where ``str_item = str(item)``.

        """
        if self:
            return 'MayBe(' + str(self._item) + ')'
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

            .. warning::

                Unsafe method ``get`` will raise ``ValueError`` if the
                ``MayBe`` is empty and an ``alt`` return item not provided.

                .. tip::

                    Best practice is to first check the ``MayBe`` in
                    a boolean context.

        :param alt: Optional alternative item to return if``MayBe`` empty.
        :returns: The item if it exists.
        :raises ValueError: When an alternate item is not provided but needed.

        """
        if self._item is not _sentinel:
            return cast(D, self._item)

        if alt is _sentinel:
            msg = 'MayBe: an alternate return item not provided to get method'
            raise ValueError(msg)
        return cast(D, alt)

    def map[U](self, f: Callable[[D], U]) -> 'MayBe[U]':
        """
        .. admonition:: Map

            Map function ``f`` over the ``MayBe``.

        :param f: Function used for the map.
        :returns: A new ``MayBe`` if not empty, otherwise ``self``.

        """
        if self:
            return MayBe(f(cast(D, self._item)))
        return cast(MayBe[U], self)

    def bind[U](self, f: 'Callable[[D], MayBe[U]]') -> 'MayBe[U]':
        """
        .. admonition:: Bind

            Flatmap function ``f`` over the contained item, if it exists.

        :param f: Function to bind.
        :returns: A new ``MayBe`` if not empty, otherwise ``self``.

        """
        return f(cast(D, self._item)) if self else cast(MayBe[U], self)

    @staticmethod
    def sequence[U](sequence_mb_u: 'Sequence[MayBe[U]]') -> 'MayBe[Sequence[U]]':
        """
        .. admonition:: Sequence

            ``Sequence[MayBe[U]]`` -> ``MayBe[Sequence[U]]``

            If all ``MayBe`` have items, then return an ``MayBe``
            of the ``Sequence`` of contained items. Otherwise return
            an empty ``Maybe``.

        """
        sequenced_list: list[U] = []

        for mb_u in sequence_mb_u:
            if mb_u:
                sequenced_list.append(mb_u.get())
            else:
                return MayBe()

        sequenced_items = type(sequence_mb_u)(sequenced_list)  # type: ignore
        return MayBe(cast(Sequence[U], sequenced_items))
