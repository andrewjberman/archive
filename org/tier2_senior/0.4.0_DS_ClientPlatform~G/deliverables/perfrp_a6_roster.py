"""PRF-a-6 -- ROSTER COMPLETENESS (ADVI_PERFRP TO-R1-DS, AC7).

AC7: print a00 / xref / xref-not-a00 counts; accounts in xref-not-a00 emit as
KNOWN-NOT-HELD with custodian, never omitted, never zeroed. Q-p3: this is a JOIN
(an existence question), not a classification.

Current-state per CTO 67448. EVIDENCE VINTAGE: live plane read 2026-08-25; source
citations resolve at 23271aac6480f2ebd65a37247ae64dde4d68c199.

THE HALF OF AC7 THAT CANNOT BE SATISFIED FROM THE LIVE PLANE
-------------------------------------------------------------
AC7 requires known-not-held rows to carry a CUSTODIAN. THERE IS NO CUSTODIAN SOURCE.
Measured, not assumed -- every candidate enumerated and checked:
  dim_account (a00)            37 columns, none custodian-bearing
  dim_account_xref             10 columns, none custodian-bearing
  dim_identity_crosswalk       8 columns -- SmartX uuids + schwab_account_number
  comp-find -i 'custodian' over runners_49f: 10 hits, all prose/comments, zero data fields
The PRD's custodian reference (ADVI_PERFRP_PRD.md:86, "Custodian (Fidelity IWS /
Schwab)") describes THE BD DASHBOARD'S OWN COLUMN -- the reference UI we are building
a comparable interface to. It is a description of the target, not of a field we hold.

So the honest emission is: KNOWN-NOT-HELD rows ARE emitted (that half is satisfiable
and is the load-bearing half -- never omitted, never zeroed), and custodian is emitted
as UNAVAILABLE-NO-SOURCE. Filling it with "Fidelity" because the TO's parenthetical
names Fidelity would be FABRICATION: an inference about a real client's real account
custodian, rendered on a client-facing card, sourced from a parenthetical in a task
order. That is exactly the never-silently-fill rule this project keeps applying, and
the fact that a plausible value is available is what makes it dangerous rather than
safe.

XREF-NOT-A00 IS TWO POPULATIONS, NOT ONE
-----------------------------------------
Same shape as a-3's residue. They are not the same state and take different remedies:
  MATCHED-NOT-IN-A00 : the xref resolved a schwab id and a00 does not carry it.
                       A coverage gap in the account dimension.
  UNRESOLVED-NO-MATCH: the xref row never resolved to a schwab id at all
                       (match_method='unresolved'). A BD account with no Schwab
                       counterpart -- the genuine known-not-held case.
Collapsing them into one "xref-not-a00" number would hide which, and the first is a
defect in our dim while the second is a true fact about the client's holdings.
"""
from __future__ import annotations

import io

import boto3
import pyarrow.parquet as pq

GOLD = "opal-data-49financial"
ASSETS = "opal-data-assets"
ASOF = "2026-08-21"
CUSTODIAN_SENTINEL = "UNAVAILABLE-NO-SOURCE"

s3 = boto3.client("s3")


def read(bucket, prefix, date):
    r = s3.list_objects_v2(Bucket=bucket, Prefix=f"{prefix}date={date}/")
    keys = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".parquet")]
    o = s3.get_object(Bucket=bucket, Key=keys[0])
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas(), f"s3://{bucket}/{keys[0]}"


