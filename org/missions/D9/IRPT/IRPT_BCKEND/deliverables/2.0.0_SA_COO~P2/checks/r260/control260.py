"""Positive control and negatives for p260_cells.py (run by the issuer at the cut). Usage: python control260.py <real_repo_root>

Synthetic git repositories: a base commit holding the REAL directory_runner.py and its import siblings (lib/trading_calendar.py, the _ids folder,
schwab_account_codes), then ONE worker commit. The positive worker commit carries the issuer's REFERENCE implementation of the rule (a string patch
of the real file), which also proves the check is satisfiable.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r260/p260_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p260_cells as P  # noqa: E402

GOLD = "data/assets/scripts/gold/investor_reporting"
SIBLINGS = ["lib/trading_calendar.py", "infra/aws/lambda/investor-reporting/_ids/ids.py", "infra/aws/lambda/investor-reporting/_ids/raw_keys.json",
            GOLD + "/schwab_account_codes.py", GOLD + "/schwab_account_codes.json", GOLD + "/directory_runner.py"]

OLD = '''    cur = {entry_key(e) for e in entries if entry_key(e)}
    gone = [e for e in (previous_entries or []) if entry_key(e) and entry_key(e) not in cur]
'''
NEW = '''    cur = {entry_key(e) for e in entries if entry_key(e)}
    retained = set(rekeyed_keys(previous_entries, entries))
    gone = [e for e in (previous_entries or []) if entry_key(e) and entry_key(e) not in cur and entry_key(e) not in retained]
'''
HELPER = '''def rekeyed_keys(previous_entries: "list[dict]", entries: "list[dict]") -> "list[str]":
    """Previous client keys this build lacks whose every account id is present in ONE current entry (a re-key, not a drop)."""
    cur = {entry_key(e) for e in entries if entry_key(e)}
    cur_accounts = [set(str(a) for a in ((e.get("ids") or {}).get("account_ids") or ())) for e in entries]
    by_key = {}
    for e in (previous_entries or []):
        k = entry_key(e)
        if k and k not in cur:
            by_key.setdefault(k, set()).update(str(a) for a in ((e.get("ids") or {}).get("account_ids") or ()))
    return sorted(k for k, acc in by_key.items() if acc and any(acc <= c for c in cur_accounts))


'''
ANCHOR = "def carry_forward_removed("


def patch(src, variant="good"):
    assert OLD in src and ANCHOR in src, "the real file no longer has the expected anchors; update the control"
    if variant == "weak_subset":                 # retains when ANY account is present (fails open)
        h = HELPER.replace("acc <= c", "bool(acc & c)")
    elif variant == "split_ok":                  # accounts may be split over entries (fails open)
        h = HELPER.replace("any(acc <= c for c in cur_accounts)", "acc <= set().union(*cur_accounts)")
    elif variant == "empty_ok":                  # an account-less entry counts as retained
        h = HELPER.replace("if acc and any", "if any")
    elif variant == "drops_held":                # changes the unchanged path: nothing is ever held
        h = HELPER
    else:
        h = HELPER
    out = src.replace(ANCHOR, h + ANCHOR, 1).replace(OLD, NEW, 1)
    if variant == "drops_held":
        out = out.replace("            held.add(entry_key(e))\n            continue\n", "            continue\n", 1)
    if variant == "no_helper":
        out = out.replace("def rekeyed_keys(", "def _rekeyed_keys_hidden(", 1).replace("set(rekeyed_keys(", "set(_rekeyed_keys_hidden(", 1)
    return out


def tests_text(names, failing=None):
    body = "".join("def %s():\n    assert %s\n\n\n" % (n, "False" if n == failing else "True") for n in names)
    return body


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(variant="good", names=P.NAMES, failing=None, runner_changed=True, tests=True, extra=None, drop=None):
    root = Path(tempfile.mkdtemp(prefix="c260_"))
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
    (d / "IBcw4_notes.md").write_text("notes\n", encoding="utf-8")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
    if drop:
        git(root, "add", "-A")
        git(root, "reset", "-q", "HEAD", "--", drop)
        git(root, "commit", "-q", "-m", "worker")
    else:
        git(root, "add", "-A")
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
    expect("clean (reference implementation)", "IBCW4-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

AC1 = [
    ("a_named_test_missing", dict(names=P.NAMES[:-1])),
    ("a_named_test_failing", dict(failing=P.NAMES[2])),
    ("no_test_file", dict(tests=False)),
]
for label, kw in AC1:
    root = build(**kw)
    expect(label, "IBCW4-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)

AC2 = [
    ("runner_unchanged", dict(runner_changed=False)),
    ("weak_subset_any_account", dict(variant="weak_subset")),
    ("split_over_entries_retained", dict(variant="split_ok")),
    ("account_less_entry_retained", dict(variant="empty_ok")),
    ("unchanged_path_altered_nothing_held", dict(variant="drops_held")),
    ("no_rekeyed_keys_helper", dict(variant="no_helper")),
]
for label, kw in AC2:
    root = build(**kw)
    expect(label, "IBCW4-AC2", root, False)
    shutil.rmtree(root, ignore_errors=True)

for label, kw in (("file_outside_paths", dict(extra=["lib/other.py"])), ("runner_not_in_commit", dict(drop=P.RUNNER)), ("tests_not_in_commit", dict(drop=P.TESTS))):
    root = build(**kw)
    expect(label, "IBCW4-AC3", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c260_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBCW4-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
