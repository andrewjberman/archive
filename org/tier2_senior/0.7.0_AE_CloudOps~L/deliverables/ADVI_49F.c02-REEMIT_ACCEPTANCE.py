#!/usr/bin/env python3
"""ADVI_49F.c02-REEMIT acceptance pass -- R-3, R-4, R-5, R-6 over EVERY stored partition,
each compared against its OWN prior VersionId. Cell C02-g-3. Seat 0.7.0_AE_CloudOps~L.

THIS IS THE INSTRUMENT THE ROUND IS GRADED ON, so it is deliberately separate from the driver:
the driver's per-date oracle is narrow (new VersionId + manifest vintage + schema, else halt),
and a wrapper that both performs an act and certifies it is the shape this fabric has been
bitten by. Ruled the right shape by 2.0.0_SA_COO 84749.

DENOMINATORS ARE PRINTED, ALWAYS, IN BOTH GRAINS. CVO 84079's bar is stated in PARTITIONS and
ACCOUNT-DAYS and those are different numbers; a ratio without its denominator is the frame
error this fabric keeps paying for.

⛔ NEVER abs() ON THE MEASURING STEP FOR R-4. The whole defect being repaired was a SIGN
inversion, and abs() destroys exactly the axis that carries it. The gap is published SIGNED,
with its min and max, and the count of NEGATIVE gaps printed even when it is zero -- an
absolute value would have scored the pre-fix data as passing.

⛔ A ZERO DENOMINATOR IS NOT A PASS. "r_gross > r_net on 0 of 0 fee days" is vacuously true and
reads green in any ratio. Partitions with no fee day are counted as NOT-EVALUABLE and reported
as their own number, never folded into the pass count. Same for the partitions whose value
columns do not exist at all.

THE THREE SPECIAL PARTITIONS carry only 10 (now 11) columns -- bmv/emv/cf_net/cf_gross are
ABSENT, not null (0.4.0_DS_ClientPlatform~C 84413, correcting its own 84239 after 4.0.0_SA_CRO
caught it). So R-3's comparison is not null==null on two columns; four columns do not exist to
compare. They are reported on their own line as NOT-EVALUABLE-BY-SCHEMA with the absent columns
named.

THE PRIOR VERSION IS RESOLVED BY TIME, NOT BY POSITION: for each date it is the newest version
whose LastModified PRECEDES that date's campaign send_time from the ledger. Taking "the second
newest" would silently compare against another campaign write if a date were ever driven twice.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BUCKET = "opal-data-49financial"
GOLD_ROOT = "gold/advi"
REGION = "us-east-1"
EXPECT_VINTAGE = "946b5c5a3c89b61865ae1f4f60a609e831034cc2"
# DEFAULT IS C02-g-3's "1.1" ON PURPOSE. C02-g-6 emits "1.2" and passes it via
# --expect-schema; retyping this constant would make a re-run of the GRADED C02-g-3
# record report 535 of 535 nonconformant, i.e. a constant edited in place silently
# rewrites a past verdict. The vintage does NOT move in either round (Q-2 FAILS on a
# moved vintage), so it stays a constant.
DEFAULT_EXPECT_SCHEMA = "1.1"

HERE = Path(__file__).resolve().parent
# See the driver: the default is the C02-g-3 ledger so that graded round remains
# reproducible; each round passes its own via --ledger.
DEFAULT_LEDGER = HERE / "ADVI_49F.c02-REEMIT_CAMPAIGN_LEDGER.jsonl"
LEDGER = DEFAULT_LEDGER

VALUE_COLS = ("bmv", "emv", "cf_net", "cf_gross")
OTHER_CANON = ("canonical_valuation", "canonical_positions", "flow_ledger", "nna_canonical")

_S3 = None


def s3():
    global _S3
    if _S3 is None:
        import boto3
        _S3 = boto3.client("s3", region_name=REGION)
    return _S3


def versions(prefix: str) -> list[dict]:
    out: list[dict] = []
    for page in s3().get_paginator("list_object_versions").paginate(
            Bucket=BUCKET, Prefix=prefix):
        out.extend(page.get("Versions", []) or [])
    return out


def read_parquet(key: str, version_id: str | None = None):
    import pandas as pd
    kw = {"Bucket": BUCKET, "Key": key}
    if version_id:
        kw["VersionId"] = version_id
    return pd.read_parquet(io.BytesIO(s3().get_object(**kw)["Body"].read()))


def load_ledger() -> dict:
    rows = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("outcome") == "ARTIFACT-COMPLETE":
            rows[r["date"]] = r
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="ADVI_49F.c02-REEMIT acceptance pass")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=str(HERE / "ADVI_49F.c02-REEMIT_ACCEPTANCE_RESULT.json"))
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER),
                    help="campaign ledger for THIS round")
    ap.add_argument("--expect-schema", default=DEFAULT_EXPECT_SCHEMA,
                    help='schema_version this round expects ("1.1" C02-g-3, "1.2" C02-g-6)')
    args = ap.parse_args()
    expect_schema = args.expect_schema
    global LEDGER
    LEDGER = Path(args.ledger)
    print(f"LEDGER: {LEDGER}", flush=True)
    print(f"EXPECTING schema_version {expect_schema!r} and vintage {EXPECT_VINTAGE}",
          flush=True)

    led = load_ledger()
    dates = sorted(led)
    if args.limit:
        dates = dates[: args.limit]
    print(f"ACCEPTANCE over {len(dates)} ARTIFACT-COMPLETE partition(s)", flush=True)

    # R-3
    r3_parts_ok = 0
    r3_parts_neval = 0
    r3_acctdays = 0
    r3_max_abs_delta = 0.0
    r3_violations: list[dict] = []
    # R-4
    r4_parts_with_fee = 0
    r4_parts_no_fee = 0
    r4_fee_acctdays = 0
    r4_fee_positive = 0
    r4_gap_min = None
    r4_gap_max = None
    r4_neg_gaps = 0
    r4_nonfee_acctdays = 0
    r4_nonfee_exact_zero = 0
    # R-5
    r5_parts_ok = 0
    r5_rows_total = 0
    r5_rows_with_vintage = 0
    r5_bad: list[str] = []
    schema_10 = []
    shape_census: dict = {}
    per_partition = []

    for i, d in enumerate(dates, 1):
        key = f"{GOLD_ROOT}/canonical/twr_daily/date={d}/data.parquet"
        send = datetime.strptime(led[d]["send_time_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc)
        vs = [v for v in versions(f"{GOLD_ROOT}/canonical/twr_daily/date={d}/")
              if v["Key"].endswith("data.parquet")]
        prior = sorted([v for v in vs if v["LastModified"] < send],
                       key=lambda v: v["LastModified"])
        new = read_parquet(key)
        man = json.loads(s3().get_object(
            Bucket=BUCKET,
            Key=f"{GOLD_ROOT}/canonical/twr_daily/date={d}/manifest.json")["Body"].read())

        # ---- R-5
        r5_rows_total += len(new)
        has_v = new["gross_leg_vintage"].notna() & (new["gross_leg_vintage"] == EXPECT_VINTAGE)
        r5_rows_with_vintage += int(has_v.sum())
        sv_ok = set(new["schema_version"].astype(str).unique()) == {expect_schema}
        if bool(has_v.all()) and sv_ok and man.get("gross_leg_vintage") == EXPECT_VINTAGE \
                and str(man.get("schema_version")) == expect_schema:
            r5_parts_ok += 1
        else:
            r5_bad.append(d)

        # THREE-STATE SCHEMA CENSUS, not two.
        # ⛔ MY FIRST VERSION OF THIS COMMENT SAID THE MIXED PRESENT-AS-NaN SHAPE IS SOMETHING
        # C02-g-5 CREATES ON 396 PARTITIONS. THAT IS FALSE AND I MEASURED IT FALSE: censused
        # all 535 served partitions on 2026-08-30 BEFORE C02-g-5 -- 532 are ALREADY
        # PRESENT-AS-NaN, 3 are ABSENT (the all-refused ones), and ZERO are clean. 412,142
        # rows carry a NaN operand, which is EXACTLY the non-OK row count, with 0 partitions
        # where the two sets differ. The mixed shape is the NORM, not a consequence.
        # WHY IT IS STRUCTURAL: the engine's refusal branches append a five-key dict with no
        # operands, and pandas unions the frame, so every refusal row reads NaN there.
        # ⛔ THE REAL TRAP, AND IT IS WORSE THAN THE ONE I FIRST WROTE: operand-NaN and
        # `status != OK` are PERFECTLY REDUNDANT on today's data (535 of 535, zero
        # mismatches). So a consumer keying on operand PRESENCE gets the right answer every
        # time and is indistinguishable from a correct status-keyed one -- and stays
        # indistinguishable after C02-g-5. Shape-keying has always been wrong and has always
        # looked right. That is why the contract sets SHAPE_IS_A_VALID_CLASSIFIER = False and
        # perfrp_contract.py:325-331 names the NaN->0 rendering (it did exactly that in
        # link_returns @2e87c580b2). Reported here per partition, with the NaN row count, so
        # the census states the shape rather than inferring it from an absence test.
        absent = [c for c in VALUE_COLS if c not in new.columns]
        present = [c for c in VALUE_COLS if c in new.columns]
        nan_rows = int(new[present].isna().any(axis=1).sum()) if present else 0
        if absent:
            shape_state = "ABSENT"
        elif nan_rows:
            shape_state = "PRESENT-AS-NaN"
        else:
            shape_state = "PRESENT-AND-POPULATED"
        shape_census[shape_state] = shape_census.get(shape_state, 0) + 1
        if shape_state != "PRESENT-AND-POPULATED":
            schema_10.append({"date": d, "shape_state": shape_state,
                              "absent_columns": absent,
                              "rows_with_a_NaN_operand": nan_rows,
                              "rows": int(len(new)),
                              "status_census": Counter(new["status"]).most_common()})

        # ---- R-3
        if not prior:
            r3_parts_neval += 1
        else:
            old = read_parquet(key, prior[-1]["VersionId"])
            if "r_net" not in old.columns or "r_net" not in new.columns:
                r3_parts_neval += 1
            else:
                j = old[["account_id", "r_net", "status"]].merge(
                    new[["account_id", "r_net", "status"]], on="account_id",
                    suffixes=("_old", "_new"))
                ok = j[(j.status_old == "OK") & (j.status_new == "OK")]
                if len(ok) == 0:
                    r3_parts_neval += 1
                else:
                    delta = (ok.r_net_new - ok.r_net_old).abs()
                    r3_acctdays += len(ok)
                    mx = float(delta.max())
                    r3_max_abs_delta = max(r3_max_abs_delta, mx)
                    if mx > 0:
                        r3_violations.append({"date": d, "max_abs_delta": mx,
                                              "nonzero": int((delta > 0).sum())})
                    else:
                        r3_parts_ok += 1

        # ---- R-4
        if any(c not in new.columns for c in ("cf_gross", "cf_net", "r_gross", "r_net")):
            r4_parts_no_fee += 1
        else:
            okn = new[new["status"] == "OK"].copy()
            if len(okn) == 0:
                r4_parts_no_fee += 1
            else:
                gap = okn["r_gross"] - okn["r_net"]
                isfee = okn["cf_gross"] != okn["cf_net"]
                fee, nofee = gap[isfee], gap[~isfee]
                r4_nonfee_acctdays += len(nofee)
                r4_nonfee_exact_zero += int((nofee == 0).sum())
                if len(fee) == 0:
                    r4_parts_no_fee += 1
                else:
                    r4_parts_with_fee += 1
                    r4_fee_acctdays += len(fee)
                    r4_fee_positive += int((fee > 0).sum())
                    r4_neg_gaps += int((fee < 0).sum())
                    lo, hi = float(fee.min()), float(fee.max())
                    r4_gap_min = lo if r4_gap_min is None else min(r4_gap_min, lo)
                    r4_gap_max = hi if r4_gap_max is None else max(r4_gap_max, hi)

        per_partition.append({
            "date": d, "rows": int(len(new)), "cols": int(len(new.columns)),
            "shape_state": shape_state, "rows_with_a_NaN_operand": nan_rows,
            "status_census": dict(Counter(new["status"])),
            "vintage_ok": bool(has_v.all()), "schema_ok": bool(sv_ok),
            "OK_rows_with_negative_bmv": (
                int(((new["status"] == "OK") & (new["bmv"] < 0)).sum())
                if "bmv" in new.columns else None),
        })
        if i % 50 == 0:
            print(f"  ... {i}/{len(dates)}", flush=True)

    # ---- R-6
    camp_start = min(datetime.strptime(r["send_time_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc) for r in led.values())
    r6 = {}
    for t in OTHER_CANON:
        vs = versions(f"{GOLD_ROOT}/canonical/{t}/")
        after = [v for v in vs if v["LastModified"] >= camp_start]
        r6[t] = {"versions_total": len(vs), "created_after_campaign_start": len(after),
                 "newest": max((v["LastModified"] for v in vs)).strftime(
                     "%Y-%m-%dT%H:%M:%SZ") if vs else None}

    res = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "campaign_start_utc": camp_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "partitions_evaluated": len(dates),
        "R3": {"partitions_identical": r3_parts_ok,
               "partitions_not_evaluable": r3_parts_neval,
               "matched_OK_account_days": r3_acctdays,
               "max_abs_delta_r_net": r3_max_abs_delta,
               "violations": r3_violations},
        "R4": {"partitions_with_fee_days": r4_parts_with_fee,
               "partitions_NOT_EVALUABLE_no_fee_day": r4_parts_no_fee,
               "fee_account_days": r4_fee_acctdays,
               "fee_account_days_gap_POSITIVE": r4_fee_positive,
               "fee_account_days_gap_NEGATIVE": r4_neg_gaps,
               "signed_gap_min": r4_gap_min, "signed_gap_max": r4_gap_max,
               "nonfee_account_days": r4_nonfee_acctdays,
               "nonfee_gap_exactly_zero": r4_nonfee_exact_zero},
        "R5": {"partitions_conformant": r5_parts_ok, "partitions_nonconformant": r5_bad,
               "rows_total": r5_rows_total, "rows_with_expected_vintage": r5_rows_with_vintage,
               "expected_vintage": EXPECT_VINTAGE, "expected_schema": expect_schema},
        "R6_out_of_domain_tables": r6,
        "SHAPE_CENSUS": shape_census,
        "NOT_EVALUABLE_BY_SCHEMA": schema_10,
        "PER_PARTITION": per_partition,
    }
    Path(args.out).write_text(json.dumps(res, indent=1), encoding="utf-8")

    print("\n================ ACCEPTANCE, WITH DENOMINATORS ================")
    print(f"partitions evaluated: {len(dates)}")
    print(f"R-3  r_net identical on {r3_parts_ok} of {len(dates)} partitions; "
          f"NOT-EVALUABLE {r3_parts_neval}")
    print(f"     max |delta r_net| = {r3_max_abs_delta:.6e} over "
          f"{r3_acctdays:,} matched OK account-days;  violations: {len(r3_violations)}")
    print(f"R-4  fee-day partitions {r4_parts_with_fee} of {len(dates)}; "
          f"NOT-EVALUABLE (no fee day) {r4_parts_no_fee}")
    print(f"     SIGNED gap POSITIVE on {r4_fee_positive:,} of {r4_fee_acctdays:,} fee "
          f"account-days;  NEGATIVE {r4_neg_gaps:,}")
    print(f"     signed gap range [{r4_gap_min}, {r4_gap_max}]  (never abs())")
    print(f"     negative control: non-fee gap EXACTLY 0 on {r4_nonfee_exact_zero:,} of "
          f"{r4_nonfee_acctdays:,}")
    print(f"R-5  conformant {r5_parts_ok} of {len(dates)} partitions; "
          f"vintage on {r5_rows_with_vintage:,} of {r5_rows_total:,} rows; "
          f"nonconformant: {r5_bad or 'none'}")
    print("R-6  out-of-domain canonical tables, versions created since campaign start:")
    for t, v in r6.items():
        print(f"       {t:24s} {v['created_after_campaign_start']} new of "
              f"{v['versions_total']} total (newest {v['newest']})")
    print("SHAPE CENSUS (three states, denominator = partitions evaluated):")
    for k in ("PRESENT-AND-POPULATED", "PRESENT-AS-NaN", "ABSENT"):
        print(f"       {k:24s} {shape_census.get(k, 0)} of {len(dates)}")
    print(f"NOT-EVALUABLE-BY-SCHEMA / mixed partitions listed: {len(schema_10)}")
    for s in schema_10:
        print(f"       {s['date']}  absent={s['absent_columns']}  rows={s['rows']}  "
              f"status={s['status_census']}")
    print(f"\nwritten: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
