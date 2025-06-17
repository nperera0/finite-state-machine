import logging
from fsm import FSM

logging.basicConfig(level=logging.INFO)


class ModThreeFSM(FSM):
    def __init__(self) -> None:
        states = ['0', '1', '2']  # represent remainder states as strings
        alphabet = ['0', '1']
        initial_state = '0'
        final_states = states  # all states valid as "final" for remainder
        transitions = {
            '0': {'0': '0', '1': '1'},
            '1': {'0': '2', '1': '0'},
            '2': {'0': '1', '1': '2'},
        }
        super().__init__(states, alphabet, initial_state, final_states, transitions)

    def run(self, binary_string: str) -> int:
        self.reset()
        super().run(binary_string)
        final_state: str = self.get_final_state()
        return int(final_state)


# Example usage:
if __name__ == "__main__":
    fsm = ModThreeFSM()
    binary_input = "1101"  # 13 decimal, 13 % 3 == 1
    remainder = fsm.run(binary_input)
    print(f"Remainder of binary '{binary_input}' mod 3 is: {remainder}")
