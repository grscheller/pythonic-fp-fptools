# Copyright 2024-2025 Geoffrey R. Scheller
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

__all__ = ['State']

from collections.abc import Callable
from pythonic_fp.circulararray.auto import CA


class State[S, A]:
    """
    .. admonition:: State Monad

        Data structure generating values while propagating changes
        of state. A pure FP implementation for the State Monad

        The ``State`` class represents neither a state nor a (value, state) pair.

        - It wraps a state transformation old_state -> (value, new_state)

          - THis state transformation is also known as a "state action".
          - The ``run`` property is this the state action wrapped by the monad.
          - The ``bind`` method performs function composition on state actions.
          - The ``eval`` method evaluates the state action by supplying it
            an initial state and returning the resulting value.

    """

    __slots__ = ('run',)

    def __init__(self, run: Callable[[S], tuple[A, S]]) -> None:
        """
        .. admonition:: Initialize

            Wrap a state transformation, also called a state action.

        :param run: State action to wrap.

        """
        self.run = run

    def bind[B](self, g: 'Callable[[A], State[S, B]]') -> 'State[S, B]':
        """
        .. admonition:: State action composition

            Perform state action composition resulting in a new
            wrapped combined state action.

        """
        def compose(s: S) -> tuple[B, S]:
            a, s = self.run(s)
            return g(a).run(s)

        return State(compose)

    def eval(self, init: S) -> A:
        """
        .. admonition:: Evaluate state action

            Evaluate the state action by passing in an initial state
            and returning the produced value. Eval is sometimes referred
            to as the run action.

        :param init: The initial state to pass into the state action.
        :returns: The final value produced by the final chain of
                  evaluations making up the state action.

        """
        a, _ = self.run(init)
        return a

    def map[B](self, f: Callable[[A], B]) -> 'State[S, B]':
        """
        .. admonition:: Map

            Map a function over the resulting value of a
            state action.

        """
        return self.bind(lambda a: State.unit(f(a)))

    def map2[B, C](self, sb: 'State[S, B]', f: Callable[[A, B], C]) -> 'State[S, C]':
        """
        .. admonition:: Map2

            Map a function of two variables over two state actions.

        """
        return self.bind(lambda a: sb.map(lambda b: f(a, b)))

    def both[B](self, rb: 'State[S, B]') -> 'State[S, tuple[A, B]]':
        """
        .. admonition:: Both

            Return a tuple of two state actions.

        """
        return self.map2(rb, lambda a, b: (a, b))

    @staticmethod
    def unit[ST, B](b: B) -> 'State[ST, B]':
        """
        .. admonition:: unit

            Create a State action returning the given value
            and propagating the present state.

        :param b: Value state action to return.
        :returns: Create a State monad from a value ``b: B``.

        """
        return State(lambda s: (b, s))

    @staticmethod
    def get[ST]() -> 'State[ST, ST]':
        """
        .. admonition:: get

            Set state action to return the current state and
            propagate it unchanged.

            - the current state is propagated unchanged
            - current value now set to current state
            - will need type annotation

        :returns: State monad wrapping a state action returning and
                  propagating the current state unchanged.

        """
        return State[ST, ST](lambda s: (s, s))

    @staticmethod
    def put[ST](s: ST) -> 'State[ST, tuple[()]]':
        """
        .. admonition:: put

            Manually insert a state.

            - ignores previous state and swaps in a new state
            - assigns a canonically meaningless value for current value

        :param s: State to insert ignoring 
        :returns: State monad wrapping a state action which ignores any
                  initial state passed in when evaluated.
        """
        return State(lambda _: ((), s))

    @staticmethod
    def modify[ST](f: Callable[[ST], ST]) -> 'State[ST, tuple[()]]':
        """
        .. admonition:: modify

            Modify previous state with a function.

        - like put, but modify previous state via ``f``
        - will need type annotation

          - mypy has no "a priori" way to know what ST is

        """
        return State.get().bind(lambda a: State.put(f(a)))  # type: ignore

    @staticmethod
    def sequence[ST, AA](sas: 'list[State[ST, AA]]') -> 'State[ST, list[AA]]':
        """
        .. admonition:: sequence a list

            Combine a list of state actions into a state action of a list.

        - all state actions must be of the same type
        - run method evaluates list front to back

        """

        def append_ret(ls: list[AA], a: AA) -> list[AA]:
            ls.append(a)
            return ls

        return CA(sas).foldl(
            lambda s1, sa: s1.map2(sa, append_ret), State.unit(list[AA]([]))
        )
