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

from pythonic_fp.containers.functional_tuple import FTuple
from pythonic_fp.queues.fifo import FIFOQueue

from pythonic_fp.fptools.either import Either


class TestEitherSequence:
    """Test Either sequence class function"""

    def test_no_rights(self) -> None:
        """Test with only left values"""
        list_of_either_int_str: list[Either[int, str]] = [
            Either.left(x) for x in range(1, 2501)
        ]
        tuple_of_either_int_str: tuple[Either[int, str], ...] = tuple(
            Either.left(x) for x in range(1, 2501)
        )
        ftuple_of_either_int_str: FTuple[Either[int, str]] = FTuple(
            Either.left(x) for x in range(1, 2501)
        )
        fifo_of_either_int_str: FIFOQueue[Either[int, str]] = FIFOQueue(
            Either.left(x) for x in range(1, 2501)
        )

        either_listInt_str = Either.sequence(list_of_either_int_str)
        either_tupleInt_str = Either.sequence(tuple_of_either_int_str)
        either_ftuple_int_str = Either.sequence(ftuple_of_either_int_str)
        either_fifo_int_str = Either.sequence(fifo_of_either_int_str)

        assert either_listInt_str == Either.left(list(range(1, 2501)))
        assert either_tupleInt_str == Either.left(tuple(range(1, 2501)))
        assert either_ftuple_int_str == Either.left(FTuple(range(1, 2501)))
        assert either_fifo_int_str == Either.left(FIFOQueue(range(1, 2501)))

    def test_with_a_right(self) -> None:
        """Test with a single right value, use multiple data structures"""
        list_of_either_int_str: list[Either[int, str]] = [
            Either.right('1'),
            Either.left(2),
            Either.left(3),
            Either.left(4),
        ]
        tuple_of_either_int_str: tuple[Either[int, str], ...] = (
            Either.left(1),
            Either.right('2'),
            Either.left(3),
            Either.left(4),
        )
        ftuple_of_either_int_str = FTuple(
            (Either.left(1), Either.left(2), Either.right('3'), Either.left(4))
        )
        fifo_of_either_int_str = FIFOQueue(
            (Either.left(1), Either.left(2), Either.left(3), Either.right('4'))
        )

        either_list_int = Either.sequence(list_of_either_int_str)
        either_tuple_int = Either.sequence(tuple_of_either_int_str)
        either_ftuple_int = Either.sequence(ftuple_of_either_int_str)
        either_fifo_int: Either[FIFOQueue[int], str] = Either.sequence(fifo_of_either_int_str)

        assert either_list_int == Either.right('1')
        assert either_tuple_int == Either.right('2')
        assert either_ftuple_int == Either.right('3')
        assert either_fifo_int == Either.right('4')

    def test_with_multiple_rights(self) -> None:
        """Test with a multiple right value"""

        type Letter = Either[str, int]
        type Letters = Either[list[str], int]

        ALPHABET: str = ' abcdefghijklmnopqrstuvwxyz'

        def alphabet_position(char_str: str) -> int:
            """Letter position in ALPHABET"""
            char = ' '
            if len(char_str):
                char = char_str[0]
            if 0 < (pos := ord(char) - 96) < 27:
                return pos
            return 0

        def letter_left(letter: str) -> Letter:
            pos = alphabet_position(letter)
            return Either.left(ALPHABET[pos])

        def letter_right(letter: str) -> Letter:
            pos = alphabet_position(letter)
            return Either.right(pos)

        letter_set_0 = list[str]()
        letter_set_1 = ['a', 'w', 's', 's', 'b', 'm', 'j']
        #       letter_set_2 = ['w', 'x', 'y', 'z', ' ']
        #       letter_set_3 = ['waldo', 'x', 'y', 'zebra', '']

        data0 = list(map(letter_left, letter_set_0))
        data1 = list(map(letter_left, letter_set_1))
        data2 = list(data1)
        data2[5] = data2[5].bind(letter_right)

        sequenced_data0 = Either.sequence(data0)
        sequenced_data1 = Either.sequence(data1)
        sequenced_data2: Letters = Either.sequence(data2)

        result0: Letters = Either.left([])
        result1: Letters = Either.left(letter_set_1)
        result2: Letters = Either.right(13)

        assert sequenced_data0 == result0
        assert sequenced_data1 == result1
        assert sequenced_data2 == result2
