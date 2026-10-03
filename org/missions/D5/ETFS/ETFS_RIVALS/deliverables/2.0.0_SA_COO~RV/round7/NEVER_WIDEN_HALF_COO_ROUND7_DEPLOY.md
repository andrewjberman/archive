# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 7 -- deploy the five rivalfunds Lambdas and the sweep schedule input at CLOUD 75ad1e4d2e, republish 2026-10-02 ONCE, fire the sweep once with its own payload; the vehicle asks for LONG_COMP_NAME from 2026-10-05

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~23:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** round 7's 8 cells are built, re-graded by the issuer and drained.
- Issuance: ce9f61d933.
- Flips: db36578751 and 2998d045a2 (8 of 8 complete).
- Chain drains: cd5f4ed84c, 9624babb0b, b19ec42030 and 75ad1e4d2e.
- At the pin, the package suite reads 596 passed, 2 skipped, 0 failed. ruff py39 is clean, py_compile is OK, and all 20
  touched files are ASCII.
- 13 of 13 round-7 mechanical checks PASS: each was re-run by the issuer in its worker's worktree before the drain
  (sa-1 x3, pv-1, cu-1, rd-1 x3, nt-1, nm-2 x2, cg-1, cs-1).

The judgment criteria are graded by `3.0.0_SA_CVO~RV`:
- rd-1's J1 on this act's real-run page;
- sa-1's J1 on the organic 2026-10-05 09:00 ET sweep.

## VERDICT: SIGNED

