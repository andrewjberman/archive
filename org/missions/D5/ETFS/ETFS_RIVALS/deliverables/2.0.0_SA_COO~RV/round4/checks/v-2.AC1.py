"""RIV-v-2 AC1 -- one revision contract: G1 reads the G4 that is NEWEST BY CAPTURE TIME, and an `import:` QA object never
outranks a live pull for the same date (analysis ruling 2; row W4-S5).

The measured case, REAL served objects (READ-ONLY): s3://opal-data-etfs/rivalfunds/etfs/gold/security_market/date=2026-09-29/
holds market-20260929-afcd903ad844.parquet (172 rows, source `import:bbg/2026-09-29/characteristics.parquet`, produced
10:59:32Z) and market-20260929-53bc393958bd.parquet (434 rows, source `blp_client.reference_data`, produced 11:10:34Z); by
name the import sorts last. Both are copied into a local sink with the 2026-09-29 inputs G1 reads (issuer silver, Bloomberg
silver, the home landing), and canonical_shape is replayed for 2026-09-29 only. Then:
  - every RESOLVED gics_source names the LIVE revision 53bc393958bd, none names afcd903ad844;
  - control: the RESOLVED GICS row count exceeds what the 172-row import alone could key (the live pull is in use)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-09-29"
LIVE, IMPORT = "53bc393958bd", "afcd903ad844"
B = "opal-data-etfs"


def run(v):
    c.setup_path()
    import boto3

    s3 = boto3.client("s3")
    pg = s3.get_paginator("list_objects_v2")
    keys = lambda p: [o["Key"] for pp in pg.paginate(Bucket=B, Prefix=p) for o in pp.get("Contents", [])]  # noqa: E731
    sink = c.tmpdir("rv_v2a_")
    want = keys(f"rivalfunds/etfs/gold/security_market/date={D}/")
    want += keys(f"issuer-site/etfs/silver/holdings/date={D}/")
    want += keys(f"bloomberg/etfs/silver/holdings/date={D}/")
    want += [f"bbg/{D}/constituents/constituents_issuer_fill.parquet"]
    for k in want:
        c.mirror_s3(sink, f"s3://{B}/{k}")
    print(f"mirrored {len(want)} objects for {D}")
    r = c.replay("gold_canonical_shape", sink, D, batch_id="v2a")
    print("canonical:", r.get("status"))
    df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={D}")
    if not len(df):
        v.check(False, "G1 written")
        return
    g1 = c.newest_rows(df.assign(_date=D))
    res = g1[g1["gics_status"].astype(str) == "RESOLVED"]
    srcs = set(res["gics_source"].astype(str))
    print(f"RESOLVED GICS rows {len(res)}; sources {sorted(srcs)[:3]}")
    v.check(len(res) > 0 and all(LIVE in x for x in srcs), f"every RESOLVED gics_source names the live G4 {LIVE}")
    v.check(not any(IMPORT in x for x in srcs), f"no gics_source names the import {IMPORT}")
    v.check(len(res) > 172, f"control: RESOLVED GICS rows {len(res)} exceed what the 172-row import could key")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
