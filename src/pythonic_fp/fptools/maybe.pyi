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

__all__ = ['MayBe']

from collections.abc import Callable, Iterator, Sequence
from typing import Never, overload, TypeVar

D = TypeVar('D', covariant=True)

class MayBe[D]:
    U = TypeVar('U', covariant=True)
    V = TypeVar('V', covariant=True)
    T = TypeVar('T')

    __slots__ = ('_value',)
    __match_args__ = ('_value',)

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, value: D) -> None: ...
    def __hash__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __iter__(self) -> Iterator[D]: ...
    def __repr__(self) -> str: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    @overload
    def get(self) -> D | Never: ...
    @overload
    def get(self, alt: D) -> D: ...
    def map[U](self, f: Callable[[D], U]) -> MayBe[U]: ...
    def bind[U](self, f: Callable[[D], MayBe[U]]) -> MayBe[U]: ...
    @staticmethod
    def sequence[U](sequence_mb_u: Sequence[MayBe[U]]) -> MayBe[Sequence[U]]: ...
