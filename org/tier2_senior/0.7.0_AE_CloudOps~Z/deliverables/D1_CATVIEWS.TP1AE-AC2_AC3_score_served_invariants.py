"""TP1AE-AC2 / AC3 scorer: D1-inv-2 and D1-inv-4 on the SERVED artifact.

Scores the two criteria that became measurable when the 13:50Z SCHEDULED publisher
fire landed category-views on the served plane. Reads the FETCHED BYTES, never a
producer's self-report.

    usage:  python D1_CATVIEWS.TP1AE-AC2_AC3_score_served_invariants.py [--self-test]

AC2 / D1-inv-2  the five gold-plane peers sum to total_aua, PER FIRM, denominator printed.
AC3 / D1-inv-4  L0 values sum to (total_aua - Insurance), and EVERY L1 set sums to its
                L0 parent, with member counts exhibited.

TWO THINGS THE CRITERIA DEMAND THAT A NAIVE SUM WOULD MISS, both implemented:

  1. "An L1 set that sums because it is EMPTY is not a pass."  A node with zero
     children trivially satisfies any sum. Those are counted and reported SEPARATELY
     as VACUOUS, never folded into the pass tally.

  2. "Report that the invariant is UNENFORCED."  D1-inv-4 has no guard in the
     producer (measured by 0.4.0_DS_ClientPlatform~Z). A passing VALUE behind NO
     GUARD is a different state from a guarded one, so the verdict says which it is.
     This scorer OBSERVES; it does not convert observation into enforcement.

TOLERANCE: exact-to-the-cent (0.005) on float sums. Stated rather than assumed,
because a tolerance chosen to make today's numbers pass is not a control.
"""
from __future__ import annotations

import json
import sys

import boto3

BUCKET = "opal-data-portal-v2"
SCOPES = ("global", "49financial", "inflection", "cottonwood")
KEY = "platinum/mdpf/{scope}/category-views.json"
TOL = 0.005

# D1-inv-4 has NO producer-side guard. Measured by 0.4.0_DS_ClientPlatform~Z and
# carried here because AC3 requires the scorer to SAY SO, not merely to pass.
INV4_ENFORCED = False

s3 = boto3.client("s3", region_name="us-east-1")


def fetch(scope: str):
    r = s3.get_object(Bucket=BUCKET, Key=KEY.format(scope=scope))
    raw = r["Body"].read()
    return json.loads(raw), len(raw), r["LastModified"]


def score_scope(scope: str, doc: dict) -> tuple:
    """Return (ac2_rows, ac3_rows, vacuous_rows) for one served body."""
    ac2, ac3, vac = [], [], []
    nodes = doc.get("nodes", {})
    sums = doc.get("sums", {})
    total = sums.get("total_aua")

    # ---- AC2 / D1-inv-2: the gold-plane peers sum to total_aua
    peer_aums = {n: (v or {}).get("aum") for n, v in nodes.items()}
    named = {n: a for n, a in peer_aums.items() if a is not None}
    peer_sum = sum(named.values())
    ok = total is not None and abs(peer_sum - total) <= TOL
    ac2.append({
        "scope": scope, "pass": ok,
        "denominator": len(peer_aums), "summed": len(named),
        "peers": sorted(peer_aums), "peer_sum": peer_sum, "total_aua": total,
        "delta": None if total is None else peer_sum - total,
    })

    # ---- AC3 / D1-inv-4: L0 sum to total - Insurance, and each L1 set to its parent
    ins = (nodes.get("Insurance") or {}).get("aum") or 0.0
    l0_sum = sum(a for n, a in named.items() if n != "Insurance")
    expect_l0 = None if total is None else total - ins
    ac3.append({
        "scope": scope, "level": "L0", "node": "(all peers less Insurance)",
        "pass": expect_l0 is not None and abs(l0_sum - expect_l0) <= TOL,
        "members": len([n for n in named if n != "Insurance"]),
        "got": l0_sum, "want": expect_l0,
        "delta": None if expect_l0 is None else l0_sum - expect_l0,
    })
    for name, node in sorted(nodes.items()):
        kids = (node or {}).get("children") or {}
        parent = (node or {}).get("aum")
        if not kids:
            vac.append({"scope": scope, "node": name,
                        "why": "no children -- an EMPTY L1 set sums trivially"})
            continue
        kid_sum = sum((k or {}).get("aum") or 0.0 for k in kids.values())
        ac3.append({
            "scope": scope, "level": "L1", "node": name,
            "pass": parent is not None and abs(kid_sum - parent) <= TOL,
            "members": len(kids), "got": kid_sum, "want": parent,
            "delta": None if parent is None else kid_sum - parent,
        })
    return ac2, ac3, vac


