"""RIV-co-1 AC1 (PRD v0.18 FWD-22, ADDENDUM F.5 items 1 and 4; ROUND15_CELLS_DRAFT.md rev 1.5): the publisher writes one chart
object per fund beside the page, covering exactly the securities whose dialog carries that fund's section, and names it in the
manifest.

Measured at the base: `publish_page` writes index.html, audit.html and manifest.json at `homes.page(day, ...)` and nothing under
`charts/`; the manifest has no `charts`; neither `render` nor `publish_page` has `dialog_fund_keys`; `rivalfunds.price_series` and
`rivalfunds.trade_markers` do not exist.

Interface (prescribed, verbatim from the cell and the round's shared vocabulary):
  - Chart object: one JSON per fund per page day at `homes.page(<day>, "charts/<FUND>.json")` (opal_naming output), shape
    `{"fund", "asof", "generated_at", "ranges": {"R30": <first day>, "R90": ..., "R365": ...}, "securities": {<security_key>:
    {"name", "source_words", "points": [[<YYYY-MM-DD>, <price>|null, <source code>], ...], "gaps": [{"start", "end", "reason"}],
    "markers": [{"side": "buy"|"sell", "start", "end", "span": bool, "usd", "bps", "r", "n_trades"}]}}}`. Source codes: `m`
    market close, `i` holding-implied. `points` ascend by date and cover `asof - 365d .. asof`. `asof = prev_trading_day(page_day)`;
    a window's first day is `asof - N calendar days`.
  - `publish_page` writes `homes.page(day, "charts/<FUND>.json")` for every fund of the page, in the shape of the shared
    vocabulary, covering exactly the securities whose dialog on the rendered page carries that fund's section
    (`render.dialog_fund_keys(html) -> {fund: [security_key, ...]}`, exported by THIS cell from a regex over the rendered HTML:
    `data-sec-dialog="<key>"` blocks and their `<section data-fund=...>` children; no render.py edit). Built from
    `price_series.load` and `trade_markers.markers`. The manifest gains `charts: {<FUND>: {"uri", "bytes", "securities",
    "markers", "thinned"}}`. The day's page publishes whether or not a chart object fails.
  The cell names the function `render.dialog_fund_keys` and also says "no render.py edit": this check takes it from `render` or,
  failing that, from `publish_page`, and prints which.

Fixture: the round-5 offline page fixture's shape (test_p2's `_put` / `_book` on a `local:` sink, page day 2026-09-30, so asof
2026-09-29; G5 replayed) with ONE difference: BASG's book has no S02. TXUE (bloomberg) and BASG (issuer) report 2026-09-25,
09-28 and 09-29; S03 is added in the window ending 09-28 (est_notional 4,047.90) and trimmed in the one ending 09-29; S05 is
trimmed in the one ending 09-29. The fixture holds no G4 market close, so every price is holding-implied (S03 on 09-29:
13,596 / 1,030 = 13.2). The securities are keyed by their raw identifier (the fixture rows are unresolved).
  - (a) `dialog_fund_keys(html)` over the served index.html equals this check's own walk of the dialog blocks (TXUE 11 keys with
    S02, BASG 10 without);
  - (b) `charts/TXUE.json` and `charts/BASG.json` are written at `homes.page(day, "charts/<FUND>.json")`, each a JSON object with
    exactly the prescribed top-level keys (plus an optional `thinned`), `fund` its fund, `asof` 2026-09-29, `ranges` R30
    2026-08-30 / R90 2026-07-01 / R365 2025-09-29, and `securities` keyed by EXACTLY the fund's dialog keys (S02 in TXUE's, not in
    BASG's), every security carrying name, source_words (non-empty strings), points, gaps, markers;
  - (c) TXUE's S03 series: points are [date, price|null, code] triples ascending from 2025-09-29 to 2026-09-29, the 2026-09-29
    point is 13.2 with code `i`, every gap carries start / end / reason; its markers hold a buy ending 2026-09-28 of usd
    4,047.90 (n_trades 1, span false) and a sell ending 2026-09-29, each with the eight prescribed keys;
  - (d) the manifest's `charts` has an entry for TXUE and for BASG with uri (the object's address), bytes (the stored length),
    securities (the count, or the keys), markers (the count in the object) and thinned false;
  - (e) control: the page itself publishes on this fixture (status OK or PARTIAL; index.html, audit.html and manifest.json
    written), the check's own walk finds TXUE's section in 11 dialogs and BASG's in 10, and the fixture's G5 holds TXUE's S03 add
    ending 2026-09-28.
FAIL at base: (a), (b), (c), (d) FAIL (no dialog_fund_keys, no chart object, no manifest charts); (e) PASSES."""
import contextlib
import io
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY, ASOF = "2026-09-30", "2026-09-29"
RANGES = {"R30": "2026-08-30", "R90": "2026-07-01", "R365": "2025-09-29"}
TOP = {"fund", "asof", "generated_at", "ranges", "securities"}
SEC_KEYS = {"name", "source_words", "points", "gaps", "markers", "currency"}
MARKER_KEYS = {"side", "start", "end", "span", "usd", "bps", "r", "n_trades"}
FUNDS = ("TXUE", "BASG")


