"""IRPT_DASHBD round 22 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-21 analysis @214a0ef324 item E1: the
release of `account_class_daily`. This cell PREPARES it (handler, packaging, role, declaration, the never-widen packet) and proves it
locally; the apply and the after-read wait on the dell2 terraform kit and are the issuer's act under the signed halves.

Usage: python <this file> <repo_root> <criterion_id>
  DB22-1-AC1  the local release run: the extended handler's account_return_daily output for the sample is byte-identical to the
              unextended handler's (sha256 equal: DELTA=0 on the served table); on every measured account-day of its
              account_class_daily output the classes sum to the account within 1e-9; the unclassified share of value is printed
              with its denominator; the reporting-gold tests pass. Base: FAIL (no record).
  DB22-1-AC2  the role writes exactly two gold prefixes (account_return_daily and account_class_daily) and still no
              dim_return_method; iam.tf carries no Delete action; locals.tf names the class table once. Base: FAIL.
  DB22-1-AC3  the never-widen packet exists and carries the blast radius, the rollback per key, both branches of the expected
              outcome, the after-read the apply will run, and a CTO half and a COO half to sign. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~19/"
REC = W + "RELEASE_LOCAL_RUN.json"
PACKET = W + "NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md"
T = "infra/aws/terraform/investor-reporting/reporting-gold/"
TESTS = "infra/aws/lambda/investor-reporting/reporting-gold/tests"


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def _text(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return p.read_bytes().decode("utf-8")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB22"))
        sys.exit(1)

    if cid == "DB22-1-AC1":
        rec = _load(root, REC, fail)
        b, a = rec.get("returns_sha256_before"), rec.get("returns_sha256_after")
        if not b or b != a:
            fail("returns table not byte-identical: before %r after %r" % (b, a))
        acct = {(r["account_id"], r["business_date"]): r["account_daily_return"] for r in rec.get("account_days") or []}
        sums = defaultdict(float)
        for r in rec.get("class_rows") or []:
            if r.get("class_return_daily") is not None:
                sums[(r["account_id"], r["business_date"])] += float(r["class_return_daily"])
        if len(acct) < 10 or any(k not in sums for k in acct):
            fail("%d measured account-days; each needs class rows and at least 10 are required" % len(acct))
        worst = max(abs(sums[k] - float(v)) for k, v in acct.items())
        if worst > 1e-9:
            fail("classes do not sum to the account: largest gap %.3e" % worst)
        u = rec.get("unclassified_share") or {}
        if u.get("value") is None or not u.get("denominator"):
            fail("unclassified share not printed with its denominator: %r" % u)
        rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TESTS], cwd=str(root),
                            capture_output=True, text=True, timeout=110)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
        if rr.returncode or not re.search(r"\d+ passed", out):
            fail("reporting-gold tests: %s" % out[-300:])
        print("OK: returns DELTA=0 (sha256 equal); %d account-days sum within %.3e; unclassified share %s of %s; %s" % (
            len(acct), worst, u.get("value"), u.get("denominator"), re.search(r"\d+ passed", out).group(0)))
    elif cid == "DB22-1-AC2":
        loc = _text(root, T + "locals.tf", fail)
        iam = _text(root, T + "iam.tf", fail)
        if loc.count('"account_class_daily"') != 1:
            fail("locals.tf names \"account_class_daily\" %d times; once is required" % loc.count('"account_class_daily"'))
        m = re.search(r"irpt_rg_gold_write_arns\s*=\s*(\[.*?\]|\w[^\n]*)\n", loc, re.S)
        if not m:
            fail("no irpt_rg_gold_write_arns in locals.tf")
        w = m.group(1)
        if "returns" not in w or "class" not in w or "method" in w:
            fail("write set is %s; it must name the returns and class prefixes and never dim_return_method" % w.strip())
        if re.search(r"s3:Delete", iam):
            fail("iam.tf carries a Delete action")
        if "table/etf-classifications" not in iam or "dynamodb:GetItem" not in iam or re.search(r"dynamodb:(Scan|Put|Update|Delete)", iam):
            fail("iam.tf must grant dynamodb:GetItem on table/etf-classifications and no Scan or write")
        print("OK: the role writes the returns and class prefixes only; no Delete; GetItem on etf-classifications only")
    elif cid == "DB22-1-AC3":
        t = _text(root, PACKET, fail).lower()
        need = ["blast radius", "rollback", "branch a", "branch b", "after-read", "cto half", "coo half"]
        miss = [n for n in need if n not in t]
        if miss:
            fail("packet lacks: %s" % miss)
        print("OK: the packet carries %s" % ", ".join(need))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
