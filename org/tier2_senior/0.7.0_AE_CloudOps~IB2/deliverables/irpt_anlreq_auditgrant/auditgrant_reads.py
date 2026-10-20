"""IRPT_ANLREQ TO-APPLY-AUDITGRANT reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python auditgrant_reads.py before    R0: the live policy document (rollback copy, Sid list, KMS context-list length, canonical sha256) and the baseline simulations
  python auditgrant_reads.py after     G1/G2: the same reads after the apply, compared with the R0 copy per Sid

The policy document is captured with get_role_policy()["PolicyDocument"] only (the inner document, the shape put-role-policy replays) and refused when it has
no statements. Every simulation is ONE resource per call. The KMS simulation passes the two context entries the statement's conditions test; its positive
control (a key under a family the role already encrypts for) runs in its own call. Nothing is written: a sample key is only a string in a simulation.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
ROLE = "irpt-ycharts-runner-role"
POLICY = "irpt-ycharts-runner-resident-policy"
NEW_SID = "WriteTheAnalysisAudit"
KMS_SID = "ReportEncryptionViaS3ForResidentFamiliesOnly"
BUCKET = "opal-data-irpt"
FIRMS = ("49financial", "cottonwood", "inflection")
HEX_A = hashlib.sha256(b"auditgrant-simulation-art").hexdigest()
HEX_B = hashlib.sha256(b"auditgrant-simulation-object").hexdigest()
AUDIT_KEY = "irpt/49financial/platinum/analysis_audit/ART-%s/%s.json" % (HEX_A, HEX_B)
OTHER_FAMILY_KEY = "irpt/49financial/platinum/some_other_family/ART-%s/%s.json" % (HEX_A, HEX_B)
CONTROL_KEY = "irpt/49financial/state/ycharts_opal_reports/control-key.pdf"  # a family the role already writes and encrypts for
NEW_PREFIXES = ["arn:aws:s3:::%s/irpt/%s/platinum/analysis_audit/*" % (BUCKET, f) for f in FIRMS]
iam = boto3.client("iam", region_name="us-east-1")
lines = []


def canon(doc):
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def statements(doc):
    st = doc["Statement"]
    return st if isinstance(st, list) else [st]


def fetch():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    if not isinstance(doc, dict) or "Statement" not in doc or not statements(doc):
        raise SystemExit("STOP: the policy read has no Statement (wrong shape or empty)")
    return doc


def sids(doc):
    return [s.get("Sid", "<no-sid>") for s in statements(doc)]


def kms_statement(doc):
    st = [s for s in statements(doc) if s.get("Sid") == KMS_SID]
    return st[0] if len(st) == 1 else None


def kms_list(doc):
    st = kms_statement(doc)
    v = ((st or {}).get("Condition") or {}).get("StringLike", {}).get("kms:EncryptionContext:aws:s3:arn")
    return v if isinstance(v, list) else ([v] if v else [])


def kms_rest(st):
    """The KMS statement with its s3-arn context list removed: what must stay byte-equal across the apply."""
    out = {}
    for k, v in st.items():
        if k == "Condition":
            v = {c: {kk: vv for kk, vv in cv.items() if kk != "kms:EncryptionContext:aws:s3:arn"} for c, cv in v.items()}
        out[k] = v
    return canon(out)


def s3_sim(action, key):
    arn = "arn:aws:s3:::%s/%s" % (BUCKET, key)
    r = iam.simulate_principal_policy(PolicySourceArn=iam.get_role(RoleName=ROLE)["Role"]["Arn"], ActionNames=[action], ResourceArns=[arn])["EvaluationResults"][0]
    return r["EvalDecision"], ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"


def kms_sim(key_arn, key):
    ctx = [{"ContextKeyName": "kms:EncryptionContext:aws:s3:arn", "ContextKeyValues": ["arn:aws:s3:::%s/%s" % (BUCKET, key)], "ContextKeyType": "string"},
           {"ContextKeyName": "kms:ViaService", "ContextKeyValues": ["s3.us-east-1.amazonaws.com"], "ContextKeyType": "string"}]
    r = iam.simulate_principal_policy(PolicySourceArn=iam.get_role(RoleName=ROLE)["Role"]["Arn"], ActionNames=["kms:GenerateDataKey"], ResourceArns=[key_arn], ContextEntries=ctx)["EvaluationResults"][0]
    return r["EvalDecision"], ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"


def main(mode):
    doc = fetch()
    h = hashlib.sha256(canon(doc).encode("utf-8")).hexdigest()
    kl = kms_list(doc)
    ks = kms_statement(doc)
    key_arn = ks["Resource"][0] if ks else None
    out = {"sids": sids(doc), "sha256": h, "kms_list_len": len(kl), "kms_key_arn_present": bool(key_arn)}
    for label, act, key in (("put_audit", "s3:PutObject", AUDIT_KEY), ("get_audit", "s3:GetObject", AUDIT_KEY), ("getver_audit", "s3:GetObjectVersion", AUDIT_KEY),
                            ("del_audit", "s3:DeleteObject", AUDIT_KEY), ("put_other", "s3:PutObject", OTHER_FAMILY_KEY), ("put_control", "s3:PutObject", CONTROL_KEY)):
        out[label] = s3_sim(act, key)
        lines.append("SIM %s %s on %s: %s matched=%s" % (mode, act, key.split("/")[3] + "/" + key.split("/")[4] if "analysis_audit" in key or "some_other" in key else key.split("/")[3], out[label][0], out[label][1]))
    out["kms_audit"] = kms_sim(key_arn, AUDIT_KEY)
    lines.append("SIM %s kms:GenerateDataKey on the system key, context s3 arn under analysis_audit and ViaService s3: %s matched=%s" % (mode, out["kms_audit"][0], out["kms_audit"][1]))
    out["kms_control"] = kms_sim(key_arn, CONTROL_KEY)
    lines.append("SIM %s kms:GenerateDataKey control (context under ycharts_opal_reports, its own call): %s matched=%s" % (mode, out["kms_control"][0], out["kms_control"][1]))
    lines.append("DOC %s statements=%d sids=%s sha256=%s kms_context_list_len=%d" % (mode, len(statements(doc)), ",".join(out["sids"]), h, len(kl)))
    if mode == "before":
        (HERE / "role_policy_before.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="ascii", newline="\n")
        out["kms_list"] = kl
        (HERE / "r0_state.json").write_text(json.dumps(out, indent=1) + "\n", encoding="ascii", newline="\n")
        base = out["put_audit"][0] == "implicitDeny" and NEW_SID not in out["sids"] and not any("analysis_audit" in x for x in kl)
        lines.append("R0 baseline %s" % ("implicitDeny put on the audit key" if base else "FAIL not the baseline: put=%s sid_present=%s kms_audit_entries=%s" % (out["put_audit"][0], NEW_SID in out["sids"], any("analysis_audit" in x for x in kl))))
        lines.append("R0 controls: s3 put on ycharts_opal_reports=%s kms control=%s kms on the audit key=%s other family put=%s" % (out["put_control"][0], out["kms_control"][0], out["kms_audit"][0], out["put_other"][0]))
    else:
        before = json.loads((HERE / "role_policy_before.json").read_text(encoding="ascii"))
        r0 = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
        bmap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(before)}
        amap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(doc)}
        new = [s for s in amap if s not in bmap]
        gone = [s for s in bmap if s not in amap]
        changed = [s for s in bmap if s in amap and bmap[s] != amap[s]]
        sid_ok = new == [NEW_SID] and not gone and [s for s in out["sids"] if s != NEW_SID] == r0["sids"]
        # the new statement's exact shape
        shape_ok = False
        new_st = [s for s in statements(doc) if s.get("Sid") == NEW_SID]
        if new_st:
            n = new_st[0]
            res = n.get("Resource")
            res = res if isinstance(res, list) else [res]
            act = n.get("Action")
            act = act if isinstance(act, list) else [act]
            shape_ok = n.get("Effect") == "Allow" and act == ["s3:PutObject"] and sorted(res) == sorted(NEW_PREFIXES) and "Condition" not in n
            lines.append("G1 new statement Effect=%s Action=%s Resource=%s Condition=%s -> %s" % (n.get("Effect"), act, res, n.get("Condition"), "exact shape" if shape_ok else "FAIL"))
        # the KMS statement differs only by its condition list gaining exactly the three prefixes
        sa, sb = kms_statement(doc), kms_statement(before)
        kms_rest_equal = kms_rest(sa) == kms_rest(sb)
        added = [x for x in kms_list(doc) if x not in kms_list(before)]
        removed = [x for x in kms_list(before) if x not in kms_list(doc)]
        kms_ok = kms_rest_equal and sorted(added) == sorted(NEW_PREFIXES) and not removed and len(kms_list(doc)) == len(kms_list(before)) + 3
        lines.append("G1 KMS statement: rest_equal=%s list %d -> %d added=%s removed=%s -> %s" % (kms_rest_equal, len(kms_list(before)), len(kms_list(doc)), added, removed, "gains exactly the three prefixes" if kms_ok else "FAIL"))
        others_equal = all(bmap[s] == amap[s] for s in bmap if s in amap and s != KMS_SID)
        g1 = sid_ok and shape_ok and kms_ok and others_equal and changed == [KMS_SID]
        lines.append("G1 sid_ok=%s changed=%s other_statements_byte_equal=%s -> %s" % (sid_ok, changed, others_equal, "other statements byte-equal" if g1 else "FAIL"))
        g2 = (out["put_audit"][0] == "allowed" and out["get_audit"][0] == "implicitDeny" and out["getver_audit"][0] == "implicitDeny" and out["del_audit"][0] == "implicitDeny"
              and out["put_other"][0] == r0["put_other"][0] and out["put_control"][0] == r0["put_control"][0] and out["kms_audit"][0] == "allowed")
        lines.append("G2 put=%s(%s) get=%s getversion=%s delete=%s other_family_put=%s (R0 %s) control_put=%s kms_audit=%s(%s) kms_control=%s -> %s" % (
            out["put_audit"][0], out["put_audit"][1], out["get_audit"][0], out["getver_audit"][0], out["del_audit"][0], out["put_other"][0], r0["put_other"][0], out["put_control"][0],
            out["kms_audit"][0], out["kms_audit"][1], out["kms_control"][0], "put allowed get delete implicitDeny on the audit key" if g2 else "FAIL"))
        lines.append("DOC sha256 before=%s after=%s kms_list_len before=%d after=%d" % (r0["sha256"], h, r0["kms_list_len"], len(kl)))
        lines.append("VERDICT g1=%s g2=%s" % (g1, g2))


if __name__ == "__main__":
    main(sys.argv[1])
    print("\n".join(lines))
    (HERE / ("reads_%s.txt" % sys.argv[1])).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
