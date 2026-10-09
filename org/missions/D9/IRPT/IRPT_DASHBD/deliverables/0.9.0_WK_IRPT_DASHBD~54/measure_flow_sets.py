"""TO-DB-b-77 measurement driver. Runs round 36's adapter (~49/orion_account_return_daily.py) UNCHANGED apart from one inserted
read-only block that re-uses its own compound()/probe_net() on the same sample, once per flow set. S3 reads only; the adapter's
local outputs go to the scratch dir. Usage (repo root):
  python <this file> --registry-key inflection --end 2026-10-08 --scratch .scratch --effect <MEASURED_EFFECT.json path>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "0.9.0_WK_IRPT_DASHBD~49" / "orion_account_return_daily.py"
ANCHOR = "    # --- lots\n"
BLOCK = '''    effect_path = Path(EFFECT_PATH)
    sets = {
        "ratified": {"net": ("ext",), "gross": ("ext", "fee")},
        "ratified_plus_journal": {"net": ("ext", "journal"), "gross": ("ext", "journal", "fee")},
        "ratified_plus_tax": {"net": ("ext", "tax"), "gross": ("ext", "tax", "fee")},
        "proposed": {"net": ("ext", "journal", "tax"), "gross": ("ext", "journal", "tax", "fee")},
    }
    measured = {}
    for label, by_basis in sets.items():
        measured[label] = {b: {"parts": list(p), "within": probe_net(p, years),
                               "computable": int((compound(p)[1] == 0).sum())} for b, p in by_basis.items()}
    import json as _json
    effect_path.write_text(_json.dumps({"_measured": measured, "_denominator": int(na)}, indent=1) + chr(10), encoding="utf-8")
    print("EFFECT " + _json.dumps(measured))
'''
text = SRC.read_bytes().decode("utf-8")
if text.count(ANCHOR) != 1:
    raise SystemExit("REFUSED: anchor not unique in %s" % SRC)
argv = sys.argv[1:]
EFFECT = argv[argv.index("--effect") + 1]
del argv[argv.index("--effect"):argv.index("--effect") + 2]
text = text.replace(ANCHOR, BLOCK + ANCHOR).replace("EFFECT_PATH", repr(EFFECT))
g = {"__file__": str(SRC), "__name__": "adapter_probe"}
exec(compile(text, str(SRC), "exec"), g)
g["main"](argv + ["--record", str(Path(EFFECT).with_name("adapter_record_scratch.json"))] if "--record" not in argv else argv)
