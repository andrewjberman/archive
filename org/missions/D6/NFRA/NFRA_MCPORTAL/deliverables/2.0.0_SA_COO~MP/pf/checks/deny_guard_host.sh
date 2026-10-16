#!/usr/bin/env bash
# MP-v-2 gate read (the issuer's, READ-ONLY, one SSM command under the gateway host's instance role): the browser guard's own verdict for each account,
# `data_entitlement.email_denial(email)` run in the gateway's venv (`import app.server` first, row Z-S48). None = the caller may proceed on /login, /sprint*, /rivalfunds*, /yearinreview*; 403 = denied; 503 = the store was unreadable.
# Prints one `GUARD <label> <verdict>` line per account (labels only). Ruling: CTO msg 35204; expected after (b): andrew None, opalbloomberg None, alyssa 403 (it stays denied: the control).
. "$(dirname "$0")/../../pc/checks/_root.sh"
T="${TMPDIR:-/tmp}/mp_guard_$$"; mkdir -p "$T"
python - "$(cygpath -m "$T")/p.json" <<'PY'
import json, sys
PROBE = (
    "import app.server\n"
    "from app import data_entitlement as D\n"
    "for label, email in (('andrew', 'andrew@opalinvest.com'), ('opalbloomberg', 'opalbloomberg@opalinvest.com'), ('alyssa', 'alyssa@opalinvest.com')):\n"
    "    print('GUARD %s %s' % (label, D.email_denial(email)))\n"
)
cmd = ("printf '%s' '" + PROBE.replace("'", "'\"'\"'") + "' > /tmp/mp_guard_probe.py; "
       "cd /opt/opal-gateway && sudo -u ec2-user env PYTHONPATH=/opt/opal-gateway .venv/bin/python /tmp/mp_guard_probe.py 2>&1 | grep '^GUARD '; rm -f /tmp/mp_guard_probe.py")
json.dump({"commands": [cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
PY
ssm_run "$T/p.json"; rm -rf "$T"
echo "ssm command=$SSM_CID status=$SSM_ST"
printf '%s\n' "$SSM_OUT" | grep '^GUARD '
a=$(printf '%s\n' "$SSM_OUT" | grep -c '^GUARD andrew None'); o=$(printf '%s\n' "$SSM_OUT" | grep -c '^GUARD opalbloomberg None'); l=$(printf '%s\n' "$SSM_OUT" | grep -c '^GUARD alyssa 403')
echo "andrew proceeds: $a; opalbloomberg proceeds: $o; alyssa still denied (control): $l"
if [ "$SSM_ST" = Success ] && [ "$a" = 1 ] && [ "$o" = 1 ] && [ "$l" = 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
