"""Negative control for the import proof: import one closure module from a BUILT bundle tree under python -I.

Usage: python -I -B mutant_probe.py <tree_root> <label>
The old pin's bundle lacks silver/opal_unidentified.py; the import of build_cottonwood_mdpf_slice must fail there
with ModuleNotFoundError, and succeed on the new pin's bundle tree.
"""
import importlib
import json
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [
    str(tree / "data/assets/scripts/gold/investor_reporting"),
    str(tree / "lib"),
    str(tree / "data/assets/scripts/gold"),
    str(tree / "data/assets/scripts/silver"),
]
try:
    importlib.import_module("build_cottonwood_mdpf_slice")
    print(json.dumps({"tree": sys.argv[2], "module": "build_cottonwood_mdpf_slice", "ok": True}))
except BaseException as e:
    print(json.dumps({"tree": sys.argv[2], "module": "build_cottonwood_mdpf_slice", "ok": False,
                      "error": type(e).__name__ + ": " + str(e)[:200]}))
