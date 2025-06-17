# FSM – Generic Finite State Machine

A lightweight, object-oriented Finite State Machine (FSM) implementation in Python. Designed for developers to build custom FSMs using clearly defined states, symbols, and transitions.

## ✨ Features

- Validate states, alphabet, and transitions on initialization
- Transition safely with error handling
- Support for reset and run methods
- Logging of state transitions
- Easily testable and extendable

---

## 🔧 Installation

This is a self-contained Python class. Simply copy `fsm.py` into your project.

```bash

fsm/
├── fsm.py                # Generic FSM base class
├── mod_three_fsm.py      # Mod-3 FSM subclass (uses FSM.py)
├── tests/
│   ├── test_fsm.py           # Tests for generic FSM class
│   └── test_mod_three_fsm.py # Tests specifically for ModThreeFSM
├── README.md             # Project overview, usage instructions
├── requirements.txt      # Optional: list dependencies (e.g. pytest, coverage)
└── .gitignore            # Ignore __pycache__, .env, etc.
```

---

## 🧱 FSM Constructor

```python
FSM(states, alphabet, initial_state, final_states, transitions)
```

### Parameters

| Name            | Type    | Description                                  |
|-----------------|---------|----------------------------------------------|
| `states`        | `list`  | All possible states of the FSM               |
| `alphabet`      | `list`  | Valid input symbols                          |
| `initial_state` | `str`   | The state the FSM starts in                  |
| `final_states`  | `list`  | Accepting states (for validation)            |
| `transitions`   | `dict`  | Mapping of `{state: {symbol: next_state}}`   |

### Raises

- `ValueError` for any invalid initial state, final state, or malformed transition table.

---

## 🚦 Example

```python
from fsm import FSM

states = ['S0', 'S1', 'S2']
alphabet = ['0', '1']
initial_state = 'S0'
final_states = ['S2']
transitions = {
    'S0': {'0': 'S0', '1': 'S1'},
    'S1': {'0': 'S2', '1': 'S1'},
    'S2': {'0': 'S2', '1': 'S2'}
}

fsm = FSM(states, alphabet, initial_state, final_states, transitions)

result = fsm.run('10')
print("Final State:", result)
print("Accepted:", fsm.get_final_state() in final_states)  # True
```

---

## 🔁 API Methods

| Method              | Description                                                      |
|---------------------|------------------------------------------------------------------|
| `transition(symbol)`| Applies a single symbol and updates state                        |
| `run(input_string)` | Runs a sequence of symbols from the initial state               |
| `reset()`           | Resets the FSM to its initial state                             |
| `get_final_state()` | Returns the current state, raises error if not in final states  |

---

## 🧪 Running Unit Tests

Unit tests are included in `test_fsm.py` using the `unittest` module.

```bash
python -m unittest tests/test_fsm.py
```

---

## 📜 License

MIT License. Use freely in personal or commercial projects.

---

## 🙋‍♂️ Author

Built by Nisal Perera — pull requests and contributions welcome!
