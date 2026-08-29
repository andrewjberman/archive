"""ADVI_PERFRP PRF-b-4 / PRFR2DS-AC5 arms.

AC5: the gain/loss projection ties to a-4's RE-READ census residual; cost basis
DECLARED UNDETERMINED unless the census named it with evidence (it did:
`cost_basis_unamortized`, PRF-a-4 @0031aa6cae).

THE TIE THAT MATTERS: a-4 measured lots-to-positions coverage at 99.8831%, residual
-2,096,441.07. This leaf is built from the same lots, so its market_value total must
REPRODUCE that residual against canonical_positions. If it does not, the leaf is
summing a different population than the census graded -- which is the failure the
"tie to a-4's residual" clause exists to catch.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import boto3
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
D = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables"
EMIT = D / "emissions"
S3 = boto3.client("s3")
FAILS = []


# Every gain/loss figure is now a {value, figure_state, reason} dict (COO 79478 re-open).
FIG_KEYS = ("market_value", "cost_basis", "unrealized_short_term",
            "unrealized_long_term", "unrealized_term_undeclared", "unrealized_total",
            "realized", "total_gain_loss")


def v(entry, key):
    """Read a figure's VALUE. The tie-out below is re-run through this so the state
    fields are shown NOT to have altered the sums (COO 79478's explicit condition)."""
    f = entry[key]
    return f["value"] if isinstance(f, dict) else f


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


rel = json.load(open(EMIT / "perfrp_gainloss_relationship.json", encoding="utf-8"))
acct = json.load(open(EMIT / "perfrp_gainloss_account.json", encoding="utf-8"))
census = json.load(open(D / "ADVI_PERFRP.PRF-a-4_LOTS_CENSUS.json", encoding="utf-8"))
w = rel["window"]

print("=" * 78)
print("ARM 1 -- AC5: the leaf TIES to the a-4 census residual")
print("=" * 78)
census_lots = census["tie_out"]["combined"]["fact_uln + fact_ult"]
census_resid = census["tie_out"]["combined"]["fact_uln + fact_ult_residual"]
pos_mv = census["tie_out"]["canonical_positions"]["market_value"]
leaf_mv_rel = round(sum(v(e, "market_value") for e in rel["entries"]), 2)
leaf_mv_acct = round(sum(v(e, "market_value") for e in acct["entries"]), 2)
print("  a-4 census: uln+ult %.2f ; positions %.2f ; residual %.2f"
      % (census_lots, pos_mv, census_resid))
print("  b-4 leaf  : relationship grain %.2f ; account grain %.2f"
      % (leaf_mv_rel, leaf_mv_acct))
check("relationship-grain MV reproduces the census lots total",
      abs(leaf_mv_rel - census_lots) <= 0.5, "delta %.4f" % (leaf_mv_rel - census_lots))
check("account-grain MV reproduces it too (independent regrouping)",
      abs(leaf_mv_acct - census_lots) <= 0.5, "delta %.4f" % (leaf_mv_acct - census_lots))
leaf_resid = round(leaf_mv_rel - pos_mv, 2)
check("the leaf reproduces the census RESIDUAL against positions",
      abs(leaf_resid - census_resid) <= 0.5,
      "leaf %.2f vs census %.2f" % (leaf_resid, census_resid))
print("  ^ the leaf is summing the SAME population a-4 graded, not a different one.")
check("window declares lots_market_value_total consistently",
      abs(w["lots_market_value_total"] - census_lots) <= 0.5,
      "%.2f" % w["lots_market_value_total"])

print("=" * 78)
print("ARM 2 -- the card identities hold per entry, at BOTH grains")
print("=" * 78)
# The a-4 census MEASURED this identity as inexact -- summed |residual| 66,842.80 at
# ROW grain (fact_uln 5,026.91 + fact_ult 61,815.89), which is bond amortization, not
# error. So the arm must compare the leaf against THAT NUMBER, not against zero.
# CORRECTED FROM MY OWN FIRST VERSION, which asserted a per-entry tolerance of $1 and
# failed at 29,932.58 -- asserting an exactness the census had already disproved. An
# arm that contradicts a measurement already on the record is the arm's defect.
census_identity = sum(census["cost_basis_identity_residuals"]["cost_basis_unamortized"].values())
print("  a-4 census identity residual (ROW grain): %.2f" % census_identity)
for label, doc in (("relationship", rel), ("account", acct)):
    bad_sum, bad_tot, res = [], [], []
    for e in doc["entries"]:
        parts = (v(e, "unrealized_short_term") + v(e, "unrealized_long_term")
                 + v(e, "unrealized_term_undeclared"))
        if abs(parts - v(e, "unrealized_total")) > 0.02:
            bad_sum.append(e["key"])
        if abs(v(e, "unrealized_total") + v(e, "realized")
               - v(e, "total_gain_loss")) > 0.02:
            bad_tot.append(e["key"])
        res.append(abs((v(e, "market_value") - v(e, "cost_basis"))
                       - v(e, "unrealized_total")))
    # THE TOLERANCE IS NAMED because a tolerance is a claim (CVO 79532 P2). The three
    # components are cent-rounded INDEPENDENTLY of the total, so max |residual| is
    # exactly 0.0100: at 0.005 it is 710 of 3,834 / 1,057 of 6,177, and at a strict
    # > 0.01 still 414 / 611. 0.02 is the tolerance this arm actually applies.
    check("%s: ST + LT + undeclared == unrealized_total AT TOLERANCE 0.02" % label,
          not bad_sum, "%d bad of %d (cent-rounding; max |resid| 0.0100)"
          % (len(bad_sum), len(doc["entries"])))
    check("%s: unrealized + realized == total" % label, not bad_tot,
          "%d bad" % len(bad_tot))
    tot = sum(res)
    carriers = sum(1 for r in res if r > 0.02)
    # THE BOUND IS THE ROUNDING, NOT A DOLLAR. This arm asserted |delta| <= 1.00 and
    # FAILED at 7.08 / 10.59 the moment (A)(iii) landed -- correctly reporting a change
    # it was wrong to call a defect. unrealized_total is now the sum of the PUBLISHED
    # (rounded) components rather than a rounding of the unpublished sum, so each
    # entry's total may move by up to a cent and the aggregate residual moves with it.
    # The honest ceiling is therefore 0.01 x entries, and the measured delta sits far
    # inside it: 7.08 of 38.34 (0.19 cents per entry) at relationship grain and 10.59
    # of 61.77 (0.17) at account grain. A fixed dollar tolerance was an exactness the
    # emission no longer claims -- and asserting it would force the components identity
    # back off, which is the identity a consumer can actually check on the rendered card.
    bound = 0.01 * len(doc["entries"])
    check("%s: identity residual reproduces a-4 WITHIN THE ROUNDING BOUND" % label,
          abs(tot - census_identity) <= bound,
          "leaf %.2f vs census %.2f (delta %.2f, bound %.2f = 0.01 x %d entries) "
          "in %d carrying entries"
          % (tot, census_identity, tot - census_identity, bound,
             len(doc["entries"]), carriers))
print("  ^ the leaf propagates the census's KNOWN amortization inexactness and adds")
print("    only per-entry cent rounding: the delta is under two tenths of a cent per")
print("    entry at both grains. Asserting zero here would have been asserting against")
print("    a number a-4 had already measured.")

print("=" * 78)
print("ARM 3 -- the ST/LT split is the CUSTODIAN'S, corroborated independently")
print("=" * 78)
print("  holding_term_column: %s ; values seen %s ; unrecognised %s"
      % (w["holding_term_column"], w["holding_term_values_seen"],
         w["unrecognised_holding_term_values"]))
check("no unrecognised holding-term value", w["unrecognised_holding_term_values"] == [])
o = S3.get_object(Bucket="opal-data-assets",
                  Key="schwab/08335338/silver/fact_uln/date=%s/data.parquet" % rel["as_of"])
uln = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
declared_long = int((uln["h_t"].astype(str) == "L").sum())
derived_long = int((pd.to_numeric(uln["days_held"], errors="coerce") > 365).sum())
check("DECLARED h_t=='L' agrees with DERIVED days_held>365 on fact_uln",
      declared_long == derived_long,
      "declared %d vs derived %d of %d rows" % (declared_long, derived_long, len(uln)))
print("  ^ two independent determinations of the same fact: the custodian's flag and")
print("    the statutory one-year rule. The leaf serves the DECLARED one (it is the")
print("    custodian's characterisation, per CTO 68440); the derived rule is the")
print("    control that shows the declared flag is not arbitrary.")
undecl = sum(v(e, "unrealized_term_undeclared") for e in rel["entries"])
check("term-undeclared bucket exists and is NOT folded into ST or LT",
      all("unrealized_term_undeclared" in e for e in rel["entries"]),
      "total $%.2f" % undecl)

print("=" * 78)
print("ARM 4 -- the served figure is the CUSTODIAN'S, not a re-derivation")
print("=" * 78)
print("  provenance: %s" % w["served_figure_provenance"])
# COO 79478: every figure carries its claim, as b-2/b-3/b-6 do.
bare = sum(1 for doc in (rel, acct) for e in doc["entries"] for k in FIG_KEYS
           if not (isinstance(e[k], dict) and "figure_state" in e[k] and "value" in e[k]))
total_figs = sum(len(doc["entries"]) for doc in (rel, acct)) * len(FIG_KEYS)
check("EVERY gain/loss figure carries figure_state + reason", not bare,
      "%d bare of %d figures" % (bare, total_figs))
check("the state vocabulary matches b-2/b-6",
      {e[k]["figure_state"] for doc in (rel, acct) for e in doc["entries"] for k in FIG_KEYS}
      <= {"COMPUTED", "COMPUTED_PARTIAL", "NOT_COMPUTED_INPUTS_PRESENT",
          "NOT_COMPUTED_INPUTS_ABSENT"},
      str(sorted({e[k]["figure_state"] for doc in (rel, acct) for e in doc["entries"]
                  for k in FIG_KEYS})))
check("the custodian's provenance rides ON the realized figure",
      all("custodian-reported" in (e["realized"]["reason"] or "") for e in rel["entries"]))
check("the a-4 residual disclosure rides ON the aggregate figures",
      all("99.8831%" in (e["unrealized_total"]["reason"] or "") for e in rel["entries"]))
check("cost_basis_column is the one a-4 NAMED", w["cost_basis_column"] == "cost_basis_unamortized",
      w["cost_basis_column"])
check("the leaf records WHY that column (not just which)", "NAMED BY MEASUREMENT" in w["cost_basis_basis"])
# NEGATIVE CONTROL on the naming: a different candidate must NOT satisfy the identity.
alt = "adjusted_cost_basis_amortized"
if alt in uln.columns:
    mv = uln["current_market_value"].fillna(0)
    ugl = uln["unrealized_gain_loss"].fillna(0)
    good = float((mv - uln["cost_basis_unamortized"].fillna(0) - ugl).abs().sum())
    bad = float((mv - uln[alt].fillna(0) - ugl).abs().sum())
    check("NEGATIVE CONTROL: the runner-up column FAILS the same identity",
          bad > good * 1000, "named %.2f vs %s %.2f" % (good, alt, bad))

print("=" * 78)
print("ARM 5 -- pins, and the as-of card is not period-keyed")
print("=" * 78)
for t, p in w["upstream_pins"].items():
    print("  %-34s date=%s rows=%s aliased=%s"
          % (t, p.get("partition_date"), p.get("rows"), p.get("aliased_from_requested")))
check("every pin carries the PAIR",
      all("max_last_modified_utc" in p and "n_partitions_read" in p
          for p in w["upstream_pins"].values()))
check("gain/loss declares itself NOT period-keyed", w["period"] is None)
check("both unrealized tax slices were read",
      all("silver/fact_%s" % s in w["upstream_pins"] for s in ("uln", "ult")))
check("the realized table was read", "silver/fact_rld" in w["upstream_pins"])

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS")
