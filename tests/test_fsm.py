import unittest
from fsm import FSM  # assuming your FSM class is in fsm.py

class TestFSM(unittest.TestCase):

    def setUp(self):
        self.states = ['S0', 'S1', 'S2']
        self.alphabet = ['0', '1']
        self.initial_state = 'S0'
        self.final_states = ['S2']
        self.transitions = {
            'S0': {'0': 'S0', '1': 'S1'},
            'S1': {'0': 'S2', '1': 'S1'},
            'S2': {'0': 'S2', '1': 'S2'}
        }

    # --- Basic Functionality Tests ---
    def test_valid_fsm_creation(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        self.assertEqual(fsm.current_state, 'S0')

    def test_invalid_initial_state(self):
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, 'SX', self.final_states, self.transitions)

    def test_invalid_final_state(self):
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, self.initial_state, ['SX'], self.transitions)

    def test_invalid_transition_state(self):
        bad_transitions = {
            'S0': {'0': 'S0', '1': 'S1'},
            'S9': {'0': 'S2'}  # Invalid source state
        }
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, bad_transitions)

    def test_invalid_transition_symbol(self):
        bad_transitions = {
            'S0': {'0': 'S0', '2': 'S1'},  # '2' not in alphabet
        }
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, bad_transitions)

    def test_transition_valid(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        fsm.transition('1')
        self.assertEqual(fsm.current_state, 'S1')

    def test_transition_invalid_symbol(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        with self.assertRaises(ValueError):
            fsm.transition('2')

    def test_transition_no_transition(self):
        incomplete_transitions = {
            'S0': {'0': 'S0'}
        }
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, incomplete_transitions)
        with self.assertRaises(ValueError):
            fsm.transition('1')

    def test_run_valid_input(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        final = fsm.run('10')
        self.assertEqual(final, 'S2')
        self.assertEqual(fsm.get_final_state(), 'S2')

    def test_run_invalid_input(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        with self.assertRaises(ValueError):
            fsm.run('102')  # '2' is invalid

    def test_get_final_state_invalid(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        fsm.run('1')  # Lands on S1
        with self.assertRaises(ValueError):
            fsm.get_final_state()

    def test_reset(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        fsm.run('10')
        fsm.reset()
        self.assertEqual(fsm.current_state, self.initial_state)

    # --- Edge Cases ---
    def test_empty_input_string(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        result = fsm.run("")
        self.assertEqual(result, 'S0')
        with self.assertRaises(ValueError):
            fsm.get_final_state()

    def test_input_leads_to_non_final_state(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        fsm.run("1")  # S0 --1--> S1 (not a final state)
        with self.assertRaises(ValueError):
            fsm.get_final_state()

    def test_no_transitions_defined(self):
        transitions = {}
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, self.initial_state, self.final_states, transitions)

    def test_partial_transitions(self):
        transitions = {
            'S0': {'0': 'S1'},  # '1' is missing
            'S1': {'0': 'S2'},
            'S2': {}
        }
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, transitions)
        with self.assertRaises(ValueError):
            fsm.run("01")  # No transition on '1' from S1

    def test_duplicate_states_symbols(self):
        states = ['S0', 'S0', 'S1']
        alphabet = ['0', '0', '1']
        transitions = {
            'S0': {'0': 'S0', '1': 'S1'},
            'S1': {'0': 'S1'}
        }
        fsm = FSM(states, alphabet, 'S0', ['S1'], transitions)
        result = fsm.run("01")
        self.assertEqual(result, 'S1')

    def test_self_loop_transition(self):
        transitions = {
            'S0': {'0': 'S0', '1': 'S1'},
            'S1': {'0': 'S1', '1': 'S1'},
            'S2': {}
        }
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, transitions)
        result = fsm.run("00001")
        self.assertEqual(result, 'S1')

    def test_correct_initial_state_used(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        fsm.run("1")  # S0 -> S1
        fsm.reset()
        self.assertEqual(fsm.current_state, 'S0')

    def test_state_with_empty_transition_dict(self):
        transitions = {
            'S0': {'0': 'S1'},
            'S1': {},  # No transitions defined for S1
            'S2': {'0': 'S2'}
        }
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, transitions)
        fsm.run("0")  # S0 -> S1
        with self.assertRaises(ValueError):
            fsm.transition('0')  # No transition defined for '0' from S1

    def test_multiple_resets(self):
        fsm = FSM(self.states, self.alphabet, self.initial_state, self.final_states, self.transitions)
        fsm.run('10')
        fsm.reset()
        self.assertEqual(fsm.current_state, 'S0')
        fsm.reset()
        self.assertEqual(fsm.current_state, 'S0')

    # --- Input validation Tests ---
    def test_empty_states(self):
        with self.assertRaises(ValueError):
            FSM([], self.alphabet, self.initial_state, self.final_states, self.transitions)

    def test_empty_alphabet(self):
        with self.assertRaises(ValueError):
            FSM(self.states, [], self.initial_state, self.final_states, self.transitions)

    def test_empty_initial_state(self):
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, '', self.final_states, self.transitions)

    def test_none_initial_state(self):
        with self.assertRaises(ValueError):
            FSM(self.states, self.alphabet, None, self.final_states, self.transitions)

    def test_empty_final_states_allowed(self):
        # No error expected, but no accepting states
        fsm = FSM(self.states, self.alphabet, self.initial_state, [], self.transitions)
        fsm.run('10')
        with self.assertRaises(ValueError):
            fsm.get_final_state()  # because current_state won't be in final_states

if __name__ == '__main__':
    unittest.main()
