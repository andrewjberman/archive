"""IRPT_DASHBD round 114, workstream ~F2 (issuer 2.0.0_SA_COO~F2) -- the F-SHIP first issuance.

  DB-f-501 (~501) the report READER (dashboard/report/reportRead.ts) and its mount in the Performance tab
                  (ReportingTab.tsx), portal branch only.                            DBF114-1-AC1 (reader), DBF114-1-AC2 (mount)
  DB-f-502 (~502) a READ of the serve path of the filled report (route, publisher, export path, hops with owners).
                  Nothing is written outside the worker's folder.                    DBF114-2-AC1

The checker grades FORM, runs the named bun tests in the worker's portal worktree (<root>/portal), and for the read
BINDS the record to the code it cites (a cited line must hold the token the record says it holds).

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
IR = "portal/src/pages/InvestorReporting/"
READER = IR + "dashboard/report/reportRead.ts"
TAB = IR + "tabs/reporting/ReportingTab.tsx"
T_READ = IR + "__tests__/irpt-dashbd/report-read.test.tsx"
T_MOUNT = IR + "__tests__/irpt-dashbd/report-tab-mount.test.tsx"
BASE_SHA = "c81d54ff31b0c44b45dabdd217b531a183723c8b"
ALLOWED = (
    "src/pages/InvestorReporting/dashboard/report/reportRead.ts",
    "src/pages/InvestorReporting/tabs/reporting/ReportingTab.tsx",
    "src/pages/InvestorReporting/__tests__/irpt-dashbd/report-read.test.tsx",
    "src/pages/InvestorReporting/__tests__/irpt-dashbd/report-tab-mount.test.tsx",
)
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~502/RD_REPORT_SERVE_PATH_R114.json"
CLAIMS = ("measured", "inferred", "held", "absent")
RISKS = ("LOCAL", "SERVED", "WORLD")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "path_template")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")
READER_TOKENS = ("export function reportReadPath", "export async function readReportAnswer", "export type ReportAnswer",
                 "/reporting/client/", "/report")
MOUNT_TOKENS = ("reportRead'", "dashboard/report/PerformanceReport'", "export function reportFor",
                'data-slot="reporting-report"', "readReportAnswer(")
READ_TITLE_WORDS = ("path", "served", "refus", "throw", "unreadable", "tenant")
MOUNT_TITLE_WORDS = ("same client", "other client", "absent", "fixture", "falls back")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def missing_tokens(text, tokens):
    return [t for t in tokens if t not in text]


def titles_of(text):
    return [m.group(2) for m in re.finditer(r"""\b(?:test|it)\(\s*(['"`])(.+?)\1""", text)]


def missing_title_words(titles, words):
    low = " | ".join(titles).lower()
    return [w for w in words if w not in low]


def bun_result(out):
    fails = re.findall(r"^\s*(\d+) fail", out, re.M)
    passes = re.findall(r"^\s*(\d+) pass", out, re.M)
    return (int(passes[-1]) if passes else 0), (int(fails[-1]) if fails else -1)


def run_bun(root, test_rel):
    bun = shutil.which("bun")
    need(bun is not None, "bun not on PATH")
    portal = Path(root) / "portal"
    rel = test_rel[len("portal/"):]
    p = subprocess.run([bun, "test", rel], cwd=str(portal), capture_output=True, text=True, timeout=100)
    out = (p.stdout or "") + (p.stderr or "")
    passes, fails = bun_result(out)
    need(p.returncode == 0 and fails == 0, "bun test %s rc=%s fail=%s" % (rel, p.returncode, fails))
    return passes


def read_text(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "missing file " + rel)
    return p.read_text(encoding="utf-8")


def ac_reader(root):
    text = read_text(root, READER)
    miss = missing_tokens(text, READER_TOKENS)
    need(not miss, "reader lacks " + repr(miss))
    ttl = titles_of(read_text(root, T_READ))
    mt = missing_title_words(ttl, READ_TITLE_WORDS)
    need(not mt, "reader test titles lack " + repr(mt))
    passes = run_bun(root, T_READ)
    need(passes >= 6, "reader tests pass %d < 6" % passes)


def changed_files(root):
    p = subprocess.run(["git", "-C", str(Path(root) / "portal"), "diff", "--name-only", BASE_SHA + "..HEAD"],
                       capture_output=True, text=True, timeout=60)
    need(p.returncode == 0, "git diff rc=%s" % p.returncode)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def outside_allowed(files):
    return [f for f in files if f not in ALLOWED]


def ac_mount(root):
    text = read_text(root, TAB)
    miss = missing_tokens(text, MOUNT_TOKENS)
    need(not miss, "tab lacks " + repr(miss))
    ttl = titles_of(read_text(root, T_MOUNT))
    mt = missing_title_words(ttl, MOUNT_TITLE_WORDS)
    need(not mt, "mount test titles lack " + repr(mt))
    passes = run_bun(root, T_MOUNT)
    need(passes >= 5, "mount tests pass %d < 5" % passes)
    out = outside_allowed(changed_files(root))
    need(not out, "files changed outside the grant: " + repr(out))


def digits_ok(obj, key=""):
    if isinstance(obj, dict):
        return all(digits_ok(v, k) for k, v in obj.items())
    if isinstance(obj, list):
        return all(digits_ok(v, key) for v in obj)
    if isinstance(obj, str) and LONG_DIGITS.search(obj) and key not in DIGIT_OK_KEYS:
        return False
    return True


def claim_ok(d):
    return isinstance(d, dict) and d.get("claim") in CLAIMS


def cites(root, d, tokens):
    f, line = d.get("file"), d.get("line")
    if not (isinstance(f, str) and isinstance(line, int) and not isinstance(line, bool)):
        return False
    p = Path(root) / f
    if not p.is_file():
        return False
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    if not (1 <= line <= len(lines)):
        return False
    return any(t in lines[line - 1].lower() for t in tokens)


def record_problems(root, rec):
    pr = []
    keys = ("as_of", "route", "publisher", "report_object", "hops", "export_path", "proposed_route", "reads",
            "files_in_repo", "served_values_changed", "pushed", "deployed")
    if not isinstance(rec, dict) or sorted(rec.keys()) != sorted(keys):
        return ["top-level fields are not exactly " + repr(keys)]
    if not (isinstance(rec["as_of"], str) and ISO.match(rec["as_of"])):
        pr.append("as_of not an ISO date")
    r = rec["route"]
    if not (claim_ok(r) and isinstance(r.get("path_template"), str) and "reporting" in r["path_template"]):
        pr.append("route form")
    elif not cites(root, r, ("manifest", "series", "summary", "reporting")):
        pr.append("route citation does not hold a reporting token")
    pu = rec["publisher"]
    if not claim_ok(pu):
        pr.append("publisher form")
    elif not cites(root, pu, ("manifest", "series", "summary", "platinum")):
        pr.append("publisher citation does not hold a platinum token")
    ro = rec["report_object"]
    if not (claim_ok(ro) and isinstance(ro.get("exists_in_platinum"), bool) and isinstance(ro.get("producer_exists"), bool)
            and isinstance(ro.get("words"), str) and ro["words"]):
        pr.append("report_object form")
    hops = rec["hops"]
    if not (isinstance(hops, list) and len(hops) >= 4):
        pr.append("hops fewer than 4")
    else:
        for i, h in enumerate(hops):
            ok = (isinstance(h, dict) and h.get("hop") == i + 1 and isinstance(h.get("what"), str) and h["what"]
                  and isinstance(h.get("owner"), str) and h["owner"] and h.get("risk") in RISKS
                  and isinstance(h.get("exists_today"), bool))
            if not ok:
                pr.append("hop %d form" % (i + 1))
    ep = rec["export_path"]
    if not (claim_ok(ep) and isinstance(ep.get("words"), str) and ep["words"] and isinstance(ep.get("reads_report_today"), bool)):
        pr.append("export_path form")
    elif not cites(root, ep, ("export", "bundle", "render", "performance_source", "print")):
        pr.append("export citation does not hold an export token")
    prt = rec["proposed_route"]
    if not (isinstance(prt, dict) and isinstance(prt.get("path_template"), str) and "report" in prt["path_template"]
            and isinstance(prt.get("words"), str) and prt["words"]):
        pr.append("proposed_route form")
    rd = rec["reads"]
    if rd != {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}:
        pr.append("reads block is not the all-zero form")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if rec[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(rec):
        pr.append("a run of 8 or more digits outside the exempt fields")
    return pr


def ac_read(root):
    p = Path(root) / REC_REL
    need(p.is_file(), "missing record " + REC_REL)
    rec = json.loads(p.read_text(encoding="utf-8"))
    pr = record_problems(root, rec)
    need(not pr, "; ".join(pr))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("tokens-green", missing_tokens("a b c", ("a", "c")), [])
    arm("tokens-red", missing_tokens("a b", ("a", "c")), ["c"])
    src = "test('reads the path', () => {})\nit(\"served and refused\", () => {})"
    arm("titles", titles_of(src), ["reads the path", "served and refused"])
    arm("title-words-green", missing_title_words(["Path of tenant", "served", "refusal", "throws", "unreadable"], READ_TITLE_WORDS), [])
    arm("title-words-red", missing_title_words(["only served"], READ_TITLE_WORDS), ["path", "refus", "throw", "unreadable", "tenant"])
    arm("bun-green", bun_result("\n 7 pass\n 0 fail\n"), (7, 0))
    arm("bun-red", bun_result("\n 7 pass\n 2 fail\n"), (7, 2))
    arm("bun-none", bun_result("nothing"), (0, -1))
    arm("allowed-green", outside_allowed(list(ALLOWED)), [])
    arm("allowed-red", outside_allowed([ALLOWED[0], "src/App.tsx"]), ["src/App.tsx"])
    arm("digits-red", digits_ok({"words": "id 12345678901"}), False)
    arm("digits-green", digits_ok({"sha256": "12345678901", "n": 3}), True)
    arm("form-red", record_problems(".", {"as_of": "x"})[0].startswith("top-level"), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF114-1-AC1": ac_reader, "DBF114-1-AC2": ac_mount, "DBF114-2-AC1": ac_read}
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
