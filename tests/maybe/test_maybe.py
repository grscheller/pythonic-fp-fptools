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

from pythonic_fp.fptools.maybe import MayBe


def add2(x: int) -> int:
    return x + 2


class TestMayBe:
    def test_identity(self) -> None:
        n1: MayBe[int] = MayBe()
        n2: MayBe[int] = MayBe()
        o1 = MayBe(42)
        o2 = MayBe(40)
        assert o1 is not o2
        o3 = o2.map(add2)
        assert o3 is not o2
        assert o1 is not o3
        assert n1 is not n2
        assert o1 is not n1
        assert n2 is not o2

    def test_equality(self) -> None:
        n1: MayBe[int] = MayBe()
        n2: MayBe[int] = MayBe()
        o1 = MayBe(42)
        o2 = MayBe(40)
        assert o1 != o2
        o3 = o2.map(add2)
        assert o3 != o2
        assert o1 == o3
        assert n1 == n2
        assert o1 != n1
        assert n2 != o2

    def test_iterate(self) -> None:
        o1 = MayBe(38)
        o2 = o1.map(add2).map(add2)
        n1: MayBe[int] = MayBe()
        l1 = [5]
        l2 = [3]
        for v in n1:
            l1.append(v)  # noqa: PERF402
        for v in o2:
            l2.append(v)  # noqa: PERF402
        assert len(l1) == 1
        assert len(l2) == 2
        assert l2[1] == 42

    def test_get(self) -> None:
        o1 = MayBe(1)
        n1: MayBe[int] = MayBe()
        assert o1.get(42) == 1
        assert n1.get(21) == 21
        assert o1.get() == 1
        try:
            foo = 42
            foo = n1.get()
        except ValueError:
            assert True
        else:
            assert False
        finally:
            assert foo == 42
        assert n1.get(13) == (10 + 3)
        assert n1.get(10 % 7) == 3

    def test_equal_self(self) -> None:
        mb42 = MayBe(40 + 2)
        ph42 = MayBe(42)
        mbno: MayBe[int] = MayBe()
        phno: MayBe[int] = MayBe()
        assert mb42 != mbno
        assert mb42 == ph42
        assert mbno == phno

    def test_map(self) -> None:
        def f(x: int) -> float:
            return x + 1.0

        mb40_int = MayBe(40)
        mb41_int = MayBe(41)
        mb41_float = MayBe(41.0)
        mb42_float = MayBe(42.0)
        mb_empty_int = MayBe[int]()
        mb_empty_float = MayBe[float]()

        assert mb40_int.map(f) == mb41_float
        assert mb40_int.map(f) != mb42_float
        assert mb41_int.map(f) == mb42_float
        assert mb_empty_int.map(f) == mb_empty_float

    def test_map_except(self) -> None:
        def f(x: int) -> float:
            if x < 0:
                raise ValueError()

            return 2.0 * x

        mb20_int = MayBe(20)
        mb21_int = MayBe(21)
        mb_neg_1_int = MayBe(-1)
        mb40_float = MayBe(40.0)
        mb42_float = MayBe(42.0)
        mb_empty_int = MayBe[int]()
        mb_empty_float = MayBe[float]()

        assert mb20_int.map_except(f) == mb40_float
        assert mb20_int.map_except(f) != mb42_float
        assert mb21_int.map_except(f) == mb42_float
        assert mb_neg_1_int.map_except(f) == mb_empty_float
        assert mb_empty_int.map_except(f) == mb_empty_float

        assert mb_neg_1_int.map_except(f) == mb_empty_int  # At runtime, all MayBe() compare as equal
        assert mb_empty_int.map_except(f) == mb_empty_int

        one_int = 1
        two_int = 2
        two_float = 2.0
        assert MayBe(one_int) != MayBe(two_int)
        assert MayBe(one_int) != MayBe(two_float)
        assert MayBe(two_int) == MayBe(two_float)  # Due to Fortran disease,
        assert two_int == two_float                # numeric types auto-promote.

    def test_bind(self) -> None:
        def f(x: int) -> MayBe[float]:
            return MayBe(x + 1.0)

        def g(x: int) -> MayBe[float]:
            return MayBe()

        one_int = 1
        two_int = 2
        two_float = 2.0
        three_float = 3.0

        mb_empty_int = MayBe[int]()
        mb_empty_float = MayBe[float]()
        mb_one_int = MayBe(one_int)
        mb_two_int = MayBe(two_int)
        mb_two_float = MayBe(two_float)
        mb_three_float = MayBe(three_float)

        assert mb_empty_int.bind(f) == mb_empty_float
        assert mb_empty_int.bind(g) == mb_empty_float
        assert mb_one_int.bind(f) == mb_two_float
        assert mb_one_int.bind(g) == mb_empty_float
        assert mb_two_int.bind(f) == mb_three_float
        assert mb_two_int.bind(g) == mb_empty_float
