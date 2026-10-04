#!/usr/bin/env bash
# OPLGTW OG-ar-1 AC1 (CTO round-15 analysis s.4 item 5): AGED_ROW_TRIAGE.json covers EVERY remediation row whose latest
# state is OPEN (computed here from remediations/REMEDIATION_v*.md, the printed denominator), and each entry carries an
# owner and exactly one of: `moves_when` (the condition that moves it), `remediated_by` (the commit or order whose
# measured result already remediates it), or `close_reason` (no condition moves it). Ids only; no row is edited here.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~27/AGED_ROW_TRIAGE.json"
python - "$(native "$F")" <<'PY'
import glob, json, os, re, sys
rows = {}
for f in sorted(glob.glob("org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/remediations/REMEDIATION_v*.md")):
    for blk in re.findall(r"```json\n(.*?)\n```", open(f, encoding="utf-8").read(), re.S):
        try:
            d = json.loads(blk)
        except ValueError:
            continue
        for r in (d if isinstance(d, list) else [d]):
            if isinstance(r, dict) and r.get("id"):
                rows[r["id"]] = r
def st(r):
    rem = r.get("remediation") or {}
    return rem.get("state") if isinstance(rem, dict) else rem
open_ids = sorted(i for i, r in rows.items() if st(r) == "OPEN" and not r.get("closed"))
if not os.path.exists(sys.argv[1]):
    print("remediation rows %d; OPEN %d; triage file absent" % (len(rows), len(open_ids))); print("RESULT: FAIL"); sys.exit(1)
t = json.load(open(sys.argv[1], encoding="utf-8")); ent = {e.get("id"): e for e in t.get("rows", [])}
miss = [i for i in open_ids if i not in ent]
bad = [i for i in open_ids if i in ent and not (ent[i].get("owner") and
       sum(1 for k in ("moves_when", "remediated_by", "close_reason") if ent[i].get(k)) == 1)]
kinds = {k: sum(1 for i in open_ids if i in ent and ent[i].get(k)) for k in ("moves_when", "remediated_by", "close_reason")}
print("remediation rows %d; OPEN %d; triaged %d; missing %d; malformed %d; %s" % (len(rows), len(open_ids), len(open_ids) - len(miss), len(miss), len(bad), kinds))
ok = open_ids and not miss and not bad
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
