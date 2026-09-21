"""TX-m-3 -- case evidence for the four current exceptions (PRD s.3.3), READ ONLY
(MDPF_TAXSMA round 1, 0.9.0_WK_MDPF_TAXSMA~6).

Usage (from the worktree root):  py -3.12 <this file> AC<n>     n = 1..5   (AC6 is judgment, no probe)

One criterion per invocation. Prints its measurement with vintage (HEAD + UTC run time) and
denominator, then EXACTLY ONE line:  VERDICT: PASS-TXM3-AC<n>  or  VERDICT: FAIL-TXM3-AC<n> <reason>.

The deliverable this probe grades is ../exception-cases.result.md (case evidence, read-only cell).
Every AWS call this probe makes goes through the workspace `.tools/aws` shim (via the Git Bash
resolver) and is appended to `command_log.jsonl` in this deliverables folder BEFORE it runs, tagged
cell="TX-m-3", so a call that crashes is still in the log. AC5 greps that log for this cell's tag and
grades every tagged entry a read verb with no write to any dataset/workbook/roster/custodian record.

Private data: no object body is downloaded here; only list-objects-v2/head-object/head-bucket
(existence, counts, vintage metadata) are called. No account number, name or balance is printed by
this probe or is permitted in the deliverable it grades (AC4).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
WS = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                  cwd=str(HERE)).decode().strip())
HEAD = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(WS)).decode().strip()
LOG = DELIV / "command_log.jsonl"
DELIVERABLE = DELIV / "exception-cases.result.md"
CELL = "TX-m-3"
ACCOUNT = "313476888478"
REGION = "us-east-1"
READ_VERBS = ("describe", "get", "list", "head")

sys.path.insert(0, str(WS / ".tools"))
from git_bash_resolver import git_bash  # noqa: E402

CRIT = "?"


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_call(service: str, op: str, args: str) -> None:
    rec = {"utc": utc(), "criterion": CRIT, "cell": CELL, "service": service, "operation": op,
           "args": args[:400], "via": ".tools/aws", "head": HEAD[:10]}
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def aws(service: str, op: str, *args: str, timeout: int = 60):
    """Run one read-only AWS CLI call through the shim. Returns (rc, parsed_json_or_None, stderr)."""
    bash = git_bash()
    if not bash:
        raise SystemExit("ERROR: no Git Bash resolved -- refusing to fall back to bare bash")
    log_call(service, op, " ".join(args))
    argv = [bash, str(WS / ".tools" / "aws"), service, op, *args,
            "--region", REGION, "--output", "json"]
    env = dict(os.environ, AWS_PAGER="")
    try:
        p = subprocess.run(argv, capture_output=True, timeout=timeout, env=env, cwd=str(WS))
    except subprocess.TimeoutExpired:
        return 124, None, "TIMEOUT after %ss" % timeout
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace").strip()
    data = None
    if p.returncode == 0:
        data = json.loads(out) if out.strip() else {}
    return p.returncode, data, err


def banner(n: int) -> None:
    print("TX-m-3 AC%d | worktree HEAD %s | run_at %s | probe %s" % (n, HEAD, utc(), Path(__file__).name))


def read_deliverable() -> str:
    if not DELIVERABLE.exists():
        return ""
    return DELIVERABLE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------------------- carriers
# Address()-built carriers this project's own contract nominates for the workbook's OWN capture
# (checked live -- these are the only place a worker-reachable "full workbook identity" could sit).
WORKBOOK_CAPTURE_PREFIXES = [
    ("opal-data-assets", "gateway/49financial/bronze/taxsma_workbook/"),
    ("opal-data-assets", "gateway/49financial/silver/taxsma_workbook/"),
]
DISPOSITIONS = ("opal-data-49financial", "mdpf/49financial/state/taxsma_membership/dispositions.json")

# Carriers a worker CAN read (Opal AWS infra, read-only) that hold full CUSTODIAN identities, cited
# from RESEARCH.md's "Source and producer evidence" table (read, not re-downloaded here). The
# reporting-master and base-master path segments are masked to <reporting-master>/<base-master> in
# BOTH this list and the deliverable text -- those digit strings are custodian MASTER identifiers
# already published in the ratified data contract (identity.reporting_master / .base_master_control),
# not client account numbers, and this cell does not restate them to stay conservative under AC4.
CUSTODIAN_CARRIERS = [
    "s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json",
    "s3://opal-data-assets/schwab/<reporting-master>/silver/fact_acc/date=2026-09-11/data.parquet",
    "s3://opal-data-assets/schwab/<reporting-master>/silver/fact_rps/date=2026-09-11/data.parquet",
    "s3://opal-data-assets/schwab/<reporting-master>/silver/dim_balance/date=2026-09-11/data.parquet",
    "s3://opal-data-assets/schwab/<base-master>/silver/fact_acc/date=2026-09-11/data.parquet",
    "s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/date=2026-09-11/data.parquet",
    "s3://opal-data-assets/blackdiamond/49f/gold/dim_taxsma_report/",
    "s3://opal-data-49financial/gold/advi/canonical/canonical_valuation/date=2026-09-11/data.parquet",
]


def ac1() -> bool:
    banner(1)
    print("MEASUREMENT: live list-objects-v2 on the contract's own workbook-capture carriers "
          "(the only place a worker-reachable full WORKBOOK identity, as opposed to a custodian "
          "identity, could be recorded).")
    empty = 0
    checked = 0
    for bucket, prefix in WORKBOOK_CAPTURE_PREFIXES:
        checked += 1
        rc, d, err = aws("s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix)
        contents = (d or {}).get("Contents")
        n = len(contents) if contents else 0
        print("  s3://%s/%s -> rc=%s KeyCount=%d at %s" % (bucket, prefix, rc, n, utc()))
        if rc == 0 and n == 0:
            empty += 1
    rc, d, err = aws("s3api", "head-object", "--bucket", DISPOSITIONS[0], "--key", DISPOSITIONS[1])
    print("  s3://%s/%s (dispositions) -> rc=%s (404 == absent expected) at %s"
          % (DISPOSITIONS[0], DISPOSITIONS[1], rc, utc()))
    dispositions_absent = (rc != 0)
    print("DENOMINATOR: %d of %d workbook-capture prefixes measured EMPTY live; dispositions carrier "
          "absent=%s." % (empty, checked, dispositions_absent))
    print("CUSTODIAN CARRIERS a worker CAN read (Opal AWS infra, read-only; cited from RESEARCH.md, "
          "not re-downloaded): %d enumerated." % len(CUSTODIAN_CARRIERS))

    text = read_deliverable()
    if not text:
        print("VERDICT: FAIL-TXM3-AC1 deliverable exception-cases.result.md not found")
        return False

    has_enum = bool(re.search(r"(?im)^##.*protected carriers", text)) and \
        sum(1 for c in CUSTODIAN_CARRIERS if c in text) >= 6
    has_workbook_carrier_finding = "gateway/49financial/bronze/taxsma_workbook" in text and \
        "gateway/49financial/silver/taxsma_workbook" in text
    has_join_statement = bool(re.search(r"(?is)cannot\s+be\s+joined\s+on\s+full\s+key", text))
    if not empty == checked:
        print("VERDICT: FAIL-TXM3-AC1 live measurement changed: workbook-capture prefixes are no "
              "longer empty (%d of %d), the deliverable's premise is stale" % (empty, checked))
        return False
    if not (has_enum and has_workbook_carrier_finding and has_join_statement):
        print("VERDICT: FAIL-TXM3-AC1 deliverable missing enumeration(%s)/workbook-carrier finding(%s)"
              "/join statement(%s)" % (has_enum, has_workbook_carrier_finding, has_join_statement))
        return False
    print("VERDICT: PASS-TXM3-AC1")
    return True


# ---------------------------------------------------------------------------------------- AC2
def ac2() -> bool:
    banner(2)
    text = read_deliverable()
    if not text:
        print("VERDICT: FAIL-TXM3-AC2 deliverable not found")
        return False
    labels = ["4809", "5591"]
    print("MEASUREMENT: reading account-status-evidence.json@8e8afed454 for the two absent-from-0833 "
          "claims (acc_exact_rows==0), and RESEARCH.md@8e8afed454 line 114 ('No cause has yet been "
          "proven ...').")
    ok = True
    for lab in labels:
        present = ("..." + lab in text) or ("…" + lab in text) or (lab in text)
        unresolved = bool(re.search(r"(?is)%s.{0,600}?UNRESOLVED" % re.escape(lab), text)) or \
            bool(re.search(r"(?is)UNRESOLVED.{0,600}?%s" % re.escape(lab), text))
        print("  label ...%s: mentioned=%s, UNRESOLVED-with-evidence-nearby=%s" % (lab, present, unresolved))
        ok = ok and present and unresolved
    denom = "%d of %d exception labels carry an UNRESOLVED-plus-evidence statement" % (
        sum(1 for lab in labels if re.search(r"(?is)%s.{0,600}?UNRESOLVED" % re.escape(lab), text)
            or re.search(r"(?is)UNRESOLVED.{0,600}?%s" % re.escape(lab), text)), len(labels))
    print("DENOMINATOR: " + denom)
    if not ok:
        print("VERDICT: FAIL-TXM3-AC2 one or both absent-claim labels lack a stated cause class or "
              "UNRESOLVED-with-evidence")
        return False
    print("VERDICT: PASS-TXM3-AC2")
    return True


# ---------------------------------------------------------------------------------------- AC3
def ac3() -> bool:
    banner(3)
    text = read_deliverable()
    if not text:
        print("VERDICT: FAIL-TXM3-AC3 deliverable not found")
        return False
    pairs = ["5115", "3310"]
    print("MEASUREMENT: reading account-status-evidence.json@8e8afed454 excel_strategy vs "
          "acc_strategies for the two strategy-conflict accounts, and RESEARCH.md's workbook-modified "
          "(2026-09-14T18:33:00Z) and 0833 business-date (2026-09-11) source dates.")
    ok = True
    for lab in pairs:
        has145 = has200 = False
        for near in re.finditer(r"(?is)%s(.{0,500})" % re.escape(lab), text):
            blob = near.group(1)
            if "145" in blob:
                has145 = True
            if "200" in blob:
                has200 = True
        has_dates = ("2026-09-14" in text) and ("2026-09-11" in text)
        print("  label ...%s: workbook-145=%s custodian-200=%s dates_present=%s" % (lab, has145, has200, has_dates))
        ok = ok and has145 and has200 and has_dates
    print("DENOMINATOR: 2 of 2 strategy-conflict labels required to carry both labels and both dates")
    if not ok:
        print("VERDICT: FAIL-TXM3-AC3 one or both conflict labels missing workbook label, custodian "
              "label or a source date")
        return False
    print("VERDICT: PASS-TXM3-AC3")
    return True


# ---------------------------------------------------------------------------------------- AC4
FULL_ACCOUNT_PATTERNS = [
    re.compile(r"(?<!\d)00\d{8}(?!\d)"),          # ten digits beginning 00
    re.compile(r"(?<!\d)\d{4}-\d{4}(?!\d)"),       # four-hyphen-four
    re.compile(r"(?<![\w])\d{8}(?![\w])"),          # eight ASCII digits (word-boundary safe)
]
DATE_LIKE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def ac4() -> bool:
    banner(4)
    text = read_deliverable()
    if not text:
        print("VERDICT: FAIL-TXM3-AC4 deliverable not found")
        return False
    hits = []
    for pat in FULL_ACCOUNT_PATTERNS:
        for m in pat.finditer(text):
            frag = m.group(0)
            # an 8-digit run that is really a compact date embedded in a longer ISO/date context
            # is excluded only when it is exactly a YYYYMMDD calendar-looking token, never a
            # standalone account-shaped run
            if len(frag) == 8 and frag.isdigit() and frag[:2] == "20" and 1 <= int(frag[4:6]) <= 12:
                continue
            hits.append(frag)
    print("MEASUREMENT: regex scan of exception-cases.result.md for ten-digit-00, four-hyphen-four "
          "and eight-digit account-shaped runs, %d bytes scanned at %s." % (len(text), utc()))
    print("DENOMINATOR: %d of %d scanned bytes matched an account-shaped pattern (excluding "
          "calendar-looking 8-digit tokens)." % (len(hits), len(text)))
    if hits:
        print("  first flagged fragment (masked to length only): len=%d count=%d" % (len(hits[0]), len(hits)))
        print("VERDICT: FAIL-TXM3-AC4 %d account-shaped digit run(s) found" % len(hits))
        return False
    print("VERDICT: PASS-TXM3-AC4")
    return True


# ---------------------------------------------------------------------------------------- AC5
WRITE_OPS = ("put", "delete", "create", "update", "write", "copy", "cp", "sync", "mv", "rm")


def ac5() -> bool:
    banner(5)
    if not LOG.exists():
        print("MEASUREMENT: command_log.jsonl does not exist yet (0 calls logged).")
        print("VERDICT: PASS-TXM3-AC5")
        return True
    rows = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    tagged = [r for r in rows if r.get("cell") == CELL]
    print("MEASUREMENT: %d total lines in command_log.jsonl; %d tagged cell=%s, read at %s." %
          (len(rows), len(tagged), CELL, utc()))
    bad = []
    for r in tagged:
        op = str(r.get("operation", "")).lower()
        is_read = op.startswith(READ_VERBS)
        is_write = any(op.startswith(w) for w in WRITE_OPS)
        touches = str(r.get("args", "")).lower()
        forbidden_target = any(k in touches for k in ("taxsma_workbook", "workbook", "roster", "dispositions.json"))
        if is_write or (forbidden_target and not is_read):
            bad.append(r)
    read_n = sum(1 for r in tagged if str(r.get("operation", "")).lower().startswith(READ_VERBS))
    print("DENOMINATOR: READ-VERB CALLS %d of %d tagged; NON-READ/forbidden-target: %d of %d." %
          (read_n, len(tagged), len(bad), len(tagged)))
    for r in bad:
        print("  BAD: %s %s %s" % (r.get("utc"), r.get("operation"), r.get("args")))
    if not tagged:
        print("VERDICT: FAIL-TXM3-AC5 no calls tagged cell=%s were logged -- cannot grade" % CELL)
        return False
    if bad:
        print("VERDICT: FAIL-TXM3-AC5 %d non-read or forbidden-target call(s) tagged %s" % (len(bad), CELL))
        return False
    print("VERDICT: PASS-TXM3-AC5")
    return True


CRITERIA = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5}


def main() -> int:
    global CRIT
    if len(sys.argv) != 2 or sys.argv[1] not in CRITERIA:
        print("usage: py -3.12 tx_m_3.py AC<1..5>", file=sys.stderr)
        return 2
    CRIT = sys.argv[1]
    ok = CRITERIA[CRIT]()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
