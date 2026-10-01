"""AMGT_CORPUS round 22 ACT 2 leg M -- the issuer's apply of the 8 RESOLVED units to the COMMITTED field_map.json, under the pair
(COO 5757501e0d / CTO 951082ff8d). Keeps a pre-image in the scratchpad path given, applies, then diffs entry by entry exactly as
x2_check.py does. Any diff outside the 8 entries restores the pre-image and exits 3 (stop limb 1).

  python m_apply.py <pre_image_path>
  -> 'M applied A of 9 changed_entries C other_changed O expected_set True|False reads_stated R tsm_unchanged True|False'
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
FM = os.path.join(RES, "field_map.json")
FACTS = [("6501 JP Equity", "SALES_REV_TURN"), ("8316 JP Equity", "SALES_REV_TURN"),
         ("6501 JP Equity", "CURR_ENTP_VAL"), ("9433 JP Equity", "CURR_ENTP_VAL"), ("8035 JP Equity", "CURR_ENTP_VAL"),
         ("8766 JP Equity", "CURR_ENTP_VAL"), ("TSM US Equity", "CURR_ENTP_VAL"),
         ("8316 JP Equity", "NET_DEBT"), ("6501 JP Equity", "BEST_SALES")]
EXPECTED = set(f for f in FACTS if f[0] != "TSM US Equity")

pre = sys.argv[1]
shutil.copyfile(FM, pre)
spec = importlib.util.spec_from_file_location("bum_m", os.path.join(RES, "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)
out = bum.apply_discriminated(FACTS, field_map_path=FM)
applied = sum(1 for r in out if r.get("applied"))

before = json.load(open(pre, encoding="utf-8"))
after = json.load(open(FM, encoding="utf-8"))
other, changed = 0, set()
if {k: v for k, v in before.items() if k != "fields"} != {k: v for k, v in after.items() if k != "fields"}:
    other += 1
bf = {e["mnemonic"]: e for e in before["fields"]}
af = {e["mnemonic"]: e for e in after["fields"]}
other += int(set(bf) != set(af))
for m in set(bf) & set(af):
    b, a = bf[m], af[m]
    per_sec = {"per_security_detail", "measured_on"} | {k for k in ("unit", "sign") if isinstance(b.get(k), dict) or isinstance(a.get(k), dict)}
    if {k: v for k, v in b.items() if k not in per_sec} != {k: v for k, v in a.items() if k not in per_sec}:
        other += 1
    secs = set(b.get("per_security_detail") or {}) | set(a.get("per_security_detail") or {})
    for k in ("unit", "sign"):
        for side in (b, a):
            if isinstance(side.get(k), dict):
                secs |= set(side[k])
    for s in secs:
        tb = [(b.get(k) or {}).get(s) if isinstance(b.get(k), dict) else None for k in ("unit", "sign")] + [(b.get("per_security_detail") or {}).get(s)]
        ta = [(a.get(k) or {}).get(s) if isinstance(a.get(k), dict) else None for k in ("unit", "sign")] + [(a.get("per_security_detail") or {}).get(s)]
        if json.dumps(tb, sort_keys=True, default=str) != json.dumps(ta, sort_keys=True, default=str):
            changed.add((s, m))
    added = set(a.get("measured_on") or []) - set(b.get("measured_on") or [])
    removed = set(b.get("measured_on") or []) - set(a.get("measured_on") or [])
    other += len(removed) + sum(1 for s in added if (s, m) not in EXPECTED)
reads = sum(1 for s, m in changed & EXPECTED
            if isinstance((((af[m].get("per_security_detail") or {}).get(s) or {}).get("unit_evidence") or {}).get("reads"), int))
tsm = ("TSM US Equity", "CURR_ENTP_VAL") not in changed
print("M applied %d of 9 changed_entries %d other_changed %d expected_set %s reads_stated %d tsm_unchanged %s" % (
    applied, len(changed), other, changed == EXPECTED, reads, tsm))
raw = open(FM, "rb").read()
print("M lf_only %s" % (b"\r" not in raw))
if not (changed == EXPECTED and other == 0 and tsm):
    shutil.copyfile(pre, FM)
    print("STOP: diff outside the 8 entries -- pre-image restored")
    sys.exit(3)
