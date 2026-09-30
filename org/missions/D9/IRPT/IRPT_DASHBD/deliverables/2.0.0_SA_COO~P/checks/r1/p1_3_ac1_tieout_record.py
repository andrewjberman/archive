"""IRPT_DASHBD round 1 AC (DB-b-3, FWD-8 / ADDENDUM ruling 11 / C-TIEOUT / C-FLOWTIME) -- the tie-out MEASUREMENT exists, was read
from the LANDED Black Diamond pulls only, and proposes the tolerance and the flow-timing winner.

Usage: python p1_3_ac1_tieout_record.py <worktree root>
Reads org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.json:
  vendor_calls == 0; oracle_keys: >= 1, every key under blackdiamond/49f/bronze/reporting_performance/ and each HeadObject 200;
  periods: >= 5 rows, each with account, bd_account, start, end, bd_twr, opal_twr_start, opal_twr_end, opal_twr_mid, abs_diff (of
  the END convention unless winner says otherwise) and reasons (list, may be empty when abs_diff <= proposed tolerance);
  summary: median, p90, max over abs_diff (recomputed here and compared, 1e-12); proposed_tieout_tolerance: a number > 0;
  flow_convention_winner in {START, END, MIDPOINT} with per-convention summary present.
Pass line: DB-3-AC1 PASS. Base (at the cut): FAIL -- no record.
"""
import json
import statistics
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REC = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.json"
ORACLE_PREFIX = "blackdiamond/49f/bronze/reporting_performance/"


def fail(msg):
    print("DB-3-AC1 FAIL: " + msg)
    sys.exit(1)


if not REC.exists():
    fail("record absent: %s" % REC)
d = json.loads(REC.read_text(encoding="utf-8"))
if int(d.get("vendor_calls", -1)) != 0:
    fail("vendor_calls = %r (must be 0: the oracle is the landed bronze)" % d.get("vendor_calls"))
keys = d.get("oracle_keys") or []
if not keys or any(not k.startswith(ORACLE_PREFIX) for k in keys):
    fail("oracle_keys empty or outside %s" % ORACLE_PREFIX)
import boto3  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")
for k in keys:
    try:
        s3.head_object(Bucket="opal-data-assets", Key=k)
    except Exception as exc:  # noqa: BLE001
        fail("oracle key not readable: %s (%s)" % (k, str(exc)[:80]))
periods = d.get("periods") or []
if len(periods) < 5:
    fail("only %d periods (need >= 5)" % len(periods))
need = {"account", "bd_account", "start", "end", "bd_twr", "opal_twr_start", "opal_twr_end", "opal_twr_mid", "abs_diff", "reasons"}
for p in periods:
    miss = need - set(p)
    if miss:
        fail("period row lacks %s: %r" % (sorted(miss), p))
diffs = sorted(float(p["abs_diff"]) for p in periods)
med = statistics.median(diffs)
p90 = diffs[min(len(diffs) - 1, int(round(0.9 * (len(diffs) - 1))))]
mx = diffs[-1]
s = d.get("summary") or {}
for name, val in (("median", med), ("p90", p90), ("max", mx)):
    if name not in s or abs(float(s[name]) - val) > 1e-12:
        fail("summary.%s %r != recomputed %.12g" % (name, s.get(name), val))
tol = d.get("proposed_tieout_tolerance")
if not isinstance(tol, (int, float)) or tol <= 0:
    fail("proposed_tieout_tolerance %r is not a positive number" % tol)
win = d.get("flow_convention_winner")
if win not in ("START", "END", "MIDPOINT"):
    fail("flow_convention_winner %r" % win)
per = d.get("per_convention_summary") or {}
if not all(c in per for c in ("START", "END", "MIDPOINT")):
    fail("per_convention_summary lacks a convention")
print("  periods %d over %d oracle keys; median %.6g p90 %.6g max %.6g; proposed tolerance %s; winner %s" % (len(periods), len(keys), med, p90, mx, tol, win))
print("DB-3-AC1 PASS")
