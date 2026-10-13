"""aifill_check_lib.py -- shared helpers for the AMGT-fa-* acceptance checks (AMGT_RESAPP round 103, workstream AIFILL).

Plain functions, no framework. Python 3.9 syntax. Every check prints one line per arm
(`ARM <name> PASS|FAIL [detail]`) and a final line `AIFILL <CELL> ARMS: YES (k of k)` or `NO (k of n)`.
"""
from __future__ import annotations

import copy
import datetime
import json
import os
import types

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(os.path.dirname(HERE), "fixtures")
NOW = datetime.datetime(2026, 10, 13, 12, 0, 0, tzinfo=datetime.timezone.utc)
BLOCK_IDS = ("mgmt_bio", "mgmt_recent", "mgmt_team_view", "thesis_pillars", "identity_description")


class Arms:
    def __init__(self, cell):
        self.cell = cell
        self.rows = []

    def run(self, name, fn):
        try:
            result = fn()
            ok = bool(result) if not isinstance(result, tuple) else bool(result[0])
            detail = "" if not isinstance(result, tuple) else str(result[1])[:200]
        except Exception as err:  # noqa: BLE001 -- an arm that raises is a failed arm, with its error printed
            ok, detail = False, "%s: %s" % (type(err).__name__, str(err)[:200])
        self.rows.append((name, ok))
        print("ARM %-52s %s %s" % (name, "PASS" if ok else "FAIL", detail))
        return ok

    def raises(self, name, exc_name, fn):
        def go():
            try:
                fn()
            except Exception as err:  # noqa: BLE001
                return type(err).__name__ == exc_name or any(c.__name__ == exc_name for c in type(err).__mro__), type(err).__name__
            return False, "did not raise"
        return self.run(name, go)

    def finish(self):
        passed = sum(1 for _, ok in self.rows if ok)
        total = len(self.rows)
        verdict = "YES" if passed == total and total > 0 else "NO"
        print("AIFILL %s ARMS: %s (%d of %d)" % (self.cell, verdict, passed, total))
        return 0 if verdict == "YES" else 1


def served_inputs():
    """A deep copy of the recorded served bodies for ASML_NA_Equity (overlay + thesis, trimmed)."""
    with open(os.path.join(FIXTURES, "served_inputs_ASML_NA_Equity.json"), "r", encoding="utf-8") as handle:
        return copy.deepcopy(json.load(handle))


def web_response():
    """The recorded real Messages API response (two web searches, cited) and the request that produced it."""
    with open(os.path.join(FIXTURES, "web_search_response_asml.json"), "r", encoding="utf-8") as handle:
        return json.load(handle)


class StubModel:
    """A ctx.model stand-in: returns canned results in order (the last repeats) and records every call."""

    def __init__(self, *results):
        self.results = list(results)
        self.calls = []

    def __call__(self, prompt, *, system=None, web_search_max_uses=0, max_tokens=1500):
        self.calls.append({"prompt": prompt, "system": system, "web_search_max_uses": web_search_max_uses, "max_tokens": max_tokens})
        index = min(len(self.calls) - 1, len(self.results) - 1)
        result = self.results[index]
        if isinstance(result, Exception):
            raise result
        return result


def result(text, citations=(), searches=(), web_search_requests=0, input_tokens=100, output_tokens=50):
    return types.SimpleNamespace(
        text=text,
        citations=[dict(c) for c in citations],
        searches=list(searches),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        web_search_requests=web_search_requests,
        model="stub-model",
        stop_reason="end_turn",
    )


def web_cite(url="https://example.com/a", title="A page", cited_text="Some cited text."):
    return {"url": url, "title": title, "cited_text": cited_text}


def ctx(inputs, model, security_key="ASML_NA_Equity", now=NOW):
    from lib.research.aifill.orchestrate import BlockContext

    return BlockContext(security_key, inputs, model, now)


def plain_ref_ok(ref):
    """An analyst-facing source label: words, not a code path."""
    return isinstance(ref, str) and ref.strip() != "" and not any(ch in ref for ch in "_[]{}") and not ref.startswith(("thesis.", "overlay."))
