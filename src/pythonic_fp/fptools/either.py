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
.. admonition:: The Either monad

    Data structure semantically containing either
    a "left" value or a "right" value, but not both.

    - Module implements a left biased either monad

      - left value is intended for the "expected" result
      - right value gives information on something "exceptional"

    - left and right values can be the same or different types
    - in a boolean context

      - left values are truthy
      - right values are falsy

    .. tip::

        Happy path without exceptions.

        Instead of catching an exception whenever the "happy path"
        fails, process the left values and either deal with or
        propagate right values.

    .. tip::

        Right ``Either`` instances can be used as sentinel values.

"""

__all__ = ['Either', 'EitherBool', 'LEFT', 'RIGHT']

from collections.abc import Callable, Iterator, Sequence
from typing import cast, Final, final, overload
from pythonic_fp.booleans.subtypable import SBool
from .maybe import MayBe


@final
class EitherBool(SBool):
    """
    .. admonition:: Type for ``LEFT`` and ``RIGHT`` singleton flags

        Boolean-like type for signaling the ``Either`` initializer
        to make a left or right ``Either`` instance.

    """

    def __repr__(self) -> str:
        """
        .. admonition:: string representation

            Two values 'LEFT' or 'RIGHT' for the truthy and falsy
            singletons respectfully. Also the default user strings.

        """
        if self:
            return 'LEFT'
        return 'RIGHT'


LEFT: Final[EitherBool] = EitherBool(True)
"""
.. admonition:: truthy Either flag

    Used by ``Either`` initializer to make a right ``Either``.

"""

RIGHT: Final[EitherBool] = EitherBool(False)
"""
.. admonition:: falsy Either flag

    Used by ``Either`` initializer to make a right ``Either``.

