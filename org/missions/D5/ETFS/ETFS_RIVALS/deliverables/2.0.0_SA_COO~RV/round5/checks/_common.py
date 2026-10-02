"""Shared helpers for the ETFS_RIVALS round-5 checks (issuer-written, 2.0.0_SA_COO~RV): re-exports round 4's helpers, plus the
fixture builders the round-5 checks share. Every check runs offline on a `local:` sink unless its docstring says it reads S3
(READ-ONLY)."""
from __future__ import annotations

import importlib.util
import json
import pathlib

_R4 = pathlib.Path(__file__).resolve().parents[2] / "round4" / "checks" / "_common.py"
_spec = importlib.util.spec_from_file_location("_rivals_r4_common", _R4)
_r4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r4)

Verdict, guarded, setup_path, local_path, tmpdir, main_root = (
    _r4.Verdict, _r4.guarded, _r4.setup_path, _r4.local_path, _r4.tmpdir, _r4.main_root)
read_parquets, gold_dir, newest_rows = _r4.read_parquets, _r4.gold_dir, _r4.newest_rows

ROOT = pathlib.Path(__file__).resolve().parents[9]  # the worktree the check runs in


def weekdays_ending(last: str, n: int) -> list[str]:
    import datetime as dt
    d, out = dt.date.fromisoformat(last), []
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d -= dt.timedelta(days=1)
    return sorted(out)


def fake_crosswalk(g):
    """Replace gold_canonical_shape's crosswalk with a fixture one (no file, no S3), the test_g12 pattern."""
    class CW:
        @staticmethod
        def resolve(form, path=None):
            if form.endswith(" US Equity"):
                t = form.split()[0]
                return {"security_key": f"{t}_US_Equity", "matched_as": "bloomberg_equity_suffix", "bloomberg": f"{t} US"}
            return {"security_key": None, "matched_as": None, "bloomberg": None, "miss": form}

        @staticmethod
        def load_crosswalk(path=None):
            return ({}, {}, {})

        @staticmethod
        def loaded_from(path=None):
            return "file:fake"

    g._crosswalk = lambda: CW
    return CW


def bbg_capture_file(tmp: pathlib.Path, date: str, funds=("TXUE", "BIDD"), sec="AAA US Equity", name=None) -> str:
    from rivalfunds.tests import test_b1_bloomberg_channel as tb1
    rows = [tb1._row(f, sec, date) for f in funds]
    cap = tb1._cap(date, f"{date}T23:00:00-04:00", rows, funds=funds)
    p = tmp / (name or f"cap-{date}.json")
    p.write_text(json.dumps(cap), encoding="utf-8")
    return str(p)


def served_g1_fund(fund: str, dates: list[str]):
    """READ-ONLY: the served G1 rows of `fund` on each of `dates` (newest object per date by revision.newest), one frame."""
    import io

    import boto3
    import pandas as pd
    from rivalfunds import homes, revision

    s3 = boto3.client("s3", region_name="us-east-1")
    frames = []
    for d in dates:
        pre = homes.canonical_shape(d)[len("s3://opal-data-etfs/"):] + "/"
        keys = [o["Key"] for o in s3.list_objects_v2(Bucket="opal-data-etfs", Prefix=pre).get("Contents", [])
                if o["Key"].endswith(".parquet")]
        pick = revision.newest(keys)
        if not pick:
            continue
        df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket="opal-data-etfs", Key=pick)["Body"].read()))
        frames.append(df[df["fund_ticker"].astype(str).str.strip() == fund])
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def served_prior_date(fund: str, before: str, lookback: int = 12) -> str | None:
    """READ-ONLY: the fund's own previous report date before `before` in served G1 (scans back `lookback` weekdays)."""
    for d in reversed(weekdays_ending(before, lookback + 1)[:-1]):
        if len(served_g1_fund(fund, [d])):
            return d
    return None


