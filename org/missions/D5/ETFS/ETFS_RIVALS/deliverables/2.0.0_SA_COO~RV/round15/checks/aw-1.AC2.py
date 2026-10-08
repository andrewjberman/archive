"""RIV-aw-1 AC2 -- CITE EVERY DOLLAR FIGURE (cell items 3, the figure half of 4 and 5, and 6; CTO rulings R19, R20; rows C-S83).

A figure an account writes that no CITED row carries is a defect even when exactly one uncited fact matches it: the chain sends ONE
correction naming the figure and the candidate fact ids. After the correction `attach_uncited` still runs as today (one match:
attached, PASS, counted in `attached_figures`; several: FAIL, the existing ambiguous reason). At most one correction per item and
4 chats per fund. The second prompt is built on the FIRST reply of item 1. A re-grade sends nothing to a model.

NO network, NO model call, NO S3: the client is a recording stub, the facts are built by the module's own `fact_pack` on small
pandas frames, `_common.offline_guards()` refuses boto3 and `requests.post`.

THE INTERFACE THIS CHECK READS (the contract for the builder; `data/etfs/scripts/rivalfunds/ai_accounts.py` only):
  - `fact_pack(fund_id, day, g5, g6, contribution, trend)` and `run_chain(fund_id, role, day, facts, readings, client, run_id,
    model=...)`, both with TODAY'S signature (the window dates come from `facts` or `day`; see aw-1.AC1.py FIXED DETAILS 1, 2).
  - the fixture's facts: four trades of 3,400,000 / 1,240,000 / 1,210,000 / 1,180,000 (Alpha, Beta, Gamma, Delta Corp), so
    "$3.4 million" is carried by ONE fact and "$1.2 million" by THREE (the TXUE shape); the 30-day contribution of Alpha Corp
    0.0125 ("+1.25%"), which every reply cites. A fact is found by its `cited_row` table and key, never by a literal id.
  - the stub client: `chat(messages, model) -> str` and `web_search(query, model) -> {"text", "urls"}`; it records every call
    and answers by the SHAPE of the messages, never by call order (the build may send a correction before or after the second
    prompt):
      no assistant turn                                          -> the FIRST prompt        (kind p1)
      last assistant turn == the first reply of item 1           -> the SECOND prompt       (kind p2), or, when the last user
                                                                    message names the defect planted in item 1 (the figure's
                                                                    digits, or the code), the CORRECTION of item 1 (kind corr1)
      last assistant turn == the first reply of item 2           -> the CORRECTION of item 2 (kind corr2)
      last assistant turn == the corrected reply of item 1       -> a second prompt built on the corrected reply (kind p2x)
    FIXED DETAIL 4 (as in AC1): a correction is `<the item's own message history> + assistant(<the item's reply, byte for byte>)
    + user(<the defects>)`.
  - FIXED DETAIL 5: the correction for an uncited figure writes the figure's digits as the reply wrote them ("3.4", "1.2") and
    each candidate fact's `id` as a whole token; for ONE candidate it names that id, for three it names all three.
  - stored: `grounding`, `grounding_reason`, `cited_rows` (an attached row carries `auto_cited: true`, as today), and inside the
    `input_manifest` JSON of EVERY row the integers `attached_figures` and `corrections` (0 or 1).
  - `attach_uncited(body, facts, cited, identifiers=None, names=None) -> (rows, notes)` and `grounding_check(text, cited_rows,
    ...) -> (ok, reason)` as today; the ambiguous reason still reads `ambiguous figure (...)` and names the candidate ids.
  - `regrade_rows(rows, facts_of, now, superseded_grader)` with today's four arguments (a `client` keyword, if the build adds
    one, is passed a client that raises). FIXED DETAIL 6: a stored `a1-chain/7` item whose text carries a period code re-grades
    FAIL with `wording: ` in its reason, a clean one re-grades PASS; the window dates come from `facts_of(fund)`.
NOT GRADED (the build's free choices): the sentences of the correction; whether it also lists facts that do not match; the order
of the correction and the second prompt; whether a re-graded row carries `attached_figures`; the new grader version string.

ARMS
  - (a) a figure carried by exactly ONE uncited fact ("$3.4 million"): exactly ONE correction of item 1, 3 chats, its user message
    names the figure and that fact's id;
  - (b) a figure matched by THREE uncited facts ("$1.2 million"): exactly ONE correction, its user message names the figure and
    lists the three candidate ids;
  - (c) the corrected reply cites the row: stored PASS, `attached_figures` 0, `corrections` 1, the row cited without
    `auto_cited`; item 2 carries `attached_figures` 0 and `corrections` 0;
  - (d) the corrected reply still omits the citation and ONE fact matches: stored PASS, `attached_figures` 1, `corrections` 1,
    one `auto_cited` row, no second correction (3 chats);
  - (e) the corrected reply still omits it and THREE match: stored FAIL, the reason holds `ambiguous figure` and the three ids,
    `attached_figures` 0, `corrections` 1, 3 chats;
  - (f) both items defective and both still defective after their correction (item 1 a code, item 2 the three-way figure):
    exactly 4 chats -- p1, p2, ONE correction each -- and both rows FAIL with `corrections` 1;
  - (g) with item 1 corrected, the second prompt is sent once and its history carries the FIRST reply of item 1; no second prompt
    is built on the corrected reply;
  - (h) `regrade_rows` sends nothing: no chat, no web search, no `default_client()`; it returns one row per stored row under a
    new run id;
  - (i) `regrade_rows` applies the wording check to a stored item (a code: FAIL `wording: `; clean: PASS);
  - (j) CONTROL: `attach_uncited` attaches the single match with `auto_cited` and notes the three-way figure with its three ids;
    `grounding_check` passes the attached text; the chain on clean replies returns 2 PASS rows.
FAIL at base 4c0f314e86: (a) to (g) no correction is ever sent (2 chats) and the manifest carries neither count; (i) a code in a
stored text re-grades PASS. (h) and (j) PASS.

`RIVALFUNDS_CHECK_ROOT` (optional): a directory holding a `rivalfunds` package to grade instead of the worktree's
`data/etfs/scripts` (the issuer's simulated-build validation); `lib` still comes from the worktree."""
import json
import inspect
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

