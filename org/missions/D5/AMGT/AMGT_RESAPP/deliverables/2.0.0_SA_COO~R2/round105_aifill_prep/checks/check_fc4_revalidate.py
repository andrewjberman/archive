"""check_fc4_revalidate.py -- acceptance arms for AMGT-fc-4 (the re-validate command: every STORED document against the CURRENT contract, counts printed, 0 refused is the gate).

  PYTHONPATH=<repo root> python check_fc4_revalidate.py
Offline: a fake reader and a fake served-inputs reader. Needs lib.research.aifill.revalidate and the NEW contract (cell fc-2) merged. The ruling (CTO round-104 analysis, item 2):
"a full re-validate of all 95 stored documents against the new contract, printing pass/refuse counts. 0 refused is the gate."
"""
from __future__ import annotations

import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

OPAL = {"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}


def doc(key, texts=None):
    from lib.research.aifill import contract

    blocks = {i: contract.none_block(i, "Reason.") for i in contract.BLOCK_IDS}
    for block_id, text in (texts or {}).items():
        blocks[block_id] = {"block_id": block_id, "source_class": "OPAL_SOURCE", "machine_written": True, "text": text, "reason": None,
                            "citations": [dict(OPAL)], "opal_inputs": [], "model_call": None}
    return {"schema": contract.SCHEMA, "security_key": key, "as_of": "2026-10-14", "generated_at": "2026-10-14T00:00:00Z",
            "producer": {"version": contract.PRODUCER_VERSION, "model": contract.PRODUCER_MODEL}, "blocks": blocks}


def run(revalidate, argv, docs, inputs=None):
    reads = []

    def reader(key):
        reads.append(key)
        return docs.get(key)

    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        rc = revalidate.main(argv, reader=reader, inputs_reader=inputs)
    finally:
        sys.stdout = real
    return rc, buf.getvalue(), reads


def main():
    from lib.research.aifill import revalidate

    arms = L.Arms("FC-4")
    good = {"A_US_Equity": doc("A_US_Equity", {"mgmt_bio": "A chief executive since 2020."}), "B_US_Equity": doc("B_US_Equity", {"mgmt_recent": "B named a new chair."}),
            "C_US_Equity": doc("C_US_Equity")}

    def all_good():
        rc, out, reads = run(revalidate, ["--names", "A_US_Equity,B_US_Equity,C_US_Equity"], good)
        return rc == 0 and "AIFILL REVALIDATE: checked 3, passed 3, refused 0, missing 0" in out and sorted(reads) == sorted(good), out[-160:]
    arms.run("three good documents: checked 3, passed 3, refused 0, missing 0, exit 0", all_good)

    def narrated():
        docs = dict(good)
        docs["D_US_Equity"] = doc("D_US_Equity", {"mgmt_bio": "I'll research this now.MUFG named a new president."})
        rc, out, _ = run(revalidate, ["--names", "A_US_Equity,D_US_Equity"], docs)
        return rc == 1 and "REFUSED D_US_Equity" in out and "narration" in out.lower() and "checked 2, passed 1, refused 1, missing 0" in out, out[-220:]
    arms.run("a narrated stored document is REFUSED by name, with the reason, exit 1", narrated)

    def missing():
        rc, out, _ = run(revalidate, ["--names", "A_US_Equity,Z_US_Equity"], good)
        return rc == 1 and "MISSING Z_US_Equity" in out and "checked 2, passed 1, refused 0, missing 1" in out, out[-160:]
    arms.run("a name with no stored document is MISSING, exit 1", missing)

    def mangled_with_inputs():
        docs = {"NESN_SW_Equity": doc("NESN_SW_Equity", {"mgmt_bio": "Nestl SA named a new chairman."}), "OK_US_Equity": doc("OK_US_Equity", {"mgmt_bio": "Nestle SA named a chairman."})}

        def inputs(key, **kw):
            return {"overlay": {"display_name": "Nestlé SA", "name": "Nestlé SA"}, "thesis": {"management": {"officers": [{"name": "Mark Schneider"}]}}, "errors": {}}
        rc, out, _ = run(revalidate, ["--names", "NESN_SW_Equity,OK_US_Equity", "--with-inputs", "--function", "stub-fn"], docs, inputs)
        return rc == 1 and "REFUSED NESN_SW_Equity" in out and "REFUSED OK_US_Equity" not in out and "refused 1" in out and "name-checked 2" in out, out[-260:]
    arms.run("--with-inputs: 'Nestl' for 'Nestl\\u00e9 SA' is REFUSED; 'Nestle' passes", mangled_with_inputs)

    def inputs_unreadable():
        docs = {"A_US_Equity": good["A_US_Equity"]}
        rc, out, _ = run(revalidate, ["--names", "A_US_Equity", "--with-inputs", "--function", "stub-fn"], docs, lambda key, **kw: {"overlay": None, "thesis": None, "errors": {"overlay": "status 500"}})
        return rc == 0 and "name-checked 0" in out and "passed 1" in out, out[-160:]
    arms.run("--with-inputs: unreadable served inputs leave the name unchecked (counted), not refused", inputs_unreadable)

    def json_out():
        docs = dict(good)
        docs["D_US_Equity"] = doc("D_US_Equity", {"mgmt_bio": "I will search for this. It grew."})
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.json")
            run(revalidate, ["--names", "A_US_Equity,D_US_Equity,Q_US_Equity", "--json", path], docs)
            data = json.load(open(path, "r", encoding="utf-8"))
        return data["checked"] == 3 and data["passed"] == 1 and list(data["refused"]) == ["D_US_Equity"] and data["missing"] == ["Q_US_Equity"], data
    arms.run("--json writes checked, passed, refused {name: problems}, missing", json_out)

    def census_file():
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "census.json")
            json.dump({"result": {"B_US_Equity": {}, "A_US_Equity": {}}}, open(path, "w", encoding="utf-8"))
            rc, out, reads = run(revalidate, ["--census-file", path], good)
        return rc == 0 and reads == ["A_US_Equity", "B_US_Equity"] and "checked 2" in out, (reads, out[-100:])
    arms.run("--census-file takes the census's names, sorted", census_file)

    def no_names():
        rc, out, _ = run(revalidate, [], good)
        return rc == 2 and "BLOCKED" in out, out[-100:]
    arms.run("no names: BLOCKED, exit 2", no_names)

    def each_read_once():
        rc, out, reads = run(revalidate, ["--names", "A_US_Equity,B_US_Equity,A_US_Equity"], good)
        return reads.count("A_US_Equity") == 1 and "checked 2" in out, reads
    arms.run("a duplicated name is read once", each_read_once)

    def uses_current_contract():
        from lib.research.aifill import contract
        real = contract.validate_document
        contract.validate_document = lambda d: ["forced problem"]
        try:
            rc, out, _ = run(revalidate, ["--names", "A_US_Equity"], good)
        finally:
            contract.validate_document = real
        return rc == 1 and "forced problem" in out, out[-120:]
    arms.run("it validates through contract.validate_document (the current contract)", uses_current_contract)

    def ascii_source():
        src = open(revalidate.__file__, "rb").read()
        return src.isascii() and b"import anthropic" not in src and b"import urllib" not in src, "non-ASCII or network import"
    arms.run("the module is ASCII and makes no model or network call", ascii_source)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
