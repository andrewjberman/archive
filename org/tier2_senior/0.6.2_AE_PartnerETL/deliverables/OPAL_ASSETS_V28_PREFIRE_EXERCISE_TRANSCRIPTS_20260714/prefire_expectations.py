"""V2-8 pre-fire expectation measurement -- committed reader over the LATEST landed
bronze partitions, BOTH masters, read-only (GetObject only; nothing written to S3).

Denominator: the 30 keys below were ENUMERATED AT RUN TIME (13b) via ListObjectsV2
Contents[-1] per schwab/{master}/bronze/{type}/ prefix, 2026-07-14 (this session).
Pipe types parse via crs_reader.parse_crs (T1 tie is a HARD RAISE inside the parse);
CS types via cs_reader.parse_cs (structurally UNVERIFIED_BY_T1).
"""
import json
import sys
import traceback

sys.path.insert(0, r"C:\Users\AndrewBerman\Desktop\ajb_workspace\data\assets\scripts\silver")

import boto3

import crs_reader
import cs_reader

BUCKET = "opal-data-assets"

KEYS = {
    "08242234": [
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
    ],
    "08335338": [
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
    ],
}


def main() -> None:
    s3 = boto3.client("s3")
    out: dict = {"bucket": BUCKET, "keys_measured": 0, "lanes": {}}
    n_total = sum(len(v) for v in KEYS.values())
    done = 0
    for master, keys in KEYS.items():
        lane: dict = {}
        for key in keys:
            done += 1
            base = key.rsplit("/", 1)[-1]
            ftype = key.split("/bronze/")[1].split("/")[0]
            print(f"[{done}/{n_total}] {key}", flush=True)
            blob = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
            rec: dict = {"key": key, "bytes": len(blob)}
            try:
                if base.split(".")[1].startswith("CS"):
                    cf = cs_reader.parse_cs(blob, source_file=base)
                    rec.update({
                        "kind": "CS",
                        "master_observed": cf.master,
                        "file_date": cf.file_date,
                        "rows": cf.n_rows,
                        "n_cols": len(cf.columns),
                        "verification": cf.verification,
                    })
                else:
                    pf = crs_reader.parse_crs(blob, source_file=base)
                    rec.update({
                        "kind": "CRS",
                        "master_observed": pf.master,
                        "business_date": pf.business_date,
                        "record_type": pf.record_type,
                        "sections": [
                            {"index": s.index, "prefix": s.data_prefix,
                             "rows": s.n_rows, "n_cols": len(s.columns)}
                            for s in pf.sections
                        ],
                        "parsed_rows": pf.parsed_rows,
                        "attested_rows": pf.attested_rows,
                        "t1_tie": pf.parsed_rows == pf.attested_rows,
                        "verification": "T1_RECONCILED",
                    })
            except Exception as e:  # a raise here is itself a pre-fire finding
                rec.update({"kind": "ERROR", "error_class": type(e).__name__,
                            "error": str(e)[:500]})
                traceback.print_exc()
            lane[ftype] = rec
            out["keys_measured"] += 1
        out["lanes"][master] = lane

    path = r"C:\Users\ANDREW~1\AppData\Local\Temp\claude\C--Users-AndrewBerman-Desktop-ajb-workspace\7d85526b-fa17-433e-b25a-b52e74a9e188\scratchpad\prefire_expectations.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print("WROTE", path, flush=True)

    for master, lane in out["lanes"].items():
        print(f"== {master}")
        for ftype in sorted(lane):
            r = lane[ftype]
            if r.get("kind") == "CRS":
                secs = " + ".join(f"{s['prefix']}:{s['rows']}" for s in r["sections"])
                tie = "TIE" if r["t1_tie"] else "!!NO-TIE!!"
                print(f"  {ftype:5s} parsed={r['parsed_rows']:>8} attested={r['attested_rows']:>8} {tie}  [{secs}]  date={r['business_date']}")
            elif r.get("kind") == "CS":
                print(f"  {ftype:5s} rows={r['rows']:>8} {r['verification']}  date={r['file_date']}")
            else:
                print(f"  {ftype:5s} ERROR {r.get('error_class')}: {r.get('error')}")


if __name__ == "__main__":
    main()
