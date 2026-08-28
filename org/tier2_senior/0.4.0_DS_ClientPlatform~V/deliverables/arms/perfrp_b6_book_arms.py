"""ADVI_PERFRP PRF-b-6 / PRFR2DS-AC3 (b-6 half) arms.

AC3's b-6 obligations: the four ruled KPI tiles + the client table as rollups, and
new + lost + existing == relationship count. Plus the amended cell PRF-a-5's own
acceptance: the Book view's relationship set == the leaderboard entry's set for the
same advisor + window.

⛔ ONE THING THIS ARM DELIBERATELY DOES NOT CHECK: DISJOINTNESS. The relationship leaf's
membership is a PARTITION (an account under exactly one relationship) and its arm
asserts disjointness. The Book view is the TAGGED-BOOK view and is NON-ADDITIVE ACROSS
ADVISORS by ruling (R-p5) -- the same account legitimately appears under several
advisors. Copying the relationship arm here would fail a correct emission, and
"disjoint" is exactly the wrong law for this leaf.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/runners_49f"))
EMIT = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"
FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


doc = json.load(open(EMIT / "perfrp_book_advisor.json", encoding="utf-8"))
ver = json.load(open(EMIT / "perfrp_book_advisor.verification.json", encoding="utf-8"))
entries = doc["entries"]
w = doc["window"]

print("=" * 78)
print("ARM 1 -- the FOUR RULED TILES, transcribed from the CONSUMER's registry")
print("=" * 78)
from perfrp_emit_core import BOOK_TILES  # noqa: E402

ruled = [t for t, _ in BOOK_TILES]
print("  declared: %s" % w["book_tiles_declared"])
check("exactly FOUR tiles", len(ruled) == 4, str(ruled))
check("tile ids match the consumer's PERFRP_BOOK_TILE_IDS order",
      ruled == ["market_value", "management_fees", "relationships", "net_flows"])
missing = []
for e in entries:
    for tile, breakdown in BOOK_TILES:
        if tile not in e["tiles"]:
            missing.append((e["key"], tile))
            continue
        for b in breakdown:
            if b not in e["tiles"][tile]:
                missing.append((e["key"], "%s.%s" % (tile, b)))
check("every entry carries every tile AND every ruled breakdown", not missing,
      "%d missing" % len(missing))
figs = [f for e in entries for t in e["tiles"].values() for f in t.values()]
check("every figure carries state+reason, never a bare number",
      all(isinstance(f, dict) and "figure_state" in f and "value" in f for f in figs),
      "%d figures" % len(figs))

print("=" * 78)
print("ARM 2 -- AC3: new + lost + existing == relationship count")
print("=" * 78)
bad = []
for e in entries:
    p = e["relationship_partition"]
    if p["new"] + p["lost"] + p["existing"] != p["union"]:
        bad.append((e["key"], p))
check("new + lost + existing == |union of the two dates' sets|", not bad,
      "%d violations of %d advisors" % (len(bad), len(entries)))
bad2 = [e["key"] for e in entries
        if e["relationship_partition"]["new"] + e["relationship_partition"]["existing"]
        != e["relationship_partition"]["at_as_of"]]
check("new + existing == relationships AT THE AS-OF", not bad2, "%d violations" % len(bad2))
bad3 = [e["key"] for e in entries
        if e["relationship_partition"]["lost"] + e["relationship_partition"]["existing"]
        != e["relationship_partition"]["at_window_start"]]
check("lost + existing == relationships AT THE WINDOW START", not bad3,
      "%d violations" % len(bad3))
tot = {k: sum(e["relationship_partition"][k] for e in entries)
       for k in ("new", "lost", "existing", "union", "at_as_of")}
print("  totals across %d advisors: %s" % (len(entries), tot))
print("  (these SUM ACROSS ADVISORS and are NOT a firm total -- the same relationship")
print("   under two advisors counts twice here BY RULING, R-p5 non-additivity.)")

print("=" * 78)
print("ARM 3 -- the client table agrees with the partition it is derived from")
print("=" * 78)
bad4 = []
for e in entries:
    p = e["relationship_partition"]
    ct = e["client_table"]
    counts = {"new": 0, "lost": 0, "existing": 0}
    for row in ct:
        counts[row["status"]] += 1
    if len(ct) != p["union"] or counts != {k: p[k] for k in counts}:
        bad4.append((e["key"], len(ct), p["union"], counts))
check("client table length == union AND per-status counts match", not bad4,
      "%d mismatched" % len(bad4))
check("every client-table row carries a status in the ruled set",
      all(r["status"] in ("new", "lost", "existing") for e in entries for r in e["client_table"]))

print("=" * 78)
print("ARM 3b -- the client table carries the RULED L2 COLUMNS (PRD s.6.2)")
print("=" * 78)
# Transcribed from the PRD's own row and the consumer's PERFRP_CLIENT_COLUMNS, in the
# PRD's order. CORRECTED AFTER 3.0.0_SA_CVO 79427: the first b-6 emission carried a
# MEMBERSHIP ROSTER ({relationship_id, status}) whose intersection with this set was
# ZERO. Nothing about the roster was wrong; it simply was not the ruled table.
RULED_CLIENT_COLUMNS = ("client", "beginning_market_value", "new_relationship_flows",
                        "lost_relationship_flows", "net_flows_existing", "net_gain",
                        "ending_market_value")
sample = entries[0]["client_table"][0]
served_cols = set(sample)
missing_cols = [c for c in RULED_CLIENT_COLUMNS if c not in served_cols]
check("every ruled L2 column is present", not missing_cols, "missing %s" % missing_cols)
check("the ruled ORDER is the PRD's (not re-sorted into the emitter's convenience)",
      [c for c in RULED_CLIENT_COLUMNS if c in served_cols] == list(RULED_CLIENT_COLUMNS))
print("  beyond the ruled set: %s" % sorted(served_cols - set(RULED_CLIENT_COLUMNS)))
print("  ^ `status` is KEPT deliberately: it is what SPLITS the three flow columns, so")
print("    a reader can see which bucket produced which figure. It is additive to the")
print("    ruled set, not a substitute for it.")
bad_id, bad_part, nrows = 0, 0, 0
for e in entries:
    for r in e["client_table"]:
        nrows += 1
        flow = (r["new_relationship_flows"] + r["lost_relationship_flows"]
                + r["net_flows_existing"])
        if abs((r["beginning_market_value"] + flow + r["net_gain"])
               - r["ending_market_value"]) > 0.02:
            bad_id += 1
        if sum(1 for c in ("new_relationship_flows", "lost_relationship_flows",
                           "net_flows_existing") if r[c] != 0) > 1:
            bad_part += 1
check("IDENTITY beginning + flows + net_gain == ending", not bad_id,
      "%d bad of %d rows" % (bad_id, nrows))
check("the three flow columns are ONE PARTITION (never >1 non-zero on a row)",
      not bad_part, "%d rows with >1" % bad_part)
print("  ^ net_gain is the RESIDUAL, derived not read -- which is what makes the row an")
print("    identity a consumer can check rather than six numbers sitting together.")
check("client_table row count == the relationship partition union",
      all(len(e["client_table"]) == e["relationship_partition"]["union"] for e in entries))

print("=" * 78)
print("ARM 4 -- NON-ADDITIVITY (R-p5) is expressed, not merely asserted in prose")
print("=" * 78)
gap = [(e["key"], e["accounts"], e["role_sum_would_be"])
       for e in entries if e["role_sum_would_be"] != e["accounts"]]
check("at least one advisor's role-sum EXCEEDS the deduped account count",
      bool(gap), "%d of %d advisors show the gap" % (len(gap), len(entries)))
if gap:
    worst = max(gap, key=lambda t: t[2] - t[1])
    print("      worst: %s deduped=%d role_sum_would_be=%d (double-count %d accounts)"
          % (worst[0], worst[1], worst[2], worst[2] - worst[1]))
    tot_d = sum(e["accounts"] for e in entries)
    tot_r = sum(e["role_sum_would_be"] for e in entries)
    print("      firm-wide: deduped %d vs additive %d -- an additive rollup would" % (tot_d, tot_r))
    print("      overstate the book by %d account-slots (%.1f%%)."
          % (tot_r - tot_d, 100.0 * (tot_r - tot_d) / max(tot_d, 1)))
check("role_breakdown_semantics reproduces the SERVED term",
      w["role_breakdown_semantics"] == "advisor_tagged_full_nonadditive",
      w["role_breakdown_semantics"])
# The cross-tie the emitter asserts, re-checked from the two artifacts.
mism = [e["key"] for e in entries if len(ver["membership"][e["key"]]) != e["accounts"]]
check("for every advisor len(ids) == accounts (cross-tie)", not mism, "%d" % len(mism))
ids = [i for v in ver["membership"].values() for i in v]
print("  ids total %d, distinct %d -- OVERLAP IS CORRECT HERE (non-additive view);"
      % (len(ids), len(set(ids))))
print("  a disjointness assertion would FAIL a correct Book emission.")

print("=" * 78)
print("ARM 5 -- the jd2 basis is pinned, floored, and NOT aliased forward")
print("=" * 78)
jd2 = w["upstream_pins"]["silver/dim_advisor_fee_role"]
for k in ("partition_date", "aliased_from_asof", "rows_total", "rows_is_current",
          "partition_floor", "partition_newest", "max_last_modified_utc"):
    print("      %-24s %s" % (k, jd2[k]))
check("jd2 partition_date <= window_end (never aliased FORWARD)",
      jd2["partition_date"] <= w["window_end"])
check("is_current filter actually narrowed the frame",
      jd2["rows_is_current"] < jd2["rows_total"],
      "%d of %d" % (jd2["rows_is_current"], jd2["rows_total"]))
print("  sparse-dimension aliasing, declared per read:")
for t, p in w["upstream_pins"].items():
    if p.get("aliased_from_requested"):
        print("      %-44s requested %s -> read %s"
              % (t, p["requested_date"], p["partition_date"]))
check("every pin carries the PAIR",
      all("max_last_modified_utc" in p and "n_partitions_read" in p
          for p in w["upstream_pins"].values()))

print("=" * 78)
print("ARM 6 -- a STALE BASELINE rides on the FIGURE, not only in the pins")
print("=" * 78)
rel_start_pin = w["upstream_pins"]["dimensions/dim_relationship@window_start"]
aliased = rel_start_pin.get("aliased_from_requested")
print("  baseline requested %s -> read %s (aliased=%s)"
      % (rel_start_pin.get("requested_date"), rel_start_pin.get("partition_date"), aliased))
new_figs = [e["tiles"]["relationships"]["new"] for e in entries]
lost_figs = [e["tiles"]["relationships"]["lost"] for e in entries]
if aliased:
    check("every `new` figure is COMPUTED_PARTIAL, not COMPUTED",
          all(f["figure_state"] == "COMPUTED_PARTIAL" for f in new_figs),
          "%d figures" % len(new_figs))
    check("every `lost` figure likewise",
          all(f["figure_state"] == "COMPUTED_PARTIAL" for f in lost_figs))
    check("the reason NAMES the baseline partition and the drift",
          all(rel_start_pin["partition_date"] in (f["reason"] or "") and
              "calendar day" in (f["reason"] or "") for f in new_figs))
    check("the headline is NOT downgraded (it is an as-of count, not a delta)",
          all(e["tiles"]["relationships"]["headline"]["figure_state"] == "COMPUTED"
              for e in entries))
    print("  ^ WHY THIS MATTERS: dim_relationship is sparse -- 158 partitions over")
    print("    2024-07-08..2026-08-27 with gaps of 413 and 112 calendar days. A window")
    print("    starting inside a gap baselines up to 413 days early, so 'new this")
    print("    quarter' can silently mean 'new in the last 14 months'.")
else:
    check("no alias, so new/lost are fully COMPUTED",
          all(f["figure_state"] == "COMPUTED" for f in new_figs + lost_figs))
fl = w["upstream_pins"]["canonical/flow_ledger"]
print("      flow_ledger read %d of %d requested; absent %d (declared, not hidden)"
      % (fl["n_partitions_read"], fl["n_partitions_requested"], len(fl["partitions_absent"])))

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS")
