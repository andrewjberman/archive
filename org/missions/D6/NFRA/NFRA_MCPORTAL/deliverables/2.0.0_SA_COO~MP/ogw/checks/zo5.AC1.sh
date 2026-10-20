#!/usr/bin/env bash
# MP-zo-5 AC1 (OGW round 2 item 3; CTO ROUND_ANALYSIS.ogw-round1.md): the worker's evidence file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~45/row_evidence.json holds exactly the four 26-day ARMED rows (W2-S8, W3-S2, C-S3, C-S8).
# Each row is {"id","proposal":"DISARM"|"OWNER_DATE","owner","date","evidence":[{"claim":"MEASURED|RECORDED|ABSENT","command","output"}]}.
# A DISARM row needs at least one MEASURED item with a non-empty command and output; an OWNER_DATE row needs an owner and an ISO
# date (YYYY-MM-DD). No row is carried silently: every one of the four has a proposal.
. "$(dirname "$0")/../../pd/checks/_root.sh"
RUN="${MP_ZO5_RUN:-$PDD/0.9.0_WK_NFRA_MCPORTAL~45/row_evidence.json}"
v=$(python - "$RUN" <<'PY'
import json, re, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("evidence=unreadable(%s)" % type(e).__name__); print("PASSCOND no"); sys.exit()
want = {"NFRA_MCPORTAL-Z-W2-S8", "NFRA_MCPORTAL-Z-W3-S2", "NFRA_MCPORTAL-Z-C-S3", "NFRA_MCPORTAL-Z-C-S8"}
rows = [r for r in (d.get("rows") or []) if isinstance(r, dict)]
ids = {r.get("id") for r in rows}
ok = 0
for r in rows:
    ev = [e for e in (r.get("evidence") or []) if isinstance(e, dict)]
    if r.get("proposal") == "DISARM":
        good = any(e.get("claim") == "MEASURED" and (e.get("command") or "").strip() and (e.get("output") or "").strip() for e in ev)
    elif r.get("proposal") == "OWNER_DATE":
        good = bool((r.get("owner") or "").strip()) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("date") or ""))
    else:
        good = False
    ok += 1 if good else 0
print("evidence=read rows=%d ids_match=%s rows_with_valid_proposal=%d of %d" % (len(rows), "yes" if ids == want and len(rows) == 4 else "no", ok, len(want)))
print("PASSCOND " + ("yes" if ids == want and len(rows) == 4 and ok == 4 else "no"))
PY
)
printf '%s\n' "$v" | grep -v '^PASSCOND'
if printf '%s' "$v" | grep -q '^PASSCOND yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
