"""check_fa3_mgmt_bio.py -- acceptance arms for AMGT-fa-3 (block mgmt_bio: the management bio summary).

  PYTHONPATH=<repo root> python check_fa3_mgmt_bio.py
Offline, model stubbed. Needs lib.research.aifill.contract and .orchestrate (cell fa-1, merged before this cell is cut).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402


def main():
    from lib.research.aifill import block_mgmt_bio as B
    from lib.research.aifill import contract

    arms = L.Arms("FA-3")
    BIO_TEXT = "Christophe Fouquet has served as chief executive since April 2024. His mandate runs to the end of the decade."

    def opal_case():
        inputs = L.served_inputs()
        m = L.StubModel(L.result(BIO_TEXT))
        block = B.build_block(L.ctx(inputs, m))
        call = m.calls[0]
        return (contract.validate_block(block) == [] and block["block_id"] == "mgmt_bio" and block["source_class"] == "OPAL_SOURCE"
                and call["web_search_max_uses"] == 0 and "Christophe Fouquet" in call["prompt"] and "joined ASML in 2008" in call["prompt"]
                and block["text"] == BIO_TEXT and len(m.calls) == 1), (block["source_class"], block.get("reason"))
    arms.run("pack states management -> OPAL_SOURCE, one call, no web search", opal_case)

    def opal_citations():
        block = B.build_block(L.ctx(L.served_inputs(), L.StubModel(L.result(BIO_TEXT))))
        cites = block["citations"]
        return (cites and all(c["source_kind"] == "opal" for c in cites) and all(L.plain_ref_ok(c["ref"]) for c in cites)
                and any("research team" in c["ref"].lower() for c in cites)
                and block["opal_inputs"] and block["model_call"] and block["model_call"]["web_search_requests"] == 0), [c["ref"] for c in cites]
    arms.run("OPAL citation is a plain-words source label (the research team's pack: ASML's CEO row has no role start, so no officer fact)", opal_citations)

    def opal_officer_fact():
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["management"] = {"status": "ABSENT", "reason": "none"}
        for officer in inputs["thesis"]["management"]["officers"]:
            if "CEO" in (officer.get("role") or ""):
                officer["role_start"] = "March 2023"
                officer["tenure_years"] = 3.5
        m = L.StubModel(L.result("Christophe Fouquet became CEO in March 2023."))
        block = B.build_block(L.ctx(inputs, m))
        refs = [c["ref"] for c in block["citations"]]
        return (block["source_class"] == "OPAL_SOURCE" and m.calls[0]["web_search_max_uses"] == 0 and "March 2023" in m.calls[0]["prompt"]
                and any("officer" in r.lower() for r in refs) and all(L.plain_ref_ok(r) for r in refs)), (block["source_class"], block.get("reason"), refs)
    arms.run("a CEO row with a role start is an Opal officer fact (plain 'officer list' citation)", opal_officer_fact)

    def numeric_guard():
        m = L.StubModel(L.result("Christophe Fouquet joined ASML in 1987 and is CEO."))
        block = B.build_block(L.ctx(L.served_inputs(), m))
        return block["source_class"] == "NONE" and "figure" in block["reason"], block.get("reason")
    arms.run("a year not in the supplied facts -> NONE naming 'figure'", numeric_guard)

    def no_information():
        block = B.build_block(L.ctx(L.served_inputs(), L.StubModel(L.result("NO_INFORMATION"))))
        return block["source_class"] == "NONE" and block["reason"] and "_" not in block["reason"], block.get("reason")
    arms.run("model says NO_INFORMATION -> NONE with a plain reason", no_information)

    def sparse_inputs():
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["management"] = {"status": "ABSENT", "reason": "none"}
        for officer in inputs["thesis"]["management"]["officers"]:
            officer["role_start"] = None
            officer["tenure_years"] = None
        return inputs

    def web_case():
        m = L.StubModel(L.result("Christophe Fouquet became CEO in 2024 after leading ASML's EUV business.",
                                 citations=[L.web_cite("https://www.asml.com/en/company/management", "ASML management"), L.web_cite("https://example.com/b", "Profile")],
                                 searches=["ASML CEO"], web_search_requests=2))
        block = B.build_block(L.ctx(sparse_inputs(), m))
        call = m.calls[0]
        return (contract.validate_block(block) == [] and block["source_class"] == "WEB_SEARCH" and call["web_search_max_uses"] >= 1
                and "Christophe Fouquet" in call["prompt"] and "ASML Holding NV" in call["prompt"]
                and [c["url"] for c in block["citations"]] == ["https://www.asml.com/en/company/management", "https://example.com/b"]
                and block["model_call"]["web_search_requests"] == 2 and block["model_call"]["model"] == "stub-model"), (block["source_class"], block.get("reason"))
    arms.run("no Opal source -> WEB_SEARCH with the model's citations", web_case)

    def web_prompt_rules():
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        B.build_block(L.ctx(sparse_inputs(), m))
        text = (m.calls[0]["prompt"] + " " + (m.calls[0]["system"] or "")).lower()
        return "no_information" in text and "plain text" in text and ("only" in text), text[:120]
    arms.run("web prompt tells the model: plain text, only supported facts, NO_INFORMATION", web_prompt_rules)

    def web_no_citation():
        block = B.build_block(L.ctx(sparse_inputs(), L.StubModel(L.result("Some bio text.", citations=[], web_search_requests=1))))
        return block["source_class"] == "NONE" and "citable" in block["reason"], block.get("reason")
    arms.run("web answer with no citation -> NONE naming 'citable'", web_no_citation)

    def web_no_info():
        block = B.build_block(L.ctx(sparse_inputs(), L.StubModel(L.result("NO_INFORMATION", citations=[L.web_cite()], web_search_requests=1))))
        return block["source_class"] == "NONE", block.get("reason")
    arms.run("web NO_INFORMATION -> NONE", web_no_info)

    def unfolded_text():
        m = L.StubModel(L.result("**Christophe Fouquet** joined ASML – in 2008.", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(sparse_inputs(), m))
        return block["text"] is not None and block["text"].isascii() and "**" not in block["text"], block.get("text")
    arms.run("model markdown and non-ASCII are folded out of the stored text", unfolded_text)

    def unknown_ceo():
        inputs = sparse_inputs()
        inputs["thesis"]["management"]["officers"] = []
        m = L.StubModel(L.result("The company's chief executive has led it since 2020.", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(inputs, m))
        return block["source_class"] == "WEB_SEARCH" and "chief executive" in m.calls[0]["prompt"].lower(), m.calls[0]["prompt"][:120]
    arms.run("no officer row: web prompt asks for 'the chief executive officer'", unknown_ceo)

    def missing_bodies():
        inputs = {"overlay": None, "thesis": None, "errors": {"thesis": "status 500"}}
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(inputs, m))
        return contract.validate_block(block) == [], block.get("reason")
    arms.run("both served bodies missing: still a valid block, no exception", missing_bodies)

    # ---- AMENDMENT 2: character limits, the sentence cut, the Opal -> web fall-through
    def opal_falls_to_web():
        m = L.StubModel(L.result("NO_INFORMATION"),
                        L.result("Christophe Fouquet became CEO of ASML in 2024.", citations=[L.web_cite("https://example.com/c", "Profile")], web_search_requests=1))
        block = B.build_block(L.ctx(L.served_inputs(), m))
        return (block["source_class"] == "WEB_SEARCH" and len(m.calls) == 2 and m.calls[0]["web_search_max_uses"] == 0
                and m.calls[1]["web_search_max_uses"] >= 1 and block["citations"][0]["url"] == "https://example.com/c"), (block["source_class"], len(m.calls), block.get("reason"))
    arms.run("an Opal path that finds nothing falls through to the web path", opal_falls_to_web)

    def opal_guard_falls_to_web_then_none():
        m = L.StubModel(L.result("Christophe Fouquet joined ASML in 1987 and is CEO."),
                        L.result("NO_INFORMATION", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(L.served_inputs(), m))
        return (block["source_class"] == "NONE" and len(m.calls) == 2 and "figure" in block["reason"] and "_" not in block["reason"]), (len(m.calls), block.get("reason"))
    arms.run("a numeric-guard failure also falls through; if the web path declines too the reason keeps 'figure'", opal_guard_falls_to_web_then_none)

    def long_text_cut():
        long_text = " ".join(["Dr. Lisa Su has led the company as chief executive officer for many years." for _ in range(20)])
        m = L.StubModel(L.result(long_text, citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(sparse_inputs(), m))
        text = block["text"] or ""
        return (block["source_class"] == "WEB_SEARCH" and 0 < len(text) <= 900 and text.endswith(".") and long_text.startswith(text)), (block["source_class"], len(text), block.get("reason"))
    arms.run("a reply over the 900-character cap is cut at the last sentence end that fits", long_text_cut)

    def long_no_sentence_end():
        m = L.StubModel(L.result("word " * 400, citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(sparse_inputs(), m))
        return block["source_class"] == "NONE" and "long" in block["reason"], block.get("reason")
    arms.run("a reply over the cap with no sentence end is withheld, naming 'long'", long_no_sentence_end)

    def prompts_state_limit():
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        B.build_block(L.ctx(sparse_inputs(), m))
        o = L.StubModel(L.result("Christophe Fouquet joined ASML in 2008."))
        B.build_block(L.ctx(L.served_inputs(), o))
        return "800 characters" in m.calls[0]["prompt"] and "800 characters" in o.calls[0]["prompt"], (m.calls[0]["prompt"][-120:])
    arms.run("both prompts state the 800-character limit", prompts_state_limit)

    arms.raises("a model failure propagates (the orchestrator converts it)", "RuntimeError",
                lambda: B.build_block(L.ctx(L.served_inputs(), L.StubModel(RuntimeError("model down")))))

    def no_io_imports():
        src = open(B.__file__, "r", encoding="utf-8").read()
        banned = [w for w in ("import boto3", "import urllib", "import requests", "import anthropic", "import socket") if w in src]
        return not banned, banned
    arms.run("the module does no I/O of its own", no_io_imports)

    def ascii_source():
        data = open(B.__file__, "rb").read()
        return data.isascii(), "non-ASCII byte in source"
    arms.run("the source file is ASCII", ascii_source)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
