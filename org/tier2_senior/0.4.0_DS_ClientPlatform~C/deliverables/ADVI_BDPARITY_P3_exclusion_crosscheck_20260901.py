"""P3-EXACT cycle 1 -- INDEPENDENT cross-check of the 64-account exclusion set.

Derives, from OUR gold twr_daily ONLY (zero vendor egress), the set of accounts carrying a
single-day |r_net| > 1.0 -- the bound 2.0.0_SA_COO 90726 s.3(A) used to define the exclusion.

WHY THIS EXISTS: 0.4.0_DS_ClientPlatform~Y measured 64 accounts (63 inside the 1Y window). This is
a SECOND DERIVATION on a DIFFERENT instrument. It is a CROSS-CHECK, never a replacement -- if the
two disagree the difference is SURFACED, not silently resolved. An exclusion list that drifts either
drives a cell the sequencer ruled untouchable or withholds one nobody excluded, and both are silent.

Loader pattern reused from org/tier1_exec/4.0.0_SA_CRO/scripts/bdparity_mechanism_magnitudes_20260830.py
(build ladder: the estate already has it) -- schema-tolerant per-partition read, printed denominators.

PRINTS ITS OWN DENOMINATORS: partitions scanned of partitions in history, rows, accounts.
"""
import pandas as pd
import pyarrow.parquet as pq
import s3fs

BUCKET = "opal-data-49financial"
PREFIX = "gold/advi/canonical/twr_daily/"
WANT = ["account_id", "business_date", "r_net", "status", "bmv"]

# The three ruled windows nest: 1Y > YTD > QTD, so their union IS the 1Y window.
ONEY_START = "2025-08-28"
ASOF = "2026-08-28"
BOUND = 1.0


def main():
    fs = s3fs.S3FileSystem(skip_instance_cache=True, use_listings_cache=False)
    files = sorted(f for f in fs.find("%s/%s" % (BUCKET, PREFIX)) if f.endswith("data.parquet"))
    want = [f for f in files if f.split("date=")[1][:10] <= ASOF]
    print("PARTITIONS: %d scanned of %d in history (cap asof %s)" % (len(want), len(files), ASOF))
    if not want:
        print("ERROR: zero partitions matched -- OUT OF CORPUS, not an absence.")
        return 1

    frames, short = [], []
    for f in want:
        sch = pq.read_schema(f, filesystem=fs).names
        cols = [c for c in WANT if c in sch]
        if "r_net" not in cols or "account_id" not in cols:
            short.append((f.split("date=")[1][:10], len(sch)))
            continue
        t = pq.read_table(f, filesystem=fs, columns=cols).to_pandas()
        if len(t):
            t["_part"] = f.split("date=")[1][:10]
            frames.append(t)
    df = pd.concat(frames, ignore_index=True)
    df["r_net"] = pd.to_numeric(df.get("r_net"), errors="coerce")
    print("ROWS %d | ACCOUNTS %d | reduced//skipped partitions: %s"
          % (len(df), df.account_id.nunique(), short if short else "none"))

    date_col = "business_date" if "business_date" in df.columns else "_part"
    df["_d"] = df[date_col].astype(str).str[:10]

    hit = df[df["r_net"].abs() > BOUND].copy()
    print("")
    print("=== |r_net| > %.1f  (the 90726 bound) ===" % BOUND)
    print("ROWS above bound (FULL HISTORY)          : %d" % len(hit))
    print("ACCOUNTS above bound (FULL HISTORY)      : %d" % hit.account_id.nunique())

    inw = hit[hit["_d"] >= ONEY_START]
    print("ROWS above bound INSIDE 1Y (%s..%s): %d" % (ONEY_START, ASOF, len(inw)))
    print("ACCOUNTS above bound INSIDE 1Y           : %d" % inw.account_id.nunique())
    print("")
    print("EXPECTED from 0.4.0_DS_ClientPlatform~Y / 90726: 64 accounts, 63 inside 1Y, 114 rows")

    accts = sorted(hit.account_id.astype(str).unique())
    print("")
    print("=== THE DERIVED ACCOUNT SET (full history), %d ids ===" % len(accts))
    for i in range(0, len(accts), 8):
        print("  " + " ".join(accts[i:i + 8]))

    out = "p3_exclusion_crosscheck_accounts.txt"
    with open(out, "w") as fh:
        fh.write("\n".join(accts) + "\n")
    print("")
    print("WROTE %s (%d ids)" % (out, len(accts)))

    print("")
    print("=== date clustering of the above-bound rows (A-class signal) ===")
    vc = hit["_d"].value_counts().head(12)
    for d, n in vc.items():
        print("  %s  %d" % (d, n))
    print("DISTINCT DATES carrying an above-bound row: %d" % hit["_d"].nunique())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
