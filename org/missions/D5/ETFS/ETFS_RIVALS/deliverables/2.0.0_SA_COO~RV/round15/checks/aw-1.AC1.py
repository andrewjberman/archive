"""RIV-aw-1 AC1 -- WORDS, NOT CODES (cell items 1, 2 and the wording half of 4 and 5; CTO rulings R19, R20; rows C-S83).

An AI account names its periods in words with the window's two ISO dates and never by the codes R30 / R90 / R365 (nor MTD / QTD /
YTD); a reply that does not is corrected ONCE; a reply still wrong after the correction is stored FAIL with a `wording: ` reason.

NO network, NO model call, NO S3: the client is a recording stub, the facts are built by the module's own `fact_pack` on small
pandas frames, `_common.offline_guards()` refuses boto3 and `requests.post`.

THE INTERFACE THIS CHECK READS (the contract for the builder; `data/etfs/scripts/rivalfunds/ai_accounts.py` only):
  - `PROMPT_VERSION` (str) and `SYSTEM` (str) module constants; `SCHEMA` (the 17 stored columns, unchanged).
  - `fact_pack(fund_id, day, g5, g6, contribution, trend)` -> `[{id, text, value, cited_row: {table, key, revision, value}}]`,
    called with today's six arguments. A fact's `text` carries no period code; its `id` and `cited_row["key"]` may.
  - `run_chain(fund_id, role, day, facts, readings, client, run_id, model=...)` -> the two stored rows (kinds `activity_30d` and
    `direction_verdict`), called with TODAY'S signature and the facts `fact_pack` returned. FIXED DETAIL 1: the window dates the
    prompts name must therefore be derivable from `facts` (or from `day`); the check passes no extra `windows` argument.
  - FIXED DETAIL 2 (the windows of the fixture): the contribution rows carry `period_start` / `period_end` per period -- R30
    2026-09-02 to 2026-10-02, R90 2026-07-04 to 2026-10-02, R365 2025-10-02 to 2026-10-02 (each start is the page day minus 30 /
    90 / 365 calendar days, the end is the page day 2026-10-02), so a build that reads the dates off the rows and a build that
    computes them from `day` in calendar days name the same dates. A build on the 30 NYSE TRADING-day window does not.
  - `wording_check(text_fields, windows) -> list[str]` (empty = clean), pure. FIXED DETAIL 3 (argument shapes):
    `text_fields` is a dict `{"text": str, "observed": [str], "inferred": [str], "invalidation": str or None}`; `windows` is a
    LIST of `(start_iso, end_iso)` pairs -- the item's own window(s), every date of which must be in `text`. A reason for a code
    names that code (any case).
  - the stub client: `chat(messages, model) -> str` (one JSON object `{"text", "observed", "inferred", "cited",
    "invalidation"}`) and `web_search(query, model) -> {"text", "urls"}`. It records every call and answers by the SHAPE of the
    messages, never by call order, so the build may send an item's correction before or after the second prompt:
      no assistant turn                                          -> the FIRST prompt        (kind p1)
      last assistant turn == the first reply of item 1           -> the SECOND prompt       (kind p2), or, when the last user
                                                                    message names the defect planted in item 1, the CORRECTION
                                                                    of item 1 (kind corr1)
      last assistant turn == the first reply of item 2           -> the CORRECTION of item 2 (kind corr2)
      last assistant turn == the corrected reply of item 1       -> a second prompt built on the corrected reply (kind p2x)
    FIXED DETAIL 4: a correction is `<the item's own message history> + assistant(<the item's reply, byte for byte>) +
    user(<the defects>)`, as the cell says.
  - stored: `grounding`, `grounding_reason`, `text`, and inside the `input_manifest` JSON an integer `corrections` (0 or 1).
NOT GRADED (the build's free choices): the sentences of any prompt or correction message; how a window is worded; where in the
prompt the dates sit (any system or user message outside the fact lines); the order of the correction and the second prompt;
the text of a reason beyond the code it names; whether the prompt tells the model to state the dates (no property of a stub run).

ARMS
  - (a) `PROMPT_VERSION == "a1-chain/7"`;
  - (b) no token R30 / R90 / R365 as a whole word in `SYSTEM`, in the system message sent, in any fact's `text`, or in any fact
    line of the first prompt once the ids in square brackets are taken out; the contribution keys still carry the codes;
  - (c) outside the fact lines, the first prompt names the 30-day window's two dates, and the second prompt's messages name the
    30-, 90- and 365-day windows' dates;
  - (d) `wording_check` returns a reason naming the code for R30, r90, R365, MTD, qtd and YTD, in `text`, `observed`, `inferred`
    and `invalidation`; nothing for XR30 / R300 / YTDS / AMTD (not whole words);
  - (e) `wording_check` returns `[]` for a clean item and a reason when a window date is missing from `text` (one missing; both
    missing; both present only in `observed`);
  - (f) the first reply of item 1 carries `R30`: exactly ONE correction chat for item 1, 3 chats in all, its user message names
    `R30`; the corrected clean reply is what is stored (text, PASS, `corrections` 1); item 2 has `corrections` 0;
  - (g) the corrected reply still carries the code: no second correction (3 chats), the corrected text stored FAIL with
    `wording: ` in `grounding_reason`, `corrections` 1;
  - (h) clean first replies: exactly 2 chats, both PASS, `corrections` 0 on both rows;
  - (i) the first reply of item 2 states neither of its window's dates: exactly ONE correction of item 2 naming the 365-day
    window's two dates; the corrected reply stored PASS with `corrections` 1; item 1 `corrections` 0;
  - (j) CONTROL: the chain on clean replies returns 2 rows (`activity_30d` item 1, `direction_verdict` item 2) with exactly the
    17 stored columns, both PASS, `prompt_version == PROMPT_VERSION`, `input_manifest` a JSON object carrying `day`.
FAIL at base 4c0f314e86: (a) a1-chain/6; (b) codes in SYSTEM and in 21 of the 25 fact texts; (c) no dates outside the fact lines; (d), (e)
no `wording_check`; (f), (g), (i) 2 chats, no correction; (h) no `corrections` in the manifest. (j) PASSES.

`RIVALFUNDS_CHECK_ROOT` (optional): a directory holding a `rivalfunds` package to grade instead of the worktree's
`data/etfs/scripts` (the issuer's simulated-build validation); `lib` still comes from the worktree."""
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

