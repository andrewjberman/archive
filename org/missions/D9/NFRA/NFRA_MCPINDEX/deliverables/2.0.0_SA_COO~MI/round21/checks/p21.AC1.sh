#!/usr/bin/env bash
# MX-c-39 A1 p21.AC1 -- the release catalog is PLACED: the tracked gateway catalog is byte-equal (md5) to the issuer's emitted candidate and passes the r21 release-candidate checks.
# P21_MD5 names the candidate md5 (default: the round 21 candidate emitted 2026-10-16 ~21:0xZ from the measure 0bc424dd91).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
WANT="${P21_MD5:-9c456f9341dd2d5ab2369f9e1479c3ab}"
T=infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml
GOT="$(md5sum "$T" | cut -d' ' -f1)"
echo "DENOMINATOR tracked catalog md5 $GOT; expected $WANT"
RC=0
[ "$GOT" = "$WANT" ] && echo "CHECK ok  : the tracked catalog is the candidate (md5 equal)" || { echo "CHECK FAIL: the tracked catalog is not the candidate"; RC=1; }
for a in AC1 AC2; do
  OUT="$(bash "$D/r21.$a.sh" 2>&1)"; R=$?
  echo "$OUT" | grep -E "^(DENOMINATOR|CHECK FAIL)" | cut -c1-200
  [ $R -eq 0 ] && echo "CHECK ok  : r21.$a PASS on the tracked catalog" || { echo "CHECK FAIL: r21.$a exit $R"; RC=1; }
done
[ $RC -eq 0 ] && echo "RESULT: PASS" || echo "RESULT: FAIL"
exit $RC
