import logging

class FSM:
    """
    Generic Finite State Machine class.

    Args:
        states (list): List of states.
        alphabet (list): List of input symbols.
        initial_state (str): Initial state name.
        final_states (list): List of final/accepting states.
        transitions (dict): Dict mapping state and input to next state.

    Raises:
        ValueError: On invalid configuration or transitions.
    """

    def __init__(
        self,
        states: list[str],
        alphabet: list[str],
        initial_state: str,
        final_states: list[str],
        transitions: dict[str, dict[str, str]]
    ) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        if initial_state not in states:
            raise ValueError(f"Invalid initial state: '{initial_state}' not in states.")
        for fs in final_states:
            if fs not in states:
                raise ValueError(f"Invalid final state: '{fs}' not in states.")
        if not self._validate_transitions(states, alphabet, transitions):
            raise ValueError("Invalid transitions.")

        self.states: list[str] = states
        self.alphabet: list[str] = alphabet
        self.initial_state: str = initial_state
        self.current_state: str = initial_state
        self.final_states: list[str] = final_states
        self.transitions: dict[str, dict[str, str]] = transitions

    @staticmethod
    def _validate_transitions(
        states: list[str],
        alphabet: list[str],
        transitions: dict[str, dict[str, str]]
    ) -> bool:
        if not transitions:
            return False

        for state, trans in transitions.items():
            if state not in states:
                return False
            for symbol, target in trans.items():
                if symbol not in alphabet or target not in states:
                    return False
        return True

    def transition(self, input_symbol: str) -> None:
        if input_symbol not in self.alphabet:
            raise ValueError(f"Invalid input symbol: '{input_symbol}'")

        if self.current_state not in self.transitions:
            raise ValueError(f"No transitions defined from current state: '{self.current_state}'")

        if input_symbol not in self.transitions[self.current_state]:
            raise ValueError(f"No transition for symbol '{input_symbol}' from state '{self.current_state}'")

        next_state: str = self.transitions[self.current_state][input_symbol]
        self.logger.info(f"Transitioning from '{self.current_state}' to '{next_state}' on symbol '{input_symbol}'")
        self.current_state = next_state

    def run(self, input_string: str) -> str:
        self.current_state = self.initial_state
        for symbol in input_string:
            self.transition(symbol)
        return self.current_state

    def reset(self) -> None:
        self.current_state = self.initial_state

    def get_final_state(self) -> str:
        if self.current_state not in self.final_states:
            raise ValueError(f"Invalid final state encountered '{self.current_state}'")
        return self.current_state
