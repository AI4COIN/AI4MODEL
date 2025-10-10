from __future__ import annotations
import argparse, sys
from .core import train_toy, evaluate_toy
from .bridge import Bridge4444
from .token import Ledger

def main(argv=None):
    argv = argv or sys.argv[1:]
    p = argparse.ArgumentParser(prog="ai4", description="AI4: model-backed token demo for 4444.four")
    sub = p.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("train", help="train a tiny toy model")
    pt.add_argument("--epochs", type=int, default=100)
    pt.add_argument("--hidden", type=int, default=4)
    pt.add_argument("--out", required=True, help="artifact output directory")

    pe = sub.add_parser("evaluate", help="evaluate a saved artifact")
    pe.add_argument("--artifact", required=True)

    pd = sub.add_parser("deploy", help="register model to the 4444.four mock")
    pd.add_argument("--artifact", required=True)
    pd.add_argument("--name", required=True)

    pi = sub.add_parser("infer", help="run inference against a deployed model URI")
    pi.add_argument("--uri", required=True)
    pi.add_argument("--input", type=float, required=True)
    pi.add_argument("--payer", default="you", help="who pays the MAT cost")
    pi.add_argument("--cost", type=int, default=1)

    pm = sub.add_parser("mint", help="mint Model Access Tokens (MAT) locally")
    pm.add_argument("--to", required=True)
    pm.add_argument("--amount", type=int, required=True)

    ptf = sub.add_parser("transfer", help="transfer MAT between identities")
    ptf.add_argument("--from", dest="sender", required=True)
    ptf.add_argument("--to", required=True)
    ptf.add_argument("--amount", type=int, required=True)

    pb = sub.add_parser("balance", help="show MAT balance for an identity")
    pb.add_argument("--who", required=True)

    pl = sub.add_parser("list", help="list deployed models")

    args = p.parse_args(argv)

    if args.cmd == "train":
        out = train_toy(epochs=args.epochs, hidden=args.hidden, out_dir=args.out)
        print(out)
    elif args.cmd == "evaluate":
        loss = evaluate_toy(args.artifact)
        print(f"MSE: {loss:.6f}")
    elif args.cmd == "deploy":
        uri = Bridge4444().deploy(args.artifact, name=args.name)
        print(uri)
    elif args.cmd == "infer":
        # charge cost via ledger
        ledger = Ledger()
        if ledger.balance_of(args.payer) < args.cost:
            sys.exit("insufficient MAT balance for inference")
        ledger.burn(args.payer, args.cost)
        y = Bridge4444().infer(args.uri, args.input)
        print(y)
    elif args.cmd == "mint":
        Ledger().mint(args.to, args.amount)
        print(f"Minted {args.amount} AI4 to {args.to}")
    elif args.cmd == "transfer":
        Ledger().transfer(args.sender, args.to, args.amount)
        print("ok")
    elif args.cmd == "balance":
        print(Ledger().balance_of(args.who))
    elif args.cmd == "list":
        for uri in Bridge4444().list_models():
            print(uri)
