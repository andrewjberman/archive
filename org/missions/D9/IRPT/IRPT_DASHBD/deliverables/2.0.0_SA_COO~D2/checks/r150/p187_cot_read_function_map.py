"""IRPT_DASHBD round 150, workstream COTMAP (issuer 2.0.0_SA_COO~D2) -- DB-b-321, C3 of the Cottonwood Performance read path: the FUNCTION-MAP. The new function
`irpt-cot-reporting-read-lambda` gets its own entry `infra/aws/lambda/ci/function-map/irpt-cot-reporting-read-lambda.json`, the twin of the 49 Financial read entry
(`irpt-49f-reporting-read-lambda.json`): the SAME source directory, the SAME files and the SAME pinned members, so the two functions run byte-identical code and differ only by
environment. The ONE member that moves in both entries is `served.py` (it carries the forward, DB-b-319): its pin becomes the commit that carries those bytes. No deploy field moves.
LOCAL: nothing is built for upload, uploaded, planned or applied; the build-only run keeps a zip on disk and prints its hash.

  DB187-1-AC1   the new entry: its keys, its tf fields, its artifact key, members equal to the 49 Financial entry's, no deploy field
  DB187-1-AC2   the re-pin: served.py in BOTH entries pinned to an ancestor commit carrying the bytes at HEAD; nothing else in the 49 Financial entry changed
  DB187-1-AC3   the real build-only run through the function map for both entries: equal hashes, package equals its sources, and the facts record

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>     green on a reference tree, red on single-fault mutants
"""
import copy
import glob
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-321.cottonwood-read-path-c3-function-map.md"
FMAP = "infra/aws/lambda/ci/function-map/"
NEW = "irpt-cot-reporting-read-lambda"
OLD = "irpt-49f-reporting-read-lambda"
SERVED = "infra/aws/lambda/investor-reporting/_authz/served.py"
ISO_TF = "infra/aws/terraform/investor-reporting/reporting-read-iso/lambda.tf"
ISO_RES = "module.irpt_reporting_read_iso.aws_lambda_function.this"
ROLE = "irpt-cot-reporting-read-role"
KEY = "investor-reporting/irpt-cot-reporting-read-lambda.zip"
DEPLOY_FIELDS = {"artifact_sha256", "last_deployed_commit", "last_deployed_at", "recorded_by", "deploy_ledger", "deployed_code_sha256"}
NEW_KEYS = {"source_dir", "files", "staged_from", "tf_file", "tf_resource", "iam_role", "pipeline", "artifact_s3_key"}
HEX40, HEX64 = re.compile(r"[0-9a-f]{40}$"), re.compile(r"[0-9a-f]{64}$")
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout, r.returncode


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------------------------------------ pure clauses
def check_new_entry(new, old):
    need(set(new) >= NEW_KEYS and not (set(new) & DEPLOY_FIELDS), "the new entry needs %s and no deploy field (%s); read keys %s" % (sorted(NEW_KEYS), sorted(DEPLOY_FIELDS), sorted(new)))
    need(set(new) - NEW_KEYS <= {"_staged_from_note", "_build_note"}, "unexpected keys in the new entry: %s" % sorted(set(new) - NEW_KEYS - {"_staged_from_note", "_build_note"}))
    for k in ("source_dir", "pipeline", "files"):
        need(new[k] == old[k], "%s must equal the 49 Financial entry's" % k)
    need(new["tf_file"] == ISO_TF and new["tf_resource"] == ISO_RES and new["iam_role"] == ROLE and new["artifact_s3_key"] == KEY,
         "tf_file, tf_resource, iam_role or artifact_s3_key differ from the agreed values")
    need(new["staged_from"] == old["staged_from"], "staged_from must equal the 49 Financial entry's member for member (same code, differing only by environment)")
    return True


