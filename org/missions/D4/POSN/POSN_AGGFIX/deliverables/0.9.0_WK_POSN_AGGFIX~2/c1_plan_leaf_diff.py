#!/usr/bin/env python3
"""PLAN_LEAF_DIFF_C1 -- POSN_AGGFIX.TO-C1-1, the leaf reader for C1-AC9 (the deploy plan) and C1-AC11 (the re-plan, AMENDMENT 3).

Reads a saved plan's `terraform show -json` and prints, per resource change with an action, every changed leaf (a leaf known
only after apply counts as changed). It then names the plan's SHAPE against the three shapes the order and both never-widen
halves sign, and exits 0 only when the plan is one of them:

  DEPLOY    (C1-AC9, AMENDMENT 2): 3 addresses -- aws_lambda_function.auth_validator_edge[0] update with s3_object_version as
            its only known leaf; aws_cloudfront_distribution.portal update whose only moving leaves are lambda_arn values whose
            before-value names auth-validator-edge; aws_wafv2_web_acl.opal_cloudfront_protection update whose only leaves are
            the three managed_rule_group_statement version values '' -> null (common-rule-set, ip-reputation,
            known-bad-inputs), after_unknown empty.
  RESIDUAL  (C1-AC11, AMENDMENT 3): 1 address -- the WebACL with exactly those three version leaves; the function and the
            distribution carry no action.
  NO-CHANGES: 0 addresses with an action.
Anything else prints SHAPE: OTHER (Branch B) and exits 1.
"""
from __future__ import annotations

import json
import re
import sys

FN = "aws_lambda_function.auth_validator_edge[0]"
DIST = "aws_cloudfront_distribution.portal"
WAF = "aws_wafv2_web_acl.opal_cloudfront_protection"
WAF_RULES = ["common-rule-set", "ip-reputation", "known-bad-inputs"]
VERSION_LEAF = re.compile(r"^/rule/(\d+)/statement/0/managed_rule_group_statement/0/version$")


def leaves(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{pre}/{k}")
    elif isinstance(o, list):
        if not o:
            yield pre, []
        for i, v in enumerate(o):
            yield from leaves(v, f"{pre}/{i}")
    else:
        yield pre, o


def moving(change: dict) -> tuple[list[str], list[str], dict, dict]:
    b = dict(leaves(change.get("before") or {}))
    a = dict(leaves(change.get("after") or {}))
    unk = sorted(k for k, v in leaves(change.get("after_unknown") or {}) if v is True)
    known = [k for k in sorted(set(b) | set(a)) if b.get(k, "<absent>") != a.get(k, "<absent>") and k not in unk]
    return known, unk, b, a


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python c1_plan_leaf_diff.py <terraform show -json output>")
        return 2
    doc = json.load(open(sys.argv[1], encoding="utf-8"))
    rcs = doc.get("resource_changes", [])
    acted = [r for r in rcs if r["change"]["actions"] not in (["no-op"], ["read"])]
    print(f"PLAN_LEAF_DIFF_C1 -- {sys.argv[1]}")
    print(f"resource_changes {len(rcs)} ; with an action {len(acted)} ; addresses {[r['address'] for r in acted]}")
    ok = {FN: False, DIST: False, WAF: False}
    for r in acted:
        ch = r["change"]
        known, unk, b, a = moving(ch)
        print(f"== {r['address']} actions {ch['actions']}: known leaf changes {len(known)}; after_unknown {len(unk)}")
        if ch["actions"] != ["update"]:
            print("   action is not update")
            continue
        if r["address"] == FN:
            for k in known:
                print(f"   {k}: {json.dumps(b.get(k, '<absent>'))} -> {json.dumps(a.get(k, '<absent>'))}")
            print(f"   after_unknown: {unk}")
            ok[FN] = known == ["/s3_object_version"]
        elif r["address"] == DIST:
            mv = sorted(set(known) | set(unk))
            arn = [k for k in mv if k.endswith("/lambda_arn")]
            non = [k for k in mv if not k.endswith("/lambda_arn")]
            bad = [k for k in arn if ":function:auth-validator-edge:" not in str(b.get(k))]
            print(f"   lambda_arn leaves moving {len(arn)}; before-values {sorted({b.get(k) for k in arn})}")
            print(f"   lambda_arn leaves whose before-value is NOT auth-validator-edge: {len(bad)}; non-association leaves: {len(non)} {non}")
            ok[DIST] = bool(arn) and not bad and not non
        elif r["address"] == WAF:
            rules = (ch.get("before") or {}).get("rule", [])
            names = []
            for k in known:
                m = VERSION_LEAF.match(k)
                nm = rules[int(m.group(1))].get("name") if m and int(m.group(1)) < len(rules) else "?"
                if m:
                    names.append(nm)
                print(f"   {k} (rule {nm}): {json.dumps(b.get(k, '<absent>'))} -> {json.dumps(a.get(k, '<absent>'))}")
            other = [k for k in known if not VERSION_LEAF.match(k)]
            vals = all(b.get(k) == "" and a.get(k, "<absent>") is None for k in known if VERSION_LEAF.match(k))
            print(f"LEAF DIFFS {len(known)} (version leaves {len(known) - len(other)} on {sorted(names)}; values '' -> null {vals}; "
                  f"other leaves {len(other)}; after_unknown {len(unk)})")
            ok[WAF] = len(known) == 3 and not other and sorted(names) == WAF_RULES and vals and not unk
        else:
            print("   address outside the signed set")
    addrs = sorted(r["address"] for r in acted)
    if not acted:
        shape = "NO-CHANGES"
    elif addrs == sorted([FN, DIST, WAF]) and all(ok.values()):
        shape = "DEPLOY (C1-AC9: function version, 25-association ARNs, 3 WAF version leaves)"
    elif addrs == [WAF] and ok[WAF]:
        shape = "RESIDUAL (C1-AC11 AMENDMENT 3: ONE address with an action, the WebACL, 3 version leaves; function and distribution no action)"
    else:
        shape = "OTHER (Branch B)"
    print(f"SHAPE: {shape}")
    return 1 if shape.startswith("OTHER") else 0


if __name__ == "__main__":
    sys.exit(main())
