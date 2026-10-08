#!/bin/bash
# drain.sh <slot> <order-stem> <criteria-csv> <merge message>
n="$1"; stem="$2"; ids="$3"; msg="$4"
R=/cygdrive/c/Users/AndrewBerman/Desktop/ajb_workspace; [ -d "$R" ] || R=/c/Users/AndrewBerman/Desktop/ajb_workspace
P=org/missions/D14/LGIC/LGIC_BLANKFIX; F=$P/surprise-channel/investigations/INVESTIGATION_v1.md
export OPAL_AGENT_SERIAL="2.0.0_SA_COO~G"
cd /c/tmp/wk-blankfix-$n || exit 9
v=$(python .tools/proof-of-spec-check.py "$P/deliverables/0.9.0_WK_LGIC_BLANKFIX~$n/$stem.proof_of_spec.json" "$ids" 2>&1 | tail -1); echo "proof: $v"
case "$v" in VALID*) ;; *) echo "NOT MERGED"; exit 1;; esac
git status --porcelain | grep -v -E "^( M portal|\?\? \.scratch)" | head -5
cd "$R" || exit 9
bash .tools/safe-merge.sh wk-LGIC_BLANKFIX-$n -m "$msg" 2>&1 | grep -E "safe-merge: (MERGED|\*\*\*)|CONFLICT" | cut -c1-170
if git status --porcelain | grep -q "^UU"; then
  others=$(git status --porcelain | grep "^UU" | grep -v "$F"); [ -n "$others" ] && { echo "OTHER CONFLICTS: $others"; exit 2; }
  python - "$F" wk-LGIC_BLANKFIX-$n <<'PY'
import sys, subprocess, re
p, br = sys.argv[1], sys.argv[2]
def show(ref): return subprocess.run(["git", "show", "%s:%s" % (ref, p)], capture_output=True).stdout.decode("utf-8")
sec = lambda t: re.split(r"(?m)^(?=## LGIC_BLANKFIX-)", t)[1:]
head = show("HEAD"); have = set(s.split(" ", 2)[1] for s in sec(head))
add = [s for s in sec(show(br)) if s.split(" ", 2)[1] not in have]
open(p, "w", encoding="utf-8", newline="\n").write(head.rstrip("\n") + "\n\n" + "\n".join(s.rstrip("\n") + "\n" for s in add))
print("row union appended", [s.split(" ", 2)[1] for s in add])
PY
  git add "$F"; bash .tools/safe-merge.sh --continue 2>&1 | grep -E "safe-merge: (MERGED|\*\*\*)|REFUSED" | cut -c1-170
fi
git log -1 --format='HEAD %h %s' | cut -c1-110
