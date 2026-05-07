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
.. admonition:: The Either Monad

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
    .. admonition:: Type for the ``LEFT`` and ``RIGHT`` singletons.

        Boolean-like type for signaling the ``Either`` initializer
        to make a left or right ``Either`` instance.

    """
    def __repr__(self) -> str:
        """
        .. admonition:: String representation

            Two values 'LEFT' or 'RIGHT' for the truthy and falsy
            singletons respectfully. Also the default user strings.

        """
        if self:
            return 'LEFT'
        return 'RIGHT'


LEFT: Final[EitherBool] = EitherBool(True)
"""
.. admonition:: Truthy Either singleton.

    Passed  to ``Either`` initializer to make a right ``Either``.

"""

RIGHT: Final[EitherBool] = EitherBool(False)
"""
.. admonition:: Falsy Either singleton.

    Passed to ``Either`` initializer to make a right ``Either``.

"""


@final
class Either[L, R]:
    """
    .. admonition:: Either Monad

        Left biased Either Monad.

        - immutable semantics
        - contains either a "left" or a "right" item, but not both.
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

            Initialize the ``Either`` instance as a "left" or a "right".

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

            If the contained value is hashable, its hash value is
            used to calculate the hash, otherwise the identity of
            the contained value is used. Hash also depends whether
            the ``Either`` is a left or a right.

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

            - left ``Either`` truthy
            - right ``Either`` falsy

        :returns: ``True`` when a left, ``False`` when a right.

        """
        return self._side is LEFT

    def __repr__(self) -> str:
        if self:
            return 'Either(' + repr(self._value) + ', LEFT)'
        return 'Either(' + repr(self._value) + ', RIGHT)'

    def __str__(self) -> str:
        if self:
            return '< ' + str(self._value) + ' | >'
        return '< | ' + str(self._value) + ' >'

    def __len__(self) -> int:
        """
        .. admonition:: Length

            Either always contains just one value.

        :returns: 1

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
        .. admonition:: Iterate

            Iterate ``value`` if a left ``Ether``.

        """
        if self:
            yield cast(L, self._value)

    def get(self) -> L:
        """
        .. admonition:: Get

            Get value if a left.

            .. warning::

                Unsafe method ``get``. Will raise ``ValueError`` if ``Either``
                is a right.

                .. tip::

                    Best practice is to first check the ``Either`` in
                    a boolean context.

        :returns: The value if a left.
        :raises ValueError: If not a left.

        """
        if self._side == RIGHT:
            msg = 'Either: get method called on a right valued Either'
            raise ValueError(msg)
        return cast(L, self._value)

    def get_left(self) -> MayBe[L]:
        """
        .. admonition:: Safer Get

            Get the value if a left.

        :returns: ``MayBe[L]``

        """
        if self._side == LEFT:
            return MayBe(cast(L, self._value))
        return MayBe()

    def get_right(self) -> MayBe[R]:
        """
        .. admonition:: Get Right

            Get the value if a right.

        :returns: ``MayBe[R]``

        """
        if self._side == RIGHT:
            return MayBe(cast(R, self._value))
        return MayBe()

    def map_right[V](self, f: Callable[[R], V]) -> 'Either[L, V]':
        """
        .. admonition:: Map Right

            Map function ``f`` over the contents of a right ``Either``.

        :param f: function to map a right value
        :returns: A new ``Either`` if a right, otherwise ``self``.

        """
        if self._side == LEFT:
            return cast(Either[L, V], self)
        return Either[L, V](f(cast(R, self._value)), RIGHT)

    def map[U](self, f: Callable[[L], U]) -> 'Either[U, R]':
        """
        .. admonition:: Map

            Map function ``f`` over left ``Either``.

        :param f: Function used to map left values.
        :returns: A new ``Either`` if a left, otherwise ``self``.

        """
        if self._side == RIGHT:
            return cast(Either[U, R], self)
        return Either(f(cast(L, self._value)), LEFT)

    def map_except[U](self, f: Callable[[L], U], fallback_right: R) -> 'Either[U, R]':
        """
        .. admonition:: Map Except

            Map ``f`` over left ``Either`` with a right fallback upon exception.

            .. warning::
                Swallows exceptions.

        :param f: Function used to map left values.
        :param fallback_right: Fallback value if exception thrown.
        :returns: A successfully mapped left, a propagated right,
                  or a right with a fallback value.

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
        .. admonition:: Bind

            Flatmap function ``f`` over a left value. Propagate right
            values.

        :param f: Function to bind.
        :returns: A new Either if a left, otherwise itself.

        """
        if self:
            return f(cast(L, self._value))
        return cast(Either[U, R], self)

    def bind_except[U](self, f: 'Callable[[L], Either[U, R]]', fallback_right: R) -> 'Either[U, R]':
        """
        .. admonition:: Bind Except

            Flatmap function ``f`` over ``Either``, with fallback upon
            exception. Propagate right values.

            .. warning::
                Swallows exceptions.

        :param f: Function to bind over values.
        :param fallback_right: Fallback value if exception thrown.
        :returns: A successfully bound left, a propagated right,
                  or a right with a fallback value.

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
    def sequence[U, V](sequence_either_uv: 'Sequence[Either[U, V]]') -> 'Either[Sequence[U], V]':
        """
        .. admonition:: Sequence

            ``Sequence[Either[U, V]]`` -> ``Either[Sequence[U], V]``

            If all ``Either`` are lefts, then return an ``Either``
            of the ``Sequence`` of contained left values. Otherwise
            return a right ``Either`` containing the first right
            encountered.

        :param sequence_either_uv: ``Sequence[Either[U, V]``
        :returns: ``Either`` of ``Sequence`` subtype of left values if
                    all sequence elements are lefts, otherwise
                    the first right encountered.

        """
        sequenced_list: list[U] = []

        for xor_uv in sequence_either_uv:
            if xor_uv:
                sequenced_list.append(xor_uv.get())
            else:
                return Either(xor_uv.get_right().get(), RIGHT)

        sequenced_items = type(sequence_either_uv)(sequenced_list)  # type: ignore
        return Either(cast(Sequence[U], sequenced_items))
