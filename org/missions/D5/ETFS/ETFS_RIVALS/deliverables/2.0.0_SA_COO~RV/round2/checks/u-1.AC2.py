"""RIV-u-1 AC2 -- the G0 stage writes peer_group_map at its builder address in a local sink: 13 rows (7 PFOE + 6 IDVZ),
the C-GOLD-MODEL provenance columns and a claim; a rerun of the same map version writes nothing new (never-overwrite)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import gold_peer_group_map

    sink = c.tmpdir("rv_g0b_")
    ev = {"mode": "daily", "date": "2026-09-30", "batch_id": "chk-g0", "sink": f"local:{sink}"}
    r1 = gold_peer_group_map.handler_entry(dict(ev))
    print("r1:", str(r1)[:300])
    d = c.gold_dir(sink, "peer_group_map")
    df, n = c.read_parquets(d)
    v.check(r1.get("status") == "OK" and n >= 1, f"status {r1.get('status')}, {n} parquet object(s) under {d}")
    v.check(len(df) == 13, f"13 map rows (got {len(df)})")
    for col in ["group_id", "home_fund_id", "fund_id", "ticker", "role", "source_policy", "effective_from", "map_version",
                "revision", "produced_at", "producer_version", "input_manifest", "claim"]:
        v.check(col in df.columns, f"column {col}")
    r2 = gold_peer_group_map.handler_entry(dict(ev, batch_id="chk-g0-rerun"))
    _, n2 = c.read_parquets(d)
    v.check(n2 == n, f"rerun of map_version writes nothing new ({n} -> {n2}; r2 status {r2.get('status')})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
