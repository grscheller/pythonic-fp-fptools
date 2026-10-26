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

"""Pickle tests for MayBe."""

import copy
import pickle

from pythonic_fp.fptools.maybe import MayBe

mb_no_42 = MayBe[int]()
mb_42 = MayBe[int](42)

mb_no_tuple = MayBe[tuple[int, str]]()
mb_tuple = MayBe((42, 'Forty-Two'))

mb_notuple_no = MayBe(((mb_no_tuple, 0), 'no'))
mb_tuple_yes = MayBe(((mb_tuple, 0), 'yes'))

maybe_test_cases = (mb_no_42, mb_42, mb_no_tuple, mb_tuple, mb_notuple_no, mb_tuple_yes)


class TestMayBePickle:
    def test_identity_survives_all_protocols(self) -> None:
        for mb in maybe_test_cases:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(mb, protocol=protocol))
                assert restored == mb, (
                    f'protocol {protocol} failed to recreate instanace'
                )

    def test_hashable_vs_unhashable(self) -> None:
        maybe_test_case_list = list(maybe_test_cases)
        for tup_or_list in maybe_test_cases, maybe_test_case_list:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(tup_or_list, protocol=protocol))
                assert restored == tup_or_list, (
                    f'protocol {protocol} failed to recreate instanace'
                )

    def test_identity_inside_containers(self) -> None:
        payload = {'one': [mb_no_42, mb_notuple_no], 'two': (mb_42, mb_tuple_yes)}
        restored = pickle.loads(pickle.dumps(payload))
        assert restored['one'][0] == mb_no_42
        assert restored['one'][1] == mb_notuple_no
        assert restored['two'][0] == mb_42
        assert restored['two'][1] == mb_tuple_yes

    def test_copy_and_deepcopy_return_the_singleton(self) -> None:
        assert copy.copy(maybe_test_cases) == maybe_test_cases
        assert copy.deepcopy(maybe_test_cases) == maybe_test_cases

    def test_repr_reproduces_the_test_cases(self) -> None:
        assert eval(repr(maybe_test_cases)) == maybe_test_cases
