#!/usr/bin/env bash
# F2-AC4 -- THE CLOCK SKEW IS MEASURED, NOT ASSUMED.
#
# At each instant f2_ask_at.sh issues one request to the gateway and keeps its
# response HEADERS (f2_gwhdr_T<n>.txt). The Date header is the SHARED reference:
# site Z reads the Date header of the SAME server, so the pair's relative skew is
# derivable at L9 with no handshake between two seats that cannot message each
# other. Local time is stamped either side of the header request and the MIDPOINT
# is used, so RTT does not land wholly on one side of the subtraction.
#
# THE FLOOR IS STATED: the HTTP Date header has ONE SECOND of resolution, so any
# |skew| below ~0.5 s is quantisation, not a measurement of agreement. A skew
# figure without that sentence would overclaim.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1
PY=${PYTHON:-python}

echo "=== f2_skew.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

"$PY" - "$D" <<'PY'
import io
import os
import re
import sys

D = sys.argv[1]
LABELS = ["T0", "T1", "T2"]


def read(p):
    return io.open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


vals = []
print("--- PER INSTANT ---")
for lb in LABELS:
    cap = read(os.path.join(D, "f2_ask_%s.txt" % lb))
    if cap is None or re.search(r"^LAPTOP_STATUS_%s=MISSED" % lb, cap, re.M):
        print("  %s: MISSED or no capture -- no skew reading" % lb)
        continue
    m = re.search(r"^LAPTOP_SKEW_S_%s=(-?[0-9.]+)" % lb, cap, re.M)
    d = re.search(r"^GATEWAY_DATE_%s=(.+?)\s*$" % lb, cap, re.M)
    hdr = read(os.path.join(D, "f2_gwhdr_%s.txt" % lb))
    hdr_date = None
    if hdr:
        hm = re.search(r"^Date:\s*(.+?)\s*$", hdr, re.M | re.I)
        hdr_date = hm.group(1) if hm else None
    if m:
        vals.append(abs(float(m.group(1))))
        print("  %s skew_s=%s gateway_date=%s (header file re-read: %s)"
              % (lb, m.group(1), d.group(1) if d else "UNREAD", hdr_date))
    else:
        print("  %s skew_s=UNREAD gateway_date=%s" % (lb, hdr_date))

print()
print("--- F2-AC4 VERDICT LINES ---")
if vals:
    print("SKEW_S_MAX=%.3f" % max(vals))
else:
    print("SKEW_S_MAX=UNREAD")
print("SKEW_SOURCE=gateway Date header")
print("SKEW_RESOLUTION_FLOOR_S=1.0  (RFC 7231 Date is second-resolution; |skew| under ~0.5 s is quantisation, not agreement)")
print("SKEW_SEMANTICS=laptop local clock MINUS gateway clock, midpoint of the header request; site Z prints its own against the SAME server, so the pair's relative skew is a subtraction at L9 and needs no handshake")
PY
echo "=== f2_skew.sh END ==="
