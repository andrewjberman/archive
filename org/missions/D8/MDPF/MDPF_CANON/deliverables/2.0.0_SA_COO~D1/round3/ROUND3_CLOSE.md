# MDPF_CANON round 3 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-11 ~05:2xZ)

Round 3 is the CTO's round-2 analysis (msg 3367 @71e85b7191), cut in one issuance @335258e392 as three cells. This packet asks the CVO
for the three judgment grades the orders left open.

| item | value |
|---|---|
| issuance | @335258e392: 3 cells, risk WORLD, fanout 2 of 2 chains, cap 8 |
| amendments | 1 @96d6e08aea (CTO msg 3417), 2 @dac583381b (msg 3431), 3 @608e838689 (msg 3457). Gate limb: only GATE (viii) graded a modification; placeholders NONE |
| `CN-c-1` global basis (X2) | ~8, `945e1add0c`, drained @b3c9b5a55e. `r3_checks.py basis` 3/3, proof VALID |
| `CN-c-2` bronze feed as a registry row, generated homes, runner grant | ~9, `5055246d57`, drained @86755fa58b. writer 3/3, homes 3/3, libs 5/5, proof VALID |
| `CN-c-3` the Inflection feeder reads the builder's address | ~9, `7ea0196750`, drained @d437b0648f. reader 3/3, proof VALID |
| deploy | CloudOps ~DELL1 `ADHOC.canon-r3-bronze-intake` @4addd887d7, COMPLETE @e81cc5d6fa (msg 3506), C1-C6, ledger CLOSED 05:06Z, 7 of 7 legs |

`round-close-check.py --round 3` before this packet: 3 of 3 complete, proof_ok 3, verdict REFUSED on the three judgment criteria below.

## The real runs (what each judgment is graded on)

- **CN-c-1 AC3:** `deliverables/0.9.0_WK_MDPF_CANON~8/X2_GLOBAL_BASIS.md` (headings: Field families, Single-firm entries, Method), read
  from the objects `portal/gold/mdpf/{global,cottonwood,inflection,49financial}/...` at as-of 2026-10-08. Disclosed by the worker, and
  not a defect of the file: the basis states what the served objects emit, and in part it contradicts the round-2 premise
  (rows W8-S1..S4: two global by_model entries held by no firm scope; the identity at `dim_mdpf_aggregate_aua_timeseries.py:2257` holds
  on 460 of 484 non-null dates; 7 of 9 single-firm account-distribution entries differ from their firm's total_aum, `generated_at`
  differs by a day). The grade asks whether a seat that did not write the file reads back every `min firms` integer and every
  single-firm account count equal.
- **CN-c-2 AC4:** ledger legs L2, L3-L5, L6 (`org/critical_paths/change_management/20261011T0439Z_mdpf-canon-r3-bronze-intake-dell1-20261011_deploy_completion.md`).
  - One on-demand Stage-0 pull on the runner, SSM `f1b89351-3669-479a-868a-598939f07e92`, PULL_EXIT=0, errors [].
  - Listing under `s3://opal-data-assets/mdpf/inflection/bronze/orion_model_composition/date=2026-10-11/` = 10 objects (nine
    `model_<id>.json`: 83,84,85,86,87,88,89,152,153, plus `_meta/pull_complete.json`). The old prefix holds no 2026-10-11 key.
  - Measured again by this seat at 05:1xZ, independent of the ledger: `code/config/bronze_homes.json` ETag
    b2d27b65d2e766f9ce599503793bb985, 464 B; builder prefix 1040 objects (1030 copied history + 10 from the pull); source prefix 1030,
    untouched.
- **CN-c-3 AC3 (`/seams`, writer to reader):** ledger leg L7. The feeder ran locally with `--bronze-source s3` and no `--upload`,
  its bronze resolved from `bronze_homes.json`, against the live `s3://opal-data-mdpf/mdpf/feeds/*/inflection/2026-10-09.parquet`.
  - Default eclipse date 2026-10-10 differed (model_aua_positions 579 vs 578 rows, non_model_aua as_of): input vintage, not bronze.
  - Re-run with `--eclipse-date 2026-10-09` (the live feed's as_of): model_composition 171, model_aua_positions 578, non_model_aua 1 =
    750 rows, DELTA=0 on every data-bearing column; only `_ingested_at` differs. Nothing written to S3.
  - What this does not show: the live parquet was built from the OLD home on 2026-10-09 and this read took the COPIED history at the
    new home for that date. It shows the copy is faithful and the reader resolves the new address; it does not show a new-home
    daily delivery. That arrives with the first routine run (below), and is confirmation only.

## For the CTO at L10 (not this packet's ask)

- **W8-S2, W8-S3 (ARMED, disarm owner this lane):** the global fold re-emits two entries no firm holds and a composition identity
  that fails on 24 dates. They route to the owner of `dim_mdpf_aggregate_aua_timeseries.py`; X2 is already GRANTED (row W8-S5, ARMED,
  Andrew's to re-read against the new basis). Not acted on here.
- **W9-S7 (ARMED) and S12:** the hand sync is done and measured (row S12). The code/ prefix is still about 20 commits behind HEAD
  outside these three files, and no repo script writes it; whether to automate the repo-to-code copy is a CTO or CloudOps ruling.
- **W9-S6:** `generated_locals.tf` drift that predates us (four `4698` keys); kept as the generator wrote it.
- **The runner** i-02448edb624a7a7cf was started by the order and reads RUNNING; row S12 states the next dispatch stops it at its
  own end. Nothing owed from a human unless that read is false at the next fire.

## Carried (not this round's acts)

1. **2026-10-11 13:30Z and 2026-10-12 13:30Z daily fires** -- read each with `r2_daily.py read --fire <fire>`. The first fire that
   runs is the first routine delivery to the builder's keys (the Sunday fire if weekends run, else Monday); its read grades FWD-1 and
   CN-a-2 AC3 together with the round-2 reads.
2. Row dispositions of the earlier rounds (D1-S3..S6 ARMED, W5-S1, W7-S1, S9) are the CVO's adjudication rows; none is cleared here.
