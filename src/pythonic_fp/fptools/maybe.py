# Copyright 2023-2025 Geoffrey R. Scheller
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

"""Pythonic FP - Maybe Monad"""

__all__ = ['MayBe']

from collections.abc import Callable, Iterator, Sequence
from typing import cast, Final, overload, TypeVar
from pythonic_fp.sentinels.flavored import Sentinel


class MayBe[D]:
    """Maybe monad, data structure wrapping a potentially missing value.

    Immutable semantics

    - can store any item of any type, including ``None``

      - with one hidden implementation dependent exception

    - immutable semantics, therefore covariant

    .. warning::

        Hashability invalidated if contained value is not hashable.

    """

    __slots__ = ('_value',)
    __match_args__ = ('_value',)

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, value: D) -> None: ...

    def __init__(self, value: D | Sentinel[str] = Sentinel('_MayBe_str')) -> None:
        self._value: D | Sentinel[str] = value

    def __hash__(self) -> int:
        return hash((Sentinel('_MayBe_str'), self._value))

    def __bool__(self) -> bool:
        return self._value is not Sentinel('_MayBe_str')

    def __iter__(self) -> Iterator[D]:
        if self:
            yield cast(D, self._value)

    def __repr__(self) -> str:
        if self:
            return 'MayBe(' + repr(self._value) + ')'
        return 'MayBe()'

    def __len__(self) -> int:
        return 1 if self else 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self._value is other._value:
            return True
        if self._value == other._value:
            return True
        return False

    @overload
    def get(self) -> D: ...
    @overload
    def get(self, alt: D) -> D: ...

    def get(self, alt: D | Sentinel[str] = Sentinel('_MayBe_str')) -> D:
        """Return the contained value if it exists, otherwise an alternate value.

        .. warning::

            Unsafe method ``get``. Will raise ``ValueError`` if MayBe empty
            and an alt return value not given. Best practice is to first check
            the MayBe in a boolean context.

        :param alt: an "optional" alternative value to return
        :raises ValueError: when an alternate value is not provided but needed

        """
        _sentinel: Final[Sentinel[str]] = Sentinel('_MayBe_str')
        if self._value is not _sentinel:
            return cast(D, self._value)
        if alt is _sentinel:
            msg = 'MayBe: an alternate return type not provided'
            raise ValueError(msg)
        return cast(D, alt)

    def map[U](self, f: Callable[[D], U]) -> 'MayBe[U]':
        """Map function `f` over contents."""

        if self:
            return MayBe(f(cast(D, self._value)))
        return cast(MayBe[U], self)

    def bind[U](self, f: 'Callable[[D], MayBe[U]]') -> 'MayBe[U]':
        """Flatmap ``MayBe`` with function ``f``."""
        return f(cast(D, self._value)) if self else cast(MayBe[U], self)

    @staticmethod
    def sequence[U](sequence_mb_u: 'Sequence[MayBe[U]]') -> 'MayBe[Sequence[U]]':
        """
        Sequence a mutable indexable of type ``Sequence[MayBe[U]]``.

        :param sequence_mb_u: Sequence of type ``Maybe[U]``
        :returns: MayBe of Sequence subtype if all values non-empty, otherwise an empty Maybe

        """
        sequenced_items: list[U] = []

        for mb_u in sequence_mb_u:
            if mb_u:
                sequenced_items.append(mb_u.get())
            else:
                return MayBe()

        return MayBe(type(sequence_mb_u)(sequenced_items))  # type: ignore
