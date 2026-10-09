"""Print every filing_source row per silver part (key, accession, parser, fetched_at, record_hash[:12]); read-only."""
import io

import boto3
import pyarrow.parquet as pq
B = "opal-data-harvest"
s3 = boto3.client("s3", region_name="us-east-1")
for pg in s3.get_paginator("list_object_versions").paginate(Bucket=B, Prefix="sec/harvest/silver/filing_source/"):
    for v in sorted(pg.get("Versions", []), key=lambda x: x["Key"]):
        t = pq.read_table(io.BytesIO(s3.get_object(Bucket=B, Key=v["Key"], VersionId=v["VersionId"])["Body"].read()))
        print(v["Key"].split("filing_source/")[1], v["VersionId"], t.num_rows, "rows")
        for r in t.to_pylist():
            if r["security_key"] in ("ASML_NA_Equity","BABA_US_Equity","NU_US_Equity","SAP_GY_Equity","PBR_US_Equity"):
                print("   ", r["security_key"], r["accession"], r.get("parser_version") or r.get("parser"), str(r["fetched_at"]), r["record_hash"][:12])
