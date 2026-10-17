"""IRPT_DASHBD round 137, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the RE-PIN of the 49 Financial gold bundle's stale members (cell DB-f-2205).

  Why: the apply of the signed pair (TO-DB-f-2204) stopped at its dry run: the bundle's `trading_calendar.py` member is pinned at a commit that predates
  `first_trading_day_on_or_after`, so the transaction stage failed by name (AttributeError). A read of all 23 pins found two stale (`lib/trading_calendar.py`,
  `infra/logic/registry/systems.json`). The round-136 closure check graded import NAMES; this one grades CONTENT.

  DBF137-1-AC1  every staged member of the entry `irpt-49f-reporting-gold-lambda` is CURRENT: its sha256 equals the file's sha256 now, its pin is a full commit that is an
                ancestor of HEAD, and the file at that commit hashes to the same sha256; the entry's files, staged pairs and other keys are the cut's
  DBF137-1-AC2  the ATTRIBUTE CLOSURE: every `member.attr` the handler and the transaction producer read from a bundle member (and every name they import from one) is defined
                at the top level of that member's PINNED blob

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

# NFRA_CTLPLN round 30 (TO-CT-cg-1): the function map is one JSON file per function; the entry is read through
# lib/opal_lambda_map.py (load_entry raises, naming the file, when it is absent).
FOLDER_REL = "infra/aws/lambda/ci/function-map"
LIB_REL = "lib/opal_lambda_map.py"
BASE ="org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/sourcemap_entry_r137_base.json"
ENTRY = "irpt-49f-reporting-gold-lambda"
CONSUMERS = ("infra/aws/lambda/investor-reporting/reporting-gold/handler.py", "data/assets/scripts/gold/irpt_reporting/account_transaction.py")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(root, *args):
    return subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, timeout=120)


def blob_at(root, pin, path):
    r = git(root, "show", "%s:%s" % (pin, path))
    return r.stdout if r.returncode == 0 else None


def top_level_names(source):
    """The names a module defines or binds at its top level (defs, classes, assignments, imports)."""
    names = set()
    for n in ast.parse(source).body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                for x in ast.walk(t):
                    if isinstance(x, ast.Name):
                        names.add(x.id)
        elif isinstance(n, ast.Import):
            names |= {(a.asname or a.name).split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            names |= {a.asname or a.name for a in n.names}
        elif isinstance(n, (ast.Try, ast.If, ast.With)):
            for x in ast.walk(n):
                if isinstance(x, (ast.FunctionDef, ast.ClassDef)):
                    names.add(x.name)
                elif isinstance(x, ast.Assign):
                    for t in x.targets:
                        if isinstance(t, ast.Name):
                            names.add(t.id)
                elif isinstance(x, ast.Import):
                    names |= {(a.asname or a.name).split(".")[0] for a in x.names}
                elif isinstance(x, ast.ImportFrom):
                    names |= {a.asname or a.name for a in x.names}
    return names


def wanted_attributes(source, member_modules):
    """{module: {attr, ...}} the consumer reads: `alias.attr` loads where alias is bound by `import module [as alias]`, and names in `from module import a, b`."""
    tree = ast.parse(source)
    alias = {}
    out = {m: set() for m in member_modules}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                base = a.name.split(".")[0]
                if base in member_modules:
                    alias[a.asname or base] = base
        elif isinstance(n, ast.ImportFrom) and n.module and n.module.split(".")[0] in member_modules:
            out[n.module.split(".")[0]] |= {a.name for a in n.names if a.name != "*"}
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in alias:
            out[alias[n.value.id]].add(n.attr)
    return {m: v for m, v in out.items() if v}


def map_lib(root):
    """lib/opal_lambda_map.py of the checked-out repository at root: the one reader of the function-map folder."""
    need(Path(root, LIB_REL).is_file(), "missing " + LIB_REL)
    spec = importlib.util.spec_from_file_location("opal_lambda_map_p137", str(Path(root, LIB_REL)))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load(root):
    entry = map_lib(root).load_entry(ENTRY, root=str(root))   # raises FileNotFoundError naming the path when absent
    need(isinstance(entry, dict), "no entry " + ENTRY + " in " + FOLDER_REL)
    bp = Path(root, BASE)
    need(bp.is_file(), "missing the cut's base shape " + BASE)
    return entry, json.loads(bp.read_text(encoding="utf-8"))


def ac1(root):
    entry, base = load(root)
    pr = []
    if entry.get("files") != base["files"]:
        pr.append("the entry's files must be the cut's %d paths, unchanged" % len(base["files"]))
    got = [[s.get("repo_path"), s.get("packaged_as")] for s in entry.get("staged_from", [])]
    if got != base["staged_from"]:
        pr.append("the entry's staged (repo_path, packaged_as) pairs must be the cut's %d, unchanged" % len(base["staged_from"]))
    if sorted(k for k in entry if k not in ("files", "staged_from")) != base["other_keys"]:
        pr.append("the entry's other keys must be the cut's")
    need(not pr, "; ".join(pr))
    stale = []
    for s in entry["staged_from"]:
        p = s["repo_path"]
        f = Path(root, p)
        if not f.is_file():
            stale.append("%s: file missing" % p)
            continue
        now = sha(f.read_bytes())
        if set(s) != {"repo_path", "pin", "packaged_as", "sha256"}:
            stale.append("%s: keys differ from {repo_path, pin, packaged_as, sha256}" % p)
        elif s["sha256"] != now:
            stale.append("%s: STALE (the pinned sha256 is not the file's sha256 now)" % p)
        elif not (len(s["pin"]) == 40 and all(c in "0123456789abcdef" for c in s["pin"])):
            stale.append("%s: pin is not a full commit hash" % p)
        else:
            b = blob_at(root, s["pin"], p)
            if b is None or sha(b) != now:
                stale.append("%s: the file at the pin commit does not hash to the pinned sha256" % p)
            elif git(root, "merge-base", "--is-ancestor", s["pin"], "HEAD").returncode != 0:
                stale.append("%s: the pin is not an ancestor of HEAD" % p)
    need(not stale, "; ".join(stale[:6]) + (" (and %d more)" % (len(stale) - 6) if len(stale) > 6 else ""))


def ac2(root):
    entry, _base = load(root)
    members = {Path(s["packaged_as"]).stem: s for s in entry["staged_from"] if s["packaged_as"].endswith(".py")}
    pr = []
    for rel in CONSUMERS:
        src = Path(root, rel).read_text(encoding="utf-8")
        for mod, attrs in wanted_attributes(src, set(members)).items():
            s = members[mod]
            blob = blob_at(root, s["pin"], s["repo_path"])
            if blob is None:
                pr.append("%s: the pinned blob of %s cannot be read" % (Path(rel).name, mod))
                continue
            have = top_level_names(blob.decode("utf-8"))
            for a in sorted(attrs - have):
                pr.append("%s reads %s.%s, which the pinned %s (pin %s) does not define" % (Path(rel).name, mod, a, mod, s["pin"][:10]))
    need(not pr, "; ".join(pr[:6]))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    src = "import trading_calendar as tc\nimport json\nfrom opal_naming import lookup, address\nx = tc.first_trading_day_on_or_after(1)\ny = tc.is_trading_day(2)\njson.loads('1')\n"
    arm("wanted", wanted_attributes(src, {"trading_calendar", "opal_naming"}), {"trading_calendar": {"first_trading_day_on_or_after", "is_trading_day"}, "opal_naming": {"lookup", "address"}})
    mod = "import os\nfrom x import y\nA = 1\ndef f():\n    pass\nclass C:\n    pass\ntry:\n    import z as zz\nexcept Exception:\n    zz = None\nif A:\n    B = 2\n"
    arm("top-level-names", top_level_names(mod) >= {"os", "y", "A", "f", "C", "zz", "B"}, True)
    arm("missing-attr-found", {"first_trading_day_on_or_after"} - top_level_names("def is_trading_day(d):\n    return True\n"), {"first_trading_day_on_or_after"})
    arm("sha", len(sha(b"x")), 64)
    arm("blob-absent", blob_at(".", "0" * 40, "x"), None)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF137-1-AC1": ac1, "DBF137-1-AC2": ac2}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
