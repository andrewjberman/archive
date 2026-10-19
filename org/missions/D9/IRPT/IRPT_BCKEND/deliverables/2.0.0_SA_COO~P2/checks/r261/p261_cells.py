"""IRPT_BCKEND workstream ~PM round 17 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: the refresh Lambda's own drop guard (disappeared_entries, resolve_disappeared, compute_delta) counts a previous client key as RETAINED when every account id of its entry is present in ONE current entry (CTO ruling on row D2-S239, msg 10788, S239 yes; reader census IBcw3 readers R02, R03, R15).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBCW5  IB-cw-5  refresh.py: a re-keyed previous key is not a disappearance, is neither held nor carried; any missing account fails closed
    AC1  the eight named tests exist in tests/test_refresh_retained_key.py and ALL pass (run now)
    AC2  DIFFERENTIAL + SCENARIOS, run by the check itself over fixtures, base (HEAD~1) versus new: the paths with no re-key give byte-identical results from disappeared_entries, resolve_disappeared and compute_delta; the re-key fixture is a disappearance in the base and none in the new module; the split, account-less and mixed fixtures fail closed; the delta carries no new key; rekeyed_keys lists exactly the retained keys; refresh.py actually changed
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only refresh.py, the new test file and the order's paths, and both code files are in it
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

DIRP = "infra/aws/lambda/investor-reporting/directory"
RUNNER = DIRP + "/refresh.py"
TESTS = DIRP + "/tests/test_refresh_retained_key.py"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~461/"
NAMES = (
    "test_a_rekeyed_previous_key_is_not_a_disappearance_in_the_delta",
    "test_a_rekeyed_previous_key_is_neither_held_nor_carried",
    "test_a_key_with_one_account_in_no_current_entry_still_disappears",
    "test_a_key_whose_accounts_are_split_over_two_current_entries_still_disappears",
    "test_a_previous_entry_with_no_account_ids_still_disappears",
    "test_a_key_absent_from_the_source_is_still_carried_terminated",
    "test_an_unknown_source_still_holds_every_unretained_disappeared_key",
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
              if ln.startswith("PASSED ") and "test_refresh_retained_key.py::" in ln}
    notpassed = [n for n in NAMES if n not in passed]
    if notpassed:
        fail("named tests not reported PASSED: %s" % ", ".join(notpassed))
    print("OK: the eight named tests exist and all pass")


def _load(name, dirpath):
    spec = importlib.util.spec_from_file_location(name, str(Path(dirpath) / "refresh.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(dirpath))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(dirpath))
    return mod


def _entry(key, accounts):
    return {"ids": {"client_id": key, "account_ids": list(accounts)}}


def _scen(mod, previous, current, source, removed="2026-10-14"):
    try:
        carried, held, newly = mod.resolve_disappeared(previous, current, source, removed)
        res = {"carried": [mod._entry_key(e) for e in carried], "held": [mod._entry_key(e) for e in held], "newly": newly, "carried_bytes": carried}
        res["disappeared"] = [mod._entry_key(e) for e in mod.disappeared_entries(previous, current)]
        res["delta"] = mod.compute_delta(previous, current)
        return json.dumps(res, sort_keys=True, default=str)
    except Exception as exc:                        # noqa: BLE001 -- the differential compares even a raise
        return json.dumps({"raised": type(exc).__name__}, sort_keys=True)


def ac2(_):
    new_dir = P6.ROOT / DIRP
    if not (new_dir / "refresh.py").is_file():
        fail("no %s" % RUNNER)
    g = subprocess.run(["git", "show", "HEAD~1:" + RUNNER], cwd=str(P6.ROOT), capture_output=True)
    h = subprocess.run(["git", "show", "HEAD:" + RUNNER], cwd=str(P6.ROOT), capture_output=True)
    if g.returncode != 0 or h.returncode != 0:
        fail("cannot read refresh.py at HEAD~1 or HEAD")
    if g.stdout.replace(b"\r\n", b"\n") == h.stdout.replace(b"\r\n", b"\n"):
        fail("refresh.py is identical to the base: a differential over an unchanged file proves nothing")
    tmp = Path(tempfile.mkdtemp(prefix="p261_base_"))
    try:
        (tmp / "refresh.py").write_bytes(g.stdout)
        s = new_dir / "expiry.py"
        if not s.is_file():
            fail("no sibling expiry.py to load the base module")
        shutil.copy(str(s), str(tmp / "expiry.py"))
        base = _load("p261_refresh_base", tmp)
        new = _load("p261_refresh_new", new_dir)
        same = (
            ("gone key, its account in no current entry, still in the source (held)", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], {"K1"}),
            ("gone key absent from the source (carried TERMINATED)", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], set()),
            ("unknown source (all gone held)", [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], None),
            ("nothing gone", [_entry("K1", ["a1"])], [_entry("K1", ["a1"])], {"K1"}),
            ("gone key with one account present and one not (held)", [_entry("K1", ["a1", "a2"])], [_entry("K9", ["a1"])], {"K1"}),
        )
        for label, prev, cur, src in same:
            b, n = _scen(base, prev, cur, src), _scen(new, prev, cur, src)
            if b != n:
                fail("%s differs between the base and the new refresh.py:\n base %s\n new  %s" % (label, b[:240], n[:240]))
        if '"held": ["K1"]' not in _scen(new, [_entry("K1", ["a1"])], [_entry("K9", ["a9"])], {"K1"}):
            fail("the held fixture did not hold (the fixture itself is broken)")
        rekey_prev = [_entry("K1", ["a1"]), _entry("K2", ["a2", "a3"])]
        rekey_cur = [_entry("R1", ["a1", "a5"]), _entry("R2", ["a2", "a3", "a7"])]
        bj = json.loads(_scen(base, rekey_prev, rekey_cur, {"K1", "K2"}))
        if bj.get("raised") or bj["delta"]["disappeared"] != 2 or bj["held"] != ["K1", "K2"]:
            fail("the re-key fixture is not a disappearance of 2 held keys in the base (the fixture itself is broken)")
        n = json.loads(_scen(new, rekey_prev, rekey_cur, {"K1", "K2"}))
        if n.get("raised") or n["held"] != [] or n["carried"] != [] or n["disappeared"] != [] or n["delta"]["disappeared"] != 0:
            fail("the re-key fixture (both gone keys have all their accounts in one current entry) must not disappear and must be neither held nor carried; got %s" % json.dumps({k: v for k, v in n.items() if k != "carried_bytes"})[:300])
        if set(n["delta"]) != set(bj["delta"]):
            fail("the delta must carry no new key: base %s, new %s" % (sorted(bj["delta"]), sorted(n["delta"])))
        nn = json.loads(_scen(new, rekey_prev, rekey_cur, None))
        if nn.get("raised") or nn["held"] != [] or nn["carried"] != []:
            fail("with an unknown source a re-keyed key is still retained (its accounts are present); got held %s carried %s" % (nn.get("held"), nn.get("carried")))
        split = json.loads(_scen(new, [_entry("K1", ["a1", "a2"])], [_entry("R1", ["a1"]), _entry("R2", ["a2"])], {"K1"}))
        if split.get("raised") or split["held"] != ["K1"] or split["delta"]["disappeared"] != 1:
            fail("a key whose accounts are split over two current entries must disappear and be held (fails closed); got held %s disappeared %s" % (split.get("held"), split.get("delta", {}).get("disappeared")))
        noacc = json.loads(_scen(new, [{"ids": {"client_id": "K1"}}], [_entry("R1", ["a1"])], {"K1"}))
        if noacc.get("raised") or noacc["held"] != ["K1"] or noacc["delta"]["disappeared"] != 1:
            fail("a previous entry with no account ids must disappear and be held (fails closed); got held %s" % noacc.get("held"))
        mixed = json.loads(_scen(new, [_entry("K1", ["a1"]), _entry("K3", ["a3"]), _entry("K4", ["a4"])], [_entry("R1", ["a1"])], {"K1", "K3"}))
        if mixed.get("raised") or mixed["held"] != ["K3"] or mixed["carried"] != ["K4"] or mixed["delta"]["disappeared"] != 2:
            fail("K1 retained, K3 held (in source, no current account), K4 carried TERMINATED (absent from the source), delta disappeared 2; got held %s carried %s disappeared %s" % (mixed.get("held"), mixed.get("carried"), mixed.get("delta", {}).get("disappeared")))
        rk = getattr(new, "rekeyed_keys", None)
        if not callable(rk):
            fail("refresh has no callable rekeyed_keys(previous_entries, current_entries)")
        got = rk(rekey_prev + [_entry("K5", ["a5x"])], rekey_cur)
        if list(got) != ["K1", "K2"]:
            fail("rekeyed_keys must return exactly the retained keys, sorted; got %s" % list(got))
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)
    print("OK: the unchanged paths are byte-identical, base versus new; the re-key fixture no longer disappears; the split, account-less and mixed fixtures fail closed; the delta has no new key; rekeyed_keys lists exactly the retained keys")


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if RUNNER not in files or TESTS not in files:
        fail("the worker's commit must contain both refresh.py and the new test file; it contains %s" % files)
    bad = [x for x in files if x not in (RUNNER, TESTS) and not x.startswith(DELIV) and "INVESTIGATION_v1.md" not in x and "TO-IB-cw-5" not in x]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: one commit, refresh.py and the new test file in it, nothing outside the order's paths")


CHECKS = {"IBCW5-AC1": ac1, "IBCW5-AC2": ac2, "IBCW5-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p261_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
