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

from typing import Any

from pythonic_fp.fptools.lazy import Lazy, lazy, real_lazy
from pythonic_fp.fptools.maybe import MayBe as MB

#-- Test happy and sad paths ---------------------------------------------------

def add2_if_pos(x: int) -> int:
    if x < 1:
        raise ValueError()
    return x + 2

def evaluate_it(lz: Lazy[int, int]) -> int:
    lz.eval()
    if lz.got_result().get():            # Opps ... typing work needed
        return lz.get_result().get()
    else:
        return -1

class Test_happy_sad_paths:

    def test_happy_path(self) -> None:
        assert evaluate_it(Lazy(add2_if_pos, 5)) == 7

    def test_sad_path(self) -> None:
        assert evaluate_it(Lazy(add2_if_pos, -42)) == -1

#---------------------------------------------------------------

def hello() -> str:
    hello = "helloooo"
    while len(hello) > 1:
        if hello == 'hello':
            return hello
        hello = hello[:-1]
    raise ValueError('hello')

def no_hello() -> str:
    hello = "helloooo"
    while len(hello) > 1:
        if hello == 'hello':
            raise ValueError('failed as expected')
        hello = hello[:-1]
    return hello

def return_str(lz: Lazy[Any, str]) -> str:
    lz.eval()
    if result := lz.get_result():
        return result.get()
    return f'Error: {lz.get_exception().get()}'

class Test_Lazy_0_1:
    def test_happy_path(self) -> None:
        lz_good = lazy(hello)
        assert return_str(lz_good) == 'hello'

    def test_sad_path(self) -> None:
        lz_bad = lazy(no_hello)
        assert return_str(lz_bad) == 'Error: failed as expected'

#---------------------------------------------------------------

class Counter:
    def __init__(self, n: int=0) -> None:
        self._cnt = n

    def inc(self) -> None:
        self._cnt += 1

    def get(self) -> int:
        return self._cnt

    def set(self, n: int) -> None:
        self._cnt = n

class TestLazy00:
    """Test for a function that

    - takes no arguments
    - throws no exceptions
    - has only side effects

    """
    def test_pure_vs_impure(self) -> None:
        cnt1 = Counter(0)

        pure = real_lazy(cnt1.inc)
        impure = lazy(cnt1.inc)

        # first check if counter works as expected
        assert cnt1.get() == 0
        assert cnt1.get() == 0
        cnt1.inc()
        cnt1.inc()
        assert cnt1.get() == 2
        cnt1.set(0)
        cnt1.inc()
        assert cnt1.get() == 1

        # test not yet evaluated
        assert pure.got_exception() == MB()
        assert impure.got_exception() == MB()
        assert pure.got_result() == MB()
        assert impure.got_result() == MB()

        # evaluate each and check side effect
        cnt1.set(0)
        impure.eval()
        assert cnt1.get() == 1
        impure.eval()
        assert cnt1.get() == 2
        pure.eval()
        assert cnt1.get() == 3
        pure.eval()
        assert cnt1.get() == 3
        impure.eval()
        assert cnt1.get() == 4
        impure.eval()
        assert cnt1.get() == 5
        pure.eval()
        assert cnt1.get() == 5
        pure.eval()
        assert cnt1.get() == 5

        # test if evaluated
        assert pure.got_exception() == MB(False)
        assert impure.got_exception() == MB(False)
        assert pure.got_result() == MB(True)
        assert impure.got_result() == MB(True)


class TestLazy10:
    """Test for a function that

    - takes one argument
    - throws no exceptions
    - has only side effects

    """
    def test_pure(self) -> None:
        cnt2 = Counter(0)

        pure = real_lazy(cnt2.set, 2)
        impure = lazy(cnt2.set, 5)

        # test not yet evaluated
        assert pure.got_exception() == MB()
        assert impure.got_exception() == MB()
        assert pure.got_result() == MB()
        assert impure.got_result() == MB()

        # evaluate each and check side effect
        assert cnt2.get() == 0
        impure.eval()
        assert cnt2.get() == 5
        pure.eval()
        assert cnt2.get() == 2
        impure.eval()
        assert cnt2.get() == 5
        impure.eval()
        assert cnt2.get() == 5
        pure.eval()
        assert cnt2.get() == 5

        # test if evaluated
        assert pure.got_exception() == MB(False)
        assert impure.got_exception() == MB(False)
        assert pure.got_result() == MB(True)
        assert impure.got_result() == MB(True)


