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

"""
.. admonition:: Maybe Monad

"""

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

          - with one hidden implementation dependent exception

        - hashable

        .. note::

            If contained item is not hashable, item's identity is
            used in the hash calculation.

    """

    __slots__ = ('_item', '_hash')
    __match_args__ = ('_item',)

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, item: D) -> None: ...

    def __init__(self, item: D | _Sentinel = _sentinel) -> None:
        """
        .. admonition:: Initializer

            Initialize ``MayBe`` with 0 or 1 items.

        :param item: Optional item to include.

        """
        self._item: D | _Sentinel = item
        self._hash: int | None = None

    def __hash__(self) -> int:
        """
        .. admonition:: Hashability

            If contained item hashable, use its hash value in
            the hash calculation, otherwise use item's identity.

        """
        if self._hash is None:
            try:
                self._hash = hash((self._item, type(self._item), _Sentinel))
            except TypeError:
                self._hash = hash((id(self._item), type(self._item), _Sentinel))

        return self._hash

    def __bool__(self) -> bool:
        """
        .. admonition:: Bool

            - truthy when item present
            - falsy when item missing

        :returns: ``True`` when not empty, ``False`` otherwise.

        """
        return self._item is not _sentinel

    def __len__(self) -> int:
        """
        .. admonition:: Length

            Number of items in the ``MayBe``.

        :returns: 1 if item present, 0 if missing.

        """
        return 1 if self else 0

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: Equality comparison

            Compare ``MayBe`` to another object.

        :param other: The object to be compared.
        :returns: ``True`` if ``other`` is another ``MayBe`` whose
                  contents compare as equal to the corresponding
                  contents of the ``MayBe``, otherwise ``False``.

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
        .. admonition:: Iterate

            Iterate ``item`` if present.

        """
        if self:
            yield cast(D, self._item)

    def __repr__(self) -> str:
        """
        .. admonition:: Representation string

            Construct the string

            - 'MayBe(repr_item)' when not empty
            - 'MayBe()` when empty

            where ``repr_item = repr(item)``.

        :returns: A string to reproduce the ``MayBe``. 

        """
        if self:
            return 'MayBe(' + repr(self._item) + ')'
        return 'MayBe()'

    def __str__(self) -> str:
        """
        .. admonition:: User string

            Construct the string

            - 'MayBe(str_item)' when not empty
            - 'MayBe()` when empty

            where ``str_item = str(item)``.

        :returns: A string to reproduce the ``MayBe``. 

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
        .. admonition:: Get item

        Return the contained item if it exists, otherwise an alternate item.

        .. warning::

            Unsafe method ``get`` will raise ``ValueError`` if the
            ``MayBe`` is empty and an ``alt`` return item not provided.

            .. tip::

                Best practice is to first check the ``MayBe`` in
                a boolean context.

        :param alt: an "optional" alternative item to return
        :returns: the contained item if it exists
        :raises ValueError: when an alternate item is not provided but needed

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

            Map function `f` over contents.

        :param f: Function used to map over items.
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
        :returns: A new ``MayBe`` if not empty, otherwise itself.

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

        :param sequence_mb_u: ``Sequence[MayBe[U]]``
        :returns: ``MayBe`` of a ``Sequence`` subtype of items if
                  all the sequence elements are non-empty, otherwise
                  an empty ``MayBe[U]``.

        """
        sequenced_list: list[U] = []

        for mb_u in sequence_mb_u:
            if mb_u:
                sequenced_list.append(mb_u.get())
            else:
                return MayBe()

        sequenced_items = type(sequence_mb_u)(sequenced_list)  # type: ignore
        return MayBe(cast(Sequence[U], sequenced_items))
