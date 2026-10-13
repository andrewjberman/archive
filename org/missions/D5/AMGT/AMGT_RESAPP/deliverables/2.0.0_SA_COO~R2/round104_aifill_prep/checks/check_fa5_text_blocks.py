"""check_fa5_text_blocks.py -- acceptance arms for AMGT-fa-5 (blocks mgmt_team_view, thesis_pillars, identity_description).

  PYTHONPATH=<repo root> python check_fa5_text_blocks.py
Offline, model stubbed. Needs lib.research.aifill.contract and .orchestrate (cell fa-1, merged before this cell is cut).
Each of the three blocks fills only where the page shows a gap: the research team's pack states no management passage
(mgmt_team_view), states no thesis pillars (thesis_pillars), or the identity header holds no description (identity_description).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402


def main():
    from lib.research.aifill import block_identity_description as D
    from lib.research.aifill import block_mgmt_team_view as T
    from lib.research.aifill import block_thesis_pillars as P
    from lib.research.aifill import contract

    arms = L.Arms("FA-5")
    web = lambda text="Plain text.": L.StubModel(L.result(text, citations=[L.web_cite("https://example.com/p", "Page")], searches=["q"], web_search_requests=1))  # noqa: E731

    # ---------------------------------------------------------------- mgmt_team_view
    def pack_none():
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["management"] = {"status": "ABSENT", "reason": "no management passage"}
        return inputs

    def team_held():
        m = web()
        block = T.build_block(L.ctx(L.served_inputs(), m))
        return block["block_id"] == "mgmt_team_view" and block["source_class"] == "NONE" and "research team" in block["reason"] and not m.calls, block.get("reason")
    arms.run("team_view: the pack states management -> NONE, no model call", team_held)

    def team_web():
        m = web("Management has a record of disciplined capital allocation.")
        block = T.build_block(L.ctx(pack_none(), m))
        call = m.calls[0]
        return (contract.validate_block(block) == [] and block["source_class"] == "WEB_SEARCH" and call["web_search_max_uses"] >= 1
                and "ASML Holding NV" in call["prompt"] and "Christophe Fouquet" in call["prompt"]
                and block["citations"][0]["url"] == "https://example.com/p"), (block["source_class"], block.get("reason"))
    arms.run("team_view: pack silent -> WEB_SEARCH, prompt names company and CEO", team_web)

    def team_not_team_voice():
        m = web()
        T.build_block(L.ctx(pack_none(), m))
        text = (m.calls[0]["prompt"] + " " + (m.calls[0]["system"] or "")).lower()
        return "research team" in text and ("not" in text) and "no_information" in text and "plain text" in text, text[:140]
    arms.run("team_view: prompt forbids speaking as the research team", team_not_team_voice)

    def team_pack_absent_key():
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"].pop("management")
        block = T.build_block(L.ctx(inputs, web()))
        return block["source_class"] == "WEB_SEARCH", block.get("reason")
    arms.run("team_view: a missing management key counts as the pack being silent", team_pack_absent_key)

    # ---------------------------------------------------------------- thesis_pillars
    def pillars_none():
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["thesis_pillars"] = []
        return inputs

    def pillars_held():
        m = web()
        block = P.build_block(L.ctx(L.served_inputs(), m))
        return block["block_id"] == "thesis_pillars" and block["source_class"] == "NONE" and "research team" in block["reason"] and not m.calls, block.get("reason")
    arms.run("pillars: the pack states pillars -> NONE, no model call", pillars_held)

    PILLAR_TEXT = "EUV lithography demand drives growth. The light source reached a new power level."

    def pillars_opal():
        m = L.StubModel(L.result(PILLAR_TEXT))
        block = P.build_block(L.ctx(pillars_none(), m))
        call = m.calls[0]
        return (contract.validate_block(block) == [] and block["source_class"] == "OPAL_SOURCE" and call["web_search_max_uses"] == 0
                and "1,000-watt light source" in call["prompt"] and all(c["source_kind"] == "opal" and L.plain_ref_ok(c["ref"]) for c in block["citations"])
                and block["citations"]), (block["source_class"], block.get("reason"))
    arms.run("pillars: pack silent, filing thesis sentences held -> OPAL_SOURCE from them", pillars_opal)

    def pillars_opal_refs():
        block = P.build_block(L.ctx(pillars_none(), L.StubModel(L.result(PILLAR_TEXT))))
        return any("filing" in c["ref"].lower() for c in block["citations"]), [c["ref"] for c in block["citations"]]
    arms.run("pillars: the opal citation names the filing analysis in words", pillars_opal_refs)

    def pillars_web():
        inputs = pillars_none()
        for s in inputs["thesis"]["drafted_sections"]:
            if s["section_id"] == "investment_thesis":
                s["sentences"] = s["sentences"][:1]
        m = web("Pillar one. Pillar two.")
        block = P.build_block(L.ctx(inputs, m))
        return block["source_class"] == "WEB_SEARCH" and m.calls[0]["web_search_max_uses"] >= 1, (block["source_class"], block.get("reason"))
    arms.run("pillars: fewer than two filing thesis sentences -> web path", pillars_web)

    def pillars_numeric():
        block = P.build_block(L.ctx(pillars_none(), L.StubModel(L.result("EUV demand grew 340 percent."))))
        return block["source_class"] == "NONE" and "figure" in block["reason"], block.get("reason")
    arms.run("pillars: a figure not in the filing sentences -> NONE naming 'figure'", pillars_numeric)

    # ---------------------------------------------------------------- identity_description
    def desc_none():
        inputs = L.served_inputs()
        inputs["overlay"]["top_band"]["description_line"] = None
        inputs["overlay"]["description"] = {"status": "ABSENT", "text": None}
        return inputs

    def desc_held():
        m = web()
        block = D.build_block(L.ctx(L.served_inputs(), m))
        return block["block_id"] == "identity_description" and block["source_class"] == "NONE" and "already" in block["reason"] and not m.calls, block.get("reason")
    arms.run("description: the header already holds one -> NONE ('already'), no model call", desc_held)

    def desc_web():
        m = web("ASML makes the lithography machines used to manufacture semiconductors.")
        block = D.build_block(L.ctx(desc_none(), m))
        call = m.calls[0]
        return (contract.validate_block(block) == [] and block["source_class"] == "WEB_SEARCH" and call["web_search_max_uses"] >= 1
                and "ASML Holding NV" in call["prompt"] and len(block["text"]) <= 400), (block["source_class"], block.get("reason"))
    arms.run("description: none held, no filing sentences -> WEB_SEARCH, text <= 400 chars", desc_web)

    def desc_long():
        block = D.build_block(L.ctx(desc_none(), web("x" * 900)))
        return block["source_class"] == "NONE" and "long" in block["reason"], block.get("reason")
    arms.run("description: an answer over 400 characters -> NONE naming 'long'", desc_long)

    def desc_opal():
        inputs = desc_none()
        inputs["thesis"]["drafted_sections"][0]["sentences"] = [
            {"text": "ASML develops and sells lithography systems for chipmakers.", "evidence": [{"id": "P0001", "location": None, "accession": None}]},
            {"text": "Its customers include the largest memory and logic producers.", "evidence": [{"id": "P0002", "location": None, "accession": None}]}]
        m = L.StubModel(L.result("ASML develops and sells lithography systems for chipmakers."))
        block = D.build_block(L.ctx(inputs, m))
        return block["source_class"] == "OPAL_SOURCE" and m.calls[0]["web_search_max_uses"] == 0 and "lithography systems" in m.calls[0]["prompt"] \
            and all(L.plain_ref_ok(c["ref"]) for c in block["citations"]), (block["source_class"], block.get("reason"))
    arms.run("description: filing company_description sentences held -> OPAL_SOURCE", desc_opal)

    def desc_overlay_missing():
        block = D.build_block(L.ctx({"overlay": None, "thesis": L.served_inputs()["thesis"], "errors": {"overlay": "status 500"}}, web()))
        return contract.validate_block(block) == [] and block["source_class"] == "NONE" and "overlay" not in block["reason"].lower(), block.get("reason")
    arms.run("description: the overlay body missing -> NONE (cannot tell whether the header has one)", desc_overlay_missing)

    # ---------------------------------------------------------------- all three
    def all_no_citation():
        for mod, inputs in ((T, pack_none()), (P, _silent_both()), (D, desc_none())):
            block = mod.build_block(L.ctx(inputs, L.StubModel(L.result("Text.", citations=[], web_search_requests=1))))
            if not (block["source_class"] == "NONE" and "citable" in block["reason"]):
                return False, (mod.__name__, block.get("reason"))
        return True

    def _silent_both():
        inputs = pillars_none()
        for s in inputs["thesis"]["drafted_sections"]:
            s["sentences"] = []
        return inputs
    arms.run("all three: a web answer with no citation -> NONE naming 'citable'", all_no_citation)

    def all_no_info():
        for mod, inputs in ((T, pack_none()), (P, _silent_both()), (D, desc_none())):
            block = mod.build_block(L.ctx(inputs, L.StubModel(L.result("NO_INFORMATION", citations=[L.web_cite()], web_search_requests=1))))
            if block["source_class"] != "NONE":
                return False, mod.__name__
        return True
    arms.run("all three: NO_INFORMATION -> NONE", all_no_info)

    for mod, label in ((T, "team_view"), (P, "pillars"), (D, "description")):
        arms.raises("%s: a model failure propagates" % label, "RuntimeError",
                    lambda mod=mod: mod.build_block(L.ctx({"overlay": {"top_band": {"description_line": None}, "description": {"status": "ABSENT"}, "name": "X", "display_name": "X"},
                                                          "thesis": {"dossier_fields": {"management": None, "thesis_pillars": []}, "management": {"officers": []}, "drafted_sections": []},
                                                          "errors": {}}, L.StubModel(RuntimeError("down")))))

    def no_io_imports():
        bad = []
        for mod in (T, P, D):
            src = open(mod.__file__, "r", encoding="utf-8").read()
            bad += [(mod.__name__, w) for w in ("import boto3", "import urllib", "import requests", "import anthropic", "import socket") if w in src]
            if not open(mod.__file__, "rb").read().isascii():
                bad.append((mod.__name__, "non-ASCII"))
        return not bad, bad
    arms.run("no I/O imports; sources are ASCII", no_io_imports)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
