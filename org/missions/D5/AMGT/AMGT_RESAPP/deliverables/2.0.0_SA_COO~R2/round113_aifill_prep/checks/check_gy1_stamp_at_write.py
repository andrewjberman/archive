"""check_gy1_stamp_at_write.py -- acceptance arms for AMGT-gy-1 (AIFILL round 113: CTO condition C-1 of the cc02 pair).

  python check_gy1_stamp_at_write.py <repo root>
Offline, stdlib only, no model, no network. The CTO's condition: the producer stamps a PASS block CLEARED at write when no hold applies,
tested with a planted PASS block and a planted REFUSED block; until it lands no new AI fill document is stored. Nine arms for the change,
and three that pass at the base as controls (the existing stamp function is untouched, and the files stay ASCII).
  validation.stamp_for_write(doc, now, hold=False): PASS block -> CLEARED (a NONE block too), REFUSED block -> HELD with verdict REFUSED
  and no raise, hold=True -> every block HELD, the input never mutated; run.main stamps before it writes a file or S3 (--hold flag).
"""
from __future__ import annotations

import contextlib
import copy
import datetime
import io
import json
import os
import sys
import tempfile

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round106_aifill_prep", "checks"))
import aifill_check_lib as L  # noqa: E402

from lib.research.aifill import contract, model, run, validation  # noqa: E402

NOW = datetime.datetime(2026, 10, 16, 18, 0, 0, tzinfo=datetime.timezone.utc)
KEY = "ASML_NA_Equity"
FIXTURE = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_RESAPP", "deliverables", "2.0.0_SA_COO~R2",
                       "round104_aifill_prep", "fixtures", "served_inputs_ASML_NA_Equity.json")
TEXT = "The officer list names the chief executive."
OPAL = {"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}


def grounded_block(block_id):
    record = {"version": "grounding/1", "checked_at": "2026-10-16T06:00:00Z",
              "sources": [{"url": None, "label": "Company officer list", "kind": "opal", "status": "OK", "http_status": None, "chars": 120}],
              "sentences": [{"text": TEXT, "verdict": "SUPPORTED", "source": 0, "quote": "names the chief executive"}], "model_call": None}
    return contract.make_block(block_id, "OPAL_SOURCE", TEXT, [dict(OPAL)], grounding=record)


def good_doc():
    blocks = {b: grounded_block(b) for b in contract.BLOCK_IDS[:4]}
    blocks["identity_description"] = contract.none_block("identity_description", "The identity header already has a company description.")
    return {"schema": contract.SCHEMA, "security_key": KEY, "as_of": "2026-10-16", "generated_at": "2026-10-16T06:00:00Z",
            "producer": {"version": contract.PRODUCER_VERSION, "model": contract.PRODUCER_MODEL}, "blocks": blocks}


def refused_doc():
    doc = good_doc()
    doc["blocks"]["mgmt_bio"]["citations"] = []  # the planted REFUSED block: an OPAL_SOURCE block with no citation
    return doc


class FakeS3(object):
    def __init__(self):
        self.puts = []

    def put_object(self, **kwargs):
        self.puts.append(kwargs)
        return {"ETag": "fake"}


def states(doc):
    return {b: (blk[contract.VALIDATION_KEY]["state"], blk[contract.VALIDATION_KEY]["verdict"]) for b, blk in doc["blocks"].items()}


def run_main(argv, client=None):
    os.environ.pop(model.KEY_ENV, None)
    sink = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(err):
        try:
            rc = run.main(argv, client=client)
        except SystemExit as stop:  # argparse refuses an unknown flag with SystemExit: that is a failed arm, never a dead check
            rc = stop.code if isinstance(stop.code, int) else 2
    return rc, sink.getvalue() + err.getvalue()


arms = L.Arms("GY-1")
fn = getattr(validation, "stamp_for_write", None)

arms.run("validation.stamp_for_write exists", lambda: (fn is not None, "missing" if fn is None else ""))
arms.run("a planted PASS block is stamped CLEARED, a NONE block too", lambda: (
    states(fn(good_doc(), NOW)) == {b: ("CLEARED", "PASS") for b in contract.BLOCK_IDS}, str(states(fn(good_doc(), NOW)))[:160]))


def refused_case():
    doc = refused_doc()
    assert contract.validate_block({k: v for k, v in doc["blocks"]["mgmt_bio"].items() if k != "validation"}), "the plant is not refused by the rule"
    got = states(fn(doc, NOW))
    want = {b: ("CLEARED", "PASS") for b in contract.BLOCK_IDS}
    want["mgmt_bio"] = ("HELD", "REFUSED")
    return got == want, str(got)[:200]


arms.run("a planted REFUSED block stays HELD with verdict REFUSED, no raise, the rest CLEARED", refused_case)
arms.run("hold=True stamps every block HELD (the verdict is kept)", lambda: (
    states(fn(good_doc(), NOW, hold=True)) == {b: ("HELD", "PASS") for b in contract.BLOCK_IDS}, ""))


def not_mutated():
    doc = good_doc()
    before = copy.deepcopy(doc)
    fn(doc, NOW)
    return doc == before, "the input document changed"


arms.run("the input document is not mutated", not_mutated)
arms.run("the stamped PASS document passes contract.validate_document", lambda: (contract.validate_document(fn(good_doc(), NOW)) == [], ""))


def file_written(argv_extra):
    with tempfile.TemporaryDirectory() as tmp:
        rc, _ = run_main(["--key", KEY, "--inputs-file", FIXTURE, "--no-model", "--out", tmp] + argv_extra)
        with open(os.path.join(tmp, KEY + ".json"), "rb") as handle:
            doc = json.loads(handle.read().decode("ascii"))
    return rc, states(doc)


arms.run("run.main writes a file whose PASS blocks are CLEARED (no hold)", lambda: (
    file_written([])[0] == 0 and set(file_written([])[1].values()) == {("CLEARED", "PASS")}, str(file_written([])[1])[:160]))
arms.run("run.main --hold writes a file whose blocks are all HELD", lambda: (
    file_written(["--hold"])[0] == 0 and set(file_written(["--hold"])[1].values()) == {("HELD", "PASS")}, str(file_written(["--hold"])[1])[:160]))


def s3_write():
    fake = FakeS3()
    rc, _ = run_main(["--key", KEY, "--inputs-file", FIXTURE, "--no-model", "--to-s3", "--confirm-write"], client=fake)
    doc = json.loads(fake.puts[0]["Body"].decode("ascii")) if fake.puts else {"blocks": {}}
    return rc == 0 and len(fake.puts) == 1 and set(states(doc).values()) == {("CLEARED", "PASS")}, "puts=%d" % len(fake.puts)


arms.run("run.main --to-s3 --confirm-write puts exactly one object whose blocks are CLEARED", s3_write)

arms.run("CONTROL: stamp_validation still defaults to HELD", lambda: (
    set(states(validation.stamp_validation(good_doc(), NOW)).values()) == {("HELD", "PASS")}, ""))
arms.raises("CONTROL: stamp_validation CLEARED over a REFUSED block still raises", "ContractError",
            lambda: validation.stamp_validation(refused_doc(), NOW, state="CLEARED"))


def ascii_files():
    bad = [p for p in ("lib/research/aifill/validation.py", "lib/research/aifill/run.py")
           if any(b > 127 for b in open(os.path.join(ROOT, p), "rb").read())]
    return not bad, ",".join(bad)


arms.run("CONTROL: validation.py and run.py stay ASCII", ascii_files)
sys.exit(arms.finish())
