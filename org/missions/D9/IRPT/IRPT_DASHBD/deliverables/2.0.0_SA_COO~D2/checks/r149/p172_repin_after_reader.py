"""IRPT_DASHBD round 149, workstream REPIN2 (issuer 2.0.0_SA_COO~D2) -- DB-b-304, the RE-PIN of three function entries after the one drain of cells DB-b-292 to DB-b-296: the Cottonwood publish function
(`irpt-cot-reporting-publish-lambda`: the publisher and the series contract changed), the 49 Financial gold function (`irpt-49f-reporting-gold-lambda`: the producer and the class module changed) and the Cottonwood
landing function (`irpt-cot-account-return-daily-lambda`: the adapter changed, the landing handler is its source_dir). Every staged member whose file at HEAD no longer has its pinned sha256 gets a new pin (the commit that
last changed it, an ancestor of HEAD) and the new sha256; every other key, entry and member stays byte for byte, the deployed fields included. The build-only package of each entry equals its sources. LOCAL: one JSON
file and a facts record; nothing is uploaded, built for upload or deployed.

  DB-b-304 (~240)   infra/aws/lambda/ci/lambda-source-map.json (three entries' staged_from) + a facts record
                    DB172-1-AC1 (each entry differs from the base only in its stale members' pins; every member of the three is fresh),
                    DB172-1-AC2 (the build-only package of each entry equals its sources and imports only pyarrow plus the runtime's),
                    DB172-1-AC3 (the facts record equals the recount; the grant)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import base64
import copy
import importlib.util
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~244"
REC_REL = D + AUTHOR + "/RD_REPIN_THREE_FACTS_R149B.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-304.repin-three-entries-after-the-reader-and-the-first-row.md"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRIES = ["irpt-cot-account-return-daily-lambda", "irpt-49f-reporting-publish-lambda", "irpt-cot-reporting-publish-lambda"]
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


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


HEX40, HEX64 = re.compile(r"[0-9a-f]{40}$"), re.compile(r"[0-9a-f]{64}$")


def check_repin_entry(key, be, ne, head_blob, pin_blob, pin_ok, sha):
    """p158's check_repin for ONE entry, except that a member keeps its OWN packaged_as (a staged file may be packaged under another name)."""
    need({k: v for k, v in be.items() if k != "staged_from"} == {k: v for k, v in ne.items() if k != "staged_from"}, "%s: the entry changed beyond staged_from (the deployed fields must be untouched)" % key)
    bs, ns = be["staged_from"], ne["staged_from"]
    need([s["repo_path"] for s in bs] == [s["repo_path"] for s in ns], "%s: staged_from must list the same members in the same order" % key)
    moved = []
    for b, n in zip(bs, ns):
        need(set(n) == {"repo_path", "pin", "packaged_as", "sha256"} and n["packaged_as"] == b["packaged_as"] and n["repo_path"] == b["repo_path"], "%s: member form: %s" % (key, n.get("repo_path")))
        need(isinstance(n["pin"], str) and HEX40.match(n["pin"]) and isinstance(n["sha256"], str) and HEX64.match(n["sha256"]), "%s: pin or sha256 form: %s" % (key, n["repo_path"]))
        need(pin_ok(n["pin"]), "%s: pin of %s is not an ancestor commit" % (key, n["repo_path"]))
        need(sha(pin_blob(n["pin"], n["repo_path"])) == n["sha256"] == sha(head_blob(n["repo_path"])), "%s: sha256 of %s differs from git show pin:path or from the file at HEAD" % (key, n["repo_path"]))
        if b["sha256"] == sha(head_blob(b["repo_path"])):
            need(n == b, "%s: member %s is not stale and must stay byte-identical" % (key, b["repo_path"]))
        else:
            need(n["pin"] != b["pin"] and n["sha256"] != b["sha256"], "%s: stale member %s must get a new pin and sha256" % (key, b["repo_path"]))
            moved.append(b["repo_path"])
    return moved


def check_all_entries(p158, base_map, new_map, head_blob, pin_blob, pin_ok):
    """The p158 re-pin clause applied to each of the three entries in turn; every OTHER entry must equal the base."""
    for k in set(base_map["functions"]) | set(new_map["functions"]):
        if k not in ENTRIES:
            need(base_map["functions"].get(k) == new_map["functions"].get(k), "an entry outside the order changed: %s" % k)
    for k in set(base_map) | set(new_map):
        if k != "functions":
            need(base_map.get(k) == new_map.get(k), "a top-level key changed: %s" % k)
    moved = {}
    for key in ENTRIES:
        need(key in base_map["functions"] and key in new_map["functions"], "entry %s is missing" % key)
        import hashlib
        moved[key] = check_repin_entry(key, base_map["functions"][key], new_map["functions"][key], head_blob, pin_blob, pin_ok, lambda b: hashlib.sha256(b).hexdigest())
    return moved


