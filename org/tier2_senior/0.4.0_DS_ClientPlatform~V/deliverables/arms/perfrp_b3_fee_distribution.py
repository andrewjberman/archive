"""FEE DISTRIBUTION -- answers 3.0.0_SA_CVO 79093's RAVC-validate question, and
CORRECTS A GRAIN ERROR IN MY OWN 79025 FIGURE.

CVO read 6 partitions and found 5 at 0-1 FEE-MANAGEMENT rows, against my reported
"FEE-MANAGEMENT on 121,564 rows across 488 of 534 partitions". Four independent misses
at P = 46/534 would be ~0.6%, so one of the two reads had to be wrong about something.

IT WAS MINE, AND IT IS A GRAIN ERROR NOT A VALUE ERROR. My census counted
`partitions carrying ANY fee-class row` with FEE_CLASSES = (FEE-MANAGEMENT, FEE-ADMIN)
and I reported that 488 beside the FEE-MANAGEMENT row count, as though both described
FEE-MANAGEMENT. They do not: FEE-ADMIN is a thin sprinkle across most partitions while
FEE-MANAGEMENT concentrates on billing dates. The 121,564 row count is unaffected --
that one was measured on FEE-MANAGEMENT alone -- but "488 of 534" was never its
denominator-mate, and pairing them implied a spread the data does not have.

CVO's hypothesis ("fee rows sit on a few billing dates per quarter") is the one this
tests, and it is theirs, not mine, so it gets a real answer rather than a defence.

Prints, per CVO 79093: min / median / p90 / max FEE-MANAGEMENT rows per partition; the
count of partitions with >= 100 rows; the top 5 dates by fee rows with dollar sums; and
the object each figure was read from (bucket / prefix / schema_version census).
"""
import io
from collections import Counter

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-49financial"
PREFIX = "gold/advi/canonical/flow_ledger/"
S3 = boto3.client("s3")


def pct(sorted_vals, q):
    if not sorted_vals:
        return 0
    i = int(round(q * (len(sorted_vals) - 1)))
    return sorted_vals[i]


def main():
    keys, tok = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = S3.list_objects_v2(**kw)
        keys += [c["Key"] for c in r.get("Contents", []) if c["Key"].endswith("data.parquet")]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    keys.sort()
    print("READ FROM: bucket=%s prefix=%s" % (BUCKET, PREFIX))
    print("DENOMINATOR: %d partitions listed" % len(keys))

    fm_per, fa_per, dollars = {}, {}, {}
    schema = Counter()
    rows_total = 0
    for k in keys:
        date = k.split("date=")[1].split("/")[0]
        o = S3.get_object(Bucket=BUCKET, Key=k)
        df = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
        rows_total += len(df)
        if "schema_version" in df.columns:
            schema.update(df["schema_version"].astype(str).unique().tolist())
        else:
            schema.update(["<ABSENT>"])
        cls = df["final_class"].astype(str)
        fm = df[cls == "FEE-MANAGEMENT"]
        fm_per[date] = len(fm)
        fa_per[date] = int((cls == "FEE-ADMIN").sum())
        dollars[date] = float(fm["signed_amount"].abs().sum()) if len(fm) else 0.0

    fm_vals = sorted(fm_per.values())
    print()
    print("=" * 76)
    print("FEE-MANAGEMENT rows per partition (denominator %d partitions, %d rows)"
          % (len(keys), rows_total))
    print("=" * 76)
    print("  total FEE-MANAGEMENT rows : %d" % sum(fm_vals))
    print("  min / median / p90 / max  : %d / %d / %d / %d"
          % (fm_vals[0], pct(fm_vals, 0.5), pct(fm_vals, 0.9), fm_vals[-1]))
    print("  partitions with >= 100 rows : %d" % sum(1 for v in fm_vals if v >= 100))
    print("  partitions with >=   1 row  : %d" % sum(1 for v in fm_vals if v >= 1))
    print("  partitions with        0    : %d" % sum(1 for v in fm_vals if v == 0))
    print()
    print("  ⛔ THE CORRECTION: partitions with >=1 FEE-ADMIN row: %d"
          % sum(1 for v in fa_per.values() if v >= 1))
    print("     partitions with >=1 of EITHER fee class          : %d"
          % sum(1 for d in fm_per if fm_per[d] >= 1 or fa_per[d] >= 1))
    print("     ^ THAT last number is the 488 I reported in 79025, and I paired it with")
    print("       the FEE-MANAGEMENT row count as if it were FEE-MANAGEMENT's own")
    print("       partition spread. It is not. The row count stands; the pairing did not.")
    print()
    print("  TOP 5 DATES by FEE-MANAGEMENT rows (with |signed_amount| sums):")
    for d, n in sorted(fm_per.items(), key=lambda kv: -kv[1])[:5]:
        print("      date=%s  %6d rows   $%.2f" % (d, n, dollars[d]))
    print()
    print("  schema_version values seen across partitions: %s" % dict(schema))
    print()
    print("=" * 76)
    top5 = sum(n for _, n in sorted(fm_per.items(), key=lambda kv: -kv[1])[:5])
    print("CONCENTRATION: the top 5 dates hold %d of %d FEE-MANAGEMENT rows (%.1f%%)."
          % (top5, sum(fm_vals), 100.0 * top5 / max(sum(fm_vals), 1)))
    print("CVO 79093's hypothesis -- fee rows sit on a few billing dates -- is the one")
    print("the distribution above either supports or refutes; read it there, not here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
