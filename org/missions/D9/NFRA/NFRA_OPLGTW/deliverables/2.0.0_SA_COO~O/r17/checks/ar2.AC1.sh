#!/usr/bin/env bash
# OPLGTW OG-ar-2 AC1 (CTO round-16 analysis s.4 item 6): ISSUER_ROWS_R17.json covers the issuer's seven OPEN
# remediation rows (W6-S2, W1-S9, W2-S6, Z-W13-S5, Z-W12-S7, S63, Z-W15-S31), each with an owner and EXACTLY ONE of:
# `moves_when` {condition, actor} | `remediated_by` {pointer, measurement} | `closure` {reason in NOT_A_DEFECT,
# CARRIED_BY, IRREMEDIABLE, ACCEPTED_BY_RULING; pointer} (docs/doctrine/THE_SURPRISE_CHANNEL.md). Z-W12-S7's entry
# names its dated act (the operator re-authorizes before ~2026-10-18). No remediation row is edited by this cell.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~21/ISSUER_ROWS_R17.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
WANT = ["W6-S2", "W1-S9", "W2-S6", "Z-W13-S5", "Z-W12-S7", "S63", "Z-W15-S31"]
REASONS = {"NOT_A_DEFECT", "CARRIED_BY", "IRREMEDIABLE", "ACCEPTED_BY_RULING"}
ent = {e.get("id", "").replace("NFRA_OPLGTW-", ""): e for e in json.load(open(sys.argv[1], encoding="utf-8")).get("rows", [])}
def good(e):
    kinds = [k for k in ("moves_when", "remediated_by", "closure") if e.get(k)]
    if not e.get("owner") or len(kinds) != 1:
        return False
    k = kinds[0]; v = e[k]
    if k == "closure":
        return isinstance(v, dict) and v.get("reason") in REASONS and bool(v.get("pointer"))
    if k == "moves_when":
        return isinstance(v, dict) and bool(v.get("condition")) and bool(v.get("actor"))
    return isinstance(v, dict) and bool(v.get("pointer")) and bool(v.get("measurement"))
miss = [i for i in WANT if i not in ent]
bad = [i for i in WANT if i in ent and not good(ent[i])]
dated = "2026-10-18" in json.dumps(ent.get("Z-W12-S7", {}))
kinds = {k: sum(1 for i in WANT if i in ent and ent[i].get(k)) for k in ("moves_when", "remediated_by", "closure")}
print("rows 7; covered %d; missing %d %s; malformed %d %s; Z-W12-S7 dated %s; %s" % (7 - len(miss), len(miss), miss, len(bad), bad, dated, kinds))
ok = not miss and not bad and dated
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