def check_repin(new, old, old_base, head_blob, pin_blob, pin_ok):
    for name, e in (("new", new), ("49F", old)):
        m = [s for s in e["staged_from"] if s["repo_path"] == SERVED]
        need(len(m) == 1, "%s entry: exactly one served.py member" % name)
        s = m[0]
        need(set(s) == {"repo_path", "pin", "packaged_as", "sha256"} and isinstance(s["pin"], str) and HEX40.match(s["pin"]) and isinstance(s["sha256"], str) and HEX64.match(s["sha256"]), "%s entry: served.py member form" % name)
        need(pin_ok(s["pin"]), "%s entry: the served.py pin is not an ancestor commit" % name)
        need(sha(pin_blob(s["pin"], SERVED)) == s["sha256"] == sha(head_blob(SERVED)), "%s entry: served.py sha256 differs from git show pin:path or the file at HEAD" % name)
    # the 49 Financial entry: ONLY the served.py member's pin and sha256 moved
    moved = [k for k in set(old) | set(old_base) if k != "staged_from" and old.get(k) != old_base.get(k)]
    need(not moved, "the 49 Financial entry changed beyond staged_from: %s" % sorted(moved))
    ob = {s["repo_path"]: s for s in old_base["staged_from"]}
    cur = {s["repo_path"]: s for s in old["staged_from"]}
    need(set(ob) == set(cur), "the 49 Financial entry's member set changed")
    changed = [p for p in cur if cur[p] != ob[p]]
    need(changed == [SERVED], "exactly the served.py member may move in the 49 Financial entry; moved %s" % changed)
    need(cur[SERVED]["pin"] != ob[SERVED]["pin"] and cur[SERVED]["sha256"] != ob[SERVED]["sha256"], "served.py in the 49 Financial entry must actually move (pin and sha256)")
    return True


def check_package(names_in_zip, expected, bytes_of_zip, bytes_expected):
    need(sorted(names_in_zip) == sorted(expected), "zip members differ: extra %s missing %s" % (sorted(set(names_in_zip) - set(expected))[:3], sorted(set(expected) - set(names_in_zip))[:3]))
    for m in expected:
        need(bytes_of_zip(m) == bytes_expected(m), "zip member %s differs from its source" % m)
    return True


def check_hashes(h_new, h_old):
    need(isinstance(h_new, str) and isinstance(h_old, str) and re.match(r"[A-Za-z0-9+/]{43}=$", h_new) and h_new == h_old, "the two entries must build byte-identical packages (equal base64 sha256)")
    return True


def check_facts(rec, h):
    exp = {"entries", "served_pin", "served_sha256", "build_only_sha256", "members", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["entries"] == [NEW, OLD], "entries must be [%s, %s]" % (NEW, OLD))
    need(isinstance(rec["served_pin"], str) and HEX40.match(rec["served_pin"]) and isinstance(rec["served_sha256"], str) and HEX64.match(rec["served_sha256"]), "served_pin or served_sha256 form")
    need(rec["build_only_sha256"] == h, "build_only_sha256 must equal the hash the real build printed")
    need(isinstance(rec["members"], int) and rec["members"] >= 30, "members: the count of zip members")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def issued_to(root):
    m = re.search(r"<issued_to>([^<]+)</issued_to>", (Path(root) / ORDER_REL).read_text(encoding="utf-8"))
    need(m is not None, "the order has no issued_to")
    return m.group(1).strip()


def worker_base_ref(root, serial, rel):
    out = git(root, "log", "--author=" + serial, "--format=%H", "--", rel)[0].decode().split()
    return (out[-1] + "^") if out else "HEAD"


def build_only(root, entry):
    import os
    r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", entry], cwd=str(root), env=dict(os.environ, BUILD_ONLY="1"), capture_output=True, text=True, timeout=600)
    m = re.search(r"BUILD_ONLY:\s*(\S+)\s+sha256=(\S+)", r.stdout + r.stderr)
    need(r.returncode == 0 and m is not None, "the build-only run of %s failed (rc %s): %s" % (entry, r.returncode, (r.stdout + r.stderr)[-300:].replace("\n", " | ")))
    zpath = m.group(1)
    if zpath.startswith("/"):
        cp = subprocess.run(["cygpath", "-w", zpath], capture_output=True, text=True)
        need(cp.returncode == 0, "cygpath could not resolve %s" % zpath)
        zpath = cp.stdout.strip()
    return zpath, m.group(2)


