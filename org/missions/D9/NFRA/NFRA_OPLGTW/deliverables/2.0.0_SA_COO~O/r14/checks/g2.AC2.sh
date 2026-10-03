#!/usr/bin/env bash
# OPLGTW OG-g-2 AC2 (G-E identity basis, CTO ruling msg 28154 (1)): IDENTITY_PILOT.json shows the pilot principal's
# tid equals the Opal tenant and her oid, read from an AUTHORITATIVE tenant source, MATCHES the write-capable roster
# pair held host-side -- compared by sha256 only; the record carries no raw oid, no email and no GUID besides the tenant.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~23/IDENTITY_PILOT.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read(); d = json.loads(raw)
TEN = "6810043e-d171-4adc-9975-068b35e179da"
h1, h2 = str(d.get("oid_sha256_tenant", "")), str(d.get("oid_sha256_roster", ""))
hexok = all(re.fullmatch(r"[0-9a-f]{64}", h) for h in (h1, h2))
guids = [g for g in re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", raw) if g != TEN]
emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", raw)
print("tid equals tenant %s; instrument named %s; hashes well-formed %s; equal %s; recorded %s; other GUIDs %d; emails %d"
      % (d.get("tid") == TEN, bool(str(d.get("tenant_read_instrument", "")).strip()), hexok, h1 == h2, d.get("match"), len(guids), len(emails)))
ok = d.get("tid") == TEN and hexok and h1 == h2 and d.get("match") == "MATCH" and not guids and not emails \
     and bool(str(d.get("tenant_read_instrument", "")).strip())
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
EOF
