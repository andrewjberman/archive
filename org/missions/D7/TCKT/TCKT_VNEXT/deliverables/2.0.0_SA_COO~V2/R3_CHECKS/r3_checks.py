"""TCKT_VNEXT round 3 -- the issuer's mechanical checks (2.0.0_SA_COO~V2). Run from the worktree root.

  pc-rules  R3-pc1-AC1  the clamp precheck decides the ticket host from the source map, the recorded commit and the
                        deployed member's content, with no typed list of allowed builds
  pc-hosts  R3-pc1-AC2  the IRPT hosts keep their release-set rule and the totals line; a host that cannot be read is named

Each prints <NAME>-OK <detail> or <NAME>-FAIL <reason>; exit 0/1. Every pytest call is bounded at 110 s.
"""
import re
import subprocess
import sys
from pathlib import Path

PC_DIR = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck")
PC_TESTS = PC_DIR / "test_clamp_precheck.py"
PC_SOURCE = PC_DIR / "clamp_precheck.py"

NAMED = {
    "pc-rules": ["test_map_live_and_commit_agree_and_clamp_present_is_clamped",
                 "test_live_build_not_the_maps_is_map_stale_and_not_clamped",
                 "test_member_not_the_recorded_commits_file_is_refused",
                 "test_a_clamp_helper_removed_is_not_clamped",
                 "test_a_route_handler_that_stops_calling_the_clamp_is_not_clamped"],
    "pc-hosts": ["test_irpt_host_on_a_release_build_is_clamped", "test_irpt_host_off_the_release_set_is_not_released",
                 "test_unreadable_host_is_named_and_the_total_is_not_full", "test_exit_zero_only_when_every_route_is_clamped"],
}


def run(names):
    if not PC_TESTS.exists():
        return False, "absent: %s" % PC_TESTS.as_posix()
    src = PC_TESTS.read_text(encoding="utf-8")
    missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", PC_TESTS.as_posix(),
                        "-k", " or ".join(names)], capture_output=True, text=True, timeout=110)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", out) or [0, 0])[1])
    if r.returncode != 0 or passed < len(names) or failed:
        return False, "rc=%d passed=%d of %d failed=%d" % (r.returncode, passed, len(names), failed)
    return True, "passed=%d of %d" % (passed, len(names))


def main(argv):
    if len(argv) != 1 or argv[0] not in NAMED:
        print("usage: r3_checks.py {%s}" % "|".join(sorted(NAMED)))
        return 2
    ok, why = run(NAMED[argv[0]])
    if ok and argv[0] == "pc-rules":
        text = PC_SOURCE.read_text(encoding="utf-8") if PC_SOURCE.exists() else ""
        if "TICKET_OK" in text:
            ok, why = False, "clamp_precheck.py still carries a typed TICKET_OK list"
    print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