Conditions:
- the pin is CLOUD 75ad1e4d2e (its package is byte-equal to 2998d045a2, where the checks ran);
- every gate below reads as stated.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-round7`).
2. **`safe-apply` of the saved plan.**
   - Plan `C:/tmp/rv_apply15.tfplan`, made from `/c/tmp/rv-fast` detached at 75ad1e4d2e after
     `rivalfunds_package.py` staged the build. The plan text is `/c/tmp/rv_plan15.txt`.
   - It reads **0 to add, 6 to change, 0 to destroy**:
     - five `aws_lambda_function.stage` `source_code_hash` changes, plus the computed `last_modified`. The before hashes are
       exactly round 6's verified set: daily ONQVdpOH, fetch +QrQbD/S, canonical 7m7xens5, silver RqrmLtL+, publish 3XoabSZo
       (live `get-function-configuration` at 23:5xZ);
     - `aws_scheduler_schedule.run["etfs-rivalfunds-sweep-daily"]`, whose target input gains `"run_path": "scheduled"`
       (pv-1). That one string is the only change.
   - No role, policy, secret, environment or trigger changes.
3. **ONE real run (the republish):** `etfs-rivalfunds-daily-lambda {"only":["publish-page"],"date":"2026-10-02","mode":"daily",
   "batch_id":"rv-publish-1002r7","sink":"s3","refresh_a1":true}`.
   - By the producer's own rule (`sweep.handler_entry`, `stamped_run_path`): an `only` fire stamps `run_path` "ad_hoc".
   - After the publish, `run_ai_step` runs. The gate is set, the day holds its publish marker, and `ai_stage.run_for_day`
     finds 2 account objects for 2026-10-02, so it returns **SKIPPED_EXISTS**: no vendor call, no attempt record, and no
     second republish.
4. **The deliberate sweep (sa-1's positive control for reachability):** `etfs-rivalfunds-daily-lambda` with the schedule's own
   payload and the date made concrete: `{"date":"2026-10-02","mode":"daily","run_path":"scheduled","sink":"s3"}`.
   - The date must be concrete. A verbatim replay now would carry `scheduled-time` 2026-10-03, a Saturday, so the sweep
     would return "not a trading day" before the AI step.
   - Expected by the producer's rule, measured by a stub-runner dry run of the pin's own `run_dag` /
     `continue_open_cursors` against S3 (`C:/tmp/r7measure/r7_sweep_dry.py` -> `sweep_dry.json`):
     - `run_dag` runs **nothing** (2026-10-02 is complete);
     - there are **0 open cursors** in the 10-day lookback;
     - `detail.ai` reads `{status: SKIPPED_EXISTS, run_path: "scheduled"}`;
     - **zero writes.**
   - This proves the deployed sweep reaches the AI step and stamps "scheduled" from its own payload. Those are round 6's two
     defects: ap-1's sweep never reached the AI stage, and the 09-30 manifest claimed "scheduled" for an `only` fire.
   - **Why the positive arm is not a vendor call today.** No page day reaches a vendor call through the full sweep without
     also rebuilding a past day. The dry run, per day:
     - 10-01 and 10-02 hold accounts;
     - 09-29 is the only day with a page and no account, but its DAG would run `build-peer-group-map` and `fetch-holdings`
       (a live fetch onto a past day);
     - 09-30 would run a dozen silver and coverage rebuilds;
     - 09-24, 09-25 and 09-28 have no page.
   - So the vendor-call branch (OK/FAILED -> attempt record -> republish) is proved offline by sa-1.AC1/AC2. Its organic
     proof is the acceptance: the 2026-10-05 09:00 ET sweep, page day 10-05, no account yet (CTO ruling 2).
5. **The vehicle** (terminal machine, CLOUD working tree), 08:03 ET 2026-10-05, runs the round-7 Bloomberg code.
   - nm-2 adds LONG_COMP_NAME to the reference request, written to the new G4 column `security_name`.
   - The past-date historical request excludes the field, so no row demotes to `pull`.
   - **Before 2026-10-05 07:00 ET the issuer proves the field live** on CUSIP-keyed securities with one read-only reference
     request, under `integrations/bloomberg/READ_HERE.md`'s budgeted sign-in. On a field error, the issuer reverts nm-2's
     `enrichment_bloomberg.py` in CLOUD before 08:03 ET.

## THE SERVED DELTA, MEASURED (2026-10-02 page, 23:3x-23:5xZ)

How it was measured:
- `r6_publish.py` overlay publishes, at the pin, with S3 reads and local writes, no Lambda and no vendor;
- the pin page was compared with the SERVED page (rv-publish-1002r6) by `C:/tmp/r7measure/r7_page.py` ->
  `page_compare_pin.json`;
- an overlay at CLOUD 130c3be101 (chains 2-4 only) gave the same bytes: chain 1 does not touch the render.

| page | served (rv-publish-1002r6) | round-7 pin |
|---|---|---|
| status / funds updated / trades | published, 13 of 13, 213 | published, 13 of 13, 213 |
| AI cards with an account (regression guard) | 12 | 12 |
| bytes (gateway cap 2,097,152) | 1,833,385 | 1,886,555 (+2.9%; 10.0% headroom) |
| one-window trend lines reading "Bet/Tilt, 1 trade" / "Single trade" (rd-1 D12) | 58 / 0 | 0 / 58 |
| bare `fear_greed` in visible text (U09) | 4 | 0 |
| `UNRESOLVED` in visible text (U13) | 94 | 0 |
| snake_case tokens in visible text | 1,519 | 795 |
| case-only name clashes across table cells (U14) | 17 | 2 (Cash/cash; Spotify Technology SA/Sa) |
| `data-unclassified-share` footnotes (U16) | 25 | 38 (one more per fund's trend) |

**Per-fund feature decreases (16 features x 13 funds): one, and it is not a loss.**
- PCLG's census reason groups go from 6 to 2. The census is one page section; the per-fund attribution follows the panel
  split.
- Page-wide, the census reads:
  - holdings missing: 4 -> **0** (BIDD, CGIC, IDVZ, SCHY reports inside the header's allowance now read covered: cs-1);
  - sector missing: 185 -> **150** (cg-1);
  - prices missing: 42 -> **44**. That +2 is measured; its cause is not shown and is inferred to be cg-1's alignment of the
    census to the rankings' window.

**Raw `XX Equity` tickers in visible text rise from 1,739 to 2,485, and this is not a regression.**
- 627 are the same identifier cells re-wrapped in a titled span (U13).
- 1,215 are holdings-table Security cells that were EMPTY on the served page: the U14 name-map shadow left them blank. They
  now show the page's one name for the security, which for a Bloomberg-sourced position is still its ticker.
- Readable names for those positions arrive with the 2026-10-05 vehicle run:
  - round 6's `get(id(), name())`;
  - nm-2's LONG_COMP_NAME through G4 `security_name`.

Left for J1 (the CVO's judgment):
- 795 snake_case tokens remain. They are cited table names (market_context, holding_contribution, trade_schedule,
  buying_trend) and guardrail and policy codes (collector_bloomberg, constituents_issuer_fill, grounding_check, ...).
- The cut left the status section's Source policy column and the cited-row table names out of rd-1.

The real act writes:
- act 3: `gold/{holding_contribution,buying_trend,input_census}/date=2026-10-02/` (+1 object each);
  `platinum/page/date=2026-10-02/{index.html,manifest.json}`, with the prior page kept under `revisions/<ts>/`; and
  `state/publish_page/date=2026-10-02/rv-publish-1002r7.json`;
- act 4: nothing.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| P1 | five Lambdas' code | round 6's set (eb6e9f04ff) | the 75ad1e4d2e set | re-apply eb6e9f04ff's build: a saved plan from a detached worktree at eb6e9f04ff after `rivalfunds_package.py` |
| P2 | sweep schedule input | `{date, mode, sink}` | + `run_path: "scheduled"` | re-apply eb6e9f04ff's generated.auto.tfvars.json (same plan as P1) |
| P3 | gold A1 tables + census, date=2026-10-02 | rv-publish-1002r6's objects | + one new object each (newest wins) | the prior objects stay; removing the new ones is an S3 delete (human-confirmed) |
| P4 | platinum page 2026-10-02 | rv-publish-1002r6 | republished ONCE, batch rv-publish-1002r7 | the prior page is kept under `revisions/<ts>/`; re-put it |
| P5 | vehicle Bloomberg request + G4 (from 2026-10-05 08:03 ET) | 10 market fields | + LONG_COMP_NAME -> G4 `security_name` | revert `enrichment_bloomberg.py` in CLOUD before 08:03 ET |

## GATES (before act 2)

1. Nothing is in flight on any rivalfunds Lambda (10 minutes of logs).
2. The live CodeSha256 values equal round 6's set (read at 23:5xZ: they do).
3. The saved plan reads 0/6/0 with exactly the hunks above.

## EXPECTED OUTCOME, BOTH BRANCHES

**Applied:** the five live CodeSha256 values equal the plan's hashes:
- daily vK1xwhs0;
- fetch DOQCSAX9;
- canonical LOORbFv0;
- silver fTe3LTYg;
- publish n0h0/K7d.

The schedule input reads `run_path: "scheduled"`. Act 3 publishes the page in the table above, and its manifest records no
`research_hypotheses_run`: no `ai_run` came with the event, and no attempt record exists. Act 4 reads SKIPPED_EXISTS /
"scheduled" and writes nothing.

From 2026-10-05:
- the 09:00 ET sweep stamps "scheduled";
- it continues any open G1 cursor within 10 trading days;
- it runs ONE OpenAI account chain for page day 10-05 (VEW-2) under a 600 s deadline;
- it republishes 10-05 under an `ai-` batch.

That is the acceptance. A FAILED account is shown, never re-rolled.

**Not applied** (any gate fails): the served stack stays at eb6e9f04ff and nothing is republished. The CLOUD working tree
still carries nm-2's request change, so the 2026-10-05 vehicle run would write G4 `security_name` for the round-6 readers.
Therefore, if the Lambdas are not at the pin by 2026-10-05 06:00 ET, the issuer reverts `enrichment_bloomberg.py` in CLOUD.
**P5 depends on P1.**
