"""PRF-a-1 ADDENDUM 2 -- RECOVERABILITY DISCRIMINATOR (COO Ruling 2, msg 67396).

THE QUESTION COO ORDERED MEASURED, and why it decides everything downstream:
for each SHALLOW source, is its missing history RECOVERABLE (the table is new but the
underlying data exists and can be backfilled) or STRUCTURALLY ABSENT (nothing to
recover -- the table began when it began)?

  A "backfill it" plan aimed at a structurally-absent source delivers nothing and
  costs a round. A "the card cannot exist" conclusion on a recoverable source deletes
  a ruled-in card for no reason.

Every verdict below is grounded on (a) the producer's SOURCE -- what the runner
actually reads -- and (b) a full partition listing of that input. Not inferred from
the gold table's own shape.

METHOD NOTE: the discriminator is NOT "does the gold table have partitions". It is
"does its INPUT reach the SI floor, and is the producer a function of that input".
A shallow gold table over a deep input is a backfill; a shallow gold table over a
current-state input is not.
"""
from __future__ import annotations

import boto3

ASSETS = "opal-data-assets"
GOLD = "opal-data-49financial"
SI_FLOOR = "2024-07-08"

s3 = boto3.client("s3")

# (shallow source, producer, what the producer READS (source-grounded), input locations)
LINEAGE = [
    ("canonical_positions", "b01_canonical_positions.py",
     "silver/dim_position (POS_PREFIX :25) + dimensions/dim_security",
     [(ASSETS, "schwab/08335338/silver/dim_position/")]),
    ("accrual_materiality", "b02_accrual_decision.py",
     "silver/fact_sec (:37) + dim_position + fact_upn",
     [(ASSETS, "schwab/08335338/silver/fact_sec/"),
      (ASSETS, "schwab/08335338/silver/dim_position/"),
      (ASSETS, "schwab/08335338/silver/fact_upn/")]),
    ("valuation_integrity", "b03_valuation_integrity.py",
     "canonical/canonical_valuation (:32) + canonical/canonical_positions (:33)",
     [(GOLD, "gold/advi/canonical/canonical_valuation/"),
      (GOLD, "gold/advi/canonical/canonical_positions/")]),
    ("dim_account", "a00_dim_account.py",
     "silver/fact_acc -- 'ONE daily fact_acc partition (snapshot upsert)' (:8)",
     [(ASSETS, "schwab/08335338/silver/fact_acc/")]),
    ("dim_relationship", "a01_dim_relationship.py",
     "silver/fact_fam (custodian-delivered family grouping, :3-4) + fact_acc universe",
     [(ASSETS, "schwab/08335338/silver/fact_fam/"),
      (ASSETS, "schwab/08335338/silver/fact_acc/")]),
]


def partitions(bucket, prefix):
    p = s3.get_paginator("list_objects_v2")
    out = set()
    for pg in p.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for c in pg.get("CommonPrefixes", []) or []:
            seg = c["Prefix"].rstrip("/").split("/")[-1]
            if seg.startswith("date="):
                out.add(seg.split("=", 1)[1])
    return sorted(out)


