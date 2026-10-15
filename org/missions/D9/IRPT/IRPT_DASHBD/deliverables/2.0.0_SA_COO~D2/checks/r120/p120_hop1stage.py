"""IRPT_DASHBD round 120, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-237, hop 1 TO THE CLOUD: the `filled_report_values` stage of the 49 Financial
reporting-gold Lambda, built LOCAL and ADDITIVE, and the facts the never-widen packet needs (CTO analysis @5e358b0a8f ruling 1).

  DB-b-237 (~191) the reporting-gold handler gains a GUARDED stage that builds the day's `filled_report_values` rows (the module of round 118) from the
                  day's gold tables and writes ONE partition at the firm's gold address, after the stages that produce its inputs and on the
                  existing daily schedule; the bundle gains the module as a member of the function's source-map entry (the pin is written by the
                  applier); nothing is applied, scheduled or written to the cloud, and no Terraform file changes. A facts record names every file,
                  the IAM cover, the schedule, the expected plan and the names.            DB120-1-AC1 (the stage and its tests), AC2 (the facts),
                                                                                           AC3 (the change is additive)

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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~191/RD_HOP1_STAGE_FACTS_R120.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-237.hop-1-reporting-gold-stage-filled-report-values-additive-build.md"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
TESTS_DIR = "infra/aws/lambda/investor-reporting/reporting-gold/tests"
NEW_TEST_REL = TESTS_DIR + "/test_filled_report_values_stage.py"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/filled_report_values.py"
BASE_TESTS = 96
MIN_NEW_TESTS = 6
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "line", "pin")
HEX64 = re.compile(r"[0-9a-f]{64}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load_json(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True)
    return r.stdout


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def numstat(root, base, rel):
    out = git(root, "diff", "--numstat", base, "HEAD", "--", rel).strip().split("\n")[0].split("\t")
    need(len(out) >= 2 and out[0].isdigit() and out[1].isdigit(), "no numstat for %s" % rel)
    return int(out[0]), int(out[1])


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_facts(rec, sha_of, file_exists, has_line):
    exp = {"firm", "stage", "files_changed", "source_map", "iam", "schedule", "expected_plan", "write_path", "tests", "names", "words", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == "49financial" and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    st = rec["stage"]
    need(isinstance(st, dict) and set(st) == {"handler_file", "functions", "guarded_import", "after_stages", "words"} and st["handler_file"] == HANDLER_REL
         and isinstance(st["functions"], list) and len(st["functions"]) >= 2 and all(nes(x) for x in st["functions"]) and st["guarded_import"] is True
         and isinstance(st["after_stages"], list) and len(st["after_stages"]) >= 1 and nes(st["words"]), "stage form")
    for fn in st["functions"]:
        need(has_line(HANDLER_REL, "def " + fn), "the handler has no function %s" % fn)
    fc = rec["files_changed"]
    need(isinstance(fc, list) and len(fc) >= 3, "files_changed must list at least the handler, the test file and the source map")
    names = []
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])), "a files_changed entry: %s" % f.get("file"))
        need(sha_of(f["file"]) == f["sha256"], "files_changed: the sha256 of %s differs from the bytes" % f["file"])
        names.append(f["file"])
    need(HANDLER_REL in names and NEW_TEST_REL in names and SOURCE_MAP_REL in names, "files_changed must name the handler, the new test file and the source map")
    need(not [n for n in names if n.startswith("infra/aws/terraform/")], "no Terraform file may change in this cell")
    sm = rec["source_map"]
    need(isinstance(sm, dict) and set(sm) == {"file", "entry", "member_added", "pin", "words"} and sm["file"] == SOURCE_MAP_REL and sm["member_added"] == MODULE_REL
         and nes(sm["entry"]) and nes(sm["pin"]) and nes(sm["words"]), "source_map form")
    iam = rec["iam"]
    need(isinstance(iam, dict) and set(iam) == {"file", "covers_new_prefix", "statement_ids", "words"} and nes(iam["file"]) and isinstance(iam["covers_new_prefix"], bool)
         and isinstance(iam["statement_ids"], list) and nes(iam["words"]) and file_exists(iam["file"]), "iam form")
    sc = rec["schedule"]
    need(isinstance(sc, dict) and set(sc) == {"file", "cron", "after_inputs", "trading_day_frontier", "words"} and file_exists(sc["file"]) and nes(sc["cron"])
         and sc["after_inputs"] is True and sc["trading_day_frontier"] is True and nes(sc["words"]), "schedule form")
    ep = rec["expected_plan"]
    need(isinstance(ep, dict) and set(ep) == {"to_add", "to_change", "to_destroy", "resources", "words"} and all(is_int(ep[k]) and ep[k] >= 0 for k in ("to_add", "to_change", "to_destroy"))
         and ep["to_destroy"] == 0 and isinstance(ep["resources"], list) and nes(ep["words"]), "expected_plan form (to_destroy must be 0)")
    wp = rec["write_path"]
    need(isinstance(wp, dict) and set(wp) == {"table", "address_form", "partition", "existing_prefixes_written"} and wp["table"] == "filled_report_values"
         and "address(" in str(wp["address_form"]) and wp["existing_prefixes_written"] == [] and nes(wp["partition"]), "write_path form (no existing prefix may be written)")
    ts = rec["tests"]
    need(isinstance(ts, dict) and set(ts) == {"file", "new_tests", "dir_total"} and ts["file"] == NEW_TEST_REL and is_int(ts["new_tests"]) and ts["new_tests"] >= MIN_NEW_TESTS
         and is_int(ts["dir_total"]) and ts["dir_total"] >= BASE_TESTS + MIN_NEW_TESTS, "tests form")
    nm = rec["names"]
    need(isinstance(nm, dict) and set(nm) == {"from_builders", "words"} and nm["from_builders"] is True and nes(nm["words"]), "names form (every new name is builder output; a new name is a registry row, not typed)")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB120-1-AC1":
        hp = root / HANDLER_REL
        tp = root / NEW_TEST_REL
        need(hp.is_file() and tp.is_file(), "no handler or no new test file")
        text = hp.read_text(encoding="utf-8")
        need(re.search(r"import filled_report_values", text) and re.search(r"except\s+\w*\s*(as\s+\w+)?\s*:", text.split("import filled_report_values", 1)[1][:400]),
             "the handler must import filled_report_values GUARDED (a try with an except that records the import error)")
        names = re.findall(r"def (test_\w+)", tp.read_text(encoding="utf-8"))
        need(len(names) >= MIN_NEW_TESTS, "the new test file needs at least %d tests, found %d" % (MIN_NEW_TESTS, len(names)))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(root / TESTS_DIR)], cwd=str(root), capture_output=True, text=True, timeout=100)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= BASE_TESTS + MIN_NEW_TESTS and "failed" not in r.stdout,
             "pytest on the handler's tests: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: the handler imports filled_report_values guarded; %s tests of the handler's directory pass (%d earlier plus %d new in the stage test file)" % (m.group(1), BASE_TESTS, len(names)))
        return True
    if cid == "DB120-1-AC2":
        rec = load_json(root, REC_REL)

        def sha_of(rel):
            return hashlib.sha256((root / rel).read_bytes()).hexdigest()

        def has_line(rel, token):
            return token in (root / rel).read_text(encoding="utf-8")
        check_facts(rec, sha_of, lambda rel: (root / rel).is_file(), has_line)
        print("OK: the facts record names %d changed files (hashes equal the bytes), the stage functions, the source-map member, the IAM cover, the schedule, an expected plan "
              "with no destroy, a write path that touches no existing prefix, and builder-derived names" % len(rec["files_changed"]))
        return True
    if cid == "DB120-1-AC3":
        base = base_commit(root)
        add, dele = numstat(root, base, HANDLER_REL)
        need(add >= 20 and dele <= 3, "the handler change must be additive: %d added, %d deleted lines (at most 3 deleted)" % (add, dele))
        a2, d2 = numstat(root, base, SOURCE_MAP_REL)
        need(a2 >= 1 and d2 <= 2, "the source map change must be a member addition: %d added, %d deleted lines (at most 2 deleted)" % (a2, d2))
        tf = git(root, "diff", "--name-only", base, "HEAD", "--", "infra/aws/terraform").strip()
        need(tf == "", "no Terraform file may change in this cell: %s" % tf[:120])
        mod = git(root, "diff", "--name-only", base, "HEAD", "--", MODULE_REL).strip()
        print("OK: additive: the handler gains %d lines and loses %d, the source map gains %d and loses %d, no Terraform file changes%s" %
              (add, dele, a2, d2, "; the module changed (named in the facts)" if mod else ""))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest(root):
    fc = [{"file": f, "sha256": "ab" * 32, "kind": "k"} for f in (HANDLER_REL, NEW_TEST_REL, SOURCE_MAP_REL)]

    def good():
        return {"firm": "49financial", "stage": {"handler_file": HANDLER_REL, "functions": ["compute_frv", "emit_frv"], "guarded_import": True, "after_stages": ["lots"], "words": "w"},
                "files_changed": json.loads(json.dumps(fc)),
                "source_map": {"file": SOURCE_MAP_REL, "entry": "e", "member_added": MODULE_REL, "pin": "written at the apply", "words": "w"},
                "iam": {"file": "infra/aws/terraform/investor-reporting/reporting-gold/iam.tf", "covers_new_prefix": True, "statement_ids": ["S"], "words": "w"},
                "schedule": {"file": "infra/aws/terraform/investor-reporting/reporting-gold/schedule.tf", "cron": "cron(41 7 ? * MON-FRI *)", "after_inputs": True, "trading_day_frontier": True, "words": "w"},
                "expected_plan": {"to_add": 0, "to_change": 1, "to_destroy": 0, "resources": ["aws_lambda_function"], "words": "w"},
                "write_path": {"table": "filled_report_values", "address_form": "opal_naming.address(...)", "partition": "date=<as_of>", "existing_prefixes_written": []},
                "tests": {"file": NEW_TEST_REL, "new_tests": 7, "dir_total": 103}, "names": {"from_builders": True, "words": "w"}, "words": "w", "claim": "measured",
                "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, sha="ab" * 32):
        try:
            return check_facts(rec, lambda rel: sha, lambda rel: True, lambda rel, token: True)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN arm failed")
    for mut, why in ((lambda r: r["files_changed"].pop(), "the source map missing"), (lambda r: r["expected_plan"].update(to_destroy=1), "a destroy"),
                     (lambda r: r["write_path"].update(existing_prefixes_written=["x"]), "an existing prefix written"), (lambda r: r["tests"].update(new_tests=3), "too few tests"),
                     (lambda r: r["names"].update(from_builders=False), "typed names"), (lambda r: r["stage"].update(guarded_import=False), "an unguarded import"),
                     (lambda r: r["files_changed"].append({"file": "infra/aws/terraform/x.tf", "sha256": "ab" * 32, "kind": "k"}), "a Terraform file"),
                     (lambda r: r.update(words="ids 1234567890"), "a digit run"), (lambda r: r.update(pushed=True), "a push flag"),
                     (lambda r: r["schedule"].update(after_inputs=False), "not after the inputs")):
        r = json.loads(json.dumps(good()))
        mut(r)
        need(grade(r) is False, "RED: " + why)
    need(grade(good(), sha="cd" * 32) is False, "RED: a sha256 that differs from the bytes must fail")
    print("selftest OK: 1 green and 11 red facts arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p120_hop1stage.py <repo_root> <criterion_id>")
            sys.exit(2)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
