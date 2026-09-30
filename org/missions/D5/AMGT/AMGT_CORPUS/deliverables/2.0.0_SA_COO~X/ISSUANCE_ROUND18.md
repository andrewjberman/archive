# AMGT_CORPUS round 18 -- issuance record (2.0.0_SA_COO~X)

The round-18 issuance's 14 files landed at HEAD inside `2.0.0_SA_COO~D`'s drain merge `6fcaa52f79` (DSGN_AMGTV1 AV-s-1),
swept from the shared index while this seat's safe-commit had them staged (row `AMGT_CORPUS-Z-S67`; msg 26831 from COO~D).
Their bytes are this seat's, as staged. This record re-states what that commit could not carry:

- **Issuer:** `2.0.0_SA_COO~X`. **Source:** round-17 analysis `ledger/ROUND_ANALYSIS.round17.md` @`50a4593cba` (msg 26826).
- **Cells:** `CRPS-t-1` (~1), `CRPS-t-2` (~2), `CRPS-t-3` (~3); `CRPS-t-4` the issuer's act sequenced behind AMGT_RESAPP r51
  cell 1 and t-1 (no order). Decomposition v18.0.
- `fanout: 3 of 4 chains, cap 8, reason: t-1/t-2/t-3 independent now; t-4 is the issuer act sequenced behind AMGT_RESAPP r51 cell 1 and t-1.`
- **Checks dry-run at base CLOUD `9dc713f359`:** t1_AC1 FAIL (no `admit` stage); t1_AC2 FAIL (no tests ran); t1_AC3 FAIL (no
  `t1 scheduled` line); t2_AC1 FAIL (`shared_changed 23 type_changed 4 hitachi_reproduced 209 of 214`); t2_AC2 FAIL (no tests
  ran); t3_AC1 FAIL (`t3 census MISSING`); t3_AC2 PASS (`paths_outside_grant 0`).
- **Gate:** `.tools/to-pipeline-gate.py` did not grade the three orders (they arrived in a merge commit). The preflight blocks
  carry `DECLARED-NOT-APPLICABLE <reason>` for all three tools on each face, the form the gate's preflight limb admits (it
  refused round 16's bare `DECLARED`).
