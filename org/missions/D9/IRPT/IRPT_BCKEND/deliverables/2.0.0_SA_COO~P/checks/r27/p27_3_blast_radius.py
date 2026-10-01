"""Round 27 AC (IB-pr-273: CTO round-26 analysis ruling 4, rows S237/S239) -- the blast-radius read of the retiring engine's
skipped-day error is on the record, measured against the DEPLOYED adapter and every served reader of twr_daily.

Usage: python p27_3_blast_radius.py <worktree root>
Reads org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~100/S237_BLAST_RADIUS.json and requires:
  `adapter`: {"function": "irpt-performance-adapter", "code_sha256": <the CodeSha256 the worker ran>, "accounts": {...}} where
      code_sha256 EQUALS the live function's CodeSha256 read now (lambda get-function-configuration), and `accounts` holds
      account 0093614544 plus at least two other S237-population accounts, each with "SI" and "3Y" answers (a figure or a named
      refusal code, verbatim from the deployed code's output) and "reads" naming the table the answer came from;
  `reader_shape`: "PARTITION_LISTING" | "CALENDAR_ENUMERATION" | "NOT_A_TWR_DAILY_READER" for the served adapter path;
  `readers`: >= 1 entries, each {"file", "served_surface", "reads_2025_01_09", "propagates"} with propagates in {true, false};
  `verdict`: "PROPAGATES" | "DOES_NOT_PROPAGATE", equal to any(readers[].propagates) plus the adapter's own verdict.
Pass line: P27-3-AC1 PASS. Base: FAIL (record absent).
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REC = root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~100/S237_BLAST_RADIUS.json"


def fail(msg):
    print("P27-3-AC1 FAIL: " + msg)
    sys.exit(1)


if not REC.exists():
    fail("record absent: %s" % REC)
d = json.loads(REC.read_text(encoding="utf-8"))
ad = d.get("adapter") or {}
if ad.get("function") != "irpt-performance-adapter":
    fail("adapter.function %r" % ad.get("function"))
import boto3  # noqa: E402

live = boto3.client("lambda", region_name="us-east-1").get_function_configuration(
    FunctionName="irpt-performance-adapter")["CodeSha256"]
if ad.get("code_sha256") != live:
    fail("adapter.code_sha256 %r is not the live CodeSha256 %r (the read must run the DEPLOYED code)" % (ad.get("code_sha256"), live))
accts = ad.get("accounts") or {}
if "0093614544" not in accts or len(accts) < 3:
    fail("accounts must hold 0093614544 plus two others (have %s)" % sorted(accts))
for a, row in accts.items():
    for k in ("SI", "3Y", "reads"):
        if k not in row or row[k] in (None, ""):
            fail("account %s lacks %s" % (a, k))
if d.get("reader_shape") not in ("PARTITION_LISTING", "CALENDAR_ENUMERATION", "NOT_A_TWR_DAILY_READER"):
    fail("reader_shape %r" % d.get("reader_shape"))
readers = d.get("readers") or []
if not readers:
    fail("no readers censused")
for r in readers:
    if not all(k in r for k in ("file", "served_surface", "reads_2025_01_09", "propagates")) or not isinstance(r["propagates"], bool):
        fail("reader row incomplete: %r" % r)
    if not (root / r["file"]).exists():
        fail("reader file absent: %s" % r["file"])
want = "PROPAGATES" if any(r["propagates"] for r in readers) or ad.get("propagates") is True else "DOES_NOT_PROPAGATE"
if d.get("verdict") != want:
    fail("verdict %r disagrees with the rows (%s)" % (d.get("verdict"), want))
print("  live CodeSha256 %s matches; %d accounts; reader_shape %s; %d readers; verdict %s" % (
    live[:12], len(accts), d["reader_shape"], len(readers), want))
print("P27-3-AC1 PASS")