def fixture():
    """c.page_fixture() with BASG holding no S02, so the two funds' dialog sets differ. Returns (spec, sink)."""
    import os

    from rivalfunds import gold_trade_schedule, guardrails, sinks
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    os.environ[guardrails.OVERRIDE_ENV] = json.dumps({"min_resolved_fraction": 0.0})
    spec = f"local:{c.tmpdir('rv_co1_')}"
    s = sinks.get_sink(spec)
    for step, d in enumerate(("2026-09-25", "2026-09-28", tp2.DAY)):
        book = tp2._book(step)
        tp2._put(s, d, {"TXUE": (book, "bloomberg", 0.1 * step),
                        "BASG": ({k: q for k, q in book.items() if k != "S02"}, "issuer", 0.1 * step)})
    r = gold_trade_schedule.handler_entry({"date": tp2.DAY, "mode": "replay", "batch_id": "g", "sink": spec})
    assert r["status"] == "OK", r
    # round 16 (RIV-pc-1): a holding-implied price is drawn only for a listing stored as USD, so the fixture's securities carry a
    # G4 row holding `currency` USD and no px_close (every price stays holding-implied)
    import io as _io

    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import homes

    for d in ("2026-09-25", "2026-09-28", tp2.DAY):
        g4 = pd.DataFrame([{"security_id": k, "date": pd.Timestamp(d).date(), "px_close": float("nan"), "currency": "USD"}
                           for k in tp2._book(0)])
        buf = _io.BytesIO()
        pq.write_table(pa.Table.from_pandas(g4, preserve_index=False), buf)
        s.put(homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}", "part-20260930T000000Z-aaaaaaaaaaaa.parquet"),
              buf.getvalue())
    return spec, s


def publish(spec):
    from rivalfunds import publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = publish_page.handler_entry(tp2._ev(spec, day=DAY))
    return r, buf.getvalue()


def walk(html: str) -> dict:
    """This check's own read of the page: fund -> sorted security keys whose `data-sec-dialog` block carries its section."""
    out: dict = {}
    for seg in html.split('data-sec-dialog="')[1:]:
        key = seg.split('"', 1)[0]
        for f in re.findall(r"<section data-fund=[\"']?([A-Za-z0-9_]+)", seg):
            out.setdefault(f, set()).add(key)
    return {f: sorted(k) for f, k in out.items()}


