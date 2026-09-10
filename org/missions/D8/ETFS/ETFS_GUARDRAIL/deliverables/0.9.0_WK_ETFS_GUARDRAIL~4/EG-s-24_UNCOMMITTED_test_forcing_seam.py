"""ETFS_GUARDRAIL.TO-EG-s-24 -- the forcing seam, hermetically.

NOT PACKAGED (archive_file zips only lambda_function.py); boto3 clients are stubbed at
MODULE level before import, so no test ever reaches a real AWS endpoint.

THE CELL'S REAL SUBJECT IS THE SAFETY ARM. `--fixture-remove` makes the monthly report
DROP ITS OWN INPUT DATA, so a scheduled fire able to reach it would publish a report over
data it silently removed. These arms prove the default is OFF, that the scheduled command
string is BIT-FOR-BIT what it was before the seam existed, and that no payload shape the
schedule can deliver reaches the flag.

THE "BEFORE" IS A REAL BEFORE, RESOLVED BY CONTENT (Rule 22a): the pre-change blob is read
out of git at a pinned commit and its sha256 is checked against the value measured on the
DEPLOYED zip member, with a negative control -- never by filename and never by a comment
claiming what it is.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import os
import subprocess
import sys
from unittest import mock

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(MODULE_DIR, "..", "..", "..", ".."))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub-topic")

# The orchestrator as it stood BEFORE this cell -- the bytes that were deployed at
# 2026-09-10T03:54:09Z, measured off the function's own code zip under EG-s-20/EG-s-21.
PRE_CHANGE_PIN = "11c0810142"
PRE_CHANGE_SHA256 = "ac0484b73a26865eab649917cec7d1bf9c5d604ccd293cc72f17cb83e9e17000"
SOURCE_REL = "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py"


class _StubBotoClient:
    def __init__(self, service_name, calls):
        self._service_name = service_name
        self._calls = calls

    def __getattr__(self, name):
        def _call(**kwargs):
            self._calls.append((self._service_name, name, kwargs))
            if name == "get_object":
                raise Exception("stub: no object")
            if name == "list_objects_v2":
                return {"KeyCount": 0, "Contents": []}
            return {}
        return _call


def _fresh_module(calls):
    with mock.patch("boto3.client", lambda service, **kw: _StubBotoClient(service, calls)):
        if "lambda_function" in sys.modules:
            del sys.modules["lambda_function"]
        return importlib.import_module("lambda_function")


def _pre_change_module(calls):
    """The PRE-CHANGE orchestrator, loaded from git at a pinned commit and verified BY
    CONTENT against the sha256 measured on the deployed zip member. A pin that does not
    hash to that value is a WRONG pin and the test says so rather than comparing against
    whatever it happened to fetch."""
    blob = subprocess.run(["git", "show", "%s:%s" % (PRE_CHANGE_PIN, SOURCE_REL)],
                          cwd=REPO_ROOT, capture_output=True)
    assert blob.returncode == 0 and blob.stdout, (
        "git show returned rc=%d / %d bytes -- a mangled ref reads clean-empty, so this "
        "assert is the positive control" % (blob.returncode, len(blob.stdout)))
    got = hashlib.sha256(blob.stdout).hexdigest()
    assert got == PRE_CHANGE_SHA256, (
        "PIN RESOLVED TO THE WRONG CONTENT: %s != %s" % (got, PRE_CHANGE_SHA256))
    path = os.path.join(REPO_ROOT, ".scratch", "egs24_pre_change_lambda_function.py")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(blob.stdout)
    spec = importlib.util.spec_from_file_location("lambda_function_pre_egs24", path)
    mod = importlib.util.module_from_spec(spec)
    with mock.patch("boto3.client", lambda service, **kw: _StubBotoClient(service, calls)):
        spec.loader.exec_module(mod)
    return mod


# Every marker-free payload shape the schedule can deliver. The EventBridge Scheduler
# target's own input is jsonencode({mode = "run"}) (infra/aws/terraform/etfs-reports/
# orchestrator.tf); the rest are the shapes a rule-style envelope or a hand invoke can
# present, including the default EventBridge envelope keys.
SCHEDULED_SHAPES = [
    {"mode": "run"},
    {},
    None,
    {"mode": "run", "month": "2026-08"},
    {"version": "0", "id": "abc", "detail-type": "Scheduled Event",
     "source": "aws.events", "account": "313476888478", "time": "2026-10-01T14:00:00Z",
     "region": "us-east-1", "resources": ["arn:aws:events:..."], "detail": {},
     "mode": "run"},
]

# Payloads that TRY to smuggle the forcing through a path the schedule could take.
SMUGGLE_SHAPES = [
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04"},            # no marker
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": False},
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": None},
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": ""},
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": 0},
    {"mode": "run", "detail": {"force_fixture_remove": "cottonwood:2026-08-04",
                               "test_run": True}},                                # nested
    {"mode": "run", "test_run": True, "FORCE_FIXTURE_REMOVE": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "Force_Fixture_Remove": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "fixture_remove": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "--fixture-remove": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "force_fixture_remove": None},
    {"mode": "run", "test_run": True, "force_fixture_remove": ""},
    {"mode": "run", "test_run": True, "force_fixture_remove": "   "},
    {"mode": "run", "test_run": True, "force_fixture_remove": []},
    {"mode": "run", "test_run": True, "force_fixture_remove": {}},
    {"mode": "run", "test_run": True, "force_fixture_remove": 1},
    {"mode": "run", "test_run": True, "force_fixture_remove": True},
    {"mode": "run", "test_run": True,
     "force_fixture_remove": ["cottonwood:2026-08-04"]},                          # list
    {"mode": "run", "test_run": True,
     "force_fixture_remove": '{"cottonwood": ["2026-08-04"]}'},                   # JSON str
]

# Shell-injection attempts through the spec: the value lands inside a single-quoted
# `su - ec2-user -c '...'` handed to SSM.
INJECTION_SPECS = [
    "cottonwood:2026-08-04'; rm -rf /tmp/x; echo '",
    "cottonwood:2026-08-04; curl http://evil",
    "cottonwood:2026-08-04 && whoami",
    "cottonwood:2026-08-04`id`",
    "cottonwood:2026-08-04$(id)",
    "cottonwood:2026-08-04\nrm -rf /",
    "cottonwood:2026-08-04 --s3-out s3://elsewhere/",
    "../../etc/passwd:2026-08-04",
    "cottonwood:2026-8-4",
    "cottonwood:not-a-date",
    "cottonwood:",
    ":2026-08-04",
    "cottonwood 2026-08-04",
]


def test_the_scheduled_command_is_bit_for_bit_what_it_was_before_the_seam():
    # (b) For every marker-free payload the schedule can deliver, the command string this
    # code builds is IDENTICAL to the command string the PRE-CHANGE code built.
    calls = []
    new = _fresh_module(calls)
    old = _pre_change_module(calls)
    compared = 0
    for ev in SCHEDULED_SHAPES:
        month = (ev or {}).get("month") or new._last_month()
        before = old._render_command(month)
        after = new._render_command(month, new._forcing_spec(ev))
        compared += 1
        assert after == before, "shape %r changed the scheduled command" % (ev,)
        assert "--fixture-remove" not in after[0]
    assert compared == len(SCHEDULED_SHAPES) == 5


def test_no_scheduled_or_smuggled_payload_reaches_the_forcing_flag():
    # (c) THE ARM THIS CELL EXISTS FOR. 0 of N reach the flag.
    calls = []
    mod = _fresh_module(calls)
    reached = []
    checked = 0
    for ev in SCHEDULED_SHAPES + SMUGGLE_SHAPES:
        spec = mod._forcing_spec(ev)
        cmd = mod._render_command("2026-08", spec)[0]
        checked += 1
        if spec or "--fixture-remove" in cmd:
            reached.append(ev)
    assert reached == [], "payloads reached the forcing flag: %r" % (reached,)
    assert checked == len(SCHEDULED_SHAPES) + len(SMUGGLE_SHAPES) == 24


def test_injection_attempts_are_refused_and_resolve_to_off():
    # (c, second half) A validated spec is the ONLY thing that reaches a shell string.
    calls = []
    mod = _fresh_module(calls)
    clean = mod._render_command("2026-08", "")[0]
    for bad in INJECTION_SPECS:
        ev = {"mode": "run", "test_run": True, "force_fixture_remove": bad}
        assert mod._forcing_spec(ev) == "", "accepted %r" % bad
        cmd = mod._render_command("2026-08", mod._forcing_spec(ev))[0]
        assert "--fixture-remove" not in cmd
        # THE PROPERTY IS THAT NONE OF THE ATTACKER'S TEXT REACHES THE COMMAND -- not that
        # the command contains no shell metacharacter. The command is `su - ec2-user -c
        # '...'` and legitimately ends in a quote; an earlier version of this assert keyed
        # on that quote and failed on the WRAPPER while the code was behaving correctly.
        assert cmd == clean, "a refused spec changed the command for %r" % bad
        # DELTA, not absence: the clean command legitimately contains `$(` (its own
        # `CHROME=$(ls -d ...)`), so "no `$(` in the command" is a false alarm about
        # pre-existing content. What must be true is that the count does not RISE.
        for frag in ("rm -rf", "curl", "whoami", "$(", "`", "passwd", "s3://elsewhere", ";"):
            assert cmd.count(frag) == clean.count(frag), (
                "fragment %r count rose from %d to %d for %r"
                % (frag, clean.count(frag), cmd.count(frag), bad))
    assert len(INJECTION_SPECS) == 13


def test_the_forcing_works_when_explicitly_asked():
    # (d) and the spec parses under the RENDERER'S OWN parser -- imported, not re-implemented.
    calls = []
    mod = _fresh_module(calls)
    spec = "cottonwood:2026-08-04,2026-08-05"
    ev = {"mode": "run", "month": "2026-08", "test_run": True, "force_fixture_remove": spec}

    assert mod._forcing_spec(ev) == spec
    cmd = mod._render_command("2026-08", mod._forcing_spec(ev))[0]
    assert (" --fixture-remove %s" % spec) in cmd
    assert cmd.rstrip("'").endswith("--fixture-remove %s" % spec)

    presentation = os.path.join(REPO_ROOT, "data", "etfs", "scripts", "presentation")
    if presentation not in sys.path:
        sys.path.insert(0, presentation)
    import render_month_end  # the PRODUCER's own parser

    parsed = render_month_end._parse_fixture_remove(spec)
    assert parsed == {"cottonwood": ["2026-08-04", "2026-08-05"]}


def test_the_seam_rides_the_test_marker_so_forcing_can_never_reach_aj():
    # The safety COMPOSITION: forcing requires TEST_MARKER, and TEST_MARKER is exactly what
    # EG-s-20's forbidden-filter keys on. So a run that drops its own input data can never
    # be a run whose recipients include aj@.
    calls = []
    # PIN THE PRODUCER'S SET for this arm: without it EMAIL_RECIPIENT falls back to the
    # module default (andrew@ alone) and the converse limb below would pass VACUOUSLY --
    # it would be asserting against a recipient set that never contained aj@ to begin with.
    prior = os.environ.get("EMAIL_RECIPIENT")
    os.environ["EMAIL_RECIPIENT"] = "aj@opalinvest.com,andrew@opalinvest.com"
    try:
        mod = _fresh_module(calls)
    finally:
        if prior is None:
            os.environ.pop("EMAIL_RECIPIENT", None)
        else:
            os.environ["EMAIL_RECIPIENT"] = prior
    assert mod.EMAIL_RECIPIENTS == ["aj@opalinvest.com", "andrew@opalinvest.com"]
    ev = {"mode": "run", "test_run": True, "force_fixture_remove": "cottonwood:2026-08-04"}
    assert mod._forcing_spec(ev) != ""
    for base in (mod.EMAIL_RECIPIENT, mod.TERMINAL_RECIPIENT):
        header, envelope = mod._resolve_recipients(ev, base)
        assert "aj@opalinvest.com" not in [a.lower() for a in envelope]
        assert "aj@" not in header.lower()
    # and the converse: any event that CAN reach aj@ resolves to no forcing at all
    for ev2 in ({"mode": "run"}, {"mode": "run", "month": "2026-08"}):
        _, envelope = mod._resolve_recipients(ev2, mod.EMAIL_RECIPIENT)
        assert "aj@opalinvest.com" in envelope
        assert mod._forcing_spec(ev2) == ""


def test_render_command_has_exactly_one_caller_and_a_defaulted_parameter():
    # S24-AC2's census, asserted rather than recalled: adding a parameter is only safe if
    # every caller is known, and a DEFAULTED parameter keeps an unknown one working.
    import ast
    src = open(os.path.join(MODULE_DIR, "lambda_function.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    callers = [n.lineno for n in ast.walk(tree)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "_render_command"]
    assert len(callers) == 1, "callers of _render_command: %r" % callers
    fn = [n for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef) and n.name == "_render_command"][0]
    assert [a.arg for a in fn.args.args] == ["month", "forcing"]
    assert len(fn.args.defaults) == 1, "`forcing` must be DEFAULTED"