AC = "AC2"
FUND, DAY = "TXUE", "2026-10-02"
WIN = {"R30": ("2026-09-02", DAY), "R90": ("2026-07-04", DAY), "R365": ("2025-10-02", DAY)}
SECS = (("AAA_US_Equity", "Alpha Corp"), ("BBB_US_Equity", "Beta Corp"), ("CCC_US_Equity", "Gamma Corp"),
        ("DDD_US_Equity", "Delta Corp"))
CONTRIB = {"R30": (0.0125, 0.0080, -0.0040, -0.0110), "R90": (0.0310, 0.0190, -0.0070, -0.0220),
           "R365": (0.0810, 0.0440, -0.0150, -0.0390)}
NOTIONAL = (3400000.0, 1240000.0, 1210000.0, 1180000.0)   # "$3.4 million" is one trade; "$1.2 million" is three
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


def tok(text, ident):
    """True when the fact id stands in the text as a whole token (T1 is not found in T11 or in C-T1-x)."""
    return bool(re.search(r"(?<![A-Za-z0-9_-])" + re.escape(str(ident)) + r"(?![A-Za-z0-9_-])", str(text)))


def cited_of(row):
    return json.loads(row["cited_rows"])


def main():
    try:
        ai = load()
        g5, g6, hc, bt = tables()
        facts = ai.fact_pack(FUND, DAY, g5, g6, hc, bt)
        c_alpha = fid(facts, "holding_contribution", "|R30|", "AAA_US_Equity")
        t_alpha = fid(facts, "trade_schedule", "AAA_US_Equity")
        t_three = [fid(facts, "trade_schedule", k) for k in ("BBB_US_Equity", "CCC_US_Equity", "DDD_US_Equity")]
    except Exception as e:  # noqa: BLE001 -- nothing can be graded without the module and its facts
        print(f"FAIL (setup) the module or its fact pack could not be loaded -- {type(e).__name__}: {e}")
        print(f"{AC} RESULT: FAIL 1 failure(s): setup")
        return 1
    print(f"fixture: fund {FUND}, page day {DAY}, {len(facts)} facts; '$3.4 million' is fact {t_alpha}; '$1.2 million' is facts "
          f"{t_three}; '+1.25%' is fact {c_alpha}")

    s30, e30 = WIN["R30"]
    s365, e365 = WIN["R365"]
    alpha_key = next(f["cited_row"]["key"] for f in facts if f["id"] == t_alpha)
    clean1 = reply(f"From {s30} to {e30} the fund's best contributor was Alpha Corp, which added +1.25% of fund return.", [c_alpha])
    clean2 = reply(f"Over the last year, from {s365} to {e365}, the lean into Alpha Corp is borne out by the last month.", [],
                   "The lean into Alpha Corp held.")
    one_txt = f"From {s30} to {e30} the fund added $3.4 million of Alpha Corp, which contributed +1.25% of fund return."
    one1 = reply(one_txt, [c_alpha])                                   # the figure of ONE uncited fact
    one1_cited = reply(one_txt, [c_alpha, t_alpha])                    # the corrected reply that cites it
    one1_again = reply(one_txt.replace("the fund added", "the fund bought"), [c_alpha])   # corrected, still uncited
    tri_txt = f"From {s30} to {e30} the fund added $1.2 million of Beta Corp, and Alpha Corp contributed +1.25% of fund return."
    tri1 = reply(tri_txt, [c_alpha])                                   # the figure of THREE uncited facts
    tri1_again = reply(tri_txt.replace("the fund added", "the fund bought"), [c_alpha])
    coded1 = reply(f"From {s30} to {e30} the top R30 contributor was Alpha Corp, which added +1.25% of fund return.", [c_alpha])
    tri2 = reply(f"Over the last year, from {s365} to {e365}, the lean into Alpha Corp is borne out by $1.2 million of buying.", [],
                 "The lean into Alpha Corp held.")
    m34, m12, mcode = r"(?<![\d.])3\.4(?!\d)", r"(?<![\d.])1\.2(?!\d)", r"\bR30\b"
    text_of = lambda raw: json.loads(raw)["text"]  # noqa: E731

    def a():
        st = Stub(one1, clean2, fixed1=one1_cited, marks1=[m34])
        chain(ai, facts, st, "run-aw1-2a")
        msg = st.last_user("corr1")
        ok = st.kinds() == {"p1": 1, "p2": 1, "corr1": 1} and bool(re.search(m34, msg)) and tok(msg, t_alpha)
        return ok, (f"chats {st.kinds()} (want p1 1, p2 1, corr1 1); correction names 3.4: {bool(re.search(m34, msg))}; names the "
                    f"fact id {t_alpha}: {tok(msg, t_alpha)}")

    def b():
        st = Stub(tri1, clean2, fixed1=tri1_again, marks1=[m12])
        chain(ai, facts, st, "run-aw1-2b")
        msg = st.last_user("corr1")
        listed = [t for t in t_three if tok(msg, t)]
        ok = st.kinds() == {"p1": 1, "p2": 1, "corr1": 1} and bool(re.search(m12, msg)) and listed == t_three
        return ok, (f"chats {st.kinds()} (want p1 1, p2 1, corr1 1); correction names 1.2: {bool(re.search(m12, msg))}; candidate "
                    f"ids listed {listed} of {t_three}")

    def cc():
        st = Stub(one1, clean2, fixed1=one1_cited, marks1=[m34])
        by, _rows = chain(ai, facts, st, "run-aw1-2c")
        r1, r2 = by["activity_30d"], by["direction_verdict"]
        mine = [r for r in cited_of(r1) if r.get("key") == alpha_key]
        m1, m2 = man(r1), man(r2)
        ok = (r1["grounding"] == "PASS" and is_int(m1.get("attached_figures"), 0) and is_int(m1.get("corrections"), 1)
              and len(mine) == 1 and not mine[0].get("auto_cited") and is_int(m2.get("attached_figures"), 0)
              and is_int(m2.get("corrections"), 0) and st.kinds() == {"p1": 1, "p2": 1, "corr1": 1})
        return ok, (f"grounding {r1['grounding']} ({r1['grounding_reason']}); item 1 attached_figures {m1.get('attached_figures')!r}, "
                    f"corrections {m1.get('corrections')!r}; the trade row cited {len(mine)} time(s), auto_cited "
                    f"{[r.get('auto_cited') for r in mine]}; item 2 attached_figures {m2.get('attached_figures')!r}, corrections "
                    f"{m2.get('corrections')!r}; chats {st.kinds()}")

    def d():
        st = Stub(one1, clean2, fixed1=one1_again, marks1=[m34])
        by, _rows = chain(ai, facts, st, "run-aw1-2d")
        r1 = by["activity_30d"]
        auto = [r for r in cited_of(r1) if r.get("auto_cited")]
        m1 = man(r1)
        ok = (r1["grounding"] == "PASS" and is_int(m1.get("attached_figures"), 1) and is_int(m1.get("corrections"), 1)
              and [r.get("key") for r in auto] == [alpha_key] and st.kinds() == {"p1": 1, "p2": 1, "corr1": 1}
              and r1["text"] == text_of(one1_again))
        return ok, (f"grounding {r1['grounding']} ({r1['grounding_reason']}); attached_figures {m1.get('attached_figures')!r}; "
                    f"corrections {m1.get('corrections')!r}; auto_cited rows {[r.get('key') for r in auto]}; chats {st.kinds()} "
                    f"(want p1 1, p2 1, corr1 1); stored text is the corrected reply: {r1['text'] == text_of(one1_again)}")

    def e():
        st = Stub(tri1, clean2, fixed1=tri1_again, marks1=[m12])
        by, _rows = chain(ai, facts, st, "run-aw1-2e")
        r1 = by["activity_30d"]
        why, m1 = str(r1["grounding_reason"]), man(r1)
        ids = [t for t in t_three if tok(why, t)]
        ok = (r1["grounding"] == "FAIL" and "ambiguous figure" in why and ids == t_three and is_int(m1.get("attached_figures"), 0)
              and is_int(m1.get("corrections"), 1) and st.kinds() == {"p1": 1, "p2": 1, "corr1": 1})
        return ok, (f"grounding {r1['grounding']}; reason {why!r}; ids in the reason {ids}; attached_figures "
                    f"{m1.get('attached_figures')!r}; corrections {m1.get('corrections')!r}; chats {st.kinds()}")

    def f():
        st = Stub(coded1, tri2, marks1=[mcode])      # each correction returns the same defective reply again
        by, _rows = chain(ai, facts, st, "run-aw1-2f")
        r1, r2 = by["activity_30d"], by["direction_verdict"]
        got = [man(r).get("corrections") for r in (r1, r2)]
        ok = (st.kinds() == {"p1": 1, "p2": 1, "corr1": 1, "corr2": 1} and len(st.calls) == 4
              and [r1["grounding"], r2["grounding"]] == ["FAIL", "FAIL"] and all(is_int(x, 1) for x in got))
        return ok, (f"chats {st.kinds()}, {len(st.calls)} in all (want p1 1, p2 1, corr1 1, corr2 1 = 4); grounding "
                    f"{[r1['grounding'], r2['grounding']]}; reasons {[r1['grounding_reason'], r2['grounding_reason']]}; "
                    f"corrections {got}")

    def g():
        st = Stub(one1, clean2, fixed1=one1_cited, marks1=[m34])
        chain(ai, facts, st, "run-aw1-2g")
        p2 = [call for call in st.calls if call["kind"] == "p2"]
        said = [[m.get("content") for m in call["messages"] if m.get("role") == "assistant"] for call in p2]
        on_first = bool(p2) and all(s == [one1] for s in said)
        k = st.kinds()
        ok = k.get("corr1") == 1 and k.get("p2") == 1 and not k.get("p2x") and not k.get("other") and on_first
        return ok, (f"chats {k} (want corr1 1, p2 1, no p2x: the item was corrected and the second prompt sent once); the second "
                    f"prompt's assistant turn is exactly the FIRST reply of item 1: {on_first}")

    def stored_rows():
        st = Stub(clean1, clean2)
        _by, rows = chain(ai, facts, st, "run-aw1-2h")
        return rows

    class Raises:
        def __init__(self):
            self.hits = []

        def chat(self, messages, model):
            self.hits.append("chat")
            raise AssertionError("a re-grade sent a chat")

        def web_search(self, query, model):
            self.hits.append("web_search")
            raise AssertionError("a re-grade sent a web search")

    def regrade(rows):
        """`regrade_rows` with every door to a model watched; returns (rows, calls seen)."""
        seen, client = [], Raises()

        def refuse(*a_, **k_):
            seen.append("default_client")
            raise AssertionError("a re-grade asked for the live client")

        keep = [(ai, "default_client", ai.default_client)]
        try:
            from rivalfunds import ai_client
            if hasattr(ai_client, "default_client"):
                keep.append((ai_client, "default_client", ai_client.default_client))
        except Exception:  # noqa: BLE001 -- no such module at this build: nothing to watch there
            pass
        kw = {"client": client} if "client" in inspect.signature(ai.regrade_rows).parameters else {}
        for mod, name, _old in keep:
            setattr(mod, name, refuse)
        try:
            out = ai.regrade_rows(rows, lambda fund: facts, "2026-10-08T14:00:00Z", "grounding_check/6", **kw)
        finally:
            for mod, name, old in keep:
                setattr(mod, name, old)
        return out, seen + client.hits

    def h():
        rows = stored_rows()
        out, seen = regrade(rows)
        ids = {r["run_id"] for r in out}
        ok = not seen and len(out) == len(rows) == 2 and len(ids) == 1 and ids != {"run-aw1-2h"}
        return ok, f"calls to a client during the re-grade: {seen}; rows in {len(rows)}, out {len(out)}; new run id {sorted(ids)}"

    def i():
        rows = [dict(r) for r in stored_rows()]
        rows[0]["text"] = text_of(coded1)
        rows[0]["observed"] = json.dumps([])
        out, seen = regrade(rows)
        by = {r["kind"]: r for r in out}
        r1, r2 = by["activity_30d"], by["direction_verdict"]
        ok = (not seen and r1["grounding"] == "FAIL" and "wording: " in str(r1["grounding_reason"]) and r2["grounding"] == "PASS")
        return ok, (f"the stored item carrying R30 re-grades {r1['grounding']} ({r1['grounding_reason']!r}); the clean item "
                    f"re-grades {r2['grounding']} ({r2['grounding_reason']!r}); client calls {seen}")

    def j():
        by_id = {x["id"]: x for x in facts}
        cited = [by_id[c_alpha]["cited_row"]]
        add1, notes1 = ai.attach_uncited(one_txt, facts, cited)
        add3, notes3 = ai.attach_uncited(tri_txt, facts, cited)
        ok1, _why1 = ai.grounding_check(one_txt, cited + add1)
        ok0, why0 = ai.grounding_check(one_txt, cited)
        rows = stored_rows()
        ok = ([r.get("key") for r in add1] == [alpha_key] and all(r.get("auto_cited") is True for r in add1) and notes1 == []
              and add3 == [] and len(notes3) == 1 and all(tok(notes3[0], t) for t in t_three) and ok1 and not ok0
              and [r["grounding"] for r in rows] == ["PASS", "PASS"] and len(rows) == 2)
        return ok, (f"single match attached {[r.get('key') for r in add1]}, notes {notes1}; three-way figure attached {len(add3)}, "
                    f"notes {notes3}; grounding with the attach {ok1}, without {ok0} ({why0}); clean chain "
                    f"{[r['grounding'] for r in rows]}")

    arm("a", "a figure of ONE uncited fact: ONE correction naming the figure and that fact's id", a)
    arm("b", "a figure of THREE uncited facts: ONE correction listing the three candidate ids", b)
    arm("c", "the corrected reply cites the row: PASS, attached_figures 0, corrections 1", cc)
    arm("d", "still uncited after the correction, one match: the attach runs, PASS, attached_figures 1", d)
    arm("e", "still uncited after the correction, three matches: FAIL with the ambiguous reason", e)
    arm("f", "at most ONE correction per item and 4 chats per fund", f)
    arm("g", "the second prompt carries the FIRST reply of item 1 when item 1 was corrected", g)
    arm("h", "regrade_rows sends nothing to a client", h)
    arm("i", "regrade_rows applies the wording check to a stored item", i)
    arm("j", "CONTROL: attach_uncited and grounding_check as today; the chain on clean replies returns 2 PASS rows", j)
    print(f"{AC} RESULT: PASS 0 failures" if not FAILS else f"{AC} RESULT: FAIL {len(FAILS)} failure(s): {', '.join(FAILS)}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
