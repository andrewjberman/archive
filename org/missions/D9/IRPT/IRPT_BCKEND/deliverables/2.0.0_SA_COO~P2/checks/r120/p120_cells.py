"""IRPT_BCKEND round 120 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order:
  IB120-1  IB-pr-422  the adapter role's two vendor session-read policies no longer depend on var.approved_performance_plan
                      (CTO msg 4488); Terraform PLAN ONLY, nothing applied; packet for the pair with IB-pr-421's zip.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB120-1-AC1  retained.tf: neither session data source nor session policy has a count that reads performance_plan_firm or
               var.approved_performance_plan; the variable is not assigned anywhere by this change. Base: FAIL (4 gated counts).
  IB120-1-AC2  plan census: adds are exactly the two aws_iam_role_policy session policies, 0 changes, 0 destroys; each grant
               names ONE secret ARN with no wildcard and the single action GetSecretValue; naming limb PASS. Base: FAIL.
  IB120-1-AC3  packet names Branch A, Branch B, both policy addresses and both secret ARNs. Base: FAIL (no packet).
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~283/"
TF = "infra/aws/terraform/investor-reporting/performance/retained.tf"
POLICIES = ("aws_iam_role_policy.performance_approved_session", "aws_iam_role_policy.performance_approved_inf_session")
BLOCKS = ('data "aws_secretsmanager_secret" "performance_cot_session"', 'resource "aws_iam_role_policy" "performance_approved_session"',
          'data "aws_secretsmanager_secret" "performance_inf_session"', 'resource "aws_iam_role_policy" "performance_approved_inf_session"')


def block(text, header):
    i = text.find(header)
    if i < 0:
        return None
    depth, j = 0, text.find("{", i)
    k = j
    while k < len(text):
        if text[k] == "{":
            depth += 1
        elif text[k] == "}":
            depth -= 1
            if depth == 0:
                return text[i:k + 1]
        k += 1
    return None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB120"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB120-1-AC1":
        text = (root / TF).read_text(encoding="utf-8")
        gated = 0
        for h in BLOCKS:
            b = block(text, h)
            if b is None:
                fail("block %s is gone; the policies are ungated, not renamed or removed" % h)
            for line in b.splitlines():
                if re.match(r"\s*count\s*=", line) and ("performance_plan_firm" in line or "approved_performance_plan" in line):
                    gated += 1
        if gated:
            fail("%d of 4 blocks still gate their count on the plan variable" % gated)
        print("OK: 4 of 4 session blocks present, 0 gated on the plan variable")
    elif cid == "IB120-1-AC2":
        c = load(D + "IB120-1_plan_census.json")
        adds = sorted(re.sub(r"\[\d+\]$", "", a) for a in c.get("adds") or [])
        if adds != sorted(POLICIES):
            fail("adds %r" % adds)
        if (c.get("changes") or []) or (c.get("destroys") or []):
            fail("changes %r destroys %r" % (c.get("changes"), c.get("destroys")))
        grants = c.get("grants") or []
        if len(grants) != 2:
            fail("%d grant(s)" % len(grants))
        arns = set()
        for g in grants:
            res, act = g.get("resources") or [], g.get("actions") or []
            if len(res) != 1 or "*" in res[0] or not res[0].startswith("arn:aws:secretsmanager:") or act != ["secretsmanager:GetSecretValue"]:
                fail("grant %r" % g)
            arns.add(res[0])
        if len(arns) != 2:
            fail("the two grants do not name two distinct secrets")
        if c.get("naming_limb") != "PASS" or not c.get("naming_limb_invocation"):
            fail("naming limb %r / invocation %r" % (c.get("naming_limb"), c.get("naming_limb_invocation")))
        print("OK: adds are exactly the 2 session policies; 0 changes, 0 destroys; 2 single-secret GetSecretValue grants; naming PASS")
    elif cid == "IB120-1-AC3":
        c = load(D + "IB120-1_plan_census.json")
        pp = root / (D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-422.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        need = ["Branch A", "Branch B"] + list(POLICIES) + [g["resources"][0] for g in c.get("grants") or []]
        for s in need:
            if s not in pk:
                fail("packet lacks %r" % s)
        print("OK: packet names both branches, 2 policy addresses and 2 secret ARNs")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