def self_test() -> int:
    """A checker that cannot report a violation is not a checker."""
    print("SELF-TEST: a hand-built body whose peers DO NOT sum, and one whose L1 set")
    print("           is EMPTY. The scorer MUST refuse the first and refuse to count")
    print("           the second as a pass.")
    good = {"nodes": {"A": {"aum": 10.0}, "B": {"aum": 5.0, "children": {"x": {"aum": 5.0}}}},
            "sums": {"total_aua": 15.0}}
    bad = {"nodes": {"A": {"aum": 10.0}, "B": {"aum": 5.0, "children": {"x": {"aum": 4.0}}}},
           "sums": {"total_aua": 99.0}}
    g2, g3, gv = score_scope("CTL", good)
    b2, b3, bv = score_scope("MUT", bad)
    ctl_ok = g2[0]["pass"] and all(r["pass"] for r in g3)
    mut_ac2_refuses = not b2[0]["pass"]
    mut_ac3_refuses = any(not r["pass"] for r in b3)
    print(f"  CONTROL arm  AC2 pass={g2[0]['pass']}  AC3 all pass={all(r['pass'] for r in g3)}"
          f"  (both MUST be True)")
    print(f"  MUTANT  arm  AC2 refuses={mut_ac2_refuses}  AC3 refuses={mut_ac3_refuses}"
          f"  (both MUST be True)")
    print(f"  VACUOUS detection: control found {len(gv)} empty-L1 node(s) "
          f"(node A has no children -- MUST be >=1)")
    ok = ctl_ok and mut_ac2_refuses and mut_ac3_refuses and len(gv) >= 1
    print("SELF-TEST " + ("PASS -- silent when correct, refuses when corrupted."
                          if ok else "FAIL -- the checker cannot discriminate. REFUSING."))
    return 0 if ok else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    all2, all3, allv, meta = [], [], [], []
    for scope in SCOPES:
        try:
            doc, nbytes, lm = fetch(scope)
        except Exception as exc:
            print(f"  INDETERMINATE {scope}: {type(exc).__name__}: {exc}")
            return 2
        meta.append((scope, nbytes, lm, doc.get("as_of")))
        a2, a3, v = score_scope(scope, doc)
        all2 += a2
        all3 += a3
        allv += v

    print("== TP1AE-AC2 / AC3: D1-inv-2 and D1-inv-4 ON THE SERVED ARTIFACT ==")
    print("   (fetched bytes, s3api UTC LastModified -- never a producer self-report)")
    for scope, nbytes, lm, as_of in meta:
        print(f"   {scope:12} {nbytes:>7} B  LastModified {lm:%Y-%m-%dT%H:%M:%SZ}  as_of {as_of}")

    print()
    print(f"AC2 / D1-inv-2 -- gold-plane peers sum to total_aua. DENOMINATOR {len(all2)} scope(s)")
    for r in all2:
        verdict = "PASS" if r["pass"] else "FAIL"
        print(f"  [{verdict}] {r['scope']:12} {r['summed']} of {r['denominator']} peers carry aum"
              f"  sum={r['peer_sum']:.2f} total_aua={r['total_aua']:.2f} delta={r['delta']:+.2f}")
        print(f"           peers: {r['peers']}")

    print()
    print(f"AC3 / D1-inv-4 -- L0 to total-Insurance, and each L1 set to its parent."
          f" DENOMINATOR {len(all3)} assertion(s)")
    for r in all3:
        verdict = "PASS" if r["pass"] else "FAIL"
        print(f"  [{verdict}] {r['scope']:12} {r['level']:3} {r['node']:26}"
              f" members={r['members']:2} got={r['got']:.2f} want={r['want']:.2f}"
              f" delta={r['delta']:+.2f}")

    print()
    print(f"VACUOUS L1 SETS -- NOT counted as passes ({len(allv)}):")
    for v in allv:
        print(f"    {v['scope']:12} {v['node']:20} {v['why']}")

    f2 = [r for r in all2 if not r["pass"]]
    f3 = [r for r in all3 if not r["pass"]]
    print()
    print(f"SCORED  AC2 {len(all2)-len(f2)}/{len(all2)} PASS   "
          f"AC3 {len(all3)-len(f3)}/{len(all3)} PASS   "
          f"VACUOUS {len(allv)} (excluded from both tallies)")
    print(f"WARN: D1-inv-4 ENFORCEMENT: {'GUARDED' if INV4_ENFORCED else 'UNENFORCED'}"
          " in the producer -- AC3 requires this be SAID, not merely passed."
          " A passing VALUE behind NO GUARD is a different state from a guarded one,"
          " and nothing here converts observation into enforcement.")
    if f2 or f3:
        print("VERDICT: REFUSED")
        return 1
    print("VERDICT: AC2 and AC3 PASS on the served artifact.")
    print("BOUND: scores AC2/AC3 only. AC1 discharged by 2.0.0_SA_COO~Z 2026-08-28T13:52:37Z;"
          " AC4 scored separately; AC5 measured @e43f37395c; AC6 is a claim-hygiene criterion"
          " over the whole face and is not scoreable by this instrument.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
