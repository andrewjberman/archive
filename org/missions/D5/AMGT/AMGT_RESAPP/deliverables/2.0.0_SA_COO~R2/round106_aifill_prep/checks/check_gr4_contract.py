"""check_gr4_contract.py -- acceptance arms for AMGT-gr-4 (the contract carries a grounding record per block and can refuse a block without one).

  PYTHONPATH=<repo root> python check_gr4_contract.py
Offline. Imports lib.research.aifill.contract. The ruling (CTO, round-105 grounding pass, 4(a)): "The contract refuses a block whose grounding record is missing." The CVO's read found four
blocks stating claims their cited sources do not carry; the record states, per sentence, the verdict and the verbatim quote from the source that carries it.
This cell adds the record and the refusal behind a switch (`GROUNDING_REQUIRED`, False at this cell: cell gr-8 turns it on once the builders produce records), so the earlier checks keep passing.
"""
from __future__ import annotations

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

TEXT = "Philipp Navratil became chief executive in September 2025. He joined Nestle in 2001."
WEB1 = {"source_kind": "web", "url": "https://www.nestle.com/about/leadership", "title": "Leadership", "quote": None, "ref": None}
WEB2 = {"source_kind": "web", "url": "https://example.com/second", "title": "Second source", "quote": None, "ref": None}
OPAL1 = {"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}
CALL = {"model": "claude-opus-5", "web_search_requests": 2, "input_tokens": 100, "output_tokens": 50}


def record(kind="web", sentences=None, sources=None):
    if kind == "web":
        sources = sources or [
            {"url": WEB1["url"], "label": None, "kind": "web", "status": "OK", "http_status": 200, "chars": 5100},
            {"url": WEB2["url"], "label": None, "kind": "web", "status": "OK", "http_status": 200, "chars": 800},
        ]
        sentences = sentences or [
            {"text": "Philipp Navratil became chief executive in September 2025.", "verdict": "SUPPORTED", "source": 0, "quote": "became Chief Executive Officer of Nestle S.A. in September 2025"},
            {"text": "He joined Nestle in 2001.", "verdict": "SUPPORTED", "source": 1, "quote": "joined Nestle in 2001 as an international auditor"},
        ]
    else:
        sources = sources or [{"url": None, "label": "Company officer list", "kind": "opal", "status": "OK", "http_status": None, "chars": 300}]
        sentences = sentences or [
            {"text": "Philipp Navratil became chief executive in September 2025.", "verdict": "SUPPORTED", "source": 0, "quote": "Philipp Navratil Chief Executive Officer"},
            {"text": "He joined Nestle in 2001.", "verdict": "SUPPORTED", "source": 0, "quote": "Philipp Navratil Chief Executive Officer"},
        ]
    return {"version": "grounding/1", "checked_at": "2026-10-14T06:00:00Z", "sources": sources, "sentences": sentences, "model_call": {"model": "claude-opus-5", "input_tokens": 900, "output_tokens": 120}}


def web_block(contract, **over):
    block = contract.none_block("mgmt_bio", "Reason.")
    block.update({"source_class": "WEB_SEARCH", "text": TEXT, "reason": None, "citations": [dict(WEB1), dict(WEB2)], "model_call": dict(CALL), "grounding": record("web")})
    block.update(over)
    return block


def opal_block(contract, **over):
    block = contract.none_block("mgmt_bio", "Reason.")
    block.update({"source_class": "OPAL_SOURCE", "text": TEXT, "reason": None, "citations": [dict(OPAL1)], "model_call": None, "grounding": record("opal")})
    block.update(over)
    return block


def main():
    from lib.research.aifill import contract

    arms = L.Arms("GR-4")
    v = lambda b, **kw: contract.validate_block(b, require_grounding=True, **kw)  # noqa: E731

    arms.run("PRODUCER_VERSION is opal-aifill/1.1.0", lambda: (contract.PRODUCER_VERSION == "opal-aifill/1.1.0", contract.PRODUCER_VERSION))
    arms.run("GROUNDING_REQUIRED exists and is False at this cell", lambda: (getattr(contract, "GROUNDING_REQUIRED", None) is False, getattr(contract, "GROUNDING_REQUIRED", "missing")))
    arms.run("none_block keeps its eight keys (no grounding key) and validates", lambda: ("grounding" not in contract.none_block("mgmt_bio", "Reason.") and v(contract.none_block("mgmt_bio", "Reason.")) == [], "ok"))
    arms.run("a grounded WEB_SEARCH block validates clean", lambda: (v(web_block(contract)) == [], v(web_block(contract))))
    arms.run("a grounded OPAL_SOURCE block validates clean", lambda: (v(opal_block(contract)) == [], v(opal_block(contract))))

    def missing_key():
        b = web_block(contract)
        del b["grounding"]
        p = v(b)
        return any("grounding" in x and "missing" in x for x in p), p[:1]
    arms.run("a non-NONE block without the key is refused: 'grounding record is missing'", missing_key)

    arms.run("grounding None on a non-NONE block is refused", lambda: ((lambda p: (any("grounding" in x for x in p), p[:1]))(v(web_block(contract, grounding=None)))))
    arms.run("without the flag, the switch decides (False: a missing record is allowed)", lambda: (contract.validate_block(web_block(contract, grounding=None)) == [], "ok"))

    def text_vs_kept():
        g = record("web")
        g["sentences"][1]["verdict"] = "UNSUPPORTED"
        p = v(web_block(contract, grounding=g))
        return any("grounding" in x for x in p), p[:1]
    arms.run("block text that is not exactly its SUPPORTED sentences is refused", text_vs_kept)

    def contradicted_in_text():
        g = record("web")
        g["sentences"][0]["verdict"] = "CONTRADICTED"
        p = v(web_block(contract, grounding=g))
        return any("grounding" in x for x in p), p[:1]
    arms.run("a CONTRADICTED sentence still in the text is refused", contradicted_in_text)

    def bad_source_index():
        g = record("web")
        g["sentences"][0]["source"] = 7
        p = v(web_block(contract, grounding=g))
        return any("grounding" in x for x in p), p[:1]
    arms.run("a supported sentence whose source index does not exist is refused", bad_source_index)

    def source_not_ok():
        for status in ("REFUSED", "NOT_FOUND", "ERROR", "EMPTY", "PAYWALL", "UNSUPPORTED"):
            g = record("web")
            g["sources"][0]["status"] = status
            if not any("grounding" in x for x in v(web_block(contract, grounding=g))):
                return False, status
        return True, "six statuses"
    arms.run("a sentence supported by a source that did not answer (any non-OK status) is refused", source_not_ok)

    def quote_short():
        g = record("web")
        g["sentences"][0]["quote"] = "too short"
        g2 = record("web")
        g2["sentences"][1]["quote"] = None
        return all(any("grounding" in x for x in v(web_block(contract, grounding=gg))) for gg in (g, g2)), "ok"
    arms.run("a supported sentence without a verbatim quote of 12 or more characters is refused", quote_short)

    def citation_unused():
        g = record("web")
        g["sentences"][1]["source"] = 0
        p = v(web_block(contract, grounding=g))
        return any("grounding" in x and "support" in x for x in p), p[:2]
    arms.run("a web citation that supports no sentence is refused", citation_unused)

    def supporter_uncited():
        p = v(web_block(contract, citations=[dict(WEB1)]))
        return any("grounding" in x for x in p), p[:2]
    arms.run("a supporting source that is not among the citations is refused", supporter_uncited)

    def opal_with_web_source():
        g = record("opal", sources=[{"url": WEB1["url"], "label": None, "kind": "web", "status": "OK", "http_status": 200, "chars": 10}])
        p = v(opal_block(contract, grounding=g))
        return any("grounding" in x for x in p), p[:1]
    arms.run("an OPAL_SOURCE block grounded on a web source is refused", opal_with_web_source)

    def opal_label_mismatch():
        g = record("opal")
        g["sources"][0]["label"] = "Something else"
        p = v(opal_block(contract, grounding=g))
        return any("grounding" in x for x in p), p[:1]
    arms.run("an opal citation whose ref is not a grounded source label is refused", opal_label_mismatch)

    def web_with_opal_source():
        g = record("web")
        g["sources"][0] = {"url": None, "label": "Company officer list", "kind": "opal", "status": "OK", "http_status": None, "chars": 3}
        p = v(web_block(contract, grounding=g))
        return any("grounding" in x for x in p), p[:1]
    arms.run("a WEB_SEARCH block grounded on an opal source is refused", web_with_opal_source)

    def none_with_record():
        b = contract.none_block("mgmt_bio", "Reason.")
        b["grounding"] = record("web")
        p = v(b)
        return any("grounding" in x for x in p), p[:1]
    arms.run("a NONE block carrying a grounding record is refused", none_with_record)

    def shape():
        bad = []
        for label, mutate in (("version", lambda g: g.update(version="grounding/9")), ("sources not a list", lambda g: g.update(sources={})), ("sentences empty", lambda g: g.update(sentences=[])),
                              ("not an object", None)):
            g = record("web")
            gg = "text" if mutate is None else (mutate(g) or g)
            if not any("grounding" in x for x in v(web_block(contract, grounding=gg))):
                bad.append(label)
        return not bad, bad
    arms.run("a wrong version, a malformed list, an empty sentence list or a non-object record is refused", shape)

    def make_ok():
        b = contract.make_block("mgmt_bio", "WEB_SEARCH", TEXT, [dict(WEB1), dict(WEB2)], model_call=dict(CALL), grounding=record("web"))
        return b["grounding"]["version"] == "grounding/1" and b["text"] == TEXT and v(b) == [], b.get("grounding", {}).get("version")
    arms.run("make_block accepts grounding= and stores the record", make_ok)

    def make_missing():
        try:
            contract.make_block("mgmt_bio", "WEB_SEARCH", TEXT, [dict(WEB1), dict(WEB2)], model_call=dict(CALL), grounding=None, require_grounding=True)
        except contract.ContractError as err:
            return "grounding" in str(err), str(err)[:100]
        return False, "accepted"
    arms.run("make_block(require_grounding=True) with no record raises ContractError naming grounding", make_missing)

    def make_folds():
        g = record("web")
        g["sentences"][0]["quote"] = "became Chief Executive Officer of Nestl\u00e9 S.A. in September 2025"
        b = contract.make_block("mgmt_bio", "WEB_SEARCH", TEXT, [dict(WEB1), dict(WEB2)], model_call=dict(CALL), grounding=g)
        q = b["grounding"]["sentences"][0]["quote"]
        return q.isascii() and "Nestle" in q, q
    arms.run("make_block folds the record's quotes and texts to ASCII (Nestle, not Nestl)", make_folds)

    def doc_refuses():
        blocks = {i: contract.none_block(i, "Reason.") for i in contract.BLOCK_IDS}
        doc = {"schema": contract.SCHEMA, "security_key": "K", "as_of": "2026-10-14", "generated_at": "2026-10-14T00:00:00Z",
               "producer": {"version": contract.PRODUCER_VERSION, "model": contract.PRODUCER_MODEL}, "blocks": blocks}
        clean = contract.validate_document(copy.deepcopy(doc), require_grounding=True) == []
        bad = copy.deepcopy(doc)
        b = web_block(contract, grounding=None)
        b["block_id"] = "mgmt_recent"
        bad["blocks"]["mgmt_recent"] = b
        p = contract.validate_document(bad, require_grounding=True)
        ok = copy.deepcopy(doc)
        g = web_block(contract)
        g["block_id"] = "mgmt_recent"
        ok["blocks"]["mgmt_recent"] = g
        return clean and any("mgmt_recent" in x and "grounding" in x for x in p) and contract.validate_document(ok, require_grounding=True) == [], p[:1]
    arms.run("validate_document: an all-NONE document is clean, an ungrounded block is named, a grounded one passes", doc_refuses)

    def roundtrip():
        b = json.loads(json.dumps(web_block(contract)))
        return v(b) == [], "ok"
    arms.run("a grounded block survives a JSON round trip", roundtrip)

    def src_check():
        src = open(contract.__file__, "rb").read()
        return src.isascii(), "non-ASCII source"
    arms.run("contract.py stays ASCII", src_check)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
