"""V2-8 pre-fire pass 2 -- FULL TYPED PATH exercised IN MEMORY on the latest landed
bronze partitions, BOTH lanes. Mirrors convert_object's exact order (parse -> T1 ->
section_frame -> dedup -> typed_table -> project) with ZERO S3 writes.

This is the cast layer (decimal128 vendor-width law, date32 law, vintage-aware drift
law) and the projection law exercised on the exact bytes the first post-swap
conversions will read -- the eclipse dtype-refusal class (CTO 162512Z) priced by
exercise, not assertion.
"""
import json
import sys
import traceback

sys.path.insert(0, r"C:\Users\AndrewBerman\Desktop\ajb_workspace\data\assets\scripts\silver")

import boto3

import crs_reader as cr
import cs_reader as cs
import schwab_conversion as conv
import schwab_projections as prj
import schwab_schemas as sch

BUCKET = "opal-data-assets"

KEYS = [
    # 08242234
    "schwab/08242234/bronze/acc/20260713/08242234.CRS20260713.ACC.zip",
    "schwab/08242234/bronze/rld/20260713/08242234.CRS20260713.RLD.zip",
    "schwab/08242234/bronze/rlu/20260605/08242234.CRS20260605.RLU.zip",
    "schwab/08242234/bronze/rlw/20260710/08242234.CRS20260710.RLW.zip",
    "schwab/08242234/bronze/rly/20260630/08242234.CRS20260630.RLY.zip",
    "schwab/08242234/bronze/rps/20260713/08242234.CRS20260713.RPS.zip",
    "schwab/08242234/bronze/rtu/20260605/08242234.CRS20260605.RTU.zip",
    "schwab/08242234/bronze/rty/20260630/08242234.CRS20260630.RTY.zip",
    "schwab/08242234/bronze/sec/20260713/08242234.CRS20260713.SEC.zip",
    "schwab/08242234/bronze/trn/20260713/08242234.CRS20260713.TRN.zip",
    "schwab/08242234/bronze/uln/20260713/08242234.CRS20260713.ULN.zip",
    "schwab/08242234/bronze/ult/20260713/08242234.CRS20260713.ULT.zip",
    "schwab/08242234/bronze/upn/20260713/08242234.CRS20260713.UPN.zip",
    "schwab/08242234/bronze/upt/20260713/08242234.CRS20260713.UPT.zip",
    # 08335338
    "schwab/08335338/bronze/acc/20260713/08335338.CRS20260713.ACC.zip",
    "schwab/08335338/bronze/fam/20260713/08335338.CS071326.FAM.zip",
    "schwab/08335338/bronze/rld/20260713/08335338.CRS20260713.RLD.zip",
    "schwab/08335338/bronze/rlu/20260605/08335338.CRS20260605.RLU.zip",
    "schwab/08335338/bronze/rly/20260630/08335338.CRS20260630.RLY.zip",
    "schwab/08335338/bronze/rps/20260713/08335338.CRS20260713.RPS.zip",
    "schwab/08335338/bronze/rtu/20260605/08335338.CRS20260605.RTU.zip",
    "schwab/08335338/bronze/rty/20260630/08335338.CRS20260630.RTY.zip",
    "schwab/08335338/bronze/sec/20260713/08335338.CRS20260713.SEC.zip",
    "schwab/08335338/bronze/slm/20260713/08335338.CS071326.SLM.zip",
    "schwab/08335338/bronze/trn/20260713/08335338.CRS20260713.TRN.zip",
    "schwab/08335338/bronze/uln/20260713/08335338.CRS20260713.ULN.zip",
    "schwab/08335338/bronze/ult/20260713/08335338.CRS20260713.ULT.zip",
    "schwab/08335338/bronze/upn/20260713/08335338.CRS20260713.UPN.zip",
    "schwab/08335338/bronze/upt/20260713/08335338.CRS20260713.UPT.zip",
]


def main() -> None:
    s3 = boto3.client("s3")
    results = []
    for i, key in enumerate(KEYS, 1):
        print(f"[{i}/{len(KEYS)}] {key}", flush=True)
        feed = conv.feed_from_key(key)
        date = conv.date_from_key(key)
        master = conv.scope_from_key(key)
        base = key.rsplit("/", 1)[-1]
        blob = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        rec = {"key": key, "master": master, "feed": feed, "date": date,
               "tables": {}, "projections": {}, "errors": []}
        try:
            if feed.upper() in ("FAM", "SLM"):
                cf = cs.parse_cs(blob, source_file=base)
                df = cs.cs_frame(cf)
                t = sch.typed_table(df, feed, 1, partition_date=date)
                rec["tables"]["fact_" + feed.lower()] = {
                    "rows_parsed": cf.n_rows, "rows_out": t.num_rows,
                    "cols_out": t.num_columns, "verification": cf.verification}
            else:
                cf = cr.parse_crs(blob, source_file=base)
                assert cf.parsed_rows == cf.attested_rows  # T1 tied inside parse too
                for sec in cf.sections:
                    fact_name = "fact_" + feed.lower() + (
                        "" if sec.index == 1 else f"_s{sec.index}")
                    df = cr.section_frame(cf, sec)
                    df, removed = cr.dedup(df)
                    t = sch.typed_table(df, feed, sec.index, partition_date=date)
                    rec["tables"][fact_name] = {
                        "rows_parsed": sec.n_rows, "dupes_removed": removed,
                        "rows_out": t.num_rows, "cols_out": t.num_columns,
                        "verification": "T1_RECONCILED"}
                    for dname, _cols in prj.projections_for(feed, sec.index):
                        dt = prj.project(t, dname)
                        prj.assert_projection_parity(dt, dname, t.num_rows) \
                            if hasattr(prj, "assert_projection_parity") else None
                        rec["projections"][dname] = {
                            "rows": dt.num_rows, "fact_rows": t.num_rows,
                            "parity": dt.num_rows == t.num_rows,
                            "cols": dt.num_columns}
        except Exception as e:
            rec["errors"].append({"class": type(e).__name__, "msg": str(e)[:400]})
            traceback.print_exc()
        results.append(rec)

    path = (r"C:\Users\ANDREW~1\AppData\Local\Temp\claude"
            r"\C--Users-AndrewBerman-Desktop-ajb-workspace"
            r"\7d85526b-fa17-433e-b25a-b52e74a9e188\scratchpad\prefire_typed_exercise.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=1)
    print("WROTE", path, flush=True)

    errs = 0
    for r in results:
        lane = r["master"]
        for name, t in r["tables"].items():
            extra = (f" dupes={t['dupes_removed']}" if t.get("dupes_removed") else "")
            print(f"  {lane} {name:12s} out={t['rows_out']:>8} cols={t['cols_out']:>3}"
                  f" [{t['verification']}]{extra}")
        for d, p in r["projections"].items():
            flag = "PARITY" if p["parity"] else "!!NO-PARITY!!"
            print(f"  {lane} {d:12s} rows={p['rows']:>8} cols={p['cols']:>3} {flag}")
        for e in r["errors"]:
            errs += 1
            print(f"  {lane} {r['feed']} ERROR {e['class']}: {e['msg']}")
    print(f"TYPED-EXERCISE COMPLETE: files={len(results)} errors={errs}", flush=True)


if __name__ == "__main__":
    main()
