"""RIV-xc-1 checks (round 29): no two funds' Direction Verdict openings share a name-abstracted frame on one page -- the
frame is computed by `ai_accounts.frame_of`; `run_chain(..., seen_frames=<dict>)` sends a colliding opening back ONCE through the
chain's existing one-correction path; `run_day` passes ONE shared dict across the day's funds.

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: a stub client, no vendor call. (Whether the vendor's replies then differ is read on the next sweep page, not here.)
"""
import inspect
import json

import pandas as pd

from rivalfunds import ai_accounts as ai

DAY = "2026-10-08"
EMPTY = pd.DataFrame(columns=["fund_id"])


def _facts(fund):
    g5 = pd.DataFrame([{"fund_id": fund, "security_key": "AAA_US", "action": "buy", "window_end": "2026-10-06",
                        "est_notional_base": 5_000_000.0}])
    return ai.fact_pack(fund, DAY, g5, EMPTY, EMPTY, EMPTY, names={"AAA_US": "Alpha Co"})


def _reply(lead, win):
    return json.dumps({"text": f"{lead} The period runs from {win[0]} to {win[1]}.", "observed": ["Alpha Co was bought."],
                       "inferred": ["It may continue."], "cited": [], "invalidation": "A sale."})


class Stub:
    def __init__(self, fund, *verdict_leads):
        self.facts = _facts(fund)
        self.wins = ai.period_windows(DAY, self.facts)
        self.leads, self.calls = list(verdict_leads), []

    def chat(self, messages, model):
        last = str(messages[-1]["content"])
        self.calls.append(last)
        if "activity_30d]" in last:
            return _reply("Alpha Co was bought.", self.wins["R30"])
        n = sum(1 for c in self.calls if "activity_30d]" not in c) - 1
        return _reply(self.leads[min(n, len(self.leads) - 1)], self.wins["R365"])

    def web_search(self, query, model):
        return {"text": "", "urls": []}


def _verdict(fund, stub, seen):
    rows = ai.run_chain(fund, "rival", DAY, stub.facts, [], stub, "r", model="stub", seen_frames=seen)
    return [r for r in rows if r["kind"] == "direction_verdict"][0]


def _frame_corrections(stub):
    return [c for c in stub.calls if "Your reply has these defects" in c and "shares its frame" in c]


def test_ac1_frame_of_abstracts_names_and_figures_and_keeps_the_leading_words():
    a = ai.frame_of("Alpha Co is the clearest fund-specific tell: it was bought. More.")
    b = ai.frame_of("Beta Corp is the clearest fund-specific tell: it was sold.")
    assert a == b == "<name> is the clearest fund-specific"
    assert ai.frame_of("Alpha Co is the clearest tell: it was bought.") == "<name> is the clearest tell:"
    assert ai.frame_of("Alpha Co added $2.7 million over 2026-09-01 to 2026-09-30.") == "<name> added <n> million over"
    assert ai.frame_of("") == ""


def test_ac2_a_colliding_opening_is_sent_back_once_and_the_reply_stands():
    seen = {}
    first = Stub("TST1", "Alpha Co is the clearest fund-specific tell: it was bought.")
    v1 = _verdict("TST1", first, seen)
    assert v1["text"].startswith("Alpha Co is the clearest fund-specific tell") and _frame_corrections(first) == []
    second = Stub("TST2", "Beta Corp is the clearest fund-specific tell: it was sold.", "Gamma Co stands out most: it was sold.")
    v2 = _verdict("TST2", second, seen)
    fixed = _frame_corrections(second)
    assert len(fixed) == 1 and "TST1" in fixed[0]                   # ONE correction, naming the fund whose frame it shares
    assert v2["text"].startswith("Gamma Co stands out most")         # the corrected reply replaces it
    assert ai.frame_of(v2["text"]) in seen and seen[ai.frame_of(v2["text"])] == "TST2"


def test_ac2_a_distinct_frame_and_an_absent_dict_draw_no_correction():
    seen = {}
    _verdict("TST1", Stub("TST1", "Alpha Co is the clearest fund-specific tell: x."), seen)
    other = Stub("TST2", "Beta Corp stands out most: y.")
    _verdict("TST2", other, seen)
    assert _frame_corrections(other) == []
    same = Stub("TST3", "Alpha Co is the clearest fund-specific tell: z.")
    ai.run_chain("TST3", "rival", DAY, same.facts, [], same, "r", model="stub")   # seen_frames not passed: as before
    assert _frame_corrections(same) == []


def test_ac3_run_day_shares_one_dict_across_the_days_funds():
    src = inspect.getsource(ai.run_day)
    assert "seen_frames" in src and "run_chain(" in src
    assert "seen_frames" in inspect.signature(ai.run_chain).parameters
