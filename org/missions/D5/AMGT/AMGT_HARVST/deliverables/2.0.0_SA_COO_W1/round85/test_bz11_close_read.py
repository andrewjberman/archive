"""Tests for bz11_close_read.py: every verdict, the CLOSE line, the since-cut, and a mutant that proves the cut discriminates."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "bz11_close_read.py")
SINCE = "2026-10-14T01:00:00Z"


def put(state, publisher, cycle_id, record=None, checkpoint=None):
    folder = os.path.join(state, "cycles", publisher)
    os.makedirs(folder, exist_ok=True)
    if record is not None:
        with open(os.path.join(folder, cycle_id + ".cycle.json"), "w", encoding="utf-8") as handle:
            json.dump(dict(record, publisher=publisher, cycle_id=cycle_id), handle)
    if checkpoint is not None:
        with open(os.path.join(folder, cycle_id + ".checkpoint.json"), "w", encoding="utf-8") as handle:
            json.dump(checkpoint, handle)


def ended(started, completed, stopped=None):
    return {"started_at": started, "ended_at": "2026-10-14T09:00:00Z", "completed": completed, "stopped": stopped}


def refusal(pub, klass="expired"):
    return {"publisher": pub, "key": "K1", "status": "sign_in_refused", "class": klass, "http_status": 401}


def read(state, since=SINCE):
    out = subprocess.run([sys.executable, SCRIPT, "--state-dir", str(state), "--since", since], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    return out.stdout.splitlines()


def test_nothing_since_the_cut_waits(tmp_path):
    assert read(tmp_path) == ["PUBLISHER=wsj VERDICT=WAITING", "PUBLISHER=barrons VERDICT=WAITING", "CLOSE=WAITING"]


def test_both_alive_is_met(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", ended("2026-10-14T01:05:00Z", True))
    put(tmp_path, "barrons", "20261014T100000Z", ended("2026-10-14T10:00:00Z", True))
    assert read(tmp_path) == ["PUBLISHER=wsj VERDICT=ALIVE", "PUBLISHER=barrons VERDICT=ALIVE", "CLOSE=MET"]


def test_a_non_expiry_class_names_the_cause_and_closes(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", ended("2026-10-14T01:05:00Z", True))
    put(tmp_path, "barrons", "20261014T100000Z", None, {"refusals": [refusal("barrons", "blocked")]})
    lines = read(tmp_path)
    assert lines[1] == "PUBLISHER=barrons VERDICT=NON_EXPIRY:blocked" and lines[-1] == "CLOSE=MET"


def test_a_refresh_that_did_not_hold_is_not_met(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", ended("2026-10-14T01:05:00Z", True))
    put(tmp_path, "barrons", "20261014T100000Z", ended("2026-10-14T10:00:00Z", False, "sign_in_refused"),
        {"refusals": [refusal("barrons"), refusal("barrons")], "refreshes": {"barrons": {"outcome": "done"}}})
    lines = read(tmp_path)
    assert lines[1] == "PUBLISHER=barrons VERDICT=NOT_CURED" and lines[-1] == "CLOSE=NOT_MET"


def test_a_failed_refresh_is_not_met(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", None,
        {"refusals": [refusal("wsj")], "refreshes": {"wsj": {"outcome": "failed"}}})
    lines = read(tmp_path)
    assert lines[0] == "PUBLISHER=wsj VERDICT=REFRESH_FAILED" and lines[-1] == "CLOSE=NOT_MET"


def test_one_refusal_and_a_done_refresh_still_waits(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", None,
        {"refusals": [refusal("wsj")], "refreshes": {"wsj": {"outcome": "done"}}})
    assert read(tmp_path)[0] == "PUBLISHER=wsj VERDICT=WAITING"


def test_a_cycle_before_the_cut_is_ignored(tmp_path):
    put(tmp_path, "wsj", "20261013T173708Z", ended("2026-10-13T17:37:08Z", True))
    put(tmp_path, "barrons", "20261013T184606Z", None, {"refusals": [refusal("barrons", "blocked")]})
    assert read(tmp_path) == ["PUBLISHER=wsj VERDICT=WAITING", "PUBLISHER=barrons VERDICT=WAITING", "CLOSE=WAITING"]


def test_mutant_without_the_cut_would_close_on_the_old_cycle(tmp_path):
    """A control: the same state read with --since in the past DOES close, so the previous test is the cut's doing."""
    put(tmp_path, "wsj", "20261013T173708Z", ended("2026-10-13T17:37:08Z", True))
    put(tmp_path, "barrons", "20261013T184606Z", ended("2026-10-13T18:46:06Z", True))
    assert read(tmp_path, since="2026-10-13T00:00:00Z")[-1] == "CLOSE=MET"
    assert read(tmp_path)[-1] == "CLOSE=WAITING"


def test_an_incomplete_ended_cycle_is_not_alive(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", ended("2026-10-14T01:05:00Z", False, "bot_check"))
    assert read(tmp_path)[0] == "PUBLISHER=wsj VERDICT=WAITING"


def test_t0_file_gives_the_cut_and_a_missing_file_waits(tmp_path):
    put(tmp_path, "wsj", "20261014T010500Z", ended("2026-10-14T01:05:00Z", True))
    put(tmp_path, "barrons", "20261014T100000Z", ended("2026-10-14T10:00:00Z", True))
    t0 = tmp_path / "t0.txt"
    t0.write_text("noise" + chr(10) + "T0=2026-10-14T01:00:00Z" + chr(10), encoding="utf-8")
    out = subprocess.run([sys.executable, SCRIPT, "--state-dir", str(tmp_path), "--t0-file", str(t0)], capture_output=True, text=True)
    assert out.stdout.splitlines()[-1] == "CLOSE=MET", out.stdout
    gone = subprocess.run([sys.executable, SCRIPT, "--state-dir", str(tmp_path), "--t0-file", str(tmp_path / "nope.txt")], capture_output=True, text=True)
    assert gone.stdout.strip() == "CLOSE=WAITING reason=no-t0-file", gone.stdout