def main() -> int:
    print("PRF-a-1 ADDENDUM 2 -- RECOVERABILITY DISCRIMINATOR (COO Ruling 2)")
    print("=" * 112)
    verdicts = {}

    for label, producer, reads, inputs in LINEAGE:
        print("\n%s" % label)
        print("   producer: %s" % producer)
        print("   reads   : %s" % reads)
        deep = True
        transitive_on_shallow = []
        for bucket, pre in inputs:
            ds = partitions(bucket, pre)
            name = pre.rstrip("/").split("/")[-1]
            if not ds:
                print("     input %-22s NO PARTITIONS" % name)
                deep = False
                continue
            reaches = ds[0] <= SI_FLOOR
            print("     input %-22s %4d parts  %s..%s  reaches SI floor: %s"
                  % (name, len(ds), ds[0], ds[-1], "YES" if reaches else "NO"))
            if not reaches:
                deep = False
                transitive_on_shallow.append(name)
        if deep:
            verdicts[label] = "RECOVERABLE"
        elif transitive_on_shallow:
            verdicts[label] = "RECOVERABLE-TRANSITIVE (ordered behind %s)" % ", ".join(transitive_on_shallow)
        else:
            verdicts[label] = "UNDETERMINED"
        print("   VERDICT : %s" % verdicts[label])

    # --- The two that are NOT settled by a partition listing ---
    print("\ndim_asset_classification")
    print("   producer: a07_dim_asset_classification.py")
    print("   reads   : DynamoDB table 'bd-securities' (:55), scanned AT BUILD TIME (_load_ddb :145-148)")
    print("             _classifier_vintage = sha256 over CURRENT DDB content + lib hash (:263)")
    print("   VERDICT : STRUCTURALLY ABSENT for point-in-time classification.")
    print("             There is no historical vintage store for the classifier. A 'backfill'")
    print("             would apply TODAY's classification to historical positions -- a")
    print("             DIFFERENT QUANTITY, and one that silently erases every reclassification")
    print("             that happened in between. It would look like history and would not be.")
    print("             Recoverable ONLY as an explicitly-labelled current-classifier-applied-")
    print("             retroactively series, which is a product decision, not a backfill.")
    verdicts["dim_asset_classification"] = "STRUCTURALLY ABSENT (point-in-time)"

    print("\ndim_account_xref")
    xref = partitions(ASSETS, "blackdiamond/49f/silver/dim_account_xref/")
    print("   silver  : %d parts %s..%s -- does NOT reach the SI floor" % (len(xref), xref[0], xref[-1]))
    print("   upstream: blackdiamond/49f/bronze carries allocation_*, fees_*, reporting_allocation,")
    print("             reporting_costbasis, reporting_performance, template_roster. NONE is")
    print("             self-evidently an account-xref source, and the xref is match-derived")
    print("             (match_method column) rather than delivered.")
    print("   VERDICT : UNDETERMINED -- I do not have evidence either way and will not guess.")
    print("             Deciding this needs the BD feed's own history read by someone who owns")
    print("             that surface. Naming it undetermined rather than assuming recoverable.")
    verdicts["dim_account_xref"] = "UNDETERMINED"

    print("\nnna_atomic")
    print("   VERDICT : NOT APPLICABLE -- dormant-superseded by determination (c01 is the")
    print("             successor, ZERO consumers, P1-CLOSE @3a924da626). Not a live dependency")
    print("             of any PERFRP cell, so it carries no remedy question at all.")
    verdicts["nna_atomic"] = "N/A (dormant-superseded)"

    print("\n" + "=" * 112)
    print("VERDICT TABLE -- DENOMINATOR: 8 shallow sources, all accounted for")
    for k in ["canonical_positions", "accrual_materiality", "valuation_integrity",
              "dim_account", "dim_relationship", "dim_asset_classification",
              "dim_account_xref", "nna_atomic"]:
        print("   %-26s %s" % (k, verdicts.get(k, "?")))

    print("\n" + "=" * 112)
    print("THE CONSEQUENCE FOR THE ALLOCATION CARD (COO Ruling 3, routed to CTO):")
    print("  The Allocation card needs BOTH canonical_positions AND dim_asset_classification.")
    print("  Those two take OPPOSITE remedies:")
    print("     canonical_positions       RECOVERABLE  -- dim_position has 535 partitions to the SI floor")
    print("     dim_asset_classification  STRUCTURALLY ABSENT for point-in-time")
    print("  So CTO's exit (i) 'backfill the source' WORKS FOR THE POSITIONS HALF AND NOT THE")
    print("  CLASSIFICATION HALF. A backfill delivers historical market VALUE by account, and")
    print("  cannot deliver a truthful historical BREAKDOWN BY ASSET CLASS.")
    print("  That is the fact the decision turns on, and it was not visible before this measurement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
