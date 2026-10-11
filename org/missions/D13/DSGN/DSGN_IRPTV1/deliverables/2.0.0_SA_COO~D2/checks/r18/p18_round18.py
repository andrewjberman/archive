"""DSGN_IRPTV1 round 18 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4798: DSGN_IRPTV1 owns the wire folder's regeneration.

Cell: IV-e-98 the generated wire folder holds generator output and nothing else; every hand-added export is emitted by the generator or
moved to a file outside the folder that its consumers import; the two generators run by one command; the drift test covers both.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV98-AC1  ~54/WIRE_REGEN.json: hand_exports non-empty, each {name, was_in, disposition GENERATOR_EMITS or MOVED_OUTSIDE, now_in,
            consumers (int >= 0)}; a MOVED_OUTSIDE now_in is not under the generated folder; hand_edits_left_in_generated == 0;
            one_command {command, runs} whose runs names both gen-wire and gen-consumed; generated_folder stated.
  IV98-AC2  the same record: drift {test_id, covers naming both generators, passes true, mutant {what, failed true}};
            typecheck_errors == 0; ive26 {outcome FIXED or NOT_FIXED with a reason}; suite_after.new_failing_ids == [];
            product_files_changed non-empty; portal_commit hex.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~54/"
HEX = re.compile(r"^[0-9a-f]{7,40}$")
GENS = ("gen-wire", "gen-consumed")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV18"))
        sys.exit(1)

    def text(v):
        return str(v or "").strip()

    p = root / (D + "WIRE_REGEN.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    if cid == "IV98-AC1":
        gf = text(r.get("generated_folder")).replace("\\", "/").rstrip("/")
        he = r.get("hand_exports") or []
        if not gf or not he:
            fail("generated_folder or hand_exports missing")
        for x in he:
            if not text(x.get("name")) or not text(x.get("was_in")) or x.get("disposition") not in ("GENERATOR_EMITS", "MOVED_OUTSIDE") \
                    or not text(x.get("now_in")) or not isinstance(x.get("consumers"), int) or x["consumers"] < 0:
                fail("hand export %r lacks its disposition, places or consumer count" % x.get("name"))
            if x["disposition"] == "MOVED_OUTSIDE" and text(x["now_in"]).replace("\\", "/").startswith(gf + "/"):
                fail("%r is MOVED_OUTSIDE but now_in is inside the generated folder" % x.get("name"))
        if r.get("hand_edits_left_in_generated") != 0:
            fail("hand_edits_left_in_generated %r, want 0" % r.get("hand_edits_left_in_generated"))
        oc = r.get("one_command") or {}
        runs = " ".join(str(v) for v in (oc.get("runs") or []))
        if not text(oc.get("command")) or any(g not in runs for g in GENS):
            fail("one_command %r does not run both generators" % oc)
        n = {"GENERATOR_EMITS": 0, "MOVED_OUTSIDE": 0}
        for x in he:
            n[x["disposition"]] += 1
        print("OK: %d hand-added export(s) placed %r; none left in the generated folder; one command runs both generators" % (len(he), n))
    elif cid == "IV98-AC2":
        d = r.get("drift") or {}
        m = d.get("mutant") or {}
        cov = " ".join(str(v) for v in (d.get("covers") or []))
        if not text(d.get("test_id")) or d.get("passes") is not True or any(g not in cov for g in GENS) or not text(m.get("what")) or m.get("failed") is not True:
            fail("drift %r" % {k: d.get(k) for k in ("test_id", "passes", "covers")})
        if r.get("typecheck_errors") != 0:
            fail("typecheck_errors %r, want 0" % r.get("typecheck_errors"))
        iv = r.get("ive26") or {}
        if iv.get("outcome") not in ("FIXED", "NOT_FIXED") or (iv["outcome"] == "NOT_FIXED" and not text(iv.get("reason"))):
            fail("ive26 %r" % iv)
        s = r.get("suite_after") or {}
        if s.get("new_failing_ids") != [] or not r.get("product_files_changed") or not HEX.match(text(r.get("portal_commit"))):
            fail("want suite_after.new_failing_ids == [], product_files_changed and a portal_commit")
        print("OK: the drift test covers both generators and a mutant breaks it; typecheck 0 errors; IVE26-AC3 %s; no new failing id" % iv["outcome"])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