"""


@final
class Either[L, R]:
    """
    .. admonition:: Either monad

        Left biased Either monad.

        - immutable semantics
        - contains either a "left" or a "right" item, but not both
        - hashable

        .. note::

            If contained item is not hashable, item's identity is
            used in the hash calculation.

    """

    __slots__ = '_value', '_side', '_hash'
    __match_args__ = ('_value', '_side')

    @overload
    def __init__(self, value: L) -> None: ...
    @overload
    def __init__(self, value: L, side: EitherBool) -> None: ...
    @overload
    def __init__(self, value: R, side: EitherBool) -> None: ...

    def __init__(self, value: L | R, side: EitherBool = LEFT) -> None:
        """
        .. admonition:: initializer

            Initialize ``Either`` instance as a "left" or a "right".

            :param value: The value contained in the ``Either``.
            :param side: Determines whether to produce
                     a left or right ``Either``.

        """
        self._value: L | R
        self._side: EitherBool
        if side:
            self._value = value
            self._side = LEFT
        else:
            self._value = value
            self._side = RIGHT
        self._hash: int | None = None

    def __hash__(self) -> int:
        """
        .. admonition:: hashability

            If contained value hashable, use its hash value in
            the hash calculation, otherwise use item's identity.

            - should be safe, the ``Either`` holds a reference to the value
            - lazily calculates hash value, then caches it
            - hash also depends if ``Either`` is a left or right

        """
        if self._hash is None:
            try:
                self._hash = hash((self._value, self._side))
            except TypeError:
                self._hash = hash((id(self._value), self._side))
        return self._hash

    def __bool__(self) -> bool:
        """
        .. admonition:: bool

            - left ``Either`` is truthy
            - right ``Either`` is falsy

        """
        return self._side is LEFT

    def __len__(self) -> int:
        """
        .. admonition:: len

            Either always contains just one value.

        """
        return 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self and other:
            if (self._value is other._value) or (self._value == other._value):
                return True

        if not self and not other:
            if (self._value is other._value) or (self._value == other._value):
                return True

        return False

    def __iter__(self) -> Iterator[L]:
        """
        .. admonition:: iterate

            Iterate ``value`` if a left ``Ether``.

        """
        if self:
            yield cast(L, self._value)

    def __repr__(self) -> str:
        """
        .. admonition:: representation string

            Return the strings

            - 'Either(repr_value, LEFT)' if a left
            - 'Either(repr_value, RIGHT)' if if a right

            Where ``repr_value = repr(value)``.

        """
        if self:
            return 'Either(' + repr(self._value) + ', LEFT)'
        return 'Either(' + repr(self._value) + ', RIGHT)'

    def __str__(self) -> str:
        """
        .. admonition:: user string

            Return the strings

            - 'Either(str_value)' when a left
            - 'Either(str_value, RIGHT)' when a right

            Where ``str_value = str(value)``.

        """
        if self:
            return '< ' + str(self._value) + ' | >'
        return '< | ' + str(self._value) + ' >'

    def get(self) -> L:
        """
        .. admonition:: get

            Get value if a left.

            :returns: The value if a left.
            :raises ValueError: If not a left.

            .. warning::

                Unsafe method ``get``. Will raise ``ValueError`` if ``Either``
                is a right.

                .. tip::

                    Best practice is to first check the ``Either`` in
                    a boolean context.

        """
        if self._side == RIGHT:
            msg = 'Either: get method called on a right valued Either'
            raise ValueError(msg)
        return cast(L, self._value)

    def get_left(self) -> MayBe[L]:
        """
        .. admonition:: get left

            Get the value if a left.

            :returns: ``MayBe[L]``

        """
        if self._side == LEFT:
            return MayBe(cast(L, self._value))
        return MayBe()

    def get_right(self) -> MayBe[R]:
        """
        .. admonition:: get right

            Get the value if a right.

            :returns: ``MayBe[R]``

        """
        if self._side == RIGHT:
            return MayBe(cast(R, self._value))
        return MayBe()

    def map_right[V](self, f: Callable[[R], V]) -> 'Either[L, V]':
        """
        .. admonition:: map right

            Map function ``f`` over the contents of a right ``Either``.

            :param f: function to map a right value
            :returns: A new ``Either`` if a right, otherwise ``self``.

        """
        if self._side == LEFT:
            return cast(Either[L, V], self)
        return Either[L, V](f(cast(R, self._value)), RIGHT)

    def map[U](self, f: Callable[[L], U]) -> 'Either[U, R]':
        """
        .. admonition:: map

            Map function ``f`` over left ``Either``.

            :param f: Function used to map left values.
            :returns: A new ``Either`` if a left, otherwise ``self``.

        """
        if self._side == RIGHT:
            return cast(Either[U, R], self)
        return Either(f(cast(L, self._value)), LEFT)

    def map_except[U](self, f: Callable[[L], U], fallback_right: R) -> 'Either[U, R]':
        """
        .. admonition:: map except

            Map ``f`` over left ``Either`` with a right fallback upon exception.

            .. warning::

                Swallows exceptions.

            :param f: Function used to map left values.
            :param fallback_right: Fallback value if exception thrown.
            :returns: A successfully mapped left, a propagated right,
                    or a right with a fallback value.

            .. warning::

                Swallows exceptions.

        """
        if self._side == RIGHT:
            return cast(Either[U, R], self)

        applied: MayBe[Either[U, R]] = MayBe()
        fall_back: MayBe[Either[U, R]] = MayBe()
        try:
            applied = MayBe(Either(f(cast(L, self._value)), LEFT))
        except (
            LookupError,
            ValueError,
            TypeError,
            BufferError,
            ArithmeticError,
            RecursionError,
            ReferenceError,
            RuntimeError,
        ):
            fall_back = MayBe(cast(Either[U, R], Either(fallback_right, RIGHT)))

        if fall_back:
            return fall_back.get()
        return applied.get()

    def bind[U](self, f: 'Callable[[L], Either[U, R]]') -> 'Either[U, R]':
        """
        .. admonition:: bind

            Flatmap function ``f`` over a left value. Propagate right
            values.

            :param f: Function to bind.
            :returns: A new Either if a left, otherwise itself.

        """
        if self:
            return f(cast(L, self._value))
        return cast(Either[U, R], self)

    def bind_except[U](
        self, f: 'Callable[[L], Either[U, R]]', fallback_right: R
    ) -> 'Either[U, R]':
        """
        .. admonition:: bind except

            Flatmap function ``f`` over ``Either``, with fallback upon
            exception. Propagate right values.

            .. warning::

                Swallows exceptions.

            :param f: Function to bind over values.
            :param fallback_right: Fallback value if exception thrown.
            :returns: A successfully bound left, a propagated right,
                    or a right with a fallback value.

            .. warning::

                Swallows exceptions.

        """
        if self._side == RIGHT:
            return cast(Either[U, R], self)

        applied: MayBe[Either[U, R]] = MayBe()
        fall_back: MayBe[Either[U, R]] = MayBe()
        try:
            if self:
                applied = MayBe(f(cast(L, self._value)))
        except (
            LookupError,
            ValueError,
            TypeError,
            BufferError,
            ArithmeticError,
            RecursionError,
            ReferenceError,
            RuntimeError,
        ):
            fall_back = MayBe(cast(Either[U, R], Either(fallback_right, RIGHT)))

        if fall_back:
            return fall_back.get()
        return applied.get()

    @staticmethod
    def sequence[U, V](
        sequence_either_uv: 'Sequence[Either[U, V]]',
    ) -> 'Either[Sequence[U], V]':
        """
        .. admonition:: sequence

            ``Sequence[Either[U, V]]`` -> ``Either[Sequence[U], V]``

            If all ``Either`` are lefts, then return an ``Either``
            of the ``Sequence`` of contained left values. Otherwise
            return a right ``Either`` containing the first right
            encountered.

        """
        sequenced_list: list[U] = []

        for either_uv in sequence_either_uv:
            if either_uv:
                sequenced_list.append(either_uv.get())
            else:
                return Either(either_uv.get_right().get(), RIGHT)

        sequenced_items = type(sequence_either_uv)(sequenced_list)  # type: ignore

        return Either(cast(Sequence[U], sequenced_items))
