"""IRPT_BCKEND round 116 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one LOCAL order (CTO ADDENDUM 20 item 3; row W272-S2):
  IB116-1  IB-pr-415  IB-pr-399's replay driver derives its pre-binding negative control from the commit before the binding change, not
                      pin^, and the control is shown to fail on the defect it guards (worker ~277)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB116-1-AC1  ~264's replay/run_replay.py no longer derives the control from `pin + "^"`; it names PRE_BINDING_REF as the parent of the
               binding commit cabad9008c. Base: FAIL (pin + "^").
  IB116-1-AC2  proof P: the control run from that ref reports the defect (a no-row internal caller selecting another firm is bound to it:
               routes_widened >= 1, verdict "control_fails_on_defect"), and the same arm on the bound entry reads not widened.
               Base: FAIL (no P).
"""
import json
import subprocess
import sys
from pathlib import Path

DRV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~264/replay/run_replay.py"
P = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~277/IB116-1_control_proof.json"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB116"))
        sys.exit(1)

    if cid == "IB116-1-AC1":
        s = (root / DRV).read_text(encoding="utf-8")
        if 'pin + "^"' in s:
            fail("driver still derives the control from pin + \"^\"")
        if "PRE_BINDING_REF" not in s or "cabad9008c" not in s:
            fail("driver does not name PRE_BINDING_REF from the binding commit cabad9008c")
        print("OK: control derived from the binding commit's parent")
    elif cid == "IB116-1-AC2":
        f = root / P
        if not f.is_file():
            fail("no %s" % P)
        p = json.loads(f.read_text(encoding="utf-8"))
        ref = str(p.get("pre_binding_ref") or "")
        rc = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", ref, "cabad9008c"], capture_output=True)
        if not ref or rc.returncode != 0 or ref.startswith("cabad9008c"):
            fail("pre_binding_ref %r is not a strict ancestor of cabad9008c" % ref)
        if p.get("verdict") != "control_fails_on_defect" or not isinstance(p.get("routes_widened"), int) or p["routes_widened"] < 1:
            fail("control %r widened %r" % (p.get("verdict"), p.get("routes_widened")))
        if p.get("bound_entry_routes_widened") != 0:
            fail("bound entry widened %r" % p.get("bound_entry_routes_widened"))
        print("OK: control from %s widens %d route(s); the bound entry widens 0" % (ref[:10], p["routes_widened"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
