"""IRPT_DASHBD round 150, workstream RELEASE (issuer 2.0.0_SA_COO~D2) -- DB-b-334, the RE-PIN of the Cottonwood landing function entry for the ONE code release (the late-posting reader of
DB-b-333 and ~F2's late-window transaction stage of DB-f-2706 are both on the trunk). Every staged member of `irpt-cot-account-return-daily-lambda` whose file at HEAD no longer has its pinned
sha256 gets a new pin (the commit that last changed it, an ancestor of HEAD) and the new sha256; every other key of the entry, every other file of the function-map folder and the file's
members stay byte for byte, the deployed fields included. The build-only package equals its sources. WORLD by the path floor: one JSON file; nothing is built for upload, uploaded or deployed.

  DBR200-1-AC1  the entry differs from the base only in its stale members' pin and sha256, every member is fresh, and the worker's commits stay in the grant
  DBR200-2-AC1  ~F2's bundle and window criterion DBF139-6-AC3 passes on the worker's tree (it runs the function's tests and the bundle criteria DBF138-6-AC1 to AC3)
  DBR200-3-AC1  the build-only package equals the entry's sources byte for byte and imports only pyarrow and pandas plus the runtime's

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~260"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-334.cottonwood-release-repin-of-the-landing-entry.md"
ENTRY = "irpt-cot-account-return-daily-lambda"
ENTRY_REL = "infra/aws/lambda/ci/function-map/" + ENTRY + ".json"
F2_CHECK = HERE.parents[2] / "2.0.0_SA_COO~F2" / "checks" / "r139" / "p139_cotwindow.py"
F2_ID = "DBF139-6-AC3"
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


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


def check_grant(changed):
    bad = [f for f in changed if f != ENTRY_REL and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(ENTRY_REL in changed, "the entry file must change")
    return True


LAZY_OK = "opal_lambda_map"


def check_lazy_map_import(sources):
    """lib/opal_naming.py imports lib/opal_lambda_map.py INSIDE a generator-side function (`_lambda_source_map`, reached only by `lambda_plane_consumers`), which the bundle does not package. That is
    allowed only as that one function-local import: no other packaged source names the module or either function, and the import is indented (never at import time)."""
    for f, text in sources.items():
        if f.endswith("lib/opal_naming.py"):
            lines = [ln for ln in text.splitlines() if "import opal_lambda_map" in ln]
            need(lines and all(ln.startswith((" ", chr(9))) for ln in lines), "opal_naming.py must import opal_lambda_map only inside a function")
        else:
            need(LAZY_OK not in text and "_lambda_source_map" not in text and "lambda_plane_consumers" not in text, "%s reaches the unpackaged map reader" % f)
    return True


def check_imports(p149, p172, third_party, sources):
    """p172's layer clause, with the one named lazy import of the map reader set aside (and graded by check_lazy_map_import)."""
    rest = set(third_party) - {LAZY_OK}
    if LAZY_OK in third_party:
        check_lazy_map_import(sources)
    return p172.check_layer_imports(p149, rest)


def load_entry(root):
    return json.loads(Path(root, ENTRY_REL).read_bytes().decode("utf-8"))


