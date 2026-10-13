"""check_fa1_contract.py -- acceptance arms for AMGT-fa-1 (the fill document contract and the orchestrator).

  PYTHONPATH=<repo root> python check_fa1_contract.py
Imports lib.research.aifill.contract and lib.research.aifill.orchestrate. At the base (before the cell) it exits 1 on the import.
"""
from __future__ import annotations

import datetime
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

WEB_CITE = {"source_kind": "web", "url": "https://a.example/x", "title": "T", "quote": None, "ref": None}
OPAL_CITE = {"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}
MODEL_CALL = {"model": "m", "web_search_requests": 1, "input_tokens": 1, "output_tokens": 1}


def main():
    from lib.research.aifill import contract, orchestrate

    arms = L.Arms("FA-1")
    ids = L.BLOCK_IDS

    arms.run("block ids and constants", lambda: contract.BLOCK_IDS == ids and contract.SCHEMA == "aifill/v1"
             and contract.SOURCE_CLASSES == ("OPAL_SOURCE", "WEB_SEARCH", "NONE") and isinstance(contract.PRODUCER_VERSION, str))

    def none_ok():
        block = contract.none_block("mgmt_bio", "No source holds this.")
        return contract.validate_block(block) == [] and block["source_class"] == "NONE" and block["text"] is None \
            and block["machine_written"] is True and block["citations"] == []
    arms.run("none_block is valid", none_ok)

    def fold_ok():
        raw = "He said “hello” – and left… **bold** costs €5 ‘x’"
        out = contract.fold_text(raw)
        return out.isascii() and "**" not in out and "hello" in out and "EUR" in out, repr(out)
    arms.run("fold_text makes plain ASCII", fold_ok)

    def web_ok():
        block = contract.make_block("mgmt_bio", "WEB_SEARCH", "He led “X”.", [WEB_CITE], model_call=MODEL_CALL)
        return contract.validate_block(block) == [] and block["text"].isascii() and block["source_class"] == "WEB_SEARCH" \
            and block["reason"] is None and block["machine_written"] is True
    arms.run("make_block WEB_SEARCH happy path (folds text)", web_ok)

    def opal_ok():
        block = contract.make_block("mgmt_recent", "OPAL_SOURCE", "A headline.", [OPAL_CITE], opal_inputs=["thesis.management.officers"])
        return contract.validate_block(block) == [] and block["opal_inputs"] == ["thesis.management.officers"]
    arms.run("make_block OPAL_SOURCE happy path", opal_ok)

    def opal_with_url_ok():
        cite = dict(OPAL_CITE, url="https://www.bloomberg.com/news/x")
        return contract.validate_block(contract.make_block("mgmt_recent", "OPAL_SOURCE", "T.", [cite])) == []
    arms.run("OPAL_SOURCE citation may carry a link", opal_with_url_ok)

    refusals = [
        ("text without a citation", lambda: contract.make_block("mgmt_bio", "WEB_SEARCH", "T.", [], model_call=MODEL_CALL)),
        ("WEB_SEARCH with only an opal citation", lambda: contract.make_block("mgmt_bio", "WEB_SEARCH", "T.", [OPAL_CITE], model_call=MODEL_CALL)),
        ("WEB_SEARCH without a model_call", lambda: contract.make_block("mgmt_bio", "WEB_SEARCH", "T.", [WEB_CITE])),
        ("WEB_SEARCH with zero searches", lambda: contract.make_block("mgmt_bio", "WEB_SEARCH", "T.", [WEB_CITE], model_call=dict(MODEL_CALL, web_search_requests=0))),
        ("web citation with a non-http url", lambda: contract.make_block("mgmt_bio", "WEB_SEARCH", "T.", [dict(WEB_CITE, url="ftp://x/y")], model_call=MODEL_CALL)),
        ("OPAL_SOURCE with a web citation", lambda: contract.make_block("mgmt_bio", "OPAL_SOURCE", "T.", [WEB_CITE])),
        ("opal citation with a code-path ref", lambda: contract.make_block("mgmt_bio", "OPAL_SOURCE", "T.", [dict(OPAL_CITE, ref="thesis.management.officers[0]")])),
        ("opal citation ref with an underscore", lambda: contract.make_block("mgmt_bio", "OPAL_SOURCE", "T.", [dict(OPAL_CITE, ref="management_status")])),
        ("unknown block id", lambda: contract.make_block("mgmt_nope", "OPAL_SOURCE", "T.", [OPAL_CITE])),
        ("unknown source class", lambda: contract.make_block("mgmt_bio", "GUESS", "T.", [OPAL_CITE])),
        ("empty text", lambda: contract.make_block("mgmt_bio", "OPAL_SOURCE", "   ", [OPAL_CITE])),
        ("text over 1200 characters", lambda: contract.make_block("mgmt_bio", "OPAL_SOURCE", "x" * 1201, [OPAL_CITE])),
    ]
    for label, fn in refusals:
        arms.raises("make_block refuses: " + label, "ContractError", fn)

    def validate_lists_problems():
        bad = contract.none_block("mgmt_bio", "r")
        bad["machine_written"] = False
        a = contract.validate_block(bad)
        bad2 = contract.none_block("mgmt_bio", "r")
        bad2["text"] = "should not be here"
        b = contract.validate_block(bad2)
        bad3 = contract.none_block("mgmt_bio", "an_underscored_reason")
        c = contract.validate_block(bad3)
        return isinstance(a, list) and a and b and c, (a, b, c)
    arms.run("validate_block lists problems (negative controls)", validate_lists_problems)

    def full_builders(ok_text="Plain text."):
        def make(block_id):
            return lambda c: contract.make_block(block_id, "OPAL_SOURCE", ok_text, [OPAL_CITE])
        return {block_id: make(block_id) for block_id in ids}

    def doc_ok():
        doc = orchestrate.build_document("ASML_NA_Equity", {"overlay": None, "thesis": None, "errors": {}}, lambda *a, **k: None, now=L.NOW, builders=full_builders())
        return contract.validate_document(doc) == [] and doc["schema"] == "aifill/v1" and doc["security_key"] == "ASML_NA_Equity" \
            and doc["as_of"] == "2026-10-13" and doc["generated_at"] == "2026-10-13T12:00:00Z" \
            and set(doc["blocks"]) == set(ids) and doc["producer"]["version"] == contract.PRODUCER_VERSION and isinstance(doc["producer"]["model"], str)
    arms.run("build_document with five builders is a valid document", doc_ok)

    def single(builder):
        builders = full_builders()
        builders["mgmt_bio"] = builder
        doc = orchestrate.build_document("K", {}, lambda *a, **k: None, now=L.NOW, builders=builders)
        return doc, doc["blocks"]["mgmt_bio"]

    def raised():
        def boom(c):
            raise ValueError("boom")
        doc, block = single(boom)
        return contract.validate_document(doc) == [] and block["source_class"] == "NONE" and "ValueError" in block["reason"], block["reason"]
    arms.run("a raising builder becomes a NONE block naming the error", raised)

    def model_error():
        class ModelError(Exception):
            pass

        def boom(c):
            raise ModelError("overloaded")
        doc, block = single(boom)
        return contract.validate_document(doc) == [] and "model call failed" in block["reason"] and "overloaded" in block["reason"], block["reason"]
    arms.run("a ModelError becomes 'model call failed'", model_error)

    def invalid_block():
        doc, block = single(lambda c: {"block_id": "mgmt_bio"})
        return contract.validate_document(doc) == [] and block["source_class"] == "NONE" and "invalid" in block["reason"], block["reason"]
    arms.run("an invalid returned block becomes a NONE block", invalid_block)

    def wrong_id_block():
        doc, block = single(lambda c: contract.make_block("mgmt_recent", "OPAL_SOURCE", "T.", [OPAL_CITE]))
        return block["block_id"] == "mgmt_bio" and block["source_class"] == "NONE", block["reason"]
    arms.run("a block returned under the wrong id is refused", wrong_id_block)

    def ctx_ok():
        seen = {}
        inputs = {"overlay": {"a": 1}, "thesis": None, "errors": {}}
        sentinel = lambda *a, **k: None  # noqa: E731

        def probe(c):
            seen["key"], seen["inputs"], seen["model"], seen["now"] = c.security_key, c.inputs, c.model, c.now
            return contract.none_block("mgmt_bio", "Probe.")
        builders = full_builders()
        builders["mgmt_bio"] = probe
        orchestrate.build_document("K1", inputs, sentinel, now=L.NOW, builders=builders)
        return seen["key"] == "K1" and seen["inputs"] is inputs and seen["model"] is sentinel and seen["now"] == L.NOW and seen["now"].tzinfo is not None
    arms.run("the builder context carries key, inputs, model, now", ctx_ok)

    def default_now():
        doc = orchestrate.build_document("K", {}, lambda *a, **k: None, builders=full_builders())
        stamp = datetime.datetime.strptime(doc["generated_at"], "%Y-%m-%dT%H:%M:%SZ")
        return abs((datetime.datetime.utcnow() - stamp).total_seconds()) < 300 and doc["as_of"] == doc["generated_at"][:10]
    arms.run("now defaults to the current UTC time", default_now)

    def not_landed():
        real = importlib.import_module

        def fake(name, *args, **kwargs):
            if name.startswith("lib.research.aifill.block_"):
                raise ModuleNotFoundError("No module named %r" % name, name=name)
            return real(name, *args, **kwargs)
        importlib.import_module = fake
        try:
            doc = orchestrate.build_document("K", {}, lambda *a, **k: None, now=L.NOW)
        finally:
            importlib.import_module = real
        reasons = [doc["blocks"][i]["reason"] for i in ids]
        return contract.validate_document(doc) == [] and all(doc["blocks"][i]["source_class"] == "NONE" for i in ids) \
            and all("not built yet" in r for r in reasons), reasons[:1]
    arms.run("default discovery: five missing modules -> five 'not built yet'", not_landed)

    def inner_missing():
        real = importlib.import_module

        def fake(name, *args, **kwargs):
            if name == "lib.research.aifill.block_mgmt_bio":
                raise ModuleNotFoundError("No module named 'somethingelse'", name="somethingelse")
            if name.startswith("lib.research.aifill.block_"):
                raise ModuleNotFoundError("No module named %r" % name, name=name)
            return real(name, *args, **kwargs)
        importlib.import_module = fake
        try:
            doc = orchestrate.build_document("K", {}, lambda *a, **k: None, now=L.NOW)
        finally:
            importlib.import_module = real
        reason = doc["blocks"]["mgmt_bio"]["reason"]
        return "ModuleNotFoundError" in reason and "not built yet" not in reason, reason
    arms.run("a builder module with a missing dependency is NOT 'not built yet'", inner_missing)

    def discovery_uses_build_block():
        real = importlib.import_module
        calls = []

        def fake(name, *args, **kwargs):
            if name == "lib.research.aifill.block_thesis_pillars":
                calls.append(name)
                import types as _t
                mod = _t.ModuleType(name)
                mod.build_block = lambda c: contract.make_block("thesis_pillars", "OPAL_SOURCE", "Pillar text.", [OPAL_CITE])
                return mod
            if name.startswith("lib.research.aifill.block_"):
                raise ModuleNotFoundError("x", name=name)
            return real(name, *args, **kwargs)
        importlib.import_module = fake
        try:
            doc = orchestrate.build_document("K", {}, lambda *a, **k: None, now=L.NOW)
        finally:
            importlib.import_module = real
        return calls and doc["blocks"]["thesis_pillars"]["source_class"] == "OPAL_SOURCE" and doc["blocks"]["thesis_pillars"]["text"] == "Pillar text."
    arms.run("default discovery calls lib.research.aifill.block_<id>.build_block", discovery_uses_build_block)

    def validate_document_refusals():
        good = orchestrate.build_document("K", {}, lambda *a, **k: None, now=L.NOW, builders=full_builders())
        problems = []

        def mutate(label, fn):
            import copy
            d = copy.deepcopy(good)
            fn(d)
            problems.append((label, contract.validate_document(d)))
        mutate("missing block", lambda d: d["blocks"].pop("mgmt_recent"))
        mutate("extra block", lambda d: d["blocks"].update({"extra": d["blocks"]["mgmt_bio"]}))
        mutate("schema", lambda d: d.update({"schema": "aifill/v0"}))
        mutate("as_of", lambda d: d.update({"as_of": "13-10-2026"}))
        mutate("empty key", lambda d: d.update({"security_key": ""}))
        mutate("non-ascii text", lambda d: d["blocks"]["mgmt_bio"].update({"text": "café"}))
        mutate("block id mismatch", lambda d: d["blocks"]["mgmt_bio"].update({"block_id": "mgmt_recent"}))
        bad = [label for label, p in problems if not p]
        return not bad, "accepted: %s" % bad
    arms.run("validate_document refuses each broken document", validate_document_refusals)

    def no_network_imports():
        for name in ("anthropic", "boto3", "requests"):
            if name in sys.modules and getattr(sys.modules[name], "__file__", None) and name in ("anthropic",):
                return False, name + " imported"
        return True
    arms.run("importing the cell did not import the anthropic SDK", no_network_imports)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
