"""check_gs2_validation.py -- acceptance arms for AMGT-gs-2 (each block of a stored fill document carries its own validation state).

  PYTHONPATH=<repo root> python check_gs2_validation.py
Offline, stdlib only. Imports lib.research.aifill.contract and lib.research.aifill.validation (new). The ruling (CTO msg 6446, 2026-10-16, (A)): the state lives in each block, as ONE new
block key, so every reader of the stored document (the Opal gateway passes blocks through whole) sees the claim beside the text. Values: the hold state (HELD until the CVO's five-name
read clears it) and the revalidate verdict (PASS or REFUSED under the contract version named). A present key is always checked; the key is optional (no switch).
"""
from __future__ import annotations

import copy
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round106_aifill_prep", "checks"))
import aifill_check_lib as L  # noqa: E402

NOW = datetime.datetime(2026, 10, 16, 7, 0, 0, tzinfo=datetime.timezone.utc)
STAMP = "2026-10-16T07:00:00Z"


def main():
    from lib.research.aifill import contract
    try:
        from lib.research.aifill import validation
    except ImportError:  # at the base the module is absent: the arms that need it FAIL, the control arms still run
        validation = None

    arms = L.Arms("GS-2")

    def blk(block_id):
        text = "The officer list names the chief executive."
        g = {"version": "grounding/1", "checked_at": "2026-10-16T06:00:00Z",
             "sources": [{"url": None, "label": "Company officer list", "kind": "opal", "status": "OK", "http_status": None, "chars": 120}],
             "sentences": [{"text": text, "verdict": "SUPPORTED", "source": 0, "quote": "names the chief executive"}], "model_call": None}
        return contract.make_block(block_id, "OPAL_SOURCE", text, [{"source_kind": "opal", "ref": "Company officer list", "url": None, "title": None, "quote": None}], grounding=g)

    def good_doc():
        blocks = {b: blk(b) for b in contract.BLOCK_IDS[:4]}
        blocks["identity_description"] = contract.none_block("identity_description", "The identity header already has a company description.")
        return {"schema": "aifill/v1", "security_key": "ASML_NA_Equity", "as_of": "2026-10-16", "generated_at": "2026-10-16T06:00:00Z",
                "producer": {"version": contract.PRODUCER_VERSION, "model": contract.PRODUCER_MODEL}, "blocks": blocks}

    def good_validation(**over):
        v = {"version": "validation/1", "state": "HELD", "verdict": "PASS", "contract": contract.PRODUCER_VERSION, "checked_at": STAMP}
        v.update(over)
        return v

    def with_validation(v, block_id="mgmt_bio"):
        block = blk(block_id)
        block["validation"] = v
        return block

    def stamped(**kw):
        return validation.stamp_validation(good_doc(), NOW, **kw)

    def without_it_still_valid():
        d = good_doc()
        return contract.validate_document(d) == [] and contract.validate_block(blk("mgmt_bio")) == [], "a document without validation no longer validates"
    arms.run("a block and a document with no validation key still validate (the key is optional)", without_it_still_valid)

    def stamp_every_block():
        d = stamped()
        vs = [b.get("validation") for b in d["blocks"].values()]
        ok = (len(vs) == 5 and all(isinstance(v, dict) and set(v) == {"version", "state", "verdict", "contract", "checked_at"} for v in vs)
              and all(v["version"] == "validation/1" and v["state"] == "HELD" and v["verdict"] == "PASS" for v in vs)
              and all(v["contract"] == contract.PRODUCER_VERSION and v["checked_at"] == STAMP for v in vs))
        return ok, vs[0]
    arms.run("stamp_validation puts the five-key validation on every block (the NONE block too): HELD, PASS, the contract version, the stamp", stamp_every_block)

    def input_unchanged():
        doc = good_doc()
        before = json.dumps(doc, sort_keys=True)
        validation.stamp_validation(doc, NOW)
        return json.dumps(doc, sort_keys=True) == before, "the input document was changed"
    arms.run("the input document is not changed", input_unchanged)

    def stamped_is_valid():
        d = stamped()
        return contract.validate_document(d) == [], contract.validate_document(d)[:2]
    arms.run("the stamped document passes validate_document", stamped_is_valid)

    def refused_block():
        doc = good_doc()
        doc["blocks"]["mgmt_bio"]["citations"] = []
        d = validation.stamp_validation(doc, NOW)
        v = {k: b["validation"]["verdict"] for k, b in d["blocks"].items()}
        return v["mgmt_bio"] == "REFUSED" and all(x == "PASS" for k, x in v.items() if k != "mgmt_bio") and d["blocks"]["mgmt_bio"]["validation"]["state"] == "HELD", v
    arms.run("a block that breaks the contract is stamped REFUSED (and HELD); the others PASS", refused_block)

    def cleared_stamp():
        d = stamped(state="CLEARED")
        return all(b["validation"]["state"] == "CLEARED" for b in d["blocks"].values()), "CLEARED not stamped"
    arms.run("state CLEARED can be stamped on a document whose blocks all PASS", cleared_stamp)

    def cleared_needs_pass():
        doc = good_doc()
        doc["blocks"]["mgmt_bio"]["citations"] = []
        try:
            validation.stamp_validation(doc, NOW, state="CLEARED")
        except contract.ContractError as err:
            return "validation" in str(err), str(err)[:120]
        return False, "no error"
    arms.run("CLEARED over a block that is REFUSED raises ContractError naming validation", cleared_needs_pass)

    arms.raises("an unknown state raises ContractError", "ContractError", lambda: validation.stamp_validation(good_doc(), NOW, state="WITHDRAWN"))
    arms.raises("a naive or missing time raises ContractError", "ContractError", lambda: validation.stamp_validation(good_doc(), None))

    def accepted_shapes():
        blocks = [with_validation(good_validation()), with_validation(good_validation(state="CLEARED")), with_validation(good_validation(verdict="REFUSED"))]
        probs = [contract.validate_block(b) for b in blocks]
        return probs[0] == [] and probs[1] == [] and probs[2] == [], probs
    arms.run("a block with a well-formed validation is accepted (HELD PASS, CLEARED PASS, HELD REFUSED)", accepted_shapes)

    def refused_shapes():
        cases = [good_validation(state="WITHDRAWN"), good_validation(verdict="MAYBE"), good_validation(version="validation/2"), good_validation(contract=""),
                 good_validation(contract=7), good_validation(checked_at="16 Oct 2026"), good_validation(state="CLEARED", verdict="REFUSED")]
        extra = good_validation()
        extra["note"] = "x"
        missing = good_validation()
        del missing["verdict"]
        cases += [extra, missing, "HELD", None]
        bad = []
        for i, v in enumerate(cases):
            problems = contract.validate_block(with_validation(v))
            ok = any(p.startswith("validation") for p in problems)
            if not ok:
                bad.append((i, problems[:2]))
        return not bad, bad
    arms.run("every malformed validation is a problem that starts with the word validation; CLEARED over REFUSED is one of them", refused_shapes)

    def key_rule():
        both = blk("mgmt_bio")
        both["validation"] = good_validation()
        only_v = {k: v for k, v in both.items() if k != "grounding"}
        neither = {k: v for k, v in both.items() if k not in ("grounding", "validation")}
        unknown = dict(both)
        unknown["extra"] = 1
        r = {"both": contract.validate_block(both), "grounding_only": contract.validate_block(blk("mgmt_bio")), "unknown": contract.validate_block(unknown)}
        only_v_problems = contract.validate_block(only_v)
        neither_problems = contract.validate_block(neither)
        return (r["both"] == [] and r["grounding_only"] == [] and r["unknown"] != [] and any("grounding" in p for p in only_v_problems) and any("grounding" in p for p in neither_problems)), {k: v[:1] for k, v in r.items()}
    arms.run("the key rule: eight, plus grounding, plus validation; an unknown key is refused; the missing-grounding rule still holds without validation", key_rule)

    def none_block_carries_it():
        b = contract.none_block("identity_description", "The identity header already has a company description.")
        b["validation"] = good_validation()
        return contract.validate_block(b) == [], contract.validate_block(b)
    arms.run("a NONE block may carry a validation", none_block_carries_it)

    def round_trip():
        d = stamped()
        back = json.loads(json.dumps(d))
        return back == d and contract.validate_document(back) == [], "round trip differs"
    arms.run("the stamped document round-trips through JSON and still validates", round_trip)

    def ascii_only():
        bs = [open(m.__file__, "rb").read() for m in (contract, validation)]  # validation None at the base: AttributeError, a FAIL
        return all(b.isascii() for b in bs) and all(x not in b for b in bs for x in (b"import anthropic", b"import boto3", b"import urllib")), "non-ASCII or a forbidden import"
    arms.run("contract.py and validation.py stay ASCII with no network import", ascii_only)

    def deep_copy_check():
        doc = good_doc()
        d = validation.stamp_validation(doc, NOW)
        d["blocks"]["mgmt_bio"]["text"] = "changed"
        return doc["blocks"]["mgmt_bio"]["text"] != "changed", "the stamped copy shares structure with the input"
    arms.run("the stamped document does not share structure with the input", deep_copy_check)

    _ = copy
    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
