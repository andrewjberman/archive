export V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m
set -u
# IRPT_ANLREQ TO-READ-PACKAGER-403 R1 (applier 0.7.0_AE_CloudOps~IB2), READ ONLY: the packager token's claim NAMES and times, read in memory by the service's own
# reader inside the service's own environment. Prints member names, the part count, claim names, UTC times, and sub/userType only as closed words. No value else.
U=irpt-analysis-resident.service
USR=$(systemctl show -p User --value $U)
WD=$(systemctl show -p WorkingDirectory --value $U)
ENVS=$(systemctl show -p Environment --value $U)
PY=$(systemctl show -p ExecStart --value $U | grep -o 'argv\[\]=[^ ]*' | head -1 | cut -d= -f2)
EXEC=$(systemctl show -p ExecStart --value $U)
WANT_ROOT=${V2S_WANT_ROOT:-/opt/irpt-resident/0485393f3a-r34m}
if [ -z "$USR" ] || [ -z "$WD" ] || [ -z "$PY" ]; then echo "R1H FAIL a unit property is empty"; exit 61; fi
if [ "$WD" != "$WANT_ROOT" ]; then echo "R1H FAIL the running root is $WD, want $WANT_ROOT"; exit 62; fi
if ! echo "$EXEC" | grep -q "$WD/ycharts/generate/resident_main.py"; then echo "R1H FAIL ExecStart does not run resident_main.py from $WD"; exit 63; fi
SETENV=""
for e in $ENVS; do SETENV="$SETENV --setenv=$e"; done
PYF=${V2S_PYFILE:-/tmp/r1_pkg403_ib2.py}
cat > "$PYF" <<'PYEOF'
import base64
import json
import re
import sys
from datetime import datetime, timezone

import boto3

root = "/opt/irpt-resident/0485393f3a-r34m"
sys.path[:0] = [root + "/ycharts/research", root + "/reports", root + "/ycharts/generate", root + "/intake", root]
try:
    import resident_installed as ri
    cfg = json.load(open(root + "/reports/resident_bindings.json"))["packager"]
    secret_name = None
    for key in ("secret_id", "secret_name", "secret", "token_secret"):
        if isinstance(cfg.get(key), str):
            secret_name = cfg[key]
            break
    print("R1 binding members=%s secret_member=%s" % (",".join(sorted(cfg)), "found" if secret_name else "NOT-FOUND"))
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    raw = ri._read_secret_string(sm)(secret_name if secret_name else "opal/ticketing/svc-irpt-packager")
    try:
        obj = json.loads(raw)
    except ValueError:
        obj = None
    if not isinstance(obj, dict):
        print("R1 members=<not-a-json-object> parts=- claims=-")
        raise SystemExit(0)
    members = sorted(obj)
    tok = obj.get("token")
    if not isinstance(tok, str) or not tok:
        print("R1 members=%s token=<absent-or-empty>" % ",".join(members))
        raise SystemExit(0)
    parts = tok.split(".")
    if len(parts) != 3:
        print("R1 members=%s parts=%d claims=-" % (",".join(members), len(parts)))
        raise SystemExit(0)
    seg = parts[1] + "=" * (-len(parts[1]) % 4)
    payload = json.loads(base64.urlsafe_b64decode(seg.encode("ascii")))
    now = datetime.now(timezone.utc)

    def utc(name):
        v = payload.get(name)
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, timezone.utc)
        return None

    def fmt(d):
        return d.strftime("%Y-%m-%dT%H:%M:%SZ") if d else "-"

    exp = utc("exp")
    sub = payload.get("sub")
    closed = lambda v: isinstance(v, str) and re.fullmatch(r"[a-z]{1,16}", v) is not None
    ut = payload.get("userType")
    scope_like = sorted(k for k in payload if "scope" in k.lower() or k.lower() in ("aud", "role", "tier"))
    extra = " ".join("%s=%s" % (k, payload[k]) for k in scope_like if closed(payload[k]))
    print("R1 members=%s parts=3 claims=%s iat=%s nbf=%s exp=%s expired=%s sub=%s userType=%s %s" % (
        ",".join(members), ",".join(sorted(payload)), fmt(utc("iat")), fmt(utc("nbf")), fmt(exp),
        ("yes" if exp < now else "no") if exp else "n/a",
        "svc-irpt-packager" if sub == "svc-irpt-packager" else "other",
        ut if closed(ut) else "-", extra))
    print("R1 now=%s" % fmt(now))
except SystemExit:
    raise
except BaseException as exc:
    print("R1 ERROR", type(exc).__module__, type(exc).__name__)
PYEOF
chmod 644 "$PYF"
echo "R1H script sha256: $(sha256sum "$PYF" | cut -d' ' -f1)"
systemd-run --quiet --wait --pipe --collect --uid="$USR" -p WorkingDirectory="$WD" $SETENV "$PY" "$PYF"
echo "R1H systemd-run rc=$?"
rm -f "$PYF"
