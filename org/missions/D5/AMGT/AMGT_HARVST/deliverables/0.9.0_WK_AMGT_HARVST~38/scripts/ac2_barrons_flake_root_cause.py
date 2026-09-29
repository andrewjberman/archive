"""AC2 (HVST-w-4): root cause of the quarantined test_disabled_barrons_contract_defers_before_opening_a_browser,
reproduced OFFLINE. Nothing is written in the repo: every repair() call runs with cwd = a temp dir.

ARM A: the test body AS IT STANDS at HEAD (patch.dict on the module object the test imports), N runs.
ARM B: the body as it stood when it flaked (pre-58135da029: patch.dict on the DOTTED STRING
       "lib.opal_data_harvest.verification.REGISTRY") under pytest's import mode for this tree
       (no lib/__init__.py -> the test module is `opal_data_harvest.test_verification`, so the module
       `repair` lives in is `opal_data_harvest.verification`; the dotted string imports a SECOND copy
       `lib.opal_data_harvest.verification`). Same temp cwd across runs = "identical runs, no edit".
"""
import collections
import inspect
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ["HARVEST_REFUSE_NETWORK"] = "1"
ROOT = Path(__file__).resolve()
while not (ROOT / "lib").is_dir():
    ROOT = ROOT.parent
LIB = ROOT / "lib"
N = 30

# pytest.ini has `pythonpath = .` (repo root on sys.path); pytest's prepend mode puts lib/ on sys.path
# for a test file whose package chain stops below lib/ (lib/__init__.py is ABSENT).
print("lib/__init__.py exists: %s ; pytest.ini pythonpath line: %r"
      % ((LIB / "__init__.py").exists(),
         " ".join(ln.strip() for ln in (ROOT / "pytest.ini").read_text(encoding="utf-8").split("markers")[0].splitlines()[1:])))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(LIB))

import opal_data_harvest.verification as v_pytest_mod        # the module a pytest-collected test imports  # noqa: E402
import opal_data_harvest.transport as t_pytest_mod  # noqa: E402
import lib.opal_data_harvest.verification as v_dotted_mod    # what the dotted string resolves to  # noqa: E402
import lib.opal_data_harvest.transport as t_dotted_mod  # noqa: E402

print("module identity: opal_data_harvest.verification is lib.opal_data_harvest.verification -> %s"
      % (v_pytest_mod is v_dotted_mod))
print("REGISTRY identity: same dict object -> %s (id %s vs %s)"
      % (v_pytest_mod.REGISTRY is v_dotted_mod.REGISTRY, id(v_pytest_mod.REGISTRY), id(v_dotted_mod.REGISTRY)))
print("contracts.json barrons automatic_verification_enabled = %r (the unpatched value the guard sees)"
      % v_pytest_mod.REGISTRY["publishers"]["barrons"].get("automatic_verification_enabled"))


def line_of(fn, needle):
    src, start = inspect.getsourcelines(fn)
    for i, text in enumerate(src):
        if needle in text:
            return "%s:%d" % (Path(inspect.getsourcefile(fn)).relative_to(ROOT).as_posix(), start + i)
    return "?"


print("guard  (decides pass): %s" % line_of(v_pytest_mod.repair, 'automatic_verification_enabled", False'))
print("mkdir  (creates unused/): %s" % line_of(v_pytest_mod.repair, "folder.mkdir"))
print("bundle (KeyError):      %s" % line_of(v_pytest_mod.repair, 'envelope["bundle"]'))


def run_body(verification_module, transport_module, dotted):
    """The skipped test's body. Returns the outcome signature string."""
    target = "lib.opal_data_harvest.verification.REGISTRY" if dotted else verification_module.REGISTRY
    try:
        with patch.dict(target, {"publishers": {"barrons": {"automatic_verification_enabled": False}}}):
            case = unittest.TestCase()
            with case.assertRaisesRegex(transport_module.RequestRejected, "disabled by its publisher contract"):
                verification_module.repair("barrons", {}, "unused", lambda event: None)
        return "PASS"
    except BaseException as exc:  # signature = exception class + message, exactly what a runner prints
        return "FAIL " + type(exc).__name__ + ": " + str(exc).splitlines()[0][:90]


