#!/usr/bin/env python3
"""CT-bf-1 regression sweep runner (worker scratch). Runs round-close-check.py for every (project, round) pair whose
decomposition file matches DECOMP.round<n>.md, and writes the JUDGMENT and ROUND-CLOSE lines per run.
Usage: python <path>/sweep_runner.py <out-file>   (run from the worktree root; reads <root>/.tools/round-close-check.py)."""
import glob
import os
import re
import subprocess
import sys

ROOT = os.getcwd()  # run from the worktree root
CHECKER = os.path.join(ROOT, ".tools", "round-close-check.py")
DECOMP = re.compile(r"DECOMP\.round(\d+)\.md$")


def runs():
    found = []
    for path in glob.glob(os.path.join(ROOT, "org", "missions", "D*", "*", "*", "decompositions", "*DECOMP.round*.md")):
        m = DECOMP.search(os.path.basename(path))
        if not m:
            continue
        proj_dir = os.path.dirname(os.path.dirname(path))
        rel = os.path.relpath(proj_dir, os.path.join(ROOT, "org", "missions")).replace(os.sep, "/")
        dgroup, macro, code = rel.split("/")
        found.append((dgroup, macro, code, int(m.group(1))))
    return sorted(found, key=lambda r: ("%s/%s" % (r[0], r[1]), r[2], r[3]))


def main(out_path: str) -> int:
    items = runs()
    timeouts = nonzero = 0
    with open(out_path, "w", encoding="utf-8", newline="\n") as out:
        for dgroup, macro, code, rnd in items:
            head = "== %s/%s %s round %d" % (dgroup, macro, code, rnd)
            try:
                p = subprocess.run([sys.executable, CHECKER, "--project", code, "--round", str(rnd)], cwd=ROOT,
                                   capture_output=True, text=True, timeout=120)
                rc = p.returncode
                body = [ln for ln in p.stdout.splitlines() if ln.startswith("  JUDGMENT ") or ln.startswith("ROUND-CLOSE ")]
                if rc != 0:
                    nonzero += 1
                    body.append("STDERR " + p.stderr.strip()[-300:])
            except subprocess.TimeoutExpired:
                timeouts += 1
                rc = 124
                body = ["TIMEOUT 120s"]
            out.write("%s rc=%s\n" % (head, rc))
            for ln in body:
                out.write(ln + "\n")
        out.write("SWEEP runs=%d timeouts=%d nonzero_rc=%d\n" % (len(items), timeouts, nonzero))
    print("runs=%d timeouts=%d nonzero_rc=%d -> %s" % (len(items), timeouts, nonzero, out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
