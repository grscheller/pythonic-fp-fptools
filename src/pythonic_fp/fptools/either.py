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

      - Left values is intended for "expected" results.
      - Right value gives information on the "unexpected"
        perhaps "exceptional" result.

    - left and right values can be the same or different types
    - in a boolean context

      - left values are truthy
      - right values are falsy

    .. tip::

        Happy path without exceptions.

        Instead of catching an exception whenever the "happy path"
        fails, process the left values then deal with or propagate
        right values.

    .. tip::

        Users of this module can avoid explicitly importing sentinel
        values LEFT and RIGHT by the static Either.left and Either.right
        class methods.

        - left_either: Either[int, str] = Either.left(42)
        - right_either: Either[int, str] = Either.right('Not forty-two')

"""

from collections.abc import Callable, Iterable, Iterator
from typing import Final, cast, final, overload

from pythonic_fp.booleans.truthy_falsy import F_Bool, T_Bool, TF_Bool

from ._recoverable import RECOVERABLE
from .maybe import MayBe

__all__ = ['Either', 'LEFT', 'RIGHT']


LEFT: Final[T_Bool] = T_Bool()
"""
.. admonition:: LEFT

    :var LEFT: The left Either singleton flag.

"""

RIGHT: Final[F_Bool] = F_Bool()
"""
.. admonition:: RIGHT

    :var RIGHT: The right Either singleton flag

