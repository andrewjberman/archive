"""INS-inv-4 / Rule 17 census -- bronze-vs-silver conformance for the 49F insurance landing plane.

Discharges the SECOND half of INS-inv-4. The first half (Rule 17a, "no parquet under bronze/")
is a key-shape test answered by a prefix walk; this is the field-and-row test that Rule 17
actually names: SILVER IS DEDUP + DTYPE ONLY -- no field slimming, no fillna, no business filter.

WHY A SCRIPT AND NOT A ONE-OFF READ: two of the four bronze insurance tables have no silver
counterpart yet (0.6.0_AE_PartnerETL's leg, per 1.0.0_SA_CTO ruling 78287). When they land, the
same read must run on four tables rather than being re-derived by whoever is seated then.

FALSIFIERS (each must be able to FIRE -- see --self-test):
  F1 field slimming  a bronze field with no silver column
  F2 invented field  a silver vendor column with no bronze field
  F3 row filter      bronze record count != silver row count
  F4 fillna          a silver column with zero nulls where bronze had absent/empty values

⛔ A CLEAN ZERO ON EVERY ARM AND A DEAD MATCHER PRINT THE SAME THING. --self-test plants one
defect per arm and requires each to fire; a run without it certifies nothing.

Bronze carriers are NOT uniform and the extension does not tell you which: the REST surfaces land
JSON objects, the bulk-export surface lands an XLSX workbook under a .json key (measured
2026-08-27, exportResultID-282397, magic 50 4b 03 04). Carrier is sniffed by magic bytes, never
by suffix.
"""

import argparse
import json
import sys

import pandas as pd

ZIP_MAGIC = b"PK\x03\x04"


def read_one(path):
    """Return (records, carrier, declared_total). Sniffs the carrier -- .json is not evidence."""
    raw = open(path, "rb").read()
    if raw[:4] == ZIP_MAGIC:
        frame = pd.read_excel(path, engine="openpyxl")
        return frame.to_dict("records"), "xlsx", None
    doc = json.loads(raw.decode("utf-8"))
    if isinstance(doc, dict) and "data" in doc:
        return doc["data"], "json:data[]", doc.get("total")
    if isinstance(doc, list):
        return doc, "json:list", None
    return [doc], "json:object", None


def read_bronze(paths):
    """Union a PAGE SET into one cohort.

    ⛔ A PAGE IS NOT AN ANSWER. The REST surfaces here page at 50; comparing one page against a
    full silver partition reports a phantom F3 row-filter violation. Measured on the first run of
    this script: offset0 alone = 50 records vs silver 77 -> F3 -27, which is the INVOCATION's
    defect, not the pipeline's. Where the payload declares `total`, it is checked against the
    union and a shortfall is raised rather than silently compared.
    """
    records, carriers, totals = [], [], set()
    for path in paths:
        recs, carrier, total = read_one(path)
        records += recs
        carriers.append(carrier)
        if total is not None:
            totals.add(total)
    carrier = carriers[0] if len(set(carriers)) == 1 else "+".join(carriers)
    if len(paths) > 1:
        carrier += f" ({len(paths)} pages)"
    if len(totals) == 1:
        declared = totals.pop()
        if declared != len(records):
            raise SystemExit(
                f"BLOCKED: page set is INCOMPLETE -- payload declares total={declared} but the "
                f"{len(paths)} file(s) given union to {len(records)} records. Supply every page; "
                f"a partial cohort makes the F3 arm report the caller's error as the pipeline's."
            )
    return records, carrier


def normalize(name):
    """xlsx headers are Title Case, silver columns snake_case. A rename is a DTYPE-layer act,
    not slimming -- comparing raw spellings would report 9 false slimming hits on table 2."""
    return "".join(ch for ch in str(name).lower() if ch.isalnum())


