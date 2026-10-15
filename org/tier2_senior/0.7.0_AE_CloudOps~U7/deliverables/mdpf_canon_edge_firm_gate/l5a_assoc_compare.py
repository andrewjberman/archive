"""L5a: before (saved plan's change.before, state refreshed at plan time) vs after (live get-distribution) associations.

usage: python l5a_assoc_compare.py <plan.json> <dist_after.json> <expected_new_version>
ASCII only. Prints one line per behavior and the denominators; exit 0 = every expectation true, 1 = not.
"""
import json
import sys

plan = json.load(open(sys.argv[1], encoding="utf-8"))
live = json.load(open(sys.argv[2], encoding="utf-8"))
N = sys.argv[3]
FN = "auth-validator-edge"


def short(arn):
    # arn:aws:lambda:us-east-1:acct:function:NAME:VER -> NAME:VER
    return ":".join(arn.split(":")[-2:])


rc = [r for r in plan["resource_changes"] if r["address"] == "aws_cloudfront_distribution.portal"][0]
b = rc["change"]["before"]
before = {}
for beh in b["ordered_cache_behavior"]:
    before[beh["path_pattern"]] = sorted((a["event_type"], short(a["lambda_arn"])) for a in beh["lambda_function_association"])
dcb = b["default_cache_behavior"][0]
before["<default>"] = sorted((a["event_type"], short(a["lambda_arn"])) for a in dcb["lambda_function_association"])

cfg = live["Distribution"]["DistributionConfig"]
after = {}
for beh in cfg["CacheBehaviors"]["Items"]:
    items = beh.get("LambdaFunctionAssociations", {}).get("Items", []) or []
    after[beh["PathPattern"]] = sorted((a["EventType"], short(a["LambdaFunctionARN"])) for a in items)
items = cfg["DefaultCacheBehavior"].get("LambdaFunctionAssociations", {}).get("Items", []) or []
after["<default>"] = sorted((a["EventType"], short(a["LambdaFunctionARN"])) for a in items)

ok = True
print("behaviors before=%d after=%d (default + ordered); CustomErrorResponses after=%s" % (len(before), len(after), cfg["CustomErrorResponses"]["Quantity"]))
if set(before) != set(after):
    ok = False
    print("FAIL: behavior path sets differ", sorted(set(before) ^ set(after)))
n_before_fn = n_after_fn = n_at_old = n_at_new = n_other_eq = n_other = 0
for p in list(before):
    bl, al = before[p], after.get(p, [])
    bfn = [x for x in bl if x[1].startswith(FN + ":")]
    afn = [x for x in al if x[1].startswith(FN + ":")]
    bo = [x for x in bl if not x[1].startswith(FN + ":")]
    ao = [x for x in al if not x[1].startswith(FN + ":")]
    n_before_fn += len(bfn)
    n_after_fn += len(afn)
    n_at_old += sum(1 for x in afn if x[1] == FN + ":23")
    n_at_new += sum(1 for x in afn if x[1] == FN + ":" + N)
    n_other += len(ao)
    good = (len(bfn) == len(afn)) and all(x[1] == FN + ":" + N for x in afn) and all(x[1] == FN + ":23" for x in bfn) and bo == ao
    if bo == ao:
        n_other_eq += len(ao)
    if not good:
        ok = False
    print("%-4s %-40s before_fn=%s after_fn=%s others_equal=%s" % ("OK" if good else "FAIL", p, [x[1] for x in bfn], [x[1] for x in afn], bo == ao))
print("auth-validator-edge associations: before=%d (all at :23 = %s) after=%d at :%s=%d at :23=%d" % (
    n_before_fn, all(x[1] == FN + ':23' for v in before.values() for x in v if x[1].startswith(FN + ':')), n_after_fn, N, n_at_new, n_at_old))
print("other associations: after=%d byte-equal to before=%d" % (n_other, n_other_eq))
print("behaviors carrying the validator: after=%d" % sum(1 for p in after if any(x[1].startswith(FN + ":") for x in after[p])))
print("VERDICT", "PASS" if ok and n_at_old == 0 and n_after_fn == n_before_fn and cfg["CustomErrorResponses"]["Quantity"] == 0 else "FAIL")
sys.exit(0 if ok else 1)
