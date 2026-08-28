"""THE FEE CENSUS -- COO 78986 item 4, refined by COO 78991 on CTO 78990.

A READ, not a spec change (Rule 27: the spec is frozen). It answers ONE question:
does the 49F classifier EVER emit FEE-MANAGEMENT?

WHY IT MATTERS: PRF-inv-6 clause 1 says "SERVED RETURN = NET-OF-FEE TWR". Measured in
PRF-b-2, r_net == r_gross on 100% of non-null rows in BOTH vintages. c02_twr_engine
builds cf_gross = cf_net - fee_cf from rows whose final_class == "FEE-MANAGEMENT", so
if the classifier never emits that class, net == gross VACUOUSLY and the served "net"
is the gross figure. Two readings, one measurement apart:
  ZERO fee debits in the RAW flows      -> the clause holds BY FACT (49F bills advisory
                                           fees outside the accounts), and the contract
                                           should say so. CTO's call on wording.
  fee debits present but mislabelled    -> a CLASSIFIER GAP; surfaced, never fixed here.

⛔ PART (i) IS AN INSTRUMENT GAP AND IS REPORTED AS ONE, NOT PROXIED.
COO 78991: "If the raw description field is not on the served flow_ledger, say which
plane carries it and stop there -- name the instrument gap rather than substituting a
proxy." MEASURED: the served gold canonical/flow_ledger carries 25 columns and NONE is
a free-text custodian description. It carries the custodian CODE TRIPLE
(tran_srcde, tr_cd, sb_cd) plus the derived final_class.
THE PLANE THAT CARRIES THE DESCRIPTION: silver/fact_trn, column
`transaction_detail_description` -- named in c00_flow_ledger.py:118-120 TRN_COLS, which
is what c00 reads at BUILD time to produce this gold table. So the raw-description
match (i) is answerable on silver/fact_trn and NOT on the served plane. Stopping there,
per the instruction.

PARTS (ii) and (iii) ARE answerable on the served plane and are measured below over
ALL served partitions, denominator printed.

NOTE ON THE VOCABULARY, so a zero is read correctly: c00_flow_ledger.py:96-107
FINAL_BY_PARTITION maps THREE upstream values onto FEE-MANAGEMENT
(FEE-MANAGEMENT, FEE-MANAGEMENT-VERIFIED, FEE-MANAGEMENT-INFERRED). A zero here is
therefore a zero across all three, not a miss on one spelling.
"""
import io
from collections import Counter

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-49financial"
PREFIX = "gold/advi/canonical/flow_ledger/"
FEE_CLASSES = ("FEE-MANAGEMENT", "FEE-ADMIN")
S3 = boto3.client("s3")


def partitions():
    keys = []
    tok = None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = S3.list_objects_v2(**kw)
        for c in r.get("Contents", []):
            if c["Key"].endswith("data.parquet"):
                keys.append(c["Key"])
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    return sorted(keys)


def main():
    keys = partitions()
    print("SERVED flow_ledger partitions (auto-paginated, counted client-side): %d" % len(keys))
    if not keys:
        print("POSITIVE CONTROL FAILED: zero partitions listed -- out of corpus, not absence")
        return 2

    final_class = Counter()
    provenance = Counter()
    rows_total = 0
    read = 0
    code_triples = set()
    fee_rows = []
    for k in keys:
        o = S3.get_object(Bucket=BUCKET, Key=k)
        df = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
        read += 1
        rows_total += len(df)
        if "final_class" in df.columns:
            final_class.update(df["final_class"].astype(str).tolist())
        if "resolution_provenance" in df.columns:
            provenance.update(df["resolution_provenance"].astype(str).tolist())
        for c in ("tran_srcde", "tr_cd", "sb_cd"):
            if c not in df.columns:
                print("*** column %s ABSENT on %s -- schema drift, stopping" % (c, k))
                return 2
        code_triples.update(zip(df["tran_srcde"].astype(str),
                                df["tr_cd"].astype(str), df["sb_cd"].astype(str)))
        hit = df[df["final_class"].astype(str).isin(FEE_CLASSES)]
        if len(hit):
            fee_rows.append((k.split("date=")[1].split("/")[0], len(hit),
                             hit["final_class"].astype(str).value_counts().to_dict()))

    print()
    print("=" * 76)
    print("DENOMINATOR: %d partitions listed, %d READ, %d rows total" % (len(keys), read, rows_total))
    print("=" * 76)
    print("(ii)+(iii) final_class census over ALL served partitions:")
    for k, v in final_class.most_common():
        print("    %-32s %8d   (%.6f%%)" % (k, v, 100.0 * v / rows_total))
    print()
    print("  FEE-MANAGEMENT count: %d of %d rows" % (final_class.get("FEE-MANAGEMENT", 0), rows_total))
    print("  FEE-ADMIN      count: %d of %d rows" % (final_class.get("FEE-ADMIN", 0), rows_total))
    print("  partitions carrying ANY fee-class row: %d of %d" % (len(fee_rows), read))
    for d, n, c in fee_rows[:20]:
        print("      date=%s  %d row(s)  %s" % (d, n, c))
    print()
    print("  resolution_provenance census:")
    for k, v in provenance.most_common():
        print("    %-32s %8d" % (k, v))
    print()
    print("  distinct custodian code triples (tran_srcde, tr_cd, sb_cd): %d" % len(code_triples))
    print("  ^ the fee determination is NOT made from these codes alone: c00_flow_ledger")
    print("    resolves them against a bound-truth classification TABLE (its 10-value live")
    print("    vocabulary), so a code census here cannot by itself answer (i).")
    print()
    print("=" * 76)
    fm = final_class.get("FEE-MANAGEMENT", 0)
    if fm == 0:
        print("RESULT: the 49F classifier emits FEE-MANAGEMENT on 0 of %d rows across all")
        print("%d served partitions. cf_gross = cf_net - fee_cf therefore subtracts NOTHING," % read)
        print("and r_net == r_gross VACUOUSLY -- which is exactly what PRF-b-2 measured.")
        print("THIS DOES NOT DECIDE by-design vs classifier-gap: that turns on part (i),")
        print("which the served plane cannot answer. silver/fact_trn carries the raw")
        print("description. CTO's question, not this seat's.")
    else:
        print("RESULT: FEE-MANAGEMENT IS emitted (%d rows). The vacuous-equality reading is" % fm)
        print("FALSIFIED; r_net == r_gross needs another explanation. Surface it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
