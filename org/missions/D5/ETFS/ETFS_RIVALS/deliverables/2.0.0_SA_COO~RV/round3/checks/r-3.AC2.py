"""RIV-r-3 AC2 -- the narrowed enrichment gate (row W5-S23; analysis ruling 2): a signed-out morning still builds G5 for
every fund whose trade window touches NO corporate action, and holds only the funds whose window does.

Real data: the last 4 IDVZ-group captures through canonical_shape in a local sink; G3 imported from a COPY of the real
dividends.json in which one real holding ONLY TXUE holds across the batch (amendment 1, row W2-S6) gains a 'Stock Split' (amount 2.0) ex-dated on the
newest requested date. The pull-enrichment marker is partitioned at the OLDEST capture's date, so it does NOT cover the
batch's newest report date (the round-2 gate would hold the whole batch). Then sweep.run_gold_chain runs the real stages:
  - build-trade-schedule is NOT skipped and writes a G5 object for the newest date;
  - the result's detail.held_funds names TXUE with a non-empty reason;
  - no held fund has a G5 row; at least one fund that is not held does (the narrowing, not a disabled gate);
  - held_funds is a strict subset of the funds in the batch."""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def planted_dividends(files: list) -> tuple[pathlib.Path, str]:
    """Plant on a security ONLY TXUE holds across the batch's captures (amendment 1, row W2-S6: a security shared with
    other funds held every fund, so no un-held fund was left to build)."""
    other = set()
    for f in files:
        dd = c.capture(f)
        h = dd["rows"][0]
        for r in dd["rows"][1:]:
            if not str(r[h.index("ORIG_IDS")]).startswith("TXUE"):
                other.add(r[h.index("ID")])
    d = c.capture(files[-1])
    rows, hdr = d["rows"], d["rows"][0]
    ii, fi = hdr.index("ID"), hdr.index("ORIG_IDS")
    sec = next(r[ii] for r in rows[1:] if str(r[fi]).startswith("TXUE") and not str(r[ii]).endswith(" Curncy")
               and r[ii] not in other and not re.fullmatch(r"\d+D", str(r[ii]).split(" ")[0]))  # 9996651D-class = cash
    div = json.loads(c.dividends_path().read_text(encoding="utf-8"))
    rec = {"Declared Date": d["requested_date"], "Ex-Date": d["requested_date"], "Record Date": d["requested_date"],
           "Payable Date": d["requested_date"], "Dividend Amount": 2.0, "Dividend Frequency": "None",
           "Dividend Type": "Stock Split"}
    div["data"].setdefault(sec, {"DVD_HIST_ALL": []})
    div["data"][sec].setdefault("DVD_HIST_ALL", []).append(rec)
    out = pathlib.Path(c.tmpdir("rv_r3a2d_")) / "dividends_planted.json"
    out.write_text(json.dumps(div), encoding="utf-8")
    return out, sec


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg, sweep

    files = c.idvz_captures(4)
    sink = c.tmpdir("rv_r3a2_")
    c.run_idvz_chain(sink, files, "canonical")
    newest = c.capture(files[-1])["requested_date"]
    oldest = c.capture(files[0])["requested_date"]
    planted, sec = planted_dividends(files)
    print("planted split on", sec, "ex", newest, "; pull-enrichment marker at", oldest)
    enrichment_bloomberg.handler_entry({"mode": "import", "dividends_json": str(planted), "batch_id": "r3-g3",
                                        "sink": f"local:{sink}", "date": oldest})
    res = sweep.run_gold_chain({"date": newest, "mode": "replay", "batch_id": "r3-chain", "sink": f"local:{sink}"})
    print("chain:", json.dumps(res.get("detail"), default=str)[:600])
    held = (res.get("detail") or {}).get("held_funds")
    v.check(isinstance(held, dict), f"detail.held_funds present ({type(held).__name__})")
    held = held if isinstance(held, dict) else {}
    v.check(bool(held.get("TXUE")), f"TXUE held with a reason ({held.get('TXUE')!r})")
    g5 = c.gold_dir(sink, "trade_schedule") / f"date={newest}"
    df, n = c.read_parquets(g5)
    v.check(n >= 1, f"a G5 object for {newest} ({n})")
    funds_in_g5 = set(df["fund_id"].astype(str)) if len(df) and "fund_id" in df.columns else set()
    print("G5 funds:", sorted(funds_in_g5), "held:", sorted(held))
    v.check(not (funds_in_g5 & set(held)), f"no held fund has a G5 row ({sorted(funds_in_g5 & set(held))})")
    v.check(bool(funds_in_g5 - set(held)), "at least one fund that is not held has G5 rows")
    batch_funds = set(c.capture_rows_by_fund(files[-1])) - {None}
    v.check(set(held) < batch_funds, f"held_funds is a strict subset of the batch's funds ({sorted(held)} < {sorted(batch_funds)})")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
