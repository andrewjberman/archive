#!/usr/bin/env python3
"""I3-AC4 detector -- the five held acts at zero, and the retirement NOT snuck in.

TWO CLAIMS, MEASURED SEPARATELY.

(a) THE EGRESS HOLD. The five forbidden act families, counted over everything this order
    authored plus the full worktree diff of the one production file in <paths>. A detector
    that cannot go non-zero is a constant, so the SAME regexes run over a PROBE this script
    writes to .scratch/ carrying one line per family. If the probe does not light up every
    family, the zeros above it mean nothing.

(b) THE RETIREMENT NOT PERFORMED. This cell makes the retirement AVAILABLE; performing it
    is a later cut's act on a decision nobody has taken. Four independent tells, read off
    the worktree bytes -- and each would go the other way if the retirement HAD been done:
      1. the STORED_IN emitter is still present and unchanged in count
      2. OWNED_BY appears in derive_stitch.py in COMMENT lines only -- never in an emit,
         never in the drop request, never in the licence table
      3. the licence table admits STORED_IN and does NOT admit OWNED_BY
      4. derive_runner.py is UNTOUCHED, so STITCH_EDGE_TYPES -- the allow-list a re-point
         would also have to widen -- still carries the same five members

COVERAGE. Every file this order authored -- the i3_* harnesses, their captures AND the
record CG-s-42.the-folds-licence.result.md -- plus the granted production file's diff.
DECLARED EXCLUSIONS, two, both structural: this detector itself (it holds the probe
literals) and the proof-of-spec instance, which is authored AFTER this run by construction
-- a self-scanning instance is impossible. It cannot see an act that left no trace in the
scanned set or the diff; the probe reports what the detector CAN see rather than asserting
what happened.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE
while WS.name and not (WS / ".git").exists():
    WS = WS.parent

PRODUCER = WS / "infra" / "aws" / "globgrph" / "derive_stitch.py"
RUNNER = WS / "infra" / "aws" / "globgrph" / "derive_runner.py"
BASELINE_PIN = "4ff4abd9a4d6d2f60fd74fef32ce64158c6bd34b"

FAMILIES = {
    "ECS_RUN_TASK_CALLS": r"ecs\s+run-task|run_task\s*\(|ecs\.run_task",
    "CODEBUILD_STARTS": r"codebuild\s+start-build|start_build\s*\(|build-derive-image\.sh",
    "S3_WRITES": r"s3\s+cp\s|s3\s+sync\s|s3api\s+put-object|put_object\s*\(|upload_file\s*\(",
    "IMAGE_PUSHES": r"docker\s+push|ecr\s+.*push|buildx\s+.*--push",
    "TERRAFORM_APPLIES": r"terraform\s+apply|safe-apply",
}
PROBE_LINES = [
    "aws ecs run-task --cluster x",
    "aws codebuild start-build --project-name x",
    "aws s3 cp local s3://bucket/key",
    "docker push 313476888478.dkr.ecr.us-east-1.amazonaws.com/x:latest",
    "terraform apply -auto-approve",
]


def sh(args):
    p = subprocess.run(args, capture_output=True, cwd=str(WS))
    return p.returncode, p.stdout.decode("utf-8", "replace")


def scan(texts) -> dict:
    out = {k: 0 for k in FAMILIES}
    for _name, txt in texts:
        for fam, pat in FAMILIES.items():
            out[fam] += len(re.findall(pat, txt))
    return out


def retirement_tells() -> tuple:
    """Four tells that the retirement was NOT performed. Returns (all_hold, rows)."""
    cur = PRODUCER.read_text(encoding="utf-8")
    rc, base = sh(["git", "show", "%s:infra/aws/globgrph/derive_stitch.py" % BASELINE_PIN])
    if rc != 0 or len(base) < 10000:
        return False, [("retrieval", False, "baseline retrieval FAILED rc=%d len=%d"
                        % (rc, len(base)))]
    rows = []

    emit_re = re.compile(r'_e\([^\n]*"STORED_IN"\)')
    n_cur, n_base = len(emit_re.findall(cur)), len(emit_re.findall(base))
    rows.append(("1 STORED_IN emitter present and unchanged",
                 n_cur == n_base and n_cur >= 1,
                 "emit sites now=%d at the pin=%d" % (n_cur, n_base)))

    owned_lines = [ln for ln in cur.splitlines() if "OWNED_BY" in ln]
    non_comment = [ln for ln in owned_lines if not ln.lstrip().startswith("#")]
    rows.append(("2 OWNED_BY appears in COMMENT lines only",
                 len(owned_lines) > 0 and not non_comment,
                 "%d line(s) name OWNED_BY, %d outside a comment" % (len(owned_lines),
                                                                     len(non_comment))))

    m = re.search(r"SOLE_WRITTEN_EDGE_TYPES: frozenset = frozenset\(\{([^}]*)\}\)", cur)
    members = m.group(1) if m else ""
    req = re.search(r"PRIOR_CYCLE_DROP_REQUEST: tuple = \(([^)]*)\)", cur)
    request = req.group(1) if req else ""
    rows.append(("3 licence admits STORED_IN, refuses OWNED_BY",
                 "STORED_IN" in members and "OWNED_BY" not in members
                 and "OWNED_BY" not in request,
                 "SOLE_WRITTEN_EDGE_TYPES={%s} PRIOR_CYCLE_DROP_REQUEST=(%s)"
                 % (members.strip(), request.strip())))

    rc2, diff = sh(["git", "diff", BASELINE_PIN, "--", "infra/aws/globgrph/derive_runner.py"])
    stitch_types = re.search(r"STITCH_EDGE_TYPES = frozenset\(\{([^}]*)\}\)",
                             RUNNER.read_text(encoding="utf-8"))
    types_txt = stitch_types.group(1) if stitch_types else ""
    rows.append(("4 derive_runner UNTOUCHED SINCE THE ORDER'S BASE; allow-list unchanged",
                 diff.strip() == "" and "OWNED_BY" not in types_txt,
                 "diff bytes=%d ; STITCH_EDGE_TYPES={%s}" % (len(diff), types_txt.strip())))

    return all(ok for _n, ok, _d in rows), rows


def main() -> int:
    self_name = Path(__file__).name
    mine = sorted(p for p in list(HERE.glob("i3_*")) + list(HERE.glob("CG-s-42.*"))
                  if p.is_file() and p.name != self_name)
    print("  EXCLUDED FROM THE SCANNED SET, DECLARED: %s -- it is the DETECTOR, and the five"
          " forbidden command literals in it ARE the probe below. Scanning it would count the"
          " control as a violation." % self_name)
    texts = [(str(p), p.read_text(encoding="utf-8", errors="replace")) for p in mine]

    # AGAINST THE ORDER'S BASE, NEVER THE INDEX: once the acts are committed a worktree
    # diff is empty, and an empty diff would silently shrink this detector's coverage to
    # the authored files alone while still printing a clean zero.
    _rc, diff = sh(["git", "diff", BASELINE_PIN, "--",
                    "infra/aws/globgrph/derive_stitch.py"])
    texts.append(("worktree diff of derive_stitch.py", diff))

    counts = scan(texts)
    print("  COVERAGE: %d file(s) authored by this order + %d bytes of diff on the one"
          " production file in <paths>" % (len(mine), len(diff)))
    for p in mine:
        print("    scanned: %s" % p.name)

    scratch = WS / ".scratch"
    scratch.mkdir(exist_ok=True)
    probe = scratch / "i3_egress_probe.txt"
    probe.write_text("\n".join(PROBE_LINES) + "\n", encoding="utf-8", newline="")
    pcounts = scan([(str(probe), probe.read_text(encoding="utf-8"))])
    fired = all(v >= 1 for v in pcounts.values())
    print("  PROBE   : %s -> %s" % (probe.name, pcounts))

    held, rows = retirement_tells()
    print("")
    print("  RETIREMENT-NOT-PERFORMED, FOUR TELLS:")
    for name, ok, detail in rows:
        print("    %-5s %s" % ("HOLDS" if ok else "BROKEN", name))
        print("          %s" % detail)

    print("")
    for fam in ("ECS_RUN_TASK_CALLS", "CODEBUILD_STARTS", "S3_WRITES", "IMAGE_PUSHES",
                "TERRAFORM_APPLIES"):
        print("%s=%d" % (fam, counts[fam]))
    print("RETIREMENT_PERFORMED=%s" % ("false" if held else "true-OR-UNPROVEN"))
    print("EGRESS_PROBE_CONTROL=%s" % ("FIRED" if fired else "DID-NOT-FIRE"))
    print("")
    print("  READ-ONLY AWS CALLS THIS ORDER DID MAKE, DISCLOSED RATHER THAN HIDDEN:")
    print("    aws s3api list-objects-v2 --bucket opal-313476888478-globgrph --prefix producers/")
    print("    aws s3api get-object   (x6, the payloads under that prefix)")
    print("  Both are READS. The face permits every read of Opal infrastructure and forbids")
    print("  every act whose effect is a publish; publishing nothing and paging nobody is the")
    print("  test, and the five counters above are how it is measured.")
    ok = fired and held and all(counts[f] == 0 for f in FAMILIES)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
