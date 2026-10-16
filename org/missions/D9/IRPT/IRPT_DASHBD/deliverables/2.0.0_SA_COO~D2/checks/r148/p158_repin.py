"""IRPT_DASHBD round 149, workstream PUBWRITE (issuer 2.0.0_SA_COO~D2) -- DB-b-290, the RE-PIN of the Cottonwood publish function's source-map entry `irpt-cot-reporting-publish-lambda` after the writer drain
(`ff6c0633a7`): four staged members changed since the entry was pinned (the publisher, the series contract, and two registry files other seats edited), so the entry's pins no longer equal the files and the bundle
would not be what the pins say. Only those members' `pin` and `sha256` move; the entry's other keys (including the deployed `artifact_sha256`, `last_deployed_commit`, `recorded_by`) and every other entry stay
byte-identical. The build-only package is rebuilt and its UNPACKED handler passes DB155-1-AC2's behaviour on a fake S3. LOCAL: one JSON file (the source map) and a facts record; nothing is uploaded or deployed.

  DB-b-290 (~234)   infra/aws/lambda/ci/lambda-source-map.json (the one entry's staged_from) + a facts record
                    DB158-1-AC1 (the entry differs from the base ONLY in the stale members' pins; every pin is an ancestor with the file's sha256),
                    DB158-1-AC2 (the build-only package equals its sources, its imports are pyarrow plus the runtime's, and the unpacked handler passes the writer's behaviour check),
                    DB158-1-AC3 (the facts record equals the recount)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~234"
REC_REL = D + AUTHOR + "/RD_PUBLISH_REPIN_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-290.publish-source-map-repin-after-the-writer-drain.md"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRY_KEY = "irpt-cot-reporting-publish-lambda"
SOURCE_DIR = "infra/aws/lambda/investor-reporting/reporting-publish-cot"
HEX40, HEX64 = re.compile(r"[0-9a-f]{40}$"), re.compile(r"[0-9a-f]{64}$")
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout, r.returncode


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.decode().split()[-1]


def own_commits(root):
    out, _ = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD")
    need(out.split(), "no commit by %s since the order was issued" % AUTHOR)
    return out.decode().split()


def p149():
    spec = importlib.util.spec_from_file_location("p149_helper", str(HERE.parent / "r147" / "p149_pubroot.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p149_helper"] = mod
    spec.loader.exec_module(mod)
    return mod


def p155():
    spec = importlib.util.spec_from_file_location("p155_helper", str(HERE / "p155_claimcal.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p155_helper"] = mod
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_repin(base_map, new_map, head_blob, pin_blob, pin_ok):
    for k in set(base_map) | set(new_map):
        if k != "functions":
            need(base_map.get(k) == new_map.get(k), "a top-level key changed: %s" % k)
    bf, nf = base_map["functions"], new_map["functions"]
    need(set(bf) == set(nf), "the set of entries changed")
    for k in bf:
        if k != ENTRY_KEY:
            need(bf[k] == nf[k], "another entry changed: %s" % k)
    be, ne = bf[ENTRY_KEY], nf[ENTRY_KEY]
    need({k: v for k, v in be.items() if k != "staged_from"} == {k: v for k, v in ne.items() if k != "staged_from"}, "the entry changed beyond staged_from (the deployed artifact_sha256, last_deployed_commit and recorded_by must be untouched)")
    bs, ns = be["staged_from"], ne["staged_from"]
    need([s["repo_path"] for s in bs] == [s["repo_path"] for s in ns] and len(ns) == len(bs), "staged_from must list the same members in the same order")
    moved = []
    for b, n in zip(bs, ns):
        need(set(n) == {"repo_path", "pin", "packaged_as", "sha256"} and n["packaged_as"] == n["repo_path"] == b["repo_path"], "member form: %s" % n.get("repo_path"))
        need(isinstance(n["pin"], str) and HEX40.match(n["pin"]) and isinstance(n["sha256"], str) and HEX64.match(n["sha256"]), "pin or sha256 form: %s" % n["repo_path"])
        need(pin_ok(n["pin"]), "pin of %s is not an ancestor commit" % n["repo_path"])
        need(sha(pin_blob(n["pin"], n["repo_path"])) == n["sha256"] == sha(head_blob(n["repo_path"])), "sha256 of %s differs from git show pin:path or from the file at HEAD" % n["repo_path"])
        if b["sha256"] == sha(head_blob(b["repo_path"])):
            need(n == b, "member %s is not stale and must stay byte-identical" % b["repo_path"])
        else:
            need(n["pin"] != b["pin"] and n["sha256"] != b["sha256"], "stale member %s must get a new pin and sha256" % b["repo_path"])
            moved.append(b["repo_path"])
    need(moved, "no member was re-pinned although the entry is stale")
    return moved


def check_facts(rec, moved, b64):
    exp = {"entry", "repinned", "unchanged_members", "build_only_sha256_b64", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["entry"] == ENTRY_KEY and sorted(rec["repinned"]) == sorted(moved), "entry or repinned differ from the recount")
    need(isinstance(rec["unchanged_members"], int) and not isinstance(rec["unchanged_members"], bool) and rec["unchanged_members"] >= 1, "unchanged_members: a whole number")
    need(rec["build_only_sha256_b64"] == b64, "build_only_sha256_b64 differs from the checker's own build")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run(root, cid):
    root = Path(root)
    h = p149()
    bm = json.loads(git(root, "show", "%s:%s" % (base_commit(root), SOURCE_MAP_REL))[0].decode("utf-8"))
    nm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))

    def head_blob(p):
        return (root / p).read_bytes()

    def pin_blob(pin, p):
        out, rc = git(root, "show", "%s:%s" % (pin, p))
        need(rc == 0, "git show %s:%s failed" % (pin[:10], p))
        return out

    def pin_ok(pin):
        return git(root, "merge-base", "--is-ancestor", pin, "HEAD")[1] == 0
    if cid == "DB158-1-AC1":
        moved = check_repin(bm, nm, head_blob, pin_blob, pin_ok)
        print("OK: the entry %s differs from the base only in %d stale member pins (%s); every pin is an ancestor commit whose file bytes equal the sha256 and the file at HEAD; no other entry or key moved" % (ENTRY_KEY, len(moved), ", ".join(Path(m).name for m in moved)))
        return True
    sm = nm["functions"][ENTRY_KEY]
    env = dict(os.environ, BUILD_ONLY="1")
    r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", ENTRY_KEY], cwd=str(root), env=env, capture_output=True, text=True, timeout=300)
    m = re.search(r"BUILD_ONLY:\s*(\S+)\s+sha256=(\S+)", r.stdout + r.stderr)
    need(r.returncode == 0 and m is not None, "the build-only run failed (rc %s): %s" % (r.returncode, (r.stdout + r.stderr)[-300:].replace("\n", " | ")))
    zpath = m.group(1)
    if zpath.startswith("/"):
        cp = subprocess.run(["cygpath", "-w", zpath], capture_output=True, text=True)
        need(cp.returncode == 0, "cygpath could not resolve %s" % zpath)
        zpath = cp.stdout.strip()
    if cid == "DB158-1-AC2":
        sources = {f: (root / ((SOURCE_DIR + "/" + f) if f == "handler.py" else f)).read_text(encoding="utf-8") for f in sm["files"] if f.endswith(".py")}
        mods = {Path(f).stem for f in sources} | {"lib"}
        h.check_imports(h.third_party(sources, mods), lambda n: n in h.layer_names(h.latest_layer_version()))
        tmp = Path(tempfile.mkdtemp(prefix="p158_pkg_"))
        try:
            with zipfile.ZipFile(zpath) as z:
                h.check_package([n for n in z.namelist() if not n.endswith("/")], sm["files"], lambda mem: z.read(mem), lambda mem: (root / ((SOURCE_DIR + "/" + mem) if mem == "handler.py" else mem)).read_bytes())
                z.extractall(tmp)
            w = p155()
            tc = w.p147().load_module(tmp / "lib" / "trading_calendar.py", "tc_unpacked_158")
            w.check_handler_run(tmp, tmp / "handler.py", tmp / "infra/aws/lambda/investor-reporting/reporting-publish/publisher.py", tc)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        print("OK: the build-only package of %d members equals its sources byte for byte, its third-party imports are pyarrow plus the runtime's (the layer holds it), and the UNPACKED handler passes the writer's behaviour on a fake S3 (income_claim, calendar_source, publisher 0.3.0, the guard)" % len(sm["files"]))
        return True
    if cid == "DB158-1-AC3":
        moved = check_repin(bm, nm, head_blob, pin_blob, pin_ok)
        b64 = __import__("base64").b64encode(bytes.fromhex(m.group(2))).decode("ascii") if re.fullmatch(r"[0-9a-f]{64}", m.group(2)) else m.group(2)
        check_facts(json.loads((root / REC_REL).read_text(encoding="utf-8")), moved, b64)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm)[0].decode().split())
        bad = [f for f in changed if f != SOURCE_MAP_REL and not f.startswith((D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/"))]
        need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
        print("OK: the facts record equals the recount (%d re-pinned members, the build-only hash); %d files changed, all in the grant" % (len(moved), len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    files = {"a.py": b"a1", "b.py": b"b1", "c.json": b"c1"}
    new_files = dict(files)
    new_files["a.py"] = b"a2"
    new_files["c.json"] = b"c2"
    pins_old = {"a.py": "%040x" % 1, "b.py": "%040x" % 2, "c.json": "%040x" % 3}
    pins_new = {"a.py": "%040x" % 4, "b.py": "%040x" % 2, "c.json": "%040x" % 5}
    hist = {(pins_old["a.py"], "a.py"): b"a1", (pins_old["b.py"], "b.py"): b"b1", (pins_old["c.json"], "c.json"): b"c1", (pins_new["a.py"], "a.py"): b"a2", (pins_new["b.py"], "b.py"): b"b1", (pins_new["c.json"], "c.json"): b"c2"}

    def entry(pins, fl):
        return {"files": ["handler.py", "a.py", "b.py", "c.json"], "artifact_sha256": "deployed", "recorded_by": "x", "staged_from": [{"repo_path": p, "pin": pins[p], "packaged_as": p, "sha256": sha(fl[p])} for p in ("a.py", "b.py", "c.json")]}
    bm = {"top": 1, "functions": {"other": {"x": 1}, ENTRY_KEY: entry(pins_old, files)}}
    nm = {"top": 1, "functions": {"other": {"x": 1}, ENTRY_KEY: entry(pins_new, new_files)}}

    def go(n, **kw):
        return check_repin(bm, n, kw.get("head", lambda p: new_files[p]), kw.get("pb", lambda pin, p: hist.get((pin, p), b"?")), kw.get("ok", lambda pin: True))
    assert sorted(go(nm)) == ["a.py", "c.json"]
    red(lambda: go(nm, ok=lambda pin: False), "pin ancestry")
    red(lambda: go(nm, pb=lambda pin, p: b"drift"), "pin content")
    red(lambda: go(nm, head=lambda p: b"moved"), "head differs")
    arms = (("other entry", lambda x: x["functions"]["other"].update(x=2)), ("top key", lambda x: x.update(top=2)), ("artifact sha", lambda x: x["functions"][ENTRY_KEY].update(artifact_sha256="new")),
            ("files", lambda x: x["functions"][ENTRY_KEY].update(files=["handler.py"])), ("member order", lambda x: x["functions"][ENTRY_KEY]["staged_from"].reverse()),
            ("fresh member moved", lambda x: x["functions"][ENTRY_KEY]["staged_from"][1].update(pin="%040x" % 9)), ("stale not moved", lambda x: x["functions"][ENTRY_KEY]["staged_from"].__setitem__(0, bm["functions"][ENTRY_KEY]["staged_from"][0])),
            ("null pin", lambda x: x["functions"][ENTRY_KEY]["staged_from"][0].update(pin=None)), ("extra key", lambda x: x["functions"][ENTRY_KEY]["staged_from"][0].update(z=1)), ("entry removed", lambda x: x["functions"].pop(ENTRY_KEY)))
    for label, fn in arms:
        x = copy.deepcopy(nm)
        fn(x)
        red(lambda: go(x), label)
    rec = {"entry": ENTRY_KEY, "repinned": ["a.py", "c.json"], "unchanged_members": 1, "build_only_sha256_b64": "b64", "words": "w" * 100}
    assert check_facts(rec, ["a.py", "c.json"], "b64")
    for label, fn in (("entry", lambda r: r.update(entry="x")), ("repinned", lambda r: r.update(repinned=["a.py"])), ("unchanged", lambda r: r.update(unchanged_members=0)), ("hash", lambda r: r.update(build_only_sha256_b64="z")),
                      ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, ["a.py", "c.json"], "b64"), label)
    print("selftest: repin (%d red arms + 3), facts (7 red arms) clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or build is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
