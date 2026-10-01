"""AMGT_RESAPP round 52, AMGT-ab-6 -- grade the never-widen limbs 5, 6 and 7 MECHANICALLY over the
three capture manifests, so the verdict is a parser's and not an eye's.

WHICH COMPARISON EACH LIMB TAKES, and why they are not the same pair:
  limb 5 (/print, /timeline on the four names): ACROSS THE WHOLE ACT, pre-apply vs post-splice.
  limb 6 (lead-list rows):                      ACROSS THE WHOLE ACT, pre-apply vs post-splice.
  limb 7 (ASML drafted sections):               ACROSS THE SPLICE ONLY -- the half says "before vs
      after THE SPLICE", so the pair is post-apply-pre-splice vs post-splice. Grading limb 7 across
      the build instead would answer a question the half did not ask.

ATTRIBUTION (CTO half condition 1): a limb-5 /print move on a name whose newest model-block stamp
MOVED between the captures is attributed to CORPUS y-4 before it counts as a rollback; a /timeline
move is attributed to an AMGT_HARVST write the same way. The stamps are carried in each manifest, so
the attribution is exercisable rather than merely promised.

VOID (limb 6): if an axis's generation_id moved between the captures the comparison is VOID for that
axis rather than passing -- a new generation is entitled to rerank.

usage (repo root):  python <this> <captures_dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(d, name):
    return json.loads((Path(d) / name / "manifest.json").read_text(encoding="utf-8"))


def by_key(man):
    return {(r["name"], r["route"]): r for r in man["rows"]}


def main():
    base = Path(sys.argv[1])
    pre = load(base, "pre-apply")
    mid = load(base, "post-apply-pre-splice")
    post = load(base, "post-splice")
    P, M, Q = by_key(pre), by_key(mid), by_key(post)

    print("CAPTURES")
    for lbl, man in (("pre-apply", pre), ("post-apply-pre-splice", mid), ("post-splice", post)):
        print("  %-22s at %s  CodeSha %s  all_200=%s" % (lbl, man["captured_at"], man["code_sha256"][:16], man["all_200"]))

    fired = []

    # ---- limb 5: pre-apply vs post-splice, byte-equal ----
    print("\nLIMB 5 -- /print and /timeline OUTPUT byte-equal across the WHOLE act (pre-apply vs post-splice)")
    l5 = [k for k in P if P[k]["limb"] == "5"]
    for k in sorted(l5):
        a, b = P[k], Q[k]
        same = a["sha256"] == b["sha256"]
        nm = k[0]
        sa = pre["model_block_stamps"]["newest"][nm]["newest_stamp"]
        sb = post["model_block_stamps"]["newest"][nm]["newest_stamp"]
        stamp_moved = sa != sb
        verdict = "EQUAL" if same else ("MOVED -> ATTRIBUTED to a block write (%s -> %s)" % (sa, sb) if stamp_moved else "MOVED, stamp did NOT move -> ROLLBACK TRIGGER")
        print("  %-16s %-9s strict=%-5s %s  %s" % (nm, k[1], a["strict"], a["sha256"][:16], verdict))
        if not same and a["strict"] and not stamp_moved:
            fired.append("limb5 %s/%s" % k)
    print("  stamps unchanged across the act: %s" % (pre["model_block_stamps"]["newest"] == post["model_block_stamps"]["newest"]))

    # ---- limb 6: pre-apply vs post-splice, projection + generation ----
    print("\nLIMB 6 -- lead-list rank/score/order/name/places_moved, projection-graded, SAME generation")
    print("  graded fields: %s" % (pre["row_fields_graded"],))
    for k in sorted(kk for kk in P if P[kk]["limb"] == "6"):
        a, b = P[k], Q[k]
        gen_same = a.get("generation_id") == b.get("generation_id")
        proj_same = a.get("projection_sha256") == b.get("projection_sha256")
        if not gen_same:
            verdict = "VOID -- generation moved %s -> %s" % (a.get("generation_id"), b.get("generation_id"))
        elif proj_same:
            verdict = "EQUAL (rows %s)" % a.get("row_count")
        else:
            verdict = "PROJECTION MOVED -> ROLLBACK TRIGGER"
            fired.append("limb6 %s" % (k[0],))
        print("  %-26s gen=%-32s proj=%s  %s" % (k[0], str(a.get("generation_id")), (a.get("projection_sha256") or "NONE")[:16], verdict))

    # ---- limb 7: ACROSS THE SPLICE ONLY ----
    print("\nLIMB 7 -- ASML drafted sections byte-equal across THE SPLICE (post-apply-pre-splice vs post-splice)")
    k = ("ASML_NA_Equity", "thesis")
    a, b = M[k], Q[k]
    same = a.get("drafting_sha256") == b.get("drafting_sha256")
    print("  drafting block sha %s -> %s   sections %s -> %s   %s"
          % ((a.get("drafting_sha256") or "NONE")[:16], (b.get("drafting_sha256") or "NONE")[:16],
             a.get("drafted_section_count"), b.get("drafted_section_count"),
             "EQUAL" if same else "MOVED -> ROLLBACK TRIGGER"))
    if not same:
        fired.append("limb7 ASML drafted sections")
    print("  (for the record, across the BUILD too: %s -> %s)"
          % ((P[k].get("drafting_sha256") or "NONE")[:16], (a.get("drafting_sha256") or "NONE")[:16]))

    # ---- the chart, the CTO half's own post-act read ----
    print("\nCTO half condition 4 -- ASML thesis_driver_chart across the act")
    for lbl, mm in (("pre-apply", P), ("post-apply-pre-splice", M), ("post-splice", Q)):
        c = mm[k].get("chart") or {}
        print("  %-22s status=%-8s source=%-8s points_count=%s" % (lbl, c.get("status"), c.get("source"), c.get("points_count")))

    print("\nROLLBACK TRIGGERS FIRED: %d %s" % (len(fired), fired if fired else ""))
    return 0 if not fired else 1


if __name__ == "__main__":
    sys.exit(main())