def load(root, name):
    return json.loads((Path(root) / FMAP / (name + ".json")).read_text(encoding="utf-8"))


def run(root, cid):
    root = Path(root)
    serial = issued_to(root)
    if cid == "DB187-1-AC1":
        check_new_entry(load(root, NEW), load(root, OLD))
        print("OK: the new entry has the agreed keys and tf fields, no deploy field, and the 49 Financial entry's source_dir, files and %d members" % len(load(root, NEW)["staged_from"]))
        return True
    if cid == "DB187-1-AC2":
        base = worker_base_ref(root, serial, FMAP + OLD + ".json")
        old_base = json.loads(git(root, "show", "%s:%s" % (base, FMAP + OLD + ".json"))[0].decode("utf-8"))

        def pin_blob(pin, p):
            out, rc = git(root, "show", "%s:%s" % (pin, p))
            need(rc == 0, "git show %s:%s failed" % (pin[:10], p))
            return out
        check_repin(load(root, NEW), load(root, OLD), old_base, lambda p: (root / p).read_bytes(), pin_blob, lambda pin: git(root, "merge-base", "--is-ancestor", pin, "HEAD")[1] == 0)
        print("OK: served.py is pinned in both entries to an ancestor commit carrying the bytes at HEAD; the 49 Financial entry changed in that one member only")
        return True
    if cid == "DB187-1-AC3":
        new, old = load(root, NEW), load(root, OLD)
        zp_new, h_new = build_only(root, NEW)
        zp_old, h_old = build_only(root, OLD)
        check_hashes(h_new, h_old)
        for zp, e in ((zp_new, new), (zp_old, old)):
            with zipfile.ZipFile(zp) as z:
                check_package([n for n in z.namelist() if not n.endswith("/")], e["files"], lambda m, z=z: z.read(m), lambda m, e=e: _source_bytes(root, e, m))
        recs = sorted(glob.glob(str(root / (D + serial) / "RD_COT_READ_FUNCTION_MAP_FACTS_R150.json")))
        need(len(recs) == 1, "the facts record RD_COT_READ_FUNCTION_MAP_FACTS_R150.json is missing from %s%s/" % (D, serial))
        rec = json.loads(Path(recs[0]).read_text(encoding="utf-8"))
        check_facts(rec, h_new)
        with zipfile.ZipFile(zp_new) as z:
            need(rec["members"] == len([n for n in z.namelist() if not n.endswith("/")]), "members must equal the zip's member count")
        print("OK: the real build-only run of both entries through the function map prints one hash, each package equals its sources member for member, and the facts record equals it")
        return True
    raise Fail("unknown criterion %s" % cid)


def _source_bytes(root, entry, member):
    staged = {s["packaged_as"]: s for s in entry["staged_from"]}
    if member in staged:
        out, rc = git(root, "show", "%s:%s" % (staged[member]["pin"], staged[member]["repo_path"]))
        need(rc == 0, "git show %s:%s failed" % (staged[member]["pin"][:10], staged[member]["repo_path"]))
        return out
    return (Path(root) / entry["source_dir"] / member).read_bytes()


