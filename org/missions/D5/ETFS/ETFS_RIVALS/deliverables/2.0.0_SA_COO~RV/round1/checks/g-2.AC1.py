"""RIV-g-2 AC1 -- trade_schedule equals the PRD's C-TRADE-SCHEDULE formula, recomputed here independently from the
cell's own canonical_shape output over the last 40 real archived BASG days (c-1 -> s-1 -> g-1 -> g-2, local sink).

Oracle: per consecutive report pair, f = median(q_t/q_{t-1}) over non-cash keys held on both dates; a trade is
|q_t - f*q_{t-1}| >= 0.002*q_{t-1}, plus every entry and exit. Key = security_id when RESOLVED else raw_identifier.
A gold row flagged ID-CHANGE may replace exactly one exit+entry pair of the oracle in the same window."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

ACTIONS = {"entry", "add", "trim", "exit"}
CONF = {"CLEAN", "FLOW-WINDOW", "STALE-WIDENED", "ID-CHANGE", "CORP-ACTION", "UNRESOLVED"}
COLS = ["fund_ticker", "security_key", "action", "window_start", "window_end", "shares_before", "shares_after",
        "flow_factor", "discretionary_shares", "est_price", "est_notional", "confidence"]


def oracle(cs):
    import pandas as pd

    cs = cs[cs["position_type"].astype(str).str.lower() != "cash"].copy()
    cs["key"] = cs["security_id"].where(cs["resolution_status"] == "RESOLVED", cs["raw_identifier"])
    dates = sorted(cs["report_date"].astype(str).unique())
    out = set()
    for a, b in zip(dates, dates[1:]):
        qa = cs[cs["report_date"].astype(str) == a].groupby("key")["quantity"].sum()
        qb = cs[cs["report_date"].astype(str) == b].groupby("key")["quantity"].sum()
        both = qa.index.intersection(qb.index)
        both = [k for k in both if qa[k] > 0]
        f = float(pd.Series([qb[k] / qa[k] for k in both]).median()) if both else 1.0
        for k in both:
            r = qb[k] - f * qa[k]
            if abs(r) >= 0.002 * qa[k]:
                out.add((k, b, "add" if r > 0 else "trim"))
        for k in qb.index.difference(qa.index):
            out.add((k, b, "entry"))
        for k in qa.index.difference(qb.index):
            out.add((k, b, "exit"))
    return out, dates


def run(v):
    c.setup_path()
    files = c.archive_files(40)
    sink = c.tmpdir("rv_g2_")
    res = c.run_chain(sink, files, through="trades")
    print("trades:", str(res["trades"])[:400])
    v.check(res["trades"].get("status") == "OK", f"trade_schedule status OK (got {res['trades'].get('status')})")
    cs_root = c.local_path(sink, c.address("rivalfunds", "etfs", "gold", "canonical_shape", "date=")).parent
    ts_root = c.local_path(sink, c.address("rivalfunds", "etfs", "gold", "trade_schedule", "date=")).parent
    cs, _ = c.read_parquets(cs_root)
    ts, n = c.read_parquets(ts_root)
    v.check(n >= 1 and len(ts) > 0, f"trade_schedule written ({len(ts)} row(s), {n} part(s))")
    missing = [k for k in COLS if k not in ts.columns]
    v.check(not missing, f"columns present (missing {missing})")
    if missing or not len(ts):
        return
    want, dates = oracle(cs)
    prev = {b: a for a, b in zip(dates, dates[1:])}
    ts["window_end"] = ts["window_end"].astype(str).str[:10]
    ts["window_start"] = ts["window_start"].astype(str).str[:10]
    v.check(set(ts["action"]) <= ACTIONS, f"action enum ({sorted(set(ts['action']))})")
    v.check(set(ts["confidence"]) <= CONF, f"confidence enum ({sorted(set(ts['confidence']))})")
    bad_win = ts[ts.apply(lambda r: prev.get(r["window_end"]) != r["window_start"], axis=1)]
    v.check(bad_win.empty, f"every window is (prior report date, report date] -- never finer ({len(bad_win)} off)")
    idc = ts[ts["confidence"] == "ID-CHANGE"]
    got = {(r.security_key, r.window_end, r.action) for r in ts[ts["confidence"] != "ID-CHANGE"].itertuples()}
    residue = want - got
    explained = sum(1 for (k, w, a) in residue if a in ("entry", "exit") and w in set(idc["window_end"]))
    v.check(got <= want, f"no gold trade outside the formula ({len(got - want)} extra: {sorted(got - want)[:5]})")
    v.check(len(residue) - explained == 0 and explained <= 2 * len(idc),
            f"every formula trade present, ID-CHANGE explaining at most its pair ({len(residue)} missing, {explained} explained by {len(idc)} ID-CHANGE row(s))")
    print(f"report dates {len(dates)}; oracle trades {len(want)}; gold rows {len(ts)}; ID-CHANGE {len(idc)}")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
