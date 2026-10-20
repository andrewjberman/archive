export V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m
set -u
# IRPT_ANLREQ TO-READ-PACKAGER-PROBE (applier 0.7.0_AE_CloudOps~IB2), READ ONLY: probe A (one package POST to a bogus ticket id through the resident's own port)
# and probe B (head and one-byte ranged get of run 6's leftover commentary draft), inside the resident service's own environment (user, cwd, Environment= entries).
# Nothing is printed of the secret, token, header, URL or email; probe B prints no byte.
U=irpt-analysis-resident.service
echo "PROBE unit: $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U)"
USR=$(systemctl show -p User --value $U)
WD=$(systemctl show -p WorkingDirectory --value $U)
ENVS=$(systemctl show -p Environment --value $U)
PY=$(systemctl show -p ExecStart --value $U | grep -o 'argv\[\]=[^ ]*' | head -1 | cut -d= -f2)
EXEC=$(systemctl show -p ExecStart --value $U)
WANT_ROOT=${V2S_WANT_ROOT:-/opt/irpt-resident/0485393f3a-r34m}
ROOT=$WD
echo "PROBE user=$USR workdir=$WD interpreter=$PY"
echo "PROBE environment entries: $(echo "$ENVS" | wc -w)"
if [ -z "$USR" ] || [ -z "$WD" ] || [ -z "$PY" ]; then echo "PROBE FAIL a unit property is empty (user, workdir or interpreter)"; exit 61; fi
if [ "$ROOT" != "$WANT_ROOT" ]; then echo "PROBE FAIL the working directory (the running root) is $ROOT, want $WANT_ROOT"; exit 62; fi
if ! echo "$EXEC" | grep -q "$ROOT/ycharts/generate/resident_main.py"; then echo "PROBE FAIL ExecStart does not run resident_main.py from $ROOT"; exit 63; fi
SETENV=""
for e in $ENVS; do SETENV="$SETENV --setenv=$e"; done
PYF=${V2S_PYFILE:-/tmp/probe_pkg_ib2.py}
cat > "$PYF" <<'PYEOF'
import json
import re
import sys

import boto3

root = "/opt/irpt-resident/0485393f3a-r34m"
sys.path[:0] = [root + "/ycharts/research", root + "/reports", root + "/ycharts/generate", root + "/intake", root]


def clean(text):
    text = re.sub(r"https?://\S+", "<redacted>", str(text))
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", "<redacted>", text)
    return re.sub(r"eyJ[A-Za-z0-9_-]{10,}", "<redacted>", text)


try:
    import opal_packager
    import resident_installed as ri
    cfg = json.load(open(root + "/reports/resident_bindings.json"))["packager"]
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    ports = opal_packager.live_ticket_ports(cfg, read_secret=ri._read_secret_string(sm), http=ri._packager_http)
    payload = {"report_ref": "x", "pdf_ref": None, "original_ref": "x", "commentary_ref": None,
               "firm": "49financial", "request_id": "REQ-" + "0" * 24, "request_revision": 1}
    try:
        print("PROBE A_RETURNED", type(ports["attach"]("TCK-20261020-00000000", payload)).__name__)
    except Exception as exc:
        print("PROBE A_EXC", type(exc).__name__, clean(str(exc)[:80]))
except BaseException as exc:
    print("PROBE A_SETUP_EXC", type(exc).__module__, type(exc).__name__, clean(str(exc)[:80]))

KEY = "irpt/49financial/state/analysis_commentaries/ART-79633aa8d7f0469502681195a8dc13ecd4e71872bc877bea713a7b330810b159/e889189c5218f84be1e747361279d092f1d4b495b908f3ea99db9b066cb6b3c3.json"
s3 = boto3.client("s3", region_name="us-east-1")
res = {}
for name, call in (("head", lambda: s3.head_object(Bucket="opal-data-irpt", Key=KEY)),
                   ("get", lambda: s3.get_object(Bucket="opal-data-irpt", Key=KEY, Range="bytes=0-0"))):
    try:
        call()
        res[name] = "ok"
    except Exception as exc:
        code = getattr(exc, "response", {}).get("Error", {}).get("Code") if hasattr(exc, "response") else None
        res[name] = code or type(exc).__name__
print("PROBE B head=%s get=%s" % (res["head"], res["get"]))
PYEOF
chmod 644 "$PYF"
echo "PROBE script sha256: $(sha256sum "$PYF" | cut -d' ' -f1)"
systemd-run --quiet --wait --pipe --collect --uid="$USR" -p WorkingDirectory="$WD" $SETENV "$PY" "$PYF"
echo "PROBE systemd-run rc=$?"
rm -f "$PYF"
