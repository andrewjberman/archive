"""CA-h-1 AC1: a source that cannot be read is shown as unreadable with its last good time, never as an empty list.
Run from the repo root. Prints H1-FAILURE-SHAPE ok=<bool> reason=<text>."""
import importlib
import os
import json
import pathlib
import sys
import tempfile

MOD = os.environ.get("H1_MOD_UNDER_TEST", "data.transcripts.scripts.muse_reader.refresh")  # the env var is the green-arm hook
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[9]))


def out(ok, reason):
    print("H1-FAILURE-SHAPE ok=%s reason=%s" % (ok, reason))
    sys.exit(0)


try:
    m = importlib.import_module(MOD)
except Exception as e:  # noqa: BLE001 -- the base has no module: that is the expected FAIL
    out(False, "import %s: %s" % (type(e).__name__, e))
names = list(getattr(m, "SOURCES", ()))
BASE4 = {"drafts", "eod_today", "open_calls", "sprint_today"}   # round 16; CA-j-13 (FWD-13) adds mentions and mail_log, so the four must be present and nothing else may be
EXTRA = {"mentions", "mail_log"}
if not BASE4 <= set(names) or not set(names) <= BASE4 | EXTRA or len(names) != len(set(names)):
    out(False, "SOURCES=%r" % (names,))


def good(items):
    return lambda: items


def boom():
    raise RuntimeError("boom")


with tempfile.TemporaryDirectory() as td:
    root = pathlib.Path(td)
    t1, t2 = "2026-10-13T16:00:00Z", "2026-10-13T16:30:00Z"
    ok_readers = {"open_calls": good([{"id": "a"}]), "drafts": good([]), "eod_today": good([{"id": "e"}]),
                  "sprint_today": good([{"id": "s"}])}
    ok_readers.update({n: good([]) for n in names if n not in ok_readers})   # a source CA-j-13 added reads as a true empty here
    m.refresh(root, ok_readers, t1)
    d0 = json.loads((root / "drafts.json").read_text(encoding="utf-8"))
    if d0.get("status") != "ok" or d0.get("items") != [] or d0.get("read_at") != t1:
        out(False, "control: a true empty must read status=ok items=[] read_at=%s, got %r" % (t1, d0))
    bad = dict(ok_readers)
    bad["open_calls"] = boom
    m.refresh(root, bad, t2)
    f = json.loads((root / "open_calls.json").read_text(encoding="utf-8"))
    if f.get("status") != "unreadable":
        out(False, "failed source status=%r" % (f.get("status"),))
    if f.get("items") is not None:
        out(False, "failed source items=%r (must be null, never [])" % (f.get("items"),))
    if f.get("last_good_at") != t1:
        out(False, "last_good_at=%r want %s" % (f.get("last_good_at"), t1))
    if "boom" not in str(f.get("error")):
        out(False, "error=%r" % (f.get("error"),))
    if f.get("read_at") != t2:
        out(False, "read_at=%r want %s" % (f.get("read_at"), t2))
    o = json.loads((root / "eod_today.json").read_text(encoding="utf-8"))
    if o.get("status") != "ok":
        out(False, "an unrelated source went down with it: %r" % (o.get("status"),))
out(True, "failed source unreadable+null+last_good_at; control true-empty ok")