def check_layer_imports(p149, third_party):
    """The bundle's third-party imports (besides boto3/botocore) are only pyarrow and pandas, and the layer holds each (the 49 Financial gold function imports pandas; p149's clause allowed pyarrow alone)."""
    extra = set(third_party) - p149.RUNTIME_PROVIDED
    need(extra <= {"pyarrow", "pandas"}, "the bundle's third-party imports must be pyarrow and pandas only, read %s" % sorted(extra))
    names = p149.layer_names(p149.latest_layer_version())
    for pkg in sorted(extra):
        need("python/%s/__init__.py" % pkg in names, "the layer zip does not hold python/%s/__init__.py" % pkg)
    return True


def check_fresh(entry, head_blob, sha):
    stale = [s["repo_path"] for s in entry["staged_from"] if sha(head_blob(s["repo_path"])) != s["sha256"]]
    need(not stale, "stale members remain: %s" % stale[:3])
    return True


def check_facts(rec, moved, unchanged, b64s):
    exp = {"entries", "repinned", "unchanged_members", "build_only_sha256_b64", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["entries"] == ENTRIES, "entries differ")
    need(isinstance(rec["repinned"], dict) and {k: sorted(v) for k, v in rec["repinned"].items()} == {k: sorted(v) for k, v in moved.items()}, "repinned differs from the recount")
    need(rec["unchanged_members"] == unchanged, "unchanged_members differ from the recount %s" % unchanged)
    need(rec["build_only_sha256_b64"] == b64s, "build_only_sha256_b64 differs from the checker's own builds")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def check_grant(changed):
    bad = [f for f in changed if f != SOURCE_MAP_REL and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(SOURCE_MAP_REL in changed, "the source map must change")
    return True


def run(root, cid):
    import hashlib
    root = Path(root)
    p158 = helper("r148/p158_repin.py", "p158_helper_165")
    p160 = helper("r149/p160_pub49f.py", "p160_helper_165")
    p149 = helper("r147/p149_pubroot.py", "p149_helper_165")
    sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
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
    moved = check_all_entries(p158, bm, nm, head_blob, pin_blob, pin_ok)
    for key in ENTRIES:
        check_fresh(nm["functions"][key], head_blob, sha)
    if cid == "DB172-1-AC1":
        print("OK: the three entries differ from the base only in their stale members' pins and sha256 (%s); every member of the three now equals its pinned bytes and the file at HEAD; no other entry, key or deployed field moved" % ", ".join("%s %d" % (k.split("-lambda")[0], len(v)) for k, v in moved.items()))
        return True
    b64s = {}
    for key in ENTRIES:
        entry = nm["functions"][key]
        p160.ENTRY_KEY = key
        zpath = p160.build_only(root)
        sources = {f: p160.source_of(root, entry, f).read_text(encoding="utf-8") for f in entry["files"] if f.endswith(".py")}
        mods = {Path(f).stem for f in sources} | {"lib"}
        check_layer_imports(p149, p149.third_party(sources, mods))
        with zipfile.ZipFile(zpath) as z:
            p149.check_package([n for n in z.namelist() if not n.endswith("/")], entry["files"], lambda mem: z.read(mem), lambda mem: p160.source_of(root, entry, mem).read_bytes())
            b64s[key] = base64.b64encode(hashlib.sha256(Path(zpath).read_bytes()).digest()).decode("ascii")
    if cid == "DB172-1-AC2":
        print("OK: the build-only package of each of the three entries equals its sources byte for byte and imports only pyarrow plus the runtime's")
        return True
    if cid == "DB172-1-AC3":
        unchanged = {k: len(nm["functions"][k]["staged_from"]) - len(moved[k]) for k in ENTRIES}
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        # the builds are deterministic, so the recount must equal what the worker recorded
        check_facts(rec, moved, unchanged, b64s)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm)[0].decode().split())
        check_grant(changed)
        print("OK: the facts record equals the recount (re-pinned members, unchanged counts, the three build-only hashes); %d files changed, all in the grant" % len(changed))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    moved = {ENTRIES[0]: ["a"], ENTRIES[1]: ["b", "c"], ENTRIES[2]: []}
    unchanged = {ENTRIES[0]: 5, ENTRIES[1]: 6, ENTRIES[2]: 3}
    b64s = {k: "h" for k in ENTRIES}
    rec = {"entries": list(ENTRIES), "repinned": moved, "unchanged_members": unchanged, "build_only_sha256_b64": b64s, "words": "w" * 100}
    assert check_facts(rec, moved, unchanged, b64s)
    farms = (("entries", lambda r: r.update(entries=ENTRIES[:2])), ("repinned", lambda r: r["repinned"].update({ENTRIES[0]: []})), ("unchanged", lambda r: r["unchanged_members"].update({ENTRIES[0]: 1})),
             ("hash", lambda r: r["build_only_sha256_b64"].update({ENTRIES[1]: "x"})), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, moved, unchanged, b64s), label)
    assert check_grant({SOURCE_MAP_REL, D + AUTHOR + "/x.json"})
    red(lambda: check_grant({D + AUTHOR + "/x.json"}), "no source map")
    red(lambda: check_grant({SOURCE_MAP_REL, "lib/x.py"}), "outside grant")
    pins = {"o": "a" * 40, "n": "b" * 40}
    sh = lambda b: {b"old": "1" * 64, b"new": "2" * 64, b"same": "3" * 64}[b]  # noqa: E731

    def mem(path, pin, content, packaged=None):
        return {"repo_path": path, "pin": pins[pin], "packaged_as": packaged or path, "sha256": sh(content)}
    be = {"artifact_sha256": "x", "staged_from": [mem("a", "o", b"old", "pk/a"), mem("b", "o", b"same")]}
    ne = {"artifact_sha256": "x", "staged_from": [mem("a", "n", b"new", "pk/a"), mem("b", "o", b"same")]}
    head = {"a": b"new", "b": b"same"}
    pb = lambda pin, path: head[path]  # noqa: E731
    assert check_repin_entry("k", be, ne, lambda p: head[p], pb, lambda pin: True, sh) == ["a"]
    for label, fn in (("deployed field", lambda e: e.update(artifact_sha256="y")), ("order", lambda e: e["staged_from"].reverse()), ("packaged_as moved", lambda e: e["staged_from"][0].update(packaged_as="zz")),
                      ("fresh member touched", lambda e: e["staged_from"][1].update(pin=pins["n"])), ("stale kept", lambda e: e["staged_from"].__setitem__(0, dict(be["staged_from"][0]))),
                      ("bad sha", lambda e: e["staged_from"][0].update(sha256="9" * 64))):
        e2 = copy.deepcopy(ne)
        fn(e2)
        red(lambda: check_repin_entry("k", be, e2, lambda p: head[p], pb, lambda pin: True, sh), label)
    red(lambda: check_repin_entry("k", be, ne, lambda p: head[p], pb, lambda pin: False, sh), "pin not an ancestor")
    entry = {"staged_from": [{"repo_path": "a", "sha256": "1"}, {"repo_path": "b", "sha256": "2"}]}
    class P149:
        RUNTIME_PROVIDED = {"boto3", "botocore"}
        layer_names = staticmethod(lambda v: {"python/pyarrow/__init__.py", "python/pandas/__init__.py"})
        latest_layer_version = staticmethod(lambda: 1)
    assert check_layer_imports(P149, ["boto3", "pandas", "pyarrow"]) and check_layer_imports(P149, ["pyarrow"])
    red(lambda: check_layer_imports(P149, ["pyarrow", "requests"]), "a foreign import")

    class P149Thin(P149):
        layer_names = staticmethod(lambda v: {"python/pyarrow/__init__.py"})
    red(lambda: check_layer_imports(P149Thin, ["pandas", "pyarrow"]), "the layer lacks pandas")
    assert check_fresh(entry, lambda p: {"a": b"x", "b": b"y"}[p], lambda b: {b"x": "1", b"y": "2"}[b])
    red(lambda: check_fresh(entry, lambda p: {"a": b"x", "b": b"z"}[p], lambda b: {b"x": "1", b"z": "9"}[b]), "a stale member remains")
    print("selftest: facts (%d red arms), grant (2) and freshness (1) clauses behave; the entry clause is the proven p158 check_repin applied to each entry" % len(farms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
