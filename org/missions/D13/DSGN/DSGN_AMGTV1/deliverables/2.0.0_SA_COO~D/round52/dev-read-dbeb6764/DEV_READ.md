# DSGN_AMGTV1 -- THE POST-PUSH READ OF PORTAL DEV `dbeb6764` (issuer `2.0.0_SA_COO~D`, 2026-10-08 ~16:4xZ)

**The push:** `0.0.0_AB_MSTR~Z`, d1b21c97..dbeb6764, on Andrew's "recs approved" (record
`org/tier1_exec/2.0.0_SA_COO~D/deliverables/ANDREW_DIRECT_20261008_155xZ_RECS_APPROVED_DSGN_DEV_PUSH_DBEB6764_THEN_PROD_PROMOTE.md`
@7eb9750741; integrator msg 31876). 5 commits, 8 files, +72 -129.

| read, by this seat | result |
|---|---|
| `git ls-remote origin DEV` in the portal | `dbeb6764eaa688230f44cfcc1763bd73db6e1142` |
| CI run 37806817498 ("CI - Build & Validate") on that sha, by `gh run view` | completed, success; 2 of 2 jobs success |
| the tree under test, `C:/tmp/wk-dsgn-amgtv1-113/portal` | HEAD `dbeb6764...`, 0 changes: the same sha as origin DEV |
| `round35/checks/instrument/instrument35.cjs`, a fresh vite build of that tree | 4 of 4 arms, rc 0; the candidate's graded cells: 76 PASS, 0 FAIL, 0 NOT_EXERCISED, 1 N/A |

The render tally equals the previous DEV read's (`round50/dev-read-4b167888/`: 76 PASS, 0 FAIL, 1 N/A), so removing the Model
tab's ledger and adding the coverage note moved no graded cell. Log: `instrument35.log` beside this file.

**Read before the push, on the same sha, and not repeated after it:** `r52.cjs` 3 of 3, `r51a.cjs` 4 of 4, `battery29.sh` ALL PASS
(0 skipped), and the walk on BA US and BP/ LN, 8 of 8 (`round51/walk/read-20261008T123449Z/`). AMD US and MSFT US were walked on
`bfba701f`, which differs from `dbeb6764` in `reasonWords.ts` and `tabs/ThesisTab.tsx` only; they were not re-walked.

**Not read:** a signed-in read of the deployed DEV site. This read is of the pushed sha's content, built locally.

**DEV moved after this read:** origin DEV is `1cbc56a7`, 9 AMGT_CORPUS commits past `dbeb6764` (5 files under
`src/pages/SecurityAnalysis`). On `1cbc56a7`, in the ~114 tree: `r51a.cjs` 4 of 4, `r52.cjs` 3 of 3, battery29 ALL PASS (0 skipped).
The render instrument was not re-run on `1cbc56a7`.

**PROD:** not promoted. PROD is `b06863fe`. The promote Andrew approved waits on the other fabrics' owners confirming their
commits in the 44-commit range (integrator msgs 31893, 31896) and on a never-widen pair (CTO msg 31880).
