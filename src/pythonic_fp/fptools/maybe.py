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

    """

    __slots__ = ('_item', '_hash')
    __match_args__ = ('_item',)

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, item: D) -> None: ...

    def __init__(self, item: D | _Sentinel = _sentinel) -> None:
        """
        .. admonition:: init

            Initialize MayBe with 1 or 0 items.

            :param item: Optional item for the MayBe instance.

            .. important::

                - A ``MayBe`` is immutable once initialized.
                - ``MayBe()`` is not a singleton.

        """
        self._item: D | _Sentinel = item
        self._hash: int | None = None

    def __hash__(self) -> int:
        """
        .. admonition:: hash

            If contained item hashable, use its hash value in
            the hash calculation, otherwise use item's identity.

            - should be safe, the MayBe holds a reference to the item.
            - Lazily calculates hash value, then caches it.

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

            :returns: True if not empty, False if empty.

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

            Compare MayBe instance to another object. Compare first
            by identity, then value.

            :returns: True only if other object is a MayBe with
                      a corresponding item, or both empty.
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

           :yields: The contained item if non-empty.

        """
        if self:
            yield cast(D, self._item)

    def __repr__(self) -> str:
        """
        .. admonition:: repr string

            Return the strings

            - 'MayBe()' if empty
            - 'MayBe(repr_item)' if not empty

            Where ``repr_item = repr(item)``.

            :returns: A string to reproduce the MayBe.

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

            :returns: A string meaningful to an end user.

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

            :param alt: Optional alternative item to return if MayBe empty.
            :returns: The item if it exists.
            :raises ValueError: When an alternate item is not provided but needed.

            .. warning::

                Unsafe method get will raise ValueError if the MayBe
                is empty and an alternate return item not provided.

                .. tip::

                    Best practice is to first check the MayBe in
                    a boolean context.

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

            Map function f over the MayBe.

            :param f: Function used for the map.
            :returns: A new MayBe instance if not empty,
                      otherwise itself.

        """
        if self:
            return MayBe(f(cast(D, self._item)))
        return cast(MayBe[U], self)

    def bind[U](self, f: 'Callable[[D], MayBe[U]]') -> 'MayBe[U]':
        """
        .. admonition:: Bind

            Flatmap function f over the MayBe.

            :param f: Function to bind.
            :returns: A new MayBe instance if not empty,
                      otherwise itself.

        """
        return f(cast(D, self._item)) if self else cast(MayBe[U], self)

    @staticmethod
    def sequence[U](sequence_mb_u: 'Sequence[MayBe[U]]') -> 'MayBe[Sequence[U]]':
        """
        .. admonition:: Sequence

            ``Sequence[MayBe[U]]`` -> ``MayBe[Sequence[U]]``

            :param sequence_mb_u: A ``Sequence`` of ``MayBe`` of the same type.
            :returns: Empty ``MayBe`` if one of the ``MayBe`` is empty.

            ,, note::

                A sequenced empty ``Sequence[MayBe[U]]`` would produce
                a ``MayBe`` of an empty ``Sequence``, not an empty
                ``MayBe``.

                .. tip

                    If above is confusing, replace the term "Sequence"
                    above with a concrete example of a ``Sequence``
                    like ``list`` or ``tuple``.


        """
        sequenced_list: list[U] = []

        for mb_u in sequence_mb_u:
            if mb_u:
                sequenced_list.append(mb_u.get())
            else:
                return MayBe()

        sequenced_items = type(sequence_mb_u)(sequenced_list)  # type: ignore
        return MayBe(cast(Sequence[U], sequenced_items))
