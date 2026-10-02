"""Rebuild #5 dry run, OTHER-6 field diff (issuer, NO WRITE): which daily fields changed on the 6 day rows the
round-37 dry run counted as OTHER (securities with no added mention whose 2026-10-02 row changed).

Builds mention + daily for ONLY those 6 securities through the capturing client (no put is sent), with the same patch
the dry run uses (build_daily reads the captured mention rows), then diffs each built row against the served row,
field by field. Prints the changed field-set per row.
"""
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R32C = os.path.join(os.path.dirname(HERE), "round32", "checks")
sys.path.insert(0, R32C)
_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

UNIVERSE = os.path.join(os.path.dirname(HERE), "round33", "securities.universe.r33.json")
KEYS = ["CICHY_US_Equity", "CNI_US_Equity", "IBN_US_Equity", "ICICIBC_IN_Equity", "ST_SP_Equity", "WALMEX*_MM_Equity"]
DAY = "2026-10-02"


def main():
    secs = [s for s in json.load(open(UNIVERSE, encoding="utf-8")) if s["security_key"] in KEYS]
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_d = [r for r in pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
                if r.get("security_key") in KEYS and str(r.get("day"))[:10] == DAY]
    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    cm = sg.CapturingClient(real)
    pg.build_mention(secs, as_of, client=cm)
    (_k, mbody), = cm.puts.items()
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
    full_mention = [r for r in served_m if r.get("security_key") not in KEYS] + mention
    orig = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: full_mention if table == pg.GOLD_TABLE else orig(table, client=client)
    cd = sg.CapturingClient(real)
    pg.build_daily(secs, as_of, client=cd)
    pg._latest_gold_snapshot_rows = orig
    (_k2, dbody), = cd.puts.items()
    built = {r["security_key"]: r for r in pq.read_table(io.BytesIO(dbody)).to_pylist() if str(r.get("day"))[:10] == DAY}
    print("served day rows %d; built day rows %d; PUTS SENT %d" % (len(served_d), len(built), cm.sent + cd.sent))
    sm = {(r["article_key"], r["security_key"]) for r in served_m if r.get("security_key") in KEYS}
    bm = {(r["article_key"], r["security_key"]) for r in mention}
    print("mention rows for the 6: served %d, built %d, added %d, gone %d" % (len(sm), len(bm), len(bm - sm), len(sm - bm)))
    out = {}
    for s in served_d:
        b = built.get(s["security_key"])
        if b is None:
            print(s["security_key"], "NOT BUILT")
            continue
        diff = {f: (str(s.get(f)), str(b.get(f))) for f in sorted(set(s) | set(b))
                if json.dumps(s.get(f), default=str) != json.dumps(b.get(f), default=str)}
        out[s["security_key"]] = diff
        print(s["security_key"], json.dumps(diff, default=str)[:600])
    json.dump(out, open(os.path.join(HERE, "gold_rebuild5_other6_diff.json"), "w", encoding="utf-8"), indent=1, default=str)


if __name__ == "__main__":
    main()
