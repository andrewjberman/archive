#!/usr/bin/env bash
# OPLGTW OG-cp-1 AC2 (PRD v2.9 C-PERSON): the new record kind is ONE contract, everywhere it is read.
#  - org/standards/NFRA_OPLGTW_CONTRACT.json and infra/aws/ec2/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json are byte-equal;
#  - state_store.record_types carries "person_access" exactly once;
#  - state_store.person_access declares the record's fields: status, revision, tools_allow, tools_deny, channels_allow,
#    channels_deny, updated_at, updated_by (and no tier field: tier records are out of this cell);
#  - app/access_state.py POLICY_RECORD_TYPES carries "person_access" (read by AST, not imported).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
python - <<'EOF'
import ast, json, sys
A = "org/standards/NFRA_OPLGTW_CONTRACT.json"
B = "infra/aws/ec2/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json"
FIELDS = {"status", "revision", "tools_allow", "tools_deny", "channels_allow", "channels_deny", "updated_at", "updated_by"}
same = open(A, "rb").read() == open(B, "rb").read()
st = json.load(open(A, encoding="utf-8")).get("state_store", {})
n = st.get("record_types", []).count("person_access")
spec = st.get("person_access") or {}
fields = set((spec.get("fields") or {}).keys()) if isinstance(spec.get("fields"), dict) else set(spec.get("fields") or [])
tree = ast.parse(open("infra/aws/ec2/opal-gateway/app/access_state.py", encoding="utf-8").read())
prt = ()
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "POLICY_RECORD_TYPES" for t in node.targets):
        prt = ast.literal_eval(node.value)
in_code = "person_access" in prt
print("contract copies byte-equal: %s; person_access in record_types %d time(s) (want 1)" % ("yes" if same else "no", n))
print("person_access fields declared %d of %d; missing %s; tier field present: %s" % (
    len(FIELDS & fields), len(FIELDS), sorted(FIELDS - fields), "yes" if "tier" in fields else "no"))
print("POLICY_RECORD_TYPES carries person_access: %s" % ("yes" if in_code else "no"))
ok = same and n == 1 and FIELDS <= fields and "tier" not in fields and in_code
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