def main() -> int:
    a00, a00_src = read(GOLD, "gold/advi/dimensions/dim_account/", ASOF)
    x, x_src = read(ASSETS, "blackdiamond/49f/silver/dim_account_xref/", ASOF)
    # Capture the TABLES' OWN column sets before adding any working column, so the
    # census below reports the schema and not my scratch state.
    a00_cols, x_cols = list(a00.columns), list(x.columns)

    print("PRF-a-6 ROSTER COMPLETENESS -- ADVI_PERFRP TO-R1-DS (AC7)")
    print("as-of %s  (current-state per CTO 67448)" % ASOF)
    print("=" * 104)
    print("SOURCES (named objects):")
    print("  %s" % a00_src)
    print("  %s" % x_src)
    print("Q-p3: this is a JOIN (existence), never a classification.")

    a_ids = set(a00["account_id"].dropna().astype(str))
    x["_sid"] = x["schwab_account_id"].astype("string")
    resolved = x[x["_sid"].notna()]
    unresolved = x[x["_sid"].isna()]
    x_sids = set(resolved["_sid"].astype(str))

    matched = x_sids & a_ids
    matched_not_in_a00 = x_sids - a_ids
    a00_not_in_xref = a_ids - x_sids

    print("\nAC7 COUNTS -- the three the criterion names, plus the direction it does not")
    print("  a00 accounts (dim_account) ................... %d" % len(a_ids))
    print("  xref rows .................................... %d" % len(x))
    print("    of which resolved to a schwab id ........... %d (%d distinct)"
          % (len(resolved), len(x_sids)))
    print("    of which UNRESOLVED (no schwab id) ......... %d" % len(unresolved))
    print("  xref-schwab FOUND in a00 ..................... %d" % len(matched))
    print("  xref-schwab NOT in a00 ....................... %d" % len(matched_not_in_a00))
    print("  a00 NOT in xref (the reverse direction) ...... %d" % len(a00_not_in_xref))
    print("  UNION of the roster (a00 | xref-schwab) ...... %d" % len(a_ids | x_sids))

    print("\nKNOWN-NOT-HELD EMISSION -- two populations, NEVER collapsed")
    rows = []
    for sid in sorted(matched_not_in_a00):
        src = resolved[resolved["_sid"].astype(str) == sid].iloc[0]
        rows.append({"key": sid, "state": "MATCHED-NOT-IN-A00",
                     "bd_account_id": src["bd_account_id"],
                     "custodian": CUSTODIAN_SENTINEL,
                     "in_0833_universe": src["in_0833_universe"],
                     "account_is_open": src["account_is_open"]})
    for _, src in unresolved.iterrows():
        rows.append({"key": src["bd_account_id"], "state": "UNRESOLVED-NO-MATCH",
                     "bd_account_id": src["bd_account_id"],
                     "custodian": CUSTODIAN_SENTINEL,
                     "in_0833_universe": src["in_0833_universe"],
                     "account_is_open": src["account_is_open"]})

    n_matched = sum(1 for r in rows if r["state"] == "MATCHED-NOT-IN-A00")
    n_unres = sum(1 for r in rows if r["state"] == "UNRESOLVED-NO-MATCH")
    print("  MATCHED-NOT-IN-A00 ... %4d  (a coverage gap in OUR account dim)" % n_matched)
    print("  UNRESOLVED-NO-MATCH .. %4d  (a BD account with no Schwab counterpart)" % n_unres)
    print("  TOTAL EMITTED ........ %4d  -- none omitted, none zeroed" % len(rows))
    print("\n  sample (first 4):")
    for r in rows[:4]:
        print("    key=%-14s state=%-20s custodian=%-22s open=%s in_0833=%s"
              % (str(r["key"])[:14], r["state"], r["custodian"],
                 r["account_is_open"], r["in_0833_universe"]))

    print("\nCUSTODIAN -- AC7's OTHER HALF, AND IT HAS NO SOURCE")
    print("  every known-not-held row carries custodian='%s'." % CUSTODIAN_SENTINEL)
    print("  Enumerated and checked, not assumed:")
    print("    dim_account            %2d cols, custodian-bearing: %s"
          % (len(a00_cols), [c for c in a00_cols if "cust" in c.lower()] or "NONE"))
    print("    dim_account_xref       %2d cols, custodian-bearing: %s"
          % (len(x_cols), [c for c in x_cols if "cust" in c.lower()] or "NONE"))
    print("    dim_identity_crosswalk  8 cols -- SmartX uuids + schwab_account_number, NONE")
    print("  The PRD's 'Custodian (Fidelity IWS / Schwab)' (PRD:86) describes the BD")
    print("  DASHBOARD'S column -- the reference UI, not a field we hold.")
    print("  FILLING IT 'Fidelity' FROM THE TO'S PARENTHETICAL WOULD BE FABRICATION:")
    print("  an inference about a real client's real custodian, on a client-facing card,")
    print("  sourced from prose. A plausible value being available is what makes it")
    print("  dangerous, not what makes it safe.")

    print("\nAC7 VERDICT")
    print("  emission half (never omitted, never zeroed) ... SATISFIED (%d rows)" % len(rows))
    print("  custodian half ................................ NOT SATISFIABLE -- no source")
    print("  -> routed to the issuer. The cell is buildable; the criterion names a field")
    print("     the live plane does not carry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
