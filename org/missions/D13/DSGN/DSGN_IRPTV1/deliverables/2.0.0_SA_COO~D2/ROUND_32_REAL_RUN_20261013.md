# DSGN_IRPTV1 round 32 -- the one real run of each outcome (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~00:1xZ-00:3xZ)

**Instrument.** A local build of the round-32 candidate (portal DEV cf52fdbf plus the five commits of worker ~73: branch `wk-DSGN_IRPTV1-73-portal` @64980b4d in the portal repository, LOCAL, a
fast-forward of origin DEV, not pushed), served on port 5174 from a workspace worktree, walked with the project's /ui-walk instrument signed in as the dormant walker account against live
data (read-only; the walker armed and disarmed itself and the post-disarm login was refused). Walk folder `tmp/ui-walk/20261013T001612Z` (local, gitignored, client data: screenshots are not
committed). Words only below; no client name and no figure.

**Drain checks (once, after the merges).** At the candidate's workspace worktree: `bun run typecheck` rc 0; `bun run lint` 0 errors (348 warnings, by the worker, rc 0); `bun test src/pages/InvestorReporting`
1222 pass, 27 skip, 1 fail (F14-AC3, the base failure that predates the round); base measured before the cut 1216 pass, 27 skip, 1 fail. IV-e-123 changed no portal file.

| outcome | cell | what the real page showed |
|---|---|---|
| the ACCOUNT node id against the account id (a read) | IV-e-123 | A READ, no page outcome. 31 of 31 producer paths read; the live 49 Financial builder mints node ids from the Schwab balance key, the directory from gold dim_account, so the ids are equal only where the two strings are equal; INF equal by rule; COT declared equal. The producer refuses or withholds an unequal account. On the real page a served 49 Financial client's one-account Holdings view showed that account's own value (read in the round-31 walk, ROUND_31_REAL_RUN_20261012.md; not re-walked in this round). The page map the CTO asked for has no source on the wire (row W72-S1). |
| the unsupported-card reason in words | IV-e-124 | PARTLY OBSERVED. On the real page an opened served vendor report (104 cards, all SUPPORTED; its producer verdict reads certified) showed no regression: every card title a name (0 codes), the one validation sentence and "Source: a vendor's report." on the face, outside the closed details; the walker counted the new reason text 0 times and the producer word UNCERTIFIED 0 times in the dialog. NOT OBSERVED on live data: an unsupported card, because the first Ready request the walker opens carries no UNCERTIFIED report. The new sentence ("The producer could not confirm this figure: N values in this report could not be confirmed.", and for a report with no producer verdict a sentence of its own) is proven on synthetic data by the worker's rendered test, its mutant and its screenshot; the issuer re-ran the whole suite and the criterion but did not re-render that synthetic page. |

**Not done here.** No UNCERTIFIED vendor report was opened on live data; no Opal report was walked (the worker's before and after render is byte-identical).

**Push state.** Workspace commits LOCAL on box/dell2; the portal candidate branch `wk-DSGN_IRPTV1-73-portal` @64980b4d is LOCAL in the portal repository. Nothing is pushed.
