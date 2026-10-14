"""check_gr6_builders.py -- acceptance arms for AMGT-gr-6 (the five builders cut at a REAL sentence end; the bio never restates the research team's passage).

  PYTHONPATH=<repo root> python check_gr6_builders.py
Offline, model stubbed. Imports the five block modules, contract and sentences (gr-1). The CVO's measured defects: KOFUBL MM mgmt_team_view ended `... totaling Ps.` on the page (every builder
carried its own copy of a cut that took an abbreviation for a sentence end), and V US mgmt_bio (OPAL_SOURCE) restated the research team's management passage printed directly above it.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

TAIL_A = "The board proposed a 2025 ordinary dividend of Ps. 7.36 per unit, totaling Ps."
TAIL_B = " 15.5 billion, payable in two instalments."
RESTATES = "The research team's passage on this page already says this, so no summary was added."


def reply_for(cap):
    """Whole sentences ending exactly 2 characters short of cap, then a tail whose 'Ps.' abbreviations straddle the cap."""
    unit = "Results for the year were solid. "
    head = ""
    while len(head) + len(unit) + len(TAIL_A) + 1 < cap - 2:
        head += unit
    pad = cap - 2 - len(head) - len(TAIL_A) - 1  # one space joins head and TAIL_A
    head = head.rstrip()
    if pad > 0:
        head = head[:-1] + (" and very steady indeed" * 40)[:pad] + "."
    full = head + " " + TAIL_A + TAIL_B
    return head, full


def sparse():
    inputs = L.served_inputs()
    inputs["thesis"]["dossier_fields"]["management"] = {"status": "ABSENT", "reason": "none"}
    inputs["thesis"]["dossier_fields"]["thesis_pillars"] = []
    inputs["overlay"]["top_band"]["description_line"] = None
    inputs["overlay"]["description"] = {"status": "ABSENT", "text": None}
    for s in inputs["thesis"]["drafted_sections"]:
        s["sentences"] = []
    inputs["overlay"]["feed"]["items"] = []
    return inputs


def main():
    from lib.research.aifill import block_identity_description as D
    from lib.research.aifill import block_mgmt_bio as B
    from lib.research.aifill import block_mgmt_recent as R
    from lib.research.aifill import block_mgmt_team_view as T
    from lib.research.aifill import block_thesis_pillars as P
    from lib.research.aifill import sentences

    arms = L.Arms("GR-6")
    web = lambda t: L.StubModel(L.result(t, citations=[L.web_cite()], web_search_requests=1))  # noqa: E731

    for name, mod, cap in (("mgmt_bio", B, 900), ("mgmt_recent", R, 800), ("mgmt_team_view", T, 800), ("thesis_pillars", P, 1000), ("identity_description", D, 400)):
        def cut_arm(mod=mod, cap=cap):
            head, full = reply_for(cap)
            block = mod.build_block(L.ctx(sparse(), web(full)))
            text = block.get("text") or ""
            return (block["source_class"] == "WEB_SEARCH" and text == head and not text.rstrip().endswith("Ps.") and len(full) > cap and len(head) <= cap), (block["source_class"], text[-40:], block.get("reason"))
        arms.run("%s: an over-cap reply is cut at the last REAL sentence end (never at 'Ps.')" % name, cut_arm)

    def within_cap_kept():
        out = []
        for mod in (B, R, T, P, D):
            text = "The company reported results for the year. The board proposed a dividend of Ps. 7.36 per unit."
            block = mod.build_block(L.ctx(sparse(), web(text)))
            out.append(block.get("text") == text)
        return all(out), out
    arms.run("a reply within the cap, abbreviations included, is kept whole by all five", within_cap_kept)

    def no_cap_fit():
        text = "A very long single clause that never stops and mentions Ps. 7 and more " * 20
        res = [mod.build_block(L.ctx(sparse(), web(text))) for mod in (B, R, T, P, D)]
        return all(b["source_class"] == "NONE" and "too long" in b["reason"] for b in res), [b["source_class"] for b in res]
    arms.run("a long reply with no real sentence end is withheld as 'too long' by all five", no_cap_fit)

    def uses_shared_helper():
        bad = []
        for mod in (B, R, T, P, D):
            src = open(mod.__file__, "r", encoding="utf-8").read()
            if "sentences" not in src:
                bad.append(mod.__name__)
        return not bad, bad
    arms.run("each builder imports the shared sentences module", uses_shared_helper)

    PACK = ("Management and capital allocation: President and CEO Christophe Fouquet joined ASML in 2008 and held several management positions in marketing and product management "
            "prior to CEO, including Chief Business Officer from 2022 to 2024. Prior to ASML, he worked at industry peers KLA Tencor and Applied Materials.")

    def pack_inputs(role_start=None):
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["management"] = {"status": "SERVED", "value": PACK}
        if role_start is not None:
            inputs["thesis"]["management"]["officers"][0]["role_start"] = role_start
            inputs["thesis"]["management"]["officers"][0]["tenure_years"] = 2
        return inputs

    def restates_withheld():
        reply = ("Christophe Fouquet joined ASML in 2008 and held several management positions in marketing and product management prior to becoming CEO. "
                 "Before ASML he worked at KLA Tencor and Applied Materials.")
        model = L.RouterModel(opal=L.result(reply), web=None)
        block = B.build_block(L.ctx(pack_inputs(), model))
        return block["source_class"] == "NONE" and RESTATES in block["reason"] and model.kinds() == ["opal", "web"], (block["source_class"], block.get("reason"), model.kinds())
    arms.run("bio: an Opal reply that restates the pack passage is withheld with the stated reason, then the web path runs", restates_withheld)

    def restates_then_web():
        reply = ("Christophe Fouquet joined ASML in 2008 and held several management positions in marketing and product management prior to becoming CEO. "
                 "Before ASML he worked at KLA Tencor and Applied Materials.")
        web_reply = L.result("Fouquet became chief executive of ASML in April 2024 after Peter Wennink retired.", citations=[L.web_cite("https://example.com/asml", "ASML news")], web_search_requests=1)
        block = B.build_block(L.ctx(pack_inputs(), L.RouterModel(opal=L.result(reply), web=web_reply)))
        return block["source_class"] == "WEB_SEARCH" and "Wennink" in block["text"], (block["source_class"], block.get("reason"))
    arms.run("bio: after the withheld restatement the web path still gets its turn", restates_then_web)

    def fresh_kept():
        reply = "Christophe Fouquet has been chief executive since 2024. He has served two years in the role."
        block = B.build_block(L.ctx(pack_inputs(role_start=2024), L.RouterModel(opal=L.result(reply), web=None)))
        return block["source_class"] == "OPAL_SOURCE" and block["text"] == reply, (block["source_class"], block.get("reason"))
    arms.run("bio: an Opal reply that adds what the pack passage lacks is kept (OPAL_SOURCE)", fresh_kept)

    def no_pack_no_check():
        inputs = pack_inputs(role_start=2024)
        inputs["thesis"]["dossier_fields"]["management"] = {"status": "ABSENT", "reason": "none"}
        reply = "Christophe Fouquet has been chief executive since 2024."
        block = B.build_block(L.ctx(inputs, L.RouterModel(opal=L.result(reply), web=None)))
        return block["source_class"] == "OPAL_SOURCE", (block["source_class"], block.get("reason"))
    arms.run("bio: with no pack passage there is nothing to restate (no check)", no_pack_no_check)

    def reason_constant():
        return getattr(B, "RESTATES_REASON", None) == RESTATES, getattr(B, "RESTATES_REASON", None)
    arms.run("bio: RESTATES_REASON is the stated sentence", reason_constant)

    def helper_cut_equal():
        head, full = reply_for(900)
        return sentences.cut_at_sentence_end(full, 900) == head, "ok"
    arms.run("the check's own fixture agrees with sentences.cut_at_sentence_end", helper_cut_equal)

    def src_check():
        bad = []
        for mod in (B, R, T, P, D):
            data = open(mod.__file__, "rb").read()
            if not data.isascii() or any(w in data for w in (b"import boto3", b"import urllib", b"import requests", b"import anthropic", b"import socket")):
                bad.append(mod.__name__)
        return not bad, bad
    arms.run("the five modules stay ASCII and do no I/O", src_check)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
