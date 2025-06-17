import unittest
from mod_three_fsm import ModThreeFSM  # Adjust the import path if needed


class TestModThreeFSM(unittest.TestCase):

    def setUp(self):
        self.fsm = ModThreeFSM()

    def test_empty_string(self):
        # Empty input, should stay in initial state '0' → remainder 0
        self.assertEqual(self.fsm.run(''), 0)

    def test_single_bits(self):
        self.assertEqual(self.fsm.run('0'), 0)
        self.assertEqual(self.fsm.run('1'), 1)

    def test_known_binaries(self):
        # binary 1101 = decimal 13, remainder 1 when divided by 3
        self.assertEqual(self.fsm.run('1101'), 1)

        # binary 1001 = decimal 9, remainder 0
        self.assertEqual(self.fsm.run('1001'), 0)

        # binary 111 = decimal 7, remainder 1
        self.assertEqual(self.fsm.run('111'), 1)

        # binary 1010 = decimal 10, remainder 1
        self.assertEqual(self.fsm.run('1010'), 1)

        # binary 0 (single zero)
        self.assertEqual(self.fsm.run('0'), 0)

    def test_all_mod3_results(self):
        # Test some binaries that map to all three possible remainders
        # remainder 0 examples
        for binary in ['0', '11', '110', '1001']:
            self.assertEqual(self.fsm.run(binary), 0)

        # remainder 1 examples
        for binary in ['1', '100', '1101', '1010']:
            self.assertEqual(self.fsm.run(binary), 1)

        # remainder 2 examples
        for binary in ['10', '101', '1110', '1000']:
            self.assertEqual(self.fsm.run(binary), 2)

    def test_invalid_input(self):
        # Input contains symbols outside '0' and '1', should raise ValueError
        with self.assertRaises(ValueError):
            self.fsm.run('2')

        with self.assertRaises(ValueError):
            self.fsm.run('abc')

        with self.assertRaises(ValueError):
            self.fsm.run('10a01')

    def test_consecutive_runs(self):
        self.assertEqual(self.fsm.run('110'), 0)
        self.assertEqual(self.fsm.run('1'), 1)  # should not be affected by previous run
        self.assertEqual(self.fsm.run('10'), 2)

    def test_long_binary_string(self):
        binary = '1' * 100  # 100 ones
        # Sum of bits = 100 → 100 % 3 = 1
        self.assertEqual(self.fsm.run(binary), 0)

    def test_leading_zeros(self):
        self.assertEqual(self.fsm.run('0000'), 0)
        self.assertEqual(self.fsm.run('0011'), 0)  # same as '11'
        self.assertEqual(self.fsm.run('0001101'), 1)  # same as '1101'

if __name__ == '__main__':
    unittest.main()
