"""ADVI_PERFRP PRF-b-3 / PRFR2DS-AC2 arms.

AC2: Sum(class MV) == level MV; drift(as-of, as-of) == 0; the residue NAMED, never
folded. Each arm states what a FAIL would mean.

The Sum-check is recomputed HERE from the emitted payload (a different traversal from
the emitter's own groupby), and separately against the raw positions partition, so the
identity is not simply the emitter agreeing with itself.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/runners_49f"))
EMIT = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"
# The as-of is READ FROM THE PAYLOAD, never typed here. A hardcoded date beside a
# derived one goes stale the moment the emission moves, and then the tie-out arm
# silently compares the payload against a DIFFERENT day's positions -- which fails
# loudly if you are lucky and passes wrongly if the totals happen to be close.
MV = "market_value_settled_unsettled"
FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


rel = json.load(open(EMIT / "perfrp_allocation_relationship.json", encoding="utf-8"))
acct = json.load(open(EMIT / "perfrp_allocation_account.json", encoding="utf-8"))

print("=" * 78)
print("ARM 1 -- the two grains are DIFFERENT payloads (round 1's `level` was unused)")
print("=" * 78)
check("relationship and account entry counts differ",
      len(rel["entries"]) != len(acct["entries"]),
      "%d vs %d" % (len(rel["entries"]), len(acct["entries"])))
check("both carry per-key classes", bool(rel["entries"][0]["classes"])
      and bool(acct["entries"][0]["classes"]))
check("each class row carries BOTH shares, never one",
      all("allocation_of_level" in c and "allocation_of_total" in c
          for e in rel["entries"] for c in e["classes"]))

print("=" * 78)
print("ARM 2 -- AC2: Sum(class MV) == level MV, recomputed from the payload")
print("=" * 78)
for label, doc in (("relationship", rel), ("account", acct)):
    worst, worst_key = 0.0, None
    for e in doc["entries"]:
        s = sum(c["market_value"] for c in e["classes"])
        d = abs(s - e["market_value"])
        if d > worst:
            worst, worst_key = d, e["key"]
    check("%s: max |Sum(class MV) - level MV|" % label, worst <= 0.01,
          "%.6f (worst key %s, %d keys)" % (worst, worst_key, len(doc["entries"])))

print("=" * 78)
print("ARM 3 -- and the level sums tie back to the RAW positions partition")
print("=" * 78)
S3 = boto3.client("s3")
ASOF = rel["allocation_as_of"]
check("both grains carry the SAME as_of", rel["allocation_as_of"] == acct["allocation_as_of"],
      "%s vs %s" % (rel["allocation_as_of"], acct["allocation_as_of"]))
print("  tie-out reads the positions partition for as_of %s (from the payload)" % ASOF)
o = S3.get_object(Bucket="opal-data-49financial",
                  Key="gold/advi/canonical/canonical_positions/date=%s/data.parquet" % ASOF)
pos = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
raw_total = float(pos[MV].sum())
for label, doc in (("relationship", rel), ("account", acct)):
    lvl = sum(e["market_value"] for e in doc["entries"])
    firm = doc["window"]["firm_market_value_total"]
    check("%s: level total == raw positions total" % label, abs(lvl - raw_total) <= 0.5,
          "level %.2f vs raw %.2f (delta %.4f)" % (lvl, raw_total, lvl - raw_total))
    check("%s: firm total == raw positions total" % label, abs(firm - raw_total) <= 0.5,
          "firm %.2f" % firm)
print("  ^ both grains partition the SAME dollars: a per-key breakdown that lost or")
print("    invented MV would separate from the raw partition here.")

print("=" * 78)
print("ARM 4 -- drift(as-of, as-of) == 0, and drift is NOT trivially zero")
print("=" * 78)
from perfrp_emit_core import allocation_drift  # noqa: E402

self_drift = allocation_drift(rel, rel)
mv_deltas = [c["market_value_delta"] for c in self_drift["classes"]]
sh_deltas = [c["share_delta"] for c in self_drift["classes"] if c["share_delta"] is not None]
check("drift(x, x): every class market_value_delta == 0", all(d == 0.0 for d in mv_deltas),
      "%d classes" % len(mv_deltas))
check("drift(x, x): every class share_delta == 0", all(d == 0.0 for d in sh_deltas))
check("drift(x, x): total_market_value_delta == 0",
      self_drift["total_market_value_delta"] == 0.0)
check("drift(x, x): every class present_in_both",
      all(c["present_in_both"] for c in self_drift["classes"]))

# NEGATIVE CONTROL. A drift function that returned zeros unconditionally would pass
# every check above. Perturb one class and require the drift to SEE it.
import copy  # noqa: E402

perturbed = copy.deepcopy(rel)
perturbed["classes"][0]["market_value"] += 1000.0
d2 = allocation_drift(rel, perturbed)
moved = [c for c in d2["classes"] if c["market_value_delta"] != 0.0]
check("NEGATIVE CONTROL: a 1,000 perturbation IS detected", len(moved) == 1,
      "%d class(es) moved, delta %.2f" % (len(moved), moved[0]["market_value_delta"] if moved else 0))
check("NEGATIVE CONTROL: total delta reflects it", d2["total_market_value_delta"] == 1000.0,
      "%.2f" % d2["total_market_value_delta"])
# A class present on ONE side only must not read as a 0.0 share move.
dropped = copy.deepcopy(rel)
gone = dropped["classes"].pop()
d3 = allocation_drift(rel, dropped)
row = [c for c in d3["classes"] if c["asset_class"] == gone["asset_class"]][0]
check("a DISAPPEARING class is flagged present_in_both=False, share_delta=None",
      row["present_in_both"] is False and row["share_delta"] is None,
      "class %r" % gone["asset_class"])

print("=" * 78)
print("ARM 5 -- the residue is NAMED and NEVER FOLDED")
print("=" * 78)
names = [c["asset_class"] for c in rel["classes"]]
print("  firm-wide classes: %s" % names)
print("  residue declared : %s" % rel["residue_states_declared"])
print("  residue present  : %s" % rel["residue_states_present"])
check("at least one residue state is present and named", bool(rel["residue_states_present"]))
check("residue is NOT folded into a real asset class",
      all(n not in ("other", "Other", "unclassified", "OTHER") for n in names))
check("the two residue states are declared SEPARATELY (never one bucket)",
      len(rel["residue_states_declared"]) == 2, str(rel["residue_states_declared"]))
check("'To Be Classified' is NOT minted (it is BD prose, not a live a07 value)",
      "To Be Classified" not in names)
res_mv = sum(c["market_value"] for c in rel["classes"]
             if c["asset_class"] in rel["residue_states_declared"])
print("  residue MV: %.2f of %.2f (%.4f%%)"
      % (res_mv, rel["window"]["firm_market_value_total"],
         100.0 * res_mv / rel["window"]["firm_market_value_total"]))

print("=" * 78)
print("ARM 6 -- pins present, with the a07 vintage caveat carried")
print("=" * 78)
pins = rel["window"]["upstream_pins"]
for t, p in pins.items():
    print("  %-38s %s" % (t, p))
check("every pin carries the PAIR", all("max_last_modified_utc" in p and "n_partitions_read" in p
                                        for p in pins.values()))
check("a07's pin declares its vintage quality",
      "vintage_quality" in pins["dimensions/dim_asset_classification"])
check("allocation declares itself NOT period-keyed", rel["period_keyed"] is False)

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS")
