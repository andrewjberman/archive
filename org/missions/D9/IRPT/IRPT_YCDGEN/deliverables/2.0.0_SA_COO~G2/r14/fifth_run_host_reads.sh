set -u
# READ ONLY. IRPT_YCDGEN round 14, the host-side reads of TCKT_VNEXT's fifth run (its pair, step 5): (i) the journal's named
# lines for one request id; (ii) the SHAPE of the sign-in receipt st32 keeps, after a check for a posted value, a cookie and
# a tokenised URL. No receipt VALUE is printed except closed tokens, booleans, integers, lengths and sha256 prefixes.
# No write, no restart, no receive, no copy of the receipt off the host. Operator 0.7.0_AE_CloudOps~YC2 for 2.0.0_SA_COO~G2.
REQ=REQ-86a5a08295b65e12749968f9
SINCE="2026-10-11 17:05:00"
UNIT=irpt-analysis-resident.service
H=/opt/investor-reporting-ycharts
echo "AT $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "ROOT=$(systemctl show $UNIT -p ExecStart | grep -o '/opt/irpt-resident/[0-9a-z-]*' | head -1)"
echo "ACTIVE=$(systemctl is-active $UNIT) RESTARTS=$(systemctl show $UNIT -p NRestarts --value) START=$(systemctl show $UNIT -p ActiveEnterTimestamp --value)"
J=$(mktemp /tmp/j5.XXXXXX)
journalctl -u $UNIT --since "$SINCE" --no-pager -o short-iso > $J
echo "WINDOW since=$SINCE lines=$(wc -l < $J) polls=$(grep -c IRPT_RESIDENT_POLL $J) tracebacks=$(grep -c Traceback $J)"
echo "REQ_LINES=$(grep -c "$REQ" $J)"
grep "$REQ" $J | cut -c1-400 | sed 's/^/REQ /'
# the worker's own named lines in the window that are not idle polls (they carry closed tokens, a class and a code)
grep -E 'IRPT_RESIDENT_|WARN:|ERROR:' $J | grep -v 'IRPT_RESIDENT_POLL handled=0' | cut -c1-400 | sed 's/^/NAMED /'
echo "SIGNIN_LINES=$(grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED' $J)"
grep -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED' $J | cut -c1-300 | sed 's/^/SIGNIN /'
rm -f $J
echo "CHILDREN=$(pgrep -P $(systemctl show $UNIT -p MainPID --value) -f 'node|chrom' 2>&1 | grep -c '^[0-9]')"
echo "QUEUE=$(aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text 2>&1)"
echo "--- capture files in $H (names, sizes, times; no content)"
ls -l --time-style=+%Y-%m-%dT%H:%M:%SZ $H 2>&1 | grep -E 'capture|receipt|stderr' | awk '{print "FILE", $5, $6, $7}'
python3.12 - "$H/last-capture.receipt.json" <<'PY'
import hashlib, json, os, re, sys
path = sys.argv[1]
if not os.path.isfile(path):
    print("RECEIPT ABSENT: no last-capture.receipt.json (no capture ran, or it kept none)")
    raise SystemExit(0)
raw = open(path, "rb").read()
print("RECEIPT present bytes=%d sha256=%s mtime_epoch=%d" % (len(raw), hashlib.sha256(raw).hexdigest()[:16], int(os.path.getmtime(path))))
try:
    doc = json.loads(raw.decode("utf-8"))
except Exception as exc:
    print("RECEIPT not JSON: %s (nothing quoted)" % type(exc).__name__)
    raise SystemExit(0)
CLOSED = re.compile(r"[A-Z][A-Z0-9_]{1,63}")          # a closed code such as a reason
KEYBAD = re.compile(r"pass|pwd|secret|cookie|token|authori[sz]ation|credential|session_?id|csrf", re.I)
URLQ = re.compile(r"https?://[^\s\"']*[?#]")           # a URL that carries a query or a fragment
COOKIE = re.compile(r"(^|[;\s])[A-Za-z0-9_.-]{2,40}=[A-Za-z0-9%_.+/=-]{16,}")   # name=long-opaque-value
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")
found = {"posted_value_key": 0, "cookie_like": 0, "tokenised_url": 0, "jwt_like": 0}
rows = []
def walk(node, where):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, where + "." + str(k) if where else str(k))
    elif isinstance(node, list):
        rows.append((where, "list", "len=%d" % len(node)))
        for i, v in enumerate(node[:50]):
            walk(v, "%s[%d]" % (where, i))
    elif isinstance(node, bool) or node is None:
        rows.append((where, "bool/null", str(node)))
    elif isinstance(node, (int, float)):
        rows.append((where, "number", str(node)))
    else:
        s = str(node)
        leaf = where.split(".")[-1]
        hit = []
        if KEYBAD.search(leaf) and s:
            found["posted_value_key"] += 1; hit.append("KEY")
        if URLQ.search(s):
            found["tokenised_url"] += 1; hit.append("URLQ")
        if COOKIE.search(s):
            found["cookie_like"] += 1; hit.append("COOKIE")
        if JWT.search(s):
            found["jwt_like"] += 1; hit.append("JWT")
        shown = s if (CLOSED.fullmatch(s) and not hit) else "len=%d sha=%s" % (len(s), hashlib.sha256(s.encode("utf-8")).hexdigest()[:10])
        rows.append((where, "string" + ("!" + "+".join(hit) if hit else ""), shown))
walk(doc, "")
print("CHECK posted_value_key=%(posted_value_key)d cookie_like=%(cookie_like)d tokenised_url=%(tokenised_url)d jwt_like=%(jwt_like)d" % found)
print("CHECK VERDICT: %s" % ("CLEAN on all four" if not any(found.values()) else "FOUND -- the flagged leaves are shown as length and hash only"))
print("LEAVES=%d" % len(rows))
for where, kind, shown in rows[:400]:
    print("LEAF %s | %s | %s" % (where, kind, shown))
PY
echo "END"
