#!/usr/bin/env bash
# co4_batch16.sh -- READ-ONLY. Is tests/test_cj2_slash_key_one_form.py named in batch 16's test list (order OG-rl-17)?
# Run from the worktree root:  bash <deliverables>/co4_batch16.sh > co4_batch16.out
# No AWS call. No write. Local git objects, the named check folders, the named order, one git ls-remote.
set -u

TEST=test_cj2_slash_key_one_form
TPATH=infra/aws/ec2/opal-gateway/tests/test_cj2_slash_key_one_form.py
ORDER=org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-17.round-47-sixteenth-batched-release-the-client-fences-the-size-caps-and-the-in-flight-guard.md
CHK1=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r47/checks
CHK2=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks
BASE_SHORT=13917ef993
BASE_FULL=13917ef993207bee6b8df0124eec5444da4d62cd
RELBR=rel-nfra-oplgtw-batch16

# Word-boundary ERE so a longer name containing the test name does not count.
RE_T="(^|[^A-Za-z0-9_])${TEST}([^A-Za-z0-9_]|\$)"
RE_CTL_POS="(^|[^A-Za-z0-9_])test_og_mg3([^A-Za-z0-9_]|\$)"
RE_CTL_NEG="(^|[^A-Za-z0-9_])test_zz_not_a_test([^A-Za-z0-9_]|\$)"

# occ ERE file... -> prints the number of matching occurrences; prints ERROR on a grep error (rc>1)
occ() {
  local out rc
  out=$(grep -oE "$1" "${@:2}")
  rc=$?
  if [ "$rc" -gt 1 ]; then
    echo "ERROR"
    return 2
  fi
  printf '%s\n' "$out" | grep -c .
}

yn() { # yn <count-or-ERROR> -> yes|no
  case "$1" in
    ERROR) echo "ERROR" ;;
    0) echo "no" ;;
    *) echo "yes" ;;
  esac
}

if [ ! -f "$ORDER" ]; then
  echo "ERROR: order not found: $ORDER"
  exit 2
fi
if [ ! -d "$CHK1" ] || [ ! -d "$CHK2" ]; then
  echo "ERROR: check folder not found: $CHK1 or $CHK2"
  exit 2
fi
echo "NOTE order=$ORDER"

# 1. CONTROLS
ctl_pos=$(occ "$RE_CTL_POS" "$ORDER")
echo "CONTROL-POSITIVE named_test=test_og_mg3 order_mentions=$ctl_pos"
ctl_neg=$(occ "$RE_CTL_NEG" "$ORDER")
echo "CONTROL-NEGATIVE named_test=test_zz_not_a_test order_mentions=$ctl_neg"

# 2. ORDER AND CHECKS
ord_n=$(occ "$RE_T" "$ORDER")
echo "B16-ORDER named_in_order=$(yn "$ord_n") count=$ord_n"

for f in "$CHK1"/* "$CHK2"/*; do
  echo "NOTE searched file=$f"
done
chk_n=$(occ "$RE_T" "$CHK1"/* "$CHK2"/*)
echo "B16-CHECKS named_in_checks=$(yn "$chk_n") count=$chk_n"
for f in "$CHK1"/* "$CHK2"/*; do
  if grep -qE "$RE_T" "$f"; then
    echo "NOTE hit file=$f"
  fi
done

# 3. BASE TREE (positive control beside the read)
if MSYS_NO_PATHCONV=1 git cat-file -e "${BASE_SHORT}^{commit}"; then
  if MSYS_NO_PATHCONV=1 git cat-file -e "${BASE_SHORT}:infra/aws/ec2/opal-gateway/app/tools.py"; then
    echo "CONTROL-BASE-POSITIVE path=infra/aws/ec2/opal-gateway/app/tools.py in_base=yes"
  else
    echo "CONTROL-BASE-POSITIVE path=infra/aws/ec2/opal-gateway/app/tools.py in_base=no"
  fi
  if MSYS_NO_PATHCONV=1 git cat-file -e "${BASE_SHORT}:${TPATH}"; then
    base_in=yes
    base_blob=$(MSYS_NO_PATHCONV=1 git rev-parse "${BASE_SHORT}:${TPATH}")
  else
    base_in=no
    base_blob=none
  fi
else
  base_in=unread
  base_blob=none
  echo "NOTE base commit ${BASE_SHORT} is not in this box's object store; in_base_tree=unread"
fi
echo "B16-BASE in_base_tree=$base_in blob=$base_blob base=$BASE_SHORT"

# 4. FULL-SUITE CLAUSE IN THE ORDER
suite_lines=$(grep -n -i "full suite" "$ORDER" | cut -d: -f1 | tr '\n' ' ')
if [ -n "$suite_lines" ]; then
  suite_yn=yes
else
  suite_yn=no
fi
echo "NOTE full-suite clause ORDER line(s): ${suite_lines:-none}"
echo "B16-SUITE full_suite_run_stated=$suite_yn"

# 5. RELEASE BRANCH AT ORIGIN (one read-only ls-remote)
lsr=$(git ls-remote origin "refs/heads/${RELBR}")
lsr_rc=$?
if [ "$lsr_rc" -ne 0 ]; then
  rel_yn=ERROR
  lsr_lines=ERROR
else
  lsr_lines=$(printf '%s\n' "$lsr" | grep -c .)
  if [ "$lsr_lines" = "0" ]; then
    rel_yn=no
  else
    rel_yn=yes
  fi
  echo "NOTE ls-remote origin refs/heads/${RELBR}: $lsr"
fi
echo "B16-REF release_branch_at_origin=$rel_yn ls_remote_lines=$lsr_lines"

# 6. VERDICT (IN if named in the order or the checks; PARTIAL if not named but in the base tree and a full-suite run is stated; else ABSENT)
ord_yn=$(yn "$ord_n")
chk_yn=$(yn "$chk_n")
if [ "$ord_yn" = "yes" ] || [ "$chk_yn" = "yes" ]; then
  verdict=IN
elif [ "$base_in" = "yes" ] && [ "$suite_yn" = "yes" ]; then
  verdict=PARTIAL
else
  verdict=ABSENT
fi
echo "CJ2-IN-BATCH16 named_in_order=$ord_yn named_in_checks=$chk_yn in_base_tree=$base_in full_suite_run_stated=$suite_yn release_branch_at_origin=$rel_yn verdict=$verdict"
