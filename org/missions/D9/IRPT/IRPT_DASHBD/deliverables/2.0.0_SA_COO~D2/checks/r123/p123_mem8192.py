"""IRPT_DASHBD round 123, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-250, the MEMORY of the hop-1 function (CTO analysis @1ffd4f5afb ruling 1): the reporting-gold function's
`memory_size` goes from 3008 to 8192 MB in lambda.tf, because the measured peak of one filled day is 4,025 MB (round 122, `RD_STAGE_MEMORY_R122.json`), 49 percent of 8192 MB and under
the 70 percent line; one pass per day stays. A one-line Terraform edit; nothing is planned, applied or deployed.

  DB-b-250 (~204) infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf: memory_size = 8192, timeout unchanged (900), nothing else; a small facts record.
                                                                                           DB123-1-AC1 (the Terraform edit), DB123-1-AC2 (the facts)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~204/RD_MEMORY_FACTS_R123.json"
MEM_REL = D + "0.9.0_WK_IRPT_DASHBD~200/RD_STAGE_MEMORY_R122.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-250.hop-1-function-memory-8192-in-the-reporting-gold-terraform.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~204"
LAMBDA_REL = "infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf"
TO_MB = 8192
FROM_MB = 3008
LIMIT_MB = 10240
PLAN_RESOURCES = ["aws_iam_role_policy.irpt_reporting_gold", "module.irpt_reporting_gold.aws_lambda_function.this"]
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "resources")
HEX64 = re.compile(r"[0-9a-f]{64}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True).stdout


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def own_numstat(root, commits, rel):
    add = dele = 0
    for c in commits:
        for ln in git(root, "show", "--numstat", "--format=", c, "--", rel).strip().splitlines():
            p = ln.split("\t")
            if len(p) >= 2 and p[0].isdigit() and p[1].isdigit():
                add += int(p[0])
                dele += int(p[1])
    return add, dele


def own_files(root, commits):
    names = set()
    for c in commits:
        names |= set(git(root, "show", "--name-only", "--format=", c).split())
    return names


def uncommented(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


def settings(text):
    """{memory_size, timeout} read from uncommented lines; each must appear exactly once."""
    t = uncommented(text)
    out = {}
    for key in ("memory_size", "timeout"):
        m = re.findall(r"^\s*%s\s*=\s*(\d+)\s*$" % key, t, re.M)
        need(len(m) == 1, "lambda.tf must carry exactly one %s assignment, found %d" % (key, len(m)))
        out[key] = int(m[0])
    return out


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_facts(rec, peak_mb, sha_of, file_exists):
    exp = {"function", "memory", "headroom", "expected_plan", "validated", "files_changed", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(nes(rec["words"]) and rec["claim"] in CLAIMS and nes(rec["function"]), "function, words or claim")
    m = rec["memory"]
    need(isinstance(m, dict) and set(m) == {"from_mb", "to_mb", "lambda_limit_mb", "timeout_seconds", "words"} and m["from_mb"] == FROM_MB and m["to_mb"] == TO_MB
         and m["lambda_limit_mb"] == LIMIT_MB and m["timeout_seconds"] == 900 and nes(m["words"]), "memory block")
    h = rec["headroom"]
    need(isinstance(h, dict) and set(h) == {"measured_peak_mb", "fraction_of_new_memory", "line_fraction", "under_line", "words"} and is_num(h["measured_peak_mb"]), "headroom block")
    need(abs(h["measured_peak_mb"] - peak_mb) <= 0.5, "measured_peak_mb %s differs from round 122's record %s" % (h["measured_peak_mb"], peak_mb))
    frac = round(peak_mb / TO_MB, 4)
    need(is_num(h["fraction_of_new_memory"]) and abs(h["fraction_of_new_memory"] - frac) <= 0.0005, "fraction_of_new_memory %s, recomputed %s" % (h["fraction_of_new_memory"], frac))
    need(h["line_fraction"] == 0.7 and h["under_line"] is (frac <= 0.7) and h["under_line"] is True and nes(h["words"]), "headroom line, under_line or words")
    ep = rec["expected_plan"]
    need(isinstance(ep, dict) and set(ep) == {"to_add", "to_change", "to_destroy", "resources", "words"} and ep["to_add"] == 0 and ep["to_change"] == 2 and ep["to_destroy"] == 0
         and sorted(ep["resources"]) == PLAN_RESOURCES and nes(ep["words"]), "expected_plan must stay 0 add / 2 change / 0 destroy on the two named resources")
    v = rec["validated"]
    need(isinstance(v, dict) and set(v) == {"ran", "words"} and isinstance(v["ran"], bool) and nes(v["words"]), "validated block")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and [f.get("file") for f in fc] == [LAMBDA_REL], "files_changed must be lambda.tf alone")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])) and sha_of(f["file"]) == f["sha256"], "files_changed entry: hash or form")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB123-1-AC1":
        s = settings((root / LAMBDA_REL).read_text(encoding="utf-8"))
        need(s["memory_size"] == TO_MB, "memory_size is %d, not %d" % (s["memory_size"], TO_MB))
        need(s["timeout"] == 900, "timeout is %d, not 900 (unchanged)" % s["timeout"])
        cs = own_commits(root)
        add, dele = own_numstat(root, cs, LAMBDA_REL)
        need(1 <= add <= 6 and dele <= 3, "lambda.tf must change by at most a few lines in the worker's own commits: +%d/-%d (needs gain 1 to 6, lose at most 3)" % (add, dele))
        other = sorted(f for f in own_files(root, cs) if f.startswith("infra/") and f != LAMBDA_REL)
        need(not other, "this worker's commits changed other infra files: %s" % other)
        print("OK: lambda.tf carries memory_size = %d and timeout = 900; +%d/-%d in the worker's own commits; no other infra file" % (s["memory_size"], add, dele))
        return True
    if cid == "DB123-1-AC2":
        rec = load(root, REC_REL)
        peak = float(load(root, MEM_REL)["peak_rss_mb"])
        check_facts(rec, peak, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file())
        print("OK: memory facts: %d to %d MB, the measured peak %.0f MB is %.1f percent of the new memory (under the 70 percent line); plan 0/2/0 on the two resources" %
              (FROM_MB, TO_MB, peak, 100.0 * peak / TO_MB))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    assert settings("resource x {\n  memory_size = 8192\n  timeout     = 900\n}\n") == {"memory_size": 8192, "timeout": 900}
    for bad in ("timeout = 900\n", "memory_size = 1\nmemory_size = 2\ntimeout = 9\n"):
        try:
            settings(bad)
            raise AssertionError("settings red arm passed")
        except Fail:
            pass
    assert settings("# memory_size = 1\n  memory_size = 8192\n  timeout = 900\n")["memory_size"] == 8192
    good = {"function": "irpt-49f-reporting-gold-lambda", "memory": {"from_mb": 3008, "to_mb": 8192, "lambda_limit_mb": 10240, "timeout_seconds": 900, "words": "w"},
            "headroom": {"measured_peak_mb": 4024.6, "fraction_of_new_memory": 0.4913, "line_fraction": 0.7, "under_line": True, "words": "w"},
            "expected_plan": {"to_add": 0, "to_change": 2, "to_destroy": 0, "resources": list(PLAN_RESOURCES), "words": "w"}, "validated": {"ran": False, "words": "no terraform"},
            "files_changed": [{"file": LAMBDA_REL, "sha256": "ab" * 32, "kind": "terraform"}], "words": "w", "claim": "inferred", "files_in_repo": False,
            "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(r, peak=4024.6, sha="ab" * 32):
        try:
            return check_facts(r, peak, lambda rel: sha, lambda rel: True)
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    for f in (lambda r: r["memory"].update(to_mb=4096), lambda r: r["headroom"].update(fraction_of_new_memory=0.6), lambda r: r["headroom"].update(measured_peak_mb=3000.0),
              lambda r: r["expected_plan"].update(to_add=1), lambda r: r.update(deployed=True), lambda r: r["files_changed"].append({"file": "x", "sha256": "ab" * 32, "kind": "k"}),
              lambda r: r["memory"].update(timeout_seconds=600), lambda r: r.update(words="id 1234567890")):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False
    assert grade(copy.deepcopy(good), sha="cd" * 32) is False
    print("selftest: the settings reader and one green and nine red facts arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
