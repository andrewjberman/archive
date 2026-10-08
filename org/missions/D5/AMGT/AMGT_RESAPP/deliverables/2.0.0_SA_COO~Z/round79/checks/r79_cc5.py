"""AMGT_RESAPP round 79 -- cell AMGT-cc-5: the two build-side repairs of the scoped function.

  python r79_cc5.py --crit AC1|AC2|AC3 [--base <commit>]

Repair 1: the generated prefix module is restamped, so the build's own drift check passes again.
Repair 2: the builder's job-record prefix of the Seeking Alpha collector joins the generator and
the ONE prefix list in the function's terraform file, which both read grants are built from.

  AC1 (build, no network): the generator's --check exits 0; its test file passes whole; the four
       prefix values present at the cut are byte-equal to the cut; the new constant is in the
       generated module and in the generator, and equals the address builder's output computed
       here.
  AC2 (build, reads the terraform file as TEXT; no terraform command): the prefix list is the
       cut's list plus exactly the builder's prefix; the two expressions that turn the list into
       the object-read grant and the list condition are the cut's, once each; no action was added
       or removed anywhere in the file; nothing else in the file's code changed.
  AC3 (bound): from the base commit to HEAD, and in the working tree, nothing under the harvest
       terraform folder or the generated files changed except the four files of the cell.

Prints `PASS|FAIL <clause> <detail>` lines and one verdict line
`R79 CC5 <crit> SERVED: YES|NO`. Exit 0 on YES, 1 on NO. Writes nothing. Runs no terraform, no
AWS call and no network call.

R79_CC5_TREE (optional) names another file tree to read the four files from and to run the
generator and its test in; git is still asked in the repository of the working directory. It
exists so the check can be shown to reach YES against a scratch copy before the cell is built.
"""
from __future__ import annotations

import argparse
import ast
import collections
import importlib.util
import os
import re
import subprocess
import sys

# the cut: CLOUD HEAD when the cell was measured, 2026-10-08 10:3xZ
BASE_AT_THE_CUT = "c08ddaf71f87097508f0739d7843fe8e2b193c73"

GEN = "infra/aws/terraform/harvest/gen_harvest_prefixes.py"
TF = "infra/aws/terraform/harvest/scoped-amgt-api.tf"
MOD = "lib/research/api/_harvest_prefixes.py"
TEST = "lib/research/api/tests/test_harvest_prefixes.py"
ALLOWED = (GEN, TF, MOD, TEST)
BOUND_PATHS = ("infra/aws/terraform/harvest", MOD, TEST)
NOT_THIS_CELLS = ("infra/logic/registry", "lib/opal_naming.py", "org/standards/NAMING_SCHEMA.json")

NEW_NAME = "SEEKING_ALPHA_JOB_RECORD_STATE_PREFIX"
HASH_NAME = "REGISTRY_HASH"
LIST_NAME = "scoped_amgt_pool_prefixes"
TESTS_AT_THE_CUT = 6
ENTRIES_AT_THE_CUT = 33

_RESULTS = []


def say(text):
    sys.stdout.write(text.encode("ascii", "backslashreplace").decode("ascii") + "\n")


def clause(ok, name, detail=""):
    _RESULTS.append(bool(ok))
    say("%s %s %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


def note(text):
    say("   %s" % text)


def verdict(crit):
    yes = bool(_RESULTS) and all(_RESULTS)
    say("R79 CC5 %s SERVED: %s" % (crit, "YES" if yes else "NO"))
    return 0 if yes else 1


def repo_root():
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=False)
        top = out.stdout.decode("utf-8", "replace").strip()
        if out.returncode == 0 and top:
            return os.path.normpath(top)
    except OSError:
        pass
    return os.getcwd()


def git(root, *args):
    out = subprocess.run(["git", "-C", root] + list(args), capture_output=True, check=False)
    return out.returncode, out.stdout.decode("utf-8", "replace"), out.stderr.decode("utf-8", "replace").strip()


