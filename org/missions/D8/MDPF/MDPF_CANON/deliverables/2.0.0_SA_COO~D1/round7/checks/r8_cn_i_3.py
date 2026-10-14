#!/usr/bin/env python3
"""r8_cn_i_3.py -- the issuer's checks for MDPF_CANON CN-i-3: the Global AUA Trend returns to PROD's text, every other scope keeps the candidate's.

The reference points, all commits of the portal repository (the worker's nested portal worktree shares their objects):
  PROD  = 5ab67a65     the current portal PROD head (the Trend Andrew wants at Global)
  CAND  = f8c7d310     PROD plus the three feature commits (CN-i-1, CN-l-2, CN-i-2); the same patches as fd5433a3, rebuilt on this PROD

  python r8_cn_i_3.py sites    arms P1 P2
  python r8_cn_i_3.py scope    arms S1 S2
  python r8_cn_i_3.py selftest

P1 every line the feature REMOVED from src/pages/ModelPortfolios.tsx (PROD's own Trend text) is present in the file at HEAD, as a trimmed line.
P2 every line the feature ADDED to it is still present at HEAD, except the lines that name the boundary note (the note is dropped at Global and is dead code elsewhere).
   P1 and P2 together say: both texts exist; the per-scope choice between them is the gate, which the issuer's render diff proves (this check is source-level).
S1 the files that differ between CAND and HEAD are exactly src/pages/ModelPortfolios.tsx, and optionally src/lib/trendGrouping.ts.
S2 CategoryViewTree.tsx, portal-proxy.ts, otherModelsAsOf.ts and aum.ts are byte-equal to CAND (the lime colour, the as-of text and its types stay).
Prints counts, never a client figure. Exit 0 only when every arm of the mode passes.
"""
import os
import subprocess
import sys

PROD = "5ab67a65"
CAND = "f8c7d310"
MP = "src/pages/ModelPortfolios.tsx"
SAME_AS_CAND = ("src/components/CategoryViewTree.tsx", "src/api/portal-proxy.ts", "src/lib/otherModelsAsOf.ts", "src/api/endpoints/aum.ts")
NOTE_TOKENS = ("detailNote", "trendDetailNote", "data-trend-detail-note")


def _root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else os.getcwd()


def _git(portal, *args):
    r = subprocess.run(["git", "-C", portal] + list(args), capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r", "")


def _lines(text):
    return [ln.strip() for ln in text.split("\n")]


def _diff_lines(portal):
    rc, out = _git(portal, "diff", "-U0", PROD, CAND, "--", MP)
    if rc != 0:
        raise SystemExit("REFUSED: cannot diff %s..%s in %s (rc %d)" % (PROD, CAND, portal, rc))
    rem, add = [], []
    for ln in out.split("\n"):
        if ln.startswith("---") or ln.startswith("+++"):
            continue
        if ln.startswith("-") and ln[1:].strip():
            rem.append(ln[1:].strip())
        elif ln.startswith("+") and ln[1:].strip():
            add.append(ln[1:].strip())
    return rem, add


def sites(portal):
    rem, add = _diff_lines(portal)
    rc, head = _git(portal, "show", "HEAD:" + MP)
    have = set(_lines(head))
    arms = []
    miss = [x for x in rem if x not in have]
    arms.append(("P1", not miss and len(rem) > 0, "%d PROD line(s) the feature removed; %d missing at HEAD" % (len(rem), len(miss))))
    add_chk = [x for x in add if not any(t in x for t in NOTE_TOKENS)]
    miss2 = [x for x in add_chk if x not in have]
    arms.append(("P2", not miss2 and len(add_chk) > 0, "%d candidate line(s) checked (%d note line(s) exempt); %d missing at HEAD" % (
        len(add_chk), len(add) - len(add_chk), len(miss2))))
    return arms, miss, miss2


def scope(portal):
    rc, names = _git(portal, "diff", "--name-only", CAND, "HEAD")
    changed = sorted(n for n in names.split("\n") if n.strip())
    allowed = {MP, "src/lib/trendGrouping.ts"}
    arms = [("S1", MP in changed and set(changed) <= allowed, "files changed since CAND: %s (allowed: %s, and trendGrouping.ts optionally)" % (changed, MP))]
    bad = []
    for p in SAME_AS_CAND:
        a = _git(portal, "rev-parse", CAND + ":" + p)[1].strip()
        b = _git(portal, "rev-parse", "HEAD:" + p)[1].strip()
        if a != b or not a:
            bad.append(p)
    arms.append(("S2", not bad, "%d protected file(s) byte-equal to CAND; differing: %s" % (len(SAME_AS_CAND) - len(bad), bad)))
    return arms


def _print(title, arms):
    k = sum(1 for _n, ok, _d in arms if ok)
    for n, ok, d in arms:
        print("  %s %s: %s" % (n, "PASS" if ok else "FAIL", d))
    print("ROUND 8 CN-I-3 %s: %d of %d arms" % (title, k, len(arms)))
    return 0 if k == len(arms) else 1


def selftest():
    # the arm logic over synthetic line sets: a missing PROD line and a dropped candidate line must each turn red
    def p1(rem, have):
        return not [x for x in rem if x not in have] and len(rem) > 0
    ok = p1(["a", "b"], {"a", "b", "c"}) and not p1(["a", "b"], {"a"}) and not p1([], {"a"})
    print("  selftest P1 logic (green, missing line red, empty set red): %s" % ok)
    print("ROUND 8 CN-I-3 SELFTEST: %s" % ("OK" if ok else "RED"))
    return 0 if ok else 1


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    if mode == "selftest":
        return selftest()
    portal = os.path.join(_root(), "portal")
    if mode == "sites":
        arms, _m1, _m2 = sites(portal)
        return _print("SITES", arms)
    if mode == "scope":
        return _print("SCOPE", scope(portal))
    print("usage: r8_cn_i_3.py sites|scope|selftest")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
