"""RIV-d-5 addendum -- the SERVED delta of the q-1 amendment-1 fix (rows Z-W4-S12/S13), measured on G2 holdings_coverage.

Mirrors, READ-ONLY, every input G2 reads (Bloomberg bronze sidecars + bytes, issuer bronze + silver, the Positioning home
landings, G1 canonical_shape), then builds G2 in replay mode TWICE over the same mirror: once with the DEPLOYED module
(`git show <deployed>:data/etfs/scripts/rivalfunds/gold_holdings_coverage.py`, d-5's apply base) and once with the module at
this tree's HEAD (the fix). The diff is per (fund_id, expected_date, source): status, row_count, selected, sidecar file.
Also diffs the deployed-module run against the SERVED G2 (the control: the mirror reproduces what is served).

    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round4/served_delta_g2.py --deployed 5a4b5b5391 --out <json>
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import io
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

BUCKET = "opal-data-etfs"


def log(*a):
    print(dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%SZ"), *a, file=sys.stderr, flush=True)


def root() -> pathlib.Path:
    return pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                       check=True).stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deployed", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    r = root()
    for p in (str(r / "data" / "etfs" / "scripts"), str(r)):
        sys.path.insert(0, p)
    import boto3
    import pandas as pd
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import homes

    s3 = boto3.client("s3", region_name="us-east-1")
    pg = s3.get_paginator("list_objects_v2")

    def keys(prefix):
        return [o["Key"] for p in pg.paginate(Bucket=BUCKET, Prefix=prefix) for o in p.get("Contents", [])]

    def rel(uri_prefix):
        return uri_prefix[len(f"s3://{BUCKET}/"):] if uri_prefix.startswith("s3://") else uri_prefix

    base = pathlib.Path(tempfile.mkdtemp(prefix="rv_g2d_"))
    sink_a = base / "deployed"

    def mirror(k):
        dst = sink_a / BUCKET / k
        dst.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(BUCKET, k, str(dst))

    sets = {
        "bloomberg_bronze": keys(rel(cb.bronze_prefix(""))),
        "issuer_bronze": keys(rel(homes.issuer_bronze(""))),
        "issuer_silver": keys(rel(homes.issuer_silver("", "x")).rsplit("date=", 1)[0]),
        "home_landings": [k for k in keys("bbg/") if k.endswith("/constituents/constituents_issuer_fill.parquet")],
        "g1": keys(rel(homes.canonical_shape("")).rsplit("date=", 1)[0]),
    }
    counts = {}
    for name, ks in sets.items():
        log("mirror", name, len(ks))
        with ThreadPoolExecutor(max_workers=24) as pool:
            list(pool.map(mirror, ks))
        counts[name] = len(ks)
    sink_b = base / "fix"
    shutil.copytree(sink_a, sink_b)
    log("mirrored", counts)

    import rivalfunds.gold_holdings_coverage as new_mod
    old_src = subprocess.run(["git", "show", f"{args.deployed}:data/etfs/scripts/rivalfunds/gold_holdings_coverage.py"],
                             capture_output=True, text=True, check=True, cwd=str(r)).stdout
    old_path = base / "gold_holdings_coverage_deployed.py"
    old_path.write_text(old_src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("rivalfunds.gold_holdings_coverage_deployed", old_path)
    old_mod = importlib.util.module_from_spec(spec)
    old_mod.__package__ = "rivalfunds"
    spec.loader.exec_module(old_mod)

    res = {}
    for label, mod, sink in (("deployed", old_mod, sink_a), ("fix", new_mod, sink_b)):
        log("G2 replay", label)
        res[label] = mod.handler_entry({"mode": "replay", "batch_id": f"g2d-{label}", "sink": f"local:{sink}",
                                        "end": "2026-09-30"})
        log(label, str(res[label])[:200])

    def g2(sink):
        d = sink / BUCKET / rel(new_mod.coverage_prefix("")).rsplit("date=", 1)[0]  # the prefix ends in a partial `date=`
        frames = [pd.read_parquet(io.BytesIO(p.read_bytes())) for p in sorted(d.rglob("*.parquet"))]
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def served():
        frames = []
        for k in keys(rel(new_mod.coverage_prefix(""))):
            if k.endswith(".parquet"):
                frames.append(pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())))
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    A, B, S = g2(sink_a), g2(sink_b), served()

    def norm(df):
        if not len(df):
            return {}
        out = {}
        for x in df.itertuples():
            k = (str(x.fund_id).strip(), str(x.expected_date)[:10], str(x.source))
            out[k] = (str(x.status), int(x.row_count) if x.row_count == x.row_count and x.row_count is not None else None,
                      bool(x.selected), str(x.sidecar_uri).rsplit("/", 1)[-1].split("-")[0] if x.sidecar_uri else None)
        return out

    a, b, sv = norm(A), norm(B), norm(S)
    per_fund = {}
    for k in sorted(set(a) | set(b)):
        f = k[0]
        rec = per_fund.setdefault(f, {"rows_deployed": 0, "rows_fix": 0, "changed": 0, "added": 0, "removed": 0, "examples": []})
        rec["rows_deployed"] += k in a
        rec["rows_fix"] += k in b
        if k in a and k in b and a[k] != b[k]:
            rec["changed"] += 1
            if len(rec["examples"]) < 3:
                rec["examples"].append([list(k), list(a[k]), list(b[k])])
        elif k in b and k not in a:
            rec["added"] += 1
        elif k in a and k not in b:
            rec["removed"] += 1
    cross = sorted({k[0] for k, v in b.items() if v[3] and k[2] == "issuer" and v[3] not in ("basg", "gqgu")}
                   | {k[0] for k, v in b.items() if k[2] == "issuer" and v[3] and k[0].lower() != v[3]})
    ctl = sum(1 for k in set(a) | set(sv) if a.get(k) != sv.get(k))
    if not a or not b:
        raise SystemExit(f"EMPTY local G2 read: deployed {len(a)} keys, fix {len(b)} keys -- the instrument, not a result")
    out = {"deployed": args.deployed, "inputs": counts, "stage": {k: str(v)[:300] for k, v in res.items()},
           "per_fund": per_fund, "issuer_rows_reading_another_funds_capture_in_fix": cross,
           "control_deployed_vs_served_differing_keys": ctl, "served_keys": len(sv), "deployed_keys": len(a)}
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "stage"}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
