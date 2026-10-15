# NFRA_CTLPLN round 15 -- the issuer's inputs for the round-15 analysis (2.0.0_SA_COO~C, DRAFT 2026-10-15 ~04:4xZ)

**Status:** CT-ae-2 and CT-ae-3 are merged and `complete`. CT-ae-1 is with worker ~97, not yet reported; its section is a placeholder and is filled at the drain. Nothing here is sent until every order of the round is terminal.

## A. CT-ae-2 -- `complete` (merge `833f1d7bb7`, flip `d531251edb`)

- `INLINE-HOLIDAY-SETS found=6 same_2026_2027=5 differs_2026_2027=1 unreadable=0 ok=True`. Six hand-typed sets, not the two the row named.
- SAME: `NYSE_HOLIDAYS` in `bd-49f-freshness-probe`, `bd-cot-freshness-probe`, `mdpf-daily-trigger`, `mdpf-freshness-checker`, `opal-assets-daily-emitter`.
- DIFFERS: `inf-gold-freshness-guard` (`MARKET_HOLIDAYS`, frozenset-wrapped literal): the ten 2026 closures match; none of the ten 2027 closures is present; first miss 2027-01-01.
- Routed by the CTO (msg 109290): dell1's, import `lib/trading_calendar` at the next deploy, before 2026-12-31. Row `NFRA_CTLPLN-S9125` (`c38dff9cf3`) names dell1 as owner.
- The order text routed a difference to MDPF; the measure found it in an INF Lambda. The order and the record disagree on routing; the CTO's ruling stands.

## B. CT-ae-3 -- `complete` (merge `193269c452`, flip `0c5972dc80`)

- `ROUND15-BATCH arms=9/9`, `OPEN-CALL-ACT-ROOTS arms=8/8`, `SAFE-COMMIT-DERIVATION cases=17/17`; proof instance VALID.
- Files mode matches a roots-named row of any kind through its roots field (the act rule unchanged). An ENFORCE refusal of the naming stage unstages every path in `IN_SCOPE` (WARN unchanged). `infra/.gitignore` ignores the census checkpoint. The identity-root search found no remaining `simulate_policy` mention.
- Carried: `NFRA_CTLPLN-W99-S1`. The placement-refusal branch of the naming stage (about `.tools/safe-commit.sh:1183-1188`) still unstages only the graded files, the same shape as `W93-S1`. INERT; the order named the ENFORCE branch only. A candidate for a later batch cell.

## C. CT-ae-1 -- placeholder

Worker ~97 is running in a fresh worktree. Its earlier run was cut off and its worktree and branch were removed (see D), so it restarted from the issuance commit. Fill with: whether tree B survived and tree A died, whether `kill-maint.ps1` or `seat-boundary.ps1` changed, the criterion lines, the merge.

## D. Process facts for the analysis

1. **Spend limit.** All three round-15 workers stopped on an HTTP 429 at about 00:5xZ. Andrew lifted it at about 03:2xZ ("Youre bot limited keep working"; record `ANDREW_WORD_SPEND_LIMIT_LIFTED_20261015.md`, `9611167855`). No spawn was attempted in between. Call 3717 was closed by the CTO on his word.
2. **A worktree and its uncommitted work can be removed while a worker is cut off.** `ctlpln-97` sat at the issuance commit, which trunk contains, so the standing merged-worktree cleanup removed it with its branch; one uncommitted test file was lost. A worker that is cut off should commit a WIP commit early. Candidate face line: "commit a work-in-progress commit as soon as a file exists".
3. **Proof-instance schema.** Worker ~99's first proof instance was schema-invalid (`config` is not an allowed artifact kind; controls lacked `determinism` and `mutant`) and cost two commits. A worker face that names an existing instance to copy field names from would have avoided it.
4. **Merge before flip.** The L6 gate refuses a `complete` flip until the proof instance is in the main tree, so the order is: re-run on the branch, merge through `safe-merge.sh`, then flip. Recorded so the next drain does it in that order.
5. **Attribution trailer.** Worker ~99 noted the face's trailer names Sonnet 5.5 while the worker runs haiku. The CTO's round-14 fact says faces need not name the model; the trailer text is the issuer's commit convention, not a claim about the worker.
6. **Close of an Andrew-act call by a seat is refused** (`open-calls.py close` reads CROSS-BOX and wants a CLOSED-BOTH file). The CTO closes it as `ruled_by=andrew`. The seat's route is one message to the CTO with the record path.

## E. Open at the end of the round (so far)

- FWD-11: a qualified wait on Andrew's word (call `laptop-20261014T205216Z-7841`); cut fresh after he names the hour.
- Carried with owners: `S9125` (dell1), `W99-S1` (a later batch), `S9119` (dell2 writer), `S9103`, `S9120`, `S9122` (per CVO), `Z-S3` and `W12-S1` (each function's next deploy), `W89-S3` (ADVI_FIRMBKTS).
