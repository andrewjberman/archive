"""Positive control and negatives for p261_cells.py (run by the issuer at the cut). Usage: python control261.py <real_repo_root>

Synthetic git repositories: a base commit holding the REAL refresh.py and expiry.py, then ONE worker commit. The positive worker commit carries the issuer's
REFERENCE implementation of the rule (a string patch of the real file), which also proves the check is satisfiable.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r261/p261_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p261_cells as P  # noqa: E402

DIRP = "infra/aws/lambda/investor-reporting/directory"
SIBLINGS = [DIRP + "/refresh.py", DIRP + "/expiry.py"]

OLD_D = '''    cur = {_entry_key(e) for e in (current_entries or []) if _entry_key(e)}
    return [e for e in (previous_entries or []) if _entry_key(e) and _entry_key(e) not in cur]
'''
NEW_D = '''    cur = {_entry_key(e) for e in (current_entries or []) if _entry_key(e)}
    retained = set(rekeyed_keys(previous_entries, current_entries))
    return [e for e in (previous_entries or []) if _entry_key(e) and _entry_key(e) not in cur and _entry_key(e) not in retained]
'''
OLD_C = "    disappeared = sorted(set(prev) - set(cur))\n"
NEW_C = "    disappeared = sorted(set(prev) - set(cur) - set(rekeyed_keys(previous_entries, current_entries)))\n"
HELPER = '''def rekeyed_keys(previous_entries, current_entries):
    """Previous keys the current build lacks whose every account id sits in ONE current entry (a re-key, not a drop)."""
    cur = {_entry_key(e) for e in (current_entries or []) if _entry_key(e)}
    cur_accounts = [set(str(a) for a in ((e.get("ids") or {}).get("account_ids") or ())) for e in (current_entries or [])]
    by_key = {}
    for e in (previous_entries or []):
        k = _entry_key(e)
        if k and k not in cur:
            by_key.setdefault(k, set()).update(str(a) for a in ((e.get("ids") or {}).get("account_ids") or ()))
    return sorted(k for k, acc in by_key.items() if acc and any(acc <= c for c in cur_accounts))


'''
ANCHOR = "def disappeared_entries("


def patch(src, variant="good"):
    for a in (OLD_D, OLD_C, ANCHOR):
        assert a in src, "the real file no longer has the expected anchor; update the control"
    h = HELPER
    if variant == "weak_subset":
        h = HELPER.replace("acc <= c", "bool(acc & c)")
    elif variant == "split_ok":
        h = HELPER.replace("any(acc <= c for c in cur_accounts)", "acc <= set().union(*cur_accounts)")
    elif variant == "empty_ok":
        h = HELPER.replace("if acc and any", "if any")
    out = src.replace(ANCHOR, h + ANCHOR, 1)
    if variant != "delta_unpatched":
        out = out.replace(OLD_C, NEW_C, 1)
    if variant != "disappeared_unpatched":
        out = out.replace(OLD_D, NEW_D, 1)
    if variant == "drops_held":
        out = out.replace("        if _entry_key(e) in source:\n            held.append(e)\n            continue\n", "        if _entry_key(e) in source:\n            continue\n", 1)
    if variant == "new_delta_key":
        out = out.replace('    return {"added": len(added), "disappeared": len(disappeared),', '    return {"rekeyed": 0, "added": len(added), "disappeared": len(disappeared),', 1)
    if variant == "no_helper":
        out = out.replace("def rekeyed_keys(", "def _rekeyed_keys_hidden(", 1).replace("set(rekeyed_keys(", "set(_rekeyed_keys_hidden(")
    return out


def tests_text(names, failing=None):
    return "".join("def %s():\n    assert %s\n\n\n" % (n, "False" if n == failing else "True") for n in names)


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(variant="good", names=P.NAMES, failing=None, runner_changed=True, tests=True, extra=None, drop=None):
    root = Path(tempfile.mkdtemp(prefix="c261_"))
    for rel in SIBLINGS:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(REAL / rel), str(root / rel))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    git(root, "config", "core.autocrlf", "false")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    if runner_changed:
        src = (root / P.RUNNER).read_bytes().decode("utf-8")
        (root / P.RUNNER).write_bytes(patch(src, variant).encode("utf-8"))
    if tests:
        (root / P.TESTS).parent.mkdir(parents=True, exist_ok=True)
        (root / P.TESTS).write_text(tests_text(names, failing), encoding="utf-8")
    d = root / P.DELIV
    d.mkdir(parents=True)
    (d / "IBcw5_notes.md").write_text("notes\n", encoding="utf-8")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
    git(root, "add", "-A")
    if drop:
        git(root, "reset", "-q", "HEAD", "--", drop)
    git(root, "commit", "-q", "-m", "worker")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=300, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-40s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean (reference implementation)", "IBCW5-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

for label, kw in (("a_named_test_missing", dict(names=P.NAMES[:-1])), ("a_named_test_failing", dict(failing=P.NAMES[2])), ("no_test_file", dict(tests=False))):
    root = build(**kw)
    expect(label, "IBCW5-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)

for label, kw in (("refresh_unchanged", dict(runner_changed=False)), ("weak_subset_any_account", dict(variant="weak_subset")),
                  ("split_over_entries_retained", dict(variant="split_ok")), ("account_less_entry_retained", dict(variant="empty_ok")),
                  ("compute_delta_unpatched", dict(variant="delta_unpatched")), ("disappeared_entries_unpatched", dict(variant="disappeared_unpatched")),
                  ("unchanged_path_altered_nothing_held", dict(variant="drops_held")), ("a_new_delta_key", dict(variant="new_delta_key")),
                  ("no_rekeyed_keys_helper", dict(variant="no_helper"))):
    root = build(**kw)
    expect(label, "IBCW5-AC2", root, False)
    shutil.rmtree(root, ignore_errors=True)

for label, kw in (("file_outside_paths", dict(extra=["lib/other.py"])), ("refresh_not_in_commit", dict(drop=P.RUNNER)), ("tests_not_in_commit", dict(drop=P.TESTS))):
    root = build(**kw)
    expect(label, "IBCW5-AC3", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c261_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBCW5-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
