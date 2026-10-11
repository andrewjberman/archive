"""ADVI_FIRMBKTS round 4: the CLOSE SIMULATION of act 3b (the CTO's act 3b CTO half), issuer 2.0.0_SA_COO~B1.

Run by the laptop lane (0.7.0_AE_CloudOps~FBL): this identity must be allowed iam:SimulatePrincipalPolicy for roles, which the
dell1 agent identity is not. READ-ONLY: s3api get-bucket-policy, iam simulate-principal-policy. Nothing is written.

For each principal it calls simulate-principal-policy with the LIVE bucket policy passed as the resource policy, for
s3:GetObject on the object ARN it was granted, and prints its EvalDecision:
  - ADMITTED (9): the nine role principals of the permitted set, on the ownership key; the performance adapter also on one
    object under its holdings gold prefix (a read it already had: it must stay allowed);
  - NEGATIVE (2): inf-gold-qa-runner-ec2-role and exec-summary-generator-role on the ownership key: any decision other than
    `allowed` passes (implicitDeny or explicitDeny).
The OAI has no role to simulate; its Allow is read from the policy document (nine served-class prefixes, Get only, no List).

  python r4_sim.py [--bucket B] [--out FILE]
Last line: ROUND 4 ACT 3B SIM: <a> of 9 admitted allowed, <d> of 2 negatives not allowed, oai statement ok=<bool>
Exit 0 only when 9, 2 and True. Plain ASCII. Reports principals and decisions only, never object contents.
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ACCOUNT = "313476888478"
# the CLI may be aws, aws.cmd or a shim (Windows): resolve it with PATHEXT, allow an override
AWS = os.environ.get("AWS_CLI") or shutil.which("aws") or shutil.which("aws.cmd") or "aws"
KEY = "advi/49financial/platinum/49financial/ownership_map.json"
GOLD_SAMPLE = "irpt/49financial/gold/holdings_performance_daily/date=2026-01-01/part-0.parquet"
ADMITTED = ["lambda-edge-execution-role", "irpt-directory-role", "irpt-export-render-role", "irpt-narrative-role",
            "irpt-status-role", "irpt-ycharts-generate-role", "irpt-holdings-role", "irpt-49f-reporting-read-role",
            "irpt-performance-adapter-role"]
NEGATIVE = ["inf-gold-qa-runner-ec2-role", "exec-summary-generator-role"]
OAI = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD"


def aws(*a):
    r = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True, timeout=120)
    if r.returncode:
        return None, (r.stderr.strip().splitlines() or ["failed"])[-1][:200]
    return json.loads(r.stdout or "{}"), ""


def decide(policy_file, role, key, bucket):
    arn = "arn:aws:iam::%s:role/%s" % (ACCOUNT, role)
    d, err = aws("iam", "simulate-principal-policy", "--policy-source-arn", arn, "--action-names", "s3:GetObject",
                 "--resource-arns", "arn:aws:s3:::%s/%s" % (bucket, key), "--resource-policy",
                 "file://" + pathlib.Path(policy_file).as_posix())
    if d is None:
        return "ERROR", err
    rs = d.get("EvaluationResults", [])
    return (rs[0].get("EvalDecision", "?") if rs else "NO-RESULT"), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", default="opal-data-49financial")
    ap.add_argument("--out")
    a = ap.parse_args()
    d, err = aws("s3api", "get-bucket-policy", "--bucket", a.bucket)
    if d is None:
        print("ERROR: get-bucket-policy: %s" % err)
        print("ROUND 4 ACT 3B SIM: 0 of 9 admitted allowed, 0 of 2 negatives not allowed, oai statement ok=False")
        return 1
    policy_text = d["Policy"]
    stm = json.loads(policy_text)["Statement"]
    # the policy travels as a FILE: a 20 KB inline argument exceeds the Windows command-line limit
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    tmp.write(policy_text)
    tmp.close()
    policy_text = tmp.name
    lines, allowed, denied = [], 0, 0
    for r in ADMITTED:
        dec, e = decide(policy_text, r, KEY, a.bucket)
        ok = dec == "allowed"
        allowed += ok
        extra = ""
        if r == "irpt-performance-adapter-role":
            dec2, _ = decide(policy_text, r, GOLD_SAMPLE, a.bucket)
            extra = " ; holdings gold sample: %s" % dec2
            allowed -= ok and dec2 != "allowed"
        lines.append("ADMITTED %-34s ownership key: %s%s%s" % (r, dec, extra, (" (%s)" % e) if e else ""))
    for r in NEGATIVE:
        dec, e = decide(policy_text, r, KEY, a.bucket)
        ok = dec in ("implicitDeny", "explicitDeny")
        denied += ok
        lines.append("NEGATIVE %-34s ownership key: %s%s" % (r, dec, (" (%s)" % e) if e else ""))
    def _aws_principal(s):
        p = s.get("Principal")
        return p.get("AWS") if isinstance(p, dict) else p

    oai = [s for s in stm if _aws_principal(s) in (OAI, [OAI]) and s.get("Effect") == "Allow"]
    oai_ok = False
    if len(oai) == 1:
        acts = oai[0].get("Action")
        acts = acts if isinstance(acts, list) else [acts]
        ress = oai[0].get("Resource")
        ress = ress if isinstance(ress, list) else [ress]
        oai_ok = acts == ["s3:GetObject"] and len(ress) == 9 and all(
            x.startswith("arn:aws:s3:::%s/advi/" % a.bucket) and x.endswith("/*") for x in ress)
        lines.append("OAI one Allow statement: Get only, %d resources, ok=%s" % (len(ress), oai_ok))
    else:
        lines.append("OAI Allow statements found: %d" % len(oai))
    out = "\n".join(lines)
    print(out)
    last = "ROUND 4 ACT 3B SIM: %d of 9 admitted allowed, %d of 2 negatives not allowed, oai statement ok=%s" % (
        allowed, denied, oai_ok)
    print(last)
    try:
        os.unlink(policy_text)
    except OSError:
        pass
    if a.out:
        open(a.out, "w", encoding="utf-8", newline="\n").write(out + "\n" + last + "\n")
    return 0 if (allowed == 9 and denied == 2 and oai_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
