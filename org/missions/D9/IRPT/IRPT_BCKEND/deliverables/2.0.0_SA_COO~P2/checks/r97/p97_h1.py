"""IRPT_BCKEND round 97 cell IB-pr-388, H1 (NFRA_TRNSPT FWD-10 C-TRIGGER; CTO msgs 1778, 2192, 2507; READY-event contract ~T2 @98ca40fd4c) -- the analysis report's
READY event to outlook-global-commentary-draft-lambda, as DESIRED Terraform (applied later under its own pair).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB97-1-AC1  core/dynamodb.tf: aws_dynamodb_table.requests carries stream_enabled = true and stream_view_type = "NEW_IMAGE"; a .tf in the
          core root declares exactly one aws_lambda_event_source_mapping whose filter carries INSERT, REPORT# and ANALYSIS, whose
          on-failure destination is an SQS queue, and whose function name is not a hand-typed literal. Base: FAIL (no stream).
  IB97-1-AC2  the commentary role is granted exactly dynamodb:DescribeStream, GetRecords, GetShardIterator and ListStreams on the requests
          table's stream ARN (a reference, not a literal), plus kms:Decrypt on the irpt key; no other action. Base: FAIL.
  IB97-1-AC3  `terraform fmt -check` passes on the core files H1 touches: dynamodb.tf, and every core .tf that declares an
          aws_lambda_event_source_mapping or names stream_arn. Three untouched files (main.tf, s3.tf, sqs.tf) are unformatted at base and
          are not graded. dell2's provider mirror lacks hashicorp/local, so an offline init/validate is not available; the applier's
          plan grades it at apply. Base: PASS (dynamodb.tf is formatted).
"""
import re
import subprocess
import sys
from pathlib import Path

CORE = "infra/aws/terraform/investor-reporting/core"
STREAM_ACTIONS = {"dynamodb:DescribeStream", "dynamodb:GetRecords", "dynamodb:GetShardIterator", "dynamodb:ListStreams"}


def block(text, kind, name=None):
    pat = r'resource\s+"%s"\s+"%s"\s*\{' % (re.escape(kind), re.escape(name) if name else r'[^"]+')
    out = []
    for m in re.finditer(pat, text):
        depth, i = 0, m.end() - 1
        while i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            if depth == 0:
                break
            i += 1
        out.append(text[m.start():i + 1])
    return out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB97-1"))
        sys.exit(1)

    core = root / CORE
    alltf = "\n".join(p.read_text(encoding="utf-8") for p in sorted(core.glob("*.tf")))
    if cid == "IB97-1-AC1":
        req = block(alltf, "aws_dynamodb_table", "requests")
        if len(req) != 1 or not re.search(r"stream_enabled\s*=\s*true", req[0]) \
                or not re.search(r'stream_view_type\s*=\s*"NEW_IMAGE"', req[0]):
            fail("requests table has no NEW_IMAGE stream")
        esm = block(alltf, "aws_lambda_event_source_mapping")
        if len(esm) != 1:
            fail("%d event source mappings in core" % len(esm))
        e = esm[0]
        for tok in ("INSERT", "REPORT#", "ANALYSIS"):
            if tok not in e:
                fail("filter lacks %s" % tok)
        if "on_failure" not in e or not re.search(r"sqs", e, re.I):
            fail("no SQS on-failure destination")
        fn = re.search(r"function_name\s*=\s*(.+)", e)
        if not fn or fn.group(1).strip().startswith('"'):
            fail("function_name is a hand-typed literal or absent: %r" % (fn.group(1) if fn else None))
        print("OK: NEW_IMAGE stream; 1 mapping filtered INSERT/REPORT#/ANALYSIS; SQS on-failure; function by reference")
    elif cid == "IB97-1-AC2":
        acts = set(re.findall(r'"(dynamodb:[A-Za-z]+)"', alltf))
        stream_ref = re.search(r"aws_dynamodb_table\.requests\.stream_arn", alltf)
        if not STREAM_ACTIONS <= acts or not stream_ref:
            fail("stream grant: actions %s, stream_arn reference %s" % (sorted(acts & STREAM_ACTIONS), bool(stream_ref)))
        pol = [b for b in re.findall(r"Statement\s*=\s*\[(.*?)\]\s*\}\)", alltf, re.S) if "stream_arn" in b]
        extra = set(re.findall(r'"([a-z0-9]+:[A-Za-z*]+)"', "".join(pol))) - STREAM_ACTIONS - {"kms:Decrypt"}
        if not pol or extra or "kms:Decrypt" not in "".join(pol):
            fail("stream policy: %d statement block(s), extra actions %s" % (len(pol), sorted(extra)))
        print("OK: 4 stream actions on requests.stream_arn + kms:Decrypt; no other action")
    elif cid == "IB97-1-AC3":
        common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=str(root),
                                capture_output=True, text=True).stdout.strip()
        cands = [root / ".tools" / "terraform.exe"] + ([Path(common).parent / ".tools" / "terraform.exe"] if common else [])
        tf = next((str(c) for c in cands if c.is_file()), "terraform")
        touched = ["dynamodb.tf"] + sorted(p.name for p in core.glob("*.tf") if p.name != "dynamodb.tf" and (
            "aws_lambda_event_source_mapping" in p.read_text(encoding="utf-8") or "stream_arn" in p.read_text(encoding="utf-8")))
        for args in (["fmt", "-check", "-no-color"] + touched,):
            p = subprocess.run([tf] + args, cwd=str(core), capture_output=True, timeout=280)
            if p.returncode != 0:
                fail("terraform %s rc %d: %s" % (args[0], p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")[-300:]))
        print("OK: terraform fmt -check passes in core")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
