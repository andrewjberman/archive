"""IRPT_DASHBD round 147, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- FWD-10 cell (a): the Performance tab prints the source's unreported trading days, cell DB-c-25 (portal).

  DBC147-1-AC1 the new bun test file exists with the named title words, carries the three exact sentences, passes (0 failures, at least 6 tests)
  DBC147-1-AC2 the three fixtures equal the CONTRACT WRITER's fresh output byte for byte; the portal mirror equals the series contract (optional names, nullable income); iv-e-124 passes
  DBC147-1-AC3 the difference control (DashboardPerformance.tsx put back to its base makes the new tests FAIL, then is restored byte-identical) and the bounds (the portal diff stays inside the grant)

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
The AC2 fresh generation runs gen_fixture_r147.py in a child process with plain `python` (lib/trading_calendar needs the user site packages).
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

PORTAL_BASE = "03f92d82c23fc270e1115c15989e7637f430e16d"
IR = "src/pages/InvestorReporting/"
TEST = IR + "__tests__/irpt-dashbd/fwd10-unreported-days.test.tsx"
PARITY = IR + "__tests__/dsgn-irptv1/iv-e-124.series-contract.test.ts"
SOURCE = IR + "dashboard/DashboardPerformance.tsx"
MIRROR = IR + "dashboard/seriesContract.ts"
FIXTURES = IR + "__tests__/irpt-dashbd/fixtures/"
NAMES = ("series-unreported-days.json", "series-no-statement.json", "series-unreported-empty.json")
ALLOWED = (SOURCE, MIRROR, IR + "__tests__/irpt-dashbd/", IR + "__tests__/dsgn-irptv1/")
CONTRACT = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
GENERATOR = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~C2/checks/r147/gen_fixture_r147.py"
WORDS = ("unreported", "window", "absent", "empty", "income", "fixture")
SENTENCES = (
    "3 trading days not reported by the source: July 14th, 2026, July 15th, 2026 and August 5th, 2026.",
    "2 trading days not reported by the source: July 14th, 2026 and July 15th, 2026.",
    "1 trading day not reported by the source: August 5th, 2026.",
)


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
    need(all(s in txt for s in SENTENCES), "the test file does not carry every exact sentence: " + "; ".join(s for s in SENTENCES if s not in txt))
    r = run([bun(), "test", TEST], portal)
    p, f = counts(r.stdout + r.stderr)
    need(r.returncode == 0 and f == 0 and p >= 6, "bun test: rc=%s pass=%s fail=%s" % (r.returncode, p, f))


def optional_names(ts):
    m = re.search(r"SERIES_OPTIONAL\s*=\s*\[(.*?)\]", ts, re.S)
    need(m is not None, "SERIES_OPTIONAL is not an array literal in seriesContract.ts")
    return re.findall(r"""['"]([A-Za-z_]+)['"]""", m.group(1))


def ac_2(root):
    root = Path(root)
    portal = root / "portal"
    with tempfile.TemporaryDirectory() as tmp:
        py = shutil.which("python")
        need(py is not None, "python is not on the PATH")
        r = run([py, str(root / GENERATOR), str(root), tmp], root)
        need(r.returncode == 0, "the contract writer's generator failed: " + (r.stdout + r.stderr)[-300:])
        for name in NAMES:
            mine = portal / FIXTURES / name
            need(mine.is_file(), "fixture absent: " + name)
            need(mine.read_bytes() == (Path(tmp) / name).read_bytes(), "fixture differs from the writer's fresh output: " + name)
    contract = json.loads((root / CONTRACT).read_text(encoding="utf-8"))
    ts = (portal / MIRROR).read_text(encoding="utf-8")
    need(optional_names(ts) == contract["series"]["optional"], "SERIES_OPTIONAL %s != contract %s" % (optional_names(ts), contract["series"]["optional"]))
    need(re.search(r"readonly\s+income\s*:\s*readonly\s*\(\s*number\s*\|\s*null\s*\)\s*\[\]", ts) is not None, "income is not typed (number | null)[]")
    r = run([bun(), "test", PARITY], portal)
    p, f = counts(r.stdout + r.stderr)
    need(r.returncode == 0 and f == 0 and p >= 1, "iv-e-124: rc=%s pass=%s fail=%s" % (r.returncode, p, f))


def ac_3(root):
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
    head_txt = src.read_text(encoding="utf-8")
    need("calendar" not in head_txt.lower(), "DashboardPerformance.tsx names a calendar: the portal must not compute unreported days")


ARMS = {"DBC147-1-AC1": ac_1, "DBC147-1-AC2": ac_2, "DBC147-1-AC3": ac_3}


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
