"""AMGT_RESAPP round 44, AMGT-rs-1 AC1 -- every SERVED case in the export carries the currency of the price it is banded against.
Over round 44's fixed capture (C:/tmp/amgt-r43-live95: the LIVE research library, 95 folders, read_at 2026-09-26T03:55:02Z, each page
capture saved beside the Model block read at the same moment), the export is REBUILT in process from this tree (round44/checks/sweep.py's
rebuild) and, for each case the payload serves as SERVED, the export's line for that case must carry the name's CRNCY (the header figure
the page's Price tile prints) right after the value. Prints the denominator. usage (repo root): PYTHONPATH="$(pwd)" python <this>"""
import importlib.util
import json
import sys
from pathlib import Path

CACHE = Path("C:/tmp/amgt-r43-live95")
spec = importlib.util.spec_from_file_location("sweep", "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round44/checks/sweep.py")
sweep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep)

served = carried = 0
misses = []
for d in sorted(p for p in CACHE.iterdir() if p.is_dir()):
    fx = next(iter(sorted((d / "served").glob("served_fixture.*.json"))), None)
    if fx is None:
        continue
    bundle = json.loads(fx.read_text(encoding="utf-8"))
    key = bundle.get("security_key") or d.name
    cases = ((bundle.get("thesis") or {}).get("model_cases") or {})
    crncy = next((f.get("value") for f in ((bundle.get("overlay") or {}).get("header_figures") or [])
                  if f.get("mnemonic") == "CRNCY"), None)
    targets = [(n, cases.get(n.lower()) or {}) for n in ("Upside", "Base", "Downside")]
    targets = [(n, c) for n, c in targets if c.get("status") == "SERVED"]
    if not targets:
        continue
    out = d / "rs1.local.rich.md"
    err = sweep.rebuild(key, fx, out)
    text = out.read_text(encoding="utf-8") if not err else ""
    for name, case in targets:
        served += 1
        line = next((ln for ln in text.splitlines() if ln.startswith("%s case: SERVED -- " % name)), "")
        ok = bool(crncy) and ("%s %s" % (case.get("value"), crncy)) in line
        carried += ok
        if not ok:
            misses.append("%s %s crncy=%s line=%r" % (key, name, crncy, line[:120]))
print("served cases carrying their price currency: %d of %d" % (carried, served))
for m in misses[:12]:
    print("  " + m)
sys.exit(0 if served and carried == served else 1)
