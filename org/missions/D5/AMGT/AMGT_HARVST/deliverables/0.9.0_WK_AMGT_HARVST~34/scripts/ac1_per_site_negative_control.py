"""HVST-z-3 AC1 -- per-site BEFORE/AFTER negative control for the dotted-string patch-target class.

Runs pytest collection IN-PROCESS over the five touched files so the test modules carry the names pytest
really gives them (opal_data_harvest.test_worker, posture.tests.test_posture, api.tests.test_scoped_amgt),
then for each of the 8 sites measures: with the patch applied, is the name READ THROUGH THE MODULE OBJECT
THE CODE UNDER TEST USES the mock?  BEFORE = the original dotted-string target; AFTER = the patch as now
written in the test file.  In-process, no network, no S3, no vendor call.
"""
import importlib
import os
import subprocess
import sys
from unittest import mock

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, ROOT)

FILES = ["lib/research/posture/tests/test_posture.py", "lib/research/api/tests/test_scoped_amgt.py",
         "lib/opal_data_harvest/test_retrieval_provenance.py", "lib/opal_data_harvest/test_verification.py",
         "lib/opal_data_harvest/test_worker.py"]
SITES = []
FACTS = []


def line_of(path, needle):
    for i, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        if needle in line:
            return i
    raise AssertionError("needle not found: %s in %s" % (needle, path))


def code_import(stmt, name):
    """Execute the code-under-test's OWN import statement (verbatim) and return the name it binds."""
    scope = {}
    exec(stmt, scope)
    return scope[name]


class Setattr:
    """monkeypatch.setattr as a context manager -- the same call the test makes -- yielding the sentinel."""

    def __init__(self, *args):
        self.args = args

    def __enter__(self):
        import pytest
        self.mp = pytest.MonkeyPatch()
        self.sentinel = object()
        self.mp.setattr(*self.args, self.sentinel)
        return self.sentinel

    def __exit__(self, *exc):
        self.mp.undo()


class DictPatch:
    """patch.dict(<target>, {...}) as the test does it; yields the value the patch installs."""

    def __init__(self, target):
        self.target = target

    def __enter__(self):
        self.p = mock.patch.dict(self.target, {"publishers": {"barrons": {"automatic_verification_enabled": "PATCHED"}}})
        self.p.start()
        return "PATCHED"

    def __exit__(self, *exc):
        self.p.stop()


def measure(label, path, before_line, before_txt, after_needle, string_ctx, object_ctx, read, owner_same, after_line=None):
    """read(): the value the code under test sees.  Took effect == read() is/== the installed mock."""
    with string_ctx() as m:
        before = read() is m or read() == m
    with object_ctx() as m:
        after = read() is m or read() == m
    SITES.append(dict(label=label, path=path, before_line=before_line, before_txt=before_txt,
                      after_line=after_line or line_of(path, after_needle), before=before, after=after, same=owner_same()))