def read_tree(tree, rel):
    """The file's text, or None when it cannot be read."""
    try:
        with open(os.path.join(tree, rel.replace("/", os.sep)), encoding="utf-8", newline="") as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError):
        return None


def read_base(root, base, rel):
    """(text, None) of the file at the base commit, or (None, why). The control: an unreadable
    base is a FAIL of the clause that asked, never an empty file."""
    code, out, err = git(root, "show", "%s:%s" % (base, rel))
    if code != 0 or not out:
        return None, "git show %s:%s rc=%d %s" % (base[:10], rel, code, err[:120])
    return out, None


def constants_of(text):
    """{name: value} for every top-level NAME = 'string' of a module's text, read by syntax tree."""
    found = {}
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                found[node.targets[0].id] = node.value.value
    return found


def builder_prefixes(tree):
    """(job-record table prefix, its tier root, None) from the address builder, or (None, None, why).
    The table prefix is the key with its partition cut; the tier root has the table cut as well."""
    if tree not in sys.path:
        sys.path.insert(0, tree)
    try:
        import lib.opal_naming as naming
        scope = naming.lookup("harvest")["long"]
        address = naming.address("seeking-alpha", scope, "state", "job_record", "date=1970-01-01")
    except Exception as exc:  # noqa: BLE001 -- the reason is the finding
        return None, None, "%s: %s" % (type(exc).__name__, exc)
    key = address.split("://", 1)[1].split("/", 1)[1]
    parts = key.split("/")
    return "/".join(parts[:-1]) + "/", "/".join(parts[:-2]) + "/", None


def run_in(tree, argv):
    env = dict(os.environ)
    env["PYTHONPATH"] = tree
    env["PYTHONIOENCODING"] = "utf-8"
    out = subprocess.run([sys.executable] + argv, cwd=tree, env=env, capture_output=True, check=False)
    return out.returncode, (out.stdout + out.stderr).decode("utf-8", "replace")


# ---------------------------------------------------------------------------------------------
def ac1(root, tree):
    code, text = run_in(tree, [GEN.replace("/", os.sep), "--check"])
    first = (text.strip().splitlines() or ["(no output)"])[0]
    clause(code == 0, "G1 the generator's --check exits 0", "exit %d; %s" % (code, first[:150]))

    code, text = run_in(tree, ["-m", "pytest", TEST, "-q", "-p", "no:cacheprovider", "--color=no"])
    passed = re.search(r"(\d+) passed", text)
    failed = re.search(r"(\d+) failed", text)
    names = re.findall(r"^FAILED (\S+)", text, re.M)
    n_passed = int(passed.group(1)) if passed else 0
    n_failed = int(failed.group(1)) if failed else 0
    clause(code == 0 and n_failed == 0 and n_passed >= TESTS_AT_THE_CUT,
           "G2 the generator's test file passes whole",
           "exit %d; passed %d (at the cut %d tests); failed %d %s" % (code, n_passed, TESTS_AT_THE_CUT, n_failed, names))

    base_text, why = read_base(root, BASE_AT_THE_CUT, MOD)
    now_text = read_tree(tree, MOD)
    if base_text is None or now_text is None:
        clause(False, "G3 the prefix values of the cut are unchanged", why or "%s cannot be read" % MOD)
        return
    base = dict((k, v) for k, v in constants_of(base_text).items() if k != HASH_NAME)
    now = dict((k, v) for k, v in constants_of(now_text).items() if k != HASH_NAME)
    moved = []
    for name in sorted(base):
        same = now.get(name) == base[name]
        note("%s at the cut %r now %r %s" % (name, base[name], now.get(name), "EQUAL" if same else "CHANGED"))
        if not same:
            moved.append(name)
    clause(len(base) == 4 and not moved, "G3 the prefix values of the cut are byte-equal to the cut",
           "%d of %d equal; changed %s" % (len(base) - len(moved), len(base), moved))

    want, _root_prefix, why = builder_prefixes(tree)
    if want is None:
        clause(False, "G4 the generated module carries the builder's job-record prefix", "builder: %s" % why)
        return
    extra = sorted(set(now) - set(base) - set([NEW_NAME]))
    clause(now.get(NEW_NAME) == want and not extra and len(now) == len(base) + 1,
           "G4 the generated module carries the builder's job-record prefix and no other new constant",
           "%s is %r; builder %r; constants %d; unexpected %s" % (NEW_NAME, now.get(NEW_NAME), want, len(now), extra))

    try:
        spec = importlib.util.spec_from_file_location("r79_cc5_generator", os.path.join(tree, GEN.replace("/", os.sep)))
        gen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen)
        computed = gen.compute()
        detail = "compute() gives %r; builder %r; names %d" % (computed.get(NEW_NAME), want, len(computed))
        ok = computed.get(NEW_NAME) == want and computed == now
    except Exception as exc:  # noqa: BLE001 -- the reason is the finding
        ok, detail = False, "%s: %s" % (type(exc).__name__, exc)
    clause(ok, "G5 the generator computes the same prefix, and its constants are the module's", detail)


