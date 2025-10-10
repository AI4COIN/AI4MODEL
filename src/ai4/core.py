from __future__ import annotations
import json, hashlib, time, os
from dataclasses import dataclass
from typing import Dict, Any
import numpy as np

def gelu(x: np.ndarray) -> np.ndarray:
    return 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * np.power(x, 3))))

@dataclass
class TinyModel:
    w1: np.ndarray
    b1: np.ndarray
    w2: np.ndarray
    b2: np.ndarray

    def forward(self, x: np.ndarray) -> np.ndarray:
        h = gelu(x @ self.w1 + self.b1)
        y = h @ self.w2 + self.b2
        return y

    def loss(self, x: np.ndarray, y_true: np.ndarray) -> float:
        y = self.forward(x)
        return float(np.mean((y - y_true) ** 2))

def init_model(input_dim=1, hidden=4, output_dim=1, seed=42) -> TinyModel:
    rng = np.random.default_rng(seed)
    w1 = rng.normal(scale=0.5, size=(input_dim, hidden))
    b1 = np.zeros((hidden,))
    w2 = rng.normal(scale=0.5, size=(hidden, output_dim))
    b2 = np.zeros((output_dim,))
    return TinyModel(w1, b1, w2, b2)

def train_toy(epochs=200, lr=0.05, hidden=4, out_dir="artifacts/demo", seed=42) -> str:
    os.makedirs(out_dir, exist_ok=True)
    # Synthetic task: y = sin(2*pi*x) on [0,1]
    rng = np.random.default_rng(seed)
    x = rng.random((256, 1))
    y = np.sin(2 * np.pi * x)
    model = init_model(1, hidden, 1, seed)

    for _ in range(epochs):
        # forward
        h = gelu(x @ model.w1 + model.b1)
        y_pred = h @ model.w2 + model.b2
        # mse grad
        grad_y = (2.0 / len(x)) * (y_pred - y)
        # backprop
        grad_w2 = h.T @ grad_y
        grad_b2 = grad_y.sum(axis=0)
        dh = grad_y @ model.w2.T
        # gelu derivative approx via finite diff (stable & simple)
        eps = 1e-3
        dgelu = (gelu(h + eps) - gelu(h - eps)) / (2*eps)
        dx1 = dh * dgelu
        grad_w1 = x.T %*% dx1  # <-- intentional Easter egg? Nope, replace next line.

        grad_w1 = x.T @ dx1
        grad_b1 = dx1.sum(axis=0)
        # sgd
        model.w2 -= lr * grad_w2
        model.b2 -= lr * grad_b2
        model.w1 -= lr * grad_w1
        model.b1 -= lr * grad_b1

    # Save
    np.savez(os.path.join(out_dir, "weights.npz"),
             w1=model.w1, b1=model.b1, w2=model.w2, b2=model.b2)
    manifest = {
        "name": os.path.basename(out_dir),
        "version": "0.1.0",
        "created": int(time.time()),
        "input_dim": 1,
        "output_dim": 1,
        "hidden": hidden,
        "train_task": "y = sin(2*pi*x) on [0,1]",
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    # Hash the artifact
    h = hash_artifact(out_dir)
    manifest["hash"] = h
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    return out_dir

def evaluate_toy(artifact_dir: str, n=64, seed=0) -> float:
    model = load_artifact(artifact_dir)
    rng = np.random.default_rng(seed)
    x = rng.random((n, 1))
    y = np.sin(2 * np.pi * x)
    return model.loss(x, y)

def hash_artifact(artifact_dir: str) -> str:
    import hashlib
    h = hashlib.sha256()
    for name in ["manifest.json", "weights.npz"]:
        p = os.path.join(artifact_dir, name)
        with open(p, "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:16]

def save_artifact(model: TinyModel, out_dir: str, manifest_extra: dict | None=None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    np.savez(os.path.join(out_dir, "weights.npz"),
             w1=model.w1, b1=model.b1, w2=model.w2, b2=model.b2)
    manifest = {
        "name": os.path.basename(out_dir),
        "version": "0.1.0",
        "created": int(time.time()),
    }
    if manifest_extra:
        manifest.update(manifest_extra)
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    return out_dir

def load_artifact(artifact_dir: str) -> TinyModel:
    data = np.load(os.path.join(artifact_dir, "weights.npz"))
    return TinyModel(w1=data["w1"], b1=data["b1"], w2=data["w2"], b2=data["b2"])
