"""STOP 3 condition-2 audit: enumerate every attribute a saved Terraform plan changes.

Both NEVER-WIDEN halves of ETFS_RIVALS round 28 (COO @d3d6c3e73f, CTO @a0ee589cc2) sign only a plan whose
sole changing attribute is each Lambda's code package. The rendered plan hides unchanged attributes behind a
"(27 unchanged attributes hidden)" line, so reading condition 2 off the text is an eyeball check over a
redacted surface. This reads the machine form instead and prints the DENOMINATOR beside the verdict.

Usage:  terraform show -json <saved.tfplan> > plan.json && python -I <this> plan.json
"""
import json
import sys
from collections import Counter

ALLOWED = {"source_code_hash", "last_modified"}

src = sys.argv[1] if len(sys.argv) > 1 else "rv_plan28.json"
plan = json.load(open(src))
rcs = plan.get("resource_changes", [])

act = Counter()
for rc in rcs:
    act[tuple(rc["change"]["actions"])] += 1
print("DENOMINATOR: %d resource_changes in the plan" % len(rcs))
print("  actions:", dict(act))

changing = [rc for rc in rcs if rc["change"]["actions"] != ["no-op"]]
print("\nNON-NO-OP: %d" % len(changing))

verdict_ok = True
for rc in sorted(changing, key=lambda r: r["address"]):
    before = rc["change"]["before"] or {}
    after = rc["change"]["after"] or {}
    unknown = rc["change"].get("after_unknown") or {}
    diffs = []
    for k in sorted(set(before) | set(after) | set(unknown)):
        if unknown.get(k) is True:
            diffs.append((k, "-> (known after apply)"))
        elif before.get(k) != after.get(k):
            diffs.append((k, "%r -> %r" % (before.get(k), after.get(k))))
    extra = [k for k, _ in diffs if k not in ALLOWED]
    print("\n%s" % rc["address"])
    print("  type=%s actions=%s" % (rc["type"], rc["change"]["actions"]))
    print("  memory_size: %r -> %r" % (before.get("memory_size"), after.get("memory_size")))
    print("  timeout:     %r -> %r" % (before.get("timeout"), after.get("timeout")))
    same = "SAME" if before.get("environment") == after.get("environment") else "*** DIFFERS ***"
    print("  environment: %s" % same)
    print("  role:        %s" % ("SAME" if before.get("role") == after.get("role") else "*** DIFFERS ***"))
    print("  changed attributes (%d): %s" % (len(diffs), [k for k, _ in diffs]))
    for k, d in diffs:
        print("      %-22s %s" % (k, d))
    if extra:
        verdict_ok = False
        print("  *** ATTRIBUTES OUTSIDE THE PACKAGE: %s ***" % extra)

types = sorted({rc["type"] for rc in changing})
addrs_ok = all(rc["address"].startswith("aws_lambda_function.stage[") for rc in changing)
print("\n--- VERDICT ---")
print("types changing: %s" % types)
print("all five are aws_lambda_function.stage: %s" % addrs_ok)
print("every action is update: %s" % all(rc["change"]["actions"] == ["update"] for rc in changing))
print("only package attributes change: %s" % verdict_ok)
branch_a = verdict_ok and addrs_ok and len(changing) == 5 and types == ["aws_lambda_function"]
print("BRANCH A" if branch_a else "*** NOT BRANCH A -- APPLY NOTHING ***")
