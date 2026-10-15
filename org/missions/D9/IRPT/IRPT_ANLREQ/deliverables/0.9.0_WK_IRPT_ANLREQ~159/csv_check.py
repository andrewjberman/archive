"""AR362-y-AC1: check the FWD-1 run 3 holdings csv (offline; no network, no AWS, no driver run).

Prints CSV-OK <n> rows, <ticker>, sha256 <first 12> only when the csv in this folder has the signed header and three
data rows: the first two byte-identical to the base file's two rows, the third <TICKER>,50,5000000 with TICKER in
{BREIT, SREIT, KPEC} and equal to chosen_ticker of r41/RUN3_HOLDINGS.json, ASCII only, LF endings, a final newline,
and the record's csv_sha256 equal to the file's. Otherwise prints CSV-BAD <why> and exits 1.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# This folder sits 7 levels below the worktree root: deliverables/<serial>/ -> IRPT_ANLREQ/ -> IRPT/ -> D9/ -> missions/ -> org/ -> root.
WT = os.path.normpath(os.path.join(HERE, *([os.pardir] * 7)))
CSV_NAME = "fwd1_holdings_49financial_r41b.csv"
RECORD = os.path.join(HERE, "r41", "RUN3_HOLDINGS.json")
BASE_CSV = os.path.join(WT, "org", "missions", "D9", "IRPT", "IRPT_ANLREQ", "deliverables",
                        "0.9.0_WK_IRPT_ANLREQ~149", "fwd1_driver", "fwd1_holdings_49financial.csv")
HEADER = b"Ticker,Dollars,Acct Market Value"
CHOICES = (b"BREIT", b"SREIT", b"KPEC")


def check(csv_path, record_path, base_path):
    """Return (True, 'CSV-OK ...') or (False, why)."""
    try:
        with open(csv_path, "rb") as fh:
            data = fh.read()
        with open(base_path, "rb") as fh:
            base = fh.read()
        with open(record_path, "rb") as fh:
            rec = json.loads(fh.read().decode("utf-8"))
    except (OSError, ValueError) as exc:
        return False, "unreadable input: %s" % exc
    if not data.isascii():
        return False, "csv carries non-ASCII bytes"
    if b"\r" in data:
        return False, "csv carries CR bytes (LF endings required)"
    if not data.endswith(b"\n"):
        return False, "csv has no final newline"
    lines = data[:-1].split(b"\n")
    if len(lines) != 4:
        return False, "csv has %d lines, expected header plus 3 rows" % len(lines)
    if lines[0] != HEADER:
        return False, "header is %r, expected %r" % (lines[0], HEADER)
    base_lines = base[:-1].split(b"\n") if base.endswith(b"\n") else None
    if base_lines is None or len(base_lines) != 3 or base_lines[0] != HEADER:
        return False, "base csv shape is not header plus 2 rows"
    if lines[1] != base_lines[1] or lines[2] != base_lines[2]:
        return False, "first two rows are not byte-identical to the base rows"
    ticker_bytes = lines[3].split(b",")[0]
    if ticker_bytes not in CHOICES:
        return False, "third row ticker %r is not in BREIT, SREIT, KPEC" % ticker_bytes
    if lines[3] != ticker_bytes + b",50,5000000":
        return False, "third row is not <TICKER>,50,5000000"
    ticker = ticker_bytes.decode("ascii")
    if rec.get("chosen_ticker") != ticker:
        return False, "record chosen_ticker %r differs from csv ticker %r" % (rec.get("chosen_ticker"), ticker)
    sha = hashlib.sha256(data).hexdigest()
    if rec.get("csv_sha256") != sha:
        return False, "record csv_sha256 %r differs from file sha256 %s" % (rec.get("csv_sha256"), sha)
    if rec.get("csv_bytes") != len(data):
        return False, "record csv_bytes %r differs from file bytes %d" % (rec.get("csv_bytes"), len(data))
    return True, "CSV-OK %d rows, %s, sha256 %s" % (len(lines) - 1, ticker, sha[:12])


def main():
    ok, msg = check(os.path.join(HERE, CSV_NAME), RECORD, BASE_CSV)
    print(msg if ok else "CSV-BAD " + msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
