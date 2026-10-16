#!/usr/bin/env bash
# OPLGTW OG-ac-1 AC1 (round-37, CTO ruling @d97ea3ae82 section 2): the DynamoDB etf-classifications table is CENSUSED, read only, and its spec names the tool, the exact grant and the refusal arm.
#  - W/ETF_CLASS_CENSUS.json: table name, ARN, item_count (an integer), key_schema (hash/range names), attribute_names (a non-empty list), classified_by counts (a dict of integer counts), a freshness field and the newest value's date, each with a `claim` word of measured|inferred|absent;
#  - W/ETF_CLASS_SPEC.md carries the three headed sections `## Tool`, `## Grant` and `## Refused`, and the grant names dynamodb:GetItem or dynamodb:Query and the table ARN, and NO dynamodb:Scan / PutItem / UpdateItem / DeleteItem / BatchWrite.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113"
[ -f "$W/ETF_CLASS_CENSUS.json" ] && [ -f "$W/ETF_CLASS_SPEC.md" ] || { echo "census or spec absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/ETF_CLASS_CENSUS.json")" "$(native "$W/ETF_CLASS_SPEC.md")" <<'PYEOF'
import json, re, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
spec = open(sys.argv[2], encoding="utf-8").read()
def val(k):
    v = c.get(k)
    return v.get("value") if isinstance(v, dict) and "value" in v else v
def claim(k):
    v = c.get(k)
    return v.get("claim") if isinstance(v, dict) else None
need = ("table_name", "table_arn", "item_count", "key_schema", "attribute_names", "classified_by_counts", "freshness_field", "newest_date")
have = [k for k in need if c.get(k) is not None]
claims_ok = all(claim(k) in ("measured", "inferred", "absent") for k in need if k in c)
ic = val("item_count")
shape = isinstance(ic, int) and isinstance(val("attribute_names"), list) and len(val("attribute_names")) > 0 and isinstance(val("classified_by_counts"), dict) \
    and all(isinstance(x, int) for x in val("classified_by_counts").values())
heads = all(re.search(r"(?m)^## %s\b" % h, spec) for h in ("Tool", "Grant", "Refused"))
g = spec.split("## Grant", 1)[1].split("\n## ", 1)[0] if "## Grant" in spec else ""
allow = ("dynamodb:GetItem" in g or "dynamodb:Query" in g) and (val("table_arn") or "@@") in g
deny_free = not re.search(r"(?<!no )(?<!never )dynamodb:(Scan|PutItem|UpdateItem|DeleteItem|BatchWriteItem)\b", re.sub(r"(?i)(no|never|not|without)[^.\n]*", "", g))
print("census: fields %d of %d; claim words ok %s; item_count/attributes/classified_by shaped %s; spec sections %s; grant names read action and the table arn %s; grant carries no write or scan action %s" % (len(have), len(need), claims_ok, shape, heads, allow, deny_free))
print("OK" if len(have) == len(need) and claims_ok and shape and heads and allow and deny_free else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
