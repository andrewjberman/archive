#!/usr/bin/env python3
"""YCD-f-6 checks (issuer-written; the worker runs them, never edits them). Usage: python f-6.check.py ACn [BASE_COMMIT]

Reads infra/aws/terraform/investor-reporting/ycharts/resident.tf from the worktree and prints one line,
`f-6.ACn RESULT: PASS` or `f-6.ACn RESULT: FAIL <reason>`. No AWS call. BASE_COMMIT defaults to the merge-base of
HEAD and CLOUD (the branch point), the commit every added and removed line is counted from.
ASCII only.
"""
import re
import subprocess
import sys

TF = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"


def sh(*args):
    out = subprocess.run(args, capture_output=True, text=True)
    return out.returncode, out.stdout, out.stderr


def text():
    return open(TF, encoding="utf-8", newline="").read().replace("\r\n", "\n")


def statements(src):
    """{Sid: the statement block text} for every Sid in the runner_resident policy."""
    blocks = {}
    for m in re.finditer(r'Sid\s*=\s*"([^"]+)"', src):
        start = src.rfind("{", 0, m.start())
        depth, i = 0, start
        while i < len(src):
            depth += src[i] == "{"
            depth -= src[i] == "}"
            i += 1
            if depth == 0:
                break
        blocks[m.group(1)] = src[start:i]
    return blocks


def actions(block, service):
    """The `service:Name` strings inside the statement's `Action = [...]` list only (never a Condition key like s3:prefix)."""
    m = re.search(r"Action\s*=\s*\[(.*?)\]", block, re.S)
    return re.findall(r'"(%s:[A-Za-z]+)"' % service, m.group(1)) if m else []


def fail(name, why):
    print("f-6.%s RESULT: FAIL %s" % (name, why))
    sys.exit(1)


def ok(name):
    print("f-6.%s RESULT: PASS" % name)


def main():
    name = sys.argv[1]
    src = text()
    st = statements(src)
    if name == "AC1":  # the file is formatted
        rc, out, err = sh("terraform", "fmt", "-check", "-diff", TF)
        (ok if rc == 0 else lambda n: fail(n, "terraform fmt -check rc=%d %s" % (rc, (out + err)[:200])))(name)
    elif name == "AC2":  # the Opal PDF prefix is derived from the registry and the research policy's firms, never typed
        m = re.search(r"ycdgen_opal_report_prefixes\s*=\s*\[(.*?)\n  \]", src, re.S)
        if not m:
            fail(name, "no local ycdgen_opal_report_prefixes")
        body = m.group(1)
        need = ['local.ycdgen_firms', 'local.ycdgen_policy.families["YCHARTS_OPAL_REPORT"]', "local.resident_bucket",
                "local.resident_scopes"]
        miss = [n for n in need if n not in body]
        if miss:
            fail(name, "prefix local does not derive from " + ", ".join(miss))
        if re.search(r"opal-data-[a-z]+|irpt/cottonwood|ycharts_opal_reports", body):
            fail(name, "a bucket, firm or table name is typed in the prefix local")
        s = st.get("RetainTheOpalReportPdf", "")
        acts = actions(s, "s3")
        if sorted(acts) != ["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject"] or "local.ycdgen_opal_report_prefixes" not in s:
            fail(name, "statement RetainTheOpalReportPdf missing or its actions/resource are wrong: %s" % acts)
        ok(name)
    elif name == "AC3":  # the KMS condition names the new prefix too
        s = st.get("ReportEncryptionViaS3ForResidentFamiliesOnly", "")
        if "local.ycdgen_opal_report_prefixes" not in s or "local.resident_write_prefixes" not in s \
                or "local.resident_read_prefixes" not in s:
            fail(name, "kms condition does not carry all three prefix lists")
        ok(name)
    elif name == "AC4":  # one GetItem, one table
        s = st.get("ReadTheCanonicalClassificationTable", "")
        acts = actions(s, "dynamodb")
        if acts != ["dynamodb:GetItem"]:
            fail(name, "actions %s" % acts)
        if not re.search(r"table/etf-classifications\"?\s*\]", s) or s.count("arn:aws:dynamodb") != 1:
            fail(name, "resource is not exactly the etf-classifications table ARN")
        ok(name)
    elif name == "AC5":  # the held fund data: get on bbg/*, list on the bucket cut to bbg/
        g = st.get("ReadTheHeldFundCharacteristics", "")
        lst = st.get("ListTheHeldFundCharacteristicsFolder", "")
        if actions(g, "s3") != ["s3:GetObject"] or "arn:aws:s3:::opal-data-etfs/bbg/*" not in g:
            fail(name, "get statement missing or wrong")
        if actions(lst, "s3") != ["s3:ListBucket"] or '"arn:aws:s3:::opal-data-etfs"' not in lst \
                or "s3:prefix" not in lst or "bbg/" not in lst:
            fail(name, "list statement missing, wrong, or not cut to the bbg/ prefix")
        ok(name)
    elif name == "AC6":  # nothing else moved
        base = sys.argv[2] if len(sys.argv) > 2 else sh("git", "merge-base", "HEAD", "CLOUD")[1].strip()
        if not re.fullmatch(r"[0-9a-f]{7,40}", base):
            fail(name, "no base commit")
        rc, diff, err = sh("git", "diff", "-U0", base, "--", TF)
        rc2, worktree, _ = sh("git", "diff", "-U0", "--", TF)
        diff = diff if diff.strip() else worktree
        removed = [ln[1:] for ln in diff.split("\n") if ln.startswith("-") and not ln.startswith("---")]
        added = [ln[1:] for ln in diff.split("\n") if ln.startswith("+") and not ln.startswith("+++")]
        # the only existing line that may change is the kms StringLike list (one line, gains one concat term)
        bad = [ln for ln in removed if "kms:EncryptionContext:aws:s3:arn" not in ln and ln.strip() != ""]
        if bad:
            fail(name, "lines removed or changed besides the kms condition: %s" % bad[:2])
        if len(removed) > 1:
            fail(name, "%d lines removed; at most the one kms condition line" % len(removed))
        head = sh("git", "rev-parse", "HEAD")[1].strip()
        full = sh("git", "rev-parse", base)[1].strip()
        # before the worker commits, HEAD is the base and its edits are in the worktree; after, they are in HEAD
        files = (sh("git", "diff", "--name-only", base)[1] if head == full else sh("git", "diff", "--name-only", base, "HEAD")[1]).split()
        extra = [f for f in files if f not in (TF, "portal") and "deliverables/0.9.0_WK_IRPT_YCDGEN" not in f and not f.endswith("INVESTIGATION_v1.md")]  # `portal` is the submodule pointer provisioning moves
        if extra:
            fail(name, "other files changed: %s" % extra[:3])
        if not added:
            fail(name, "no change found against base %s" % base[:10])
        ok(name)
    else:
        fail(name, "unknown check")


main()
