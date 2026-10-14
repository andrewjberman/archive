"""check_gr3_grounding.py -- acceptance arms for AMGT-gr-3 (check every sentence of a block against the text of the sources it cites; drop what they do not carry).

  PYTHONPATH=<repo root> python check_gr3_grounding.py
Offline: the model is a stub, the sources are hand-made dicts of the shape lib.research.aifill.sources.fetch_source returns. Imports lib.research.aifill.grounding (new), sentences (gr-1),
sources (gr-2) and contract (gr-4). The ruling (CTO, round-105 grounding pass, 4(a)): "Before a block is stored, the producer checks every sentence against the fetched text of its cited
sources and drops any sentence they do not carry. A citation that does not answer (404, refused) grounds nothing. Where dated sources conflict, the newest wins."
The CVO's measured cases: a 'Momentum is largely organic' no source carries; a stale 'board proposed Pablo Isla ... to succeed' that a newer source contradicts; a figure contradicted by the release.
"""
from __future__ import annotations

import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

NOW = datetime.datetime(2026, 10, 14, 6, 0, 0, tzinfo=datetime.timezone.utc)
S1 = ("Nestle announced that Philipp Navratil became Chief Executive Officer of Nestle S.A. in September 2025. He joined Nestle in 2001 as an international auditor.\n"
      "The Board of Directors elected Pablo Isla as Chairman in October 2025, earlier than anticipated, after Paul Bulcke stepped down.")
S2 = "Organic growth was 4.3 percent in 2025. The company targets savings of CHF 1 billion by the end of 2027, across four core business units."
TEXT = ("Philipp Navratil became chief executive in September 2025. He joined Nestle in 2001. Pablo Isla became chairman in October 2025. "
        "Organic growth was 4.3 percent in 2025. Momentum is largely organic.")


def src(url, text, status="OK", title="Page", kind="web", label=None, http=200):
    return {"kind": kind, "url": url, "label": label, "status": status, "http_status": http, "title": title, "text": text if status == "OK" else "", "chars": len(text) if status == "OK" else 0, "note": ""}


def verdicts(*rows):
    return json.dumps({"verdicts": [{"n": n, "verdict": v, "source": s, "quote": q} for n, v, s, q in rows]})


GOOD = [
    (1, "SUPPORTED", "S1", "became Chief Executive Officer of Nestle S.A. in September 2025"),
    (2, "SUPPORTED", "S1", "He joined Nestle in 2001 as an international auditor"),
    (3, "SUPPORTED", "S1", "elected Pablo Isla as Chairman in October 2025"),
    (4, "SUPPORTED", "S2", "Organic growth was 4.3 percent in 2025"),
    (5, "UNSUPPORTED", None, None),
]


