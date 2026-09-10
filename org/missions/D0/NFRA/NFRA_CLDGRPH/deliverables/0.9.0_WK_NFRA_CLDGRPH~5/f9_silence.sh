#!/usr/bin/env bash
# f9_silence.sh -- F9-AC4 exerciser. 0.9.0_WK_NFRA_CLDGRPH~5, TO-CG-F-9 (CG-s-29).
#
# THE 120-SECOND SILENCE TEST, laptop half: a commit touching org/modules/graph/ -- a path
# the retired hook's filter regex MATCHES, so before S29 it would have published -- is
# followed by a 120 s wait, and both stitch keys' LastModified are unchanged across that
# window, with the marker still the cloud producer's.
#
# THE BASELINE IS THE READ TAKEN IMMEDIATELY BEFORE THE FILTER COMMIT, and it is an
# ARTIFACT (f9_keys_pre_filter_commit.txt beside this script), not a constant typed here.
# WHY, measured and disclosed: this order's FIRST silence run used the pre-order baseline
# (18:49:36Z / 18:49:37Z) and read 0 of 2 -- not because the filter commit published, but
# because BETWEEN the two reads the keys moved TWICE by acts of other seats: at
# 2026-09-09T19:45:44Z the ISSUER's own commit 6de9b76d93 fired this laptop's hook, which
# was still installed for 46 more seconds, and published producer=stitch-local; then the
# issuer started an ad-hoc opal-stitch-produce build at 19:52Z to re-assert
# producer=stitch-codebuild. A baseline that spans another writer's act cannot answer
# "did THIS commit publish" -- it answers "did anything publish", which is a different
# question and the wrong one for this criterion. Row NFRA_CLDGRPH-W5-S4 records it; the
# first run's transcript is kept verbatim at f9_silence_run1.txt.
#
# SECOND, INDEPENDENT LIMB: both keys' LastModified PREDATE the filter commit's own
# timestamp. A publish caused by that commit cannot carry a LastModified earlier than the
# commit, so this limb cannot be satisfied by a stale baseline. (It ages: the next cloud
# publish -- the 03:00Z nightly -- moves both keys past the commit, which is why the
# equality limb above is the criterion's token and this one is the corroborator.)
#
# Reads only: head-object + get-object. ZERO S3 writes.
set -u
WS="$(git rev-parse --show-toplevel 2>/dev/null)"; [ -n "$WS" ] || { echo "ERROR: no repo root"; exit 9; }
cd "$WS" || exit 9
HERE="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~5"
AWS=".tools/aws"
BUCKET="opal-313476888478-globgrph"
ART_KEY="stitch/stitch_graph.json"
MRK_KEY="stitch/stitch_marker.json"
POINTER="org/modules/graph/STITCH_HOOK_RETIRED.md"
PRE="$HERE/f9_keys_pre_filter_commit.txt"
WAIT_S="${1:-125}"

lastmod() { "$AWS" s3api head-object --bucket "$BUCKET" --key "$1" --query LastModified --output text 2>&1 | tr -d '\r'; }

echo "F9-AC4 -- A FILTER-MATCHING COMMIT ON THIS CLONE PUBLISHES NOTHING"
echo "RUN_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ ! -s "$PRE" ]; then echo "ERROR: baseline artifact missing: $PRE"; exit 8; fi
BASE_ART="$(cat "$PRE" | grep '^PRE_COMMIT_ARTIFACT_LASTMODIFIED=' | head -1 | sed 's/^[^=]*=//' | tr -d '\r')"
BASE_MRK="$(cat "$PRE" | grep '^PRE_COMMIT_MARKER_LASTMODIFIED=' | head -1 | sed 's/^[^=]*=//' | tr -d '\r')"
BASE_AT="$(cat "$PRE" | grep '^PRE_COMMIT_READ_AT=' | head -1 | sed 's/^[^=]*=//' | tr -d '\r')"
echo "BASELINE_READ_AT=$BASE_AT  (immediately before the filter commit)"
echo "BASELINE_ARTIFACT=$BASE_ART"
echo "BASELINE_MARKER=$BASE_MRK"