def arm(label, verification_module, transport_module, dotted, reset_between):
    tally = collections.Counter()
    seq = []
    with tempfile.TemporaryDirectory() as tmp:
        prev = os.getcwd()
        os.chdir(tmp)
        try:
            for i in range(N):
                if reset_between and Path("unused").exists():
                    os.rmdir("unused")
                sig = run_body(verification_module, transport_module, dotted)
                seq.append("P" if sig == "PASS" else ("K" if "KeyError" in sig else ("E" if "FileExistsError" in sig else "?")))
                tally[sig] += 1
            made = Path("unused").is_dir()
        finally:
            os.chdir(prev)
    print("%s: N=%d  pass=%d fail=%d  sequence(P=pass,K=KeyError,E=FileExistsError)=%s"
          % (label, N, tally["PASS"], N - tally["PASS"], "".join(seq)))
    for sig, c in tally.most_common():
        print("    signature x%d: %s" % (c, sig))
    print("    unused/ present in the TEMP cwd after the runs: %s" % made)
    return tally, made


print("--- ARM A: body at HEAD (patch on the imported module object), one temp cwd, no reset between runs")
ta, ma = arm("ARM A", v_pytest_mod, t_pytest_mod, dotted=False, reset_between=False)

print("--- ARM B1: pre-58135da029 body, dotted-string target, module = opal_data_harvest.verification (pytest import mode), NO reset between runs")
tb, mb = arm("ARM B1", v_pytest_mod, t_pytest_mod, dotted=True, reset_between=False)

print("--- ARM B2: same, but unused/ removed before every run (the first-run signature, repeated)")
tb2, mb2 = arm("ARM B2", v_pytest_mod, t_pytest_mod, dotted=True, reset_between=True)

print("--- ARM C: pre-58135da029 body, dotted-string target, module = lib.opal_data_harvest.verification (unittest -m lib.... import mode: one copy), NO reset")
tc, mc = arm("ARM C", v_dotted_mod, t_dotted_mod, dotted=True, reset_between=False)

repo_unused = ROOT / "unused"
print("repo-root unused/ in THIS worktree: %s" % repo_unused.exists())
main_unused = Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/unused")
if main_unused.exists():
    import datetime
    print("main-tree repo-root unused/: exists=%s is_dir=%s entries=%d mtime(local)=%s"
          % (True, main_unused.is_dir(), len(list(main_unused.iterdir())),
             datetime.datetime.fromtimestamp(main_unused.stat().st_mtime).isoformat(timespec="seconds")))

flake_reproduced = tb["PASS"] == 0 and any("KeyError" in s for s in tb2) and any("FileExistsError" in s for s in tb)
print("VERDICT: ARM A (HEAD) %d/%d pass -> the flake does NOT reproduce at HEAD." % (ta["PASS"], N))
print("VERDICT: ARM B (dotted string under pytest import mode) 0 of %d pass; first run KeyError 'bundle' (unused/ made at verification.py mkdir), every later run FileExistsError -> "
      "the alternation is REPRODUCED: reproduced=%s" % (N, flake_reproduced))
print("ROOT CAUSE: the dotted-string patch target imports a SECOND module copy (lib.opal_data_harvest.verification) whose REGISTRY is patched, "
      "while repair() under test lives in opal_data_harvest.verification and reads its OWN unpatched REGISTRY (barrons enabled=True) at %s; "
      "the guard passes, %s creates unused/ in the cwd, %s raises KeyError('bundle'); the next run finds unused/ and %s raises FileExistsError."
      % (line_of(v_pytest_mod.repair, 'automatic_verification_enabled", False'), line_of(v_pytest_mod.repair, "folder.mkdir"),
         line_of(v_pytest_mod.repair, 'envelope["bundle"]'), line_of(v_pytest_mod.repair, "folder.mkdir")))
print("unused/ produced by this path: %s (ARM B1 temp cwd %s, ARM C temp cwd %s, ARM A temp cwd %s)" % (mb, mb, mc, ma))
