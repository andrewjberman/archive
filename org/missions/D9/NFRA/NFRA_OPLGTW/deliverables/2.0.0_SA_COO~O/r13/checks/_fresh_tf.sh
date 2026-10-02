#!/usr/bin/env bash
# _fresh_tf.sh -- sourced by tf.AC1/AC2: make a FRESH linked worktree of HEAD (sparse cone, no copy, no pruning of the root),
# `terraform init` the opal-gateway root there with EVERY TF_VAR_* unset, and run one plan. Prints only the plan's
# summary line, its "Error:" count and its "No value for required variable" count; never a variable or resource value.
# fresh_plan <label> [extra plan args...] -> sets PLAN_RC, PLAN_ERRORS, PLAN_NOVALUE, PLAN_SUMMARY.
TF_ROOT_REL="infra/aws/terraform/opal-gateway"
fresh_plan() {
  label="$1"; shift
  base="${TMP:-/tmp}/og_r13_fresh_$$_${label}"
  rm -rf "$base" 2>/dev/null
  # SPARSE cone (disk at limit, 0.0.0_AB_MSTR~Z msg 28166): infra/aws (the whole root and every lambda/module path it
  # references), org/standards, lib. The root itself is complete -- not a pruned copy.
  git worktree add --no-checkout --detach "$base" HEAD >/dev/null 2>&1 || { echo "fresh worktree add failed"; PLAN_RC=99; return; }
  git -C "$base" sparse-checkout set --cone infra/aws org/standards lib >/dev/null 2>&1 && git -C "$base" read-tree -mu HEAD >/dev/null 2>&1 \
    || { echo "sparse checkout failed"; git worktree remove --force "$base" >/dev/null 2>&1; PLAN_RC=99; return; }
  echo "fresh worktree $base at $(git -C "$base" rev-parse --short HEAD) (untracked files in the root: $(git -C "$base" status --porcelain -- "$TF_ROOT_REL" | grep -c .))"
  out="${base}.plan.out"
  ( cd "$base/$TF_ROOT_REL" || exit 98
    for v in $(env | sed -n 's/^\(TF_VAR_[A-Za-z0-9_]*\)=.*/\1/p'); do unset "$v"; done
    terraform init -input=false -no-color >"${base}.init.out" 2>&1 || { echo "INIT_FAILED"; tail -5 "${base}.init.out" | grep -E "Error" ; exit 97; }
    terraform plan -input=false -lock=false -no-color -detailed-exitcode "$@" >"$out" 2>&1
  ); PLAN_RC=$?
  PLAN_ERRORS=$(grep -c "^Error:\|│ Error:" "$out" 2>/dev/null || echo 0)
  PLAN_NOVALUE=$(grep -c "No value for required variable" "$out" 2>/dev/null || echo 0)
  PLAN_SUMMARY=$(grep -E "^Plan: |No changes\." "$out" 2>/dev/null | head -1)
  [ -n "$PLAN_SUMMARY" ] || PLAN_SUMMARY="(no plan summary line)"
  git worktree remove --force "$base" >/dev/null 2>&1; rm -f "${base}.init.out"
  echo "plan rc=$PLAN_RC; errors $PLAN_ERRORS; missing required variables $PLAN_NOVALUE; $PLAN_SUMMARY"
  rm -f "$out"
}
