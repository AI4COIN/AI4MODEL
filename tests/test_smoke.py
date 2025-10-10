import os
from ai4.core import train_toy, evaluate_toy
from ai4.bridge import Bridge4444
from ai4.token import Ledger

def test_flow(tmp_path):
    art = train_toy(epochs=3, out_dir=tmp_path.as_posix())
    assert os.path.exists(os.path.join(art, "weights.npz"))
    loss = evaluate_toy(art)
    assert loss >= 0.0
    uri = Bridge4444().deploy(art, name="t")
    assert uri.startswith("mat://ai4/")
    L = Ledger()
    L.mint("tester", 2)
    assert L.balance_of("tester") == 2
