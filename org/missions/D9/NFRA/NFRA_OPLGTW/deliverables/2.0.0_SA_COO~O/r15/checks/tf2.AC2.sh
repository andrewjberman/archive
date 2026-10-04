#!/usr/bin/env bash
# OPLGTW OG-tf-2 AC2 (analysis round 14 R2): gateway/principals/rosters carries mcportal_owner_key and
# mcportal_owner_key_claim whose value sha256 equal the live grant writer's MCPORTAL_OWNER_KEY / MCPORTAL_OWNER_KEY_CLAIM,
# and its three pre-existing keys are still present. Booleans and counts only; no value is printed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
S="${TMP:-/tmp}/og_r15_tf2_$$.json"
aws secretsmanager get-secret-value --region us-east-1 --secret-id gateway/principals/rosters --query SecretString --output text | tr -d '\r' > "$S.sec"
aws lambda get-function-configuration --region us-east-1 --function-name mcportal-grant-writer-lambda --query Environment.Variables --output json | tr -d '\r' > "$S.env"
python - "$(native "$S.sec")" "$(native "$S.env")" <<'PY'
import hashlib, json, sys
s = json.load(open(sys.argv[1], encoding="utf-8")); e = json.load(open(sys.argv[2], encoding="utf-8")) or {}
def H(v):
    return hashlib.sha256(str(v).encode("utf-8")).hexdigest()
k1 = "mcportal_owner_key" in s and "MCPORTAL_OWNER_KEY" in e and H(s["mcportal_owner_key"]) == H(e["MCPORTAL_OWNER_KEY"])
k2 = ("mcportal_owner_key_claim" in s and "MCPORTAL_OWNER_KEY_CLAIM" in e
      and H(s["mcportal_owner_key_claim"]) == H(e["MCPORTAL_OWNER_KEY_CLAIM"]))
pre = all(k in s for k in ("master_admin", "write_capable", "taxsma_workbook_identity"))
print("secret keys %d; owner_key equal %s; owner_key_claim equal %s; pre-existing three present %s" % (len(s), k1, k2, pre))
ok = k1 and k2 and pre
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
PY
rc=$?; rm -f "$S.sec" "$S.env"; exit $rc
