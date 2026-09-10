#!/usr/bin/env python3
"""I2-AC4 detector -- the five held acts, counted over everything this order wrote.

A DETECTOR THAT CANNOT GO NON-ZERO IS A CONSTANT: the same regexes run over a PROBE file
this script writes to .scratch/ containing one line per forbidden act. The probe must light
up every family, or the zero above it means nothing.

Coverage: the files this order authored (deliverables/<serial>/i2_*) plus the full worktree
diff of the granted surface. It cannot see an act that left no trace in either -- which is
why the probe arm reports what the detector CAN see rather than asserting what happened.
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


def scan(texts) -> dict:
    out = {k: 0 for k in FAMILIES}
    for name, txt in texts:
        for fam, pat in FAMILIES.items():
            out[fam] += len(re.findall(pat, txt))
    return out


def main() -> int:
    self_name = Path(__file__).name
    mine = sorted(p for p in HERE.glob("i2_*") if p.is_file() and p.name != self_name)
    print("  EXCLUDED FROM THE SCANNED SET, DECLARED: %s -- it is the DETECTOR, and the five"
          " forbidden command literals in it ARE the probe below. Scanning it would count the"
          " control as a violation." % self_name)
    texts = [(str(p), p.read_text(encoding="utf-8", errors="replace")) for p in mine]

    diff = subprocess.run(["git", "-C", str(WS), "diff", "--", "infra/aws/globgrph/derive_stitch.py"],
                          capture_output=True).stdout.decode("utf-8", "replace")
    texts.append(("worktree diff of derive_stitch.py", diff))

    counts = scan(texts)
    print("  COVERAGE: %d file(s) authored by this order + %d bytes of diff on the one"
          " production file in <paths>" % (len(mine), len(diff)))
    for p in mine:
        print("    scanned: %s" % p.name)

    # ---- the probe: the same detector on a file that SHOULD light up every family --------
    scratch = WS / ".scratch"
    scratch.mkdir(exist_ok=True)
    probe = scratch / "i2_egress_probe.txt"
    probe.write_text("\n".join(PROBE_LINES) + "\n", encoding="utf-8")
    pcounts = scan([(str(probe), probe.read_text(encoding="utf-8"))])
    fired = all(v >= 1 for v in pcounts.values())
    print("  PROBE   : %s -> %s" % (probe.name, pcounts))

    # ---- the magnitude assertion ---------------------------------------------------------
    claims = []
    for name, txt in texts:
        for m in re.finditer(r"MAGNITUDE[_A-Z]*=([A-Za-z0-9_/-]+)", txt):
            claims.append((name, m.group(0)))
    manufactured = [c for c in claims
                    if not re.search(r"=(UNMEASURED|false)", c[1])]
    print("  MAGNITUDE CLAIMS: %d, all of the form UNMEASURED/false: %s"
          % (len(claims), not manufactured))

    print("")
    for fam in ("ECS_RUN_TASK_CALLS", "CODEBUILD_STARTS", "S3_WRITES", "IMAGE_PUSHES",
                "TERRAFORM_APPLIES"):
        print("%s=%d" % (fam, counts[fam]))
    print("MAGNITUDE_MANUFACTURED=%s" % str(bool(manufactured)).lower())
    print("EGRESS_PROBE_CONTROL=%s" % ("FIRED" if fired else "DID-NOT-FIRE"))
    ok = fired and not manufactured and all(counts[f] == 0 for f in FAMILIES)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
