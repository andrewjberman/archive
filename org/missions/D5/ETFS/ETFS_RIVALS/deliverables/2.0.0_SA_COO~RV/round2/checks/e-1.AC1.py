"""RIV-e-1 AC1 -- the real DVD_HIST_ALL pull (dividends.json, 738 securities, CRO~Z's scripted R-21 run) imports into G3
corporate_actions in a local sink with nothing dropped: one G3 row per dividend record in the file; the event_type mapping is
TOTAL over the file's raw types (an unmapped type is carried as unmapped:<raw>, never lost); each share-changing type's
count equals the file's raw count (Stock Split -> split, Stock Dividend -> stock_div, Spinoff -> spinoff, Bonus -> bonus,
Rights Issue -> rights); the provenance columns and a claim are present."""
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

SHARE_CHANGING = {"Stock Split": "split", "Stock Dividend": "stock_div", "Spinoff": "spinoff", "Bonus": "bonus",
                  "Rights Issue": "rights"}


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg

    src = c.dividends_path()
    d = json.loads(src.read_text(encoding="utf-8"))
    raw = collections.Counter()
    n_rec = 0
    for sec, body in d["data"].items():
        recs = body.get("DVD_HIST_ALL") if isinstance(body, dict) else None
        if isinstance(recs, list):
            for r in recs:
                n_rec += 1
                raw[r.get("Dividend Type")] += 1
    print(f"file: {len(d['data'])} securities, {n_rec} dividend records, raw types {dict(raw)}")
    sink = c.tmpdir("rv_e1_")
    r = enrichment_bloomberg.handler_entry({"mode": "import", "dividends_json": str(src), "batch_id": "chk-e1",
                                           "sink": f"local:{sink}", "date": "2026-09-30"})
    print("r:", str(r)[:300])
    df, n = c.read_parquets(c.gold_dir(sink, "corporate_actions"))
    v.check(n >= 1, f"G3 objects written: {n}")
    events = df[df["event_type"].notna()] if "event_type" in df.columns else df.iloc[0:0]
    v.check(len(events) == n_rec, f"one G3 row per dividend record ({len(events)} == {n_rec})")
    got = collections.Counter(events["event_type"]) if len(events) else collections.Counter()
    for rawt, et in SHARE_CHANGING.items():
        v.check(got.get(et, 0) == raw.get(rawt, 0), f"{rawt} -> {et}: {got.get(et, 0)} == file {raw.get(rawt, 0)}")
    unmapped_raw = [t for t in raw if t not in SHARE_CHANGING]
    covered = sum(got.values())
    v.check(covered == n_rec, f"mapping total: {covered} typed rows of {n_rec} (non-share-changing raw types {unmapped_raw})")
    for col in ["security_id", "event_type", "ex_date", "amount", "revision", "produced_at", "producer_version",
                "input_manifest", "claim"]:
        v.check(col in df.columns, f"column {col}")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
