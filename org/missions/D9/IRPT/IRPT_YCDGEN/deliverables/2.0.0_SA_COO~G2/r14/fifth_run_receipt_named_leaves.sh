set -u
# READ ONLY. IRPT_YCDGEN round 14: read out NAMED leaves of the sign-in receipt the fifth run left on the host, the list
# IRPT_BCKEND asked for (2.0.0_SA_COO~P2 msg 5551, cell IB141-1). No new run, no request, no sign-in. A value is printed
# ONLY if it is a boolean, null, a number, or a short closed word (letters, digits, _ . : - and nothing else, 40 characters
# at most); anything else is shown as a length and a hash. The receipt is not copied. Operator 0.7.0_AE_CloudOps~YC2.
H=/opt/investor-reporting-ycharts
echo "AT $(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3.12 - "$H/last-capture.receipt.json" <<'PY'
import hashlib, json, os, re, sys
path = sys.argv[1]
if not os.path.isfile(path):
    print("RECEIPT ABSENT")
    raise SystemExit(0)
raw = open(path, "rb").read()
print("RECEIPT bytes=%d sha256=%s mtime_epoch=%d (the j5 read saw bytes=3824 sha256=c1157ec45071b41e)" % (
    len(raw), hashlib.sha256(raw).hexdigest()[:16], int(os.path.getmtime(path))))
doc = json.loads(raw.decode("utf-8"))
WORD = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,39}")
shown = withheld = 0
def show(value):
    global shown, withheld
    if value is None or isinstance(value, (bool, int, float)):
        shown += 1
        return repr(value)
    s = str(value)
    if WORD.fullmatch(s):
        shown += 1
        return s
    withheld += 1
    return "WITHHELD len=%d sha=%s" % (len(s), hashlib.sha256(s.encode("utf-8")).hexdigest()[:10])
def get(node, *keys):
    for k in keys:
        if isinstance(node, dict) and k in node:
            node = node[k]
        elif isinstance(node, list) and isinstance(k, int) and 0 <= k < len(node):
            node = node[k]
        else:
            return "ABSENT"
    return node
def line(n, label, value):
    if value == "ABSENT":
        print("ASK %s | %s | ABSENT" % (n, label))
    elif isinstance(value, list):
        print("ASK %s | %s | list len=%d | %s" % (n, label, len(value), ", ".join(show(v) for v in value[:20])))
    elif isinstance(value, dict):
        print("ASK %s | %s | object with keys: %s" % (n, label, ", ".join(sorted(map(str, value)))[:300]))
    else:
        print("ASK %s | %s | %s" % (n, label, show(value)))
pp = get(doc, "probe_pair")
line("1", "probe_pair.without_token_waf_action_class", get(pp, "without_token_waf_action_class"))
line("2", "probe_pair.without_token_via", get(pp, "without_token_via"))
line("3", "probe_pair.without_token_content_type_class", get(pp, "without_token_content_type_class"))
line("4", "probe_pair.with_token_waf_action_class", get(pp, "with_token_waf_action_class"))
line("5a", "probe_pair.with_token_via", get(pp, "with_token_via"))
line("5b", "probe_pair.with_token_errored", get(pp, "with_token_errored"))
line("6", "probe_pair.sent_without_token.session_cookie_names_present", get(pp, "sent_without_token", "session_cookie_names_present"))
steps = get(doc, "steps")
n = len(steps) if isinstance(steps, list) else 0
print("STEPS=%d" % n)
for i in range(1, n):
    line("7", "steps[%d].probe_via" % i, get(steps, i, "probe_via"))
for i in range(0, n):
    line("8", "steps[%d].state" % i, get(steps, i, "state"))
    line("8", "steps[%d].via" % i, get(steps, i, "via"))
# two controls the list did not ask for, so the answers can be placed: the same-named state and status leaves of the pair
line("c1", "probe_pair.without_token_state", get(pp, "without_token_state"))
line("c2", "probe_pair.with_token_state", get(pp, "with_token_state"))
line("c3", "reason", get(doc, "reason"))
print("SHOWN=%d WITHHELD=%d" % (shown, withheld))
PY
echo "END"