def _json(s, uri):
    try:
        return json.loads(s.get(uri).decode("utf-8")) if s.exists(uri) else None
    except Exception as e:  # noqa: BLE001 -- an unreadable object is a failed arm, not a crash
        print("unreadable", uri, type(e).__name__, e)
        return None


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import homes, publish_page, render

    spec, s = fixture()
    r, out = publish(spec)
    idx_uri, aud_uri, man_uri = homes.page(DAY, "index.html"), homes.page(DAY, "audit.html"), homes.page(DAY, "manifest.json")
    html = s.get(idx_uri).decode("utf-8") if s.exists(idx_uri) else ""
    man = _json(s, man_uri) or {}
    mine = walk(html)
    print("publish:", r.get("status"), "| index.html", len(html.encode("utf-8")), "B | stdout FAIL lines:",
          [ln[:60] for ln in out.splitlines() if ln.startswith("FAIL:")])
    print("check's walk:", {f: len(k) for f, k in mine.items()}, "| S02 in TXUE:", "S02" in mine.get("TXUE", []),
          "| S02 in BASG:", "S02" in mine.get("BASG", []))

    home = next((m for m in (render, publish_page) if hasattr(m, "dialog_fund_keys")), None)
    theirs = None
    if home is not None:
        try:
            theirs = {str(f): sorted(str(k) for k in ks) for f, ks in (home.dialog_fund_keys(html) or {}).items() if ks}
        except Exception as e:  # noqa: BLE001
            print("dialog_fund_keys error:", type(e).__name__, e)
    print("dialog_fund_keys lives in:", getattr(home, "__name__", None), "| returns:",
          None if theirs is None else {f: len(k) for f, k in theirs.items()})
    v.check(bool(mine) and theirs == mine, "(a) dialog_fund_keys(html) equals the check's own walk of the dialog blocks")

    charts = {f: _json(s, homes.page(DAY, f"charts/{f}.json")) for f in FUNDS}
    written = sorted(u.rsplit("/", 1)[-1] for u in s.list(homes.page(DAY, "charts/")))
    print("objects under charts/:", written)
    ok_b = True
    for f in FUNDS:
        o = charts[f] if isinstance(charts[f], dict) else {}
        secs = o.get("securities") if isinstance(o.get("securities"), dict) else {}
        shape = all(isinstance(x, dict) and SEC_KEYS <= set(x) and isinstance(x.get("name"), str) and x["name"].strip()
                    and isinstance(x.get("source_words"), str) and x["source_words"].strip()
                    and isinstance(x.get("points"), list) and isinstance(x.get("gaps"), list) and isinstance(x.get("markers"), list)
                    for x in secs.values())
        print(f"  {f}: keys {sorted(o)} | fund {o.get('fund')} asof {o.get('asof')} generated_at {o.get('generated_at')!r} "
              f"ranges {o.get('ranges')} | securities {len(secs)} (dialog keys {len(mine.get(f, []))}) | per-security shape {shape}")
        ok_b = ok_b and (set(o) - {"thinned"} == TOP and o.get("fund") == f and o.get("asof") == ASOF
                         and isinstance(o.get("generated_at"), str) and bool(o["generated_at"].strip()) and o.get("ranges") == RANGES
                         and bool(secs) and sorted(secs) == mine.get(f) and shape)
    v.check(ok_b and "S02" in (charts["TXUE"] or {}).get("securities", {}) and "S02" not in (charts["BASG"] or {}).get("securities", {}),
            "(b) one chart object per fund at homes.page(day, 'charts/<FUND>.json') in the prescribed shape, covering exactly the "
            "securities whose dialog carries that fund's section")

    s03 = ((charts["TXUE"] or {}).get("securities") or {}).get("S03") or {}
    pts = [p for p in s03.get("points") or [] if isinstance(p, list) and len(p) == 3]
    dates = [str(p[0]) for p in pts]
    last = pts[-1] if pts else [None, None, None]
    gaps, marks = s03.get("gaps") or [], s03.get("markers") or []
    buys = [m for m in marks if isinstance(m, dict) and m.get("side") == "buy" and str(m.get("end"))[:10] == "2026-09-28"]
    sells = [m for m in marks if isinstance(m, dict) and m.get("side") == "sell" and str(m.get("end"))[:10] == "2026-09-29"]
    print("TXUE S03: points", len(s03.get("points") or []), "| first", dates[:1], "| last", last, "| gaps", len(gaps),
          "| markers", [(m.get("side"), m.get("end"), m.get("usd"), m.get("bps"), m.get("r"), m.get("n_trades"), m.get("span"))
                        for m in marks if isinstance(m, dict)])
    v.check(len(pts) == len(s03.get("points") or [None]) and dates == sorted(dates) and len(set(dates)) == len(dates)
            and dates[:1] == [RANGES["R365"]] and dates[-1:] == [ASOF] and last[2] == "i" and isinstance(last[1], (int, float))
            and abs(last[1] - 13.2) < 1e-6 and all(p[2] in ("m", "i", None) and (p[1] is None) == (p[2] is None) for p in pts)
            and bool(gaps) and all(isinstance(g, dict) and {"start", "end", "reason"} <= set(g) for g in gaps)
            and len(buys) == 1 and abs(float(buys[0].get("usd") or 0) - 4047.9) < 0.01 and buys[0].get("n_trades") == 1
            and buys[0].get("span") is False and len(sells) == 1 and all(set(m) == MARKER_KEYS for m in buys + sells),
            "(c) TXUE's S03: points ascend 2025-09-29 .. 2026-09-29 as [date, price|null, code], 09-29 is 13.2 holding-implied, "
            "gaps carry their reason, and the markers hold the 09-28 buy of 4,047.90 and the 09-29 sell")

    mc = man.get("charts") if isinstance(man.get("charts"), dict) else {}
    ok_d = bool(mc)
    for f in FUNDS:
        e = mc.get(f) if isinstance(mc.get(f), dict) else {}
        uri = homes.page(DAY, f"charts/{f}.json")
        stored = len(s.get(uri)) if s.exists(uri) else None
        secs = ((charts[f] or {}).get("securities") or {}) if isinstance(charts[f], dict) else {}
        n_mark = sum(len(x.get("markers") or []) for x in secs.values() if isinstance(x, dict))
        print(f"  manifest charts[{f}]:", {k: (x if not isinstance(x, list) else f"<{len(x)} items>") for k, x in e.items()},
              "| stored bytes", stored, "| object securities", len(secs), "| object markers", n_mark)
        sec_ok = e.get("securities") == len(secs) or (isinstance(e.get("securities"), list) and sorted(e["securities"]) == sorted(secs))
        ok_d = ok_d and (set(e) >= {"uri", "bytes", "securities", "markers", "thinned"} and e.get("uri") == uri
                         and stored is not None and e.get("bytes") == stored and bool(secs) and sec_ok
                         and e.get("markers") == n_mark and n_mark > 0 and e.get("thinned") is False)
    v.check(ok_d, "(d) the manifest's charts entry of each fund carries uri, bytes, securities, markers and thinned false, "
                  "agreeing with the stored object")

    g5_uri = next((u for u in s.list(homes.trade_schedule("2026-09-28")) if u.endswith(".parquet")), None)
    g5 = pq.read_table(io.BytesIO(s.get(g5_uri))).to_pandas() if g5_uri else None
    add = [] if g5 is None else [(x.action, round(float(x.est_notional), 2)) for x in g5.itertuples()
                                 if x.fund_ticker == "TXUE" and x.security_key == "S03"]
    print("control: status", r.get("status"), "| index", s.exists(idx_uri), "audit", s.exists(aud_uri), "manifest", s.exists(man_uri),
          "| G5 TXUE S03 window ending 09-28:", add)
    v.check(r.get("status") in ("OK", "PARTIAL") and s.exists(idx_uri) and s.exists(aud_uri) and s.exists(man_uri)
            and man.get("page_date") == DAY and len(mine.get("TXUE", [])) == 11 and len(mine.get("BASG", [])) == 10
            and "S02" in mine["TXUE"] and "S02" not in mine["BASG"] and add == [("add", 4047.9)],
            "(e) control: the page publishes on the fixture, TXUE's section is in 11 dialogs and BASG's in 10, and G5 holds "
            "TXUE's S03 add ending 2026-09-28")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
