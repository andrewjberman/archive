"""IRPT_DASHBD round 146, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- FWD-10 on the Performance tab: the partial-history sentence and the absent fallback footnote, cell DB-c-24 (portal).

  DBC146-1-AC1 the new bun test file exists with the named title words, passes (0 failures, at least 6 tests), and the record's printed sentence for 2026-07-10 is exactly "Returns from July 10, 2026."
  DBC146-1-AC2 the difference control (DashboardPerformance.tsx put back to its base version makes the new tests FAIL, then is restored byte-identical) and the bounds (the portal diff stays inside the grant)

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

PORTAL_BASE = "e578b378d332ad1505018be3801466dac7aeeade"
IR = "src/pages/InvestorReporting/"
TEST = IR + "__tests__/irpt-dashbd/fwd10-partial-history-and-no-fallback.test.tsx"
SOURCE = IR + "dashboard/DashboardPerformance.tsx"
ALLOWED = (IR + "dashboard/DashboardPerformance.tsx", IR + "dashboard/coverageWords.ts", IR + "__tests__/irpt-dashbd/", IR + "__tests__/dsgn-irptv1/")
RECORD = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~416/BUILD_R146.json"
WORDS = ("partial history", "first data date", "cause", "full", "fallback", "window")
SENTENCE = "Returns from July 10, 2026."
CAUSE = re.compile(r"because|since|empty|silver|source|custodian|black diamond|missing|gap|earlier days", re.I)


def run(cmd, cwd, timeout=110):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def bun():
    b = shutil.which("bun")
    need(b is not None, "bun is not on the PATH")
    return b


def counts(out):
    p = re.search(r"(\d+)\s+pass", out)
    f = re.search(r"(\d+)\s+fail", out)
    return (int(p.group(1)) if p else 0, int(f.group(1)) if f else 0)


def ac_1(root):
    root = Path(root)
    portal = root / "portal"
    t = portal / TEST
    need(t.is_file(), "the new test file is absent")
    txt = t.read_text(encoding="utf-8")
    titles = [m.group(2) for m in re.finditer(r"""\b(?:test|it)\(\s*(['"`])(.+?)\1""", txt)]
    need(len(titles) >= 6, "fewer than 6 test titles")
    joined = " | ".join(titles).lower()
    need(all(w in joined for w in WORDS), "a required title word is missing: " + ", ".join(w for w in WORDS if w not in joined))
    r = run([bun(), "test", TEST], portal)
    out = r.stdout + r.stderr
    p, f = counts(out)
    need(r.returncode == 0 and f == 0 and p >= 6, "bun test: rc=%s pass=%s fail=%s" % (r.returncode, p, f))
    rec = p114.load(root, RECORD)
    need(rec["partial_history_sentence_for_2026_07_10"] == SENTENCE, "the recorded sentence is not exactly: " + SENTENCE)


def ac_2(root):
    root = Path(root)
    portal = root / "portal"
    gd = run(["git", "-C", str(portal), "rev-parse", "--git-dir"], root).stdout.strip()
    cd = run(["git", "-C", str(portal), "rev-parse", "--git-common-dir"], root).stdout.strip()
    need(Path(gd).resolve() != Path(cd).resolve(), "refusing to run the difference control on a main checkout (only a linked worktree)")
    src = portal / SOURCE
    need(src.is_file(), "DashboardPerformance.tsx absent")
    mine = src.read_bytes()
    base = run(["git", "-C", str(portal), "show", "%s:%s" % (PORTAL_BASE, SOURCE)], root).stdout
    need(base != "" and base.encode("utf-8") != mine, "the worker did not change DashboardPerformance.tsx")
    try:
        src.write_bytes(base.encode("utf-8"))
        r = run([bun(), "test", TEST], portal)
        p, f = counts(r.stdout + r.stderr)
        need(r.returncode != 0 and f >= 2, "the difference control did not fail at least 2 tests (rc=%s fail=%s)" % (r.returncode, f))
    finally:
        src.write_bytes(mine)
    need(src.read_bytes() == mine, "the checker could not restore the worker's file")
    changed = [x for x in run(["git", "-C", str(portal), "diff", "--name-only", PORTAL_BASE, "HEAD"], root).stdout.splitlines() if x.strip()]
    need(changed, "the portal diff from the base is empty")
    extra = [x for x in changed if not any(x == a or (a.endswith("/") and x.startswith(a)) for a in ALLOWED)]
    need(not extra, "portal files outside the grant changed: " + ", ".join(extra[:5]))
    rec = p114.load(root, RECORD)
    need(rec["cause_words_found"] == 0 and not CAUSE.search(rec["partial_history_sentence_for_2026_07_10"]), "cause words in the sentence")
    need(rec["pushed"] is False and rec["deployed"] is False, "pushed or deployed is not false")


ARMS = {"DBC146-1-AC1": ac_1, "DBC146-1-AC2": ac_2}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
