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

from pythonic_fp.fptools.state import State


class Test_simple:
    def test_simple_counter(self) -> None:
        sc = State(lambda s: (s + 1, s + 1))

        assert sc.run(0) == (1, 1)
        assert sc.run(42) == (43, 43)

        sc1 = sc.bind(lambda a: sc)
        assert sc1.run(0) == (2, 2)

        sc2 = sc.bind(lambda a: sc)
        assert sc2.run(40) == (42, 42)

        start = State.put(0)
        sc3 = start.bind(lambda _: sc)
        assert sc3.run(40) == (1, 1)

        sc4 = sc.bind(lambda a: sc).bind(lambda a: sc)
        assert sc4.run(0) == (3, 3)
        assert sc4.run(0) == (3, 3)

        sc5 = sc4.bind(lambda _: sc1)
        ss, aa = sc5.run(5)
        assert ss == 10
        assert aa == 10

        s1, a1 = sc.run(5)
        s2, a2 = sc.run(s1)
        assert (s1, a1) == (6, 6)
        assert (s2, a2) == (7, 7)

    def test_mod3_count(self) -> None:
        m3a: State[int, int] = State(lambda s: (s, (s + 1) % 3))
        m3b = m3a.map(lambda a: 2 * a + 1)

        assert (0, 1) == m3a.run(0)
        assert (1, 2) == m3a.run(1)
        assert (2, 0) == m3a.run(2)
        assert (3, 1) == m3a.run(3)
        assert (4, 2) == m3a.run(4)
        assert (5, 0) == m3a.run(5)

        assert m3a.eval(0) == 0
        assert m3a.eval(1) == 1
        assert m3a.eval(2) == 2
        assert m3a.eval(3) == 3
        assert m3a.eval(4) == 4
        assert m3a.eval(5) == 5
        assert m3a.eval(42) == 42

        a1, s1 = m3a.run(0)
        a2, s2 = m3a.run(s1)
        a3, s3 = m3a.run(s2)
        a4, s4 = m3a.run(s3)
        a5, s5 = m3a.run(s4)
        a6, s6 = m3a.run(s5)

        assert (a1, s1) == (0, 1)
        assert (a2, s2) == (1, 2)
        assert (a3, s3) == (2, 0)
        assert (a4, s4) == (0, 1)
        assert (a5, s5) == (1, 2)
        assert (a6, s6) == (2, 0)

        assert m3b.run(0) == (1, 1)
        assert m3b.run(1) == (3, 2)
        assert m3b.run(2) == (5, 0)
        assert m3b.run(3) == (7, 1)
        assert m3b.run(4) == (9, 2)
        assert m3b.run(5) == (11, 0)

        a1, s1 = m3b.run(0)
        a2, s2 = m3b.run(s1)
        a3, s3 = m3b.run(s2)
        a4, s4 = m3b.run(s3)
        a5, s5 = m3b.run(s4)
        a6, s6 = m3b.run(s5)

        assert (a1, s1) == (1, 1)
        assert (a2, s2) == (3, 2)
        assert (a3, s3) == (5, 0)
        assert (a4, s4) == (1, 1)
        assert (a5, s5) == (3, 2)
        assert (a6, s6) == (5, 0)

    def test_countdown(self) -> None:
        def cntdn(a: int) -> State[int, int]:
            if a == 0:
                return State(lambda a: (6, 6))
            else:
                return State(lambda a: (a - 1, a - 1))

        start: State[int, int] = State.unit(100)
        assert 100 == start.eval(42)
        countdown: State[int, int] = start.bind(cntdn)
        assert countdown.eval(5) == 4
        assert countdown.eval(100) == 99
        countdown = countdown.bind(cntdn).bind(cntdn)
        assert countdown.eval(5) == 2
        assert countdown.eval(100) == 97
        countdown = countdown.bind(cntdn)
        assert countdown.eval(5) == 1
        countdown = countdown.bind(cntdn)
        assert countdown.eval(5) == 0
        countdown = countdown.bind(cntdn)
        assert countdown.eval(5) == 6
        assert countdown.eval(6) == 0
        assert countdown.eval(4) == 5

    def test_modify(self) -> None:
        def square(n1: int) -> int:
            return n1 * n1

        count: State[int, int] = State(lambda s: (s, s + 1))

        def cnt(a: int) -> State[int, int]:
            return State(lambda a: (a, a + 1))

        sqr_st = State.modify(square)

        assert count.run(0) == (0, 1)
        assert count.bind(cnt).run(0) == (1, 2)
        assert count.bind(cnt).bind(cnt).run(0) == (2, 3)
        assert count.bind(cnt).bind(cnt).then(sqr_st).run(0) == ((), 9)
        assert count.bind(cnt).bind(cnt).then(sqr_st).bind(cnt).run(0) == (9, 10)

        do_it = count.bind(cnt).bind(cnt).then(sqr_st).bind(cnt).then(sqr_st).bind(cnt)
        a, s = do_it.run(0)
        assert (a, s) == (100, 101)

    def test_get(self) -> None:
        get_sa: State[object, object] = State.get()
        t = get_sa.run('foo')
        assert (t[0], t[1]) == ('foo', 'foo')

    def test_put(self) -> None:
        put_sa: State[object, tuple[()]] = State.put('bar')
        t = put_sa.run('foo')
        assert (t[0], t[1]) == ((), 'bar')

    def test_map(self) -> None:
        sa0: State[int, int] = State(lambda s: (1, s))
        sa1 = sa0.map(lambda n: n * 4)
        n, s = sa0.run(21)
        assert (n, s) == (1, 21)
        n, s = sa1.run(21)
        assert (n, s) == (4, 21)
        sa2: State[int, int] = State.get().map(lambda n: 2 * n)
        n, s = sa2.run(21)
        assert (n, s) == (42, 21)

    def test_map2(self) -> None:
        sa20: State[int, int] = State(lambda s: (20, s))
        sa11: State[int, int] = State(lambda s: (11, s))
        sa42 = sa20.map2(sa11, lambda x, y: x + 2 * y)
        n, s = sa42.run(0)
        assert (n, s) == (42, 0)

    def test_sequence_list(self) -> None:
        sa1 = State(lambda s: (str(s), s + 1))
        sa2 = State(lambda s: (str(s), s + 2))
        sa3 = State(lambda s: (str(s), s + 3))
        sa4 = State(lambda s: (str(s), s + 4))
        sas = [sa1, sa2, sa3, sa4]
        sal = State.sequence_list(sas)
        ll, ss = sal.run(0)
        assert ss == 10
        assert ll == ['0', '1', '3', '6']

        sa1 = State(lambda s: (str(1), s))
        sa2 = State(lambda s: (str(2), s))
        sa3 = State(lambda s: (str(3), s))
        sa4 = State(lambda s: (str(4), s))
        sas = [sa1, sa2, sa3, sa4]
        sal = State.sequence_list(sas)
        ll, ss = sal.run(0)
        assert ss == 0
        assert ll == ['1', '2', '3', '4']
