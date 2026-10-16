"""ADVI_COTBKF TO-CB-dc-1 (issuer's check): did the apply change the live SSM document by exactly the one account_attributes step, and nothing else?

Read-only (aws.cmd shim: ssm list-document-versions / get-document, s3api head-object / list-objects-v2). Prints counts and booleans only.
  python dc1_apply_check.py doc
    SILVER-DOC default_version=<n> prior_version=4 added=<n> removed=<n> added_is_account_attributes=<bool> nongating=<bool> after_holdings=<bool>
  python dc1_apply_check.py state
    SILVER-STATE manifest_unchanged=<bool> partitions=<n> existing_partition_unchanged=<bool>
  python dc1_apply_check.py selftest
    SILVER-DOC-SELFTEST good=<line> gating=<line> misplaced=<line> removal=<line>   (the same comparison run on synthetic edits of live version 4)
Rules: doc compares the runCommand list of the default version with version 4 line by line: added = lines in the default and not in 4, removed = the reverse;
added_is_account_attributes = the one added line holds '--table account_attributes'; nongating = it is a '{ ... || echo ...; } &&' group; after_holdings = it sits
immediately after the line holding '--table holdings'. state compares the manifest's VersionId and the 2026-08-19 partition's VersionId with the values read at the
COO half's signing, and counts the keys under silver/account_attributes/ (expect 1 until the first scheduled fire writes the rest).
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
AWS = str(REPO / ".tools" / "aws.cmd")
DOC = "opal-cot-silver-run"
BUCKET = "opal-data-cot"
MANIFEST_VID = "EJDw_ZHST0x7oLC_k34IoqWcC80hn6.w"
PARTITION_VID = "Bf6UyF9aiOcZGinRnCnFYpO_b04WXiPH"


def aws(*a):
    r = subprocess.run([AWS, *a], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("aws %s rc=%d" % (" ".join(a[:3]), r.returncode))
    return r.stdout


def commands(version):
    txt = aws("ssm", "get-document", "--name", DOC, "--document-version", str(version), "--query", "Content", "--output", "text")
    return json.loads(txt)["mainSteps"][0]["inputs"]["runCommand"]


def compare(prior, cur):
    added = [c for c in cur if c not in prior]
    removed = [c for c in prior if c not in cur]
    one = added[0] if len(added) == 1 else ""
    is_aa = "--table account_attributes" in one
    nongating = is_aa and one.strip().startswith("{") and "|| echo" in one and one.rstrip().endswith("&&")
    hold = [i for i, c in enumerate(cur) if "--table holdings" in c]
    after = bool(is_aa and hold and cur.index(one) == hold[0] + 1)
    return len(added), len(removed), is_aa, nongating, after


def line_for(prior, cur):
    a, r, is_aa, ng, af = compare(prior, cur)
    return "added=%d removed=%d added_is_account_attributes=%s nongating=%s after_holdings=%s" % (a, r, is_aa, ng, af)


mode = sys.argv[1] if len(sys.argv) > 1 else "doc"
if mode in ("doc", "selftest"):
    vers = json.loads(aws("ssm", "list-document-versions", "--name", DOC, "--output", "json"))["DocumentVersions"]
    default = [v["DocumentVersion"] for v in vers if v.get("IsDefaultVersion")][0]
    prior = commands(4)
    if mode == "doc":
        cur = commands(default)
        print("SILVER-DOC default_version=%s prior_version=4 %s" % (default, line_for(prior, cur)))
    else:
        hi = [i for i, c in enumerate(prior) if "--table holdings" in c][0]
        good = "  { python3.11 /tmp/cot_silver_merge.py --table account_attributes $DATE_ARG || echo 'WARN: account_attributes refresh failed -- NON-GATING'; } &&"
        gating = "  python3.11 /tmp/cot_silver_merge.py --table account_attributes $DATE_ARG &&"
        out = {
            "good": prior[: hi + 1] + [good] + prior[hi + 1:],
            "gating": prior[: hi + 1] + [gating] + prior[hi + 1:],
            "misplaced": prior[:hi] + [good] + prior[hi:],
            "removal": prior[: hi + 1] + [good] + prior[hi + 2:],
        }
        print("SILVER-DOC-SELFTEST " + " ".join("%s=[%s]" % (k, line_for(prior, v).replace(" ", ",")) for k, v in out.items()))
else:
    head = json.loads(aws("s3api", "head-object", "--bucket", BUCKET, "--key", "silver/cot_incremental_manifest_account_attributes.json", "--output", "json"))
    part = json.loads(aws("s3api", "head-object", "--bucket", BUCKET, "--key", "silver/account_attributes/2026-08-19.parquet", "--output", "json"))
    lst = json.loads(aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "silver/account_attributes/", "--output", "json"))
    n = len(lst.get("Contents", []))
    print("SILVER-STATE manifest_unchanged=%s partitions=%d existing_partition_unchanged=%s"
          % (head.get("VersionId") == MANIFEST_VID, n, part.get("VersionId") == PARTITION_VID))
