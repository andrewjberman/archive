"""IRPT_ANLREQ TO-APPLY-STATUSGRANT reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python statusgrant_reads.py before    R0: the live policy document (rollback copy, Sid list, retained-families resources, canonical sha256) and the baseline simulations
  python statusgrant_reads.py after     G1/G2: the same reads after the apply, compared with the R0 copy per Sid

The policy document is captured with get_role_policy()["PolicyDocument"] only (the inner document, the shape put-role-policy replays) and refused when
it has no statements. The simulations are ONE resource per call; the unchanged control (original_holdings of the same firm) runs in its own call.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
ROLE = "irpt-status-role"
POLICY = "irpt-status-policy"
FAMILIES_SID = "ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly"
BUCKET = "opal-data-irpt"
PDF_KEY = "irpt/49financial/state/ycharts_opal_reports/ART-ed570a0dcc2f3f1f30420dc349789710e0425dd950c12b929a3964737b3870f9/c396092e57eaaecd4bcf0fba68a5ae3b93eb9239383fb19dbff3c7ea7e642b38.pdf"
ORIG_KEY = "irpt/49financial/state/original_holdings/ART-fe93d2291df0822809a1cf29ea26de9a0373c4b5407b0220b6505b2ae8928add/723cdf9cd7006bcb27121ef1f3b78d27ba062605c44f973d53474a7e4a414ca1.csv"
FIRMS = ("49financial", "cottonwood", "inflection")
NEW_RES = ["arn:aws:s3:::%s/irpt/%s/state/ycharts_opal_reports/*" % (BUCKET, f) for f in FIRMS]
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


def sim(action, key):
    arn = "arn:aws:s3:::%s/%s" % (BUCKET, key)
    r = iam.simulate_principal_policy(PolicySourceArn=iam.get_role(RoleName=ROLE)["Role"]["Arn"], ActionNames=[action], ResourceArns=[arn])["EvaluationResults"][0]
    stm = ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"
    return r["EvalDecision"], stm


def sids(doc):
    return [s.get("Sid", "<no-sid>") for s in statements(doc)]


def fam_resources(doc):
    st = [s for s in statements(doc) if s.get("Sid") == FAMILIES_SID]
    if len(st) != 1:
        return None
    res = st[0].get("Resource")
    return res if isinstance(res, list) else [res]


def main(mode):
    doc = fetch()
    h = hashlib.sha256(canon(doc).encode("utf-8")).hexdigest()
    fr = fam_resources(doc)
    out = {"sids": sids(doc), "sha256": h, "families_resource_count": None if fr is None else len(fr)}
    for label, act, key in (("pdf_get", "s3:GetObject", PDF_KEY), ("pdf_getver", "s3:GetObjectVersion", PDF_KEY), ("pdf_put", "s3:PutObject", PDF_KEY),
                            ("orig_get", "s3:GetObject", ORIG_KEY), ("pdf_del", "s3:DeleteObject", PDF_KEY)):
        out[label] = sim(act, key)
        lines.append("SIM %s %s on %s: %s matched=%s" % (mode, act, key.split("/")[3], out[label][0], out[label][1]))
    lines.append("DOC %s statements=%d sids=%s sha256=%s families_resources=%s" % (mode, len(statements(doc)), ",".join(out["sids"]), h, out["families_resource_count"]))
    if mode == "before":
        (HERE / "role_policy_before.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="ascii", newline="\n")
        out["families_resources"] = fr
        (HERE / "r0_state.json").write_text(json.dumps(out, indent=1) + "\n", encoding="ascii", newline="\n")
        present = fr is not None and any("ycharts_opal_reports" in x for x in fr)
        base = out["pdf_get"][0] == "implicitDeny" and out["pdf_getver"][0] == "implicitDeny" and not present
        lines.append("R0 baseline %s" % ("implicitDeny get and getversion" if base else "FAIL not the baseline: get=%s getversion=%s family_present=%s" % (out["pdf_get"][0], out["pdf_getver"][0], present)))
        lines.append("R0 families statement resources=%s (18 expected) sid_present=%s" % (out["families_resource_count"], fr is not None))
        lines.append("R0 control: original_holdings GetObject = %s" % out["orig_get"][0])
    else:
        before = json.loads((HERE / "role_policy_before.json").read_text(encoding="ascii"))
        r0 = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
        bmap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(before)}
        amap = {s.get("Sid", "<no-sid>"): canon(s) for s in statements(doc)}
        new = [s for s in amap if s not in bmap]
        gone = [s for s in bmap if s not in amap]
        changed = [s for s in bmap if s in amap and bmap[s] != amap[s]]
        sid_equal = out["sids"] == r0["sids"]
        only_fam_changed = changed == [FAMILIES_SID]
        a_res, b_res = fr, r0["families_resources"]
        res_ok = a_res is not None and sorted(a_res) == sorted(list(b_res) + NEW_RES) and len(a_res) == len(b_res) + 3
        # the family statement, apart from its Resource, is byte-equal
        sa = [s for s in statements(doc) if s.get("Sid") == FAMILIES_SID][0]
        sb = [s for s in statements(before) if s.get("Sid") == FAMILIES_SID][0]
        rest_equal = canon({k: v for k, v in sa.items() if k != "Resource"}) == canon({k: v for k, v in sb.items() if k != "Resource"})
        g1 = sid_equal and not new and not gone and only_fam_changed and res_ok and rest_equal
        lines.append("G1 sid_list_equal=%s new=%s removed=%s changed=%s families_resources %s -> %s (plus exactly %s) rest_of_statement_equal=%s -> %s" % (
            sid_equal, new, gone, changed, len(b_res), len(a_res or []), NEW_RES, rest_equal, "other statements byte-equal" if g1 else "FAIL"))
        g2 = (out["pdf_get"][0] == "allowed" and out["pdf_getver"][0] == "allowed" and out["pdf_put"][0] == "implicitDeny" and out["pdf_del"][0] == "implicitDeny"
              and out["orig_get"][0] == r0["orig_get"][0])
        lines.append("G2 get=%s(%s) getversion=%s(%s) put=%s delete=%s original_holdings_get=%s (R0 %s) -> %s" % (
            out["pdf_get"][0], out["pdf_get"][1], out["pdf_getver"][0], out["pdf_getver"][1], out["pdf_put"][0], out["pdf_del"][0], out["orig_get"][0], r0["orig_get"][0],
            "get and getversion allowed put implicitDeny on ycharts_opal_reports" if g2 else "FAIL"))
        lines.append("DOC sha256 before=%s after=%s" % (r0["sha256"], h))
        lines.append("VERDICT g1=%s g2=%s" % (g1, g2))


if __name__ == "__main__":
    main(sys.argv[1])
    print("\n".join(lines))
    (HERE / ("reads_%s.txt" % sys.argv[1])).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
