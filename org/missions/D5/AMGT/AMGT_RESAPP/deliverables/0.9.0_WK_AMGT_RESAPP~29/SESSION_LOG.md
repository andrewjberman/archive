# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~29 -- AMGT_RESAPP.TO-AMGT-rk-17

Worktree: C:/tmp/wk-amgt-12-29, branch wk-amgt_resapp-12-29, tip ed8d4fe3de (fresh; nobody worked here before).

## What this order was

AMGT-rk-17 -- verify (not run) the two Bloomberg pulls the issuer (2.0.0_SA_COO~Z) already ran directly on
Andrew's word at 20:18-20:20Z UTC 2026-09-16: the model-block pull over the 33 keyed crosswalk names, and
the price-axis pull. The order is explicit that both runs already happened and that re-running either
producer is forbidden. The worker's job is entirely verification against the live store plus the crosswalk,
per five acceptance criteria (AC1-AC5), and writing the proof-of-spec instance.

## What was done

1. Printed `git rev-parse --abbrev-ref HEAD` (wk-amgt_resapp-12-29) and confirmed org/, .tools/ and every path
   in section 3 exist. No BLOCKING row.
2. Ran AC1 (crosswalk live read): records 89, keyed_names 33, all 33 names printed, matching the issuer's
   dry-run pre-state exactly. PASS.
3. Ran AC2 (raw/bloomberg/ live read, ISSUER AMENDMENT 17 split): raw_keys 34 (>= 30 bar). PASS.
4. Ran AC3 (derived/model_block/ live read, ISSUER AMENDMENT 17 split): attempted 33, blocks_landed 34,
   landed_of_attempted 33 of 33, missing 0. PASS.
5. Ran AC4 (DynamoDB opal-harvest-security-metrics scan): 194 items scanned, 3 TRENDING_PRICE axis_date
   values found (two pre-existing at 2026-09-10, one new generation-tagged), newest_axis_date 2026-09-15 --
   later than the pre-state's 2026-09-10. PASS.
6. Ran AC5 (schtasks census): opal_shaped_tasks 11, exact match to the issuer's pre-stated 11-task list
   including the FreezeTripwire duplicate; no new task, no re-enabled task. PASS.
7. Ran a MUTANT CONTROL: re-executed AC3's live listing with the OLD (pre-amendment-17) single-segment
   key split. It reproduced the exact defect the amendment describes -- landed_of_attempted 31 of 33,
   missing ['BP/_LN_Equity', 'NG/_LN_Equity'] -- confirming the fix in the current invocation is real and
   not merely asserted.
8. Ran a DETERMINISM CONTROL: AC1 and AC5's live reads were each run twice; both pairs printed identical
   deciding values across runs.
9. Wrote the proof-of-spec instance, ran `python .tools/proof-of-spec-check.py <instance> AC1,AC2,AC3,AC4,AC5`.
   First pass returned rc=1 with two violations: (a) artifact-coverage on the DynamoDB artifact row (no
   acceptance row referenced it by token or `artifact_covered_by`); (b) invocation-alignment[AC3] -- the
   AC3 invocation as relayed verbatim in this worker's WORKER FACE (spawn prompt) read `import boto3,json`
   while the governing task-order FILE on disk at ed8d4fe3de:121 reads `import boto3,json,io`. Fixed both:
   added `artifact_covered_by: ["AC4"]` to the DynamoDB artifact row, and corrected AC3's recorded invocation
   to the file-literal string (re-run first to confirm byte-identical output with and without the unused
   `io` import). Second pass: rc=0, violations=0, VALID.
10. Filed surprise row AMGT_RESAPP-Z-W29-S1 (OBSERVATION/INERT/GROUNDED) documenting the WORKER FACE vs
    task-order-FILE text divergence on AC3's invocation -- caught mechanically by the checker, corrected,
    no bar moved. Spliced into the one fenced JSON array in INVESTIGATION_v1.md by textual append (307 rows
    total after; 0 CRLF, 0 non-ASCII bytes confirmed post-splice); the file was NOT re-serialized.
11. Flipped `<status>` in the task-order file from `pending` to `complete` (RECORD FACE field, inside this
    worker's `<paths>` grant, per section 6's explicit instruction).

## Not done / declared exclusions

- Did not re-run model_block_pull.py or price_axis_pull.py (explicitly forbidden; both runs already happened).
- Did not pull the 56 unresolved (no security_key) crosswalk records (explicitly not authorized).
- Did not arm any schedule, cron, or recurring trigger (explicitly reserved; AC5 confirms nothing was armed).

## Result

All five criteria PASS by output. proof-of-spec-check.py rc=0 on the final instance. Task order status
flipped to complete. One surprise row filed (AMGT_RESAPP-Z-W29-S1), OBSERVATION/INERT, self-resolving.
