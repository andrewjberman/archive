"""NFRA_CTLPLN round 27 FWD-18, site Z: ONE read of tabulate from SCRATCH_TARGET_Z only (XB-20261016T051708Z-662b step 4).

Run from a folder outside the workspace as:
    PYTHONPATH=<SCRATCH_TARGET_Z> python -s read_from_scratch.py
Prints where tabulate was imported from, its version, and one read-only table: one row per .json receipt in PACK3/receipts.
"""
import glob
import json
import os
import sys

import tabulate

RECEIPTS = r"C:\Users\Opal Bloomberg\opal_intake_r27\PACK3\receipts"

print("sys.path[0:3] =", sys.path[0:3])
print("PYTHONPATH =", os.environ.get("PYTHONPATH"))
print("tabulate.__file__ =", tabulate.__file__)
print("tabulate.__version__ =", tabulate.__version__)

rows = []
for path in sorted(glob.glob(os.path.join(RECEIPTS, "*.json"))):
    with open(path, encoding="utf-8") as fh:
        rec = json.load(fh)
    rows.append([os.path.basename(path), rec.get("schema"), (rec.get("install") or {}).get("rc"),
                 (rec.get("received_sha256") or "")[:12]])
print(tabulate.tabulate(rows, headers=["file", "kind", "rc", "received_sha256[:12]"]))
print("rows:", len(rows))