def page_fixture():
    """The test_p2 `sink` fixture, built outside pytest: three report days of TXUE (bloomberg) and BASG (issuer), G5 replayed.
    The identity floor is pinned to 0.0 (these checks are about what the page shows). Returns (spec, sink, tmp_dir)."""
    import os

    from rivalfunds import gold_trade_schedule, guardrails, sinks
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    os.environ[guardrails.OVERRIDE_ENV] = json.dumps({"min_resolved_fraction": 0.0})
    tmp = pathlib.Path(tmpdir("rv_page_"))
    spec = f"local:{tmp}"
    s = sinks.get_sink(spec)
    for step, d in enumerate(("2026-09-25", "2026-09-28", tp2.DAY)):
        tp2._put(s, d, {"TXUE": (tp2._book(step), "bloomberg", 0.1 * step), "BASG": (tp2._book(step), "issuer", 0.1 * step)})
    r = gold_trade_schedule.handler_entry({"date": tp2.DAY, "mode": "replay", "batch_id": "g", "sink": spec})
    assert r["status"] == "OK", r
    return spec, s, tmp


# ---- amendment A1 (Addendum B) fixtures -------------------------------------------------------------------------------------

AI_DAY = "2026-10-02"


def ai2_tables():
    """Small G5, G6, holding_contribution and buying_trend frames for fund TXUE (contract shapes, amendment A1)."""
    import datetime as dt

    import pandas as pd
    d = dt.date.fromisoformat
    g5 = pd.DataFrame([
        {"fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": "S1", "security_key": "S1", "action": "add",
         "window_start": d("2026-09-14"), "window_end": d("2026-09-15"), "est_notional_base": 1000.0, "dataset_revision": "r1"},
        {"fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": "S2", "security_key": "S2", "action": "add",
         "window_start": d("2026-07-31"), "window_end": d("2026-08-03"), "est_notional_base": 2000.0, "dataset_revision": "r1"}])
    g6 = pd.DataFrame([{"fund_id": "TXUE", "window_end": d("2026-09-15"), "status": None, "reason": None},
                       {"fund_id": "TXUE", "window_end": d("2026-08-03"), "status": None, "reason": None}])
    hc = pd.DataFrame([
        {"fund_id": "TXUE", "role": "rival", "period": p, "period_start": "2026-09-02", "period_end": AI_DAY, "axis": "security",
         "bucket": "S1", "security_name": "S1", "contribution": 0.0125, "price_coverage": "full", "n_days_priced": 20,
         "n_days_period": 20, "rank_best": 1, "rank_worst": 2, "n_ranked": 2, "n_missing": 0, "claim": "INFERRED", "revision": "hc1"}
        for p in ("R30", "MTD")])
    bt = pd.DataFrame([{"fund_id": "TXUE", "role": "rival", "window_start": "2026-01-02", "window_end": AI_DAY,
                        "n_trading_days": 189, "axis": "security", "bucket": "S1", "security_name": "S1",
                        "net_notional_base": 3000.0, "n_windows": 3, "lean": "into", "rank": 1, "reading": "tilt",
                        "trend_mark": "+ + + 0 0 0 0 0 0 0", "n_refused_windows": 0, "claim": "INFERRED", "revision": "bt1"}])
    return g5, g6, hc, bt


def ai2_readings(missing=()):
    """Market readings in the ai-1 contract; every source fresh unless named in `missing`."""
    out = []
    for src, name in (("fear_greed", "stock_price_strength"), ("rsi", "equities"), ("trending_topics", "rates"),
                      ("keyword_sentiment", "tariffs"), ("harvest_chatter", "S1")):
        if src in missing:
            out.append({"source": src, "name": name, "value": None, "as_of": None, "age_trading_days": None, "status": "missing",
                        "location": None, "series": None, "reason": "absent in fixture"})
        else:
            out.append({"source": src, "name": name, "value": 1.5, "as_of": "2026-10-01", "age_trading_days": 1, "status": "fresh",
                        "location": f"s3://fixture/{src}", "series": [["2026-10-01", 1.5]], "reason": None})
    return out


class StubClient:
    """The injected AI client (no vendor call): `chat(messages, model) -> str` returns the next canned JSON reply and records the
    messages; `web_search(query, model) -> {"text", "urls"}` records the query."""

    def __init__(self, replies):
        self.replies, self.calls, self.web = list(replies), [], []

    def chat(self, messages, model):
        self.calls.append([dict(m) for m in messages])
        return self.replies.pop(0)

    def web_search(self, query, model):
        self.web.append(query)
        return {"text": "Web summary of the market this week.", "urls": ["https://example.com/a"]}


def ai2_reply(text, cited, invalidation="a reversal of the S1 adds"):
    return json.dumps({"text": text, "observed": [text], "inferred": ["the manager may keep adding"], "cited": cited,
                       "invalidation": invalidation})
