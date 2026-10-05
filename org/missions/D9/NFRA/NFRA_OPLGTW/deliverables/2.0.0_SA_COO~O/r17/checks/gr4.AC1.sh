#!/usr/bin/env bash
# OPLGTW OG-gr-4 AC1 (CTO round-16 analysis s.4 item 3): GR4_BALANCE_GRAIN.json measures dim_balance's grain
# (account,) for uniqueness on EVERY served snapshot (14 days x 2 masters at the cut; the denominator is the served
# census the record prints, and must be >= 28), and serves one dim_balance rows page through the served construction
# (synthetic principal, 0 grants written, state store untouched). Consistency: grain unique on every snapshot AND the
# page OK; or NOT unique somewhere AND the page REFUSED paging_refused_no_unique_grain AND a surprise row id named.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~26/GR4_BALANCE_GRAIN.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
snaps = d.get("snapshots", [])
served = d.get("served_snapshot_census", 0)
measured = [s for s in snaps if isinstance(s.get("rows"), int) and isinstance(s.get("duplicate_keys"), int)]
dup = [s for s in measured if s["duplicate_keys"] > 0]
page = str(d.get("page", ""))
unique_branch = not dup and page == "OK"
refuse_branch = bool(dup) and "paging_refused_no_unique_grain" in page and bool(d.get("row_id"))
print("served census %d; measured %d; snapshots with duplicate (account,) keys %d; page %s" % (served, len(measured), len(dup), page[:60]))
ok = (served >= 28 and len(measured) == served and (unique_branch or refuse_branch)
      and d.get("synthetic_principal") is True and d.get("grants_written") == 0 and d.get("state_store_written") is False)
print("branch: %s" % ("UNIQUE+SERVED" if unique_branch else "NOT-UNIQUE+REFUSED+ROW" if refuse_branch else "INCONSISTENT"))
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
