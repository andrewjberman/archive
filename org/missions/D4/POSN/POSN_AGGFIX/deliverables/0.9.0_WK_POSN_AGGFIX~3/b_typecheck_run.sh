#!/usr/bin/env bash
# POSN_AGGFIX.TO-B1-1 / TO-B2-1 (slot ~3) -- <TYPECHECK_RUN_B>: the portal's OWN typecheck, shown able to fail.
#   1. the command is READ from package.json scripts.typecheck at portal HEAD (never typed here), and printed;
#   2. it runs in the portal worktree through the junctioned install; exit code and the count of `error TS` lines printed;
#   3. the SAME command runs on a scratch copy of HEAD (git archive of the files tsc reads) carrying ONE deliberate
#      type error, with node_modules junctioned to the same install -- and must exit non-zero on that line.
# TO-B2-1: the three result lines print key=value fields separated by ; or , (exit_code=N; error_TS_line_count=M).
#   The old layout "EXIT=2  error TS lines=1" put an exit code directly before the noun, which reads as "2 error" --
#   to proof-of-spec-check's count-bar limb and to a person. Only the wording moved; every computed value is unchanged.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# POSIX form of the root, from `pwd` and never from rev-parse: rev-parse prints `C:/...`, and a drive-letter colon
# inside PATH splits the entry, so `tsc` was not found at all (first run: exit 127, recorded, not a portal result).
ROOT="$(cd "$(git -C "$HERE" rev-parse --show-toplevel)" && pwd)"
PORTAL="$ROOT/portal"
SCR="$ROOT/.scratch/typecheck"
mkdir -p "$SCR"
HEAD_SHA=$(git -C "$PORTAL" rev-parse HEAD)
CMD=$(git -C "$PORTAL" show HEAD:package.json | python -c "import json,sys; print(json.load(sys.stdin)['scripts']['typecheck'])")
if [ -z "$CMD" ]; then echo "BLOCKED: no scripts.typecheck in package.json at HEAD"; exit 1; fi
echo "PORTAL: $PORTAL  HEAD $HEAD_SHA  branch $(git -C "$PORTAL" rev-parse --abbrev-ref HEAD)"
echo "src working-tree changes vs HEAD: $(git -C "$PORTAL" status --porcelain -- src | wc -l)  (0 = the run below IS HEAD)"
echo "TYPECHECK COMMAND (package.json scripts.typecheck at HEAD): $CMD"
export PATH="$PORTAL/node_modules/.bin:$PATH"
echo "RESOLVED: tsc -> $(command -v tsc)   $(cd "$PORTAL" && tsc --version)"
echo "node_modules: $(cd "$PORTAL" && ls -ld node_modules | sed 's/.*node_modules/node_modules/')"

echo ""
echo "=== RUN 1: the portal worktree at HEAD ==="
(cd "$PORTAL" && eval "$CMD") > "$SCR/run1.out" 2>&1
rc1=$?
cat "$SCR/run1.out"
n1=$(cat "$SCR/run1.out" | grep -c "error TS")
echo "RUN 1: exit_code=$rc1; error_TS_line_count=$n1"

echo ""
echo "=== RUN 2: a scratch copy of HEAD carrying ONE deliberate type error ==="
TC="$SCR/copy_$(date +%Y%m%dT%H%M%S)"
mkdir -p "$TC"
FILES="package.json tsconfig.json tsconfig.app.json tsconfig.node.json vite.config.ts src"
git -C "$PORTAL" archive HEAD $FILES | tar -x -C "$TC"
echo "COPY: git archive HEAD $FILES -> ${TC#$ROOT/}  ($(find "$TC/src" -type f | wc -l) files under src)"
WIN_TC=$(cd "$TC" && pwd -W)
WIN_NM=$(cd "$PORTAL/node_modules" && pwd -W)
powershell.exe -NoProfile -Command "New-Item -ItemType Junction -Path '$WIN_TC\\node_modules' -Target '$WIN_NM' | Out-Null; Test-Path '$WIN_TC\\node_modules\\typescript\\package.json'"
TARGET="$TC/src/pages/Positioning/shared/bookSet.ts"
printf '\nexport const __B_TYPECHECK_CONTROL: number = %s\n' "'a string is not a number'" >> "$TARGET"
INJ_LINE=$(wc -l < "$TARGET")
echo "INJECTED at src/pages/Positioning/shared/bookSet.ts:$INJ_LINE -> $(tail -1 "$TARGET")"
(cd "$TC" && eval "$CMD") > "$SCR/run2.out" 2>&1
rc2=$?
cat "$SCR/run2.out"
n2=$(cat "$SCR/run2.out" | grep -c "error TS")
hit=$(cat "$SCR/run2.out" | grep -c "bookSet.ts($INJ_LINE,")
echo "RUN 2: exit_code=$rc2; error_TS_line_count=$n2; on_injected_line=$hit"

echo ""
echo "VERDICT INPUTS: run1 exit_code=$rc1, error_TS_line_count=$n1 (want 0 and 0) | scratch copy exit_code=$rc2, error_TS_line_count=$n2, injected_line_hits=$hit (want non-zero and at least 1)"
if [ "$rc1" = 0 ] && [ "$n1" = 0 ] && [ "$rc2" != 0 ] && [ "$hit" -ge 1 ]; then echo "EXIT=0"; exit 0; fi
echo "EXIT=1"
exit 1
