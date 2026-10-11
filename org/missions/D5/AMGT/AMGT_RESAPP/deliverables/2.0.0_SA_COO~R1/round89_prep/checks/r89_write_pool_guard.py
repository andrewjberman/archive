"""AMGT_RESAPP round-89 PREP -- AMGT_RESAPP-S5: every crosswalk write_pool caller refuses ABSENT over a served count.

  python r89_write_pool_guard.py            (run from the repo root, PYTHONPATH=<repo root>)

CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_AMGT_RESAPP_S5_WRITE_POOL_GUARD_20261010.md`: kk-1's guard sits in
`crosswalk.main` only; `write_pool` is reached by three callers, and `add_security.py`'s twin of the swallowing helper lets a run
on a library-less box write `research_universe: absent` over a served folder count. The refusal lives in `write_pool`, bounded:
it fires only when `document` is a crosswalk document; the union write (no document, a different shape) stays byte-identical.

Over a STUBBED S3 client only (the harness of test_write_pool_union.py): no network, no real put.
    G1 door A (add_security._mint_pool, research library absent on this device): nothing is put and the served object's
       sha256 is unchanged.
    G2 door B (crosswalk.write_pool with a crosswalk document built without research folders): nothing is put and the
       served object's sha256 is unchanged.
    G3 the control arm (a document that CARRIES research folders, same served pool): the write lands -- a guard that
       refuses everything would pass G1 and G2.
    G4 the union write (write_pool with no document): lands byte-identical.
Verdict: R89 WRITE-POOL GUARD: YES|NO (exit 0|1). At the base (2026-10-11) G1 and G2 FAIL, G3 and G4 PASS.
"""
from __future__ import annotations

import copy
import hashlib
import os
import sys
import tempfile
from unittest import mock

from lib.research.identity import add_security, crosswalk
from lib.research.identity.tests.test_write_pool_union import KEY, _document, _FakeS3

FOLDERS_SERVED = 97


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _served_with_folders(document):
    served = copy.deepcopy(document)
    served["research_universe"] = {"source": "X:/Research", "read_at": "2026-10-07T17:18:12Z", "folders": FOLDERS_SERVED}
    served.setdefault("denominators", {})["research_folders_live"] = FOLDERS_SERVED
    return served


def _seeded(document):
    fake = _FakeS3()
    body = crosswalk.serialise(_served_with_folders(document))
    fake.seed(KEY, body)
    return fake, hashlib.sha256(body).hexdigest()


def _attempt(fn):
    """(raised?, the exception text). A refusal may be a raise or a nonzero return; both mean 'no put' when puts is empty."""
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 -- the arm grades the OBSERVABLE (puts, sha), not the exception class
        return True, "%s: %s" % (type(exc).__name__, str(exc)[:140])
    return False, ""


def main():
    document, rows, source = _document()
    absent = copy.deepcopy(document)
    absent["research_universe"] = {"absent": "no research_folders argument given to build_crosswalk"}
    absent_payload = crosswalk.serialise(absent)
    empty_library = tempfile.mkdtemp(prefix="r89_nolib_")
    missing_root = os.path.join(empty_library, "does-not-exist")

    # G1 -- door A: the add_security mint, on a device whose research library is absent (a set-but-missing root).
    fake, served_sha = _seeded(document)
    with mock.patch.dict(os.environ, {"OPAL_RESEARCH_LIBRARY_ROOT": missing_root}):
        raised, why = _attempt(lambda: add_security._mint_pool("2026-09-19", rows, source, None, None, client=fake))
    now_sha = hashlib.sha256(fake.objects[KEY]["Body"]).hexdigest()
    print("   door A: raised=%s puts=%s served sha equal=%s %s" % (raised, fake.puts, now_sha == served_sha, why))
    g1 = say(not fake.puts and now_sha == served_sha,
             "G1 door A (add_security._mint_pool, library absent): no put, the served object unchanged")

    # G2 -- door B: write_pool handed a crosswalk document with research_universe absent over the served count.
    fake, served_sha = _seeded(document)
    raised, why = _attempt(lambda: crosswalk.write_pool(KEY, absent_payload, document=absent, client=fake))
    now_sha = hashlib.sha256(fake.objects[KEY]["Body"]).hexdigest()
    print("   door B: raised=%s puts=%s served sha equal=%s %s" % (raised, fake.puts, now_sha == served_sha, why))
    g2 = say(not fake.puts and now_sha == served_sha,
             "G2 door B (write_pool, document research_universe absent): no put, the served object unchanged")

    # G3 -- the control: a document that carries research folders lands over the same served pool.
    carrying = copy.deepcopy(document)
    carrying["research_universe"] = {"source": "X:/Research", "read_at": "2026-10-11T00:00:00Z", "folders": FOLDERS_SERVED + 2}
    carrying.setdefault("denominators", {})["research_folders_live"] = FOLDERS_SERVED + 2
    fake, served_sha = _seeded(document)
    crosswalk.write_pool(KEY, crosswalk.serialise(carrying), document=carrying, client=fake)
    print("   control: puts=%s" % (fake.puts,))
    g3 = say(fake.puts == [KEY], "G3 control: a document carrying research folders is written over the served count")

    # G4 -- the union write (no document, another shape) is unchanged.
    fake, _ = _seeded(document)
    crosswalk.write_pool(KEY, b'{"x": 1}\n', client=fake)
    g4 = say(fake.objects[KEY]["Body"] == b'{"x": 1}\n', "G4 the union write (no document) lands byte-identical")

    ok = g1 and g2 and g3 and g4
    print("R89 WRITE-POOL GUARD: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
