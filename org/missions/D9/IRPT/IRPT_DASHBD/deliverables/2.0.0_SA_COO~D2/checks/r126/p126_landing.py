"""IRPT_DASHBD round 126, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-257, the COTTONWOOD LANDING ROOT MADE READY FOR ITS PAIR (CTO ROUND-126 ANALYSIS @2cf3e13682
ruling 1): the Terraform root's memory set from the round-125 measurement, the source-map entry's staged members pinned and hashed and its Terraform fields filled (the builder
refuses an entry whose tf_file does not name the pipeline), and a build-only package that carries exactly the declared members. LOCAL: nothing is planned, applied, uploaded
or deployed; BUILD_ONLY=1 builds a zip after every gate, uploads nothing and writes no source-map field.

  DB-b-257 (~210)   lambda.tf memory_size 8192 -> 1024; the source-map entry irpt-cot-account-return-daily-lambda; a facts record
                    DB126-1-AC1 (memory), AC2 (the source-map entry), AC3 (the build-only package and the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                      the pure clauses on synthetic arms
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~210/RD_COT_LANDING_FACTS_R126.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-257.cottonwood-landing-root-memory-1024-pins-and-build-only-package.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~210"
ROOT_DIR = "infra/aws/terraform/investor-reporting/account-return-daily/"
LAMBDA_TF = ROOT_DIR + "lambda.tf"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRY_KEY = "irpt-cot-account-return-daily-lambda"
LANDING_REL = D + "0.9.0_WK_IRPT_DASHBD~195/RD_CW_LANDING_FACTS_R120.json"
MEM_REL = D + "0.9.0_WK_IRPT_DASHBD~208/RD_COT_MEMORY_R125.json"
TF_RESOURCE = "module.irpt_account_return_daily.aws_lambda_function.this"
EDITABLE_ENTRY_KEYS = {"staged_from", "tf_file", "tf_resource", "iam_role", "_tf_note", "_staged_from_note"}
HEX40 = re.compile(r"[0-9a-f]{40}$")
HEX64 = re.compile(r"[0-9a-f]{64}$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "name", "names", "pin", "zip", "build_only_sha256")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, k)]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def git(root, *a, raw=False):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout if raw else r.stdout.decode("utf-8", "replace")


def base_commit(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    return base[-1]


def blob(root, rev, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (rev, rel)], capture_output=True)
    need(r.returncode == 0, "git show %s:%s failed" % (rev[:10], rel))
    return r.stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------------------------------------ pure clauses
def code_lines(text):
    return [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def check_memory(base_text, new_text, mem_rec):
    new_code = code_lines(new_text)
    base_code = code_lines(base_text)
    need(any(re.fullmatch(r"memory_size\s*=\s*1024", ln) for ln in new_code), "lambda.tf must carry memory_size = 1024")
    need(any(re.fullmatch(r"timeout\s*=\s*900", ln) for ln in new_code), "timeout must stay 900")
    need(any(re.fullmatch(r"reserved_concurrent_executions\s*=\s*1", ln) for ln in new_code), "reserved_concurrent_executions must stay 1")
    removed = [ln for ln in base_code if ln not in new_code]
    added = [ln for ln in new_code if ln not in base_code]
    need(len(removed) == 1 and re.fullmatch(r"memory_size\s*=\s*8192", removed[0]), "the only code line removed must be memory_size = 8192: %s" % removed[:3])
    need(len(added) == 1 and re.fullmatch(r"memory_size\s*=\s*1024", added[0]), "the only code line added must be memory_size = 1024: %s" % added[:3])
    comments = "\n".join(ln for ln in new_text.splitlines() if ln.lstrip().startswith("#"))
    need("RD_COT_MEMORY_R125" in comments, "the comment must cite RD_COT_MEMORY_R125")
    pk = float(mem_rec["peak_rss_mb"])
    shown = {str(int(pk)), str(int(pk) + 1), "%.0f" % pk, "%.1f" % pk}
    need(any(re.search(r"(?<![\d.])%s(?![\d])" % re.escape(s), comments) for s in shown), "the comment must state the measured peak (%s MB)" % pk)
    need("unmeasured" not in comments.lower(), "the comment still says the peak is unmeasured")
    need(mem_rec["chosen_memory_mb"] == 1024, "the measurement record chose %s, not 1024" % mem_rec["chosen_memory_mb"])
    return True


def check_entry(base_map, new_map, head_blob, pin_blob, pin_ok, expect_role):
    """base_map/new_map: parsed source maps; head_blob(path)/pin_blob(pin,path) -> bytes; pin_ok(pin) -> bool (a commit that is an ancestor of HEAD)."""
    need(set(base_map["functions"]) == set(new_map["functions"]), "the set of functions changed")
    for k, v in base_map["functions"].items():
        if k != ENTRY_KEY:
            need(new_map["functions"][k] == v, "another entry changed: %s" % k)
    for k in base_map:
        if k != "functions":
            need(new_map.get(k) == base_map[k], "a top-level key changed: %s" % k)
    be, ne = base_map["functions"][ENTRY_KEY], new_map["functions"][ENTRY_KEY]
    for k in set(be) | set(ne):
        if k not in EDITABLE_ENTRY_KEYS:
            need(be.get(k) == ne.get(k), "entry key %s changed" % k)
    need(ne.get("tf_file") == LAMBDA_TF, "tf_file must be %s" % LAMBDA_TF)
    need("investor-reporting" in ne["tf_file"], "tf_file must name the pipeline")
    need(ne.get("tf_resource") == TF_RESOURCE, "tf_resource must be %s" % TF_RESOURCE)
    need(ne.get("iam_role") == expect_role, "iam_role must be the builder's execution role name %s, got %s" % (expect_role, ne.get("iam_role")))
    bs, ns = be["staged_from"], ne.get("staged_from")
    need(isinstance(ns, list) and len(ns) == len(bs) == 15, "staged_from must keep its 15 members")
    for b, n in zip(bs, ns):
        need(b["repo_path"] == n["repo_path"] and b["packaged_as"] == n["packaged_as"], "member identity changed: %s" % b["repo_path"])
        need(set(n) == {"repo_path", "pin", "packaged_as", "sha256"}, "member keys changed: %s" % b["repo_path"])
        need(isinstance(n["pin"], str) and HEX40.match(n["pin"]), "pin of %s is not a full 40-hex commit" % n["repo_path"])
        need(isinstance(n["sha256"], str) and HEX64.match(n["sha256"]), "sha256 of %s is not 64 hex" % n["repo_path"])
        need(pin_ok(n["pin"]), "pin of %s is not a commit that is an ancestor of HEAD" % n["repo_path"])
        pb = pin_blob(n["pin"], n["repo_path"])
        need(sha(pb) == n["sha256"], "sha256 of %s differs from git show pin:path" % n["repo_path"])
        need(sha(head_blob(n["repo_path"])) == n["sha256"], "the pinned bytes of %s differ from HEAD's" % n["repo_path"])
    return True


def check_package(names_in_zip, expected_members, bytes_of_zip, bytes_expected):
    need(sorted(names_in_zip) == sorted(expected_members), "zip members differ: extra %s missing %s" %
         (sorted(set(names_in_zip) - set(expected_members))[:3], sorted(set(expected_members) - set(names_in_zip))[:3]))
    for m in expected_members:
        need(bytes_of_zip(m) == bytes_expected(m), "zip member %s differs from its source" % m)
    return True


def check_facts(rec, recount_names, build_sha, n_members):
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    exp = {"firm", "names", "memory_mb", "peak_rss_mb", "members", "build_only_sha256", "plan_expected", "pins_written_by", "words"}
    need(set(rec) == exp, "record keys differ: extra %s missing %s" % (sorted(set(rec) - exp), sorted(exp - set(rec))))
    need(rec["firm"] == "cottonwood", "firm must be cottonwood")
    need(rec["names"] == recount_names, "names differ from the builder's five: %s" % rec["names"])
    need(rec["memory_mb"] == 1024 and rec["members"] == n_members, "memory_mb must be 1024 and members %d" % n_members)
    need(isinstance(rec["peak_rss_mb"], (int, float)) and 100 < rec["peak_rss_mb"] < 717, "peak_rss_mb must be the measured peak under 70 percent of 1024")
    need(rec["build_only_sha256"] == build_sha, "build_only_sha256 differs from the checker's own build-only run")
    need(rec["plan_expected"] == {"add": 7, "change": 0, "destroy": 0, "claim": "inferred"}, "plan_expected must be 7/0/0 claimed inferred")
    need(rec["pins_written_by"] == AUTHOR, "pins_written_by must be %s" % AUTHOR)
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1500, "words must be one paragraph of 80 to 1500 characters")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def builder_names(root, args_list):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    out = []
    for a in args_list:
        kw = {"qualifier": a["qualifier"]} if a.get("qualifier") else {}
        out.append(opal_naming.name(a["system"], a["scope"], a["function"], a["kind"], **kw))
    return out


def run(root, cid):
    root = Path(root)
    base = base_commit(root)
    if cid == "DB126-1-AC1":
        mem = json.loads((root / MEM_REL).read_text(encoding="utf-8"))
        check_memory(blob(root, base, LAMBDA_TF).decode("utf-8"), (root / LAMBDA_TF).read_text(encoding="utf-8"), mem)
        others = [f for f in git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", ROOT_DIR).split() if f != LAMBDA_TF]
        for f in others:
            need(blob(root, "HEAD", f) == blob(root, base, f), "another root file changed: %s" % f)
        print("OK: lambda.tf memory_size 1024 (measured peak %s MB, record cited), timeout 900 and reserved concurrency 1 kept, the only code line changed is memory_size, %d other root files byte-equal to the base" % (mem["peak_rss_mb"], len(others)))
        return True
    landing = json.loads((root / LANDING_REL).read_text(encoding="utf-8"))
    names = builder_names(root, [x["builder_args"] for x in landing["names"]])
    if cid == "DB126-1-AC2":
        bm = json.loads(blob(root, base, SOURCE_MAP_REL).decode("utf-8"))
        nm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))
        role = names[1]
        need(role.endswith("-execution-role"), "the second builder name is not the execution role: %s" % role)
        check_entry(bm, nm, lambda p: blob(root, "HEAD", p), lambda pin, p: blob(root, pin, p),
                    lambda pin: subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", pin, "HEAD"], capture_output=True).returncode == 0
                    and git(root, "cat-file", "-t", pin).strip() == "commit", role)
        print("OK: source-map entry %s: 15 members pinned to ancestor commits with sha256 equal to git show and to HEAD, tf_file/tf_resource/iam_role filled (%s), no other entry or key changed" % (ENTRY_KEY, role))
        return True
    if cid == "DB126-1-AC3":
        sm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))
        ent = sm["functions"][ENTRY_KEY]
        env = dict(os.environ, BUILD_ONLY="1")
        r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", ENTRY_KEY], cwd=str(root), env=env, capture_output=True, text=True, timeout=240)
        out = r.stdout + r.stderr
        m = re.search(r"BUILD_ONLY:\s*(\S+)\s+sha256=(\S+)", out)
        need(r.returncode == 0 and m is not None, "the build-only run failed (rc %s): %s" % (r.returncode, out[-300:].replace("\n", " | ")))
        zpath, zsha = m.group(1), m.group(2)
        if zpath.startswith("/"):
            cp = subprocess.run(["cygpath", "-w", zpath], capture_output=True, text=True)
            need(cp.returncode == 0 and cp.stdout.strip(), "cygpath could not resolve the build-only zip path %s" % zpath)
            zpath = cp.stdout.strip()
        need(Path(zpath).is_file(), "the build-only zip is not at %s" % zpath)
        members = list(ent["files"])
        with zipfile.ZipFile(zpath) as z:
            def expected(mem):
                src = ent["source_dir"] + "/" + mem if mem == "handler.py" else mem
                return blob(root, "HEAD", src)
            check_package([n for n in z.namelist() if not n.endswith("/")], members, lambda mem: z.read(mem), expected)
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec, names, zsha, len(members))
        print("OK: build-only package of %d members equals its sources byte for byte; the record's five names equal the builder's, memory 1024, build sha equals this run's, plan 7/0/0 inferred" % len(members))
        return True
    raise Fail("unknown criterion %s" % cid)


# ------------------------------------------------------------------------------------------------ the self-test
def selftest():
    import copy
    base_tf = '# top\nmodule "m" {\n  timeout = 900\n  memory_size = 8192\n  reserved_concurrent_executions = 1\n}\n# This function\'s own peak is unmeasured\n'
    good_tf = '# measured RD_COT_MEMORY_R125 peak 654 MB\nmodule "m" {\n  timeout = 900\n  memory_size = 1024\n  reserved_concurrent_executions = 1\n}\n'
    mem = {"peak_rss_mb": 654.2, "chosen_memory_mb": 1024}

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)

    assert check_memory(base_tf, good_tf, mem)
    red(lambda: check_memory(base_tf, good_tf.replace("1024", "2048"), mem), "wrong size")
    red(lambda: check_memory(base_tf, good_tf.replace("timeout = 900", "timeout = 600"), mem), "timeout changed")
    red(lambda: check_memory(base_tf, good_tf.replace("RD_COT_MEMORY_R125", "x"), mem), "no citation")
    red(lambda: check_memory(base_tf, good_tf + "# unmeasured\n", mem), "still unmeasured")
    red(lambda: check_memory(base_tf, good_tf.replace("}\n", "  extra = 1\n}\n"), mem), "extra code line")

    files = ["a.py", "b.json"]
    contents = {f: f.encode() * 3 for f in files}
    pins = {f: ("%040x" % (i + 1)) for i, f in enumerate(files)}

    def mk_map(staged, tf_file, tf_res, role):
        return {"functions": {"other": {"x": 1}, ENTRY_KEY: {"source_dir": "s", "files": ["handler.py"] + files, "tf_file": tf_file, "tf_resource": tf_res, "iam_role": role,
                                                              "staged_from": staged, "artifact_s3_key": "k"}}}
    base_staged = [{"repo_path": f, "pin": None, "packaged_as": f, "sha256": None} for f in files]
    # the entry check wants 15 members; extend the synthetic list
    for i in range(13):
        f = "m%d.json" % i
        files.append(f)
        contents[f] = f.encode() * 2
        pins[f] = "%040x" % (100 + i)
        base_staged.append({"repo_path": f, "pin": None, "packaged_as": f, "sha256": None})
    new_staged = [{"repo_path": f, "pin": pins[f], "packaged_as": f, "sha256": sha(contents[f])} for f in files]
    bm = mk_map(base_staged, None, None, None)
    nm = mk_map(new_staged, LAMBDA_TF, TF_RESOURCE, "irpt-cot-account-return-daily-execution-role")
    def head_blob(p):
        return contents[p]

    def pin_blob(pin, p):
        return contents[p]

    def ok_pin(pin):
        return True

    assert check_entry(bm, nm, head_blob, pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role")
    red(lambda: check_entry(bm, nm, head_blob, pin_blob, lambda p: False, "irpt-cot-account-return-daily-execution-role"), "pin not an ancestor")
    red(lambda: check_entry(bm, nm, head_blob, lambda pin, p: b"drift", ok_pin, "irpt-cot-account-return-daily-execution-role"), "pin content differs")
    red(lambda: check_entry(bm, nm, lambda p: b"moved", pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role"), "HEAD differs from the pin")
    bad = copy.deepcopy(nm)
    bad["functions"][ENTRY_KEY]["staged_from"][0]["pin"] = "main"
    red(lambda: check_entry(bm, bad, head_blob, pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role"), "moving ref")
    bad = copy.deepcopy(nm)
    bad["functions"][ENTRY_KEY]["tf_file"] = "infra/other.tf"
    red(lambda: check_entry(bm, bad, head_blob, pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role"), "tf_file")
    bad = copy.deepcopy(nm)
    bad["functions"]["other"]["x"] = 2
    red(lambda: check_entry(bm, bad, head_blob, pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role"), "other entry changed")
    bad = copy.deepcopy(nm)
    bad["functions"][ENTRY_KEY]["files"] = ["handler.py"]
    red(lambda: check_entry(bm, bad, head_blob, pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role"), "files list changed")
    red(lambda: check_entry(bm, nm, head_blob, pin_blob, ok_pin, "irpt-wrong-role"), "iam_role")
    bad = copy.deepcopy(nm)
    bad["functions"][ENTRY_KEY]["staged_from"].pop()
    red(lambda: check_entry(bm, bad, head_blob, pin_blob, ok_pin, "irpt-cot-account-return-daily-execution-role"), "a member lost")

    members = ["handler.py", "a.py"]
    src = {"handler.py": b"h", "a.py": b"a"}
    assert check_package(members, members, lambda m: src[m], lambda m: src[m])
    red(lambda: check_package(members + ["extra.py"], members, lambda m: src.get(m, b""), lambda m: src[m]), "extra member")
    red(lambda: check_package(["handler.py"], members, lambda m: src[m], lambda m: src[m]), "missing member")
    red(lambda: check_package(members, members, lambda m: b"x", lambda m: src[m]), "bytes differ")

    nm5 = ["a", "b", "c", "d", "e"]
    rec = {"firm": "cottonwood", "names": nm5, "memory_mb": 1024, "peak_rss_mb": 654.2, "members": 16, "build_only_sha256": "AbC=", "plan_expected": {"add": 7, "change": 0, "destroy": 0, "claim": "inferred"},
           "pins_written_by": AUTHOR, "words": "w" * 120}
    assert check_facts(rec, nm5, "AbC=", 16)
    for label, fn in (("sha", lambda r: r.update(build_only_sha256="x")), ("memory", lambda r: r.update(memory_mb=2048)), ("names", lambda r: r.update(names=["a"])),
                      ("plan", lambda r: r["plan_expected"].update(add=6)), ("peak", lambda r: r.update(peak_rss_mb=800)), ("author", lambda r: r.update(pins_written_by="x")),
                      ("words", lambda r: r.update(words="short")), ("extra key", lambda r: r.update(x=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, nm5, "AbC=", 16), label)
    print("selftest: memory, entry (11 red arms), package and facts clauses behave")
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except (Fail, OSError, ValueError, KeyError, TypeError, IndexError) as e:
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
