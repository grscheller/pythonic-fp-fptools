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

from collections.abc import Callable
from typing import Any, Final, Never, TypeVar, ParamSpec
from .function import sequenced
from .either import Either, LEFT, RIGHT
from .maybe import MayBe

__all__ = ['Lazy', 'lazy', 'real_lazy']

D = TypeVar('D')
R = TypeVar('R', contravariant=True)
P = ParamSpec('P')

class Lazy[D, R]:
    __slots__ = ('_f', '_d', '_result', '_pure', '_evaluated', '_exceptional')

    _f: Callable[[D], R]
    _d: D
    _pure: bool
    _evaluated: bool
    _exceptional: MayBe[bool]
    _result: Either[R, Exception]

    def __init__(self, f: Callable[[D], R], d: D, pure: bool = True) -> None: ...
    def __bool__(self) -> bool: ...
    def eval(self) -> None: ...
    def got_result(self) -> MayBe[bool]: ...
    def got_exception(self) -> MayBe[bool]: ...
    def get(self, alt: R | None = None) -> R | Never: ...
    def get_result(self) -> MayBe[R]: ...
    def get_exception(self) -> MayBe[Exception]: ...

def lazy[**P, R](
    f: Callable[P, R], *args: P.args, **kwargs: P.kwargs
) -> Lazy[tuple[Any, ...], R]: ...
def real_lazy[**P, R](
    f: Callable[P, R], *args: P.args, **kwargs: P.kwargs
) -> Lazy[tuple[Any, ...], R]: ...
