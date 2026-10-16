#!/usr/bin/env python3
"""AR-y-368 inputs checker (0.9.0_WK_IRPT_ANLREQ~165). Prints INPUTS-OK only when the run 3 csv, the decisions file and
the record agree with each other and with the door source bytes at git HEAD. Offline: git show, sha256 and node (the
driver's own readDecisionsFile validator, read from the signed driver file). Never calls the driver's main, the network
or AWS. Exit 0 = INPUTS-OK, 1 = INPUTS-BAD <why>."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
DRIVER = ROOT / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs"
BASE_CSV = ROOT / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_holdings_49financial.csv"
RECORD = HERE / "r41" / "RUN3_TICKER_BRANCHES.json"
CSV = HERE / "fwd1_holdings_49financial_r41c.csv"
DECISIONS = HERE / "fwd1_decisions_r41c.json"
HEADER = "Ticker,Dollars,Acct Market Value"
ORDER = ["A1", "A2", "B"]
ROW_TAIL = ",50,5000000"
MAX_ROWS = 5
NODE_CODE = ("import { pathToFileURL } from 'node:url';"
             "const m = await import(pathToFileURL(process.env.FWD_DRIVER).href);"
             "console.log(JSON.stringify(m.readDecisionsFile(process.env.FWD_DECISIONS)));")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_head_lines(rel):
    """The file's lines at git HEAD (the repo's own bytes), or None when the path is absent at HEAD."""
    proc = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:" + rel], capture_output=True, timeout=120)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace").split("\n")


def node_verdict(decisions_path):
    """The driver's own reader and validator (readDecisionsFile -> validateDecisions), run through node."""
    env = dict(os.environ, FWD_DRIVER=str(DRIVER), FWD_DECISIONS=str(decisions_path))
    proc = subprocess.run(["node", "--input-type=module", "-e", NODE_CODE], env=env, capture_output=True,
                          text=True, timeout=120)
    if proc.returncode != 0:
        return None, "node rc=%d" % proc.returncode
    out = proc.stdout.strip().splitlines()
    try:
        return json.loads(out[-1]), None
    except (IndexError, ValueError):
        return None, "validator output is not JSON"


