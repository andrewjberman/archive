# ANNOUNCE OG-gw-2 -- PHASE A (steps 1-6), numbers only, no value

Worker `0.9.0_WK_NFRA_OPLGTW~26`, round 15, branch `wk-NFRA_OPLGTW-26-r15` at CLOUD `4b6afce2d2`. Nothing applied.

1. **Released ref.** Manifest `services.opal-gateway.deployed_commit` = `af2d7629702528c050860314a7867d8ea0cecfbf`. `build_package.py` printed
   `staging from deployed_commit af2d762970`, rc 0.
2. **Content diff (deployed zip read in memory vs staged).** 11 files deployed, 11 staged: 8 SAME, 3 DIFF, 0 only-deployed, 0 only-staged.
   DIFF: `app/config.py` (27507 -> 29788 bytes), `app/data_entitlement.py` (31834 -> 32133), `org/standards/NFRA_OPLGTW_CONTRACT.json` (8806 -> 9189).
   Deployed `CodeSha256` `nhz+dwJsDJLO9X3o1exvKdQ+OYE+PraxZSop2BJt9zI=`, 54650 bytes, State/LastUpdateStatus Active/Successful.
   Behaviour changes: 1 admission change (a `dim_transaction` grant goes REFUSED -> ADMITTED, via the contract's `fields`); 0 new required config keys;
   `config.py` and `data_entitlement.py` changes do not reach any grant-writer call site. File: `GW2_BEHAVIOUR_DIFF.md`.
3. **Environment before-record.** `GW2_ENV_BEFORE.json`: 3 keys, 3 sha256 hashes (64 hex chars each), names and hashes only.
4. **Targeted plan** (`-target=aws_lambda_function.mcportal_grant_writer`, fresh sparse worktree at `4b6afce2d2`, `.build/staged` from `build_package.py`, layer zip = deployed layer v1,
   sha256 b64 `oO8BxcnG9EOvVz/pMpHlQCUGzkayANH3ryCKpNAaKfk=` equal to the live layer's `CodeSha256`; the two variables fed as `TF_VAR_*` read in memory from the live environment):
   `Plan: 0 to add, 1 to change, 0 to destroy.` rc 2. Exactly one non-no-op resource change of 4 in the plan: `aws_lambda_function.mcportal_grant_writer`, action `update`
   (in place), changing attributes `last_modified` and `source_code_hash` (`nhz+dwJs...` -> `ZyYCPPyP...`). `environment` before == after (3 keys each). Plan saved out of the repo.
   The fresh cone needed `infra/logic` (row `NFRA_OPLGTW-Z-W26-S2`).
5. **Tests.** `pytest tests` in the lambda directory: 23 passed (that run loads the worktree's source gateway tree, not the staged closure; row `-W26-S4`).
   Against the staged closure (copy of `.build/staged` + the 3 writer test files + a provenance test): 21 passed (20 writer tests + 1 provenance), 0 failed.
6. **Rollback (Terraform only).** Deployed zip bytes saved outside the repo, 54650 bytes, sha256 `9e1cfe77026c0c92cef57de8d5ec6f29d43e39813e3eb6b1652a29d8126df732`
   (its base64 sha256 equals the deployed `CodeSha256`). Rollback worktree `.build/staged` = those bytes extracted (11 files); the same targeted plan with the same variable feed: rc 0,
   `No changes`, 0 non-no-op of 4, and the rollback config's `source_code_hash` = `nhz+dwJsDJLO9X3o1exvKdQ+OYE+PraxZSop2BJt9zI=` = the live hash = the `before` of step 4's update.
   The in-place-update shape of the rollback exists only against post-apply state and was NOT observed at PHASE A (row `NFRA_OPLGTW-Z-W26-S3`); the equal-and-opposite hash pair is the measured proxy.

Rows filed: `NFRA_OPLGTW-Z-W26-S1` .. `-S4` (all OBSERVATION; S2 ARMED, disarm_owner `2.0.0_SA_COO~O`; S1, S3, S4 INERT).
