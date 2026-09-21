#!/usr/bin/env python3
"""One-shot mutant control for the MX-c-1 proof-of-spec `controls.mutant` field (never committed as an
acceptance criterion -- this is the PASSING-ASSERTION-NEVER-MUTATED-HAS-NEVER-BEEN-TESTED control the
PROOF_OF_SPEC schema requires alongside the 7 criteria).

It plants a SECOND synthetic writer (a file whose own bytes assign a variable from a literal containing
'DATA_CATALOG.yaml' and then open() it in 'w' mode) purely in-memory -- by monkeypatching mx_c_1's
git_ls_files() to also report the fixture's path -- and re-runs the AC3 logic (exactly-one-writer REFUSAL).
Expected: AC3 flips from PASS (1 writer) to FAIL (2 writers, REFUSED). Then the patch is removed and AC3 is
re-run once more to confirm it returns to PASS (the mutant does not leave residue).
"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("mx_c_1", os.path.join(HERE, "mx_c_1.py"))
mx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mx)

FIXTURE_REL = os.path.join(
    "org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables",
    "0.9.0_WK_NFRA_MCPINDEX~1", "probes", "_mutant_fixture.py",
).replace(os.sep, "/")
FIXTURE_ABS = os.path.join(mx.REPO, FIXTURE_REL.replace("/", os.sep))

FIXTURE_SRC = (
    "import os\n"
    "OUT2 = os.path.join(os.path.dirname(__file__), \"DATA_CATALOG.yaml\")\n"
    "with open(OUT2, \"w\") as f:\n"
    "    f.write(\"mutant\")\n"
)


def run_ac3(capture_only):
    buf = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = buf
    try:
        mx.ac3()
    finally:
        sys.stdout = real_stdout
    out = buf.getvalue()
    if capture_only:
        return out
    print(out)
    return out


def main():
    with io.open(FIXTURE_ABS, "w", encoding="ascii") as f:
        f.write(FIXTURE_SRC)

    real_git_ls_files = mx.git_ls_files
    try:
        mx.git_ls_files = lambda: real_git_ls_files() + [FIXTURE_REL]
        print("=== ENGAGED (2 writers: the real emitter + the planted fixture) ===")
        out_engaged = run_ac3(False)
    finally:
        mx.git_ls_files = real_git_ls_files
        os.remove(FIXTURE_ABS)

    print("=== DISENGAGED (fixture removed, patch reverted; 1 writer) ===")
    out_disengaged = run_ac3(False)

    engaged_ok = "VERDICT: FAIL-MXC1-AC3 REFUSED -- 2 writers found, not exactly one" in out_engaged
    disengaged_ok = "VERDICT: PASS-MXC1-AC3" in out_disengaged
    print("MUTANT descriptION: planted a second synthetic writer via a monkeypatched git_ls_files(); "
          "AC3's 'exactly one writer' REFUSAL must fire with the plant present and must NOT fire with it "
          "removed.")
    print("MUTANT expected: engaged -> FAIL-MXC1-AC3 REFUSED (2 writers); disengaged -> PASS-MXC1-AC3 (1 writer)")
    print("MUTANT observed: engaged_ok=%s disengaged_ok=%s" % (engaged_ok, disengaged_ok))
    status = "FIRED-AS-EXPECTED" if (engaged_ok and disengaged_ok) else "DID-NOT-FIRE (deliverable INVALID)"
    print("MUTANT status: %s" % status)
    return 0 if status == "FIRED-AS-EXPECTED" else 1


if __name__ == "__main__":
    sys.exit(main())