def check(record, csv_path, decisions_path):
    """Returns (violations, results). results is a list of (name, ok); violations are the failing names with why."""
    results = []
    violations = []

    def ck(name, ok, why=""):
        results.append((name, bool(ok)))
        if not ok:
            violations.append("%s%s" % (name, (" (" + why + ")") if why else ""))

    raw = Path(csv_path).read_bytes()
    ck("csv ascii, LF only, final newline", all(b < 128 for b in raw) and b"\r" not in raw and raw.endswith(b"\n"))
    lines = raw.decode("ascii", "replace").split("\n")[:-1]
    ck("csv exact header", bool(lines) and lines[0] == HEADER, repr(lines[0]) if lines else "empty")
    data = lines[1:]
    base_lines = Path(BASE_CSV).read_bytes().decode("ascii", "replace").split("\n")[:-1]
    ck("csv first two rows byte-identical to the signed base rows",
       data[:2] == base_lines[1:3], "csv %r base %r" % (data[:2], base_lines[1:3]))
    branches = record.get("branches", {}) if isinstance(record, dict) else {}
    est = [b for b in ORDER if isinstance(branches.get(b), dict) and branches[b].get("status") == "established"]
    tickers = [branches[b].get("chosen_ticker") for b in est]
    ck("record: established branches carry a chosen ticker", all(isinstance(t, str) and t for t in tickers))
    ck("csv row count is 2 signed + one per established branch, at most %d" % MAX_ROWS,
       len(data) == 2 + len(est) and len(data) <= MAX_ROWS, "%d data rows, %d established" % (len(data), len(est)))
    ck("csv branch rows in order A1, A2, B", data[2:] == [t + ROW_TAIL for t in tickers],
       repr(data[2:]))
    ck("record established_branches equals the computed list", record.get("established_branches") == est,
       repr(record.get("established_branches")))
    ck("record csv_sha256 equals the file", record.get("csv_sha256") == sha256_file(csv_path))
    ck("record csv_bytes equals the file", record.get("csv_bytes") == Path(csv_path).stat().st_size)
    ck("record decisions_sha256 equals the file", record.get("decisions_sha256") == sha256_file(decisions_path))
    verdict, err = node_verdict(decisions_path)
    ck("decisions file passes the driver's readDecisionsFile validator", verdict is not None and verdict.get("ok") is True,
       err or repr(verdict))
    decisions = (verdict or {}).get("decisions", []) if verdict else []
    csv_tickers = [row.split(",")[0] for row in data]
    ck("every decision names a symbol present in the csv",
       all(d.get("symbol") in csv_tickers for d in decisions), repr([d.get("symbol") for d in decisions]))
    expected = {}
    for b in ("A1", "A2"):
        if b in est:
            expected[branches[b]["chosen_ticker"]] = "yes" if b == "A1" else "replace"
    got = {d.get("symbol"): d.get("answer") for d in decisions}
    ck("decisions name exactly the established A1 (yes) and A2 (replace) branches", got == expected,
       "got %r expected %r" % (got, expected))
    for d in decisions:
        if d.get("answer") == "replace":
            ck("A2 replacement is a csv-independent ticker not already a csv row",
               d.get("replacement") not in csv_tickers, repr(d.get("replacement")))
    for b in ORDER:
        br = branches.get(b)
        ck("branch %s carries a status of established or UNESTABLISHED-OFFLINE" % b,
           isinstance(br, dict) and br.get("status") in ("established", "UNESTABLISHED-OFFLINE"))
        if not isinstance(br, dict):
            continue
        if br.get("status") == "UNESTABLISHED-OFFLINE":
            cands = br.get("candidates_for_a_live_read") or []
            ck("branch %s unestablished: reason and 1 to 3 candidates" % b,
               bool(br.get("reason_if_unestablished")) and 1 <= len(cands) <= 3, repr(cands))
    clean = record.get("clean") if isinstance(record, dict) else None
    ck("clean branch carries its tickers and evidence",
       isinstance(clean, dict) and bool(clean.get("tickers")) and bool(clean.get("evidence")))
    # Every evidence quote in the record must occur at its cited file and line at git HEAD.
    holders = [branches.get(b, {}) for b in ORDER] + [clean or {}]
    for holder in holders:
        for ev in holder.get("evidence", []) if isinstance(holder, dict) else []:
            rel, line, quote = ev.get("file"), ev.get("line"), ev.get("quote")
            head = git_head_lines(rel) if isinstance(rel, str) else None
            ok = (head is not None and isinstance(line, int) and 1 <= line <= len(head)
                  and isinstance(quote, str) and quote != "" and quote in head[line - 1].rstrip("\r"))
            ck("evidence quote at %s:%s" % (rel, line), ok, "quote not at the cited HEAD line")
    return violations, results


def main():
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    violations, results = check(record, CSV, DECISIONS)
    passed = sum(1 for _, ok in results if ok)
    quotes = [r for r in results if r[0].startswith("evidence quote")]
    branches = record.get("branches", {})
    est = [b for b in ORDER if isinstance(branches.get(b), dict) and branches[b].get("status") == "established"]
    rows = len(CSV.read_bytes().decode("ascii", "replace").split("\n")[:-1]) - 1
    if violations:
        print("INPUTS-BAD " + "; ".join(violations) + " ; checks %d of %d passed" % (passed, len(results)))
        return 1
    print("INPUTS-OK %d rows, branches %s, decisions valid, csv sha256 %s; checks %d of %d passed; "
          "evidence quotes %d of %d at git HEAD" % (
              rows, ",".join(est) if est else "none", sha256_file(CSV)[:12], passed, len(results),
              sum(1 for _, ok in quotes if ok), len(quotes)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
