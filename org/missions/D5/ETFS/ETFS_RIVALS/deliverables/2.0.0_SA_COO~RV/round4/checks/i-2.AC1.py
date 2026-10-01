"""RIV-i-2 AC1 -- BASG's issuer-only report dates resolve identity through a MEASURED alias (analysis ruling 3; row W4-S2):
a CUSIP joined to a Bloomberg key on an earlier co-held date (the RIV-i-1 root-ticker + shares join) keeps that key on a day
the daily Bloomberg request never carries BASG. Never a guess: a CUSIP that was never joined stays UNRESOLVED.

REAL served inputs (READ-ONLY): issuer silver for 2026-09-28 and 2026-09-30, and the BASG Bloomberg silver objects for
2026-09-28 (the last co-held date: the census ends there; 2026-09-29/30 have none -- the daily Bloomberg request excludes BASG).
canonical_shape is replayed for 2026-09-28..2026-09-30 in a local sink. Then, for BASG's non-cash rows on 2026-09-30:
  - at least 90% are RESOLVED (served today: 0 of 33);
  - each resolved row's security_id equals the key its CUSIP resolved to on 2026-09-28 (one identity, carried, not re-guessed);
  - control: 2026-09-28's BASG rows still resolve at >= 95% (the alias does not displace the same-day join)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D0, D1 = "2026-09-28", "2026-09-30"  # the last co-held date (the PFOE census ends 09-28) and an issuer-only date
B = "opal-data-etfs"


def run(v):
    c.setup_path()
    import boto3

    s3 = boto3.client("s3")
    pg = s3.get_paginator("list_objects_v2")
    keys = lambda p: [o["Key"] for pp in pg.paginate(Bucket=B, Prefix=p) for o in pp.get("Contents", [])]  # noqa: E731
    sink = c.tmpdir("rv_i2a_")
    want = keys(f"issuer-site/etfs/silver/holdings/date={D0}/") + keys(f"issuer-site/etfs/silver/holdings/date={D1}/")
    want += [k for k in keys(f"bloomberg/etfs/silver/holdings/date={D0}/") if k.rsplit("/", 1)[-1].startswith("BASG-")]
    for k in want:
        c.mirror_s3(sink, f"s3://{B}/{k}")
    print(f"mirrored {len(want)} objects")
    from rivalfunds import gold_canonical_shape

    gold_canonical_shape.handler_entry({"mode": "replay", "batch_id": "i2a", "sink": f"local:{sink}", "date": D1,
                                        "start": D0, "end": D1})
    out = {}
    for d in (D0, D1):
        df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={d}")
        g = c.newest_rows(df.assign(_date=d)) if len(df) else df
        g = g[(g["fund_ticker"].astype(str).str.strip() == "BASG") & ~g["is_cash_line"].astype(bool)] if len(g) else g
        out[d] = g
        ok = int((g["resolution_status"] == "RESOLVED").sum()) if len(g) else 0
        print(f"{d}: BASG non-cash resolved {ok}/{len(g)}")
    g0, g1 = out[D0], out[D1]
    f1 = float((g1["resolution_status"] == "RESOLVED").mean()) if len(g1) else 0.0
    f0 = float((g0["resolution_status"] == "RESOLVED").mean()) if len(g0) else 0.0
    v.check(len(g1) > 0 and f1 >= 0.90, f"{D1} BASG resolved {f1:.3f} >= 0.90")
    key0 = dict(zip(g0["security_cusip"].astype(str), g0["security_id"].astype(str))) if len(g0) else {}
    r1 = g1[g1["resolution_status"] == "RESOLVED"] if len(g1) else g1
    bad = [(cu, k) for cu, k in zip(r1["security_cusip"].astype(str), r1["security_id"].astype(str)) if key0.get(cu) != k]
    v.check(len(r1) > 0 and not bad, f"every {D1} key equals its CUSIP's {D0} key ({bad[:3]})")
    v.check(f0 >= 0.95, f"control: {D0} BASG still resolves {f0:.3f} >= 0.95")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