# ---------------------------------------------------------------------------------------------
def list_entries(text):
    """The quoted entries of the prefix list, in file order, or None when the list is not found."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^\s*%s\s*=\s*\[\s*$" % LIST_NAME, line):
            start = index
            break
    if start is None:
        return None
    entries = []
    for line in lines[start + 1:]:
        if re.match(r"^\s*\]\s*$", line):
            return entries
        hit = re.match(r'^\s*"([^"]*)"\s*,?\s*$', line)
        if hit:
            entries.append(hit.group(1))
    return None


def code_lines(text):
    """The file's lines that are not blank and not a whole-line comment, stripped."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            out.append(stripped)
    return out


def actions_of(lines):
    """Every quoted service:Action token on the code lines, counted."""
    found = collections.Counter()
    for line in lines:
        for token in re.findall(r'"([a-z0-9-]+:[A-Za-z*]+)"', line):
            found[token] += 1
    return found


def ac2(root, tree):
    base_text, why = read_base(root, BASE_AT_THE_CUT, TF)
    now_text = read_tree(tree, TF)
    if base_text is None or now_text is None:
        clause(False, "T0 the terraform file is read at the cut and now", why or "%s cannot be read" % TF)
        return
    base_list = list_entries(base_text)
    now_list = list_entries(now_text)
    if not clause(base_list is not None and now_list is not None and len(base_list) == ENTRIES_AT_THE_CUT,
                  "T0 the prefix list is found at the cut and now",
                  "at the cut %s entries (expected %d); now %s"
                  % (len(base_list) if base_list is not None else None, ENTRIES_AT_THE_CUT,
                     len(now_list) if now_list is not None else None)):
        return
    want, tier_root, why = builder_prefixes(tree)
    if want is None:
        clause(False, "T1 the list is the cut's list plus the builder's prefix", "builder: %s" % why)
        return

    kept = [entry for entry in now_list if entry in base_list]
    added = [entry for entry in now_list if entry not in base_list]
    gone = [entry for entry in base_list if entry not in now_list]
    clause(kept == base_list and added == [want] and len(now_list) == len(set(now_list)),
           "T1 the list is the cut's list in the cut's order plus exactly the builder's job-record prefix",
           "entries %d (at the cut %d); added %s; removed %s; builder %r" % (len(now_list), len(base_list), added, gone, want))
    clause(tier_root not in now_list and all(entry.endswith("/") for entry in added),
           "T2 the added entry ends in a slash and the whole state tier is not granted",
           "tier root %r in the list: %s" % (tier_root, tier_root in now_list))

    base_code = code_lines(base_text)
    now_code = code_lines(now_text)
    grant = [line for line in base_code if LIST_NAME in line and "for p in" in line]
    shaped = len(grant) == 2 and all(now_code.count(line) == 1 for line in grant)
    uses = [line for line in now_code if LIST_NAME in line]
    clause(shaped and len(uses) == 3,
           "T3 one object-read expression and one list-condition expression read the list, as at the cut",
           "expressions at the cut %d; each present once now %s; code lines naming the list %d (expected 3)"
           % (len(grant), shaped, len(uses)))

    base_actions = actions_of(base_code)
    now_actions = actions_of(now_code)
    more = sorted((now_actions - base_actions).elements())
    fewer = sorted((base_actions - now_actions).elements())
    clause(not more and not fewer, "T4 no action was added or removed anywhere in the file",
           "action tokens %d (at the cut %d); added %s; removed %s"
           % (sum(now_actions.values()), sum(base_actions.values()), more, fewer))

    entry_line = '"%s",' % want
    rest = list(now_code)
    if entry_line in rest:
        rest.remove(entry_line)
    typed = [line for line in rest if want in line or "job_record" in line]
    clause(rest == base_code and not typed,
           "T5 apart from the one list entry the file's code is the cut's; no other line names the new prefix",
           "code lines %d (at the cut %d); other lines naming it %d" % (len(now_code), len(base_code), len(typed)))


