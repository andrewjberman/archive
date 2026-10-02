#!/usr/bin/env bash
# OPLGTW OG-wp-1 AC1 (row Z-W12-S8; analysis round 12 s.3b): the record DENY_RECORD_ORIGIN.json states the census of the
# access-state table from a STRONG read, the deny record's origin (writer, approver, written_utc,
# source_authorization -- each a value or "ABSENT: <reason>"), a disposition proposal for it, and the three synthetic
# partitions recorded as fixtures. It carries no email address and no GUID (no personal identifier).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~20/DENY_RECORD_ORIGIN.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read(); d = json.loads(raw); bad = []
c = d.get("census", {})
for k in ("partitions_real", "partitions_synthetic", "email_deny_active", "items_total"):
    if not isinstance(c.get(k), int): bad.append("census." + k)
if c.get("strong_read") is not True: bad.append("census.strong_read")
o = d.get("deny_record", {})
for k in ("writer", "approver", "written_utc", "source_authorization"):
    if not str(o.get(k, "")).strip(): bad.append("deny_record." + k)
if d.get("deny_disposition") not in ("REVOKE_PROPOSED", "KEEP_WITH_REASON"): bad.append("deny_disposition")
if not str(d.get("deny_reason", "")).strip(): bad.append("deny_reason")
if d.get("synthetic_partitions") != "FIXTURE_RECORDED": bad.append("synthetic_partitions")
pii = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", raw)) + len(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", raw))
print("census real %s synthetic %s email_deny_active %s items %s; disposition %s; missing/invalid %d %s; email/GUID strings %d"
      % (c.get("partitions_real"), c.get("partitions_synthetic"), c.get("email_deny_active"), c.get("items_total"),
         d.get("deny_disposition"), len(bad), bad, pii))
ok = not bad and pii == 0
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
EOF
