"""BP-a-4 -- trace the CANONICAL row of one (asset, date) with the instrument's own core.

Why this exists: trace_price.py run_live reads the daily silver/prices/<date>.parquet AND the canonical object,
and when both carry the asset on the date it takes the stable pick (daily first). For the thread holding the lot
prices carry the CANONICAL row, so the daily-first pick reports the wrong winner and no trades. This driver calls
the instrument's own trace_asset_date() with the canonical object as the only object read. Nothing is re-implemented:
the module is loaded from its own path and its functions are called as written.

Usage (from the worktree root):
  python org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~4/trace_canonical_only.py \
      --asset "<asset_name>" --date YYYY-MM-DD --out <file.json>
Read verbs only (S3 get_object on opal-data-bd). Prints no account, client or advisor field.
"""
import argparse
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TRACE = os.path.normpath(os.path.join(HERE, "..", "0.9.0_WK_ADVI_BDPRCE~2", "trace_price.py"))


def load_instrument():
    spec = importlib.util.spec_from_file_location("trace_price", TRACE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    tp = load_instrument()
    consts = tp.load_constants(tp.find_pipeline_src(None))
    s3 = tp.s3_client()
    canon = tp.read_obj(s3, tp.BUCKET, tp.CANON_KEY)
    if canon is None:
        print("TRACE ERROR: canonical object not read", file=sys.stderr)
        return 2
    rec = tp.trace_asset_date(args.asset, args.date, consts, None, canon,
                              lambda: tp.read_txn(s3, tp.BUCKET, args.date),
                              lambda: tp.read_hist(s3, tp.BUCKET))
    rec["objects_read"] = ["canonical:" + canon[1] + "@" + str(canon[2])]
    rec["bucket"] = tp.BUCKET
    rec["constants"] = {"src": consts["src_rel"], "max_unit_price": consts["max_unit_price"],
                        "lines": consts["lines"]}
    rec["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec["script"] = "trace_canonical_only.py (BP-a-4) calling trace_price.py trace_asset_date"
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, indent=2, ensure_ascii=True, default=str) + "\n")
    print("TRACE WROTE %s asset=%s date=%s source=%s trades=%d match=%s"
          % (args.out, json.dumps(rec["asset_name"]), rec["date"], rec["price_source"],
             len(rec.get("trade_ids") or []), str(rec.get("match")).lower()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
