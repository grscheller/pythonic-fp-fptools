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
from typing import TypeVar

S = TypeVar('S')
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
ST = TypeVar('ST')
AA = TypeVar('AA')

class State[S, A]:
    __slots__ = ('run',)

    run: Callable[[S], tuple[A, S]]

    def __init__(self, run: Callable[[S], tuple[A, S]]) -> None: ...
    def bind[B](self, g: Callable[[A], State[S, B]]) -> State[S, B]: ...
    def eval(self, init: S) -> A: ...
    def map[B](self, f: Callable[[A], B]) -> State[S, B]: ...
    def map2[B, C](self, sb: State[S, B], f: Callable[[A, B], C]) -> State[S, C]: ...
    def both[B](self, rb: State[S, B]) -> State[S, tuple[A, B]]: ...
    @staticmethod
    def unit[ST, B](b: B) -> State[ST, B]: ...
    @staticmethod
    def get[ST]() -> State[ST, ST]: ...
    @staticmethod
    def put[ST](s: ST) -> State[ST, tuple[()]]: ...
    @staticmethod
    def modify[ST](f: Callable[[ST], ST]) -> State[ST, tuple[()]]: ...
    @staticmethod
    def sequence[ST, AA](sas: list[State[ST, AA]]) -> State[ST, list[AA]]: ...
