#!/usr/bin/env bash
# _root.sh -- sourced by every NFRA_MCPMSP round-1 check: cd to the PARENT worktree root, never a nested repo.
_R="$(git rev-parse --show-superproject-working-tree 2>/dev/null)"
[ -n "$_R" ] || _R="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$_R" ] || { echo "ERROR: not inside a git worktree"; exit 9; }
cd "$_R" || { echo "ERROR: cannot cd to $_R"; exit 9; }
# pipefail: every check captures out=$(cmd | tr -d CR); without it rc is tr's exit status.
set -o pipefail
G="infra/aws/ec2/opal-gateway"
MPW_DIR="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
TF_DIR="infra/aws/terraform/opal-gateway"
AWS="$(pwd)/.tools/aws"
GW_INSTANCE="i-07dccb1615503ac99"
GW_ROLE="opal-gateway-role"
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }
opal_name() { python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name(*sys.argv[1:5]))" "$@" 2>&1 | tr -d '\r' | tail -1; }
acct() { timeout 30 "$AWS" sts get-caller-identity --query Account --output text 2>/dev/null | tr -d '\r'; }
# pytest_named <test path> <min passed per name> <name>...  -> prints the pytest tail + per-name counts; rc 0 only when
# nothing failed and every named test PASSED at least <min> times.
pytest_named() {
  local path="$1" min="$2"; shift 2
  [ -e "$path" ] || { echo "$path absent"; return 1; }
  local out; out=$(cd "$(dirname "$path")/.." 2>/dev/null && timeout 100 python -m pytest "$(basename "$(dirname "$path")")/$(basename "$path")" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
  local tail; tail=$(printf '%s\n' "$out" | tail -1)
  local failed; failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
  local ok=1 line="" n c
  for n in "$@"; do c=$(printf '%s\n' "$out" | grep -cE "::${n}(\[[^]]*\])? PASSED"); line="$line $n=$c"; [ "$c" -ge "$min" ] || ok=0; done
  echo "pytest: $tail;$line"
  [ "$failed" = 0 ] && [ "$ok" = 1 ]
}
ledger_closed() {
  local slug="$1"
  local entry; entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
  local sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${slug}.json" 2>/dev/null && sent=yes
  local l; l=$(timeout 60 python .tools/deploy_ledger.py list 2>&1); local listed; listed=$(printf '%s\n' "$l" | grep -c -- "$slug")
  local den; den=$(printf '%s\n' "$l" | grep -m1 'SCAN DENOMINATOR' || echo "(no denominator)")
  echo "slug $slug: entry files at HEAD=$entry; sentinel at HEAD=$sent; listed OPEN/HELD=$listed; $den"
  [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR'
}
# ssm_run <python-json-cmd-string-file> -> sets SSM_OUT and SSM_ST
ssm_run() {
  local params="$1" cid st=""
  cid=$(timeout 40 "$AWS" ssm send-command --instance-ids "$GW_INSTANCE" --document-name AWS-RunShellScript --parameters "file://$(native "$params")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
  for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
  SSM_OUT=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$GW_INSTANCE" --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
  SSM_ST="${st:-NONE}"; SSM_CID="${cid:-NONE}"
}
# sim <principal-arn> <action> <resource-arn> -> the ONE decision for that single resource (one call per resource: a
# multi-resource call can collapse into a single templated row, measured at the cut).
sim() { timeout 40 "$AWS" iam simulate-principal-policy --policy-source-arn "$1" --action-names "$2" --resource-arns "$3" --query "EvaluationResults[0].EvalDecision" --output text 2>&1 | tr -d '\r' | tail -1; }
