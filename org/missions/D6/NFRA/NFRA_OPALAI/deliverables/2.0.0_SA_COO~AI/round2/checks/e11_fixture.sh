#!/usr/bin/env bash
# e11_fixture.sh -- sourced by e11.AC1.sh and e11.AC3.sh (OA-e-11, row NFRA_OPALAI-Z-S17). Builds a SCRATCH superproject
# with one submodule named opal_ai under a mktemp dir. No network: the submodule source is a local repo (file protocol).
# The lane file, the validator and BOTH hook scripts are copied from the COMMITTED bytes of the tree under test (git show
# HEAD:<path>), so the fixture grades what the worker committed, not an unlanded edit.
# Exports: FX (fixture root), SUPER, NESTED (main nested checkout), OUTSIDE (nested linked worktree outside SUPER),
# and the function fx_commit <dir> <author-serial> <new-file> -> prints "landed" or "refused rc=<n>".
FX="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/e11fx_$$")"; mkdir -p "$FX"
SUPER="$FX/super"; NESTED="$SUPER/opal_ai"; OUTSIDE="$FX/outside"
export OWNED_PATHS_AUDIT_LOG="$FX/audit.log"   # never the real org/git-author-override-audit.log
_fx_git() { git -c user.name=fixture -c user.email=fixture@opal.agent -c protocol.file.allow=always "$@"; }
_fx_fail() { echo "FIXTURE-ERROR: $1"; echo "RESULT: FAIL"; exit 1; }
_fx_git init -q -b main "$FX/subsrc" || _fx_fail "init subsrc"
_fx_git -C "$FX/subsrc" commit -q --allow-empty -m init || _fx_fail "subsrc commit"
_fx_git init -q -b main "$SUPER" || _fx_fail "init super"
mkdir -p "$SUPER/.tools/git-hooks"
for f in .owned-paths.yaml .tools/owned-paths-validate.py .tools/git-hooks/owned-paths-check.sh .tools/git-hooks/install-owned-paths.sh; do
    git show "HEAD:$f" > "$SUPER/$f" 2>/dev/null || _fx_fail "cannot read HEAD:$f"
done
( cd "$SUPER" && _fx_git submodule add -q "$FX/subsrc" opal_ai >/dev/null 2>&1 ) || _fx_fail "submodule add"
_fx_git -C "$SUPER" add -A >/dev/null 2>&1; _fx_git -C "$SUPER" commit -q --no-verify -m fixture || _fx_fail "super commit"
_fx_git -C "$NESTED" worktree add -q "$OUTSIDE" -b wk-fixture-outside >/dev/null 2>&1 || _fx_fail "nested worktree add"
( cd "$SUPER" && bash .tools/git-hooks/install-owned-paths.sh --submodule opal_ai >/dev/null 2>&1 ) || _fx_fail "install --submodule"
( cd "$SUPER" && bash .tools/git-hooks/install-owned-paths.sh >/dev/null 2>&1 ) || _fx_fail "install parent"
fx_commit() { # fx_commit <dir> <author-serial> <new-file>
    local d="$1" a="$2" f="$3" before after rc
    before=$(git -C "$d" rev-parse HEAD 2>/dev/null)
    mkdir -p "$(dirname "$d/$f")"; printf 'planted by e11 fixture\n' > "$d/$f"
    git -C "$d" add -- "$f" >/dev/null 2>&1
    GIT_AUTHOR_NAME="$a" GIT_AUTHOR_EMAIL="$a@opal.agent" timeout 60 \
        git -C "$d" -c user.name=fixture -c user.email=fixture@opal.agent commit -q --author "$a <$a@opal.agent>" -m planted -- "$f" >"$FX/last.out" 2>&1
    rc=$?
    after=$(git -C "$d" rev-parse HEAD 2>/dev/null)
    if [ "$before" != "$after" ]; then echo "landed"; else echo "refused rc=$rc"; fi
}
