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

"""Pickle and cross process tests for MayBe."""

import copy
import os
import pickle
import subprocess
import sys

import pytest

from pythonic_fp.fptools.maybe import MayBe

mb_no_str = MayBe[str]()
mb_str = MayBe('forty-two')

mb_no_tuple = MayBe[tuple[int, str]]()
mb_tuple = MayBe((42, 'Forty-Two'))

mb_notuple_no = MayBe(((mb_no_tuple, 0), 'no'))
mb_tuple_yes = MayBe(((mb_tuple, 0), 'yes'))

maybe_test_cases = (mb_no_str, mb_str, mb_no_tuple, mb_tuple, mb_notuple_no, mb_tuple_yes)


class TestMayBePickle:
    def test_equality_survives_all_protocols(self) -> None:
        for mb in maybe_test_cases:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(mb, protocol=protocol))
                assert restored == mb, (
                    f'protocol {protocol} failed to recreate instance'
                )

    def test_collections_of_maybe_round_trip(self) -> None:
        maybe_test_case_list = list(maybe_test_cases)
        for tup_or_list in maybe_test_cases, maybe_test_case_list:
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(tup_or_list, protocol=protocol))
                assert restored == tup_or_list, (
                    f'protocol {protocol} failed to recreate instance'
                )

    def test_emptiness_survives_all_protocols(self) -> None:
        for mb in (mb_no_str, mb_no_tuple):
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                restored = pickle.loads(pickle.dumps(mb, protocol=protocol))
                assert not restored, f'protocol {protocol} made an empty MayBe truthy'

    def test_nested_in_containers(self) -> None:
        payload = {'one': [mb_no_str, mb_notuple_no], 'two': (mb_str, mb_tuple_yes)}
        restored = pickle.loads(pickle.dumps(payload))
        assert restored['one'][0] == mb_no_str
        assert restored['one'][1] == mb_notuple_no
        assert restored['two'][0] == mb_str
        assert restored['two'][1] == mb_tuple_yes

    def test_copy_and_deepcopy_return_equal_maybe(self) -> None:
        assert copy.copy(maybe_test_cases) == maybe_test_cases
        assert copy.deepcopy(maybe_test_cases) == maybe_test_cases

    def test_repr_reproduces_the_test_cases(self) -> None:
        assert eval(repr(maybe_test_cases)) == maybe_test_cases

    def test_unhashable_contents(self) -> None:
        mb_list = MayBe([1, 2])
        with pytest.raises(TypeError):
            hash(mb_list)
        restored = pickle.loads(pickle.dumps(mb_list))
        assert restored == mb_list
        with pytest.raises(TypeError):
            hash(restored)



_DUMP = """
import pickle, sys
from pythonic_fp.fptools.maybe import MayBe
mb = MayBe('forty-two')
hash(mb)
sys.stdout.buffer.write(pickle.dumps(mb))
"""

_LOAD = """
import pickle, sys
from pythonic_fp.fptools.maybe import MayBe
restored = pickle.loads(sys.stdin.buffer.read())
fresh = MayBe('forty-two')
assert restored == fresh, 'unpickled MayBe not equal to a fresh one'
assert hash(restored) == hash(fresh), 'stale hash carried across the pickle'
assert len({restored, fresh}) == 1, 'equal MayBe instances landed in two set slots'
print('ok')
"""


def _run(script, seed, data=None):
    env = dict(os.environ, PYTHONHASHSEED=seed)
    return subprocess.run(
        [sys.executable, '-c', script],
        input=data,
        env=env,
        capture_output=True,
        check=True,
    )


class TestMayBePickleAcrossProcesses:
    def test_hash_not_carried_across_processes(self) -> None:
        """A cached hash must not survive into a process with another hash seed."""
        blob = _run(_DUMP, seed='1').stdout
        done = _run(_LOAD, seed='2', data=blob)
        assert done.stdout.strip() == b'ok'
