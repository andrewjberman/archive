"""AMGT_CORPUS round 22, CRPS-x-2 -- the unit apply, run on a TEMP COPY of the committed field_map.json (the committed file is
never written), then diffed entry by entry against the committed map, plus the u-1 reader probed on the temp map. Read-only on
the repo (S3 raw reads through discriminate_facts). The issuer's file.

  -> 'x2 applied A of 9 skipped S changed_entries C other_changed O expected_set True|False reads_stated R
      tsm_unchanged True|False reader_6501_best_sales <UNIT CLASS>'
"""
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
FM = os.path.join(RES, "field_map.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FACTS = [("6501 JP Equity", "SALES_REV_TURN"), ("8316 JP Equity", "SALES_REV_TURN"),
         ("6501 JP Equity", "CURR_ENTP_VAL"), ("9433 JP Equity", "CURR_ENTP_VAL"), ("8035 JP Equity", "CURR_ENTP_VAL"),
         ("8766 JP Equity", "CURR_ENTP_VAL"), ("TSM US Equity", "CURR_ENTP_VAL"),
         ("8316 JP Equity", "NET_DEBT"), ("6501 JP Equity", "BEST_SALES")]
EXPECTED = set(f for f in FACTS if f[0] != "TSM US Equity")

d = tempfile.mkdtemp(prefix="x2_apply_")
tmp = os.path.join(d, "field_map.json")
shutil.copyfile(FM, tmp)
bum = load("bum_x2", os.path.join(RES, "build_unit_map.py"))
out = bum.apply_discriminated(FACTS, field_map_path=tmp)
applied = sum(1 for r in out if r.get("applied"))
skipped = sum(1 for r in out if not r.get("applied"))

before = json.load(open(FM, encoding="utf-8"))
after = json.load(open(tmp, encoding="utf-8"))
other = 0
changed = set()
if {k: v for k, v in before.items() if k != "fields"} != {k: v for k, v in after.items() if k != "fields"}:
    other += 1
bf = {e["mnemonic"]: e for e in before["fields"]}
af = {e["mnemonic"]: e for e in after["fields"]}
if set(bf) != set(af):
    other += 1
for m in set(bf) & set(af):
    b, a = bf[m], af[m]
    per_sec = {"per_security_detail", "measured_on"}
    per_sec |= {k for k in ("unit", "sign") if isinstance(b.get(k), dict) or isinstance(a.get(k), dict)}
    if {k: v for k, v in b.items() if k not in per_sec} != {k: v for k, v in a.items() if k not in per_sec}:
        other += 1
    secs = set((b.get("per_security_detail") or {})) | set((a.get("per_security_detail") or {}))
    for k in ("unit", "sign"):
        for side in (b, a):
            if isinstance(side.get(k), dict):
                secs |= set(side[k])
    for s in secs:
        tb = [(b.get(k) or {}).get(s) if isinstance(b.get(k), dict) else None for k in ("unit", "sign")]
        ta = [(a.get(k) or {}).get(s) if isinstance(a.get(k), dict) else None for k in ("unit", "sign")]
        tb.append((b.get("per_security_detail") or {}).get(s))
        ta.append((a.get("per_security_detail") or {}).get(s))
        if json.dumps(tb, sort_keys=True, default=str) != json.dumps(ta, sort_keys=True, default=str):
            changed.add((s, m))
    added = set(a.get("measured_on") or []) - set(b.get("measured_on") or [])
    removed = set(b.get("measured_on") or []) - set(a.get("measured_on") or [])
    other += len(removed) + sum(1 for s in added if (s, m) not in EXPECTED)

reads = 0
for s, m in changed & EXPECTED:
    ev = ((af[m].get("per_security_detail") or {}).get(s) or {}).get("unit_evidence") or {}
    reads += int(isinstance(ev.get("reads"), int) and ev["reads"] >= 1)
tsm_same = (("TSM US Equity", "CURR_ENTP_VAL") not in changed)

mbp = load("mbp_x2", os.path.join(RES, "model_block_pull.py"))
mbp._FIELD_MAP_PATH = type(mbp._FIELD_MAP_PATH)(tmp)
mbp._FIELD_MAP_CACHE = None
u = str(mbp._resolved_unit("BEST_SALES", "6501 JP Equity"))
cls = "UNRESOLVED" if u.startswith("UNRESOLVED") else ("POINTER" if u.startswith("SEE field_map") else u)
shutil.rmtree(d, ignore_errors=True)
print("x2 applied %d of 9 skipped %d changed_entries %d other_changed %d expected_set %s reads_stated %d tsm_unchanged %s "
      "reader_6501_best_sales %s" % (applied, skipped, len(changed), other, changed == EXPECTED, reads, tsm_same, cls))
