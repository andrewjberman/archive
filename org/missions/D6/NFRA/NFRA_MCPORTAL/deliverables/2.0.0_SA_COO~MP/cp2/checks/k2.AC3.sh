#!/usr/bin/env bash
# MP-k-2 AC3 (the never-widen pair before the act, and NEVER-2 after it; ruling msg 32404): at HEAD,
#   - the ASK deliverables/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-k-2.md exists;
#   - BOTH halves exist and each cites the ASK by path: deliverables/1.0.0_SA_CTO~O/NEVER_WIDEN_HALF_CTO_MP-k-2_*.md and
#     deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-k-2_*.md;
#   - the ledger entry for slug nfra-mcportal-cp2-close-request-grant is committed, its sentinel is gone, and
#     deploy_ledger.py list does not show it.
# (That the halves PRECEDE the apply is the order's step order and the issuer's drain read, not this check.)
. "$(dirname "$0")/_root.sh"
PD=org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables; SLUG=nfra-mcportal-cp2-close-request-grant
ask=no; git cat-file -e "HEAD:$PD/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-k-2.md" 2>/dev/null && ask=yes
h=0; for f in $(git ls-tree -r --name-only HEAD "$PD/1.0.0_SA_CTO~O/" "$PD/2.0.0_SA_COO~MP/" | grep -E "NEVER_WIDEN_HALF_(CTO|COO)_MP-k-2_[^/]*\.md$"); do
  git show "HEAD:$f" | grep -qF "NEVER_WIDEN_ASK_MP-k-2.md" && h=$((h+1)); done
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
l=$(timeout 60 python .tools/deploy_ledger.py list 2>&1); listed=$(printf '%s\n' "$l" | grep -c -- "$SLUG"); den=$(printf '%s\n' "$l" | grep -m1 'SCAN DENOMINATOR' || echo "(no denominator)")
echo "ask=$ask; halves citing the ask=$h of 2; entry files at HEAD=$entry; sentinel at HEAD=$sent; listed OPEN/HELD=$listed; $den"
if [ "$ask" = yes ] && [ "$h" -ge 2 ] && [ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$listed" = 0 ] && printf '%s' "$den" | grep -q 'SCAN DENOMINATOR'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
