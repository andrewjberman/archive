"""INSR1DS-AC3 / INS-c-3 -- the forbidden-field census.

The criterion: the insurance snapshot plane carries NO analytics, NO returns, NO
series. A snapshot plane that grows a series has become an asset-management
calculation, which INS-inv-1 forbids.

WHY THIS IS A PREDICATE AND NOT A PROSE PROMISE: the gold table does not exist
yet (0 insurance keys over 480,954 walked). A promise not to add analytics fields
is unfalsifiable; a runnable census is not. This runs against the DESIGNED column
set today and against the LIVE parquet the day it exists -- same predicate, so the
design cannot drift from the check.

TWO HAZARDS THIS FILE IS BUILT AGAINST, both measured in this estate:
  1. SUBSTRING OVERCOUNT. A case-insensitive 'egress' returned 19 hits in this
     estate, all of them 'regression'. So every token here is matched on WORD
     BOUNDARIES over a snake_case split, never as a bare substring, and every hit
     is PRINTED for reading -- a count nobody reads is a count of the pattern's
     accidents.
  2. A CONTROL THAT CANNOT FAIL. A census that returns 0 on a clean schema proves
     nothing unless it can return >0. run_controls() feeds it a schema that MUST
     trip, and the module refuses to report a PASS if that control comes back clean.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# THE FORBIDDEN SET -- a Rule 24 enumeration act, four postulates stated.
#
# AXIS INTENT (one, and only one): "does this column carry a DERIVED
#   ASSET-MANAGEMENT QUANTITY, or a TIME AXIS WIDER THAN THIS ROW'S SNAPSHOT?"
#   It does NOT mix in sensitivity, ownership, or vendor provenance -- those are
#   different axes and belong to different checks.
# GRAIN: every value is a COLUMN-NAME TOKEN. No value is a table-level or
#   row-level property, so nothing sits at a different grain from its siblings.
# MECE: the three groups below are disjoint by construction (a token appears in
#   exactly one) and are collectively exhaustive OVER THE DECLARED AXIS -- the
#   axis is derived-AM-quantity-or-wider-time-axis, and a column that is neither
#   is permitted by definition, which is what makes the axis exhaustive rather
#   than merely long.
# STATE COHERENCE: all three groups move together under ONE remedy -- delete the
#   column from the gold schema. There is no member here that a schema edit
#   cannot reach, so this axis carries no stability defect.
# ---------------------------------------------------------------------------

RETURNS_AND_PERFORMANCE = {
    "twr", "irr", "mwr", "return", "returns", "cagr", "yield", "ytd", "mtd",
    "qtd", "itd", "alpha", "beta", "sharpe", "sortino", "stddev", "volatility",
    "drawdown", "benchmark", "attribution", "pnl", "gain", "gains", "loss",
    "losses", "realized", "unrealized", "performance",
}

WIDER_TIME_AXIS = {
    "series", "history", "historical", "prior", "previous", "trailing",
    "rolling", "change", "delta", "growth", "since", "inception", "period",
    "cumulative", "annualized",
}

DERIVED_AGGREGATE = {
    "avg", "average", "mean", "median", "stdev", "variance", "percentile",
    "quartile", "rank", "weight", "weighted", "allocation", "pct", "ratio",
    "score", "index",
}

FORBIDDEN = {
    "returns_and_performance": RETURNS_AND_PERFORMANCE,
    "wider_time_axis": WIDER_TIME_AXIS,
    "derived_aggregate": DERIVED_AGGREGATE,
}

# as_of_date is the ONE permitted date and it is the row's own snapshot stamp, not
# a time axis. Named explicitly so the check cannot drift into flagging it.
PERMITTED_DATE_TOKENS = {"asof", "as", "of", "asofdate", "date", "ingested", "at"}


def _tokens(column: str) -> list[str]:
    """snake_case / camelCase -> lowercase word tokens. Word boundaries, never substrings."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", column)
    return [t for t in re.split(r"[^A-Za-z0-9]+", spaced.lower()) if t]


