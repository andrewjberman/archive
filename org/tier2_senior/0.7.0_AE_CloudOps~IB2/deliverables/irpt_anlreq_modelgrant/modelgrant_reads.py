"""IRPT_ANLREQ TO-APPLY-MODELGRANT reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python modelgrant_reads.py before    R0: the live policy document (rollback copy, sid list, canonical sha256) and the baseline simulations
  python modelgrant_reads.py after     G1/G2: the same reads after the apply, compared with the R0 copy per Sid
  python modelgrant_reads.py host      the host-side G4 probe is NOT here (it runs on the host through SSM, see host_g4.sh)

The policy document is captured with get_role_policy()["PolicyDocument"] only (the inner document, the shape put-role-policy replays) and refused when
it has no statements. The simulations are ONE resource per call; a positive control (a family the role already writes) runs in its own call.
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
NEW_SID = "ReadTheModelReturnSeriesAndPositioning"
BUCKET = "opal-data-portal-v2"
K1 = "json/benchmarks/model_portfolio_timeseries.json"
K2 = "json/positioning/positioning_data.json"
K3 = "json/benchmarks/other.json"
CONTROL = ("opal-data-irpt", "irpt/49financial/state/ycharts_opal_reports/control-key.pdf")  # a family the role already writes (run 7's R0 read allowed)
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


def sim(action, key, bucket=BUCKET):
    arn = "arn:aws:s3:::%s/%s" % (bucket, key)
    r = iam.simulate_principal_policy(PolicySourceArn=iam.get_role(RoleName=ROLE)["Role"]["Arn"], ActionNames=[action], ResourceArns=[arn])["EvaluationResults"][0]
    stm = ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"
    return r["EvalDecision"], stm


def sids(doc):
    return [s.get("Sid", "<no-sid>") for s in statements(doc)]


def main(mode):
    doc = fetch()
    h = hashlib.sha256(canon(doc).encode("utf-8")).hexdigest()
    out = {"sids": sids(doc), "sha256": h}
    for label, act, key in (("k1_get", "s3:GetObject", K1), ("k2_get", "s3:GetObject", K2), ("k3_get", "s3:GetObject", K3), ("k1_put", "s3:PutObject", K1),
                            ("k1_del", "s3:DeleteObject", K1), ("k2_put", "s3:PutObject", K2), ("k1_getver", "s3:GetObjectVersion", K1)):
        out[label] = sim(act, key)
        lines.append("SIM %s %s on %s: %s matched=%s" % (mode, act, key, out[label][0], out[label][1]))
    out["control_put"] = sim("s3:PutObject", CONTROL[1], CONTROL[0])
    lines.append("SIM %s control s3:PutObject on a ycharts_opal_reports key of opal-data-irpt (a grant the role already holds): %s matched=%s" % (mode, out["control_put"][0], out["control_put"][1]))
    lines.append("DOC %s statements=%d sids=%s sha256=%s" % (mode, len(statements(doc)), ",".join(out["sids"]), h))
    if mode == "before":
        (HERE / "role_policy_before.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="ascii", newline="\n")
        (HERE / "r0_state.json").write_text(json.dumps(out, indent=1) + "\n", encoding="ascii", newline="\n")
        four = [out["k1_get"][0], out["k2_get"][0], out["k3_get"][0], out["k1_put"][0]]
        base = all(x == "implicitDeny" for x in four) and NEW_SID not in out["sids"]
        lines.append("R0 baseline %s" % ("implicitDeny on all four" if base else "FAIL not the baseline: %s sid_present=%s" % (four, NEW_SID in out["sids"])))
        lines.append("R0 control: simulator can say allowed (control put) = %s" % (out["control_put"][0] == "allowed"))
    else:
        before = json.loads((HERE / "role_policy_before.json").read_text(encoding="ascii"))
        r0 = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
        bmap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(before)}
        amap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(doc)}
        new = [s for s in amap if s not in bmap]
        gone = [s for s in bmap if s not in amap]
        changed = [s for s in bmap if s in amap and bmap[s] != amap[s]]
        g1 = new == [NEW_SID] and not gone and not changed and [s for s in out["sids"] if s != NEW_SID] == r0["sids"]
        lines.append("G1 new=%s removed=%s changed=%s -> %s" % (new, gone, changed, "other statements byte-equal" if g1 else "FAIL"))
        new_st = [s for s in statements(doc) if s.get("Sid") == NEW_SID]
        shape_ok = False
        if new_st:
            n = new_st[0]
            res = n.get("Resource")
            res = res if isinstance(res, list) else [res]
            act = n.get("Action")
            act = act if isinstance(act, list) else [act]
            shape_ok = n.get("Effect") == "Allow" and act == ["s3:GetObject"] and sorted(res) == sorted(["arn:aws:s3:::%s/%s" % (BUCKET, K1), "arn:aws:s3:::%s/%s" % (BUCKET, K2)]) and "Condition" not in n
            lines.append("G1 statement Effect=%s Action=%s Resource=%s Condition=%s -> %s" % (n.get("Effect"), act, res, n.get("Condition"), "exact shape" if shape_ok else "FAIL"))
        g2 = (out["k1_get"][0] == "allowed" and out["k2_get"][0] == "allowed" and out["k1_put"][0] == "implicitDeny" and out["k3_get"][0] == "implicitDeny"
              and out["k1_del"][0] == "implicitDeny" and out["k2_put"][0] == "implicitDeny" and out["k1_getver"][0] == "implicitDeny")
        lines.append("G2 k1_get=%s(%s) k2_get=%s(%s) k1_put=%s k2_put=%s k1_delete=%s k1_getversion=%s k3_get=%s -> %s" % (
            out["k1_get"][0], out["k1_get"][1], out["k2_get"][0], out["k2_get"][1], out["k1_put"][0], out["k2_put"][0], out["k1_del"][0], out["k1_getver"][0], out["k3_get"][0],
            "get allowed on two keys put and third key implicitDeny" if g2 else "FAIL"))
        lines.append("DOC sha256 before=%s after=%s" % (r0["sha256"], h))
        lines.append("VERDICT g1=%s shape=%s g2=%s" % (g1, shape_ok, g2))


if __name__ == "__main__":
    main(sys.argv[1])
    print("\n".join(lines))
    (HERE / ("reads_%s.txt" % sys.argv[1])).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
