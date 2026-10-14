"""RIV-xc-2 checks (round 30): `ai_accounts.frame_of` compares FAMILIES, not a fixed five-token window, and `run_chain` STORES the
reason a correction was sent (round-29 analysis ruling 2; the CVO's row D1-C-S20: IDVZ "is the clearest fund-specific tell" and
TXUE "is the clearest tell" are one family a reader sees, and the five-token window split them at token 5).

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: a stub client, no vendor call. Whether the vendor's replies then fall into 13 distinct families is J1 and the next sweep
page (the CVO's read), not here.

The rule this file pins (`frame_of`, v2):
  1. As v1: first sentence (split at the first sentence-final `.`, `!` or `?` followed by whitespace), tokenised on whitespace, each
     token stripped of `,;.!?"'()` at both ends (`:` is kept), a token with a digit is `<n>` (consecutive `<n>` collapse), a run of
     name-like tokens is one `<name>`, everything else lowercased.
  2. THE CLAUSE: tokens up to and including the first token whose raw form ends in `:`; with no such token, the whole first sentence.
  3. THE STOP-LIST (data, `FRAME_STOP` in ai_accounts.py): the tokens `fund-specific`, `most`, `single`, `particular` are removed
     from the clause. `clearest` is NOT in it: it stays as the head word.
  4. The frame is the first EIGHT tokens of the clause joined by single spaces (fewer if fewer). `frame_of("")` is `""`.
"""
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


def _rows(fund, stub, seen):
    return ai.run_chain(fund, "rival", DAY, stub.facts, [], stub, "r", model="stub", seen_frames=seen)


def _verdict(rows):
    return [r for r in rows if r["kind"] == "direction_verdict"][0]


def _frame_corrections(stub):
    return [c for c in stub.calls if "Your reply has these defects" in c and "shares its frame" in c]


def test_ac1_frame_of_compares_families_and_the_planted_pair_reads_same():
    # the stop-list is gone from the frame; `clearest` stays as the head word
    a = ai.frame_of("Alpha Co is the clearest fund-specific tell: it was bought. More.")
    b = ai.frame_of("Beta Corp is the clearest tell: it was sold.")
    assert a == b == "<name> is the clearest tell:"
    # THE PLANTED PAIR (the negative arm the five-token window missed): the 2026-10-14 openings of IDVZ and TXUE
    idvz = ai.frame_of("IDVZ is the clearest fund-specific tell: it added Alpha Co.")
    txue = ai.frame_of("TXUE is the clearest tell: it sold Beta Corp.")
    assert idvz == txue == "<name> is the clearest tell:"
    # the control: openings that are different families stay different
    assert ai.frame_of("Gamma Co stands out most: it was sold.") == "<name> stands out:"
    assert ai.frame_of("Gamma Co stands out most: it was sold.") != idvz
    assert ai.frame_of("Alpha Co added $2.7 million over 2026-09-01 to 2026-09-30.") == "<name> added <n> million over <n> to <n>"
    # the clause ends at the colon; no colon means the whole first sentence, capped at eight tokens
    assert ai.frame_of("Alpha Co is the single most particular tell: x.") == "<name> is the tell:"
    assert ai.frame_of("Alpha Co led it all the way home today and then some.") == "<name> led it all the way home today"
    assert ai.frame_of("") == ""
    assert ai.FRAME_STOP == frozenset(("fund-specific", "most", "single", "particular"))


def test_ac2_a_correction_stores_its_reason_and_a_still_shared_reply_is_marked_not_resent():
    seen = {}
    first = Stub("TST1", "Alpha Co is the clearest fund-specific tell: it was bought.")
    m1 = json.loads(_verdict(_rows("TST1", first, seen))["input_manifest"])
    assert "shared_frame_with" not in m1 and "frame_still_shared" not in m1          # the first fund drew no correction
    # a family-sharing reply, corrected once into a distinct one: the reason is stored, nothing is marked
    second = Stub("TST2", "Beta Corp is the clearest tell: it was sold.", "Gamma Co stands out most: it was sold.")
    v2 = _verdict(_rows("TST2", second, seen))
    m2 = json.loads(v2["input_manifest"])
    assert len(_frame_corrections(second)) == 1 and m2["shared_frame_with"] == "TST1" and m2["corrections"] == 1
    assert "frame_still_shared" not in m2 and v2["text"].startswith("Gamma Co stands out most")
    # a reply that STILL shares the family after the one correction: ONE correction only, the reason stored, the row marked
    third = Stub("TST3", "Delta Inc is the clearest tell: it was sold.", "Delta Inc is the clearest fund-specific tell: it was sold again.")
    v3 = _verdict(_rows("TST3", third, seen))
    m3 = json.loads(v3["input_manifest"])
    assert len(_frame_corrections(third)) == 1 and m3["corrections"] == 1
    assert m3["shared_frame_with"] == "TST1" and m3["frame_still_shared"] is True
    assert v3["text"].startswith("Delta Inc is the clearest fund-specific tell: it was sold again")   # the reply stands
    assert seen["<name> is the clearest tell:"] == "TST1"                                              # first fund wins the record
    # the activity row's manifest carries neither key
    act = [r for r in _rows("TST4", Stub("TST4", "Epsilon Co rose: it was bought."), seen) if r["kind"] == "activity_30d"][0]
    assert "shared_frame_with" not in json.loads(act["input_manifest"])