AC = "AC1"
FUND, DAY = "TXUE", "2026-10-02"
WIN = {"R30": ("2026-09-02", DAY), "R90": ("2026-07-04", DAY), "R365": ("2025-10-02", DAY)}
SECS = (("AAA_US_Equity", "Alpha Corp"), ("BBB_US_Equity", "Beta Corp"), ("CCC_US_Equity", "Gamma Corp"),
        ("DDD_US_Equity", "Delta Corp"))
CONTRIB = {"R30": (0.0125, 0.0080, -0.0040, -0.0110), "R90": (0.0310, 0.0190, -0.0070, -0.0220),
           "R365": (0.0810, 0.0440, -0.0150, -0.0390)}
NOTIONAL = (3400000.0, 1240000.0, 1210000.0, 1180000.0)   # "$3.4 million" is one trade; "$1.2 million" is three
CODES = re.compile(r"\b(R30|R90|R365)\b", re.I)
COLUMNS = ["fund_id", "run_id", "item_id", "kind", "text", "observed", "inferred", "cited_rows", "invalidation",
           "input_vintages", "web_reads", "grounding", "grounding_reason", "model_version", "prompt_version", "input_manifest",
           "produced_at"]
FAILS: list = []


def arm(letter, title, fn):
    """Run one arm; an exception (a name the module does not have yet) is that arm's FAIL, never the script's crash."""
    try:
        ok, detail = fn()
    except Exception as e:  # noqa: BLE001
        ok, detail = False, f"{type(e).__name__}: {e}"
    print(f"{'OK' if ok else 'FAIL'} ({letter}) {title} -- {detail}")
    if not ok:
        FAILS.append(letter)


def load():
    c.setup_path()
    c.offline_guards()
    alt = os.environ.get("RIVALFUNDS_CHECK_ROOT")
    if alt:
        sys.path.insert(0, alt)
    from rivalfunds import ai_accounts as ai
    print(f"module under check: {ai.__file__}")
    return ai


