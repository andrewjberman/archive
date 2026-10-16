#!/usr/bin/env bash
# MP-pf-7 read step (the issuer's; a worker runs it and keeps its stdout). READ-ONLY. Three reads, in this order, printing one line each:
#   SIM   `iam simulate-principal-policy` for THIS box's AWS identity (the IAM user the `.tools/aws` shim resolves to, NOT the gateway host role) on the grant table's ARN:
#         dynamodb:Scan (the question), dynamodb:DescribeTable (positive control) and the same Scan for the operator role opal-gateway-access-admin (negative control: measured denied, so it must read a deny and the simulator discriminates; this IAM user allows even a nonexistent action, so that would be no control).
#         If Scan is not `allowed` the script prints `RESULT: STOP` and reads nothing else: the cell files a BLOCKING row and a never-widen ask for read-only Scan on that one table follows; no other route.
#   RAW   a raw client-side-paginated `aws dynamodb scan` of gateway-access-state-table under that identity (--no-paginate, the LastEvaluatedKey followed, keys only): Count and ScannedCount per page and summed,
#         then the grant-bearing principal set: distinct (tid, oid) of items whose pk is POLICY#<tid>#<oid> with GUIDs and whose sk record type is principal_profile, data_entitlement or person_access, as 12-hex digests
#         of "<tid>:<oid>" lower-case (probe-* and EMAILDENY keys are not GUIDs and are excluded the way `canonical_guid` excludes them). No app code is imported.
#   PAGE  the set the People view lists, from the host under the instance role over SSM (_r3_page_probe.py).
# Output: `SIM ...`, `RAW {json}`, `ssm command=<id> status=<s>`, `R3PAGE {json}` and `RESULT: READ` (or `RESULT: STOP` / `RESULT: INCOMPLETE`). Raw ids never appear.
. "$(dirname "$0")/../../pc/checks/_root.sh"
TB=gateway-access-state-table; RG=us-east-1; ME="${MP_PF7_ARN:-arn:aws:iam::313476888478:user/Andrew_Berman}"
T="${TMPDIR:-/tmp}/mp_pf7_$$"; mkdir -p "$T"; TM="$(cygpath -m "$T")"
ARN=$(timeout 40 "$AWS" dynamodb describe-table --table-name "$TB" --region $RG --query Table.TableArn --output text 2>&1 | tr -d '\r')
sim() { timeout 40 "$AWS" iam simulate-principal-policy --policy-source-arn "${2:-$ME}" --action-names "$1" --resource-arns "$ARN" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1 | tr -d '\r' | tail -1; }
S=$(sim dynamodb:Scan); D=$(sim dynamodb:DescribeTable); N=$(sim dynamodb:Scan "arn:aws:iam::313476888478:role/opal-gateway-access-admin")
echo "SIM identity=$(printf '%s' "$ME" | sed 's#.*/##') table_arn_ok=$([ "${ARN#arn:aws:dynamodb:}" != "$ARN" ] && echo yes || echo no) Scan=$S DescribeTable=$D OperatorRoleScan=$N"
if [ "$S" != allowed ]; then echo "RESULT: STOP"; rm -rf "$T"; exit 3; fi
# the raw scan, one page at a time, keys only
i=0; KEY=""; while :; do
  i=$((i+1))
  if [ -z "$KEY" ]; then timeout 90 "$AWS" dynamodb scan --table-name "$TB" --region $RG --projection-expression "#p, #s" --expression-attribute-names '{"#p":"pk","#s":"sk"}' --no-paginate --output json > "$T/page_$i.json" 2> "$T/err_$i.txt"
  else printf '%s' "$KEY" > "$T/key_$i.json"; timeout 90 "$AWS" dynamodb scan --table-name "$TB" --region $RG --projection-expression "#p, #s" --expression-attribute-names '{"#p":"pk","#s":"sk"}' --no-paginate --exclusive-start-key "file://$TM/key_$i.json" --output json > "$T/page_$i.json" 2> "$T/err_$i.txt"; fi
  KEY=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(json.dumps(d['LastEvaluatedKey']) if d.get('LastEvaluatedKey') else '')" "$TM/page_$i.json" 2>/dev/null | tr -d '\r')
  [ -z "$KEY" ] && break; [ "$i" -ge 50 ] && break
done
python - "$TM" "$i" <<'PY'
import hashlib, json, re, sys
d, n = sys.argv[1], int(sys.argv[2])
GUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
BEARING = {"principal_profile", "data_entitlement", "person_access"}
pages, count, scanned, policy, bearing, audit = [], 0, 0, 0, set(), set()
policy_total, excluded = 0, {}
dg = lambda t, o: hashlib.sha256(("%s:%s" % (t.lower(), o.lower())).encode()).hexdigest()[:12]
ok = True
for k in range(1, n + 1):
    try:
        p = json.load(open("%s/page_%d.json" % (d, k), encoding="utf-8"))
    except Exception:
        ok = False; break
    pages.append([p.get("Count"), p.get("ScannedCount")]); count += p.get("Count") or 0; scanned += p.get("ScannedCount") or 0
    for it in p.get("Items") or []:
        pk, sk = it["pk"]["S"], it["sk"]["S"]
        parts = pk.split("#")
        if parts[0] == "POLICY":
            policy_total += 1
        if len(parts) != 3 or parts[0] != "POLICY" or not (GUID.match(parts[1]) and GUID.match(parts[2])):
            if parts[0] == "POLICY":
                key = "emaildeny" if parts[1:2] == ["EMAILDENY"] else ("probe" if parts[1:2] and parts[1].startswith("probe-") else "other_not_a_principal_key")
                excluded[key] = excluded.get(key, 0) + 1
            continue
        policy += 1
        rt = sk.split("#")[0]
        if rt in BEARING: bearing.add(dg(parts[1], parts[2]))
        elif rt == "operator_audit":
            audit.add(dg(parts[1], parts[2])); excluded["operator_audit_item"] = excluded.get("operator_audit_item", 0) + 1
        else: excluded["other_record_type_on_a_principal"] = excluded.get("other_record_type_on_a_principal", 0) + 1
WHY = {"emaildeny": "POLICY#EMAILDENY#<digest> is an email deny entry, not a principal key", "probe": "POLICY#probe-* is a test probe key whose id is not a GUID (canonical_guid excludes it as the page does)",
       "other_not_a_principal_key": "a POLICY# key that is not POLICY#<guid>#<guid>", "operator_audit_item": "an audit row of the grant writer, not a grant (a principal with only audit rows is counted as audit_only_principals)",
       "other_record_type_on_a_principal": "a record type that is not principal_profile, data_entitlement or person_access"}
print("RAW " + json.dumps({"complete": ok, "pages": n, "per_page": pages, "count": count, "scanned": scanned, "policy_items": policy,
      "policy_total": policy_total, "excluded": [{"class": k, "count": v, "reason": WHY[k]} for k, v in sorted(excluded.items())],
      "raw_set": sorted(bearing), "raw_n": len(bearing), "audit_only_principals": len(audit - bearing)}))
PY
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks/_r3_page_probe.py "$TM/params.json"
ssm_run "$T/params.json"
echo "ssm command=$SSM_CID status=$SSM_ST"
printf '%s\n' "$SSM_OUT" | grep -m1 '^R3PAGE ' || echo "no R3PAGE line; last output: $(printf '%s\n' "$SSM_OUT" | tail -1 | cut -c1-300)"
rm -rf "$T"
echo "RESULT: READ"
