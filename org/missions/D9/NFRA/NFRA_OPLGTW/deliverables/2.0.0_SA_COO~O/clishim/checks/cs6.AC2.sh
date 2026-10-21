#!/usr/bin/env bash
# OPLGTW OG-cs-6 AC2 (cli-shim workstream, wave 3): the footprint and the format of the folder reader's IAM text.
#   cs6.AC2.sh <order-file>
#  (a) the files that differ from the commit that added <order-file>, under infra/aws/terraform/opal-gateway/ (committed, uncommitted and untracked), are exactly folder_reader_iam.tf (no other .tf, no state, no variables.tf);
#  (b) `terraform fmt -check` accepts that file (formatting only: nothing is initialised, planned or applied).
ORDER="$1"
BASE=$(git log --diff-filter=A --format=%H -1 -- "$ORDER")
D=infra/aws/terraform/opal-gateway
got=$( { git diff --name-only "$BASE" -- "$D"; git ls-files --others --exclude-standard -- "$D"; } | sort -u | paste -sd, -)
want="$D/folder_reader_iam.tf"
ok=1
if [ -n "$BASE" ] && [ "$got" = "$want" ]; then echo "files that differ under $D: $got (want exactly $want): ok"; else echo "files that differ under $D: ${got:-none} (want exactly $want): NO"; ok=0; fi
TF=terraform; command -v terraform >/dev/null 2>&1 || TF=""
if [ -z "$TF" ]; then echo "terraform fmt -check: NO (terraform not found)"; ok=0
elif [ -f "$want" ]; then
  out=$(terraform fmt -check -diff "$want" 2>&1 | tr -d '\r'); rc=$?
  if [ -z "$out" ]; then echo "terraform fmt -check accepts folder_reader_iam.tf: ok"; else echo "terraform fmt -check accepts folder_reader_iam.tf: NO ($(printf '%s' "$out" | head -c 160))"; ok=0; fi
else echo "terraform fmt -check accepts folder_reader_iam.tf: NO (file absent)"; ok=0; fi
[ "$ok" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
