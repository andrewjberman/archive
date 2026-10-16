"""IRPT_DASHBD round 150, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the page mirror takes on series contract 0.3.3 (history_scope_claim and history_scope_basis), cell DB-c-30 (portal).

  DBC151-1-AC1 SERIES_OPTIONAL equals the contract's series.optional in order (eight names); SeriesDocument declares history_scope_claim and history_scope_basis as optional strings;
               iv-e-124 and the round-147 unreported-days test pass (0 failures)
  DBC151-1-AC2 the difference control (seriesContract.ts put back to its base makes iv-e-124 FAIL, then is restored byte-identical) and the bounds (the portal diff touches only seriesContract.ts and the test folders; DashboardPerformance.tsx is untouched)

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import importlib.util
import json
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

PORTAL_BASE = "34a6baf8657bb166676dc3b8c3eec97ee8d3e585"
IR = "src/pages/InvestorReporting/"
MIRROR = IR + "dashboard/seriesContract.ts"
SENTENCE_SRC = IR + "dashboard/DashboardPerformance.tsx"
PARITY = IR + "__tests__/dsgn-irptv1/iv-e-124.series-contract.test.ts"
UNREPORTED = IR + "__tests__/irpt-dashbd/fwd10-unreported-days.test.tsx"
ALLOWED = (MIRROR, IR + "__tests__/irpt-dashbd/", IR + "__tests__/dsgn-irptv1/")
CONTRACT = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"


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


def optional_names(ts):
    m = re.search(r"SERIES_OPTIONAL\s*=\s*\[(.*?)\]", ts, re.S)
    need(m is not None, "SERIES_OPTIONAL is not an array literal in seriesContract.ts")
    return re.findall(r"""['"]([A-Za-z_]+)['"]""", m.group(1))


def ac_1(root):
    root = Path(root)
    portal = root / "portal"
    contract = json.loads((root / CONTRACT).read_text(encoding="utf-8"))
    need(contract["contract_version"] == "0.3.3", "the trunk contract in this tree reads %s, not 0.3.3" % contract["contract_version"])
    ts = (portal / MIRROR).read_text(encoding="utf-8")
    need(optional_names(ts) == contract["series"]["optional"], "SERIES_OPTIONAL %s != contract %s" % (optional_names(ts), contract["series"]["optional"]))
    need(re.search(r"readonly\s+history_scope_claim\?\s*:\s*string", ts) is not None, "SeriesDocument does not declare history_scope_claim?: string")
    need(re.search(r"readonly\s+history_scope_basis\?\s*:\s*string", ts) is not None, "SeriesDocument does not declare history_scope_basis?: string")
    r = run([bun(), "test", PARITY, UNREPORTED], portal)
    p, f = counts(r.stdout + r.stderr)
    need(r.returncode == 0 and f == 0 and p >= 9, "iv-e-124 and the unreported-days test: rc=%s pass=%s fail=%s" % (r.returncode, p, f))


def ac_2(root):
    root = Path(root)
    portal = root / "portal"
    gd = run(["git", "-C", str(portal), "rev-parse", "--git-dir"], root).stdout.strip()
    cd = run(["git", "-C", str(portal), "rev-parse", "--git-common-dir"], root).stdout.strip()
    need(Path(gd).resolve() != Path(cd).resolve(), "refusing to run the difference control on a main checkout (only a linked worktree)")
    src = portal / MIRROR
    mine = src.read_bytes()
    base = run(["git", "-C", str(portal), "show", "%s:%s" % (PORTAL_BASE, MIRROR)], root).stdout
    need(base != "" and base.encode("utf-8") != mine, "the worker did not change seriesContract.ts")
    try:
        src.write_bytes(base.encode("utf-8"))
        r = run([bun(), "test", PARITY], portal)
        p, f = counts(r.stdout + r.stderr)
        need(r.returncode != 0 and f >= 1, "the difference control did not fail iv-e-124 (rc=%s fail=%s)" % (r.returncode, f))
    finally:
        src.write_bytes(mine)
    need(src.read_bytes() == mine, "the checker could not restore the worker's file")
    changed = [x for x in run(["git", "-C", str(portal), "diff", "--name-only", PORTAL_BASE, "HEAD"], root).stdout.splitlines() if x.strip()]
    need(changed, "the portal diff from the base is empty")
    extra = [x for x in changed if not any(x == a or (a.endswith("/") and x.startswith(a)) for a in ALLOWED)]
    need(not extra, "portal files outside the grant changed: " + ", ".join(extra[:5]))
    need(SENTENCE_SRC not in changed, "DashboardPerformance.tsx changed: this cell edits the mirror only")


ARMS = {"DBC151-1-AC1": ac_1, "DBC151-1-AC2": ac_2}


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
