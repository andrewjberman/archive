"""IRPT_DASHBD round 136, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the 49 FINANCIAL GOLD LAMBDA'S BUNDLE gains the transaction producer (W2b).

  DB-f-2203 (~2203) the function-map folder `infra/aws/lambda/ci/function-map/` (one file per function; the retired single map was split by TO-CT-ca-1), the entry `irpt-49f-reporting-gold-lambda`: `files` gains `account_transaction.py` and `transaction_words.json` (the
                    two paths below, appended LAST, in that order) and `staged_from` gains the two matching pins (commit, sha256 of the file at that commit and now). Every other key of
                    the entry, and every other function of the file, is untouched. The producer's imports (account_return_daily, opal_naming, trading_calendar, pandas, pyarrow) are
                    already members or the layer. The pins of the members already in the entry are NOT re-pinned here (another lane's act); the build and the apply are the applier's.
                    DBF136-3-AC1 (the entry and the two pins), DBF136-3-AC2 (the import closure and the rest of the file)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import ast
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

# CT-ca-1 (NFRA_CTLPLN round 30): the map is one JSON file per function. The entry is read through lib/opal_lambda_map.py
# (load_entry raises when the file is absent); the metadata the retired map carried is stated by the folder's README.
FOLDER_REL = "infra/aws/lambda/ci/function-map"
LIB_REL = "lib/opal_lambda_map.py"
META_KEYS = ("_description", "_updated", "_note")
BASE = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/sourcemap_base_entry.json"
ENTRY = "irpt-49f-reporting-gold-lambda"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_transaction.py"
WORDS = "data/assets/scripts/gold/irpt_reporting/transaction_words.json"
NEW = [PRODUCER, WORDS]
LAYER_MODULES = {"pandas", "pyarrow", "numpy", "boto3", "botocore"}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_show(root, pin, path):
    run = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, path)], capture_output=True, timeout=120)
    return run.stdout if run.returncode == 0 else None


def entry_problems(entry, base):
    """The entry is the base plus the two members, LAST, in order; the other keys and the base members' paths are unchanged (their pins may move: another lane's act)."""
    pr = []
    if entry.get("files") != base["files"] + NEW:
        pr.append("files must be the base's %d paths and then %s, in that order" % (len(base["files"]), NEW))
    sf = entry.get("staged_from")
    if not isinstance(sf, list):
        return pr + ["staged_from must be a list"]
    got = [[s.get("repo_path"), s.get("packaged_as")] for s in sf if isinstance(s, dict)]
    if got != base["staged_from"] + [[p, p] for p in NEW]:
        pr.append("staged_from must be the base's %d (repo_path, packaged_as) pairs and then the two new members packaged at their own repo paths, in order" % len(base["staged_from"]))
    if sorted(k for k in entry if k not in ("files", "staged_from")) != base["other_keys"]:
        pr.append("the entry's other keys must be the base's: %r" % (base["other_keys"],))
    for p in NEW:
        if p not in entry.get("files", []):
            pr.append("%s is missing from files" % p)
    return pr


def import_problems(source, members):
    """Every import of the producer is stdlib, the Lambda layer, or a bundle member (by module basename)."""
    pr = []
    mods = set()
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            mods.add(n.module.split(".")[0])
    names = {Path(m).stem for m in members}
    for m in sorted(mods):
        if m in sys.stdlib_module_names or m in LAYER_MODULES or m in names:
            continue
        pr.append("the producer imports %s, which is neither stdlib, the layer nor a bundle member" % m)
    return pr


def map_lib(root):
    """lib/opal_lambda_map.py of the checked-out repository at root: the one reader of the function-map folder."""
    need(Path(root, LIB_REL).is_file(), "missing " + LIB_REL)
    spec = importlib.util.spec_from_file_location("opal_lambda_map_p136", str(Path(root, LIB_REL)))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def readme_keys(root):
    """The metadata keys the folder's README states (one '- `key`: ' line each)."""
    text = Path(root, FOLDER_REL, "README.md").read_bytes().decode("utf-8")
    return set(re.findall(r"^- `(_[a-z_]+)`: ", text, re.M))


def load(root):
    try:
        entry = map_lib(root).load_entry(ENTRY, root=str(root))
    except FileNotFoundError as e:
        raise Fail(str(e))
    need(isinstance(entry, dict), "the function map has no entry " + ENTRY)
    bp = Path(root, BASE)
    need(bp.is_file(), "missing the pinned base entry " + BASE)
    return entry, json.loads(bp.read_text(encoding="utf-8"))


def ac1(root):
    entry, base = load(root)
    pr = entry_problems(entry, base)
    need(not pr, "; ".join(pr))
    pins = {s["repo_path"]: s for s in entry["staged_from"][-2:]}
    for p in NEW:
        s = pins[p]
        need(set(s) == {"repo_path", "pin", "packaged_as", "sha256"}, "%s pin must carry exactly repo_path, pin, packaged_as, sha256" % p)
        now = Path(root, p).read_bytes()
        need(s["sha256"] == sha(now), "%s: the pin's sha256 is not the file's sha256 now" % p)
        need(len(s["pin"]) == 40 and all(c in "0123456789abcdef" for c in s["pin"]), "%s: pin must be a full commit hash" % p)
        blob = git_show(root, s["pin"], p)
        need(blob is not None, "%s: the file does not exist at the pin commit %s" % (p, s["pin"][:10]))
        need(sha(blob) == s["sha256"], "%s: the file at the pin commit hashes differently from the pin's sha256" % p)


def ac2(root):
    entry, _base = load(root)
    need(PRODUCER in entry["files"] and WORDS in entry["files"], "the entry's files must hold the producer and its words file (the closure is graded over the entry)")
    src = Path(root, PRODUCER).read_text(encoding="utf-8")
    pr = import_problems(src, entry["files"])
    need(not pr, "; ".join(pr))
    listed = readme_keys(root)
    need(all(k in listed for k in META_KEYS), "a metadata key of the function map is missing from its README: %s" % [k for k in META_KEYS if k not in listed])
    need(Path(root, FOLDER_REL, ENTRY + ".json").read_bytes().decode("utf-8").isascii(), "the function file of the entry must stay ASCII")


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    base = {"files": ["h.py", "a.py"], "staged_from": [["a.py", "a.py"]], "other_keys": ["source_dir"]}
    good = {"files": ["h.py", "a.py"] + NEW, "staged_from": [{"repo_path": "a.py", "packaged_as": "a.py", "pin": "x", "sha256": "y"}] +
            [{"repo_path": p, "packaged_as": p, "pin": "x", "sha256": "y"} for p in NEW], "source_dir": "d"}
    arm("entry-green", entry_problems(good, base), [])
    arm("entry-order", len(entry_problems(dict(good, files=["h.py", "a.py", NEW[1], NEW[0]]), base)), 1)
    arm("entry-extra-key", len(entry_problems(dict(good, extra=1), base)), 1)
    arm("entry-pair", len(entry_problems(dict(good, staged_from=good["staged_from"][:2]), base)), 1)
    arm("imports-green", import_problems("import json\nimport pandas\nimport a\n", ["a.py"]), [])
    arm("imports-red", len(import_problems("import requests\n", ["a.py"])), 1)
    arm("git-show-absent", git_show(".", "0" * 40, "x"), None)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF136-3-AC1": ac1, "DBF136-3-AC2": ac2}
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