def tables():
    import datetime as dt

    import pandas as pd
    d = dt.date.fromisoformat
    g5 = pd.DataFrame([{"fund_id": FUND, "fund_ticker": FUND, "security_id": k, "security_key": k, "action": "add",
                        "window_start": d("2026-09-14"), "window_end": d("2026-09-15"), "est_notional_base": n,
                        "dataset_revision": "r1"} for (k, _n), n in zip(SECS, NOTIONAL)])
    g6 = pd.DataFrame([{"fund_id": FUND, "window_end": d("2026-09-15"), "status": None, "reason": None}])
    rows = []
    for p, vals in CONTRIB.items():
        for i, ((k, nm), v) in enumerate(zip(SECS, vals)):
            rows.append({"fund_id": FUND, "fund_ticker": FUND, "role": "rival", "period": p, "period_start": WIN[p][0],
                         "period_end": WIN[p][1], "axis": "security", "bucket": k, "security_name": nm, "contribution": v,
                         "price_coverage": "full", "n_days_priced": 20, "n_days_period": 20, "rank_best": i + 1,
                         "rank_worst": len(SECS) - i, "n_ranked": len(SECS), "n_missing": 0, "claim": "INFERRED",
                         "revision": "hc1"})
    bt = pd.DataFrame([{"fund_id": FUND, "role": "rival", "period": "R365", "window_start": WIN["R365"][0],
                        "window_end": WIN["R365"][1], "n_trading_days": 250, "axis": "security", "bucket": SECS[0][0],
                        "security_name": SECS[0][1], "net_notional_base": 7700000.0, "n_windows": 3, "lean": "into", "rank": 1,
                        "reading": "tilt", "trend_mark": "+ + + 0 0 0 0 0 0 0", "n_refused_windows": 0, "claim": "INFERRED",
                        "revision": "bt1"}])
    return g5, g6, pd.DataFrame(rows), bt


def fid(facts, table, *parts):
    """The id of the first fact whose cited row is in `table` and whose key holds every part (a security that is both a best and
    a worst contributor has two facts on ONE row: either id cites it)."""
    got = [f["id"] for f in facts if f["cited_row"]["table"] == table and all(p in str(f["cited_row"]["key"]) for p in parts)]
    if not got:
        raise KeyError(f"no {table} fact keyed {parts}")
    return got[0]


def reply(text, cited, observed="Alpha Corp led the contributors."):
    return json.dumps({"text": text, "observed": [observed], "inferred": ["The manager may keep adding."], "cited": list(cited),
                       "invalidation": "A reversal of the Alpha Corp adds."})


class Stub:
    """The recording stub client (docstring: THE INTERFACE). `marks1`: regexes of the defect planted in item 1's first reply."""

    def __init__(self, first1, first2, fixed1=None, fixed2=None, marks1=()):
        self.first1, self.first2, self.fixed1, self.fixed2, self.marks1 = first1, first2, fixed1, fixed2, list(marks1)
        self.calls, self.web = [], []

    def _kind(self, msgs):
        said = [m.get("content") for m in msgs if m.get("role") == "assistant"]
        users = [str(m.get("content")) for m in msgs if m.get("role") == "user"]
        if not said:
            return "p1"
        if said[-1] == self.first2:
            return "corr2"
        if self.fixed1 is not None and self.fixed1 != self.first1 and said[-1] == self.fixed1:
            return "p2x"
        if said[-1] == self.first1:
            return "corr1" if users and any(re.search(m, users[-1], re.I) for m in self.marks1) else "p2"
        return "other"

    def chat(self, messages, model):
        msgs = [dict(m) for m in messages]
        kind = self._kind(msgs)
        self.calls.append({"kind": kind, "messages": msgs})
        return {"p1": self.first1, "corr1": self.fixed1 or self.first1, "corr2": self.fixed2 or self.first2}.get(kind, self.first2)

    def web_search(self, query, model):
        self.web.append(query)
        return {"text": "Web summary of the market this week.", "urls": ["https://example.com/a"]}

    def kinds(self):
        out = {}
        for call in self.calls:
            out[call["kind"]] = out.get(call["kind"], 0) + 1
        return out

    def last_user(self, kind):
        for call in self.calls:
            if call["kind"] == kind:
                return [str(m.get("content")) for m in call["messages"] if m.get("role") == "user"][-1]
        return ""


def readings():
    return [{"source": s, "name": n, "value": 1.5, "as_of": "2026-10-01", "age_trading_days": 1, "status": "fresh",
             "location": f"s3://fixture/{s}", "series": [["2026-10-01", 1.5]], "reason": None}
            for s, n in (("fear_greed", "stock_price_strength"), ("rsi", "equities"), ("trending_topics", "rates"),
                         ("keyword_sentiment", "tariffs"), ("harvest_chatter", "chatter"))]


