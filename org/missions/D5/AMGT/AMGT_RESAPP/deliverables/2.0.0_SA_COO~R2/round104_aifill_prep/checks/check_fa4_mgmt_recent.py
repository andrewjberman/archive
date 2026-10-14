"""check_fa4_mgmt_recent.py -- acceptance arms for AMGT-fa-4 (block mgmt_recent: recent developments on executive management).

  PYTHONPATH=<repo root> python check_fa4_mgmt_recent.py
Offline, model stubbed. Needs lib.research.aifill.contract and .orchestrate (cell fa-1, merged before this cell is cut).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402


def item(title, day, key, publisher="bbg", url="https://www.bloomberg.com/news/articles/x"):
    return {"publisher": publisher, "publisher_name": "Bloomberg", "published_at": day + "T06:00:00Z", "published_date": day, "article_key": key,
            "url": url, "title": title, "headline": title}


def main():
    from lib.research.aifill import block_mgmt_recent as B
    from lib.research.aifill import contract

    arms = L.Arms("FA-4")

    def with_items(*items):
        inputs = L.served_inputs()
        inputs["overlay"]["feed"]["items"] = list(items)
        inputs["overlay"]["feed"]["item_count"] = len(items)
        return inputs

    HEAD = item("ASML names new chief financial officer", "2026-10-01", "bbg:A1")
    OTHER = item("Qualcomm licenses patents linked to Huawei", "2026-10-05", "bbg:A2")
    OLD = item("ASML CEO to step down", "2026-03-01", "bbg:A3")
    SUMMARY = "ASML named a new chief financial officer."

    def opal_case():
        m = L.StubModel(L.result(SUMMARY))
        block = B.build_block(L.ctx(with_items(HEAD, OTHER), m))
        call = m.calls[0]
        return (contract.validate_block(block) == [] and block["source_class"] == "OPAL_SOURCE" and call["web_search_max_uses"] == 0
                and "new chief financial officer" in call["prompt"] and "Qualcomm" not in call["prompt"] and len(m.calls) == 1), (block["source_class"], block.get("reason"))
    arms.run("a management headline in the last 90 days -> OPAL_SOURCE, only that headline sent", opal_case)

    def opal_citations():
        block = B.build_block(L.ctx(with_items(HEAD, OTHER), L.StubModel(L.result(SUMMARY))))
        cites = block["citations"]
        return (len(cites) == 1 and cites[0]["source_kind"] == "opal" and cites[0]["url"] == HEAD["url"] and L.plain_ref_ok(cites[0]["ref"])
                and "Bloomberg" in cites[0]["ref"] and "2026-10-01" in cites[0]["ref"] and cites[0]["title"] == HEAD["title"]), cites
    arms.run("one opal citation per headline used: plain ref, link, title", opal_citations)

    def old_ignored():
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(with_items(OLD, OTHER), m))
        return block["source_class"] == "WEB_SEARCH" and m.calls[0]["web_search_max_uses"] >= 1, block.get("reason")
    arms.run("a headline older than 90 days is not Opal evidence -> web path", old_ignored)

    def no_items():
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(with_items(), m))
        return block["source_class"] == "WEB_SEARCH", block.get("reason")
    arms.run("empty feed -> web path", no_items)

    def numeric_guard():
        block = B.build_block(L.ctx(with_items(HEAD), L.StubModel(L.result("ASML named a new CFO and raised guidance to 45 billion."))))
        return block["source_class"] == "NONE" and "figure" in block["reason"], block.get("reason")
    arms.run("a figure not in the headlines -> NONE naming 'figure'", numeric_guard)

    def web_prompt():
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        B.build_block(L.ctx(with_items(), m))
        text = (m.calls[0]["prompt"] + " " + (m.calls[0]["system"] or "")).lower()
        return "ASML Holding NV" in m.calls[0]["prompt"] and ("recent" in text) and "no_information" in text and "plain text" in text, text[:120]
    arms.run("web prompt names the company, 'recent', plain text, NO_INFORMATION", web_prompt)

    def web_no_citation():
        block = B.build_block(L.ctx(with_items(), L.StubModel(L.result("Text.", citations=[], web_search_requests=1))))
        return block["source_class"] == "NONE" and "citable" in block["reason"], block.get("reason")
    arms.run("web answer with no citation -> NONE naming 'citable'", web_no_citation)

    def no_info():
        block = B.build_block(L.ctx(with_items(), L.StubModel(L.result("NO_INFORMATION", citations=[L.web_cite()], web_search_requests=1))))
        return block["source_class"] == "NONE", block.get("reason")
    arms.run("NO_INFORMATION -> NONE", no_info)

    def missing_feed():
        for inputs in ({"overlay": None, "thesis": None, "errors": {}}, {"overlay": {"feed": None}, "thesis": None, "errors": {}}):
            m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
            block = B.build_block(L.ctx(inputs, m))
            if contract.validate_block(block) != []:
                return False, block
        return True
    arms.run("overlay missing or feed null: valid block, no exception", missing_feed)

    def now_is_ctx_now():
        far = L.NOW.replace(year=2028)
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(with_items(HEAD), m, now=far))
        return block["source_class"] == "WEB_SEARCH", block.get("reason")
    arms.run("the 90-day window is measured from ctx.now, not the wall clock", now_is_ctx_now)

    # ---- AMENDMENT 2
    def opal_falls_to_web():
        m = L.StubModel(L.result("NO_INFORMATION"), L.result("The company named a new chief financial officer.", citations=[L.web_cite("https://example.com/n", "News")], web_search_requests=1))
        block = B.build_block(L.ctx(with_items(HEAD), m))
        return (block["source_class"] == "WEB_SEARCH" and len(m.calls) == 2 and m.calls[0]["web_search_max_uses"] == 0 and m.calls[1]["web_search_max_uses"] >= 1), (block["source_class"], len(m.calls), block.get("reason"))
    arms.run("an Opal path that finds nothing falls through to the web path", opal_falls_to_web)

    def guard_falls_then_none():
        m = L.StubModel(L.result("ASML named a new CFO and raised guidance to 45 billion."), L.result("NO_INFORMATION", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(with_items(HEAD), m))
        return block["source_class"] == "NONE" and len(m.calls) == 2 and "figure" in block["reason"] and "_" not in block["reason"], (len(m.calls), block.get("reason"))
    arms.run("a numeric-guard failure falls through; if the web path declines too the reason keeps 'figure'", guard_falls_then_none)

    def long_text_cut():
        long_text = " ".join(["The company announced a leadership change at the top." for _ in range(30)])
        m = L.StubModel(L.result(long_text, citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(with_items(), m))
        text = block["text"] or ""
        return (block["source_class"] == "WEB_SEARCH" and 0 < len(text) <= 800 and text.endswith(".") and long_text.startswith(text)), (block["source_class"], len(text), block.get("reason"))
    arms.run("a reply over the 800-character cap is cut at the last sentence end that fits", long_text_cut)

    def long_no_sentence_end():
        block = B.build_block(L.ctx(with_items(), L.StubModel(L.result("word " * 400, citations=[L.web_cite()], web_search_requests=1))))
        return block["source_class"] == "NONE" and "long" in block["reason"], block.get("reason")
    arms.run("a reply over the cap with no sentence end is withheld, naming 'long'", long_no_sentence_end)

    def prompts_state_limit():
        m = L.StubModel(L.result("Text.", citations=[L.web_cite()], web_search_requests=1))
        B.build_block(L.ctx(with_items(), m))
        o = L.StubModel(L.result("ASML named a new chief financial officer."))
        B.build_block(L.ctx(with_items(HEAD), o))
        return "700 characters" in m.calls[0]["prompt"] and "700 characters" in o.calls[0]["prompt"], m.calls[0]["prompt"][-100:]
    arms.run("both prompts state the 700-character limit", prompts_state_limit)

    arms.raises("a model failure propagates", "RuntimeError", lambda: B.build_block(L.ctx(with_items(HEAD), L.StubModel(RuntimeError("down")))))

    def no_io_imports():
        src = open(B.__file__, "r", encoding="utf-8").read()
        banned = [w for w in ("import boto3", "import urllib", "import requests", "import anthropic", "import socket") if w in src]
        return not banned and open(B.__file__, "rb").read().isascii(), banned
    arms.run("no I/O imports; source is ASCII", no_io_imports)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
