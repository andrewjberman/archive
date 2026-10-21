# AR-g-186 AC3: the issuer's re-grade on the full tree (2026-10-21)

Order `IRPT_ANLREQ.TO-AR-g-186` (worker `0.9.0_WK_IRPT_ANLREQ~359`). The worker's proof instance records AR186-g-AC3 as FAIL
(`AR-GAPNOTE-tests-FAIL rc=1 passed=84 ... 1 failed, 84 passed`): one pre-existing test,
`test_no_second_classification_read_default_client_is_the_etf_classifier`, imports
`infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py`, which is tracked at HEAD but outside the worker's sparse cone (row
`IRPT_ANLREQ-D2-W359-S1`). The gap is the issuer's sparse cone, not a defect of the cell.

Re-run by the issuer `2.0.0_SA_COO~G2` on the full main tree after the merge of `wk-IRPT_ANLREQ-359` (merge `8faec6ba970`) and of
`wk-IRPT_ANLREQ-358` (`44240238b9f`):

| invocation | result |
|---|---|
| `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_gapnote_checks.py gaps` | `AR-GAPNOTE-gaps-OK` |
| `... ar_gapnote_checks.py placeholder` | `AR-GAPNOTE-placeholder-OK` |
| `... ar_gapnote_checks.py tests` | `AR-GAPNOTE-tests-OK passed=85` |

The worker's proof instance stays as the worker wrote it (its lane); this file supersedes its AC3 FAIL, and the order flips to complete on this
re-grade. Row W359-S1 is dispositioned by this note: the sparse cone for the next worker order adds `infra/aws/lambda/v2_portal/_shared` for
any cell whose tests read the classification client. The issuer's drain run of the whole `ycharts/research/tests` directory also found two
failures caused by this cell's one added CSS rule (the pinned fixture-HTML hashes); they are cut as AR-g-187.
