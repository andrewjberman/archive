"""check_gr5_orchestrate.py -- acceptance arms for AMGT-gr-5 (the orchestrator grounds every filled block before the document is built; the run command supplies the fetcher).

  PYTHONPATH=<repo root> python check_gr5_orchestrate.py
Offline: stub builders, a router model (answers by kind of call), a stub fetch. Imports lib.research.aifill.orchestrate, contract (gr-4), grounding (gr-3), sentences (gr-1), run.
The CTO's 4(a): no block is stored whose sentences were not checked against the text of the sources it cites. The step sits in ONE place (the orchestrator), after a builder returns, so all five
builders are covered and none of them is rewritten for it.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

U1, U2, U3 = "https://www.nestle.com/leadership", "https://example.com/results", "https://example.com/other"
S1 = ("Nestle announced that Philipp Navratil became Chief Executive Officer of Nestle S.A. in September 2025. He joined Nestle in 2001 as an international auditor.\n"
      "The Board of Directors elected Pablo Isla as Chairman in October 2025, earlier than anticipated, after Paul Bulcke stepped down.")
S2 = "Organic growth was 4.3 percent in 2025. The company targets savings of CHF 1 billion by the end of 2027, across four core business units."
TEXT = ("Philipp Navratil became chief executive in September 2025. He joined Nestle in 2001. Pablo Isla became chairman in October 2025. "
        "Organic growth was 4.3 percent in 2025. Momentum is largely organic.")
SUPPORT = {
    "became chief executive": ("S1", "became Chief Executive Officer of Nestle S.A. in September 2025"),
    "joined Nestle": ("S1", "He joined Nestle in 2001 as an international auditor"),
    "became chairman": ("S1", "elected Pablo Isla as Chairman in October 2025"),
    "Organic growth": ("S2", "Organic growth was 4.3 percent in 2025"),
}
CALL = {"model": "claude-opus-5", "web_search_requests": 2, "input_tokens": 100, "output_tokens": 50}
REASON = "None of the model's statements could be confirmed in a source that answered, so the text was withheld."


def web_cites(*urls):
    return [{"source_kind": "web", "url": u, "title": "Title " + u[-6:], "quote": "q", "ref": None} for u in urls]


def pages():
    return {U1: L.source_page(U1, S1), U2: L.source_page(U2, S2), U3: L.source_page(U3, "An unrelated page about shipping and logistics across many harbours and ports. " * 6)}


def stub_builder(contract, block_id, source_class, text, cites, opal_inputs=(), call=None):
    def build(ctx):
        return contract.make_block(block_id, source_class, text, cites, opal_inputs, call)
    return build


def none_builder(contract, block_id):
    return lambda ctx: contract.none_block(block_id, "Nothing here.")


def doc_with(orch, contract, builder_map, model, fetch, inputs=None, **kw):
    builders = {i: none_builder(contract, i) for i in contract.BLOCK_IDS}
    builders.update(builder_map)
    return orch.build_document("ASML_NA_Equity", inputs if inputs is not None else L.served_inputs(), model, L.NOW, builders=builders, fetch=fetch, **kw)


def main():
    from lib.research.aifill import contract, orchestrate as orch, sentences

    arms = L.Arms("GR-5")
    BIO = "mgmt_bio"

    def web_map(text=TEXT, urls=(U1, U2)):
        return {BIO: stub_builder(contract, BIO, "WEB_SEARCH", text, web_cites(*urls), (), CALL)}

    arms.run("BlockContext takes a fetch argument and defaults it to None", lambda: (L.ctx_f({}, None, fetch=len).fetch is len and orch.BlockContext("K", {}, None, L.NOW).fetch is None, "ok"))

    def passes_fetch():
        seen = []
        builders = {i: none_builder(contract, i) for i in contract.BLOCK_IDS}

        def spy(ctx):
            seen.append(ctx.fetch)
            return contract.none_block(BIO, "Nothing.")
        builders[BIO] = spy
        marker = lambda url: None  # noqa: E731
        orch.build_document("K", {}, None, L.NOW, builders=builders, fetch=marker)
        return len(seen) == 1 and callable(seen[0]), "ok"
    arms.run("build_document hands a callable fetch to every builder's context", passes_fetch)

    def basic():
        model = L.RouterModel(support=SUPPORT)
        fetch = L.fetcher(pages())
        doc = doc_with(orch, contract, web_map(), model, fetch)
        b = doc["blocks"][BIO]
        kept = " ".join(sentences.split_sentences(TEXT)[:4])
        return (b["source_class"] == "WEB_SEARCH" and b["text"] == kept and [c["url"] for c in b["citations"]] == [U1, U2] and b["grounding"]["version"] == "grounding/1"
                and model.kinds() == ["ground"] and contract.validate_document(doc, require_grounding=True) == []), (b["source_class"], b["text"][-40:], model.kinds())
    arms.run("a WEB_SEARCH block: unsupported sentence dropped, citations kept, record attached, the document is valid with grounding required", basic)

    def prune():
        model = L.RouterModel(support=SUPPORT)
        doc = doc_with(orch, contract, web_map(urls=(U1, U2, U3)), model, L.fetcher(pages()))
        urls = [c["url"] for c in doc["blocks"][BIO]["citations"]]
        return urls == [U1, U2], urls
    arms.run("a citation that supports no kept sentence is dropped from the block", prune)

    def preserved_meta():
        doc = doc_with(orch, contract, web_map(), L.RouterModel(support=SUPPORT), L.fetcher(pages()))
        b = doc["blocks"][BIO]
        return b["model_call"] == CALL and b["citations"][0]["title"] == "Title " + U1[-6:] and b["citations"][0]["quote"] == "q" and b["grounding"]["model_call"]["input_tokens"] == 100, b["model_call"]
    arms.run("the answer's model_call, citation titles and quotes are kept; the grounding call's tokens are in the record", preserved_meta)

    def all_unsupported():
        doc = doc_with(orch, contract, web_map(), L.RouterModel(support={}), L.fetcher(pages()))
        b = doc["blocks"][BIO]
        return b["source_class"] == "NONE" and b["reason"] == REASON, (b["source_class"], b.get("reason"))
    arms.run("every sentence unsupported -> a NONE block with the stated reason", all_unsupported)

    def no_fetcher():
        doc = doc_with(orch, contract, web_map(), L.RouterModel(support=SUPPORT), None)
        b = doc["blocks"][BIO]
        return b["source_class"] == "NONE" and b["reason"] == REASON, (b["source_class"], b.get("reason"))
    arms.run("no fetcher -> NONE, never an ungrounded filled block", no_fetcher)

    def dead_sources():
        bad = {U1: L.source_page(U1, "", "REFUSED", None, 403), U2: L.source_page(U2, "", "NOT_FOUND", None, 404)}
        model = L.RouterModel(support=SUPPORT)
        doc = doc_with(orch, contract, web_map(), model, L.fetcher(bad))
        b = doc["blocks"][BIO]
        return b["source_class"] == "NONE" and b["reason"] == REASON and model.calls == [], (b["source_class"], len(model.calls))
    arms.run("all cited pages refused or missing -> NONE with the stated reason, no grounding call", dead_sources)

    def cache():
        m = {BIO: stub_builder(contract, BIO, "WEB_SEARCH", TEXT, web_cites(U1, U2), (), CALL),
             "mgmt_recent": stub_builder(contract, "mgmt_recent", "WEB_SEARCH", TEXT, web_cites(U1, U2), (), CALL)}
        fetch = L.fetcher(pages())
        doc_with(orch, contract, m, L.RouterModel(support=SUPPORT), fetch)
        return sorted(fetch.asked) == sorted([U1, U2]), fetch.asked
    arms.run("a url cited by two blocks of one document is fetched once", cache)

    def cap_eight():
        urls = ["https://example.com/p%d" % i for i in range(12)]
        pg = {u: L.source_page(u, S2 + " " + "More words about nothing in particular. " * 10) for u in urls}
        fetch = L.fetcher(pg)
        doc_with(orch, contract, web_map(urls=urls), L.RouterModel(support={"Organic growth": ("S1", "Organic growth was 4.3 percent in 2025")}), fetch)
        return len(fetch.asked) == 8 and fetch.asked == urls[:8], len(fetch.asked)
    arms.run("at most eight cited pages are fetched for one block (the first eight)", cap_eight)

    def none_untouched():
        model = L.RouterModel(support=SUPPORT)
        fetch = L.fetcher(pages())
        doc = doc_with(orch, contract, {}, model, fetch)
        return model.calls == [] and fetch.asked == [] and all(b["source_class"] == "NONE" for b in doc["blocks"].values()), (len(model.calls), fetch.asked)
    arms.run("NONE blocks cost nothing: no fetch, no model call", none_untouched)

    def opal():
        inputs = L.served_inputs()
        inputs.setdefault("thesis", {}).setdefault("management", {})["officers"] = [{"name": "Christophe Fouquet", "role": "President and CEO", "role_start": 2024, "tenure_years": 2}]
        cite = [{"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}]
        text = "Christophe Fouquet is president and CEO. He has served two years. He founded the company."
        m = {BIO: stub_builder(contract, BIO, "OPAL_SOURCE", text, cite, ["thesis.management.officers"], None)}
        model = L.RouterModel(support={"is president": ("S1", "Christophe Fouquet role President and CEO"), "two years": ("S1", "tenure years 2")})
        fetch = L.fetcher(pages())
        doc = doc_with(orch, contract, m, model, fetch, inputs=inputs)
        b = doc["blocks"][BIO]
        return (b["source_class"] == "OPAL_SOURCE" and b["text"] == "Christophe Fouquet is president and CEO. He has served two years." and fetch.asked == []
                and contract.validate_document(doc, require_grounding=True) == []), (b["source_class"], b.get("text"), b.get("reason"))
    arms.run("an OPAL_SOURCE block is grounded on the served fields it lists (opal_inputs); nothing is fetched", opal)

    def opal_unresolved():
        cite = [{"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}]
        m = {BIO: stub_builder(contract, BIO, "OPAL_SOURCE", "A claim about someone.", cite, ["thesis.no.such.path"], None)}
        doc = doc_with(orch, contract, m, L.RouterModel(support=SUPPORT), L.fetcher(pages()))
        b = doc["blocks"][BIO]
        return b["source_class"] == "NONE" and b["reason"] == REASON, (b["source_class"], b.get("reason"))
    arms.run("an OPAL_SOURCE block whose listed fields are not in the inputs -> NONE with the stated reason", opal_unresolved)

    def model_down():
        doc = doc_with(orch, contract, web_map(), L.RouterModel(grounding_error=RuntimeError("model down")), L.fetcher(pages()))
        b = doc["blocks"][BIO]
        return b["source_class"] == "NONE" and b["reason"] == REASON, (b["source_class"], b.get("reason"))
    arms.run("a failing grounding call -> NONE with the stated reason; build_document does not raise", model_down)

    def version():
        doc = doc_with(orch, contract, web_map(), L.RouterModel(support=SUPPORT), L.fetcher(pages()))
        return doc["producer"]["version"] == "opal-aifill/1.1.0", doc["producer"]
    arms.run("the document's producer version is opal-aifill/1.1.0", version)

    def ground_off():
        model = L.RouterModel(support=SUPPORT)
        doc = doc_with(orch, contract, web_map(), model, L.fetcher(pages()), ground=False)
        b = doc["blocks"][BIO]
        return b["source_class"] == "WEB_SEARCH" and b["text"] == TEXT and model.calls == [] and "grounding" not in b, (b["source_class"], len(model.calls))
    arms.run("ground=False leaves a builder's block as it is (the earlier behaviour, for the earlier tests)", ground_off)

    def deterministic():
        a = doc_with(orch, contract, web_map(), L.RouterModel(support=SUPPORT), L.fetcher(pages()))
        b = doc_with(orch, contract, web_map(), L.RouterModel(support=SUPPORT), L.fetcher(pages()))
        return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), "ok"
    arms.run("the same inputs give the same document", deterministic)

    def run_passes_fetch():
        from lib.research.aifill import run as runmod

        asked = []

        def fake_fetch(url):
            asked.append(url)
            return L.source_page(url, S1)
        import inspect
        sig = inspect.signature(runmod.main)
        return "fetch" in sig.parameters and callable(runmod.default_fetch), list(sig.parameters)
    arms.run("run.main accepts a fetch argument and the module offers default_fetch", run_passes_fetch)

    def run_no_model():
        from lib.research.aifill import run as runmod

        asked = []
        rc = runmod.main(["--key", "ASML_NA_Equity", "--no-model", "--inputs-file", os.path.join(L.FIXTURES, "served_inputs_ASML_NA_Equity.json")], fetch=lambda u: asked.append(u))
        return rc == 0 and asked == [], (rc, asked)
    arms.run("run --no-model fetches nothing", run_no_model)

    def src_check():
        src = open(orch.__file__, "rb").read()
        return src.isascii() and b"import urllib" not in src and b"import boto3" not in src and b"import anthropic" not in src, "non-ASCII or a network import"
    arms.run("orchestrate.py stays ASCII and does no network of its own", src_check)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
