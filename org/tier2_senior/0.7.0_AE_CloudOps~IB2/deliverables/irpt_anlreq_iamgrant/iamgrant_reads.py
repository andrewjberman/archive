"""IRPT_ANLREQ TO-APPLY-IAMGRANT reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python iamgrant_reads.py before    R0: the live policy document (rollback copy, sid list, canonical sha256) and the baseline simulations
  python iamgrant_reads.py after     G1/G2: the same reads after the apply, compared with the R0 copy per Sid

The policy document is captured with get_role_policy()["PolicyDocument"] only (the inner document, the shape put-role-policy replays) and refused when
it has no statements. The simulations are ONE resource per call; a positive control (a family the role already reads) runs in its own call.
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
BUCKET = "opal-data-irpt"
STATE = HERE.parent / "irpt_anlreq_commentary_e2e6" / "state_e2e6.json"
iam = boto3.client("iam", region_name="us-east-1")
lines = []


def keys():
    ks = json.loads(STATE.read_text(encoding="utf-8"))["leftover_blob_keys"]
    pick = {}
    for k in ks:
        pick.setdefault(k.split("/")[3], k)
    return pick


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


def sim(action, key):
    arn = "arn:aws:s3:::%s/%s" % (BUCKET, key)
    r = iam.simulate_principal_policy(PolicySourceArn=iam.get_role(RoleName=ROLE)["Role"]["Arn"], ActionNames=[action], ResourceArns=[arn])["EvaluationResults"][0]
    stm = ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"
    return r["EvalDecision"], stm


def sids(doc):
    return [s.get("Sid", "<no-sid>") for s in statements(doc)]


def main(mode):
    doc = fetch()
    h = hashlib.sha256(canon(doc).encode("utf-8")).hexdigest()
    ks = keys()
    com, rep, orig = ks["analysis_commentaries"], ks["ycharts_opal_reports"], ks["original_holdings"]
    def fam(k):
        return k.split("/")[3]

    out ={"sids": sids(doc), "sha256": h}
    for label, act, key in (("com_get", "s3:GetObject", com), ("com_getver", "s3:GetObjectVersion", com), ("com_put", "s3:PutObject", com),
                            ("rep_put", "s3:PutObject", rep), ("orig_get", "s3:GetObject", orig)):
        out[label] = sim(act, key)
        lines.append("SIM %s %s on %s: %s matched=%s" % (mode, act, fam(key), out[label][0], out[label][1]))
    lines.append("DOC %s statements=%d sids=%s sha256=%s" % (mode, len(statements(doc)), ",".join(out["sids"]), h))
    if mode == "before":
        (HERE / "role_policy_before.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="ascii", newline="\n")
        (HERE / "r0_state.json").write_text(json.dumps(out, indent=1) + "\n", encoding="ascii", newline="\n")
        base = out["com_get"][0] == "implicitDeny" and out["com_put"][0] == "implicitDeny" and "ReadTheAnalysisCommentaryDraft" not in out["sids"]
        lines.append("R0 baseline %s" % ("implicitDeny get and put" if base else "FAIL not the baseline"))
        lines.append("R0 controls: rep_put=%s orig_get=%s" % (out["rep_put"][0], out["orig_get"][0]))
    else:
        before = json.loads((HERE / "role_policy_before.json").read_text(encoding="ascii"))
        r0 = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
        bmap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(before)}
        amap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(doc)}
        new = [s for s in amap if s not in bmap]
        gone = [s for s in bmap if s not in amap]
        changed = [s for s in bmap if s in amap and bmap[s] != amap[s]]
        g1 = new == ["ReadTheAnalysisCommentaryDraft"] and not gone and not changed and [s for s in out["sids"] if s != "ReadTheAnalysisCommentaryDraft"] == r0["sids"]
        lines.append("G1 new=%s removed=%s changed=%s -> %s" % (new, gone, changed, "other statements byte-equal" if g1 else "FAIL"))
        new_st = [s for s in statements(doc) if s.get("Sid") == "ReadTheAnalysisCommentaryDraft"]
        if new_st:
            n = new_st[0]
            res = n.get("Resource")
            lines.append("G1 statement Effect=%s Action=%s Resource=%s" % (n.get("Effect"), n.get("Action"), res))
        g2 = out["com_get"][0] == "allowed" and out["com_put"][0] == "implicitDeny" and out["rep_put"][0] == "allowed" and out["orig_get"][0] == r0["orig_get"][0]
        lines.append("G2 get=%s put=%s getversion=%s rep_put=%s orig_get=%s (R0 orig_get=%s) -> %s" % (out["com_get"][0], out["com_put"][0], out["com_getver"][0], out["rep_put"][0], out["orig_get"][0], r0["orig_get"][0], "get allowed put implicitDeny on analysis_commentaries" if g2 else "FAIL"))
        lines.append("DOC sha256 before=%s after=%s" % (r0["sha256"], h))


if __name__ == "__main__":
    main(sys.argv[1])
    print("\n".join(lines))
    (HERE / ("reads_%s.txt" % sys.argv[1])).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
