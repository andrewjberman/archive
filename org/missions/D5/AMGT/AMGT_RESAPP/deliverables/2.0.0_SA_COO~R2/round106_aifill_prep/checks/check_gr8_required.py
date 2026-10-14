"""check_gr8_required.py -- acceptance arms for AMGT-gr-8 (the contract REQUIRES the grounding record; the whole producer works under it).

  PYTHONPATH=<repo root> python check_gr8_required.py
Offline: real builders, orchestrator, grounding and contract with a router model and a stub fetch. Needs cells gr-1 to gr-6 merged. The CTO's 4(a): "The contract refuses a block whose grounding
record is missing." Until this cell the requirement was a switch left off so the earlier tests kept passing; this cell turns it on and brings the earlier tests onto a shared helper.
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

U1, U2 = "https://www.nestle.com/leadership", "https://example.com/results"
S1 = ("Nestle announced that Philipp Navratil became Chief Executive Officer of Nestle S.A. in September 2025. He joined Nestle in 2001 as an international auditor.")
TEXT = "Philipp Navratil became chief executive in September 2025. He joined Nestle in 2001."
SUPPORT = {"became chief executive": ("S1", "became Chief Executive Officer of Nestle S.A. in September 2025"), "joined Nestle": ("S1", "He joined Nestle in 2001 as an international auditor")}


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


def old_doc(contract):
    """A stored round-105 style document: filled blocks with no grounding key."""
    blocks = {i: contract.none_block(i, "Reason.") for i in contract.BLOCK_IDS}
    blocks["mgmt_bio"] = {"block_id": "mgmt_bio", "source_class": "WEB_SEARCH", "machine_written": True, "text": TEXT, "reason": None,
                          "citations": [{"source_kind": "web", "url": U1, "title": "T", "quote": None, "ref": None}], "opal_inputs": [],
                          "model_call": {"model": "claude-opus-5", "web_search_requests": 1, "input_tokens": 1, "output_tokens": 1}}
    return {"schema": contract.SCHEMA, "security_key": "K_US_Equity", "as_of": "2026-10-14", "generated_at": "2026-10-14T03:00:00Z",
            "producer": {"version": "opal-aifill/1.0.0", "model": contract.PRODUCER_MODEL}, "blocks": blocks}


def main():
    from lib.research.aifill import contract, orchestrate, revalidate, store

    arms = L.Arms("GR-8")
    arms.run("contract.GROUNDING_REQUIRED is True", lambda: (contract.GROUNDING_REQUIRED is True, contract.GROUNDING_REQUIRED))

    def default_refuses():
        doc = old_doc(contract)
        p = contract.validate_document(doc)
        q = contract.validate_block(doc["blocks"]["mgmt_bio"])
        return any("mgmt_bio" in x and "grounding" in x for x in p) and any("grounding" in x for x in q), p[:1]
    arms.run("a filled block with no grounding record is refused by default (block and document level)", default_refuses)

    def make_refuses():
        try:
            contract.make_block("mgmt_bio", "WEB_SEARCH", TEXT, [{"source_kind": "web", "url": U1, "title": "T", "quote": None, "ref": None}],
                                model_call={"model": "claude-opus-5", "web_search_requests": 1, "input_tokens": 1, "output_tokens": 1})
        except contract.ContractError as err:
            return "grounding" in str(err), str(err)[:90]
        return False, "accepted"
    arms.run("make_block with no record raises ContractError naming grounding", make_refuses)

    def end_to_end():
        model = L.RouterModel(web=L.result(TEXT, citations=[L.web_cite(U1, "Nestle leadership"), L.web_cite(U2, "Results")], web_search_requests=1), support=SUPPORT)
        fetch = L.fetcher({U1: L.source_page(U1, S1), U2: L.source_page(U2, "Organic growth was 4.3 percent in 2025. " * 8)})
        doc = orchestrate.build_document("ASML_NA_Equity", sparse(), model, L.NOW, fetch=fetch)
        classes = {i: doc["blocks"][i]["source_class"] for i in contract.BLOCK_IDS}
        filled = [i for i, c in classes.items() if c == "WEB_SEARCH"]
        ok = len(filled) == 5 and all(doc["blocks"][i]["grounding"]["version"] == "grounding/1" for i in filled) and contract.validate_document(doc) == []
        ok = ok and all([c["url"] for c in doc["blocks"][i]["citations"]] == [U1] for i in filled)
        return ok, classes
    arms.run("the real builders, orchestrator and grounding produce five grounded WEB_SEARCH blocks and a document valid under the requirement", end_to_end)

    def end_to_end_none():
        model = L.RouterModel(web=L.result(TEXT, citations=[L.web_cite(U1, "Nestle leadership")], web_search_requests=1), support={})
        fetch = L.fetcher({U1: L.source_page(U1, S1)})
        doc = orchestrate.build_document("ASML_NA_Equity", sparse(), model, L.NOW, fetch=fetch)
        return all(b["source_class"] == "NONE" for b in doc["blocks"].values()) and contract.validate_document(doc) == [], {i: b["source_class"] for i, b in doc["blocks"].items()}
    arms.run("when no sentence can be confirmed the document is five NONE blocks, and still valid", end_to_end_none)

    def revalidate_old():
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            rc = revalidate.main(["--names", "K_US_Equity"], reader=lambda key: old_doc(contract))
        finally:
            sys.stdout = real
        out = buf.getvalue()
        return rc == 1 and "REFUSED K_US_Equity" in out and "grounding" in out and "refused 1" in out, out[-200:]
    arms.run("revalidate refuses an old stored document naming the missing grounding record", revalidate_old)

    def served_ok():
        from lib.research.api import scoped_amgt

        model = L.RouterModel(web=L.result(TEXT, citations=[L.web_cite(U1, "Nestle leadership")], web_search_requests=1), support=SUPPORT)
        fetch = L.fetcher({U1: L.source_page(U1, S1)})
        doc = orchestrate.build_document("ASML_NA_Equity", sparse(), model, L.NOW, fetch=fetch)
        ok, why = scoped_amgt._validate_ai_fill_document(doc, "ASML_NA_Equity")
        return ok, why
    arms.run("the served API's own validator accepts a grounded document (the restore will not turn it INVALID)", served_ok)

    def size_ascii():
        model = L.RouterModel(web=L.result(TEXT, citations=[L.web_cite(U1, "Nestle leadership")], web_search_requests=1), support=SUPPORT)
        fetch = L.fetcher({U1: L.source_page(U1, S1)})
        doc = orchestrate.build_document("ASML_NA_Equity", sparse(), model, L.NOW, fetch=fetch)
        data = store.document_bytes(doc)
        return data.isascii() and len(data) < 150000 and json.loads(data.decode("ascii"))["blocks"]["mgmt_bio"]["grounding"]["version"] == "grounding/1", len(data)
    arms.run("the stored bytes are ASCII, under 150,000, and carry the record", size_ascii)

    def tests_helper():
        path = os.path.join(os.getcwd(), "lib", "research", "aifill", "tests", "grounded.py")
        return os.path.isfile(path), path
    arms.run("the shared test helper lib/research/aifill/tests/grounded.py exists", tests_helper)

    def src_check():
        src = open(contract.__file__, "rb").read()
        return src.isascii(), "non-ASCII"
    arms.run("contract.py stays ASCII", src_check)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
