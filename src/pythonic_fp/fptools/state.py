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
from typing import final
from pythonic_fp.circulararray.auto import CA


@final
class State[S, A]:
    """
    .. admonition:: State monad

        A pure FP implementation of the State Monad, a data structure
        generating values while propagating changes of state.

        .. note::

            A monad is a value in a context. The State monad wraps neither
            a state nor a ``(value, state)`` pair.

            It wraps a transformation ``old_state -> (value, new_state)``
            called a "state action".

            .. admonition:: Class State

                Instance members:

                - Property *run* is the **state action**
                - Method *bind* performs state action composition
                - Method *eval* performs the **run action**

                  - the **run action** evaluates the **state action** by

                    - supplying an initial state
                    - returning the resulting value

                Static members:

                - Method unit creates a State instance whose
                  run action returns the supplied constant value.
                - Method get creates a State instance whose
                  run action returns the current state.
                - Method set creates a State which ignores
                  the old state and swaps in a new one.
                - Method modify creates a State instance which
                  modifies the previous state via a function.
                - Method sequence combine a list of State instances
                  into a State whose run action returns the list
                  of generated values.

    """

    __slots__ = ('run',)

    def __init__(self, run: Callable[[S], tuple[A, S]]) -> None:
        """
        .. admonition:: init

            :param run: State action.
            :type run: ``S -> (A, S)`` where A is the type of the
                       generated value and S is the type of a state.

        """
        self.run = run

    def bind[B](self, g: 'Callable[[A], State[S, B]]') -> 'State[S, B]':
        """
        .. admonition:: state action composition

            :param g: A function that produces a ``State[S, B]``
                      from an ``A``.
            :returns: A ``State[S, B]`` whose state action is the
                      composition of the state actions from ``self``
                      followed by the one produced by ``g``.

        """
        def compose(s: S) -> tuple[B, S]:
            a, s = self.run(s)
            return g(a).run(s)

        return State(compose)

    def eval(self, init: S) -> A:
        """
        .. admonition:: run action

            Evaluate the state action by passing in an initial state
            and returning the produced value.

            :param init: An initial state to pass into the state action.
            :returns: The value produced by the run action.

        """
        a, _ = self.run(init)
        return a

    def map[B](self, f: Callable[[A], B]) -> 'State[S, B]':
        """
        .. admonition:: map

            Map function f over the resulting value of a
            state action propagating the current state.

            :param f: Function to map.
            :returns: A new State instance whose run action produces f(a)
                      where a is the value produced by the current State
                      instance and just propagates the current state.

        """
        return self.bind(lambda a: State.unit(f(a)))

    def map2[B, C](self, sb: 'State[S, B]', f: Callable[[A, B], C]) -> 'State[S, C]':
        """
        .. admonition:: map2

            Combine two state monads, self and sb, with a function.
            Resulting run action just propagates the current state.

            :param sb: State instance to combine with the current instance.
            :param f: Function used by the resulting run action
                      on the values produced by the run actions
                      of the current State instance and ``sb`` using
                      the same initial state.

        """
        return self.bind(lambda a: sb.map(lambda b: f(a, b)))

    def both[B](self, rb: 'State[S, B]') -> 'State[S, tuple[A, B]]':
        """
        .. admonition:: both

            Return a State instance whose run action returns a tuple
            from from the run actions of the current State and sb.

            :param sb: A State instance to be combined with the current one.

        """
        return self.map2(rb, lambda a, b: (a, b))

    @staticmethod
    def unit[ST, B](b: B) -> 'State[ST, B]':
        """
        .. admonition:: unit

            Create a State whose run action returns the given
            constant b  and propagate the present state.

            :param b: Value the new State's run action will return.
            :returns: A new State[ST, B] from a value b: B.

        """
        return State(lambda s: (b, s))

    @staticmethod
    def get[ST]() -> 'State[ST, ST]':
        """
        .. admonition:: get state

            Set run action to return the current state and
            propagate it unchanged.

            - the current state is propagated unchanged
            - current value now set to current state
            - will need type annotation

            :returns: A state monad wrapping a state action to return
                    the current state. Propagates the current state
                    unchanged.

        """
        return State[ST, ST](lambda s: (s, s))

    @staticmethod
    def put[ST](s: ST) -> 'State[ST, tuple[()]]':
        """
        .. admonition:: put state

            Manually insert a new state.

            - ignores previous state and swaps in a new state
            - resulting run action will return an empty tuple

              - the traditional canonically meaningless value in FP

            :param s: The state to swap in for current state
            :returns: State monad wrapping a state action which ignores
                      any initial state passed in when evaluated.
            :rtype: State[ST, tuple[()]]

        """
        return State(lambda _: ((), s))

    @staticmethod
    def modify[ST](f: Callable[[ST], ST]) -> 'State[ST, tuple[()]]':
        """
        .. admonition:: modify

            Modify previous state with a function. Like put, but modify
            previous state via f.

            :param f: Function to modify the current state.
            :returns: A State monad with a modified state.
            :rtype: State[ST, tuple[()]]

            .. note::

                Will need type annotation. Static type checkers like
                mypy have no *a priori* knowledge of what ``ST``
                could be.

        """
        return State.get().bind(lambda a: State.put(f(a)))  # type: ignore

    @staticmethod
    def sequence[ST, AA](sas: 'list[State[ST, AA]]') -> 'State[ST, list[AA]]':
        """
        .. admonition:: sequence a list

            Combine a list of state monads into a state monad whose
            run action returns a list of the values returned by each
            run action from the original list.

            :param sas: A list of state monads all of type ``State[ST, AA]``.
            :returns: A state monad whose run action produces a list of
                      the values produced by the list of State actions
                      provided to the method.
            :rtype: State[ST, list[AA]]
 
            .. note::

                The run action evaluates the run actions of the list
                front to back. The state is also propagated, not
                necessarily unchanged, front to back.

        """

        def append_ret(ls: list[AA], a: AA) -> list[AA]:
            ls.append(a)
            return ls

        return CA(sas).foldl(
            lambda s1, sa: s1.map2(sa, append_ret), State.unit(list[AA]([]))
        )