def selftest(ref_root):
    ref = Path(ref_root)
    new, old = load(ref, NEW), load(ref, OLD)
    head = (ref / SERVED).read_bytes()
    other = next(i for i, s in enumerate(old["staged_from"]) if s["repo_path"] != SERVED)
    base_old = copy.deepcopy(old)
    for s in base_old["staged_from"]:
        if s["repo_path"] == SERVED:
            s["pin"], s["sha256"] = "%040x" % 1, "%064x" % 2

    def repin(n=new, o=old, base=base_old, pb=lambda pin, p: head, ok=lambda pin: True):
        return check_repin(n, o, base, lambda p: head, pb, ok)
    check_new_entry(new, old)
    assert repin()
    n = 0

    def red(fn, label):
        nonlocal n
        try:
            fn()
        except Fail:
            n += 1
            return
        raise AssertionError("mutant passed: " + label)

    def edit(entry, fn):
        e = copy.deepcopy(entry)
        fn(e)
        return e
    red(lambda: check_new_entry(edit(new, lambda e: e.update(artifact_sha256="x")), old), "deploy field on the new entry")
    red(lambda: check_new_entry(edit(new, lambda e: e.update(tf_resource="x")), old), "tf_resource")
    red(lambda: check_new_entry(edit(new, lambda e: e.update(iam_role="x")), old), "iam_role")
    red(lambda: check_new_entry(edit(new, lambda e: e.update(artifact_s3_key="x")), old), "artifact key")
    red(lambda: check_new_entry(edit(new, lambda e: e.update(tf_file="x")), old), "tf_file")
    red(lambda: check_new_entry(edit(new, lambda e: e.update(files=e["files"][:-1])), old), "files")
    red(lambda: check_new_entry(edit(new, lambda e: e["staged_from"].pop()), old), "member lost")
    red(lambda: check_new_entry(edit(new, lambda e: e["staged_from"][0].update(sha256="%064x" % 5)), old), "member sha")
    red(lambda: check_new_entry(edit(new, lambda e: e.update(source_dir="x")), old), "source_dir")
    red(lambda: check_new_entry(edit(new, lambda e: e.pop("tf_file")), old), "key lost")
    red(lambda: repin(ok=lambda pin: False), "pin ancestry")
    red(lambda: repin(pb=lambda pin, p: b"drift"), "pin content")
    red(lambda: repin(o=edit(old, lambda e: e["staged_from"][[s["repo_path"] for s in e["staged_from"]].index(SERVED)].update(sha256="%064x" % 9))), "sha256 differs from the file")
    red(lambda: repin(base=copy.deepcopy(old)), "served.py did not move")
    red(lambda: repin(o=edit(old, lambda e: e.update(artifact_sha256="x"))), "a deploy field moved")
    red(lambda: repin(o=edit(old, lambda e: e["staged_from"][other].update(pin="%040x" % 7))), "another member moved")
    red(lambda: repin(o=edit(old, lambda e: e["staged_from"].pop(other))), "member set changed")
    red(lambda: repin(n=edit(new, lambda e: e["staged_from"].append(dict(e["staged_from"][0])))), "new member duplicated")
    red(lambda: repin(o=edit(old, lambda e: e.update(tf_resource="x"))), "49F tf_resource moved")
    assert check_package(["a", "b"], ["a", "b"], lambda m: b"1", lambda m: b"1")
    red(lambda: check_package(["a", "b", "c"], ["a", "b"], lambda m: b"1", lambda m: b"1"), "extra member")
    red(lambda: check_package(["a", "b"], ["a", "b"], lambda m: b"1", lambda m: b"2"), "bytes")
    h = "A" * 43 + "="
    assert check_hashes(h, h)
    red(lambda: check_hashes(h, "B" * 43 + "="), "hashes differ")
    red(lambda: check_hashes("short", "short"), "hash form")
    rec = {"entries": [NEW, OLD], "served_pin": "%040x" % 3, "served_sha256": "%064x" % 4, "build_only_sha256": h, "members": 32, "words": "w" * 100}
    assert check_facts(rec, h)
    for label, fn in (("entries", lambda r: r.update(entries=[OLD, NEW])), ("pin", lambda r: r.update(served_pin="x")), ("hash", lambda r: r.update(build_only_sha256="x")),
                      ("members", lambda r: r.update(members=3)), ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, h), label)
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or build is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
