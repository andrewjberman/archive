set -u
# IRPT_ANLREQ TO-APPLY-R32R V1 census (condition 1), READ ONLY. Sent as the SSM command text; stages nothing in S3 and writes no file on the host.
# Lists every file under the r31 root and the r32 root with its sha256 (runtime __pycache__ directories and *.pyc files excluded, and counted),
# joins the two lists on the path and prints: the counts, every member that differs, every member only in r32, every member only in r31.
R=/opt/irpt-resident
A=$R/0485393f3a-r31
B=$R/0485393f3a-r32
list() { ( cd "$1" && find . -type f ! -path '*/__pycache__/*' ! -name '*.pyc' -print0 | sort -z | xargs -0 sha256sum ); }
echo "CENSUS at $(date -u +%Y-%m-%dT%H:%M:%SZ) roots $A and $B"
echo "CENSUS running root: $(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
L31=$(list $A)
L32=$(list $B)
echo "CENSUS excluded runtime files: r31 pyc=$(find $A -name '*.pyc' | wc -l) pycache_dirs=$(find $A -type d -name __pycache__ | wc -l); r32 pyc=$(find $B -name '*.pyc' | wc -l) pycache_dirs=$(find $B -type d -name __pycache__ | wc -l)"
echo "CENSUS paths containing a space (the join cannot read them): r31=$(printf '%s\n' "$L31" | grep -c '  .* ') r32=$(printf '%s\n' "$L32" | grep -c '  .* ')"
{ printf '%s\n' "$L31" | sed 's/^/31 /'; printf '%s\n' "$L32" | sed 's/^/32 /'; } | awk '
  { side=$1; sha=$2; path=$3
    if (side=="31") { s31[path]=sha; n31++ } else { s32[path]=sha; n32++ } }
  END {
    for (p in s32) { if (!(p in s31)) { only32++; print "ONLY-R32 " p } else if (s31[p]!=s32[p]) { diff++; print "DIFFERS " p } else same++ }
    for (p in s31) if (!(p in s32)) { only31++; print "ONLY-R31 " p }
    printf "COUNTS r31_files=%d r32_files=%d identical=%d differ=%d only_r32=%d only_r31=%d\n", n31, n32, same, diff, only32, only31 }' | sort
echo "CENSUS bindings sha256 $(sha256sum $B/reports/resident_bindings.json | cut -d' ' -f1) (want c4a810eee18cfd4fea725588cecdb306809dfa5a7082838cb8196abae36d31e1)"
echo "CENSUS opal_pricing block in the r32 bindings:"
grep -n -A7 '"opal_pricing"' $B/reports/resident_bindings.json | cut -c1-160
echo "CENSUS commentary family registration lines in resident_installed.py: $(grep -c 'irpt-anlreq-x10-v1' $B/reports/resident_installed.py)"
grep -n 'irpt-anlreq-x10-v1' $B/reports/resident_installed.py | cut -c1-200 | head -4
echo "CENSUS unit ExecStart root now: $(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) active=$(systemctl is-active irpt-analysis-resident.service)"
echo "CENSUS queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