def run(root, cid):
    root = Path(root)
    p172 = helper("r149/p172_repin_after_reader.py", "p172_helper_200")
    sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
    new = load_entry(root)

    def head_blob(p):
        return (root / p).read_bytes()

    def pin_blob(pin, p):
        out, rc = git(root, "show", "%s:%s" % (pin, p))
        need(rc == 0, "git show %s:%s failed" % (pin[:10], p))
        return out

    def pin_ok(pin):
        return git(root, "merge-base", "--is-ancestor", pin, "HEAD")[1] == 0
    if cid == "DBR200-1-AC1":
        p172.check_fresh(new, head_blob, sha)  # first: at the base this is the clause that fails
        base = json.loads(git(root, "show", "%s:%s" % (base_commit(root), ENTRY_REL))[0].decode("utf-8"))
        moved = p172.check_repin_entry(ENTRY, base, new, head_blob, pin_blob, pin_ok, sha)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm)[0].decode().split())
        check_grant(changed)
        print("OK: the entry differs from the base only in %d stale member(s) (%s); every member equals its pinned bytes and the file at HEAD; %d file(s) changed, all in the grant" % (len(moved), ", ".join(Path(m).name for m in moved), len(changed)))
        return True
    if cid == "DBR200-2-AC1":
        r = subprocess.run([sys.executable, "-I", str(F2_CHECK), str(root), F2_ID], capture_output=True, text=True, timeout=1500)
        need(F2_CHECK.is_file(), "the p139 checker is missing: %s" % F2_CHECK)
        lines = (r.stdout or "").strip().splitlines()
        need(r.returncode == 0 and lines and lines[-1] == F2_ID + " PASS", "%s did not pass: %s" % (F2_ID, " | ".join(lines[-3:] + (r.stderr or "").strip().splitlines()[-2:])[:300]))
        print("OK: %s PASS on the worker's tree" % F2_ID)
        return True
    if cid == "DBR200-3-AC1":
        p160 = helper("r149/p160_pub49f.py", "p160_helper_200")
        p149 = helper("r147/p149_pubroot.py", "p149_helper_200")
        p160.ENTRY_KEY = ENTRY
        zpath = p160.build_only(root)
        sources = {f: p160.source_of(root, new, f).read_text(encoding="utf-8") for f in new["files"] if f.endswith(".py")}
        mods = {Path(f).stem for f in sources} | {"lib"}
        check_imports(p149, p172, p149.third_party(sources, mods), sources)
        with zipfile.ZipFile(zpath) as z:
            p149.check_package([n for n in z.namelist() if not n.endswith("/")], new["files"], lambda mem: z.read(mem), lambda mem: p160.source_of(root, new, mem).read_bytes())
        print("OK: the build-only package equals the entry's sources byte for byte and imports only pyarrow and pandas plus the runtime's")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            need(type(exc).__name__ == "Fail", "red arm %s died with %r" % (label, exc))
            return
        raise AssertionError("red arm passed: " + label)
    assert check_grant({ENTRY_REL, D + AUTHOR + "/x.json"})
    assert check_grant({ENTRY_REL, "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md"})
    red(lambda: check_grant({D + AUTHOR + "/x.json"}), "no entry file")
    red(lambda: check_grant({ENTRY_REL, "lib/x.py"}), "a file outside the grant")
    red(lambda: check_grant({ENTRY_REL, "infra/aws/lambda/ci/function-map/other.json"}), "another function-map file")
    p172 = helper("r149/p172_repin_after_reader.py", "p172_helper_200s")
    pins = {"o": "a" * 40, "n": "b" * 40}
    sh = lambda b: {b"old": "1" * 64, b"new": "2" * 64, b"same": "3" * 64}[b]  # noqa: E731

    def mem(path, pin, content):
        return {"repo_path": path, "pin": pins[pin], "packaged_as": path, "sha256": sh(content)}
    be = {"artifact_sha256": "x", "files": ["a", "b"], "staged_from": [mem("a", "o", b"old"), mem("b", "o", b"same")]}
    ne = {"artifact_sha256": "x", "files": ["a", "b"], "staged_from": [mem("a", "n", b"new"), mem("b", "o", b"same")]}
    head = {"a": b"new", "b": b"same"}
    pb = lambda pin, path: head[path]  # noqa: E731
    assert p172.check_repin_entry("k", be, ne, lambda p: head[p], pb, lambda pin: True, sh) == ["a"]
    arms = (("deployed field", lambda e: e.update(artifact_sha256="y")), ("files list", lambda e: e["files"].append("c")), ("fresh member touched", lambda e: e["staged_from"][1].update(pin=pins["n"])),
            ("stale kept", lambda e: e["staged_from"].__setitem__(0, dict(be["staged_from"][0]))), ("bad sha", lambda e: e["staged_from"][0].update(sha256="9" * 64)))
    for label, fn in arms:
        e2 = copy.deepcopy(ne)
        fn(e2)
        red(lambda: p172.check_repin_entry("k", be, e2, lambda p: head[p], pb, lambda pin: True, sh), label)
    red(lambda: p172.check_repin_entry("k", be, ne, lambda p: head[p], pb, lambda pin: False, sh), "pin not an ancestor")
    nl = chr(10)
    naming_ok = {"x/lib/opal_naming.py": "def _lambda_source_map():" + nl + "    import opal_lambda_map" + nl, "x/handler.py": "import boto3" + nl}
    assert check_lazy_map_import(naming_ok)
    for label, srcs in (("top-level import", {"x/lib/opal_naming.py": "import opal_lambda_map" + nl}), ("another source names it", dict(naming_ok, **{"x/handler.py": "import opal_lambda_map" + nl})),
                        ("another source calls the consumers", dict(naming_ok, **{"x/handler.py": "lambda_plane_consumers(1)" + nl}))):
        red(lambda: check_lazy_map_import(srcs), label)
    print("selftest: grant (5 arms) and entry (%d arms plus ancestor) clauses behave" % len(arms))
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
