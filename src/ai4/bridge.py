from __future__ import annotations
import os, json, pathlib
from typing import Dict, Any
from .core import load_artifact

REG_HOME = pathlib.Path(os.path.expanduser("~/.ai4"))
REG_HOME.mkdir(parents=True, exist_ok=True)
REGISTRY = REG_HOME / "registry.json"

def _load_registry() -> Dict[str, Any]:
    if REGISTRY.exists():
        with open(REGISTRY, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"models": {}}
    return {"models": {}}

def _save_registry(data: Dict[str, Any]) -> None:
    with open(REGISTRY, "w") as f:
        json.dump(data, f, indent=2)

class Bridge4444:
    def __init__(self, cost_per_call:int=1):
        self.cost_per_call = cost_per_call

    def deploy(self, artifact_dir: str, name: str) -> str:
        """Registers a model locally and returns a mat:// URI."""
        reg = _load_registry()
        _ = load_artifact(artifact_dir)  # sanity check it loads
        from .core import hash_artifact
        h = hash_artifact(artifact_dir)
        uri = f"mat://ai4/{name}@{h}"
        reg["models"][uri] = {
            "name": name,
            "artifact": os.path.abspath(artifact_dir),
            "hash": h,
            "calls": 0,
        }
        _save_registry(reg)
        return uri

    def list_models(self):
        return list(_load_registry().get("models", {}).keys())

    def infer(self, uri: str, x: float) -> float:
        reg = _load_registry()
        meta = reg.get("models", {}).get(uri)
        if not meta:
            raise ValueError(f"Unknown model URI: {uri}")
        model = load_artifact(meta["artifact"])
        import numpy as np
        y = model.forward(np.array([[x]], dtype=float))[0,0].item()
        meta["calls"] = int(meta.get("calls", 0)) + 1
        reg["models"][uri] = meta
        _save_registry(reg)
        return y
