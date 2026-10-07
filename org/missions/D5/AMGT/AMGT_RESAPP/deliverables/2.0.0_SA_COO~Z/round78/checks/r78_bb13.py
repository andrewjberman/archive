"""AMGT_RESAPP round 78 -- AMGT-bb-13: Peers V below three peers (row AMGT_RESAPP-Z-S162 part 3).

  --crit AC1|AC2|AC3 --where local

Andrew's word, 2026-10-07 (ledger/CTO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md ADDENDUM 2, card 2): with fewer than 3
peers every Peers V measure reads not available with a reason naming the count ("2 peers; 3 are needed"); it is never
a value computed on 1 or 2. Proof: a plant at 2 peers and one at 3.

AC1 (build, with its difference control):
    C1 plants at 0, 1 and 2 peers: no score, all six measures not available, and the score's reason and every
       measure's reason are the count sentence ("0 peers; 3 are needed", "1 peer; 3 are needed", "2 peers; 3 are needed");
    C2 the count sentence carries none of the old status words or symbols;
    C3 the control at 3 peers: the count sentence is NOT used (three is enough to pass this rule; the older floors,
       unchanged, still say why no score is shown);
    C4 the control at 8 peers: the same score as before this cell (-1.0823626487770477 on the planted set).
AC2 (bound, must hold before and after): the ruled floors are unchanged (8 peers for the score, 3 measures, 6 peers
    per measure) and the two existing test files for this score pass.
AC3 (build): the plant tests in lib/research/scores/tests/test_peers_v_short_set.py pass.
Verdict: R78 BB13 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

TEST = "lib/research/scores/tests/test_peers_v_short_set.py"
EXISTING = ("lib/research/scores/tests/test_peers_v_mapping.py", "lib/research/api/tests/test_score_modules.py")
OLD_WORDS = ("|K|", "|M|", "suppressed", "dropped", "ABSENT", "need >=")
SENTENCE = {0: "0 peers; 3 are needed", 1: "1 peer; 3 are needed", 2: "2 peers; 3 are needed"}
V_AT_EIGHT = -1.0823626487770477


def _row(v):
    return {"factors": {"fcfy": v, "ey_ntm": v + 1, "shldr_yield": v + 2, "peg_ntm": 1.5}}


def _plant(peers_v, n):
    return peers_v.score_peers_v(_row(4.0), {"P%d" % i: _row(3.0 + i) for i in range(n)}, subject_key="S")


def _reasons(out):
    measures = out.get("measures") or {}
    return [(m.get("absent_reason") if isinstance(m, dict) else None) for m in measures.values()]


def _pytest(paths):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + list(paths), capture_output=True,
                       timeout=100)
    tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
    print("   " + tail)
    return p.returncode == 0 and " passed" in tail and "failed" not in tail, "rc=%d" % p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        if not os.path.isfile(TEST):
            clause("C1 the plant test file exists", False, TEST)
            return verdict(a, ok)
        passed, detail = _pytest([TEST])
        clause("C1 every plant case passes", passed, detail)
        return verdict(a, ok)

    from lib.research.scores import peers_v

    if a.crit == "AC2":
        floors = (peers_v.MIN_PEERS_FOR_V, peers_v.MIN_MEASURES_FOR_V, peers_v.MIN_PEERS_PER_MEASURE)
        clause("C1 the ruled floors are unchanged", floors == (8, 3, 6), repr(floors))
        passed, detail = _pytest(EXISTING)
        clause("C2 the existing tests of this score pass", passed, detail)
        return verdict(a, ok)

    short_ok, seen = [], []
    for n in (0, 1, 2):
        out = _plant(peers_v, n)
        reasons = _reasons(out)
        print("   plant at %d: score %r; reason %r; measure reasons %s" % (n, out.get("V"), out.get("absent_reason"), sorted(set(map(str, reasons)))))
        seen.extend([out.get("absent_reason")] + reasons)
        short_ok.append(out.get("V") is None and len(reasons) == 6 and out.get("absent_reason") == SENTENCE[n]
                        and out.get("reason") == SENTENCE[n] and all(r == SENTENCE[n] for r in reasons)
                        and (out.get("M") or []) == [])
    clause("C1 below 3 peers the score and all six measures read the count sentence", all(short_ok))
    clause("C2 the count sentence carries no status word or symbol",
           all(isinstance(r, str) and not any(w in r for w in OLD_WORDS) for r in seen))
    three = _plant(peers_v, 3)
    three_reasons = [three.get("absent_reason")] + _reasons(three)
    print("   plant at 3: score %r; reason %r" % (three.get("V"), three.get("absent_reason")))
    clause("C3 at 3 peers the count sentence is not used",
           all(isinstance(r, str) and "are needed" not in r for r in three_reasons) and three.get("K") == 3)
    eight = _plant(peers_v, 8)
    value = eight.get("V")
    clause("C4 at 8 peers the score is the same as before",
           isinstance(value, float) and abs(value - V_AT_EIGHT) < 1e-12 and eight.get("state") == "MEASURED", repr(value))
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB13 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