def census(columns: list[str]) -> dict:
    """Return every violation, WITH its denominator and the token that matched."""
    hits = []
    for col in columns:
        toks = set(_tokens(col))
        if toks and not (toks - PERMITTED_DATE_TOKENS):
            continue  # a pure date-stamp column
        for group, vocab in FORBIDDEN.items():
            matched = sorted(toks & vocab)
            if matched:
                hits.append({"column": col, "group": group, "matched_tokens": matched})
    return {
        "denominator_columns_scanned": len(columns),
        "violations": len(hits),
        "hits": hits,
        "verdict": "CLEAN" if not hits else "FORBIDDEN FIELDS PRESENT",
    }


def run_controls() -> bool:
    """A control that cannot fail is not a control. Both arms, reachable from
    DIFFERENT truths -- the negative arm must come back CLEAN and the positive
    arm must come back DIRTY, or this module has no standing to report anything."""
    neg = census(["bd_account_id", "account_id", "relationship_id", "bd_account_number",
                  "carrier", "product", "current_emv", "as_of_date", "spine_class"])
    pos = census(["bd_account_id", "twr_ytd", "nav_series", "avg_weight"])
    ok_neg = neg["violations"] == 0
    ok_pos = pos["violations"] >= 3
    print(f"  CONTROL neg (clean schema, must be 0):  {neg['violations']} -> {'OK' if ok_neg else 'FAILED'}")
    for h in neg["hits"]:
        print(f"      UNEXPECTED: {h['column']} -> {h['group']} {h['matched_tokens']}")
    print(f"  CONTROL pos (3 planted, must be >=3):   {pos['violations']} -> {'OK' if ok_pos else 'FAILED'}")
    for h in pos["hits"]:
        print(f"      planted hit: {h['column']:14s} {h['group']:24s} {h['matched_tokens']}")
    return ok_neg and ok_pos


# The DESIGNED gold schema for insurance_nav_current. Spine legs per COO ruling
# 70462: account / relationship / firm carried as REAL IDs; the ADVISOR leg is
# NOT-DERIVABLE-UPSTREAM and is deliberately ABSENT rather than name-joined --
# a name-string join across a 160,091-row dim is a silent-collision generator.
DESIGNED_SCHEMA = [
    "bd_account_id",          # BD-native, the source's own id
    "bd_account_number",
    "account_id",             # Opal 10-char, via JD2 bd_account_id -> account_id
    "relationship_id",        # via dim_relationship.account_id -> relationship_id
    "firm",                   # constant for this tree; carried, not derived
    "spine_class",            # linked | unassigned  (never dropped)
    "advisor_basis",          # literal 'NOT-DERIVABLE-UPSTREAM' + the reason
    "carrier",                # v1 characteristic -- field name UNVERIFIED, see note
    "product",                # v1 characteristic -- field name UNVERIFIED, see note
    "current_emv",            # the snapshot value
    "as_of_date",             # the ONE date: this row's statement stamp
    "source_pipeline",
    "schema_version",
    "_ingested_at",
]

if __name__ == "__main__":
    print("INSR1DS-AC3 -- forbidden-field census\n")
    print("CONTROLS (run FIRST -- a census nobody has seen fail proves nothing):")
    controls_ok = run_controls()
    print()
    if not controls_ok:
        print("REFUSING TO REPORT: the controls did not both hold. The instrument is not trustworthy.")
        raise SystemExit(2)

    r = census(DESIGNED_SCHEMA)
    print("DESIGNED SCHEMA CENSUS  (insurance_nav_current, as designed 2026-08-25)")
    print(f"  DENOMINATOR: {r['denominator_columns_scanned']} columns scanned")
    print(f"  VIOLATIONS : {r['violations']}")
    print(f"  VERDICT    : {r['verdict']}")
    for h in r["hits"]:
        print(f"     {h['column']} -> {h['group']} {h['matched_tokens']}")
    print()
    print("SCOPE, stated so this is not over-read: this censuses the DESIGNED column")
    print("set. It is a DESIGN-layer result, NOT an APPLIED one -- no insurance table")
    print("exists (0 keys over 480,954 walked). The same predicate re-runs against the")
    print("live parquet the day it lands; that run, not this one, is the APPLIED claim.")
    print()
    print("CARRIED FORWARD, unresolved and NOT hidden: 'carrier' and 'product' are")
    print("PRD s.11 #6's assumed field names. The populated insuranceCharacteristics")
    print("schema is UNKNOWN (one specimen, empty). INS-a-2's occupancy census resolves")
    print("them to real names or declares them ABSENT. I did not design around a guess")
    print("silently -- the guess is labelled here.")
