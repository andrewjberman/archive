#!/usr/bin/env python
"""OG-zs-1 A1 conditions (i) and (ii): snapshot the live WebACL's rule set, hashed, never printed.

The ruling accepts a 2-change plan ONLY if the WebACL's rule set is identical either side of the
apply. This writes that evidence in the shape the order names:

    {"rules": [{"name", "priority", "statement_sha256"}, ...], "rules_sha256"}

TWO HASHES, deliberately, because the named field alone would not catch the whole class:

  statement_sha256   canonical sha256 of that rule's `Statement` only -- the field the order names.
  rules_sha256       canonical sha256 of the WHOLE ordered rule list, every attribute included
                     (Action/OverrideAction, VisibilityConfig, RuleLabels, anything else). The churn
                     I measured in the plan touched `override_action` lines, so a digest over
                     `Statement` alone could read EQUAL across a change to how a rule ACTS. The
                     stronger digest is the one the before/after comparison turns on.

Rule bodies are hashed and never written: a managed-rule-group statement carries vendor rule names
and any excluded/overridden rule names, which is configuration detail this record does not need.

Usage: python .../zs1_acl_snapshot.py before|after
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys

ACL_NAME = "opal-cloudfront-protection"
ACL_ID = "a09833c0-4043-49fc-a92c-0dcdeaff9abd"
W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~Z")
SHIM = os.path.join(".tools", "aws.cmd" if sys.platform == "win32" else "aws")


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha(obj) -> str:
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


def main() -> int:
    phase = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if phase not in ("before", "after"):
        raise SystemExit("usage: zs1_acl_snapshot.py before|after")
    r = subprocess.run([SHIM, "wafv2", "get-web-acl", "--scope", "CLOUDFRONT", "--region", "us-east-1",
                        "--id", ACL_ID, "--name", ACL_NAME, "--output", "json"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("REFUSED: get-web-acl rc=%d: %s" % (r.returncode, r.stderr.decode("utf-8", "replace")[:300]))
    doc = json.loads(r.stdout.decode("utf-8", "replace"))
    acl = doc["WebACL"]
    rules = acl.get("Rules") or []
    if not rules:
        raise SystemExit("REFUSED: the ACL read returned 0 rules -- a vacuous read is not a before-state")
    ordered = sorted(rules, key=lambda x: (x.get("Priority", 0), x.get("Name", "")))
    rec = {
     "phase": phase,
     "read_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
     "web_acl": {"name": ACL_NAME, "id": ACL_ID, "scope": "CLOUDFRONT",
                 "lock_token": doc.get("LockToken"), "capacity": acl.get("Capacity")},
     "rule_count": len(ordered),
     "rules": [{"name": x.get("Name"), "priority": x.get("Priority"),
                "statement_sha256": sha(x.get("Statement"))} for x in ordered],
     "rules_sha256": sha(ordered),
     "digest_scope": ("statement_sha256 covers that rule's Statement only (the field the order names); "
                      "rules_sha256 covers the WHOLE ordered rule list -- every attribute, including "
                      "Action/OverrideAction and VisibilityConfig -- because the churn in the plan touched "
                      "override_action lines and a Statement-only digest could read EQUAL across a change to "
                      "how a rule acts. The before/after comparison turns on rules_sha256."),
     "bodies_printed": False,
     "read_by": "0.7.0_AE_CloudOps~Z",
    }
    out = os.path.join(W, "ZS1_ACL_%s.json" % phase.upper())
    io.open(out, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print("  wrote %s" % out)
    print("  rules: %d -> %s" % (len(ordered), ", ".join("%s/%s" % (x.get("Priority"), x.get("Name")) for x in ordered)))
    print("  rules_sha256: %s" % rec["rules_sha256"])
    if phase == "after":
        before = os.path.join(W, "ZS1_ACL_BEFORE.json")
        if not os.path.exists(before):
            raise SystemExit("REFUSED: no BEFORE snapshot to compare against")
        b = json.load(io.open(before, encoding="utf-8"))
        same = b["rules_sha256"] == rec["rules_sha256"]
        print("  BEFORE rules_sha256: %s" % b["rules_sha256"])
        print("  EQUAL: %s  (condition (ii): %s)"
              % (same, "satisfied" if same else "VIOLATED -- restore the before state and file an ARMED row"))
        moved = [x["name"] for x in rec["rules"]
                 if x["statement_sha256"] not in {y["statement_sha256"] for y in b["rules"]}]
        print("  rules whose statement digest is not in the before set: %d %s" % (len(moved), moved))
        return 0 if same else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
