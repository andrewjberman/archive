"""IRPT_ANLREQ TO-APPLY-AUDITPOLICY reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python auditpolicy_reads.py before                  R0: the five inline policies (names, canonical sha256), the attached list, the baseline simulations
  python auditpolicy_reads.py policy-absent <NAME>    R0: the new managed policy must NOT exist (NoSuchEntity); NAME is the one the plan renders
  python auditpolicy_reads.py after <NAME>            G1/G2: inline policies unchanged, attached list plus the new policy, its default version, the simulations

The simulation helpers are the audit-grant ones (one resource per call; the KMS simulation passes the two context entries the statement's conditions test; a
positive control runs in its own call). Nothing is written: the sample key is only a string in a simulation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("auditgrant_reads", str(HERE.parent / "irpt_anlreq_auditgrant" / "auditgrant_reads.py"))
ag = importlib.util.module_from_spec(spec)
sys.modules["auditgrant_reads"] = ag
spec.loader.exec_module(ag)
iam = boto3.client("iam", region_name="us-east-1")
ROLE = ag.ROLE
WRITE_SID = "WriteTheAnalysisAudit"
KMS_SID = "AuditEncryptionViaS3ForAuditPrefixesOnly"
lines = []


def canon(doc):
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def inline_state():
    out = {}
    for n in iam.list_role_policies(RoleName=ROLE)["PolicyNames"]:
        d = iam.get_role_policy(RoleName=ROLE, PolicyName=n)["PolicyDocument"]
        out[n] = hashlib.sha256(canon(d).encode("utf-8")).hexdigest()
    return out


def attached():
    return sorted(p["PolicyName"] for p in iam.list_attached_role_policies(RoleName=ROLE)["AttachedPolicies"])


def kms_key_arn():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName="irpt-ycharts-runner-resident-policy")["PolicyDocument"]
    st = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    return [s for s in st if s.get("Sid") == ag.KMS_SID][0]["Resource"][0]


def sims(mode):
    key_arn = kms_key_arn()
    out = {}
    for label, act, key in (("put_audit", "s3:PutObject", ag.AUDIT_KEY), ("get_audit", "s3:GetObject", ag.AUDIT_KEY), ("getver_audit", "s3:GetObjectVersion", ag.AUDIT_KEY),
                            ("del_audit", "s3:DeleteObject", ag.AUDIT_KEY), ("put_other", "s3:PutObject", ag.OTHER_FAMILY_KEY), ("put_control", "s3:PutObject", ag.CONTROL_KEY)):
        out[label] = ag.s3_sim(act, key)
        lines.append("SIM %s %s on %s: %s matched=%s" % (mode, act, label, out[label][0], out[label][1]))
    out["kms_audit"] = ag.kms_sim(key_arn, ag.AUDIT_KEY)
    lines.append("SIM %s kms:GenerateDataKey for the audit key's context (ViaService s3): %s matched=%s" % (mode, out["kms_audit"][0], out["kms_audit"][1]))
    out["kms_control"] = ag.kms_sim(key_arn, ag.CONTROL_KEY)
    lines.append("SIM %s kms:GenerateDataKey control (context under ycharts_opal_reports, its own call): %s matched=%s" % (mode, out["kms_control"][0], out["kms_control"][1]))
    return out


def before():
    st = inline_state()
    at = attached()
    sm = sims("before")
    for n, h in sorted(st.items()):
        lines.append("INLINE before %s sha256=%s" % (n, h))
    lines.append("ATTACHED before %s" % at)
    base = sm["put_audit"][0] == "implicitDeny"
    lines.append("R0 baseline %s" % ("implicitDeny put on the audit key" if base else "FAIL not the baseline: put=%s" % sm["put_audit"][0]))
    lines.append("R0 controls: s3 put on ycharts_opal_reports=%s kms audit=%s kms control=%s other family put=%s" % (sm["put_control"][0], sm["kms_audit"][0], sm["kms_control"][0], sm["put_other"][0]))
    (HERE / "r0_state.json").write_text(json.dumps({"inline": st, "attached": at, "sims": sm}, indent=1) + "\n", encoding="ascii", newline="\n")


def policy_absent(name):
    arn = "arn:aws:iam::%s:policy/%s" % (boto3.client("sts", region_name="us-east-1").get_caller_identity()["Account"], name)
    try:
        iam.get_policy(PolicyArn=arn)
        lines.append("R0 policy %s: EXISTS -> STOP" % name)
        return
    except iam.exceptions.NoSuchEntityException:
        lines.append("R0 new policy %s does not exist before the apply (NoSuchEntity) as ordered" % name)
    lines.append("R0 policy ARN would be %s" % arn)
    s = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
    s["policy_name"], s["policy_arn"] = name, arn
    (HERE / "r0_state.json").write_text(json.dumps(s, indent=1) + "\n", encoding="ascii", newline="\n")


def after(name):
    r0 = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
    arn = r0["policy_arn"]
    st = inline_state()
    at = attached()
    sm = sims("after")
    for n, h in sorted(st.items()):
        lines.append("INLINE after %s sha256=%s (R0 %s) %s" % (n, h, r0["inline"].get(n), "EQUAL" if h == r0["inline"].get(n) else "DIFFERENT"))
    inline_ok = st == r0["inline"]
    att_ok = sorted(r0["attached"] + [name]) == at
    lines.append("ATTACHED after %s (R0 %s) -> %s" % (at, r0["attached"], "R0 plus the new policy" if att_ok else "FAIL"))
    pol = iam.get_policy(PolicyArn=arn)["Policy"]
    ver = iam.get_policy_version(PolicyArn=arn, VersionId=pol["DefaultVersionId"])["PolicyVersion"]["Document"]
    stm = ver["Statement"] if isinstance(ver["Statement"], list) else [ver["Statement"]]
    sids = [s.get("Sid") for s in stm]
    w = [s for s in stm if s.get("Sid") == WRITE_SID]
    k = [s for s in stm if s.get("Sid") == KMS_SID]

    def acts(s):
        return sorted(s["Action"] if isinstance(s["Action"], list) else [s["Action"]])

    doc_ok = sids == [WRITE_SID, KMS_SID] and acts(w[0]) == ["s3:PutObject"] and acts(k[0]) == ["kms:Decrypt", "kms:GenerateDataKey"] and sorted(w[0]["Resource"]) == sorted(ag.NEW_PREFIXES)
    lines.append("POLICY default version %s: sids=%s write_actions=%s kms_actions=%s write_resources=%s -> %s" % (pol["DefaultVersionId"], sids, acts(w[0]) if w else None, acts(k[0]) if k else None, sorted(w[0]["Resource"]) if w else None, "exactly the two statements" if doc_ok else "FAIL"))
    ents = iam.list_entities_for_policy(PolicyArn=arn)
    roles = [r["RoleName"] for r in ents["PolicyRoles"]]
    only_runner = roles == [ROLE] and not ents["PolicyUsers"] and not ents["PolicyGroups"]
    lines.append("ATTACHMENT entities: roles=%s users=%d groups=%d -> %s" % (roles, len(ents["PolicyUsers"]), len(ents["PolicyGroups"]), "the runner role only" if only_runner else "FAIL"))
    g1 = inline_ok and att_ok and doc_ok and only_runner
    lines.append("G1 inline_equal=%s attached_ok=%s policy_exact=%s runner_only=%s -> %s" % (inline_ok, att_ok, doc_ok, only_runner, "inline policies unchanged" if g1 else "FAIL"))
    g2 = (sm["put_audit"][0] == "allowed" and sm["get_audit"][0] == "implicitDeny" and sm["getver_audit"][0] == "implicitDeny" and sm["del_audit"][0] == "implicitDeny"
          and sm["put_other"][0] == r0["sims"]["put_other"][0] and sm["kms_audit"][0] == "allowed")
    lines.append("G2 put=%s(%s) get=%s getversion=%s delete=%s other_family_put=%s (R0 %s) kms_audit=%s -> %s" % (
        sm["put_audit"][0], sm["put_audit"][1], sm["get_audit"][0], sm["getver_audit"][0], sm["del_audit"][0], sm["put_other"][0], r0["sims"]["put_other"][0], sm["kms_audit"][0],
        "put allowed get delete implicitDeny on the audit key" if g2 else "FAIL"))
    lines.append("VERDICT g1=%s g2=%s" % (g1, g2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "before":
        before()
    elif mode == "policy-absent":
        policy_absent(sys.argv[2])
    elif mode == "after":
        after(sys.argv[2])
    else:
        raise SystemExit("usage: before | policy-absent NAME | after NAME")
    print("\n".join(lines))
    (HERE / ("reads_%s.txt" % mode)).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