class TestLazy01:
    """Test for functions or methods that

    - take no arguments
    - can throw exceptions
    - returns one value

    """
    def test_lazy_01(self) -> None:
        state: list[int] = []

        def foo() -> int:
            state.append(42)
            return 42

        def bar() -> int:
            value = 42
            divisor = 0
            quotient = int(value/divisor)
            state.append(quotient)
            return value

        def baz() -> int:
            value = int('forty-two')
            return value

        def buz() -> int:
            value = 42 + 'forty-two'  # type: ignore
            return value

        lz_foo = lazy(foo)
        lz_bar = lazy(bar)
        lz_baz = lazy(baz)
        lz_buz = lazy(buz)
        rlz_foo = real_lazy(foo)
        rlz_bar = real_lazy(bar)
        rlz_baz = real_lazy(baz)
        rlz_buz = real_lazy(buz)

        # test not yet evaluated
        assert lz_foo.got_result() == MB()
        assert lz_bar.got_result() == MB()
        assert lz_baz.got_result() == MB()
        assert lz_buz.got_result() == MB()
        assert lz_foo.got_exception() == MB()
        assert lz_bar.got_exception() == MB()
        assert lz_baz.got_exception() == MB()
        assert lz_buz.got_exception() == MB()
        assert rlz_foo.got_result() == MB()
        assert rlz_bar.got_result() == MB()
        assert rlz_baz.got_result() == MB()
        assert rlz_buz.got_result() == MB()
        assert rlz_foo.got_exception() == MB()
        assert rlz_bar.got_exception() == MB()
        assert rlz_baz.got_exception() == MB()
        assert rlz_buz.got_exception() == MB()

        lz_foo.eval()
        if lz_foo.got_result():
            assert lz_foo.get_result() == MB(42)
            assert lz_foo.get() == 42
            assert lz_foo.get(100) == 42
        else:
            assert False

        if lz_foo.got_exception():     # Confusing! API change needed
            assert lz_foo.get_exception() == MB()
        else:
            assert False

        assert len(state) == 1
        lz_bar.eval()
        if lz_bar.got_result():        # Confusing! MB(x: bool) always True 
            assert lz_bar.get_result() == MB()
        else:
            assert False

        if lz_bar.got_exception():
            exc = lz_bar.get_exception().get()    # a bit verbose
            assert isinstance(exc, ZeroDivisionError)
        else:
            assert False
        assert len(state) == 1

        rlz_foo.eval()
        if rlz_foo.got_result().get():
            assert rlz_foo.get_result() == MB(42)
        else:
            assert False

        if rlz_foo.got_exception().get():
            assert False
        else:
            assert rlz_foo.get_result() == MB(42)

        lz_bar.eval()
        if lz_bar.got_result().get():
            assert False
        else:
            assert lz_bar.get_result() == MB()
        assert len(state) == 2

        if rlz_bar.got_exception():
            assert False
        assert len(state) == 2

        rlz_bar.eval()
        assert len(state) == 2
        rlz_bar.eval()
        assert len(state) == 2
        lz_foo.eval()
        assert len(state) == 3
        lz_bar.eval()
        assert len(state) == 3
        rlz_bar.eval()
        assert len(state) == 3

        lz_baz.eval()
        rlz_baz.eval()
        assert lz_baz.got_exception() == MB(True)
        assert rlz_baz.got_exception() == MB(True)

class TestLazy_with_class:
    """Test with class methods."""
    def test_lazy_with_class(self) -> None:
        class Secret:
            def __init__(self, secret: int):
                self._secret = secret

            def get_secret(self) -> int:
                if (ret := self._secret) != 13:
                    return ret
                else:
                    raise RuntimeError(13)

        secret10 = Secret(10)
        secret13 = Secret(13)

        lz_get_secret10 = lazy(secret10.get_secret)
        lz_get_secret10.eval()
        assert lz_get_secret10.got_exception() == MB(False)
        assert lz_get_secret10.get_result() == MB(10)
        assert lz_get_secret10.get_exception() == MB()

        lz_get_secret13 = lazy(secret13.get_secret)
        lz_get_secret13.eval()
        assert lz_get_secret13.got_exception() == MB(True)
        assert lz_get_secret13.get_result() == MB()
        assert repr(lz_get_secret13.get_exception().get()) == 'RuntimeError(13)'