class Plugin:
    def pytest_collection_finish(self, session):
        M = sys.modules
        # ---- 4 posture sites ---------------------------------------------------------------
        tp = M["posture.tests.test_posture"]
        # membership.py:161 `from lib.research.identity import crosswalk` (call-time), then crosswalk.resolve(...)
        cw = "from lib.research.identity import crosswalk as X"
        # comparable.py:179 `from lib.research.peers import engine as peers_engine`, then peers_engine.peers(...)
        eng = "from lib.research.peers import engine as X"
        for before_line, after_line in ((63, 65), (100, 102), (142, 144)):
            measure("posture crosswalk.resolve", FILES[0], before_line,
                    '@mock.patch("lib.research.identity.crosswalk.resolve", side_effect=_no_x1)',
                    'crosswalk_module, "resolve", side_effect=_no_x1)',
                    lambda: mock.patch("lib.research.identity.crosswalk.resolve"),
                    lambda: mock.patch.object(tp.crosswalk_module, "resolve"),
                    lambda: code_import(cw, "X").resolve,
                    lambda: tp.crosswalk_module is code_import(cw, "X"), after_line=after_line)
        measure("posture engine.peers", FILES[0], 188,
                'with mock.patch("lib.research.peers.engine.peers", side_effect=fake_peers):',
                'peers_engine_module, "peers", side_effect=fake_peers)',
                lambda: mock.patch("lib.research.peers.engine.peers"),
                lambda: mock.patch.object(tp.peers_engine_module, "peers"),
                lambda: code_import(eng, "X").peers,
                lambda: tp.peers_engine_module is code_import(eng, "X"))
        # ---- scoped_amgt: scoped_amgt.py:3224 `from lib.research.watchlist.store import star, unstar` (call-time)
        ts = M["api.tests.test_scoped_amgt"]
        star = "from lib.research.watchlist.store import star as X"
        measure("scoped_amgt watchlist.store.star", FILES[1], 278,
                'monkeypatch.setattr("lib.research.watchlist.store.star", fake_star)',
                'monkeypatch.setattr(watchlist_store, "star", fake_star)',
                lambda: Setattr("lib.research.watchlist.store.star"),
                lambda: Setattr(ts.watchlist_store, "star"),
                lambda: code_import(star, "X"),
                lambda: ts.watchlist_store is code_import("import lib.research.watchlist.store as X", "X"))
        # ---- retrieval_provenance: __main__.py:182 `import lib.research.harvest.store as store`; store._default_client()
        hs = "import lib.research.harvest.store as X"
        hs_test = importlib.import_module("lib.research.harvest.store")  # == the test's local `from lib.research.harvest import store`
        measure("retrieval_provenance harvest.store._default_client", FILES[2], 646,
                'monkeypatch.setattr("lib.research.harvest.store._default_client", lambda: _StubS3Client())',
                'monkeypatch.setattr(harvest_store, "_default_client"',
                lambda: Setattr("lib.research.harvest.store._default_client"),
                lambda: Setattr(hs_test, "_default_client"),
                lambda: code_import(hs, "X")._default_client,
                lambda: hs_test is code_import(hs, "X"))
        # ---- test_verification:18 patch.dict REGISTRY (the patch.dict variant)
        tv = M["opal_data_harvest.test_verification"]
        cut = M[tv.repair.__module__]  # the module `repair` (the code under test) really lives in under pytest
        measure("verification REGISTRY (patch.dict)", FILES[3], 18,
                'with patch.dict("lib.opal_data_harvest.verification.REGISTRY",',
                'with patch.dict(verification_module.REGISTRY,',
                lambda: DictPatch(importlib.import_module("lib.opal_data_harvest.verification").REGISTRY),
                lambda: DictPatch(tv.verification_module.REGISTRY),
                lambda: cut.REGISTRY["publishers"]["barrons"].get("automatic_verification_enabled"),
                lambda: tv.verification_module is cut)
        FACTS.append("verification: code under test lives in %r; the string target imports %r; REGISTRY dicts are the same object -> %s" % (
            tv.repair.__module__, "lib.opal_data_harvest.verification",
            importlib.import_module("lib.opal_data_harvest.verification").REGISTRY is cut.REGISTRY))
        # ---- test_worker:51 transport.time.time
        tw = M["opal_data_harvest.test_worker"]
        cutt = M[tw.PacedSession.__module__]
        lib_t = importlib.import_module("lib.opal_data_harvest.transport")
        measure("worker transport.time.time", FILES[4], 51,
                'with patch("lib.opal_data_harvest.transport.time.time", return_value=100):',
                'patch.object(transport_module.time, "time", return_value=100)',
                lambda: mock.patch("lib.opal_data_harvest.transport.time.time"),
                lambda: mock.patch.object(tw.transport_module.time, "time"),
                lambda: cutt.time.time,
                lambda: tw.transport_module is cutt)
        SITES[-1]["note"] = ("test_worker.py:51 works ONLY by the stdlib-singleton coincidence (see FACTS): the two transport module objects are "
                             "DIFFERENT, `time` is one process-wide object. The before-state has no failing form to exhibit; the control below shows the "
                             "same split DOES no-op on a non-singleton name.")
        FACTS.append("worker: code under test lives in %r; string target imports %r; the two module objects are the same -> %s" % (
            tw.PacedSession.__module__, "lib.opal_data_harvest.transport", lib_t is cutt))
        FACTS.append("worker: the stdlib singleton -- lib_transport.time is code-under-test transport.time -> %s (this is why BEFORE 'works')" % (lib_t.time is cutt.time))
        with mock.patch("lib.opal_data_harvest.transport.retry_seconds") as m:
            FACTS.append("worker CONTROL, same split, a NON-singleton name: patch('lib.opal_data_harvest.transport.retry_seconds') "
                         "seen by the code under test's module -> %s (the coincidence does not extend past `time`)" % (cutt.retry_seconds is m))


def main():
    import pytest
    rc = pytest.main(["--collect-only", "-q", "-p", "no:cacheprovider"] + FILES, plugins=[Plugin()])
    print("\n" + "=" * 100)
    print("AC1 -- per-site negative control (in-process pytest collection rc=%s; %d sites measured)" % (rc, len(SITES)))
    after_ok = 0
    misses = 0
    for n, s in enumerate(SITES, 1):
        print("\nSITE %d/%d  %s" % (n, len(SITES), s["label"]))
        print("  BEFORE  %s:%d  %s" % (s["path"], s["before_line"], s["before_txt"]))
        print("  AFTER   %s:%d" % (s["path"], s["after_line"]))
        if s["before"]:
            print("  BEFORE-state: patch DID take effect through the code-under-test's module (string resolved to the SAME object"
                  " or a shared singleton). The no-op CANNOT be exhibited here; what is proved instead: the string-target and the"
                  " code-under-test agree today, and the AFTER form binds to the module object by identity, not by re-import.")
        else:
            misses += 1
            print("  BEFORE-state: patch did NOT take effect through the code-under-test's module -- THE NO-OP, DEMONSTRATED.")
        if s.get("note"):
            print("  NOTE: " + s["note"])
        print("  AFTER-state : patch takes effect = %s ; patched module object IS the code-under-test's module object = %s" % (s["after"], s["same"]))
        if s["after"] and s["same"]:
            after_ok += 1
    print("\nFACTS")
    for f in FACTS:
        print("  " + f)
    print("\nAC1 SUMMARY: %d of %d sites reported; AFTER proved on %d of %d; BEFORE no-op demonstrated on %d of %d"
          % (len(SITES), 8, after_ok, len(SITES), misses, len(SITES)))
    sys.exit(0 if len(SITES) == 8 and after_ok == 8 else 1)


if __name__ == "__main__":
    main()
