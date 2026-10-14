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


# ---------------------------------------------------------------------------
# Round 106 (grounding pass) helpers
# ---------------------------------------------------------------------------
GROUND_SYSTEM_PREFIX = "You check sentences against sources."


def sentence_lines(prompt):
    """The numbered sentences of a grounding prompt: {n: text}, from the lines `N. text` after the line `SENTENCES`."""
    out = {}
    seen = False
    for line in prompt.splitlines():
        if line.strip() == "SENTENCES":
            seen = True
            continue
        if seen and ". " in line:
            head, _, rest = line.partition(". ")
            if head.isdigit():
                out[int(head)] = rest
    return out


def verdict_json(prompt, support):
    """Verdict JSON for a grounding prompt. `support` maps a substring of a sentence to (source label like 'S1', verbatim quote); other sentences are UNSUPPORTED."""
    rows = []
    for n, text in sorted(sentence_lines(prompt).items()):
        hit = next(((lab, quote) for sub, (lab, quote) in support.items() if sub in text), None)
        if hit:
            rows.append({"n": n, "verdict": "SUPPORTED", "source": hit[0], "quote": hit[1]})
        else:
            rows.append({"n": n, "verdict": "UNSUPPORTED", "source": None, "quote": None})
    return json.dumps({"verdicts": rows})


class RouterModel(object):
    """A ctx.model stand-in that answers by KIND of call: the grounding call (system starts with the grounding prefix) gets verdict JSON built from `support`;
    a call with web_search_max_uses 0 is the Opal-path answer, one above 0 the web-path answer. Every call is recorded."""

    def __init__(self, opal=None, web=None, support=None, grounding_error=None):
        self.opal, self.web, self.support, self.grounding_error = opal, web, support or {}, grounding_error
        self.calls = []

    def __call__(self, prompt, *, system=None, web_search_max_uses=0, max_tokens=1500):
        kind = "ground" if (system or "").startswith(GROUND_SYSTEM_PREFIX) else ("web" if web_search_max_uses > 0 else "opal")
        self.calls.append({"kind": kind, "prompt": prompt, "system": system, "web_search_max_uses": web_search_max_uses, "max_tokens": max_tokens})
        if kind == "ground":
            if self.grounding_error:
                raise self.grounding_error
            return result(verdict_json(prompt, self.support))
        res = self.opal if kind == "opal" else self.web
        if res is None:
            return result("NO_INFORMATION")
        if isinstance(res, Exception):
            raise res
        return res

    def kinds(self):
        return [c["kind"] for c in self.calls]


def source_page(url, text, status="OK", title="Page", http=200):
    """A fetch_source-shaped dict."""
    return {"kind": "web", "url": url, "label": None, "status": status, "http_status": http, "title": title,
            "text": text if status == "OK" else "", "chars": len(text) if status == "OK" else 0, "note": ""}


def fetcher(pages):
    """A ctx.fetch stand-in: url -> source dict from `pages` (a dict url -> source dict); an unknown url reads NOT_FOUND. Records every url asked."""
    asked = []

    def fetch(url):
        asked.append(url)
        return dict(pages.get(url) or source_page(url, "", "NOT_FOUND", None, 404))
    fetch.asked = asked
    return fetch


def ctx_f(inputs, model, fetch=None, security_key="ASML_NA_Equity", now=NOW):
    """A BlockContext carrying a fetch seam (cell gr-5 adds the argument)."""
    from lib.research.aifill.orchestrate import BlockContext

    return BlockContext(security_key, inputs, model, now, fetch=fetch)
