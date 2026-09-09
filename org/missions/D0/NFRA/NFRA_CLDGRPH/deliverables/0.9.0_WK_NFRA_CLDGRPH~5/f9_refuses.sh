#!/usr/bin/env bash
# f9_refuses.sh -- F9-AC1 exerciser. 0.9.0_WK_NFRA_CLDGRPH~5, TO-CG-F-9 (CG-s-29).
#
# Proves: .tools/stitch-refresh REFUSES to publish -- exit 3, the refusal text names
# the cloud producer opal-stitch-produce, NO derive ran, and both stitch keys'
# LastModified are byte-equal before and after the attempt.
# Writes ZERO S3 objects (head-object reads only).
set -u
WS="$(git rev-parse --show-toplevel 2>/dev/null)"; [ -n "$WS" ] || { echo "ERROR: no repo root"; exit 9; }
cd "$WS" || exit 9
AWS=".tools/aws"
BUCKET="opal-313476888478-globgrph"
ART_KEY="stitch/stitch_graph.json"
MRK_KEY="stitch/stitch_marker.json"
TMP="${TMPDIR:-/tmp}"

lastmod() { "$AWS" s3api head-object --bucket "$BUCKET" --key "$1" --query LastModified --output text 2>&1 | tr -d '\r'; }
stamp()   { if [ -f "$1" ]; then echo "$(stat -c '%Y:%s' "$1")"; else echo "ABSENT"; fi; }

echo "F9-AC1 -- .tools/stitch-refresh REFUSES TO PUBLISH"
echo "RUN_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "REPO_ROOT=$WS"
echo "HEAD=$(git rev-parse HEAD)"

A_BEFORE="$(lastmod "$ART_KEY")"
M_BEFORE="$(lastmod "$MRK_KEY")"
ART_TMP_BEFORE="$(stamp "$TMP/stitch_graph.json")"
MRK_TMP_BEFORE="$(stamp "$TMP/stitch_marker.json")"
echo "ARTIFACT_LASTMODIFIED_BEFORE=$A_BEFORE"
echo "MARKER_LASTMODIFIED_BEFORE=$M_BEFORE"
echo "LOCAL_DERIVE_ARTIFACT_BEFORE=$ART_TMP_BEFORE"

OUT="$TMP/f9_stitch_refresh_out.$$"
ERR="$TMP/f9_stitch_refresh_err.$$"
bash .tools/stitch-refresh >"$OUT" 2>"$ERR"
RC=$?
echo "STITCH_REFRESH_RC=$RC"
echo "--- stdout (verbatim) ---"; cat "$OUT"; echo "--- stderr (verbatim) ---"; cat "$ERR"; echo "--- end ---"
echo "STDOUT_BYTES=$(wc -c < "$OUT" | tr -d ' ')"

if cat "$ERR" | grep -q 'opal-stitch-produce'; then
  echo "REFUSAL_NAMES=opal-stitch-produce"
else
  echo "REFUSAL_NAMES=ABSENT"
fi

# DERIVE_RAN -- two independent tells: (1) any derive/marker output line;
# (2) the local derive artifact in TMP touched by the run.
DERIVE_TELL=0
if cat "$OUT" "$ERR" | grep -qE 'AC-GRAIN|GRAIN_SENTINEL|derive_stitch|^marker:|Traceback|OK: stitch published'; then DERIVE_TELL=1; fi
ART_TMP_AFTER="$(stamp "$TMP/stitch_graph.json")"
MRK_TMP_AFTER="$(stamp "$TMP/stitch_marker.json")"
if [ "$ART_TMP_BEFORE" != "$ART_TMP_AFTER" ] || [ "$MRK_TMP_BEFORE" != "$MRK_TMP_AFTER" ]; then DERIVE_TELL=1; fi
if [ "$DERIVE_TELL" = "0" ]; then echo "DERIVE_RAN=false"; else echo "DERIVE_RAN=true"; fi
echo "LOCAL_DERIVE_ARTIFACT_AFTER=$ART_TMP_AFTER"

A_AFTER="$(lastmod "$ART_KEY")"
M_AFTER="$(lastmod "$MRK_KEY")"
echo "ARTIFACT_LASTMODIFIED_AFTER=$A_AFTER"
echo "MARKER_LASTMODIFIED_AFTER=$M_AFTER"
N=0
[ "$A_BEFORE" = "$A_AFTER" ] && N=$((N+1))
[ "$M_BEFORE" = "$M_AFTER" ] && N=$((N+1))
echo "KEYS_LASTMODIFIED_UNCHANGED=$N of 2"

# Negative control on the equality test: it must be able to read UNEQUAL.
if [ "$A_BEFORE" = "${A_AFTER}X" ]; then echo "EQUALITY_CONTROL=BROKEN"; else echo "EQUALITY_CONTROL=CAN-FAIL"; fi
rm -f "$OUT" "$ERR"
exit 0
