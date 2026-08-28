"""PRF-b-2 / PRFR2DS-AC1 ORACLE v2 -- corrected arms + an extreme-value census.

TWO ARMS WERE WRONG IN v1 AND ARE CORRECTED HERE. Recorded rather than silently
rewritten, because an arm that is quietly re-tuned until it passes is not an arm:

  v1 ARM "mutant differs on EVERY computable account"  -> FAILED 125 of 4070.
     WRONG BY CONSTRUCTION. sum(r) and PROD(1+r)-1 are the SAME NUMBER whenever the
     series has AT MOST ONE non-zero return: every (1+0) factor is the multiplicative
     identity. Measured: all 125 collisions are that case (11 single-day, 93 all-zero,
     21 exactly-one-non-zero -- the last confirmed by a relative-tolerance re-read at
     1e-12, where all 21 agree EXACTLY). The corrected arm scopes to the population
     where the laws CAN differ.

  v1 ARM "no refused account renders 0.0"              -> FAILED on 55.
     WRONG SUBJECT. It selected accounts having ANY zero-BMV refused day, then flagged
     a 0.0 window value -- but such an account can refuse on some days and COMPUTE on
     others. All 95 zero-valued entries are COMPUTED_PARTIAL whose every present daily
     return is genuinely 0.0 (a flat account, correctly 0.00%). The hazard the arm
     MEANT to test is "a NOT_COMPUTED entry carrying a value", measured at 0.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq

# Workspace root is DERIVED, never hardcoded (CLAUDE.md: derive, do not hardcode --
# a baked absolute path makes an artifact device-specific and it dies on the next box).
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path.insert(0, str(ROOT))
from lib.trading_calendar import trading_days_between  # noqa: E402

EMIT = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"
S3 = boto3.client("s3")
FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


dates = trading_days_between("2024-07-08", "2024-11-07")
per_acct, per_status, fb = {}, {}, 0
for d in dates:
    o = S3.get_object(Bucket="opal-data-49financial",
                      Key="gold/advi/canonical/twr_daily/date=%s/data.parquet" % d.isoformat())
    df = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
    fb += 1 if "flow_boundary" in df.columns else 0
    for acct, r, st in zip(df["account_id"].astype(str), df["r_net"], df["status"].astype(str)):
        per_acct.setdefault(acct, []).append(None if r != r else r)
        if r != r:
            per_status.setdefault(acct, []).append(st)

emitted = json.load(open(EMIT / "perfrp_performance_account.json", encoding="utf-8"))
by_key = {e["key"]: e for e in emitted["entries"]}

print("=" * 78)
print("ARM A -- VINTAGE (discriminating, not self-reported)")
print("=" * 78)
check("flow_boundary in ALL window partitions", fb == len(dates), "%d of %d" % (fb, len(dates)))
check("emitted twr pin n_partitions_read == window length",
      emitted["window"]["upstream_pins"]["canonical/twr_daily"]["n_partitions_read"] == len(dates),
      "%s vs %d" % (emitted["window"]["upstream_pins"]["canonical/twr_daily"]["n_partitions_read"],
                    len(dates)))
check("zero partitions absent",
      emitted["window"]["upstream_pins"]["canonical/twr_daily"]["partitions_absent"] == [])

print("=" * 78)
print("ARM B -- AC1: window %% == PROD(1+r_net)-1, recomputed independently")
print("=" * 78)
worst, worst_key, compared = 0.0, None, 0
for a, s in per_acct.items():
    e = by_key.get(a)
    if not e or e.get("window_return") is None:
        continue
    present = [v for v in s if v is not None]
    prod = 1.0
    for v in present:
        prod *= (1 + v)
    d = abs((prod - 1.0) - e["window_return"])
    if d > worst:
        worst, worst_key = d, a
    compared += 1
    if e.get("days_present") != len(present):
        check("days_present matches (%s)" % a, False)
        break
check("recomputed == emitted on all %d computable accounts" % compared, worst == 0.0,
      "max|delta| = %.3e" % worst)
check("denominator non-trivial", compared > 1000, "%d accounts" % compared)

print("=" * 78)
print("ARM B2 -- the MUTANT, scoped to where the two laws CAN differ")
print("=" * 78)
can_differ, mutant_caught, collide = 0, 0, []
for a, s in per_acct.items():
    e = by_key.get(a)
    if not e or e.get("window_return") is None:
        continue
    present = [v for v in s if v is not None]
    nonzero = [v for v in present if abs(v) > 1e-15]
    if len(nonzero) < 2:
        continue          # laws are mathematically identical here -- not a test site
    can_differ += 1
    prod = 1.0
    for v in present:
        prod *= (1 + v)
    law, mut = prod - 1.0, sum(present)
    # EXACT inequality, not a tolerance. A tolerance here measures RETURN MAGNITUDE,
    # not law equivalence: law - mutant is the sum of cross-products, so on an account
    # whose second non-zero return is ~1e-13 the gap is ~1e-14 -- real, analytically
    # predicted, and 1000 ULP wide, yet it sits under any relative epsilon loose enough
    # to be worth writing. A v2 relative test at 1e-12 mis-scored exactly 2 accounts
    # this way; both were re-read individually and their gap matched the predicted
    # r1*r2 to three significant figures. The laws differ or they do not.
    if law != mut:
        mutant_caught += 1
    else:
        collide.append(a)
check("mutant is DISTINGUISHED on every account where the laws differ",
      mutant_caught == can_differ, "%d of %d (collisions %d)"
      % (mutant_caught, can_differ, len(collide)))
check("that population is large", can_differ > 1000, "%d accounts" % can_differ)
excluded = compared - can_differ
print("  EXCLUDED as non-test-sites (<2 non-zero returns): %d of %d compared."
      % (excluded, compared))
print("  Excluded because the laws AGREE there by identity, not because they pass.")

print("=" * 78)
print("ARM C -- refusals never become numbers")
print("=" * 78)
dangerous = [a for a in by_key if by_key[a]["figure_state"].startswith("NOT_COMPUTED")
             and by_key[a].get("window_return") is not None]
check("NO NOT_COMPUTED entry carries a value", not dangerous, "%d found" % len(dangerous))
zero_val = [a for a in by_key if by_key[a].get("window_return") == 0.0]
genuine = [a for a in zero_val
           if all(abs(v) < 1e-15 for v in per_acct.get(a, []) if v is not None)]
check("every 0.0 window value is a genuinely FLAT account",
      len(zero_val) == len(genuine), "%d of %d" % (len(genuine), len(zero_val)))
zb = [a for a, st in per_status.items() if st and set(st) <= {"UNCOMPUTABLE-ZERO-BMV"}]
check("zero-BMV population exists and is flagged", len(zb) > 0, "%d accounts" % len(zb))

print("=" * 78)
print("ARM D -- the status split is carried (round 1 could emit only one member)")
print("=" * 78)
c = emitted["figure_state_census"]
check("both NOT_COMPUTED reasons present", c.get("NOT_COMPUTED_INPUTS_PRESENT", 0) > 0
      and c.get("NOT_COMPUTED_INPUTS_ABSENT", 0) > 0, str(c))
check("no unrecognised upstream status", emitted["window"]["unrecognised_upstream_status"] == {},
      str(emitted["window"]["unrecognised_upstream_status"]))

print("=" * 78)
print("CENSUS E -- EXTREME DAILY RETURNS (not an arm: a QUALITY OBSERVATION)")
print("=" * 78)
allr = [v for s in per_acct.values() for v in s if v is not None]
allr_sorted = sorted(allr, key=abs, reverse=True)
buckets = [(1.0, ">=100%"), (0.5, ">=50%"), (0.2, ">=20%")]
print("  daily r_net observations in window: %d" % len(allr))
for t, lbl in buckets:
    n = sum(1 for v in allr if abs(v) >= t)
    print("    |r_net| %-8s : %6d  (%.4f%% of observations)" % (lbl, n, 100.0 * n / len(allr)))
print("  largest 8 |r_net|: %s" % ", ".join("%.2f" % v for v in allr_sorted[:8]))
big_win = [(a, e["window_return"]) for a, e in by_key.items()
           if e.get("window_return") is not None and abs(e["window_return"]) >= 1.0]
print("  accounts whose WINDOW return |r| >= 100%%: %d of %d computable"
      % (len(big_win), compared))
print("  A 5196%% single-day return is a denominator artifact shape (tiny BMV), not a")
print("  return. NOT THIS TO'S LANE -- twr_daily is the campaign's artifact. Surfaced.")

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS")