# --- the filter commit, DERIVED from the log so a grader can re-run this -------------
C_FULL="$(git log --full-history -1 --format=%H -- "$POINTER")"
if [ -z "$C_FULL" ]; then echo "FILTER_COMMIT=ABSENT"; exit 5; fi
echo "FILTER_COMMIT=$(echo "$C_FULL" | cut -c1-10)"
echo "FILTER_COMMIT_FULL=$C_FULL"
# %cI carries its own offset; never a literal Z typed into a --date=format (that renders
# LOCAL and stamps it UTC -- this script printed 15:59:10Z for a 19:59:10Z commit once).
echo "FILTER_COMMIT_AT=$(git show -s --format=%cI "$C_FULL")"
echo "FILTER_COMMIT_AT_UTC=$(TZ=UTC0 git show -s --format=%cd --date=format-local:%Y-%m-%dT%H:%M:%SZ "$C_FULL")"
C_EPOCH="$(git show -s --format=%ct "$C_FULL")"
echo "--- paths in that commit; the retired hook's filter regex, at its :23 @2e8dd90435, was"
echo "--- ^(portal(\$|/)|data/.*/scripts/|org/modules/graph/|infra/aws/globgrph/(derive_stitch|extract_portal_stitch)\.py) ---"
git show --no-commit-id --name-only -r --format= "$C_FULL"
MATCHED="$(git show --no-commit-id --name-only -r --format= "$C_FULL" | grep -cE '^(portal($|/)|data/.*/scripts/|org/modules/graph/|infra/aws/globgrph/(derive_stitch|extract_portal_stitch)\.py)')"
echo "FILTER_MATCHING_PATHS_IN_COMMIT=$MATCHED"

# --- the wait -------------------------------------------------------------------------
T0="$(date +%s)"; i=0
while [ "$i" -lt "$WAIT_S" ]; do
  echo "t=+${i}s  $(date -u +%Y-%m-%dT%H:%M:%SZ)  waiting"
  sleep 15; i=$((i + 15))
done
T1="$(date +%s)"
echo "WAITED_S=$((T1 - T0))"

A1="$(lastmod "$ART_KEY")"; M1="$(lastmod "$MRK_KEY")"
echo "ARTIFACT_LASTMODIFIED_AFTER=$A1"
echo "MARKER_LASTMODIFIED_AFTER=$M1"
N=0
[ "$A1" = "$BASE_ART" ] && N=$((N + 1))
[ "$M1" = "$BASE_MRK" ] && N=$((N + 1))
echo "KEYS_LASTMODIFIED_UNCHANGED=$N of 2"
[ "$A1" = "${BASE_ART}X" ] && echo "EQUALITY_CONTROL=BROKEN" || echo "EQUALITY_CONTROL=CAN-FAIL"

# --- limb 2: both keys predate the filter commit --------------------------------------
epoch_of() { date -u -d "$1" +%s 2>/dev/null || echo "NaN"; }
AE="$(epoch_of "$A1")"; ME="$(epoch_of "$M1")"
P=0
[ "$AE" != "NaN" ] && [ "$AE" -lt "$C_EPOCH" ] && P=$((P + 1))
[ "$ME" != "NaN" ] && [ "$ME" -lt "$C_EPOCH" ] && P=$((P + 1))
echo "FILTER_COMMIT_EPOCH=$C_EPOCH  ARTIFACT_EPOCH=$AE  MARKER_EPOCH=$ME"
echo "KEYS_PREDATE_FILTER_COMMIT=$P of 2"

# --- the marker's producer -------------------------------------------------------------
# RELATIVE output path on purpose: the .tools/aws shim (CLI v1 under MSYS) rewrites an
# absolute unix output path -- get-object to "/tmp/x.json" lands at C:/tmp/x.json and the
# bash-side [ -s ] then reads FALSE. Measured here 2026-09-09T19:38Z.
mkdir -p .scratch
MF=".scratch/f9_marker_read.$$.json"
"$AWS" s3api get-object --bucket "$BUCKET" --key "$MRK_KEY" "$MF" >/dev/null 2>&1
if [ -s "$MF" ]; then
  echo "--- the marker body, verbatim ---"; cat "$MF" | tr -d '\r'; echo ""; echo "--- end ---"
  PROD="$(cat "$MF" | grep -o '"producer"[^,}]*' | head -1 | sed 's/.*: *"//; s/".*//' | tr -d '\r')"
  echo "MARKER_PRODUCER=$PROD"
else
  echo "MARKER_PRODUCER=UNREADABLE"
fi
rm -f "$MF"
exit 0
