"""OG-v-4 probe: python og_v4.py AC<n>

Prints its measurement with its denominator, then exactly one line
`VERDICT: PASS-OGV4-AC<n>` or `VERDICT: FAIL-OGV4-AC<n> <reason>`. rc 0 on PASS, 1 on FAIL,
2 on usage error.

PHASE 1 HAND-OFF (0.9.0_WK_NFRA_OPLGTW~6): only AC8 (the re-seal) is implemented here. AC1-AC7,
AC9 and the judgment rows J1/J2 belong to PHASE 2, handed only once G-C and G-D are at HEAD, and
are NOT implemented by this phase -- calling this probe with any other id is a usage error.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PROBE = Path(__file__).resolve()
CELL_DIR_DEFAULT = PROBE.parents[0].parent  # .../deliverables/0.9.0_WK_NFRA_OPLGTW~6/
ROOT = PROBE.parents[8]

VENV_PY = ROOT / ".venv-og" / "Scripts" / "python.exe"

# The two PHASE-2 inputs whose ABSENCE, in PHASE 1, is the precondition the re-seal's property
# depends on -- see TO-OG-v-4 WORKER FACE lines 33-40 and BOUNDS "G-C and G-D".
GC_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/1.0.0_SA_CTO~A/G-C_CONTROLLED_IDENTITY_AND_GRANT.md"
GD_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/CONTROLLED_WALKTHROUGH_RECORD.md"

RQ_IDS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5", "RQ6"]

AC = [None]


def fail_msg(reason: str) -> str:
    return "VERDICT: FAIL-OGV4-" + AC[0] + " " + reason


def verdict(ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-OGV4-" + AC[0])
        return 0
    print(fail_msg(reason))
    return 1


def _sealed_expected(cell: Path) -> dict:
    p = cell / "SEALED_EXPECTED.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="ascii"))


def _git_head(root: Path) -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        raise RuntimeError("git rev-parse HEAD failed rc=" + str(out.returncode) + ": " + out.stderr)
    return out.stdout.strip()


def _git_path_absent_at(root: Path, commit: str, path: str) -> tuple[bool, int, str]:
    """Returns (absent, rc, stderr) for `git cat-file -e <commit>:<path>` -- rc!=0 means the
    path does not exist at that commit (absent), regardless of the specific error text."""
    out = subprocess.run(
        ["git", "cat-file", "-e", commit + ":" + path],
        cwd=str(root), capture_output=True, text=True, timeout=30,
    )
    return (out.returncode != 0, out.returncode, out.stderr.strip())


# ---------------------------------------------------------------------------------------------
def ac8(cell: Path) -> int:
    # Step 1 -- measure, right now, the absence of G-C and G-D at a named commit. This read
    # happens BEFORE the re-seal instrument runs, in this same probe invocation, so the record
    # it produces is contemporaneous with the moment the new seal is cut -- not a claim made
    # after the fact from memory.
    commit = _git_head(ROOT)
    gc_absent, gc_rc, gc_err = _git_path_absent_at(ROOT, commit, GC_PATH)
    gd_absent, gd_rc, gd_err = _git_path_absent_at(ROOT, commit, GD_PATH)
    print("GATE CHECK at commit " + commit + ": G-C (" + GC_PATH + ") git cat-file -e rc="
          + str(gc_rc) + " -> " + ("ABSENT" if gc_absent else "PRESENT") + " (" + gc_err + ")")
    print("GATE CHECK at commit " + commit + ": G-D (" + GD_PATH + ") git cat-file -e rc="
          + str(gd_rc) + " -> " + ("ABSENT" if gd_absent else "PRESENT") + " (" + gd_err + ")")

    if not (gc_absent and gd_absent):
        return verdict(
            False,
            "re-seal property already lost at " + commit + ": G-C absent=" + str(gc_absent)
            + " G-D absent=" + str(gd_absent) + " -- refusing to re-seal, do not proceed",
        )

    # Step 2 -- capture the OLD (OG-v-3, salt lost) digests before they are overwritten.
    old_sealed = _sealed_expected(cell)
    old_digests = {q.get("id"): q.get("expected_answer_hash") for q in old_sealed.get("questions", [])}

    # Step 3 -- run the COMMITTED sealing instrument exactly as committed. No reimplementation:
    # this is a subprocess call to the same file OG-v-3 used.
    src_path = cell / "compute_expected.py"
    if not src_path.is_file():
        return verdict(False, "compute_expected.py missing at " + str(src_path))
    run = subprocess.run([str(VENV_PY), str(src_path)], capture_output=True, text=True, timeout=280)
    print("RESEAL RUN: rc=" + str(run.returncode) + " stdout=" + run.stdout.strip())
    if run.returncode != 0:
        return verdict(False, "compute_expected.py failed as committed, rc=" + str(run.returncode)
                        + " stderr_tail=" + run.stderr.strip()[-500:])

    # Step 4 -- augment the freshly-cut SEALED_EXPECTED.json with the absence record measured
    # in Step 1. This adds metadata only; every computed value (salt, hashes, qualified objects)
    # comes solely from compute_expected.py, unmodified.
    new_sealed = _sealed_expected(cell)
    new_sealed["preseal_absence_check"] = {
        "commit": commit,
        "paths_checked": [GC_PATH, GD_PATH],
        "reads": [
            {"path": GC_PATH, "instrument": "git cat-file -e <commit>:<path>",
             "rc": gc_rc, "result": "ABSENT" if gc_absent else "PRESENT", "stderr": gc_err},
            {"path": GD_PATH, "instrument": "git cat-file -e <commit>:<path>",
             "rc": gd_rc, "result": "ABSENT" if gd_absent else "PRESENT", "stderr": gd_err},
        ],
        "note": (
            "Measured immediately before invoking compute_expected.py in this same probe "
            "invocation, i.e. at the moment this seal was cut. Both ABSENT is the precondition "
            "PHASE 1 (the re-seal) requires: the controlled walkthrough (G-D) had not happened, "
            "and its controlled identity/grant record (G-C) did not exist, so no result was "
            "observable when these expectations were fixed."
        ),
    }
    (cell / "SEALED_EXPECTED.json").write_text(
        json.dumps(new_sealed, indent=2, sort_keys=True) + "\n", encoding="ascii",
    )

    # Step 5 -- print the new digests beside the old ones; they DIFFER BY CONSTRUCTION (a fresh
    # salt) and are never expected to reproduce OG-v-3's lost-salt digests.
    new_digests = {q.get("id"): q.get("expected_answer_hash") for q in new_sealed.get("questions", [])}
    ids_present = sorted(new_digests.keys())
    print("DIGEST COMPARISON -- OLD (OG-v-3, salt at C:/tmp/nfra-oplgtw-sealed/expected/SALT.txt "
          "is GONE) vs NEW (this re-seal, fresh salt just minted); DIFFER BY CONSTRUCTION, never "
          "expected to reproduce:")
    differ = 0
    for rq in RQ_IDS:
        o = old_digests.get(rq, "<none>")
        n = new_digests.get(rq, "<none>")
        is_diff = (o != n)
        if is_diff:
            differ += 1
        print("  " + rq + ": old=" + str(o) + " new=" + str(n) + " differ=" + str(is_diff))
    print("DENOMINATOR: " + str(len(RQ_IDS)) + " question(s); " + str(differ)
          + " of " + str(len(RQ_IDS)) + " differ from the old (lost-salt) digest, as expected "
          "for a fresh salt")

    problems = []
    if ids_present != RQ_IDS:
        problems.append("question ids " + str(ids_present) + " != " + str(RQ_IDS))
    if differ != len(RQ_IDS):
        problems.append(str(len(RQ_IDS) - differ) + " digest(s) unexpectedly identical to the old seal")
    if "preseal_absence_check" not in new_sealed:
        problems.append("preseal_absence_check missing from SEALED_EXPECTED.json")

    ok = not problems
    return verdict(ok, "; ".join(problems))


def main(argv) -> int:
    if len(argv) != 1 or not re.fullmatch(r"AC[1-9]", argv[0]):
        print("usage: og_v4.py AC<1-9>")
        return 2
    AC[0] = argv[0]
    print("PROBE: og_v4 " + AC[0] + " over " + str(CELL_DIR_DEFAULT))
    if AC[0] != "AC8":
        print(fail_msg("not implemented in PHASE 1 (0.9.0_WK_NFRA_OPLGTW~6) -- " + AC[0]
                        + " belongs to PHASE 2, handed only after G-C and G-D are at HEAD"))
        return 2
    return ac8(CELL_DIR_DEFAULT)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