"""


@final
class Either[L, R]:
    """
    .. admonition:: either monad

        Left biased Either monad.

        - immutable
        - contains either a "left" or a "right" item, but not both
        - hashable

    """

    __slots__ = ('_hash', '_side', '_value')
    __match_args__ = ('_value', '_side')

    @overload
    def __init__(self, value: L, side: T_Bool) -> None: ...
    @overload
    def __init__(self, value: R, side: F_Bool) -> None: ...

    def __init__(self, value: L | R, side: TF_Bool) -> None:
        """
        .. admonition:: init

            Initialize Either instance as a left or a right Either.

            :param value: The value contained in the Either.
            :param side: Determines whether to produce
                         a "left" or a "right" Either.
            :type side: TF_Bool

        """
        self._value: L | R
        self._side: TF_Bool
        self._value = value
        self._side = side
        self._hash: int | None = None

    def __hash__(self) -> int:
        """
        .. admonition:: hash

            If contained value hashable, use its hash value in
            the hash calculation, otherwise use the value's identity.

            - Should be safe, the ``Either`` holds
              a reference to the value.
            - Lazily calculates hash value, then caches it.
            - The hash also depends if the Either is a left or right.

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

            - left Either instances are truthy
            - right Either instances are falsy

            :returns: ``True`` if ``Either`` is a left,
                      ``False`` if a right.

        """
        return self._side is LEFT

    def __len__(self) -> int:
        """
        .. admonition:: len

            An Either always contains just one value.

            :returns: 1

        """
        return 1

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: equality comparison

            Compare Either to another object. Compare first
            by identity, then value.

            .. note::

                Pythonic choice was made to allow left or right
                ``Either`` monads to compare as equal if they have
                different right or left "phantom" types respectively.

                - Allows for more flexible equality checking at the
                  expense of not flagging possible type or name
                  mismatches.
                - Flagging such a type mismatch would require a Liskov
                  Substitution Principle violation.

            :param other: The object to be compared.
            :returns: True only if other is a Either of the same side
                      containing objects which compare as equal.

        """
        if not isinstance(other, type(self)):
            return False

        if self and other:
            return (self._value is other._value) or (self._value == other._value)

        if not self and not other:
            return (self._value is other._value) or (self._value == other._value)

        return False

    def __iter__(self) -> Iterator[L]:
        """
        .. admonition:: iter

            Yield the contained value if Either is a left.

            :yields: The contained value if a left.

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

            :returns: A string to reproduce the Either.

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

            :returns: A string meaningful to an end user.

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

                Unsafe method get will raise ValueError() if the Either
                is a right.

                .. tip::

                    Best practice is to first check the Either in
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

            :returns: MayBe wrapping a left value.
            :rtype: MayBe[L]

        """
        if self._side == LEFT:
            return MayBe(cast(L, self._value))
        return MayBe()

    def get_right(self) -> MayBe[R]:
        """
        .. admonition:: get right

            Get the value if a right.

            :returns: MayBe wrapping a right value.
            :rtype: MayBe[R]

        """
        if self._side == RIGHT:
            return MayBe(cast(R, self._value))
        return MayBe()

    def map_right[V](self, f: Callable[[R], V]) -> Either[L, V]:
        """
        .. admonition:: map right

            Map the function f over the contents of a right Either.

            :param f: A function to map a right value.
            :returns: A new Either instance if a right,
                      otherwise itself.

        """
        if self._side == LEFT:
            return cast(Either[L, V], self)
        return Either[L, V](f(cast(R, self._value)), RIGHT)

    def map[U](self, f: Callable[[L], U]) -> Either[U, R]:
        """
        .. admonition:: map

            Map function f over the Either.

            :param f: Mapping function.
            :returns: A new Either instance if a left,
                      otherwise itself.

        """
        if self._side == RIGHT:
            return cast(Either[U, R], self)
        return Either.left(f(cast(L, self._value)))

    def map_except[U](self, f: Callable[[L], U], fallback_right: R) -> Either[U, R]:
        """
        .. admonition:: map_except

            Map function f over the Either with right fallback
            upon exception.

            :param f: Mapping function.
            :param fallback_right: Fallback value if exception thrown.
            :returns: New left instance if successfully mapped,
                      a propagated right, or a new right when
                      an exception is thrown.

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
        if self._side == RIGHT:
            return cast(Either[U, R], self)

        applied: MayBe[Either[U, R]] = MayBe()
        fall_back: MayBe[Either[U, R]] = MayBe()
        try:
            applied = MayBe(Either.left(f(cast(L, self._value))))
        except RECOVERABLE:
            fall_back = MayBe(Either.right(fallback_right))

        if fall_back:
            return fall_back.get()
        return applied.get()

    def bind[U](self, f: Callable[[L], Either[U, R]]) -> Either[U, R]:
        """
        .. admonition:: bind

            Flatmap function f over a left value. Propagate right values.

            :param f: Function to bind.
            :returns: A new Either if a left,
                      itself if a right.

        """
        if self:
            return f(cast(L, self._value))

        return cast(Either[U, R], self)

    def bind_except[U](
        self, f: Callable[[L], Either[U, R]], fallback_right: R
    ) -> Either[U, R]:
        """
        .. admonition:: bind_except

            Flatmap function f over the Either, with fallback upon
            exception. Propagate right values.

            :param f: Function to bind over contained values.
            :param fallback_right: Fallback value if exception thrown.
            :returns: A successfully bound left, a propagated right,
                      or a right with the fallback value.

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
        if self._side == RIGHT:
            return cast(Either[U, R], self)

        applied = MayBe[Either[U, R]]()
        fall_back = MayBe[Either[U, R]]()
        try:
            applied = MayBe(f(cast(L, self._value)))
        except RECOVERABLE:
            fall_back = MayBe(cast(Either[U, R], Either.right(fallback_right)))

        if fall_back:
            return fall_back.get()
        return applied.get()

    @staticmethod
    def left[U, V](value: U) -> Either[U, V]:
        """
        .. admonition:: Either.left

            Helper static method to explicitly construct a left Either.

            :param value: The left value to use when constructing the Either.
            :returns: A left Either

        """
        return Either[U, V](value, LEFT)

    @staticmethod
    def right[U, V](value: V) -> Either[U, V]:
        """
        .. admonition:: Either.right

            Helper static method to explicitly construct a left Either.

            :param value: The left value to use when constructing the Either.
            :returns: A right Either

        """
        return Either[U, V](value, RIGHT)

    @staticmethod
    def sequence[U, V](
        iterable_either_uv: Iterable[Either[U, V]],
    ) -> Either[Iterable[U], V]:
        """
        .. admonition:: Either.sequence

            ``Iterable[Either[U, V]] -> Either[Iterable[U], V]``

            If all ``Either`` are lefts, then return an ``Either`` of an
            ``Iterable`` of contained left values. Otherwise return
            a right ``Either`` containing the first right encountered.

            :param sequence_either_uv: An Iterable of Either[U, V] values.
            :returns: A left Either containing an Iterable of all the
                      left values if none are right Either values,
                      otherwise a right Either containing the first
                      right value.

            .. note::

                A sequenced empty Iterable[Either[U, V]] would produce
                a MayBe of an empty Iterable, not an empty MayBe.

        """
        sequenced_list: list[U] = []

        for either_uv in iterable_either_uv:
            if either_uv:
                sequenced_list.append(either_uv.get())
            else:
                return Either.right(either_uv.get_right().get())

        return Either(type(iterable_either_uv)(sequenced_list), LEFT)
