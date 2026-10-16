set -u
# IRPT_ANLREQ TO-APPLY-R34B V1 census, READ ONLY. Sent as the SSM command text; stages nothing in S3 and writes no file on the host.
# Lists every file under the r32 root and the r34 root with its sha256 (runtime __pycache__ directories and *.pyc files excluded, and counted),
# joins the two lists on the path and prints the counts, every member that differs, every member only in r34, every member only in r32;
# then the bindings difference by key name, the pool pin and pricing.
R=/opt/irpt-resident
A=$R/0485393f3a-r32
B=$R/0485393f3a-r34
list() { ( cd "$1" && find . -type f ! -path '*/__pycache__/*' ! -name '*.pyc' -print0 | sort -z | xargs -0 sha256sum ); }
echo "CENSUS at $(date -u +%Y-%m-%dT%H:%M:%SZ) roots $A and $B"
echo "CENSUS running root: $(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)"
L32=$(list $A)
L34=$(list $B)
echo "CENSUS excluded runtime files: r32 pyc=$(find $A -name '*.pyc' | wc -l) pycache_dirs=$(find $A -type d -name __pycache__ | wc -l); r34 pyc=$(find $B -name '*.pyc' | wc -l) pycache_dirs=$(find $B -type d -name __pycache__ | wc -l)"
echo "CENSUS paths containing a space (the join cannot read them): r32=$(printf '%s\n' "$L32" | grep -c '  .* ') r34=$(printf '%s\n' "$L34" | grep -c '  .* ')"
{ printf '%s\n' "$L32" | sed 's/^/32 /'; printf '%s\n' "$L34" | sed 's/^/34 /'; } | awk '
  { side=$1; sha=$2; path=$3
    if (side=="32") { s32[path]=sha; n32++ } else { s34[path]=sha; n34++ } }
  END {
    for (p in s34) { if (!(p in s32)) { only34++; print "ONLY-R34 " p } else if (s32[p]!=s34[p]) { diff++; print "DIFFERS " p } else same++ }
    for (p in s32) if (!(p in s34)) { only32++; print "ONLY-R32 " p }
    printf "COUNTS r32_files=%d r34_files=%d identical=%d differ=%d only_r34=%d only_r32=%d\n", n32, n34, same, diff, only34, only32 }' | sort
python3.12 - "$A" "$B" <<'PY'
import hashlib, json, os, sys
a, b = sys.argv[1], sys.argv[2]
da = json.load(open(os.path.join(a, "reports/resident_bindings.json")))
db = json.load(open(os.path.join(b, "reports/resident_bindings.json")))
only_b = sorted(k for k in db if k not in da)
only_a = sorted(k for k in da if k not in db)
changed = sorted(k for k in da if k in db and da[k] != db[k])
print("CENSUS bindings top-level keys only in r34:", only_b, "only in r32:", only_a, "present in both with a different value:", changed)
print("CENSUS bindings sha256 r34 %s" % hashlib.sha256(open(os.path.join(b, "reports/resident_bindings.json"), "rb").read()).hexdigest())
sp = db.get("opal_swap_pool")
print("CENSUS opal_swap_pool binding:", json.dumps(sp, sort_keys=True))
pool = os.path.normpath(os.path.join(b, "reports", (sp or {}).get("path", "")))
print("CENSUS pool file on disk sha256 %s (binding sha256 %s) equal: %s" % (hashlib.sha256(open(pool, "rb").read()).hexdigest(), (sp or {}).get("sha256"), hashlib.sha256(open(pool, "rb").read()).hexdigest() == (sp or {}).get("sha256")))
pr = db.get("opal_pricing")
print("CENSUS opal_pricing in r34:", json.dumps(pr, sort_keys=True), "| in r32:", json.dumps(da.get("opal_pricing"), sort_keys=True))
PY
echo "CENSUS producer list line: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $B/ycharts/generate/resident_worker.py)"
echo "CENSUS unit ExecStart root now: $(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) active=$(systemctl is-active irpt-analysis-resident.service) restarts=$(systemctl show irpt-analysis-resident.service -p NRestarts --value)"
echo "CENSUS queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "CENSUS journal sign-in lines since the new unit start: $(journalctl -u irpt-analysis-resident.service --since "$(systemctl show irpt-analysis-resident.service -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED') (expect 0)"
