"""RIV-g-4 AC3 -- a PLANTED income-funded purchase is a trade LABELLED income_funded: in a copy of the newest real capture
one real USD-denominated TXUE holding is increased by 10% (notional N at its implied price), and a G3 cash_div record for
another real USD TXUE holding (ex-date inside the window) is imported with an amount whose receipt (amount x shares held)
is >= N; G5 then shows that add with income_funded true. Control: the same add with NO dividend record reads
income_funded false."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def plant(files, with_income):
    prev, cur = files[-2], files[-1]
    d = c.capture(cur)
    rows, hdr = d["rows"], d["rows"][0]
    ii, fi, pi, ci, mi = (hdr.index(k) for k in ("ID", "ORIG_IDS", "POSITION", "CURRENCY", "REPORTED_MKT_VAL"))
    usd = [k for k, r in enumerate(rows[1:], 1) if str(r[fi]).startswith("TXUE") and r[ci] == "USD"
           and not str(r[ii]).endswith(" Curncy") and (r[pi] or 0) > 0 and (r[mi] or 0) > 0]
    a, b = usd[0], usd[1]
    buy_sec, div_sec = rows[a][ii], rows[b][ii]
    px = rows[a][mi] / rows[a][pi]
    notional = 0.10 * rows[a][pi] * px
    rows[a] = list(rows[a])
    rows[a][pi] = rows[a][pi] * 1.10
    rows[a][mi] = rows[a][pi] * px
    tmp = pathlib.Path(c.tmpdir("rv_g53p_"))
    pcap = tmp / cur.name
    pcap.write_text(json.dumps({**d, "rows": rows}), encoding="utf-8")
    sink = c.tmpdir("rv_g53_")
    c.import_bloomberg(sink, [prev, pcap])
    date = d["requested_date"]
    c.replay("silver_bloomberg", sink, date)
    c.replay("gold_canonical_shape", sink, date)
    from rivalfunds import enrichment_bloomberg

    per_share = 1.25 * notional / rows[b][pi]
    recs = [{"Declared Date": date, "Ex-Date": date, "Record Date": date, "Payable Date": date, "Dividend Amount": per_share,
             "Dividend Frequency": "Irreg", "Dividend Type": "Special Cash"}] if with_income else []
    dj = tmp / "planted_income.json"
    dj.write_text(json.dumps({"start": "20240901", "end": "20260930", "securities": 1, "missing": [],
                              "data": {div_sec: {"DVD_HIST_ALL": recs}}}), encoding="utf-8")
    enrichment_bloomberg.handler_entry({"mode": "import", "dividends_json": str(dj), "batch_id": "chk-inc",
                                        "sink": f"local:{sink}", "date": date})
    c.replay("gold_trade_schedule", sink, date)
    t, _ = c.read_parquets(c.gold_dir(sink, "trade_schedule"))
    hit = t[(t["fund_id"] == "TXUE") & (t["security_id"].astype(str) == buy_sec)] if len(t) else t
    return hit, buy_sec


def run(v):
    c.setup_path()
    files = c.idvz_captures(2)
    hit, sec = plant(files, with_income=True)
    v.check(len(hit) >= 1, f"the planted add on {sec} is a trade ({len(hit)} row(s))")
    v.check(len(hit) and bool(hit["income_funded"].any()), f"income_funded true with income in the window ({list(hit.get('income_funded', []))})")
    ctl, _ = plant(files, with_income=False)
    v.check(len(ctl) >= 1 and not bool(ctl["income_funded"].any()), f"control: income_funded false without income ({list(ctl.get('income_funded', []))})")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