def chain(ai, facts, stub, run_id):
    rows = ai.run_chain(FUND, "rival", DAY, facts, readings(), stub, run_id, model="stub-model")
    return {r["kind"]: r for r in rows}, rows


def man(row):
    return json.loads(row["input_manifest"])


def is_int(v, want):
    return isinstance(v, int) and not isinstance(v, bool) and v == want


def fact_lines(text, facts):
    """(the lines of a prompt that carry a fact, the rest): a fact line holds a fact's id in square brackets, or its text."""
    inside, outside = [], []
    for ln in str(text).splitlines():
        (inside if any(f"[{f['id']}]" in ln or f["text"] in ln for f in facts) else outside).append(ln)
    return inside, outside


def main():
    try:
        ai = load()
        g5, g6, hc, bt = tables()
        facts = ai.fact_pack(FUND, DAY, g5, g6, hc, bt)
        c_alpha = fid(facts, "holding_contribution", "|R30|", "AAA_US_Equity")
    except Exception as e:  # noqa: BLE001 -- nothing can be graded without the module and its facts
        print(f"FAIL (setup) the module or its fact pack could not be loaded -- {type(e).__name__}: {e}")
        print(f"{AC} RESULT: FAIL 1 failure(s): setup")
        return 1
    print(f"fixture: fund {FUND}, page day {DAY}, {len(facts)} facts {[f['id'] for f in facts]}; windows {WIN}")

    s30, e30 = WIN["R30"]
    s365, e365 = WIN["R365"]
    clean1 = reply(f"From {s30} to {e30} the fund's best contributor was Alpha Corp, which added +1.25% of fund return.", [c_alpha])
    clean2 = reply(f"Over the last year, from {s365} to {e365}, the lean into Alpha Corp is borne out by the last month.", [],
                   "The lean into Alpha Corp held.")
    coded1 = reply(f"From {s30} to {e30} the top R30 contributor was Alpha Corp, which added +1.25% of fund return.", [c_alpha])
    coded1b = reply(f"Between {s30} and {e30} Alpha Corp was the R30 leader, adding +1.25% of fund return.", [c_alpha])
    nodate2 = reply("The lean into Alpha Corp is borne out by the last month.", [], "The lean into Alpha Corp held.")
    text_of = lambda raw: json.loads(raw)["text"]  # noqa: E731

    base = Stub(clean1, clean2)
    try:
        _by, base_rows = chain(ai, facts, base, "run-aw1-clean")
        base_err = None
    except Exception as e:  # noqa: BLE001
        base_rows, base_err = [], f"{type(e).__name__}: {e}"
    print(f"clean chain: chats {base.kinds()} | web searches {len(base.web)} | rows {len(base_rows)} | error {base_err}")

    def a():
        return ai.PROMPT_VERSION == "a1-chain/7", f"PROMPT_VERSION {ai.PROMPT_VERSION!r}"

    def b():
        sysmsg = [m["content"] for call in base.calls[:1] for m in call["messages"] if m.get("role") == "system"]
        bad_sys = sorted(set(CODES.findall(ai.SYSTEM)) | {x for s in sysmsg for x in CODES.findall(str(s))})
        bad_text = sorted(f["id"] for f in facts if CODES.search(f["text"]))
        user1 = base.last_user("p1")
        bad_sent, unsent = [], []
        for f in facts:
            lines = [ln for ln in user1.splitlines() if f["id"] in ln]
            if not lines:
                unsent.append(f["id"])
            if any(CODES.search(re.sub(r"\[[^\]]*\]", " ", ln).replace(f["id"], " ")) for ln in lines):
                bad_sent.append(f["id"])
        keys = sorted({str(f["cited_row"]["key"]).split("|")[1] for f in facts if f["cited_row"]["table"] == "holding_contribution"})
        ok = not bad_sys and not bad_text and not bad_sent and not unsent and bool(sysmsg) and keys == ["R30", "R365", "R90"]
        return ok, (f"codes in SYSTEM / the system message {bad_sys}; facts whose text carries a code {len(bad_text)} {bad_text[:4]}; "
                    f"sent fact lines carrying a code {len(bad_sent)}; facts not in the first prompt {len(unsent)}; "
                    f"contribution key periods {keys}")

    def cc():
        p1 = next(call for call in base.calls if call["kind"] == "p1")
        p2 = next(call for call in base.calls if call["kind"] == "p2")
        scope = lambda call: "\n".join(ln for m in call["messages"] if m.get("role") in ("system", "user")  # noqa: E731
                                       for ln in fact_lines(m.get("content"), facts)[1])
        t1, t2 = scope(p1), scope(p2)
        miss1 = [d for d in WIN["R30"] if d not in t1]
        miss2 = [f"{p}:{d}" for p in ("R30", "R90", "R365") for d in WIN[p] if d not in t2]
        return not miss1 and not miss2, (f"first prompt outside the fact lines lacks {miss1}; second prompt's messages outside the "
                                         f"fact lines lack {miss2}")

    def wc(text, observed=(), inferred=(), invalidation=None, win="R30"):
        got = ai.wording_check({"text": text, "observed": list(observed), "inferred": list(inferred), "invalidation": invalidation},
                               [WIN[win]])
        if not isinstance(got, list) or not all(isinstance(x, str) for x in got):
            raise TypeError(f"wording_check returned {got!r}, not a list of str")
        return got

    ok_text = f"From {s30} to {e30} the fund added to Alpha Corp."

    def d():
        cases = [("R30", wc(f"From {s30} to {e30} the top R30 contributor was Alpha Corp.")),
                 ("R90", wc(ok_text, observed=["the r90 leaders held"])),
                 ("R365", wc(ok_text, inferred=["the R365 trend is intact"])),
                 ("MTD", wc(ok_text, invalidation="a weak MTD print")),
                 ("QTD", wc(f"From {s30} to {e30} the qtd leaders held.")),
                 ("YTD", wc(ok_text, observed=["YTD the fund leads"]))]
        missed = [code for code, got in cases if not any(re.search(rf"\b{code}\b", r, re.I) for r in got)]
        part = wc(f"From {s30} to {e30} the XR30 sleeve, the R300 share class, YTDS and AMTD were unchanged.")
        return not missed and part == [], (f"codes with no reason naming them: {missed}; reasons for XR30 / R300 / YTDS / AMTD "
                                           f"(not whole words): {part}; e.g. {cases[0][1]}")

    def e():
        clean = wc(ok_text, observed=["Alpha Corp was added."], inferred=["The manager may keep adding."], invalidation="A reversal.")
        one = wc(f"Since {s30} the fund added to Alpha Corp.")
        none = wc("The fund added to Alpha Corp.")
        elsewhere = wc("The fund added to Alpha Corp.", observed=[f"The window runs {s30} to {e30}."])
        y_clean = wc(f"From {s365} to {e365} the lean held.", win="R365")
        y_wrong = wc(ok_text, win="R365")
        ok = clean == [] and y_clean == [] and all(len(x) > 0 for x in (one, none, elsewhere, y_wrong))
        return ok, (f"clean item {clean}; clean 365-day item {y_clean}; one date missing {one}; both missing {none}; dates only in "
                    f"observed {elsewhere}; the 30-day dates where the 365-day window is asked {y_wrong}")

    def f():
        st = Stub(coded1, clean2, fixed1=clean1, marks1=[r"\bR30\b"])
        by, rows = chain(ai, facts, st, "run-aw1-f")
        r1, r2 = by["activity_30d"], by["direction_verdict"]
        named = bool(re.search(r"\bR30\b", st.last_user("corr1"), re.I))
        ok = (st.kinds() == {"p1": 1, "p2": 1, "corr1": 1} and named and r1["text"] == text_of(clean1) and r1["grounding"] == "PASS"
              and is_int(man(r1).get("corrections"), 1) and is_int(man(r2).get("corrections"), 0) and len(rows) == 2)
        return ok, (f"chats {st.kinds()} (want p1 1, p2 1, corr1 1); correction names R30: {named}; stored text is the corrected "
                    f"reply: {r1['text'] == text_of(clean1)}; grounding {r1['grounding']}; corrections item 1 "
                    f"{man(r1).get('corrections')!r}, item 2 {man(r2).get('corrections')!r}")

    def g():
        st = Stub(coded1, clean2, fixed1=coded1b, marks1=[r"\bR30\b"])
        by, _rows = chain(ai, facts, st, "run-aw1-g")
        r1 = by["activity_30d"]
        why = str(r1["grounding_reason"])
        ok = (st.kinds() == {"p1": 1, "p2": 1, "corr1": 1} and r1["grounding"] == "FAIL" and "wording: " in why
              and r1["text"] == text_of(coded1b) and is_int(man(r1).get("corrections"), 1)
              and by["direction_verdict"]["grounding"] == "PASS")
        return ok, (f"chats {st.kinds()} (want p1 1, p2 1, corr1 1: no second correction); grounding {r1['grounding']}; reason "
                    f"{why!r}; stored text is the corrected reply: {r1['text'] == text_of(coded1b)}; corrections "
                    f"{man(r1).get('corrections')!r}")

    def h():
        if base_err:
            raise RuntimeError(base_err)
        got = [man(r).get("corrections") for r in base_rows]
        ok = base.kinds() == {"p1": 1, "p2": 1} and [r["grounding"] for r in base_rows] == ["PASS", "PASS"] and all(is_int(x, 0) for x in got)
        return ok, f"chats {base.kinds()} (want exactly p1 1, p2 1); grounding {[r['grounding'] for r in base_rows]}; corrections {got}"

    def i():
        st = Stub(clean1, nodate2, fixed2=clean2)
        by, _rows = chain(ai, facts, st, "run-aw1-i")
        r1, r2 = by["activity_30d"], by["direction_verdict"]
        msg = st.last_user("corr2")
        named = [dd for dd in WIN["R365"] if dd in msg]
        ok = (st.kinds() == {"p1": 1, "p2": 1, "corr2": 1} and len(named) == 2 and r2["text"] == text_of(clean2)
              and r2["grounding"] == "PASS" and is_int(man(r2).get("corrections"), 1) and is_int(man(r1).get("corrections"), 0))
        return ok, (f"chats {st.kinds()} (want p1 1, p2 1, corr2 1); correction names the 365-day dates {named}; stored text is the "
                    f"corrected reply: {r2['text'] == text_of(clean2)}; grounding {r2['grounding']} ({r2['grounding_reason']}); "
                    f"corrections item 2 {man(r2).get('corrections')!r}, item 1 {man(r1).get('corrections')!r}")

    def j():
        if base_err:
            raise RuntimeError(base_err)
        shape = [(r["kind"], r["item_id"]) for r in base_rows]
        cols = all(sorted(r) == sorted(COLUMNS) for r in base_rows) and list(ai.SCHEMA.names) == COLUMNS
        mans = [man(r) for r in base_rows]
        ok = (shape == [("activity_30d", "1"), ("direction_verdict", "2")] and cols
              and [r["grounding"] for r in base_rows] == ["PASS", "PASS"] and all(r["prompt_version"] == ai.PROMPT_VERSION for r in base_rows)
              and all(isinstance(m, dict) and m.get("day") == DAY for m in mans) and base_rows[0]["text"] == text_of(clean1)
              and len(base.calls) >= 2)
        return ok, (f"rows {shape}; the 17 stored columns and no other: {cols}; grounding {[r['grounding'] for r in base_rows]} "
                    f"{[r['grounding_reason'] for r in base_rows]}; manifest day {[m.get('day') for m in mans]}")

    arm("a", "PROMPT_VERSION is a1-chain/7", a)
    arm("b", "no R30 / R90 / R365 in SYSTEM or in the text of a fact line sent to the model", b)
    arm("c", "the first prompt names the 30-day window's dates; the second names the 30-, 90- and 365-day windows' dates", cc)
    arm("d", "wording_check returns a reason naming each period code, whole word, any case, in any of the four fields", d)
    arm("e", "wording_check returns [] for a clean item and a reason when a window date is missing from text", e)
    arm("f", "a code in the first reply: ONE correction naming it, the corrected clean reply stored PASS with corrections 1", f)
    arm("g", "a code still in the corrected reply: no second correction, stored FAIL with a 'wording: ' reason", g)
    arm("h", "clean first replies: exactly 2 chats, corrections 0", h)
    arm("i", "the window's dates missing from the second item: ONE correction naming both dates, stored PASS", i)
    arm("j", "CONTROL: the chain on clean replies returns its 2 rows with the 17 stored columns, both PASS", j)
    print(f"{AC} RESULT: PASS 0 failures" if not FAILS else f"{AC} RESULT: FAIL {len(FAILS)} failure(s): {', '.join(FAILS)}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
