"""DSGN_IRPTV1 round 13 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's rulings msg 4336 on the FWD-1 trace pair.

Cell: IV-e-88 the pair REVISED to the four rulings (the trace makes the calls the page makes, no others, each named in the radius) and the
RUNNER built at a pin with its offline tests. Nothing is minted, written or called.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV88-AC1  ~48/fwd1_trace_runner/ holds the runner and a tests file; `python -m pytest <tests file> -q` exits 0; ~48/RUNNER_RECORD.json
            names runner_file, tests_file, tests {passed > 0, failed == 0}, post_allow_list (exactly two route templates, selections
            and directory/resolve), exp_max_minutes == 30, and guards, each true: refuses_post_outside_allow_list_before_send,
            refuses_exp_over_max, deletes_row_only_after_exp, makes_no_call_on_import.
  IV88-AC2  ~48/FWD1_TRACE_PAIR_v2.md carries "## Rulings applied", "## Measured at signing", "## The identity", "## The act",
            "## Blast radius", "## Branches", "## What must hold before a run order cites this pair", "## COO half", "## CTO half";
            each half reads UNSIGNED; the Rulings section names msg 4336 and states which route the Performance tab calls with a
            file-and-line citation in ~48/RUNNER_RECORD.json performance_route {route, source: {file, line}, in_trace (bool)};
            no address outside opal.invalid and no digit run of 8 or more.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~48/"
GUARDS = ("refuses_post_outside_allow_list_before_send", "refuses_exp_over_max", "deletes_row_only_after_exp", "makes_no_call_on_import")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV13"))
        sys.exit(1)

    p = root / (D + "RUNNER_RECORD.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    if cid == "IV88-AC1":
        rf, tf = str(r.get("runner_file") or ""), str(r.get("tests_file") or "")
        if not rf.startswith(D + "fwd1_trace_runner/") or not tf.startswith(D + "fwd1_trace_runner/") or not (root / rf).is_file() or not (root / tf).is_file():
            fail("runner_file %r / tests_file %r are not files under %sfwd1_trace_runner/" % (rf, tf, D))
        t = r.get("tests") or {}
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0:
            fail("tests %r" % t)
        allow = r.get("post_allow_list") or []
        if len(allow) != 2 or not any("selections" in a for a in allow) or not any("directory/resolve" in a for a in allow):
            fail("post_allow_list %r, want exactly the selections and directory/resolve route templates" % allow)
        if r.get("exp_max_minutes") != 30:
            fail("exp_max_minutes %r" % r.get("exp_max_minutes"))
        g = r.get("guards") or {}
        for k in GUARDS:
            if g.get(k) is not True:
                fail("guard %s is %r" % (k, g.get(k)))
        run = subprocess.run([sys.executable, "-m", "pytest", tf, "-q"], cwd=str(root), capture_output=True)
        if run.returncode != 0:
            fail("pytest %s exited %d" % (tf, run.returncode))
        print("OK: the runner's tests pass; POST allow-list is the two routes; exp cap 30; four guards stated and tested")
    elif cid == "IV88-AC2":
        q = root / (D + "FWD1_TRACE_PAIR_v2.md")
        if not q.is_file():
            fail("no packet")
        t = q.read_text(encoding="utf-8")
        for hd in ("## Rulings applied", "## Measured at signing", "## The identity", "## The act", "## Blast radius", "## Branches",
                   "## What must hold before a run order cites this pair", "## COO half", "## CTO half"):
            if hd not in t:
                fail("missing heading %r" % hd)
        for hd in ("## COO half", "## CTO half"):
            if "UNSIGNED" not in re.split(r"\n## ", t.split(hd, 1)[1], maxsplit=1)[0]:
                fail("%s not UNSIGNED" % hd)
        if "4336" not in re.split(r"\n## ", t.split("## Rulings applied", 1)[1], maxsplit=1)[0]:
            fail("the Rulings section does not name msg 4336")
        pr = r.get("performance_route") or {}
        src = pr.get("source") or {}
        if not pr.get("route") or not src.get("file") or not isinstance(src.get("line"), int) or not isinstance(pr.get("in_trace"), bool):
            fail("performance_route %r" % pr)
        bad = [a for a in re.findall(r"[\w.+-]+@[\w.-]+", t) if not a.lower().endswith("opal.invalid") and "opal.agent" not in a.lower()]
        if bad:
            fail("an address outside opal.invalid: %r" % bad[:3])
        if re.search(r"(?<![0-9A-Za-z])\d{8,}(?![0-9A-Za-z])", t):
            fail("a digit run of 8 or more is in the packet")
        print("OK: pair v2 sections present, rulings of msg 4336 applied, the Performance route named with its source; both halves UNSIGNED")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
