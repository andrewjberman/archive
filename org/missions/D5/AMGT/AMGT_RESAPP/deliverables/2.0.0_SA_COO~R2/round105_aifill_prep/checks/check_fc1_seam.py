"""check_fc1_seam.py -- acceptance arms for AMGT-fc-1 (the model seam keeps ONLY the model's final answer, never its narration).

  PYTHONPATH=<repo root> python check_fc1_seam.py
Offline. Imports lib.research.aifill.model. The defect (CVO C-S133): `parse_response` joined EVERY text block of a web-search reply, so the model's pre-search
chatter ("I'll research this now.") was glued onto the answer ("now.MUFG announced ...").
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402


def text(t, cites=()):
    block = {"type": "text", "text": t}
    if cites:
        block["citations"] = [{"type": "web_search_result_location", "url": u, "title": "T " + u, "cited_text": "c"} for u in cites]
    return block


def tool(q):
    return {"type": "server_tool_use", "id": "srvtoolu_" + q, "name": "web_search", "input": {"query": q}}


def result(url):
    return {"type": "web_search_tool_result", "tool_use_id": "x", "content": [{"type": "web_search_result", "url": url, "title": "R"}]}


def response(content, stop="end_turn", searches=None):
    return {"content": content, "stop_reason": stop, "model": "claude-opus-5",
            "usage": {"input_tokens": 100, "output_tokens": 50, "server_tool_use": {"web_search_requests": searches if searches is not None else sum(1 for b in content if b["type"] == "server_tool_use")}}}


def main():
    from lib.research.aifill import model

    arms = L.Arms("FC-1")
    fixture = L.web_response()["response"]

    def recorded():
        r = model.parse_response(fixture)
        urls = [c["url"] for c in r.citations]
        return "Christophe Fouquet" in r.text and len(set(urls)) >= 3 and r.web_search_requests == 2, (len(urls), r.text[:50])
    arms.run("the recorded real response still parses: text, 3+ citations, 2 searches", recorded)

    def preamble_dropped():
        r = model.parse_response(response([text("I'll research this now."), tool("q1"), result("https://a.example/1"), text("MUFG named a new president.", ["https://a.example/1"])]))
        return r.text == "MUFG named a new president." and "research" not in r.text, repr(r.text)
    arms.run("one preamble block before the search is dropped (the CVO's case)", preamble_dropped)

    def many_segments():
        r = model.parse_response(response([text("Let me check."), tool("q1"), result("https://a.example/1"), text("Now another look."), tool("q2"), result("https://a.example/2"),
                                          text("Final one. "), text("Final two.", ["https://a.example/2"])]))
        return r.text == "Final one. Final two.", repr(r.text)
    arms.run("narration around several searches: only the text after the LAST search result is kept", many_segments)

    def no_tools():
        r = model.parse_response(response([text("Hello "), text("world.")]))
        return r.text == "Hello world." and r.web_search_requests == 0, repr(r.text)
    arms.run("a reply with no search keeps all its text (the Opal path)", no_tools)

    def citations_final_only():
        r = model.parse_response(response([text("Chatter.", ["https://noise.example/x"]), tool("q"), result("https://a.example/1"), text("Answer.", ["https://good.example/y"])]))
        urls = [c["url"] for c in r.citations]
        return urls == ["https://good.example/y"], urls
    arms.run("citations are taken from the final segment only", citations_final_only)

    def narration_between_tool_and_result_order():
        r = model.parse_response(response([tool("q"), text("Searching again."), result("https://a.example/1"), text("The answer.")]))
        return r.text == "The answer.", repr(r.text)
    arms.run("text between a search call and its result is not the answer either", narration_between_tool_and_result_order)

    arms.raises("nothing after the last search is a ModelError (no answer)", "ModelError",
                lambda: model.parse_response(response([text("I'll research this."), tool("q"), result("https://a.example/1")])))

    arms.raises("a whitespace-only final segment is a ModelError", "ModelError",
                lambda: model.parse_response(response([tool("q"), result("https://a.example/1"), text("   ")])))

    arms.raises("max_tokens is still a ModelError", "ModelError",
                lambda: model.parse_response(response([tool("q"), result("https://a.example/1"), text("Cut off")], stop="max_tokens")))

    def counts_unchanged():
        r = model.parse_response(response([text("x"), tool("q1"), result("https://a.example/1"), tool("q2"), result("https://a.example/2"), text("Done.")]))
        return r.searches == ["q1", "q2"] and r.web_search_requests == 2 and r.input_tokens == 100 and r.output_tokens == 50, (r.searches, r.web_search_requests)
    arms.run("searches, web_search_requests and token counts still cover the whole reply", counts_unchanged)

    def call_model_uses_it():
        out = model.call_model("P", web_search_max_uses=2, transport=lambda body: response([text("I'll look into it."), tool("q"), result("https://a.example/1"), text("Answer only.")]))
        return out.text == "Answer only.", repr(out.text)
    arms.run("call_model returns the final answer only", call_model_uses_it)

    def no_sdk():
        return "anthropic" not in sys.modules, "anthropic imported"
    arms.run("the anthropic SDK is still never imported", no_sdk)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
