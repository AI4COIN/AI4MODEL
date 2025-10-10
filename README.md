<!--
  AI4MODEL README (styled)
  Repo: AI4
-->

<p align="center">
  <img src="assets/ai4model-logo.png" alt="AI4MODEL" width="520">
</p>

<h1 align="center">AI4MODEL</h1>
<p align="center">Model-backed access tokens on the fictional <b>4444.four</b> network. <br>Train → Package → Deploy → Meter with <b>$AI4</b>.</p>
<p align="center"> 0x4e94837171e9eDc02Cad8F74a199B5f2f1394444  </p>

<p align="center">
  <a href="https://twitter.com/AI4MODEL"><img alt="Follow on X" src="https://img.shields.io/badge/follow-@AI4MODEL-1DA1F2?logo=x&logoColor=white"></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-black"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue">
  <img alt="CI" src="https://img.shields.io/badge/CI-GitHub%20Actions-grey">
  <img alt="Token" src="https://img.shields.io/badge/token-%24AI4-yellow">
</p>

> **Heads‑up**: This project is a teaching **proof‑of‑concept**. 4444.four is mocked locally. $AI4 here represents *usage credits*, not a financial instrument.

---

## TL;DR

- Tiny NumPy model (Linear → GELU → Linear)
- Deterministic artifacts (`weights.npz` + `manifest.json`)
- Local **4444.four** mock with `mat://` URIs
- JSON‑backed **Model Access Token** ledger (**$AI4**)
- Clean CLI for the full flow

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"

# train + evaluate
ai4 train --epochs 50 --out artifacts/demo
ai4 evaluate --artifact artifacts/demo

# deploy to the 4444.four mock
ai4 deploy --artifact artifacts/demo --name demo-linear
# -> mat://ai4/demo-linear@<hash>

# mint usage credits and run inference
ai4 mint --to you --amount 100
ai4 balance --who you
ai4 infer --uri mat://ai4/demo-linear@<hash> --input 0.42
```

### CLI Cheatsheet

```
ai4 train      # Train a toy model and save an artifact
ai4 evaluate   # Evaluate an artifact on synthetic data
ai4 deploy     # Register the artifact in the 4444.four mock, returns mat:// URI
ai4 infer      # Run inference; debits 1 $AI4 by default
ai4 mint       # Mint $AI4 credits in the local ledger
ai4 transfer   # Transfer $AI4 between identities
ai4 balance    # Show an identity's balance
ai4 list       # List deployed models
```

---

## What is AI4MODEL?

**AI4MODEL** is a compact, workshop‑friendly reference that explores *model‑as‑an‑asset* ideas:

- **Artifacts**: portable model + metadata
- **Access as a token**: **$AI4** = *Model Access Token* (usage credit)
- **URIs**: `mat://ai4/<name>@<hash>`
- **Local first**: no external services required to demo the concept

> The “4444.four” endpoints are emulated locally and persist under `~/.ai4/`.

---

## Token: $AI4 (Model Access Token)

- **Type**: usage credit for inference on the mocked 4444.four
- **Ledger**: local JSON file (see `src/ai4/token.py`)
- **Reference contract**: `contracts/AI4Token.sol` (ERC‑20‑like, testnet/demo only)
- **Default pricing**: `1 $AI4` per inference (configurable at the CLI)

> Not audited. Not an investment product. Educational only.

---

## Architecture

```
src/ai4
├── core.py        # Tiny numpy model + train/eval + serialize/deserialize
├── bridge.py      # 4444.four mock: deploy() / infer() / list_models()
├── token.py       # JSON‑backed $AI4 ledger
└── cli.py         # Argparse CLI wiring
```

- **Artifacts**: `weights.npz` + `manifest.json`
- **Registry**: `~/.ai4/registry.json`
- **Metering**: debits $AI4 on each inference

---

## Mock API (4444.four)

- `POST /deploy` → `Bridge4444.deploy(artifact_dir, name)`
- `POST /inference` → `Bridge4444.infer(uri, x)`

> Swap `bridge.py` with HTTP calls if you later host a real service.

---

## Roadmap (nice‑to‑have)

- [ ] Pluggable pricing per model
- [ ] Multi‑input support & simple schemas
- [ ] Optional remote registry backend
- [ ] Deterministic artifact signing

---

## Community & Links

- **X (Twitter)**: https://twitter.com/AI4MODEL  
- **Issues**: use GitHub Issues for bugs & ideas  
- **License**: MIT

---

### Security & Ethics

This is a **teaching** repo. Do not misrepresent it as a live network or a financial product.
