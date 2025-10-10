from __future__ import annotations
import json, pathlib
from typing import Dict

LEDGER_FILE = pathlib.Path.home() / ".ai4" / "ledger.json"
LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)

def _read() -> Dict[str, int]:
    if LEDGER_FILE.exists():
        try:
            with open(LEDGER_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def _write(data: Dict[str, int]) -> None:
    with open(LEDGER_FILE, "w") as f:
        json.dump(data, f, indent=2)

class Ledger:
    symbol = "AI4"
    def __init__(self):
        self._state = _read()

    def mint(self, to: str, amount: int) -> None:
        self._state[to] = int(self._state.get(to, 0)) + int(amount)
        _write(self._state)

    def burn(self, who: str, amount: int) -> None:
        if self._state.get(who, 0) < amount:
            raise ValueError("insufficient balance")
        self._state[who] -= int(amount)
        _write(self._state)

    def transfer(self, sender: str, recipient: str, amount: int) -> None:
        if self._state.get(sender, 0) < amount:
            raise ValueError("insufficient balance")
        self._state[sender] -= int(amount)
        self._state[recipient] = int(self._state.get(recipient, 0)) + int(amount)
        _write(self._state)

    def balance_of(self, who: str) -> int:
        return int(self._state.get(who, 0))
