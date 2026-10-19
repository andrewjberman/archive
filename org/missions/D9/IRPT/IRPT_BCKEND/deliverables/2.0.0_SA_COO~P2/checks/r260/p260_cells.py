"""IRPT_BCKEND workstream ~PM round 16 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: the runner's drop guard counts a previous client key as RETAINED when every account id of its entry is present in ONE current entry (CTO ruling on row D2-S239, msg 10788, S239 yes).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBCW4  IB-cw-4  directory_runner.py: carry_forward_removed leaves a re-keyed previous key neither held nor carried; any missing account fails closed
    AC1  the eight named tests exist in tests/test_directory_runner_retained_key.py and ALL pass (run now)
    AC2  DIFFERENTIAL + SCENARIOS, run by the check itself over fixtures, base (HEAD~1) versus new: a gone key with no account in a current entry, a gone key absent from the source, a missing source and an unchanged build give byte-identical results; the issuer's re-key fixture is retained by the new module (and held by the base), a split fixture and an account-less fixture are held, and the new rekeyed_keys lists exactly the retained keys; directory_runner.py actually changed
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only directory_runner.py, the new test file and the order's paths, and both code files are in it
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

DIRP = "data/assets/scripts/gold/investor_reporting"
RUNNER = DIRP + "/directory_runner.py"
TESTS = DIRP + "/tests/test_directory_runner_retained_key.py"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~460/"
NAMES = (
    "test_a_key_whose_every_account_is_in_one_current_entry_is_retained",
    "test_a_retained_key_is_neither_held_nor_carried_terminated",
    "test_a_key_with_one_account_in_no_current_entry_is_held",
    "test_a_key_whose_accounts_are_split_over_two_current_entries_is_held",
    "test_a_previous_entry_with_no_account_ids_is_held",
    "test_a_key_absent_from_the_source_is_still_carried_terminated",
    "test_a_missing_source_still_holds_every_unretained_gone_key",
    "test_rekeyed_keys_lists_exactly_the_retained_keys",
)
fail = P6.fail


def ac1(_):
    f = P6.ROOT / TESTS
    if not f.is_file():
        fail("no %s" % TESTS)
    src = f.read_text(encoding="utf-8")
    missing = [n for n in NAMES if "def %s(" % n not in src]
    if missing:
        fail("missing tests: %s" % ", ".join(missing))
    p = subprocess.run([sys.executable, "-m", "pytest", TESTS, "-q", "-rA", "--color=no", "-p", "no:cacheprovider"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=300)
    out = p.stdout
    if p.returncode != 0:
        fail("pytest rc %s: %s" % (p.returncode, out[-300:].replace("\n", " | ")))
    passed = {ln.strip().split("::")[-1].strip() for ln in out.replace("\\", "/").splitlines()
              if ln.startswith("PASSED ") and "test_directory_runner_retained_key.py::" in ln}
    notpassed = [n for n in NAMES if n not in passed]
    if notpassed:
        fail("named tests not reported PASSED: %s" % ", ".join(notpassed))
    print("OK: the eight named tests exist and all pass")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _entry(key, accounts):
    return {"ids": {"client_id": key, "account_ids": list(accounts)}}


def _scen(mod, label, previous, current, source, removed="2026-10-14"):
    try:
        carried, held = mod.carry_forward_removed(previous, current, source, removed)
        return json.dumps({"carried": [e["ids"]["client_id"] for e in carried], "held": held, "carried_bytes": carried}, sort_keys=True, default=str)
    except Exception as exc:                        # noqa: BLE001 -- the differential compares even a raise
        return json.dumps({"raised": type(exc).__name__}, sort_keys=True)


def ac2(_):
    new_path = P6.ROOT / RUNNER
    if not new_path.is_file():
        fail("no %s" % RUNNER)
    g = subprocess.run(["git", "show", "HEAD~1:" + RUNNER], cwd=str(P6.ROOT), capture_output=True)
    h = subprocess.run(["git", "show", "HEAD:" + RUNNER], cwd=str(P6.ROOT), capture_output=True)
    if g.returncode != 0 or h.returncode != 0:
        fail("cannot read directory_runner.py at HEAD~1 or HEAD")
    if g.stdout.replace(b"\r\n", b"\n") == h.stdout.replace(b"\r\n", b"\n"):
        fail("directory_runner.py is identical to the base: a differential over an unchanged file proves nothing")
    base_path = new_path.parent / "_p260_base_directory_runner.py"
    base_path.write_bytes(g.stdout)
    try:
        base = _load(base_path, "p260_runner_base")
        new = _load(new_path, "p260_runner_new")
        same = (
            ("gone key, its account in no current entry, still in the source (held)", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], {"K1"}),
            ("gone key absent from the source (carried TERMINATED)", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], set()),
            ("unknown source (nothing carried, all gone held)", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], None),
            ("nothing gone", [_entry("K1", ["a1"])], [_entry("K1", ["a1"])], {"K1"}),
            ("gone key with one account present and one not (held)", [_entry("K1", ["a1", "a2"])], [_entry("K9", ["a1"])], {"K1"}),
        )
        for label, prev, cur, src in same:
            b, n = _scen(base, label, prev, cur, src), _scen(new, label, prev, cur, src)
            if b != n:
                fail("%s differs between the base and the new runner:\n base %s\n new  %s" % (label, b[:240], n[:240]))
        if '"held": ["K1"]' not in _scen(new, "x", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], {"K1"}):
            fail("the held fixture did not hold (the fixture itself is broken)")
        rekey_prev = [_entry("K1", ["a1"]), _entry("K2", ["a2", "a3"])]
        rekey_cur = [_entry("R1", ["a1", "a5"]), _entry("R2", ["a2", "a3", "a7"])]
        if '"held": []' in _scen(base, "x", rekey_prev, rekey_cur, {"K1", "K2"}):
            fail("the re-key fixture is not held by the base (the fixture itself is broken)")
        n = json.loads(_scen(new, "re-key", rekey_prev, rekey_cur, {"K1", "K2"}))
        if n.get("raised") or n["held"] != [] or n["carried"] != []:
            fail("the re-key fixture (both gone keys have all their accounts in one current entry) must be neither held nor carried; got %s" % json.dumps(n)[:240])
        nn = json.loads(_scen(new, "re-key with unknown source", rekey_prev, rekey_cur, None))
        if nn.get("raised") or nn["held"] != [] or nn["carried"] != []:
            fail("with an unknown source a re-keyed key is still retained (its accounts are present); got %s" % json.dumps(nn)[:240])
        split = json.loads(_scen(new, "split", [_entry("K1", ["a1", "a2"])], [_entry("R1", ["a1"]), _entry("R2", ["a2"])], {"K1"}))
        if split.get("raised") or split["held"] != ["K1"]:
            fail("a key whose accounts are split over two current entries must be held (fails closed); got %s" % json.dumps(split)[:240])
        noacc = json.loads(_scen(new, "no account ids", [{"ids": {"client_id": "K1"}}], [_entry("R1", ["a1"])], {"K1"}))
        if noacc.get("raised") or noacc["held"] != ["K1"]:
            fail("a previous entry with no account ids must be held (fails closed); got %s" % json.dumps(noacc)[:240])
        mixed = json.loads(_scen(new, "mixed", [_entry("K1", ["a1"]), _entry("K3", ["a3"]), _entry("K4", ["a4"])], [_entry("R1", ["a1"])], {"K1", "K3"}))
        if mixed.get("raised") or mixed["held"] != ["K3"] or mixed["carried"] != ["K4"]:
            fail("K1 retained, K3 held (in source, no current account), K4 carried TERMINATED (absent from the source); got %s" % json.dumps(mixed)[:240])
        rk = getattr(new, "rekeyed_keys", None)
        if not callable(rk):
            fail("directory_runner has no callable rekeyed_keys(previous_entries, entries)")
        got = rk(rekey_prev + [_entry("K5", ["a5x"])], rekey_cur)
        if list(got) != ["K1", "K2"]:
            fail("rekeyed_keys must return exactly the retained keys, sorted; got %s" % list(got))
    finally:
        try:
            base_path.unlink()
        except OSError:
            pass
    print("OK: the unchanged paths are byte-identical, base versus new; the re-key fixture is retained, the split, account-less and mixed fixtures fail closed; rekeyed_keys lists exactly the retained keys")


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if RUNNER not in files or TESTS not in files:
        fail("the worker's commit must contain both directory_runner.py and the new test file; it contains %s" % files)
    bad = [x for x in files if x not in (RUNNER, TESTS) and not x.startswith(DELIV) and "INVESTIGATION_v1.md" not in x and "TO-IB-cw-4" not in x]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: one commit, directory_runner.py and the new test file in it, nothing outside the order's paths")


CHECKS = {"IBCW4-AC1": ac1, "IBCW4-AC2": ac2, "IBCW4-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p260_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
