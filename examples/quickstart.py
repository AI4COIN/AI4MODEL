from ai4.core import train_toy
from ai4.bridge import Bridge4444
from ai4.token import Ledger

artifact = train_toy(epochs=20, out_dir="artifacts/quickstart")
uri = Bridge4444().deploy(artifact, name="quickstart")
print("Deployed:", uri)

ledger = Ledger()
ledger.mint("you", 3)
print("Balance:", ledger.balance_of("you"))
