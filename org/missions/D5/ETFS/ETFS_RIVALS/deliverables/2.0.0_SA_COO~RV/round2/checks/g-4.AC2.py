"""RIV-g-4 AC2 -- a PLANTED 2-for-1 split never reads as a trade: in a copy of the newest real capture one real TXUE holding's
position is doubled, and a G3 'Stock Split' record (Dividend Amount 2.0) with ex-date inside that window is imported; G5
then has NO trade for that security in that window, and G6 records corporate_action_count >= 1 for TXUE's window. Control:
the same doubling WITHOUT the split record reads as a trade (an add)."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def plant(files, with_split):
    prev, cur = files[-2], files[-1]
    d = c.capture(cur)
    rows, hdr = d["rows"], d["rows"][0]
    ii, fi, pi = hdr.index("ID"), hdr.index("ORIG_IDS"), hdr.index("POSITION")
    idx = next(k for k, r in enumerate(rows[1:], 1)
               if str(r[fi]).startswith("TXUE") and not str(r[ii]).endswith(" Curncy") and (r[pi] or 0) > 0)
    sec = rows[idx][ii]
    rows[idx] = list(rows[idx])
    rows[idx][pi] = rows[idx][pi] * 2
    tmp = pathlib.Path(c.tmpdir("rv_g52p_"))
    pcap = tmp / cur.name
    pcap.write_text(json.dumps({**d, "rows": rows}), encoding="utf-8")
    sink = c.tmpdir("rv_g52b_")
    c.import_bloomberg(sink, [prev, pcap])
    date = d["requested_date"]
    c.replay("silver_bloomberg", sink, date)
    c.replay("gold_canonical_shape", sink, date)
    from rivalfunds import enrichment_bloomberg

    divs = {"start": "20240901", "end": "20260930", "securities": 1, "missing": [],
            "data": {sec: {"DVD_HIST_ALL": ([{"Declared Date": date, "Ex-Date": date, "Record Date": date, "Payable Date": date,
                                               "Dividend Amount": 2.0, "Dividend Frequency": "Irreg",
                                               "Dividend Type": "Stock Split"}] if with_split else [])}}}
    dj = tmp / "planted_dividends.json"
    dj.write_text(json.dumps(divs), encoding="utf-8")
    enrichment_bloomberg.handler_entry({"mode": "import", "dividends_json": str(dj), "batch_id": "chk-plant",
                                        "sink": f"local:{sink}", "date": date})
    c.replay("gold_trade_schedule", sink, date)
    return sink, sec, date


def run(v):
    c.setup_path()
    files = c.idvz_captures(2)
    sink, sec, date = plant(files, with_split=True)
    t, _ = c.read_parquets(c.gold_dir(sink, "trade_schedule"))
    g6, _ = c.read_parquets(c.gold_dir(sink, "flow_reconciliation"))
    hit = t[(t["fund_id"] == "TXUE") & (t["security_id"].astype(str) == sec)] if len(t) else t
    v.check(len(hit) == 0, f"split: no TXUE trade on {sec} ({len(hit)} found)")
    cac = g6[g6["fund_id"] == "TXUE"]["corporate_action_count"] if len(g6) and "corporate_action_count" in g6.columns else []
    v.check(len(cac) and int(max(cac)) >= 1, f"G6 TXUE corporate_action_count {list(cac)}")
    sink2, sec2, _ = plant(files, with_split=False)
    t2, _ = c.read_parquets(c.gold_dir(sink2, "trade_schedule"))
    ctl = t2[(t2["fund_id"] == "TXUE") & (t2["security_id"].astype(str) == sec2)] if len(t2) else t2
    v.check(len(ctl) >= 1 and "add" in set(ctl.get("action", [])), f"control (no split record): the doubling reads as an add ({list(ctl.get('action', []))})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
