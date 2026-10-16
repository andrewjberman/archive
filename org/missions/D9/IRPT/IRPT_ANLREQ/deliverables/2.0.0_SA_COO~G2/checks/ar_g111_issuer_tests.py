"""IRPT_ANLREQ AR-g-111 issuer tests (2.0.0_SA_COO~G2): irpt-status returns the closed failure code and its words (C-HOP-FAILURE).

Run by ar_g111_checks.py with AR111_ROOT = the investor-reporting folder to grade. Offline fixtures of the ops tests; no network. ASCII only.
"""
import importlib
import json
import os
import re
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(os.environ["AR111_ROOT"])
for rel in ("ops/tests", "ops", "ycharts/generate", "intake", "reports", "_keys", "_authz", "_gate", "_scope", "_ids", "lib"):
    if (ROOT / rel).is_dir():
        sys.path.insert(0, str(ROOT / rel))

import test_owned_report as support  # noqa: E402
import durable_job  # noqa: E402

owned_status = importlib.import_module("owned_status")
status = owned_status.status
world = support.world  # noqa: F841 (fixtures of the ops tests, used by name)
retention_world = support.retention_world  # noqa: F841
report_world = support.report_world
SCHEMA = json.loads((support.report_support.ROOT / "docs/contracts/investor-reporting/v1/StatusEnvelope.schema.json").read_text())

HOP_CODES = [(hop, code) for hop, codes in durable_job.HOP_FAILURE_CODES.items() for code in codes]
AT = "2026-10-16T03:00:00Z"


def hop_row(hop, code):
    return {"M": {"hop": {"S": hop}, "code": {"S": code}, "at": {"S": AT}}}


def read(r):
    return owned_status.OwnedJobStatusReader(requests=r.requests, reports=r.reader).read(r.w.case.principal, r.id)


def test_every_writer_code_has_words_and_the_table_is_closed():
    writer_codes = {code for _hop, code in HOP_CODES}
    assert writer_codes <= set(status.FAILURE_WORDS)
    assert set(status.FAILURE_WORDS) == writer_codes | {"DELIVERIES_EXHAUSTED"}
    assert set(status.FAILURE_STEP_WORDS) == {"READY_SIGNAL", "COMMENTARY", "PACKAGER", "GENERATE"}
    for text in list(status.FAILURE_WORDS.values()) + list(status.FAILURE_STEP_WORDS.values()):
        assert text.strip() and all(ord(c) < 128 for c in text) and "{" not in text and "%" not in text
    for code in status.FAILURE_WORDS:
        assert re.fullmatch(r"[A-Z0-9_]+", code)


def test_failure_words_falls_back_to_the_step_then_the_generate_step_never_blank():
    assert status.failure_words("PACKAGER_FAILED", "PACKAGER") == status.FAILURE_WORDS["PACKAGER_FAILED"]
    assert status.failure_words("SOMETHING_NEW", "COMMENTARY") == status.FAILURE_STEP_WORDS["COMMENTARY"]
    assert status.failure_words(None, "PACKAGER") == status.FAILURE_STEP_WORDS["PACKAGER"]
    assert status.failure_words("SOMETHING_NEW", "NO_SUCH_STEP") == status.FAILURE_STEP_WORDS["GENERATE"]
    assert status.failure_words(None, None) == status.FAILURE_STEP_WORDS["GENERATE"]


@pytest.mark.parametrize("hop,code", HOP_CODES)
def test_a_hop_failure_travels_as_the_reason_code_with_its_words(report_world, hop, code):
    r = report_world
    before = read(r)
    r.job["hop_failure"] = hop_row(hop, code)
    value = read(r)
    assert value["public_reason_code"] == code and value["state"] == before["state"]
    assert [(a["action"], a["safe"], a["description"]) for a in value["actions"]] == \
        [(a["action"], a["safe"], a["description"]) for a in before["actions"]] + [("NONE", True, status.FAILURE_WORDS[code])]
    assert value["source_dates"] == before["source_dates"]
    assert AT not in json.dumps(value) and "hop_failure" not in json.dumps(value)
    jsonschema.Draft202012Validator(SCHEMA).validate(value)
    assert status.validate_envelope(value) == []


def test_a_known_hop_with_an_unknown_code_reads_the_steps_generic_words(report_world):
    r = report_world
    before = read(r)
    r.job["hop_failure"] = hop_row("PACKAGER", "PACKAGER_SOMETHING_NEW")
    value = read(r)
    assert value["public_reason_code"] == before["public_reason_code"]
    assert value["actions"][-1] == {"action": "NONE", "safe": True, "description": status.FAILURE_STEP_WORDS["PACKAGER"]}
    assert "SOMETHING_NEW" not in json.dumps(value)


def test_an_unknown_hop_is_ignored(report_world):
    r = report_world
    before = read(r)
    r.job["hop_failure"] = hop_row("NOPE", "PACKAGER_FAILED")
    after = read(r)
    assert {k: v for k, v in after.items() if k != "internal_correlation_id"} == {k: v for k, v in before.items() if k != "internal_correlation_id"}


def test_no_hop_failure_leaves_a_ready_job_unchanged_and_words_free(report_world):
    r = report_world
    value = read(r)
    assert all(a["action"] != "NONE" for a in value["actions"])


@pytest.mark.parametrize("phase", ["FAILED", "ATTENTION"])
def test_a_generate_failure_keeps_its_reason_and_reads_known_detail_codes(report_world, phase):
    r = report_world
    r.job["state"]["S"] = phase
    reason = owned_status.PHASES[phase][1]
    r.job["job_detail"]["S"] = json.dumps({"code": "DELIVERIES_EXHAUSTED", "cause": "X", "receives": 5, "cause_claim": "measured"})
    known = read(r)
    assert known["public_reason_code"] == reason
    assert known["actions"] == [{"action": "NONE", "safe": True, "description": status.FAILURE_WORDS["DELIVERIES_EXHAUSTED"]}]
    r.job["job_detail"]["S"] = json.dumps({"code": "TOLERANCE_REQUIRES_STATIC"})
    other = read(r)
    assert other["public_reason_code"] == reason
    assert other["actions"] == [{"action": "NONE", "safe": True, "description": status.FAILURE_STEP_WORDS["GENERATE"]}]
    assert "TOLERANCE" not in json.dumps(other)


@pytest.mark.parametrize("phase", ["RECEIVED", "CLAIMED", "CERTIFYING"])
def test_running_phases_keep_only_the_wait_action(report_world, phase):
    r = report_world
    r.job["state"]["S"] = phase
    assert all(a["action"] == "WAIT" for a in read(r)["actions"])
