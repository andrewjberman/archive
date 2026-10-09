#!/usr/bin/env bash
# MS-rr-1 AC1 (the seam on the DEPLOYED bytes): the opal-gateway tree at the deployed commit $GW_DEPLOYED is extracted to
# a temp dir; the worker's deliverables/0.9.0_WK_NFRA_MCPMSP~9/rr1_seam.py, run against it, drives ONE domain refusal
# through app/asker_scope.py (calling identity caller@opalinvest.com, Teams sender pat@gmail.com, audit to a temp file)
# and then lists it through app/admin_refusals.py list_refusals() from that same file. It prints ONE line:
#   SEAM user=<entry user> sender_email=<entry args.sender_email> listed_sender_email=<the listed row's sender_email>
# PASS when user=caller@opalinvest.com, sender_email=pat@gmail.com and listed_sender_email=pat@gmail.com.
. "$(dirname "$0")/_root.sh"
S="$R2/0.9.0_WK_NFRA_MCPMSP~9/rr1_seam.py"
[ -f "$S" ] || { echo "$S absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_rr1.XXXXXX")"
git archive "$GW_DEPLOYED" infra/aws/ec2/opal-gateway | tar -x -C "$T" || { echo "extract of $GW_DEPLOYED failed"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python "$S" --gateway "$(native "$T/infra/aws/ec2/opal-gateway")" 2>&1 | tr -d '\r')
rm -rf "$T"
line=$(printf '%s\n' "$out" | grep -m1 '^SEAM ')
echo "deployed=$GW_DEPLOYED; ${line:-no SEAM line; tail: $(printf '%s\n' "$out" | tail -3 | tr '\n' ' ')}"
if [ "$line" = "SEAM user=caller@opalinvest.com sender_email=pat@gmail.com listed_sender_email=pat@gmail.com" ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
