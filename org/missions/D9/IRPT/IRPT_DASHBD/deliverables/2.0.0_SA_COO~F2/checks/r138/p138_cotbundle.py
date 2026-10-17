"""IRPT_DASHBD round 138, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the COTTONWOOD LANDING FUNCTION'S BUNDLE gains the transaction producer (cell DB-f-2606).

  The function-map file `infra/aws/lambda/ci/function-map/irpt-cot-account-return-daily-lambda.json`: `files` gains the five paths in NEW (appended LAST, in that order) and `staged_from`
  gains the five matching pins (commit, sha256 of the file at that commit and now), each packaged at its own repo path. The producer chain (account_transaction_cottonwood ->
  account_transaction -> account_return_daily -> stream_parquet, and the words file beside the producer) was read by import. Every other key of the entry and every other file of the
  folder is untouched. The 15 existing pins MAY move (a re-pin where a new member needs a newer attribute of an existing one: the lesson of the 49 Financial apply's STOP) but no
  member leaves and none is added beyond NEW. The build, the upload and the apply are the applier's.
  DBF138-6-AC1 (the entry and the five pins), DBF138-6-AC2 (the ATTRIBUTE CLOSURE over the pinned blobs), DBF138-6-AC3 (the BUNDLE SMOKE: the handler imports the producer in the bundle layout)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

R136 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/"
BASE = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r138/cotbundle_base_entry.json"
LIB_REL = "lib/opal_lambda_map.py"
ENTRY = "irpt-cot-account-return-daily-lambda"
HANDLER_REL = "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
D = "data/assets/scripts/gold/irpt_reporting/"
NEW = [D + "account_transaction_cottonwood.py", D + "account_transaction.py", D + "account_return_daily.py", D + "transaction_words.json",
       "data/assets/scripts/lib/stream_parquet.py"]
PIN_KEYS = {"repo_path", "pin", "packaged_as", "sha256"}


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


def _load_repin():
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("p137_repin_for_cot", str(here.parent / "r136" / "p137_repin.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RP = _load_repin()


def entry_problems(entry, base):
    """The entry is the base plus the NEW members, LAST, in order; the other keys and the base members' paths are unchanged (the base members' pins may move)."""
    pr = []
    if entry.get("files") != base["files"] + NEW:
        pr.append("files must be the base's %d paths and then the %d new ones, in that order" % (len(base["files"]), len(NEW)))
    sf = entry.get("staged_from")
    if not isinstance(sf, list):
        return pr + ["staged_from must be a list"]
    got = [[s.get("repo_path"), s.get("packaged_as")] for s in sf if isinstance(s, dict)]
    if got != base["staged_from"] + [[p, p] for p in NEW]:
        pr.append("staged_from must be the base's %d (repo_path, packaged_as) pairs and then the new members packaged at their own repo paths, in order" % len(base["staged_from"]))
    if sorted(k for k in entry if k not in ("files", "staged_from")) != base["other_keys"]:
        pr.append("the entry's other keys must be the base's: %r" % (base["other_keys"],))
    for s in sf:
        if isinstance(s, dict) and set(s) != PIN_KEYS:
            pr.append("a pin must carry exactly repo_path, pin, packaged_as, sha256 (%s)" % s.get("repo_path"))
    return pr


def load(root):
    lib = Path(root, LIB_REL)
    need(lib.is_file(), "missing " + LIB_REL)
    spec = importlib.util.spec_from_file_location("opal_lambda_map_p138", str(lib))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        entry = mod.load_entry(ENTRY, root=str(root))
    except FileNotFoundError as e:
        raise Fail(str(e))
    need(isinstance(entry, dict), "no entry " + ENTRY)
    bp = Path(root, BASE)
    need(bp.is_file(), "missing the pinned base entry " + BASE)
    return entry, json.loads(bp.read_text(encoding="utf-8"))


def ac1(root):
    entry, base = load(root)
    pr = entry_problems(entry, base)
    need(not pr, "; ".join(pr))
    for s in entry["staged_from"]:
        b = blob_at(root, s["pin"], s["repo_path"]) if len(s["pin"]) == 40 else None
        need(b is not None and sha(b) == s["sha256"], "%s: the file at its pin does not hash to the pin's sha256" % s["repo_path"])
    for p in NEW:
        s = next(x for x in entry["staged_from"] if x["repo_path"] == p)
        f = Path(root, p)
        need(f.is_file(), "%s: missing in the tree" % p)
        need(s["sha256"] == sha(f.read_bytes()), "%s: the pin's sha256 is not the file's sha256 now" % p)
        need(all(c in "0123456789abcdef" for c in s["pin"]), "%s: pin must be a full commit hash" % p)
        need(git(root, "merge-base", "--is-ancestor", s["pin"], "HEAD").returncode == 0, "%s: the pin is not an ancestor of HEAD" % p)


def consumers(entry):
    return [HANDLER_REL] + [p for p in NEW if p.endswith(".py")]


def ac2(root):
    entry, _base = load(root)
    members = {Path(s["packaged_as"]).stem: s for s in entry["staged_from"] if s["packaged_as"].endswith(".py")}
    pr = []
    for rel in consumers(entry):
        src = Path(root, rel).read_text(encoding="utf-8")
        for mod, attrs in RP.wanted_attributes(src, set(members)).items():
            s = members[mod]
            blob = blob_at(root, s["pin"], s["repo_path"])
            if blob is None:
                pr.append("%s: the pinned blob of %s cannot be read" % (Path(rel).name, mod))
                continue
            have = RP.top_level_names(blob.decode("utf-8"))
            for a in sorted(attrs - have):
                pr.append("%s reads %s.%s, which the pinned %s (pin %s) does not define" % (Path(rel).name, mod, a, mod, s["pin"][:10]))
    need(not pr, "; ".join(pr[:6]))


SMOKE = "import handler as h\nassert h.ATC_IMPORT_ERROR is None, h.ATC_IMPORT_ERROR\nassert callable(h.atc.normalize_trn) and callable(h.atc.emit_transaction_day)\nprint('SMOKE_OK')\n"


def lay_out(root, entry, dest):
    """The pinned members at their packaged paths and the source_dir handler, as the build packages them."""
    written = []
    for s in entry["staged_from"]:
        b = blob_at(root, s["pin"], s["repo_path"])
        need(b is not None, "the pinned blob of %s at %s cannot be read" % (s["repo_path"], s["pin"][:10]))
        t = Path(dest, s["packaged_as"])
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_bytes(b)
        written.append(s["packaged_as"])
    src_dir = Path(root, entry["source_dir"])
    for name in entry.get("files", []):
        if name in written:
            continue
        f = src_dir / name
        if f.is_file():
            Path(dest, name).parent.mkdir(parents=True, exist_ok=True)
            Path(dest, name).write_bytes(f.read_bytes())
            written.append(name)
    return written


def ac3(root):
    entry, _base = load(root)
    with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as other:
        bundle = Path(td, "var_task")
        bundle.mkdir()
        lay_out(root, entry, bundle)
        prog = "import sys\nsys.path.insert(0, %r)\n%s" % (str(bundle), SMOKE)
        r = subprocess.run([sys.executable, "-I", "-c", prog], capture_output=True, text=True, timeout=300, cwd=other)
        out = (r.stdout or "") + (r.stderr or "")
        need(r.returncode == 0 and "SMOKE_OK" in out, "the bundle smoke failed (rc %s): %s" % (r.returncode, out.strip()[-400:]))


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
    pin = lambda p: {"repo_path": p, "packaged_as": p, "pin": "x", "sha256": "y"}  # noqa: E731
    good = {"files": ["h.py", "a.py"] + NEW, "staged_from": [pin("a.py")] + [pin(p) for p in NEW], "source_dir": "d"}
    arm("entry-green", entry_problems(good, base), [])
    arm("entry-order", len(entry_problems(dict(good, files=["h.py", "a.py"] + NEW[::-1]), base)), 1)
    arm("entry-extra-key", len(entry_problems(dict(good, extra=1), base)), 1)
    arm("entry-missing-member", len(entry_problems(dict(good, staged_from=good["staged_from"][:-1]), base)), 1)
    arm("entry-bad-pin-keys", len(entry_problems(dict(good, staged_from=[dict(pin("a.py"), extra=1)] + good["staged_from"][1:]), base)), 1)
    arm("entry-base-member-dropped", len(entry_problems(dict(good, files=["h.py"] + NEW), base)) >= 1, True)
    arm("blob-absent", blob_at(".", "0" * 40, "x"), None)
    arm("smoke-text", "ATC_IMPORT_ERROR is None" in SMOKE and "SMOKE_OK" in SMOKE, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF138-6-AC1", "DBF138-6-AC2", "DBF138-6-AC3"):
        print("usage: p138_cotbundle.py <repo_root> DBF138-6-AC1|AC2|AC3 | --selftest")
        return 2
    try:
        {"DBF138-6-AC1": ac1, "DBF138-6-AC2": ac2, "DBF138-6-AC3": ac3}[argv[2]](argv[1])
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