def census(records, frame):
    bronze_fields = set()
    for rec in records:
        bronze_fields |= set(rec.keys())
    meta = {c for c in frame.columns if c.startswith("_")}
    vendor = set(frame.columns) - meta

    b_norm = {normalize(f): f for f in bronze_fields}
    v_norm = {normalize(c): c for c in vendor}

    return {
        "bronze_records": len(records),
        "bronze_fields": len(bronze_fields),
        "silver_rows": len(frame),
        "silver_vendor_cols": len(vendor),
        "silver_meta_cols": sorted(meta),
        "F1_slimming": sorted(b_norm[k] for k in set(b_norm) - set(v_norm)),
        "F2_invented": sorted(v_norm[k] for k in set(v_norm) - set(b_norm)),
        "F3_row_delta": len(records) - len(frame),
        "F4_no_null_cols": sorted(c for c in vendor if frame[c].notna().all()),
    }


def report(label, records, frame, carrier):
    r = census(records, frame)
    verdict = not r["F1_slimming"] and not r["F2_invented"] and r["F3_row_delta"] == 0
    print(f"\n[{label}] carrier={carrier}")
    print(f"  DENOMINATOR bronze records={r['bronze_records']} fields={r['bronze_fields']} "
          f"| silver rows={r['silver_rows']} vendor={r['silver_vendor_cols']} "
          f"meta={len(r['silver_meta_cols'])}")
    print(f"  F1 slimming : {len(r['F1_slimming'])} {r['F1_slimming']}")
    print(f"  F2 invented : {len(r['F2_invented'])} {r['F2_invented']}")
    print(f"  F3 row delta: {r['F3_row_delta']}")
    print(f"  F4 zero-null vendor cols (fillna CANDIDATES, not verdicts): {r['F4_no_null_cols']}")
    print(f"  RULE 17: {'CONFORMS' if verdict else 'VIOLATION'}")
    return r, verdict


def self_test(records, frame):
    """Each arm must fire from a DIFFERENT planted truth. An arm that cannot fire is a dead
    matcher, and a dead matcher prints the same clean zero as a conforming table."""
    print("\n" + "=" * 62)
    print("SELF-TEST -- can each falsifier FIRE?")
    print("=" * 62)
    results = []

    victim = sorted(set().union(*(set(r.keys()) for r in records)))[0]
    m1 = [{k: v for k, v in r.items() if k != victim} for r in records]
    fired = bool(census(m1, frame)["F2_invented"])
    print(f"  M1 bronze loses field {victim!r:<28} -> F2 {'FIRES' if fired else 'DEAD'}")
    results.append(fired)

    m2 = frame.copy()
    m2["invented_twr_ytd"] = 0.0
    fired = "invented_twr_ytd" in census(records, m2)["F2_invented"]
    print(f"  M2 silver gains an invented column        -> F2 {'FIRES' if fired else 'DEAD'}")
    results.append(fired)

    fired = census(records[:-5], frame)["F3_row_delta"] != 0
    print(f"  M3 bronze loses 5 records                 -> F3 {'FIRES' if fired else 'DEAD'}")
    results.append(fired)

    m4 = frame.copy()
    m4[m4.columns[0]] = m4[m4.columns[0]].fillna("FILLED")
    fired = m4.columns[0] in census(records, m4)["F4_no_null_cols"]
    print(f"  M4 silver fillna on {str(m4.columns[0])!r:<21} -> F4 {'FIRES' if fired else 'n/a (col had no nulls)'}")

    ok = all(results)
    print(f"  SELF-TEST: {'PASS' if ok else 'FAIL'} ({sum(results)}/{len(results)} required arms fired)")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", action="append", nargs=3, metavar=("LABEL", "BRONZE", "SILVER"),
                    required=True,
                    help="repeatable: table label, bronze file(s) COMMA-SEPARATED (every page of "
                         "the cohort), silver parquet")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    conforming, total = 0, 0
    first = None
    for label, bronze_arg, silver_path in args.pair:
        records, carrier = read_bronze([p for p in bronze_arg.split(",") if p])
        frame = pd.read_parquet(silver_path)
        _, verdict = report(label, records, frame, carrier)
        conforming += int(verdict)
        total += 1
        if first is None:
            first = (records, frame)

    ok = True
    if args.self_test and first:
        ok = self_test(*first)

    print(f"\nDENOMINATOR: {conforming}/{total} table(s) CONFORM to Rule 17.")
    if not ok:
        print("BLOCKED: self-test failed -- the census cannot detect what it exists to detect.")
        return 2
    return 0 if conforming == total else 1


if __name__ == "__main__":
    sys.exit(main())
