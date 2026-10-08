# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 27 -- the Lambda deploy at pin 325bd4e0f8 (RIV-ho-1, RIV-rk-1, RIV-tw-1) and ONE republish of 2026-10-08

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-08 ~13:4xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

## VERDICT: SIGNED

Conditions: the plan applied is `C:/tmp/rv_apply27.tfplan` made at pin 325bd4e0f8 in `C:/tmp/rv-r8`, 0 to add, 5 to
change, 0 to destroy; a NEVER-2 ledger entry `etfs-rivalfunds-r27` is opened before the apply; the apply and the
republish do not run inside 10:55Z-11:15Z or 12:55Z-13:15Z; every read below holds at the apply.

## Blast radius

- **What moves:** the code package of the five rivalfunds Lambdas (daily, fetch-holdings, build-silver,
  build-canonical-shape, publish-page). Nothing else in the plan: no IAM, no schedule, no memory, no environment.
- **What the package gains over the deployed pin 0576fb051f** (`git diff --stat` over the seven staged paths of
  `rivalfunds_package.py`, tests left out): 4 files, +257 -12 -- `enrichment_bloomberg.py` +113 (never run by a
  Lambda: it is the vehicle's file), `history_owed.py` +77 (new; imported only by that file behind the switch),
  `gold_holding_contribution.py` +75 -12 and `gold_canonical_shape.py` +4 -4 (the reader, RIV-rk-1). `lib/`,
  `infra/logic/registry`, the naming schema and `etf_positioning_gold.py`: 0 lines.
- **What the republish may write** (payload: daily Lambda, `only: [publish-page]`, date 2026-10-08, mode daily,
  sink s3, `refresh_a1` true -- the payload run under ledger `etfs-rivalfunds-r26` leg L3): one `input_census` object and
  its state record (as on round 26). The tables and the page are written only if their content differs.

## The expected outcome, read from the producer's rule, both branches

Writers of the served tables and page on this path: 1 (the daily Lambda's publish-page step with `refresh_a1`); its
rule is `write_unique` -- an object is put only when no object of the same content digest exists at the date -- and the
publisher puts a page only when the rendered bytes differ from the served bytes.

- **Branch A, expected: nothing but the census is written.** Evidence: (1) the round-27 code and the deployed code,
  run on this box over the same live inputs for 2026-10-08, name their tables with the SAME content digests --
  `buying_trend` 76800731cb5d and `holding_contribution` 2200e2c0b9ad from both -- and differ bit-for-bit in no column
  but `revision` and `produced_at`. (2) Against the served objects of 13:00Z (`before_after_tables_2026-10-08.r27_deploy.json`):
  holding_contribution 0 moved of 6,074, buying_trend 0 moved of 1,417 (tolerance 1e-12 abs, 1e-9 rel); 13 of 13 chart
  objects' `securities` data identical; audit page byte-equal.
- **Branch B, stated because it is reachable:** this box's digests differ from the Lambda's own (served
  `buying_trend` ebed8c26b96b, `holding_contribution` db6b4ec57a4e): three float columns differ in the last digit
  between a Windows run and the Lambda's (e.g. 0.9926820140465206 against 0.9926820140465203). That is platform, not
  round 27, by (1). If the Lambda nonetheless wrote NEW table objects, the page would be re-rendered and every AI
  account's badge would read "Grounded on an earlier build" with a "Written against earlier tables" line, until the
  next 13:00Z sweep (63 regions of `index.html` on this box's run show exactly that and nothing else). No figure
  would move. On branch B this seat reports it the same turn and does NOT roll back for it alone.

## One figure by hand (R14)

Not offered as new: no figure moves on either branch. The round's hand read stands in the CVO's ADJUDICATION_v35
(three owed units against the stored closes) and v36/v37 (the 11:00Z and 13:00Z pages).

## Rollback, per key

- Lambdas: apply a plan made at pin 0576fb051f (content of the five packages as deployed 01:41Z 2026-10-08); then
  fd633ec4d2, then f9f8334ef6, as before.
- Objects: none to remove on branch A (the census object is additive and read by nothing served). On branch B the new
  table objects are newer revisions at the same date; removing them is an S3 delete and needs a human's word -- the
  remedy is instead the next sweep, which re-grounds the accounts.

## Not covered by this half

- The switch `RIVALFUNDS_HISTORY_OWED`: a Lambda never reads it (the file that does is the vehicle's). Unset everywhere.
- RIV-tw-1's own read: the 2026-10-09 11:00Z vehicle run (the merge's pair, already whole).
- The pin is a commit of site-Z CLOUD made BEFORE 0.0.0_AB_MSTR~Z's merge window of 13:24Z; the deploy does not carry
  origin's 908 commits. The first deploy after that merge lists what origin changed in the seven staged paths.
