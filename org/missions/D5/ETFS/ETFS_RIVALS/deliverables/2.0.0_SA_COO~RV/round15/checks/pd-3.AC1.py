"""RIV-pd-3 AC1 (FWD-23; F.2 last bullet; ROUND15_CELLS_DRAFT.md revision 1.5): the AI accounts are written on the same three
periods as the page -- R30, R90, R365 -- and name no MTD, QTD or YTD.

Measured today (CLOUD 90e794e816): `ai_accounts.fact_pack` builds its contribution facts from
`("R30",5),("MTD",3),("QTD",3),("YTD",3)` (:165) and its trend facts from the YTD rows (:175-184, id `Y-...`, text "year to date
leaned ...", key `<fund>|YTD|<bucket>`); the module has no `PACK_PERIODS`.

Interface (prescribed, verbatim from the cell): the fact pack is built from `("R30",5),("R90",3),("R365",3)` and the R365 trend
rows; fact keys read `<fund>|R90|<bucket>` / `<fund>|R365|<bucket>`; no fact label names MTD, QTD or YTD; the prompt text names
the three periods in plain words (last 30 / 90 / 365 days). `ai_accounts.PACK_PERIODS = ("R30","R90","R365")` is the one constant.
Fixture (no vendor call, no sink): fund TXUE on 2026-10-02; one trade (round 5's `ai2_tables` G5 / G6); security-axis
holding_contribution rows for SIX periods (R30, R90, R365, MTD, QTD, YTD), four securities each, every contribution value
distinct per period; buying_trend rows carrying a `period` column -- one R365 row (Epsilon Corp, net 7777.0) and one YTD row
(Zeta Corp, net 3000.0). The prompt text is read from the messages `run_chain` hands a recording stub client.
  - (a) `ai_accounts.PACK_PERIODS == ("R30", "R90", "R365")`;
  - (b) the pack cites holding_contribution `TXUE|R90|<bucket>` and `TXUE|R365|<bucket>` for the top three and bottom three of
    each (all four fixture securities), each value copied from that period's own row;
  - (c) no fact cites a key of period MTD, QTD or YTD; and no fact id, no fact text and no message sent to the client contains
    "MTD", "QTD", "YTD", "month to date", "quarter to date" or "year to date" (case-insensitive);
  - (d) the trend facts come from the R365 rows: the buying_trend citations are exactly {`TXUE|R365|Epsilon Corp`: 7777.0};
  - (e) the prompt text outside the FACTS and READINGS lines names 30, 90 and 365 days (digits or words);
  - (f) control: the R30 facts are present (five-deep rule on four securities: `TXUE|R30|<bucket>` for all four, ids
    `C-R30-best1` and `C-R30-worst1`) and the trade fact T1 is in the pack.
FAIL at base: (a), (b), (c), (d), (e) FAIL (no constant; MTD / QTD / YTD facts; YTD trend; "thirty days" only); (f) PASSES."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

h = c._r11  # round 11's helpers (the A1 / AI fixtures round 14's _common does not re-export)
FUND, DAY = "TXUE", h.AI_DAY
SECS = ("Alpha Corp", "Beta Corp", "Gamma Corp", "Delta Corp")
# one distinct base per period, so a value names the period row it was copied from
BASE = {"R30": 0.0100, "R90": 0.0200, "R365": 0.0300, "MTD": 0.0400, "QTD": 0.0500, "YTD": 0.0600}
BANNED = ("mtd", "qtd", "ytd", "month to date", "quarter to date", "year to date")
WORDS = {"30": r"\b(30|thirty)\b", "90": r"\b(90|ninety)\b",
         "365": r"\b(365|three[ -]hundred[ -](and[ -])?sixty[ -]five)\b"}


def values(period):
    return {s: round(BASE[period] + 0.0011 * (len(SECS) - i), 6) for i, s in enumerate(SECS)}


def fixture():
    import pandas as pd
    g5, g6, _hc, _bt = h.ai2_tables()
    rows = []
    for p in BASE:
        rows += h.contribution_rows(FUND, p, values(p))
    for r in rows:
        r["fund_ticker"] = FUND
    trend = [{"fund_id": FUND, "role": "rival", "period": p, "window_start": "2025-10-02", "window_end": DAY,
              "n_trading_days": 250, "axis": "security", "bucket": b, "security_name": b, "net_notional_base": net,
              "n_windows": 3, "lean": "into", "rank": 1, "reading": "tilt", "trend_mark": "+ + + 0 0 0 0 0 0 0",
              "n_refused_windows": 0, "claim": "INFERRED", "revision": "bt1"}
             for p, b, net in (("R365", "Epsilon Corp", 7777.0), ("YTD", "Zeta Corp", 3000.0))]
    return g5, g6, pd.DataFrame(rows), pd.DataFrame(trend)


def banned_in(text):
    low = str(text).lower()
    return [w for w in BANNED if w in low]


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import ai_accounts as ai

    g5, g6, hc, bt = fixture()
    facts = ai.fact_pack(FUND, DAY, g5, g6, hc, bt)
    cites = [f["cited_row"] for f in facts]
    hc_keys = {r["key"]: r["value"] for r in cites if r["table"] == "holding_contribution"}
    bt_keys = {r["key"]: r["value"] for r in cites if r["table"] == "buying_trend"}
    periods = sorted({k.split("|")[1] for k in list(hc_keys) + list(bt_keys)})
    print(f"facts: {len(facts)} | ids: {[f['id'] for f in facts]}")
    print("periods cited (holding_contribution + buying_trend):", periods)

    pack = getattr(ai, "PACK_PERIODS", None)
    print("PACK_PERIODS:", pack)
    v.check(pack == ("R30", "R90", "R365"), '(a) ai_accounts.PACK_PERIODS == ("R30", "R90", "R365")')

    want = {p: {f"{FUND}|{p}|{s}": val for s, val in values(p).items()} for p in ("R90", "R365")}
    got = {p: {k: val for k, val in hc_keys.items() if k.split("|")[1] == p} for p in ("R90", "R365")}
    print("R90 facts:", got["R90"])
    print("R365 facts:", got["R365"])
    v.check(got == want, "(b) the pack cites <fund>|R90|<bucket> and <fund>|R365|<bucket>, each value from its own period's row")

    # the messages run_chain hands the client (a recording stub: no vendor call)
    sent, chain_err = [], None
    try:
        client = h.StubClient([h.ai2_reply("TXUE added to its book.", []), h.ai2_reply("The trend is borne out.", [])])
        ai.run_chain(FUND, "rival", DAY, facts, h.ai2_readings(), client, "run-pd3", model="stub-model")
        sent = [m["content"] for call in client.calls for m in call if m.get("role") in ("system", "user")]
        print("client.chat calls:", len(client.calls), "| web searches:", len(client.web))
    except Exception as e:  # noqa: BLE001 -- a chain that raises fails the prompt arms, not the fact arms
        chain_err = f"{type(e).__name__}: {e}"
        print("run_chain raised:", chain_err)
    prompt_all = "\n".join(dict.fromkeys(sent))

    old_keys = sorted(k for k in list(hc_keys) + list(bt_keys) if k.split("|")[1] in ("MTD", "QTD", "YTD"))
    bad_facts = sorted({f["id"] for f in facts if banned_in(f["id"]) or banned_in(f["text"])})
    bad_prompt = banned_in(prompt_all)
    print(f"keys of MTD/QTD/YTD: {len(old_keys)} {old_keys[:4]} | facts naming a banned period: {len(bad_facts)} {bad_facts[:6]}"
          f" | banned words in the sent prompt text: {bad_prompt}")
    v.check(not old_keys and not bad_facts and bool(prompt_all) and not bad_prompt,
            "(c) no fact keyed MTD / QTD / YTD; no fact id, fact text or sent prompt names MTD, QTD, YTD or their long forms")

    print("buying_trend citations:", bt_keys)
    v.check(bt_keys == {f"{FUND}|R365|Epsilon Corp": 7777.0}, "(d) the trend facts come from the R365 rows only")

    frame = "\n".join(ln for ln in prompt_all.splitlines() if not ln.startswith("- "))   # drop the FACTS and READINGS lines
    named = {k: bool(re.search(rx, frame, re.I)) for k, rx in WORDS.items()}
    print("prompt text names (30, 90, 365):", named, "| says 'days':", "days" in frame.lower(), "| chain error:", chain_err)
    v.check(all(named.values()) and "days" in frame.lower(),
            "(e) the prompt text names the three periods in plain words (last 30 / 90 / 365 days)")

    r30 = {k: val for k, val in hc_keys.items() if k.split("|")[1] == "R30"}
    ids = {f["id"] for f in facts}
    print("R30 facts:", r30, "| trade facts:", sorted(i for i in ids if i.startswith("T")))
    v.check(r30 == {f"{FUND}|R30|{s}": val for s, val in values("R30").items()} and {"C-R30-best1", "C-R30-worst1", "T1"} <= ids,
            "(f) control: the R30 contribution facts and the trade fact are in the pack")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
