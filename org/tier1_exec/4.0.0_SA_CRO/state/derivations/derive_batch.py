"""Generalized RCG batch derivation: ALL remaining tracked ARCHIVE labels, unit-grouped
(thread grain under org/threads/, immediate-parent-dir grain elsewhere), greedy
directory-complete cut <= cap, org/threads/ units first (finish that cohort).
Usage: derive_batch.py <batch_lower_id e.g. b0005> [cap]
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import OrderedDict, defaultdict
from pathlib import Path

WS = Path(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
# Outputs are TRANSIENT intermediates (the durable copy of a batch list is its
# BATCHES.jsonl row) -- they go to RCG_OUT_DIR or system temp, NEVER this repo dir.
SCRATCH = Path(os.environ.get("RCG_OUT_DIR", tempfile.gettempdir()))
BID = sys.argv[1]
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 500

sys.path.insert(0, str(WS / "rcg" / "bin"))
import scan as rcg_scan  # noqa: E402

latest: "OrderedDict[str, dict]" = OrderedDict()
n_rows = 0
for line in (WS / "rcg/ledger/LABELS.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    n_rows += 1
    row = json.loads(line)
    if row.get("path"):
        latest[row["path"]] = row
print(f"[denominator] LABELS rows {n_rows}; distinct paths {len(latest)}")

out = subprocess.run(["git", "ls-files", "-z"], cwd=WS, capture_output=True,
                     text=True, encoding="utf-8")
if out.returncode != 0:
    sys.exit(f"git ls-files rc={out.returncode}")
tracked = set(x for x in out.stdout.split("\0") if x)
print(f"[denominator] git-tracked files repo-wide: {len(tracked)}")

# Exclusions come from the CONTRACTED surface (state/exclusions.jsonl, last-row-wins
# per path; any non-"released" status excludes) -- never a session-mortal scratch file.
_excl_rows: dict = {}
for _line in (Path(__file__).parents[1] / "exclusions.jsonl").read_text(
        encoding="utf-8").splitlines():
    if _line.strip():
        _r = json.loads(_line)
        if _r.get("path"):
            _excl_rows[_r["path"]] = _r
stragglers = set(p for p, r in _excl_rows.items() if r.get("status") != "released")
candidates = sorted(p for p, r in latest.items()
                    if r.get("label") == "ARCHIVE" and p in tracked and p not in stragglers)
n_straggler_present = sum(1 for p in stragglers if p in tracked)
print(f"candidates (ARCHIVE at last-row-wins, tracked, minus {len(stragglers)} CTO~B "
      f"stragglers of which {n_straggler_present} still tracked): {len(candidates)}")

rules = rcg_scan.compile_charters()
protected = [p for p in candidates if rcg_scan.charter_of(p, rules)[1] != "SCORE"]
print(f"protected-charter members: {len(protected)}")
if protected:
    for p in protected[:10]:
        print(f"  PROTECTED: {p}")
    sys.exit("ABORT: protected members in candidate set")

cand_set = set(candidates)
c7 = []
for p in candidates:
    if Path(p).name == "__init__.py":
        d = str(Path(p).parent).replace("\\", "/")
        if any(t.startswith(d + "/") and t != p and t not in cand_set for t in tracked):
            c7.append(p)
n_init = sum(1 for p in candidates if Path(p).name == "__init__.py")
print(f"__init__.py: {n_init}; C7 violations: {len(c7)}")
if c7:
    for p in c7[:10]:
        print(f"  C7: {p}")
    sys.exit("ABORT: C7 violations")

def unit(p: str) -> str:
    parts = p.split("/")
    if p.startswith("org/threads/"):
        return "/".join(parts[:3]) if len(parts) > 3 else p
    return str(Path(p).parent).replace("\\", "/")

by_unit: dict[str, list[str]] = defaultdict(list)
for p in candidates:
    by_unit[unit(p)].append(p)
threads_units = sorted(u for u in by_unit if u.startswith("org/threads/"))
other_units = sorted(u for u in by_unit if not u.startswith("org/threads/"))
print(f"[denominator] units: {len(by_unit)} ({len(threads_units)} org/threads-grain, "
      f"{len(other_units)} dir-grain); largest: "
      f"{max((len(v), k) for k, v in by_unit.items())}")

chosen: list[str] = []
skipped = 0
for u in threads_units + other_units:  # finish org/threads first, then general tail
    mem = sorted(by_unit[u])
    if len(chosen) + len(mem) <= CAP:
        chosen.extend(mem)
    else:
        skipped += 1
chosen.sort()

# C7 over the CHOSEN set with nested semantics (the gate's denominator, B-0006 lesson):
# an __init__.py may ship only if no tracked file under its package dir survives the batch
chosen_set = set(chosen)
c7_dropped = []
changed = True
while changed:
    changed = False
    for p in list(chosen_set):
        if Path(p).name == "__init__.py":
            d = str(Path(p).parent).replace("\\", "/")
            if any(t.startswith(d + "/") and t != p and t not in chosen_set for t in tracked):
                chosen_set.discard(p)
                c7_dropped.append(p)
                changed = True
chosen = sorted(chosen_set)
print(f"C7-over-chosen (nested): dropped {len(c7_dropped)} __init__.py deferred to ship "
      f"with their packages: {c7_dropped if c7_dropped else '[]'}")

sha = hashlib.sha256("\n".join(chosen).encode("utf-8")).hexdigest()
(SCRATCH / f"{BID}_paths.txt").write_bytes(("\n".join(chosen) + "\n").encode("utf-8"))

# cohort summary at top-2-level grain for the ledger row
cohorts = sorted({"/".join(p.split("/")[:2]) for p in chosen})
(SCRATCH / f"{BID}_cohorts.json").write_text(json.dumps(cohorts), encoding="utf-8")
units_in = {unit(p) for p in chosen}
print(f"cut: {len(chosen)} files / {len(units_in)} units (skipped {skipped} units); cap {CAP}")
print(f"sha256_sorted_list: {sha}")
print(f"queue after: {len(candidates) - len(chosen)}")
print(f"cohorts ({len(cohorts)}): {json.dumps(cohorts)}")