# ---------------------------------------------------------------------------------------------
def ac3(root, base):
    code, _out, err = git(root, "cat-file", "-e", "%s^{commit}" % base)
    if not clause(code == 0, "B0 the base commit is known to this repository", "%s rc=%d %s" % (base[:12], code, err[:100])):
        return
    _code, head, _err = git(root, "rev-parse", "HEAD")
    code, out, err = git(root, "diff", "--name-only", "%s..HEAD" % base, "--", *BOUND_PATHS)
    changed = [line.strip() for line in out.splitlines() if line.strip()]
    outside = [path for path in changed if path not in ALLOWED]
    clause(code == 0 and not outside,
           "B1 from the base to HEAD only the cell's four files changed under the harvest folder and the generated files",
           "base %s HEAD %s; changed %s; outside the cell %s %s" % (base[:10], head.strip()[:10], changed, outside, err[:80]))

    code, out, err = git(root, "status", "--porcelain", "--", *BOUND_PATHS)
    dirty = [line[3:].strip().strip('"') for line in out.splitlines() if line.strip()]
    outside = [path for path in dirty if path not in ALLOWED]
    clause(code == 0 and not outside,
           "B2 the working tree holds no uncommitted change outside the cell's four files in those places",
           "uncommitted %s; outside the cell %s %s" % (dirty, outside, err[:80]))

    code, out, _err = git(root, "diff", "--name-only", "%s..HEAD" % base, "--", *NOT_THIS_CELLS)
    registry = [line.strip() for line in out.splitlines() if line.strip()]
    note("not graded: files changed from the base to HEAD under the naming registry and its builder: %d %s"
         % (len(registry), registry[:6]))


def main(argv=None):
    parser = argparse.ArgumentParser(description="AMGT_RESAPP round 79, cell AMGT-cc-5")
    parser.add_argument("--crit", required=True, choices=("AC1", "AC2", "AC3"))
    parser.add_argument("--base", default=BASE_AT_THE_CUT, help="AC3 only: the commit the cell started from")
    args = parser.parse_args(argv)
    root = repo_root()
    tree = os.environ.get("R79_CC5_TREE") or root
    if tree != root:
        note("reading files from %s; git is asked in %s" % (tree, root))
    if args.crit == "AC1":
        ac1(root, tree)
    elif args.crit == "AC2":
        ac2(root, tree)
    else:
        ac3(root, args.base)
    return verdict(args.crit)


if __name__ == "__main__":
    sys.exit(main())
