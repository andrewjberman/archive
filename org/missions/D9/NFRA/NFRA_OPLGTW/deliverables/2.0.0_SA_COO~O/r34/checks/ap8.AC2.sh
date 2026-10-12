#!/usr/bin/env bash
# OPLGTW OG-ap-8 AC2 (the live grant, read now): the inline policy named in W/ap8_policy.json ({"role","policy_name"}) is read
# LIVE with iam get-role-policy. It has exactly one statement, Action s3:PutObject only, Resource exactly
# arn:aws:s3:::opal-data-transcripts/sharepoint/transcripts/bronze/market_update/* .
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap8_policy.json"
[ -f "$F" ] || { echo "ap8_policy.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r role pol <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('role',''),d.get('policy_name',''))" "$(native "$F")" | tr -d '\r')"
export AP8_DOC; AP8_DOC=$(bash .tools/aws iam get-role-policy --role-name "$role" --policy-name "$pol" --output json 2>&1 | tr -d '\r'); rc=$?
python - "$rc" <<'PY'
import json, sys, urllib.parse
rc = sys.argv[1]
import os
raw = os.environ.get('AP8_DOC', '')
try:
    d = json.loads(raw); pd = d.get("PolicyDocument")
    pd = json.loads(urllib.parse.unquote(pd)) if isinstance(pd, str) else pd
    st = pd.get("Statement", []); st = st if isinstance(st, list) else [st]
except Exception as exc:
    print("live read rc=%s unparseable: %s" % (rc, str(exc)[:120])); raise SystemExit(1)
want_res = "arn:aws:s3:::opal-data-transcripts/sharepoint/transcripts/bronze/market_update/*"
def lst(v): return v if isinstance(v, list) else [v]
ok = len(st) == 1 and lst(st[0].get("Action")) == ["s3:PutObject"] and lst(st[0].get("Resource")) == [want_res] \
     and st[0].get("Effect") == "Allow"
print("live read rc=%s; statements %d; actions %s; resources %s" % (rc, len(st), lst(st[0].get("Action")) if st else None,
      lst(st[0].get("Resource")) if st else None))
raise SystemExit(0 if ok and rc == "0" else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
