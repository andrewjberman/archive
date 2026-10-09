#!/usr/bin/env bash
# AMGT_RESAPP round 87 -- the issuer's ONE REAL RUN at close (read-only: the live function, the stored name list, the stored drafts).
#   bash r87_real_run.sh   prints every block's verdict lines; run from the repository root.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
D="org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1"
FN=opal-amgt-scoped-api
hash() { .tools/aws lambda get-function-configuration --function-name "$FN" --query '[CodeSha256,LastModified]' --output text; }
v() { grep -E "^(PASS|FAIL)|: (YES|NO)| ALL: " ; }
echo "# AMGT_RESAPP round 87 -- the issuer's one real run, $(date -u +%Y-%m-%dT%H:%M:%SZ), $(hostname | tr A-Z a-z)"
echo "## live function hash before"; hash
echo "## r87_withheld deployed (ll-1 via ll-3, ll-2)"; python "$D/round87_prep/checks/r87_withheld.py" --crit AC1 2>&1 | v
python "$D/round87_prep/checks/r87_withheld.py" --crit NU --keys NU_US_Equity 2>&1 | v
echo "## r87_dossier deployed (ll-3, AMGT_CORPUS /9)"; python "$D/round87_prep/checks/r87_dossier.py" --want amgt-corpus-dossier/9 2>&1 | v
echo "## r87_rows (ll-4 ledger)"; python "$D/round87_prep/checks/r87_rows.py" --ledger "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~348/DISPOSITION_LEDGER.json" 2>&1 | v
echo "## r86_description deployed (round 86, no regression)"; py -3.12 "$D/round86_prep/checks/r86_description.py" --crit AC1 2>&1 | v
echo "## r85_sentences deployed, outside company_description, vs the r86 base (kk-3)"
py -3.12 "$D/round85_prep/checks/r85_sentences.py" --crit AC1 --where deployed --exclude-section company_description \
  --base-file "$D/round86_prep/checks/r86_sentences_base.json" 2>&1 | v
echo "## r85_crosswalk AC1 on the latest stored name list (kk-1, AMENDMENT 4 admit list)"
python "$D/round85_prep/checks/r85_crosswalk.py" --crit AC1 --reference crosswalk/v1/2026-10-07.json \
  --admit as_of,denominators.with_issuer_cik,research_universe.read_at,research_universe.folders,denominators.research_folders_live,research_universe.source 2>&1 | v
echo "## r84_listing deployed (kk-1 AC2)"; python "$D/round84_prep/checks/r84_listing.py" --crit AC1 --where deployed 2>&1 | v
echo "## r86_yield on kk-5's offline NU draft (floor 29)"
py -3.12 "$D/round86_prep/checks/r86_yield.py" --crit AC1 --floor 29 \
  --draft "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~345/offline/draft.json" 2>&1 | v
echo "## kk-4 issuer sources (writers)"; py -3.12 -m pytest lib/research/identity/tests/test_writers_carry_issuer.py -q 2>&1 | tail -1
echo "## kk-1 guard tests"; py -3.12 -m pytest lib/research/identity/tests/test_crosswalk_refuses_absent_library.py -q 2>&1 | tail -1
K=ASML_NA_Equity,BABA_US_Equity,NU_US_Equity,PBR_US_Equity,SAP_GY_Equity
echo "## r84_store AC1 + AC2 (five names)"
python "$D/round84_prep/checks/r84_store.py" --key "$K" --crit AC1 --where deployed 2>&1 | grep -E " ALL: "
python "$D/round84_prep/checks/r84_store.py" --key "$K" --crit AC2 --where deployed 2>&1 | grep -E " ALL: "
echo "## r80-r82 deployed (no regression)"
python "$D/round82_prep/checks/r82_deployed.py" 2>&1 | grep -E "DEPLOYED"
python "$D/round81/checks/r81_deployed.py" 2>&1 | grep -E "DEPLOYED"
python "$D/round80/checks/r80_deployed.py" 2>&1 | grep -E "DEPLOYED"
echo "## live function hash after"; hash