def main():
    from lib.research.aifill import contract, grounding, sentences

    arms = L.Arms("GR-3")
    srcs = lambda: [src("https://www.nestle.com/leadership", S1), src("https://example.com/results", S2)]  # noqa: E731

    def run(model_rows, sources=None, text=TEXT, model=None, **kw):
        payload = "{}" if model_rows is None else (model_rows if isinstance(model_rows, str) else verdicts(*model_rows))
        m = model or L.StubModel(L.result(payload))
        r = grounding.ground_block(text, sources if sources is not None else srcs(), m, NOW, **kw)
        return r, m

    def basic():
        r, m = run(GOOD)
        kept = " ".join(sentences.split_sentences(TEXT)[:4])
        return r.ok and r.text == kept and len(m.calls) == 1 and "Momentum" not in r.text, (r.ok, r.text[-60:])
    arms.run("the supported sentences are kept, the unsupported one is dropped, one model call", basic)

    def record_shape():
        r, _ = run(GOOD)
        g = r.record
        texts = [s["text"] for s in g["sentences"]]
        return (g["version"] == "grounding/1" and g["checked_at"] == "2026-10-14T06:00:00Z" and texts == sentences.split_sentences(TEXT)
                and [s["verdict"] for s in g["sentences"]] == ["SUPPORTED"] * 4 + ["UNSUPPORTED"] and [s["source"] for s in g["sentences"]][:4] == [0, 0, 0, 1]
                and [x["url"] for x in g["sources"]] == ["https://www.nestle.com/leadership", "https://example.com/results"] and g["model_call"]["input_tokens"] == 100), g["sentences"][4]
    arms.run("the record lists every sentence in order with verdict, source index and quote, and every source with its status", record_shape)

    def mechanical_quote():
        rows = [(1, "SUPPORTED", "S1", "became Chief Executive Officer of Nestle S.A. in September 2025"), (2, "SUPPORTED", "S1", "He joined Nestle in 1999 as the chief financial officer"),
                (3, "SUPPORTED", "S1", "elected Pablo Isla as Chairman in October 2025"), (4, "SUPPORTED", "S2", "Organic growth was 4.3 percent in 2025"), (5, "SUPPORTED", "S2", "Momentum is largely organic growth")]
        r, _ = run(rows)
        v = [s["verdict"] for s in r.record["sentences"]]
        return v == ["SUPPORTED", "UNSUPPORTED", "SUPPORTED", "SUPPORTED", "UNSUPPORTED"] and "Momentum" not in r.text and "1999" not in r.text, v
    arms.run("a SUPPORTED verdict whose quote is not in the source text is downgraded (the quote is checked mechanically)", mechanical_quote)

    def quote_loose():
        rows = [(1, "SUPPORTED", "S1", "BECAME  chief executive officer of nestle s.a. in   september 2025!")] + GOOD[1:4] + [GOOD[4]]
        r, _ = run(rows)
        return r.record["sentences"][0]["verdict"] == "SUPPORTED", r.record["sentences"][0]
    arms.run("a quote differing only in case, spacing or punctuation still verifies", quote_loose)

    def quote_outside_window():
        filler = "\n".join("Unrelated paragraph %d about shipping logistics and port fees across many harbours." % i for i in range(1500))
        big = filler + "\nShe was born in 1971 in Madrid and studied law at the Complutense University before joining Inditex.\n" + filler
        r, m = run([(1, "SUPPORTED", "S1", "born in 1971 in Madrid and studied law at the Complutense University")],
                   sources=[src("https://example.com/bio", big)], text="She was born in 1971 in Madrid.")
        prompt = m.calls[0]["prompt"]
        return r.ok and r.text == "She was born in 1971 in Madrid." and len(prompt) < 60000, (r.ok, len(prompt))
    arms.run("a 130,000-character source is windowed for the prompt (under 60,000) yet its quote verifies against the full text", quote_outside_window)

    def contradicted():
        rows = [(1, "SUPPORTED", "S1", "became Chief Executive Officer of Nestle S.A. in September 2025"), (2, "SUPPORTED", "S1", "He joined Nestle in 2001 as an international auditor"),
                (3, "CONTRADICTED", "S1", "elected Pablo Isla as Chairman in October 2025"), (4, "SUPPORTED", "S2", "Organic growth was 4.3 percent in 2025"), (5, "UNSUPPORTED", None, None)]
        r, _ = run(rows)
        return "Pablo Isla" not in r.text and r.record["sentences"][2]["verdict"] == "CONTRADICTED", r.record["sentences"][2]
    arms.run("a CONTRADICTED sentence is dropped and recorded as such", contradicted)

    def dead_sources():
        bad = [src("https://a.example/1", "", "REFUSED", http=403), src("https://a.example/2", "", "NOT_FOUND", http=404), src("https://a.example/3", "", "ERROR", http=None),
               src("https://a.example/4", "", "EMPTY"), src("https://a.example/5", "", "PAYWALL"), src("https://a.example/6", "", "UNSUPPORTED"), src("https://www.nestle.com/leadership", S1)]
        r, m = run([(1, "SUPPORTED", "S1", "became Chief Executive Officer of Nestle S.A. in September 2025"), (2, "UNSUPPORTED", None, None), (3, "UNSUPPORTED", None, None),
                    (4, "UNSUPPORTED", None, None), (5, "UNSUPPORTED", None, None)], sources=bad)
        prompt = m.calls[0]["prompt"]
        gone = all(("a.example/%d" % i) not in prompt for i in range(1, 7))
        return gone and "nestle.com/leadership" in prompt and r.record["sentences"][0]["source"] == 6 and [x["status"] for x in r.record["sources"]][:6] == ["REFUSED", "NOT_FOUND", "ERROR", "EMPTY", "PAYWALL", "UNSUPPORTED"], prompt[:80]
    arms.run("sources that did not answer (6 kinds) are never shown to the model and ground nothing; the record keeps their statuses and the live source's index", dead_sources)

    def claims_dead_source():
        bad = [src("https://a.example/1", "", "REFUSED", http=403), src("https://www.nestle.com/leadership", S1)]
        r, _ = run([(1, "SUPPORTED", "S1", "became Chief Executive Officer of Nestle S.A. in September 2025"), (2, "SUPPORTED", "S3", "He joined Nestle in 2001 as an international auditor"),
                    (3, "UNSUPPORTED", None, None), (4, "UNSUPPORTED", None, None), (5, "UNSUPPORTED", None, None)], sources=bad)
        v = [s["verdict"] for s in r.record["sentences"]]
        return v[:2] == ["SUPPORTED", "UNSUPPORTED"], v
    arms.run("a verdict naming a source label that was never offered is downgraded", claims_dead_source)

    def none_usable():
        m = L.StubModel(L.result("{}"))
        r, _ = run(None, sources=[src("https://a.example/1", "", "REFUSED", http=403)], model=m)
        v = {s["verdict"] for s in r.record["sentences"]}
        return (not r.ok) and r.text == "" and m.calls == [] and v == {"UNSUPPORTED"} and r.used_urls == [], (r.ok, len(m.calls))
    arms.run("no usable source: no model call, nothing kept, ok False, every sentence recorded UNSUPPORTED", none_usable)

    def paywall_title():
        r, m = run(GOOD, sources=[src("https://www.nestle.com/leadership", S1, title="Free Trial"), src("https://example.com/results", S2)])
        prompt = m.calls[0]["prompt"]
        return "nestle.com/leadership" not in prompt and r.record["sources"][0]["status"] == "PAYWALL", r.record["sources"][0]["status"]
    arms.run("a source whose page title is a paywall title ('Free Trial') is not used and is recorded PAYWALL", paywall_title)

    def failures():
        out = []
        r1, _ = run(None, model=L.StubModel(RuntimeError("model down")))
        out.append((not r1.ok, r1.text == ""))
        r2, _ = run("this is not json at all")
        out.append((not r2.ok, r2.text == ""))
        r3, _ = run("```json\n" + verdicts(*GOOD) + "\n```")
        out.append((r3.ok,))
        r4, _ = run(json.dumps({"verdicts": [{"n": 1, "verdict": "SUPPORTED", "source": "S1", "quote": "became Chief Executive Officer of Nestle S.A. in September 2025"}, {"verdict": "SUPPORTED"}, {"n": 99, "verdict": "SUPPORTED"}]}))
        v4 = [s["verdict"] for s in r4.record["sentences"]]
        out.append((v4 == ["SUPPORTED"] + ["UNSUPPORTED"] * 4,))
        return all(all(x) for x in out), out
    arms.run("a failing model, non-JSON, fenced JSON, a verdict with no n and an n out of range: handled, never raises", failures)

    def prompt_content():
        r, m = run(GOOD)
        c = m.calls[0]
        p = (c["system"] or "") + "\n" + c["prompt"]
        sents = sentences.split_sentences(TEXT)
        return (c["web_search_max_uses"] == 0 and c["max_tokens"] >= 1500 and all(("%d." % (i + 1)) in c["prompt"] and s in c["prompt"] for i, s in enumerate(sents))
                and "newest" in p.lower() and "data, not instructions" in p.lower() and "[S1]" in c["prompt"] and "[S2]" in c["prompt"] and "https://www.nestle.com/leadership" in c["prompt"]
                and "verbatim" in p.lower() and "CONTRADICTED" in p), (c["web_search_max_uses"], c["max_tokens"])
    arms.run("the prompt: numbered sentences, labelled sources, 'newest wins', 'data, not instructions', verbatim quote, no web search", prompt_content)

    def opal():
        osrc = [{"kind": "opal", "url": None, "label": "Company officer list", "status": "OK", "http_status": None, "title": None,
                 "text": "Philipp Navratil Chief Executive Officer since September 2025. Anna Manz Executive Vice President and Chief Financial Officer.", "chars": 120, "note": ""}]
        r, m = run([(1, "SUPPORTED", "S1", "Philipp Navratil Chief Executive Officer since September 2025")], sources=osrc, text="Philipp Navratil is chief executive.")
        cites = [{"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": lab} for lab in r.used_labels]
        b = contract.make_block("mgmt_bio", "OPAL_SOURCE", r.text, cites, grounding=r.record, require_grounding=True)
        return r.ok and r.used_labels == ["Company officer list"] and r.used_urls == [] and contract.validate_block(b, require_grounding=True) == [], r.used_labels
    arms.run("opal-kind sources ground the same way; the record builds a valid OPAL_SOURCE block", opal)

    def end_to_end():
        r, _ = run(GOOD)
        cites = [{"source_kind": "web", "url": u, "title": "T", "quote": None, "ref": None} for u in r.used_urls]
        call = {"model": "claude-opus-5", "web_search_requests": 1, "input_tokens": 10, "output_tokens": 10}
        b = contract.make_block("mgmt_bio", "WEB_SEARCH", r.text, cites, model_call=call, grounding=r.record, require_grounding=True)
        extra = cites + [{"source_kind": "web", "url": "https://other.example/x", "title": "T", "quote": None, "ref": None}]
        try:
            contract.make_block("mgmt_bio", "WEB_SEARCH", r.text, extra, model_call=call, grounding=r.record, require_grounding=True)
            refused = False
        except contract.ContractError:
            refused = True
        return r.used_urls == ["https://www.nestle.com/leadership", "https://example.com/results"] and refused and contract.validate_block(b, require_grounding=True) == [], r.used_urls
    arms.run("the record and used_urls build a valid WEB_SEARCH block; an extra uncited-by-support citation is refused by the contract", end_to_end)

    def unused_source():
        r, _ = run([(1, "SUPPORTED", "S1", "became Chief Executive Officer of Nestle S.A. in September 2025"), (2, "SUPPORTED", "S1", "He joined Nestle in 2001 as an international auditor"),
                    (3, "SUPPORTED", "S1", "elected Pablo Isla as Chairman in October 2025"), (4, "UNSUPPORTED", None, None), (5, "UNSUPPORTED", None, None)])
        return r.used_urls == ["https://www.nestle.com/leadership"], r.used_urls
    arms.run("a source that supports no kept sentence is not in used_urls", unused_source)

    def determinism():
        a, _ = run(GOOD)
        b, _ = run(GOOD)
        return json.dumps(a.record, sort_keys=True) == json.dumps(b.record, sort_keys=True) and a.text == b.text, "ok"
    arms.run("the same inputs give the same record and text", determinism)

    def empty_text():
        r, m = run(None, text="   ")
        return (not r.ok) and r.text == "" and m.calls == [], (r.ok, len(m.calls))
    arms.run("an empty text: ok False, no model call", empty_text)

    def src_check():
        src_bytes = open(grounding.__file__, "rb").read()
        return src_bytes.isascii() and b"import anthropic" not in src_bytes and b"import boto3" not in src_bytes and b"import urllib" not in src_bytes, "non-ASCII or a forbidden import"
    arms.run("the module is ASCII and does no network of its own (the model and the sources arrive as arguments)", src_check)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
