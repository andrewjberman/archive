export V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m
set -u
# IRPT_ANLREQ TO-READ-PACKAGER-CFPROBE (applier 0.7.0_AE_CloudOps~IB2), READ ONLY: step 1 (ONE package POST to a bogus ticket id through the CloudFront alias, the api_base
# overridden IN MEMORY only) and step 3 (the packager token's iss and aud as closed words), inside the resident service's own environment (user, cwd, Environment= entries).
# Nothing is printed of the secret, token, header, URL or email.
U=irpt-analysis-resident.service
echo "CFP unit: $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U)"
USR=$(systemctl show -p User --value $U)
WD=$(systemctl show -p WorkingDirectory --value $U)
ENVS=$(systemctl show -p Environment --value $U)
PY=$(systemctl show -p ExecStart --value $U | grep -o 'argv\[\]=[^ ]*' | head -1 | cut -d= -f2)
EXEC=$(systemctl show -p ExecStart --value $U)
WANT_ROOT=${V2S_WANT_ROOT:-/opt/irpt-resident/0485393f3a-r34m}
ROOT=$WD
echo "CFP user=$USR workdir=$WD interpreter=$PY"
if [ -z "$USR" ] || [ -z "$WD" ] || [ -z "$PY" ]; then echo "CFP FAIL a unit property is empty (user, workdir or interpreter)"; exit 61; fi
if [ "$ROOT" != "$WANT_ROOT" ]; then echo "CFP FAIL the working directory (the running root) is $ROOT, want $WANT_ROOT"; exit 62; fi
if ! echo "$EXEC" | grep -q "$ROOT/ycharts/generate/resident_main.py"; then echo "CFP FAIL ExecStart does not run resident_main.py from $ROOT"; exit 63; fi
SETENV=""
for e in $ENVS; do SETENV="$SETENV --setenv=$e"; done
PYF=${V2S_PYFILE:-/tmp/cfprobe_pkg_ib2.py}
cat > "$PYF" <<'PYEOF'
import base64
import json
import re
import sys
from datetime import datetime, timezone

import boto3

root = "/opt/irpt-resident/0485393f3a-r34m"
sys.path[:0] = [root + "/ycharts/research", root + "/reports", root + "/ycharts/generate", root + "/intake", root]


def clean(text):
    text = re.sub(r"https?://\S+", "<redacted>", str(text))
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", "<redacted>", text)
    return re.sub(r"eyJ[A-Za-z0-9_-]{10,}", "<redacted>", text)


def stamp():
    return datetime.now(timezone.utc).strftime("%H:%M:%S") + "Z"


try:
    import opal_packager
    import resident_installed as ri
    cfg = dict(json.load(open(root + "/reports/resident_bindings.json"))["packager"])
    secret_name = cfg["secret_name"]
    cfg["api_base"] = "https://opalinvest.dev"
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    ports = opal_packager.live_ticket_ports(cfg, read_secret=ri._read_secret_string(sm), http=ri._packager_http)
    payload = {"report_ref": "x", "pdf_ref": None, "original_ref": "x", "commentary_ref": None,
               "firm": "49financial", "request_id": "REQ-" + "0" * 24, "request_revision": 1}
    t0 = stamp()
    try:
        print("CFP A2_RETURNED", type(ports["attach"]("TCK-20261020-00000000", payload)).__name__, "at", t0)
    except Exception as exc:
        print("CFP A2_EXC", type(exc).__name__, clean(str(exc)[:80]), "at", t0)
except BaseException as exc:
    print("CFP A2_SETUP_EXC", type(exc).__module__, type(exc).__name__, clean(str(exc)[:80]))
    secret_name = None

try:
    sm2 = boto3.client("secretsmanager", region_name="us-east-1")
    raw = ri._read_secret_string(sm2)(secret_name or "opal/ticketing/svc-irpt-packager")
    tok = json.loads(raw)["token"]
    seg = tok.split(".")[1]
    payload_claims = json.loads(base64.urlsafe_b64decode((seg + "=" * (-len(seg) % 4)).encode("ascii")))
    iss = "opal-portal-auth" if payload_claims.get("iss") == "opal-portal-auth" else "other"
    aud = "opal-portal-api" if payload_claims.get("aud") == "opal-portal-api" else "other"
    print("CFP T iss=%s aud=%s" % (iss, aud))
except BaseException as exc:
    print("CFP T_EXC", type(exc).__module__, type(exc).__name__)
PYEOF
chmod 644 "$PYF"
echo "CFP script sha256: $(sha256sum "$PYF" | cut -d' ' -f1)"
systemd-run --quiet --wait --pipe --collect --uid="$USR" -p WorkingDirectory="$WD" $SETENV "$PY" "$PYF"
echo "CFP systemd-run rc=$?"
rm -f "$PYF"
