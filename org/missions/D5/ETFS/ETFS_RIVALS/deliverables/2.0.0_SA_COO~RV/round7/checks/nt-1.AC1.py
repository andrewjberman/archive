"""RIV-nt-1 AC1 (ROUND_ANALYSIS.round6.md section 3 item 5): ONE deterministic tie-break in the name pick. Two names
for one security key on the SAME newest report date give the same pick whatever the row order, in BOTH producers.
Source: the round-6 served-delta measurement (C:/tmp/r6measure/a1_compare.json): 57 holding_contribution and 17
buying_trend `security_name` cells differ between the Lambda build and a local run of the same code with no newer
input, each a pair of real names for one key (e.g. TSM_US_Equity "TAIWAN SEMICONDUCTOR-SP ADR" against "Taiwan
Semiconductor Manufacturing Co Ltd"). Base ed61068340: the newest-name map `identity_maps` sorts the G1 rows by
report date (`gold_holding_contribution.py:159`, pandas `sort_values`, quicksort, not stable past 16 rows) and the
LAST non-blank name of the newest date wins (`:165`), so a same-date tie resolves by row order. holding_contribution
reads it as `display_name([own name, map name])` (`:413`); buying_trend as `display_name([map name])`
(`gold_buying_trend.py:160`, `:223`). This check proves the pick follows row order; it does not prove which order
difference split the Lambda and the local run.

Tie-break (prescribed): among the non-blank names on the key's newest report date carrying a name, the map holds
`names.display_name(sorted(set(candidates)))`: the longest real name (a 30-character cut ranks below), ties to the
code-point-smallest candidate. Older dates never compete. Interface: `gold_holding_contribution.identity_maps(g1)`,
`gold_holding_contribution.build(g1, g4, day, universe_entries)` and `gold_buying_trend.build(g5, g6, g1, day,
universe_entries)`, signatures unchanged; a fund's own name still comes first in holding_contribution.

Pure, offline frames (page day 2026-10-02). TXUE (Bloomberg-sourced: no security_name) holds S1, S2, S3 on 09-30 and
10-01, with one G5 add of each (window end 09-30). Names come only from the issuer funds:
  S1 TSM_US_Equity  09-30: BASG "TAIWAN SEMICONDUCTOR-SP ADR", BIDD "Taiwan Semiconductor Manufacturing Co Ltd";
  S2 GOOG_US_Equity 09-30: BASG "ALPHABET INC-CL C", BIDD "Alphabet Inc Cl C" (equal length: the code-point arm);
  S3 NEWC_US_Equity 09-29: BASG "Old Name Corporation Holdings Plc"; 09-30: BIDD "New Name Corp" (control).
The G1 rows are fed in four orders: as built, reversed, and two seeded shuffles.
  - (a) holding_contribution: every security-axis name cell is the same under all four orders;
  - (b) buying_trend: every security-axis name cell is the same under all four orders;
  - (c) TXUE's S1 and S2 read display_name(sorted(candidates)) in BOTH producers under every order;
  - (d) control, different dates: TXUE's S3 reads "New Name Corp" (the newest date's name, though the older is
    longer) in both producers under every order.
FAIL at base: (a), (b), (c) FAIL (the reversed order flips S1 and S2); (d) PASS."""
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE = "2026-10-02"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"},
           {"group_id": "IDVZ", "fund_id": "BIDD", "role": "rival"},
           {"group_id": "PFOE", "fund_id": "BASG", "role": "rival"}]
S1, S2, S3 = "TSM_US_Equity", "GOOG_US_Equity", "NEWC_US_Equity"
TIES = {S1: ("TAIWAN SEMICONDUCTOR-SP ADR", "Taiwan Semiconductor Manufacturing Co Ltd"),
        S2: ("ALPHABET INC-CL C", "Alphabet Inc Cl C")}
NEW = "New Name Corp"


