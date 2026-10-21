# AR-g-183 AC2: the issuer's re-grade on the full tree (2026-10-21)

Order `IRPT_ANLREQ.TO-AR-g-183` (worker `0.9.0_WK_IRPT_ANLREQ~356`). The worker's proof instance records AR183-g-AC2 as FAIL
(`AR-REASON-tests-FAIL rc=1 passed=22 ... 11 failed, 22 passed, 18 errors`) because its sparse worktree omitted two committed inputs of
the four test files: `data/firm_registry.json` (row IRPT_ANLREQ-D2-W356-S1) and `infra/aws/ec2/investor-reporting-ycharts/`
(row IRPT_ANLREQ-D2-W356-S2). Both gaps are the issuer's sparse cone, not a defect of the cell.

Re-run by the issuer `2.0.0_SA_COO~G2` on the full main tree after the merge of `wk-IRPT_ANLREQ-356` (merge `c02fdd2fd64`):

| invocation | result |
|---|---|
| `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_reason_checks.py reason` | `AR-REASON-reason-OK` |
| `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_reason_checks.py tests` | `AR-REASON-tests-OK passed=51` |

The worker's proof instance is left as the worker wrote it (the lane protects it); this file supersedes its AC2 FAIL, and the order flips to
complete on this re-grade. Rows W356-S1 and W356-S2 are dispositioned by this note: the sparse cone for the next worker order adds
`data/` and `infra/aws/ec2/investor-reporting-ycharts` for any cell whose tests read the firm registry.
