#!/usr/bin/env python3
"""LIVE_WAF_READ_C1 -- POSN_AGGFIX.TO-C1-1 AMENDMENT 2, criteria C1-AC19 (--phase before) and C1-AC20 (--phase after).

Reads the LIVE WebACL opal-cloudfront-protection (wafv2 get-web-acl, scope CLOUDFRONT, us-east-1) -- never Terraform,
never the plan -- and records, per rule: name, priority, action, override_action, statement (the managed rule group's
name, vendor and version when it is a managed rule group statement; the whole statement, canonical JSON, for every
rule) and visibility_config.

  --phase before  prints the LockToken and every rule, writes .scratch/c1_waf_before.json (the per-rule fields plus
                  the whole get-web-acl response, which is the restore input the COO half names), prints
                  `WAF RULES CAPTURED <n>` and whether the three managed rules are present.
  --phase after   the same read, compared field by field against .scratch/c1_waf_before.json; prints the managed rules'
                  version fields on both sides, the rule counts, both LockTokens, and `WAF RULES UNCHANGED <k> of <n>`.
Exit 0 when the expectation holds; 1 when it does not; 2 on a read failure.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("c1_edge_route_census", HERE / "c1_edge_route_census.py")
census = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(census)
ROOT = census.ROOT
NAME = "opal-cloudfront-protection"
BEFORE_FILE = ROOT / ".scratch" / "c1_waf_before.json"
MANAGED = ("common-rule-set", "ip-reputation", "known-bad-inputs")
FIELDS = ("name", "priority", "action", "override_action", "statement", "visibility_config")


def aws_json(args: str) -> dict:
    rc, out, err = census.run_bash(f"aws {args} --output json", timeout=180)
    if rc != 0:
        print(f"ERROR: aws {args} rc={rc}: {err.strip()[:300]}")
        sys.exit(2)
    return json.loads(out)


def canon(v) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"))


def read_live() -> tuple[dict, list[dict]]:
    listed = aws_json("wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1")
    acls = [a for a in listed.get("WebACLs", []) if a.get("Name") == NAME]
    print(f"  list-web-acls CLOUDFRONT us-east-1: {len(listed.get('WebACLs', []))} WebACL(s); named {NAME}: {len(acls)}")
    if len(acls) != 1:
        print(f"ERROR: expected exactly 1 WebACL named {NAME}, found {len(acls)}")
        sys.exit(2)
    acl_id = acls[0]["Id"]
    resp = aws_json(f"wafv2 get-web-acl --name {NAME} --scope CLOUDFRONT --id {acl_id} --region us-east-1")
    rules = []
    for r in resp["WebACL"].get("Rules", []):
        st = r.get("Statement", {})
        mrg = st.get("ManagedRuleGroupStatement")
        rules.append({
            "name": r.get("Name"),
            "priority": r.get("Priority"),
            "action": canon(r["Action"]) if "Action" in r else None,
            "override_action": canon(r["OverrideAction"]) if "OverrideAction" in r else None,
            "statement": canon(st),
            "managed": None if mrg is None else {
                "name": mrg.get("Name"), "vendor": mrg.get("VendorName"),
                "version": mrg.get("Version", "<absent>")},
            "visibility_config": canon(r.get("VisibilityConfig")),
        })
    return resp, rules


def show(rules: list[dict]) -> None:
    for r in sorted(rules, key=lambda x: x["priority"]):
        m = r["managed"]
        stmt = (f"managed {m['vendor']}/{m['name']} version={m['version']}" if m else
                f"statement {r['statement'][:90]}")
        act = f"override_action {r['override_action']}" if r["override_action"] else f"action {r['action']}"
        print(f"  rule p{r['priority']} {r['name']:<22} {act:<40} {stmt}")
        print(f"       visibility_config {r['visibility_config']}")


def main() -> int:
    if "--phase" not in sys.argv or sys.argv[sys.argv.index("--phase") + 1] not in ("before", "after"):
        print("usage: python c1_live_waf_read.py --phase before|after")
        return 2
    phase = sys.argv[sys.argv.index("--phase") + 1]
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"C1-{'AC19' if phase == 'before' else 'AC20'} LIVE_WAF_READ_C1 -- WebACL {NAME} (CLOUDFRONT, us-east-1) at {now}")
    resp, rules = read_live()
    lock = resp.get("LockToken", "")
    print(f"  LockToken {lock}; WebACL Id {resp['WebACL'].get('Id')}; DefaultAction {canon(resp['WebACL'].get('DefaultAction'))}")
    show(rules)
    names = {r["name"] for r in rules}
    present = [m for m in MANAGED if m in names]
    if phase == "before":
        BEFORE_FILE.parent.mkdir(parents=True, exist_ok=True)
        BEFORE_FILE.write_text(json.dumps({"read_at": now, "lock_token": lock, "rules": rules,
                                           "get_web_acl_response": resp}, indent=2) + "\n", encoding="utf-8")
        print(f"  written: {BEFORE_FILE}")
        print(f"  managed rules present: {len(present)} of {len(MANAGED)} {present}")
        print(f"WAF RULES CAPTURED {len(rules)}")
        return 0 if (rules and len(present) == len(MANAGED)) else 1
    if not BEFORE_FILE.exists():
        print(f"  {BEFORE_FILE} ABSENT -- C1-AC19 was not captured; nothing to compare")
        return 1
    before = json.loads(BEFORE_FILE.read_text(encoding="utf-8"))
    b_rules = {r["name"]: r for r in before["rules"]}
    a_rules = {r["name"]: r for r in rules}
    print(f"  LockToken before {before['lock_token']} (read {before['read_at']}); LockToken after {lock}")
    print(f"  rule count before {len(b_rules)}; after {len(a_rules)}")
    unchanged = 0
    for name in sorted(set(b_rules) | set(a_rules)):
        b, a = b_rules.get(name), a_rules.get(name)
        if b is None or a is None:
            print(f"  DIFFER {name}: present before={b is not None} after={a is not None}")
            continue
        diffs = [f for f in FIELDS if b[f] != a[f]]
        if diffs:
            for f in diffs:
                print(f"  DIFFER {name} {f}: before {b[f]} after {a[f]}")
        else:
            unchanged += 1
        if b["managed"] or a["managed"]:
            bv = (b["managed"] or {}).get("version")
            av = (a["managed"] or {}).get("version")
            print(f"  managed version {name}: before {bv} after {av}")
    n = len(b_rules)
    print(f"WAF RULES UNCHANGED {unchanged} of {n}")
    return 0 if (unchanged == n and len(a_rules) == n) else 1


if __name__ == "__main__":
    sys.exit(main())
