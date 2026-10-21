"""IRPT_ANLREQ TO-APPLY-TICKETREAD reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY, nothing is written or read from the table.

  python ticketread_reads.py before                 R0: five inline policies (names, canonical sha256), attached list, the five baseline arms on the role
  python ticketread_reads.py policy-absent NAME     R0: the new managed policy must NOT exist (NoSuchEntity)
  python ticketread_reads.py custom PLAN_JSON       S: the five arms on the plan's rendered policy document (simulate-custom-policy, before apply)
  python ticketread_reads.py after NAME             V: inline policies unchanged, attached list, the policy document, the five arms on the role

One resource per call; the context entries (dynamodb:Attributes as stringList, dynamodb:Select as string) only where the arm names them.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
ACCOUNT = "313476888478"
ROLE = "irpt-ycharts-runner-role"
ROLE_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, ROLE)
TICKETS = "arn:aws:dynamodb:%s:%s:table/opal-tickets" % (REGION, ACCOUNT)
USERS = "arn:aws:dynamodb:%s:%s:table/opal-users-v2" % (REGION, ACCOUNT)
INDEX = TICKETS + "/index/status-index"
OK_ATTRS = ["ticket_id", "ticket_type", "answers", "created_at"]
iam = boto3.client("iam", region_name=REGION)
lines = []


def ctx(attrs=None, select=None):
    out = []
    if attrs is not None:
        out.append({"ContextKeyName": "dynamodb:Attributes", "ContextKeyValues": list(attrs), "ContextKeyType": "stringList"})
    if select is not None:
        out.append({"ContextKeyName": "dynamodb:Select", "ContextKeyValues": [select], "ContextKeyType": "string"})
    return out


# (label, action, resource, attributes, select, expectation)
ARMS = [
    ("S1", "dynamodb:GetItem", TICKETS, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "allowed"),
    ("S2", "dynamodb:GetItem", TICKETS, None, None, "implicitDeny"),
    ("S3a", "dynamodb:GetItem", TICKETS, ["ticket_id", "requester"], None, "implicitDeny"),
    ("S3b", "dynamodb:GetItem", TICKETS, ["ticket_id", "created_by"], None, "implicitDeny"),
    ("S4a", "dynamodb:Query", TICKETS, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "implicitDeny"),
    ("S4b", "dynamodb:Scan", TICKETS, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "implicitDeny"),
    ("S4c", "dynamodb:BatchGetItem", TICKETS, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "implicitDeny"),
    ("S4d", "dynamodb:PutItem", TICKETS, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "implicitDeny"),
    ("S5a", "dynamodb:GetItem", USERS, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "implicitDeny"),
    ("S5b", "dynamodb:GetItem", INDEX, OK_ATTRS, "SPECIFIC_ATTRIBUTES", "implicitDeny"),
]


def sim_role(action, resource, attrs, select):
    r = iam.simulate_principal_policy(PolicySourceArn=ROLE_ARN, ActionNames=[action], ResourceArns=[resource], ContextEntries=ctx(attrs, select))["EvaluationResults"][0]
    matched = ",".join(sorted({m.get("SourcePolicyId", "?") for m in r.get("MatchedStatements", [])})) or "-"
    return r["EvalDecision"], matched


def sim_custom(doc_text, action, resource, attrs, select):
    r = iam.simulate_custom_policy(PolicyInputList=[doc_text], ActionNames=[action], ResourceArns=[resource], ContextEntries=ctx(attrs, select))["EvaluationResults"][0]
    matched = ",".join(sorted({m.get("SourcePolicyId", "?") for m in r.get("MatchedStatements", [])})) or "-"
    return r["EvalDecision"], matched


def canon(doc):
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def inline_state():
    out = {}
    for n in iam.list_role_policies(RoleName=ROLE)["PolicyNames"]:
        out[n] = hashlib.sha256(canon(iam.get_role_policy(RoleName=ROLE, PolicyName=n)["PolicyDocument"]).encode("utf-8")).hexdigest()
    return out


def attached():
    return sorted(p["PolicyName"] for p in iam.list_attached_role_policies(RoleName=ROLE)["AttachedPolicies"])


def arms_on(fn, tag):
    """Run the ten arm calls; returns {label: (decision, matched)} and prints each beside its expectation."""
    out = {}
    for label, action, res, attrs, sel, want in ARMS:
        d, m = fn(action, res, attrs, sel)
        out[label] = (d, m)
        short = res.split(":table/")[1]
        lines.append("ARM %s %s %s %s attrs=%s select=%s -> %s matched=%s (expect %s)" % (tag, label, action, short, "none" if attrs is None else ",".join(attrs), sel or "none", d, m, want))
    return out


def before():
    st, at = inline_state(), attached()
    arms = arms_on(sim_role, "role-before")
    for n, h in sorted(st.items()):
        lines.append("INLINE before %s sha256=%s" % (n, h))
    lines.append("ATTACHED before %s" % at)
    s1 = arms["S1"][0]
    lines.append("R0 baseline %s" % ("implicitDeny on the ticket read" if s1 == "implicitDeny" else "FAIL S1 reads %s" % s1))
    (HERE / "r0_state.json").write_text(json.dumps({"inline": st, "attached": at, "arms": arms}, indent=1) + "\n", encoding="ascii", newline="\n")


def policy_absent(name):
    arn = "arn:aws:iam::%s:policy/%s" % (ACCOUNT, name)
    try:
        iam.get_policy(PolicyArn=arn)
        lines.append("R0 policy %s: EXISTS -> STOP" % name)
        return
    except iam.exceptions.NoSuchEntityException:
        lines.append("R0 new policy %s does not exist before the apply (NoSuchEntity) as ordered" % name)
    s = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
    s["policy_name"], s["policy_arn"] = name, arn
    (HERE / "r0_state.json").write_text(json.dumps(s, indent=1) + "\n", encoding="ascii", newline="\n")


def custom(plan_json):
    plan = json.loads(Path(plan_json).read_text(encoding="utf-8"))
    pol = [r for r in plan["resource_changes"] if r["address"] == "aws_iam_policy.resident_ticket_read"][0]["change"]["after"]["policy"]
    arms = arms_on(lambda a, r, at, se: sim_custom(pol, a, r, at, se), "custom-before-apply")
    bad = [k for k, (d, _) in arms.items() if d != [x for x in ARMS if x[0] == k][0][5]]
    lines.append("S arms %s" % ("held before apply" if not bad else "FAIL differ: %s" % ",".join(bad)))
    (HERE / "s_custom_state.json").write_text(json.dumps({"arms": arms, "differ": bad}, indent=1) + "\n", encoding="ascii", newline="\n")


def after(name):
    r0 = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
    arn = r0["policy_arn"]
    st, at = inline_state(), attached()
    arms = arms_on(sim_role, "role-after")
    for n, h in sorted(st.items()):
        lines.append("INLINE after %s sha256=%s (R0 %s) %s" % (n, h, r0["inline"].get(n), "EQUAL" if h == r0["inline"].get(n) else "DIFFERENT"))
    inline_ok = st == r0["inline"]
    att_ok = sorted(r0["attached"] + [name]) == at
    lines.append("ATTACHED after %s (R0 %s) -> %s" % (at, r0["attached"], "R0 plus the new policy" if att_ok else "FAIL"))
    pol = iam.get_policy(PolicyArn=arn)["Policy"]
    ver = iam.get_policy_version(PolicyArn=arn, VersionId=pol["DefaultVersionId"])["PolicyVersion"]["Document"]
    stm = ver["Statement"] if isinstance(ver["Statement"], list) else [ver["Statement"]]
    one = len(stm) == 1 and stm[0].get("Sid") == "ReadTheFiledTicketForTheAuditOnly"
    lines.append("POLICY default version %s: statements=%d sids=%s -> %s" % (pol["DefaultVersionId"], len(stm), [s.get("Sid") for s in stm], "exactly the one statement" if one else "FAIL"))
    ents = iam.list_entities_for_policy(PolicyArn=arn)
    roles = [r["RoleName"] for r in ents["PolicyRoles"]]
    only = roles == [ROLE] and not ents["PolicyUsers"] and not ents["PolicyGroups"]
    lines.append("ATTACHMENT entities: roles=%s users=%d groups=%d -> %s" % (roles, len(ents["PolicyUsers"]), len(ents["PolicyGroups"]), "the runner role only" if only else "FAIL"))
    g1 = inline_ok and att_ok and one and only
    lines.append("G1 inline_equal=%s attached_ok=%s one_statement=%s runner_only=%s -> %s" % (inline_ok, att_ok, one, only, "inline policies unchanged" if g1 else "FAIL"))
    bad = []
    for label, action, res, attrs, sel, want in ARMS:
        d, m = arms[label]
        if label == "S5a":
            ok = d == r0["arms"]["S5a"][0] and name not in m
        elif label == "S1":
            ok = d == "allowed" and m == name
        else:
            ok = d == want
        if not ok:
            bad.append(label)
    lines.append("G2 arms %s" % ("held on the role" if not bad else "FAIL differ: %s" % ",".join(bad)))
    lines.append("VERDICT g1=%s g2=%s" % (g1, not bad))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "before":
        before()
    elif mode == "policy-absent":
        policy_absent(sys.argv[2])
    elif mode == "custom":
        custom(sys.argv[2])
    elif mode == "after":
        after(sys.argv[2])
    else:
        raise SystemExit("usage: before | policy-absent NAME | custom PLAN_JSON | after NAME")
    print("\n".join(lines))
    (HERE / ("reads_%s.txt" % mode)).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
