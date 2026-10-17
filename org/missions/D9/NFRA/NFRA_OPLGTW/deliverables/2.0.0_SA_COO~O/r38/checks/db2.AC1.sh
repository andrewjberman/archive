#!/usr/bin/env bash
# OPLGTW OG-db-2 AC1 (round 40): the OG-db-1 PREFLIGHT block is re-landed on deploy-to-ec2.sh and nothing else changes.
# Usage: db2.AC1.sh <worker serial>   (run from the worker's worktree root, after its commit)
#  - the pre-cell blob is the file at the parent of the first commit by <serial> that touched it; the post-cell blob is HEAD's;
#  - the diff between them is ONE insertion and no deletion; the inserted lines equal, in order, the block as trunk has it at 33fb4d9708
#    (from the line "# --- NFRA_OPLGTW OG-db-1" through the line `if [ "${1:-}" = "--preflight-only" ]; then echo "PREFLIGHT OK"; exit 0; fi`) plus at most one trailing blank line;
#  - the insertion sits immediately before the "# --- NFRA_OPLGTW OG-tl-1" block; `bash -n` reads the post-cell file clean.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
serial="$1"
F=infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
SRC_REF="${DB2_SRC_REF:-33fb4d9708}"   # DB2_SRC_REF: dry run only
[ -n "$serial" ] || { echo "usage: db2.AC1.sh <worker serial>"; echo "RESULT: FAIL"; exit 2; }
first=$(git log --author="${serial} <" --format=%H -- "$F" | tail -1 | tr -d '\r')
[ -n "$first" ] || { echo "no commit by ${serial} touches ${F}"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$first" "$SRC_REF" "$F" <<'PYEOF'
import difflib, subprocess, sys
first, ref, f = sys.argv[1:4]
def show(r):
    return subprocess.run(["git", "show", "%s:%s" % (r, f)], capture_output=True).stdout.decode("utf-8", "replace").splitlines()
pre, post, src = show(first + "^"), show("HEAD"), show(ref)
start = next((i for i, l in enumerate(src) if l.startswith("# --- NFRA_OPLGTW OG-db-1")), None)
end = next((i for i, l in enumerate(src) if "then echo" in l and "PREFLIGHT OK" in l), None)
if start is None or end is None or end < start:
    print("source block not found at " + ref); print("NO"); sys.exit(0)
block = src[start:end + 1]
ops = [o for o in difflib.SequenceMatcher(a=pre, b=post, autojunk=False).get_opcodes() if o[0] != "equal"]
ins = [o for o in ops if o[0] == "insert"]
other = [o for o in ops if o[0] != "insert"]
added = post[ins[0][3]:ins[0][4]] if len(ins) == 1 else []
body = added[:]
while body and body[-1] == "":
    body.pop()
while body and body[0] == "":
    body.pop(0)
same = body == block
nxt = post[ins[0][4]:ins[0][4] + 2] if len(ins) == 1 else []
before_tl = any(l.startswith("# --- NFRA_OPLGTW OG-tl-1") for l in nxt)
print("diff of the deploy script across the cell: %d insertion(s), %d other change(s) (want 1 and 0)" % (len(ins), len(other)))
print("inserted lines %d, the trunk block has %d, equal in order: %s; inserted before the OG-tl-1 block: %s" % (len(body), len(block), "yes" if same else "no", "yes" if before_tl else "no"))
print("OK" if (len(ins) == 1 and not other and same and before_tl) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
syn=no; git show "HEAD:$F" > "${TMPDIR:-/tmp}/_db2_syn.sh" 2>/dev/null && bash -n "${TMPDIR:-/tmp}/_db2_syn.sh" 2>/dev/null && syn=ok
rm -f "${TMPDIR:-/tmp}/_db2_syn.sh"
echo "bash -n on the post-cell file: $syn"
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$syn" = ok ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
