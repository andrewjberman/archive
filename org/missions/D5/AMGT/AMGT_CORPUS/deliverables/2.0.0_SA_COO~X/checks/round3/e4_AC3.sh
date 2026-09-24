#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e4_AC3. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python - <<'EOF'
import re
sheet=open("org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~1/DOSSIER_INTERFACE.md",encoding="utf-8",errors="replace").read()
import os, subprocess
# the portal is a submodule and a LINKED worktree carries it empty: read types.ts from the MAIN worktree (the one holding
# the shared .git), found via --git-common-dir, so the check reads the same live file from every worktree (row Z-W1-S5)
common=subprocess.run(["git","rev-parse","--path-format=absolute","--git-common-dir"],capture_output=True,text=True).stdout.strip()
main=os.path.dirname(common)
ts=open(os.path.join(main,"portal/src/pages/SecurityAnalysis/types.ts"),encoding="utf-8",errors="replace").read().splitlines()
cites=sorted(set(int(m.group(1)) for m in re.finditer(r"types\.ts:(\d+)", sheet)))
for n in cites:
    live=ts[n-1].strip() if 0 < n <= len(ts) else "(out of range)"
    print("citation types.ts:%d live: %s" % (n, live[:80]))
print("citations %d" % len(cites))
EOF