def g1_frame():
    import pandas as pd
    base = {"is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0, "weight": 0.3,
            "raw_identifier": None, "gics_sector": None}
    rows = [dict(base, fund_id="TXUE", fund_ticker="TXUE", report_date=d, security_id=k, security_name=None,
                 market_value=1000.0 + 10.0 * i)
            for i, d in enumerate(("2026-09-30", "2026-10-01")) for k in (S1, S2, S3)]
    for f, j in (("BASG", 0), ("BIDD", 1)):
        rows += [dict(base, fund_id=f, fund_ticker=f, report_date="2026-09-30", security_id=k, security_name=TIES[k][j],
                      market_value=1000.0) for k in (S1, S2)]
    rows.append(dict(base, fund_id="BASG", fund_ticker="BASG", report_date="2026-09-29", security_id=S3,
                     security_name="Old Name Corporation Holdings Plc", market_value=1000.0))
    rows.append(dict(base, fund_id="BIDD", fund_ticker="BIDD", report_date="2026-09-30", security_id=S3,
                     security_name=NEW, market_value=1000.0))
    return pd.DataFrame(rows)


def orders(g1):
    idx = list(range(len(g1)))
    out = {"as built": idx, "reversed": idx[::-1]}
    for seed in (7, 11):
        p = idx[:]
        random.Random(seed).shuffle(p)
        out[f"shuffle {seed}"] = p
    return {k: g1.iloc[p].reset_index(drop=True) for k, p in out.items()}


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds.names import display_name

    g4 = pd.DataFrame(columns=["security_id", "date", "px_close", "total_return_index", "gics_sector"])
    g5 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": k, "security_key": k, "action": "add",
                        "window_end": "2026-09-30", "est_notional_base": 1e6 * (i + 1)}
                       for i, k in enumerate((S1, S2, S3))])
    g6 = pd.DataFrame(columns=["fund_id", "fund_ticker", "window_end", "status", "reason"])
    hc_by, bt_by = {}, {}
    for name, g1 in orders(g1_frame()).items():
        h = hc.build(g1, g4, PAGE, ENTRIES)
        h = h[h.axis == "security"]
        hc_by[name] = {(r.fund_id, r.period, r.bucket): r.security_name for r in h.itertuples()}
        b = bt.build(g5, g6, g1, PAGE, ENTRIES)
        b = b[b.axis == "security"]
        bt_by[name] = {(r.fund_id, r.lean, r.bucket): r.security_name for r in b.itertuples()}
    want = {k: display_name(sorted(set(TIES[k]))) for k in TIES}
    want[S3] = display_name([NEW])
    print("prescribed picks:", want)

    def diff(by):
        ref = by["as built"]
        return {o: sorted(k for k in set(ref) | set(m) if ref.get(k) != m.get(k))
                for o, m in by.items() if o != "as built"}

    for label, by in (("holding_contribution", hc_by), ("buying_trend", bt_by)):
        for o, m in by.items():
            print(f"{label} [{o}] TXUE:",
                  {k[2]: n for k, n in sorted(m.items()) if k[0] == "TXUE" and k[1] in ("MTD", "into")})
    dh, db = diff(hc_by), diff(bt_by)
    print("holding_contribution cells that move with the row order:", {o: len(x) for o, x in dh.items()})
    print("buying_trend cells that move with the row order:", {o: len(x) for o, x in db.items()})
    v.check(bool(hc_by["as built"]) and not any(dh.values()),
            "(a) holding_contribution: every security-axis name cell is the same under all four row orders")
    v.check(bool(bt_by["as built"]) and not any(db.values()),
            "(b) buying_trend: every security-axis name cell is the same under all four row orders")

    def txue(by, key):
        return {n for m in by.values() for k, n in m.items() if k[0] == "TXUE" and k[2] == key}

    v.check(all(txue(by, k) == {want[k]} for by in (hc_by, bt_by) for k in (S1, S2)),
            f"(c) TXUE's S1 and S2 read display_name(sorted(candidates)) in both producers under every order "
            f"(S1 {sorted(txue(hc_by, S1) | txue(bt_by, S1))}, S2 {sorted(txue(hc_by, S2) | txue(bt_by, S2))})")
    v.check(all(txue(by, S3) == {want[S3]} for by in (hc_by, bt_by)),
            "(d) control: TXUE's S3 reads the newest date's name 'New Name Corp' in both producers under every order")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
