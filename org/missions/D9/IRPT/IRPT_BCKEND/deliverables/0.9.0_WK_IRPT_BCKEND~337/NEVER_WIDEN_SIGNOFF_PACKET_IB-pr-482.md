# Never-widen sign-off packet -- IB-pr-482: irpt-performance-adapter rebuilt from one pin so the claim follows the excluded day's status (C-CHAINCLAIM)

Prepared by 0.9.0_WK_IRPT_BCKEND~337 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO-IB-pr-482 (CTO msg 6517, PRD ADDENDUM v0.51 section 2 item 2; contract C-CHAINCLAIM, ADDENDUM v0.48 as amended by v0.49 section 1). **Nothing here was uploaded, applied or deployed**: BUILD_ONLY from a committed tree, offline replays on SYNTHETIC frames, AWS reads only (the live zip through `get-function`, and S3 list/get of the served holdings gold up to the cap day 2026-10-08). No Lambda was invoked, nobody signed in, no vendor was called. No client data is in this packet or its files: counts, sha256 and reason codes only.

**READ THIS FIRST.**

1. **The served change, in words.** The holdings-basis reader (`performance/holdings_gold.py`, merged at `6a875f0dfd` by TO-IB-pr-476) now sets `value_facts.claim` by the STATUS of the day left out of the chain, wherever the day sits in the window. `NO-PRIOR-HOLDINGS`, and `NON-POSITIVE-BASE` on a day whose prior day held no position row (`held_count` 0), are days with no base: a figure chained across them keeps `measured`. Every other non-OK day (`ALL-HOLDINGS-EXCLUDED`, `IMPLAUSIBLE-RETURN`, `FOLLOWS-DISCONTINUITY`, a `NON-POSITIVE-BASE` day whose prior day held a position row or whose count the gold does not carry, and any status the rule does not name) leaves a return out, and the claim reads `inferred`. A missing trading day still reads `inferred`, as before.
2. **Two integers are added beside `days_linked`** in `report.optional_facts.value_facts`: `days_without_base` and `days_with_return_left_out`; they sum to `days_excluded` on every account read (30843 of 30843 figures in the eight cells). The contract admits them (value_facts is an object or null with open members).
3. **The figures do not move.** The eight cells below were read with the live reader and the reader as built over the same cached partitions: 30843 figures compared, every cell's figure hash equal before and after (`figures_unchanged` = true). Only the claim, and the two new integers, change on the wire.
4. **PARTIAL stays.** All three absences (accrual basis, fees and income, money-weighted return) hold on every holdings-basis answer, so `entry.py` keeps choosing PARTIAL from the absences list alone; no byte of `entry.py` changes. The claim and the two integers, not the state, tell a window with a left-out return from one without.
5. **One member changes.** Built against live: 71 members each, **1 member differs: `holdings_gold.py`**; no member is only in one zip; the changed member's built sha256 equals the repo blob at the pin.
6. **The source map is NOT edited** (outside this order's grant). The zip is built from `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~337/candidate_source_map_482.json` (a map holding only this function, every other key verbatim, ONLY the `holdings_gold.py` pin moved to the pin below) via `BAU_SOURCE_MAP_OVERRIDE`. The apply order must land that one re-pin into `infra/aws/lambda/ci/lambda-source-map.json` first, or the real-map build reproduces the live bytes and its sha256 will differ from the one signed (row `IRPT_BCKEND-D2-W337-S2`, ARMED, disarm owner `2.0.0_SA_COO~P2`).

## Base, pin and the two zips

| item | value |
|---|---|
| base_commit | `05219b844491b6c3c9309b6b3747e54edb823299` |
| pin_commit (the tree built from, carries `6a875f0dfd`) | `05219b844491b6c3c9309b6b3747e54edb823299` |
| function | `irpt-performance-adapter` (the only function whose `staged_from` lists `holdings_gold.py`) |
| built sha256 (CodeSha256 form) | `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=` (hex `69b7a9e21ed19e0312f49a2641476470e4f7119f96f79dce77178ad0791dcc5a`, 446422 bytes) |
| live sha256 (CodeSha256 form, `$LATEST`, last modified 2026-10-12T14:11:01Z) | `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=` (hex `90c07cc4223ddfff502d49f3825548b34108458d3b4922c1894e659fc889c147`, 445757 bytes; the downloaded `Code.Location` zip hashes to it) |
| built twice, byte-identical | YES (second build hex `69b7a9e21ed19e0312f49a2641476470e4f7119f96f79dce77178ad0791dcc5a`) |
| real `lambda-source-map.json` sha256 before / after the builds | `cecf1e8ff82415e3e4798f1c9f3765cf0af7be8d0823ea1cd6bcdd218a60fe94` / `cecf1e8ff82415e3e4798f1c9f3765cf0af7be8d0823ea1cd6bcdd218a60fe94` (byte-identical) |
| changed members vs live | 1 of 71: `holdings_gold.py` |

| changed member | built member sha256 | repo blob sha256 at the pin | live member sha256 |
|---|---|---|---|
| `holdings_gold.py` | `5be3ce00941215c64f96bf03780e9760dee5ff843879e53e4e3b69e49f10580a` | `5be3ce00941215c64f96bf03780e9760dee5ff843879e53e4e3b69e49f10580a` | `d41e861212a7c1a5bdea2529b774651c0fc258ad555bf5063c816677befe216c` |

Signature instrument `deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py` (both limbs, run at its own path on each zip's own bytes):
- built: `signature_closure calls=186 checked=186 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=114 attr_mismatched=0`
- live (the negative-control context): `signature_closure calls=186 checked=186 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=114 attr_mismatched=0`
Both zips read 0 signature and 0 attribute mismatches, which is expected: only one non-signature member differs, and no call into it changed shape. The tests of the pin: `test_chain_claim.py` with `test_partial_only_when_absence_holds.py` 23 passed.

## The MOVES, with the REACH beside them (per firm and window; cap day 2026-10-08; counts taken at the pin `05219b8444`)

The REACH is the accounts the new rule applies to (`days_with_return_left_out` above 0). The MOVES are the accounts whose served claim actually goes `measured` to `inferred` (measured with the live reader, inferred with the reader as built). The difference is accounts already `inferred` at base for a missing trading day (row `IRPT_BCKEND-D2-W319-S1`); for those the figure and the claim read the same before and after. **The pair is signed against the MOVES (column 4), not the reach.**

| firm entry | window | REACH (rule applies) | **MOVES (measured -> inferred)** | already inferred at base | accounts with a figure | partitions read |
|---|---|---|---|---|---|---|
| 49F entry | SI | 23 | **23** | 0 | 6896 | 566 |
| 49F entry | YTD | 19 | **19** | 0 | 6832 | 566 |
| 49F entry | QTD | 2 | **2** | 0 | 6722 | 566 |
| 49F entry | 1Y | 20 | **20** | 0 | 6840 | 566 |
| Orion (Inflection) entry | SI | 894 | **750** | 144 | 926 | 1619 |
| Orion (Inflection) entry | YTD | 200 | **76** | 124 | 906 | 1619 |
| Orion (Inflection) entry | QTD | 7 | **7** | 0 | 805 | 1619 |
| Orion (Inflection) entry | 1Y | 240 | **106** | 134 | 916 | 1619 |

These equal the CTO's numbers (v0.49 reach; v0.51 moves: 49F 23, 19, 2, 20; orion 750, 76, 7, 106) in all 16 cells. Partitions: 49F listed 567, 566 used (<= 2026-10-08); orion listed 1620, 1619 used. Accounts the reader refuses are the same before and after in every cell (`refusals_differ` 0). No `inferred` -> `measured` move occurs (0). The claim counts per cell, base then after, are in `IB167-2_release_counts.json` (`claim_at_base`, `claim_after`).

## Branch A -- land it (digest-gated, never a mint)

1. Open the NEVER-2 ledger entry first (`.tools/deploy_ledger.py open ...`) and commit its `.open_deploys` sentinel at once; it names EVERY task family that pulls this artifact (`irpt-performance-adapter` only, one `describe-task-definition`-style sweep of `staged_from` users: no other function lists `holdings_gold.py`).
2. **START READ:** `get-function-configuration` CodeSha256 must equal the live value above (`kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=`); anything else: STOP, no apply.
3. Land the single re-pin (`holdings_gold.py` -> `05219b844491b6c3c9309b6b3747e54edb823299`, sha256 `5be3ce00941215c64f96bf03780e9760dee5ff843879e53e4e3b69e49f10580a`) into `infra/aws/lambda/ci/lambda-source-map.json` (the candidate map's `_repins_IB_pr_482` row is the exact edit), from a clean tree at the pin or a descendant whose `performance/` tree is unchanged.
4. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter` and compare the printed sha256 to `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=`. **ABORT on any difference: never upload a different digest than the one signed, never mint a new artifact in place of it.**
5. Then the same without BUILD_ONLY (upload), then the module's Terraform path (`infra/aws/terraform/investor-reporting/performance`, `s3_object_version` + `source_code_hash` only, plan to a planfile showing 1 change and 0 to destroy, apply with `bash .tools/safe-apply.sh`). No IAM, route, schedule, layer, environment or table change.
6. **After:** live CodeSha256 equals `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=`; re-plan shows 0 changes; the census for the function shows `changed_members=0`; the direct-invoke proof below; close the ledger entry.

## Branch B -- restore the live version

- **What is restored:** the live code, CodeSha256 `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=` (hex `90c07cc4223ddfff502d49f3825548b34108458d3b4922c1894e659fc889c147`), last modified 2026-10-12T14:11:01Z. It equals the `artifact_sha256` of the source map at HEAD.
- **Named and re-read at apply:** the S3 object version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-performance-adapter.zip` whose `content-sha256` metadata equals that CodeSha256 is NOT read here (an S3 version listing of the artifact bucket is outside this order's allowed AWS calls). The apply worker names it at step 1 of Branch A, BEFORE any upload, writes it into the ledger entry, and re-reads at restore time that `get-function-configuration` CodeSha256 is still the built value and that version is still addressable.
- **Rollback per key:** one key, `investor-reporting/irpt-performance-adapter.zip`: redeploy that S3 version through the same Terraform path (`s3_object_version` + `source_code_hash`), never a console edit and never `aws lambda update-function-code`; then CodeSha256 equals the live value above and the re-plan is 0 changes. Nothing else is moved by the apply, so nothing else is restored: no table, route, IAM or layer.
- **What the restore does to served values:** the claim on the MOVES accounts reads `measured` again; the figures never moved. **Stored revisions stay as stored**: a retained report's revision is the sha256 of the whole record (`repository.py:202`), so a record written with the new claim is a new revision and overwrites nothing; the restore removes none and needs none removed.
- **Trigger:** a 5xx or `TypeError` in the function's log group after the apply, a direct-invoke arm below that fails, or a figure that differs from its before-read: restore at once.

## The ADDENDUM 18 red list

`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the pin: **2 failed, 203 passed in 5.47s**. The FAILED node ids (2):
- `_contracts/tests/test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve`
- `_contracts/tests/test_seam_paired.py::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]`

Same two as `0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json` (2 failed at `361c44fa9d`). Their targets are the response contract and fixture of `analysis-request-original`. This cell's changed member is `infra/aws/lambda/investor-reporting/performance/holdings_gold.py`; this cell changed 10 paths vs its base, all under its deliverables folder. Intersection with the red tests' target surface (`infra/aws/lambda/investor-reporting/_contracts/`, `docs/contracts/investor-reporting/`) and with any path naming a red operation: **0 changed, 0 member, 0 naming** -- STOP = **no**. The packet does not cite "suite green".

## The replay arms (offline, SYNTHETIC; the four frames of `performance/tests/test_chain_claim.py`; built zip's `holdings_gold.py` against the live zip's, each imported from its extracted zip)

| arm | built claim | live claim | built days_without_base / days_with_return_left_out | figure built = live | verdict |
|---|---|---|---|---|---|
| no-base days only (NO-PRIOR-HOLDINGS and NON-POSITIVE-BASE with held_count 0) | measured | measured | 2 / 0 | yes (0.010040080080031988) | expected-diff |
| ALL-HOLDINGS-EXCLUDED | inferred | measured | 0 / 1 | yes (0.012060160240191964) | expected-diff |
| NON-POSITIVE-BASE with a prior-day position row (held_count 2) | inferred | measured | 0 / 1 | yes (0.012060160240191964) | expected-diff |
| an unnamed status (A-STATUS-THE-PRODUCER-NEVER-WROTE) | inferred | measured | 0 / 1 | yes (0.012060160240191964) | expected-diff |

The figure of every arm is `identical`; the claim arms 2 to 4 are `expected-diff` (live `measured`, built `inferred`); arm 1 keeps `measured` and differs only by the two new integers on built. Instrument: `deliverables/0.9.0_WK_IRPT_BCKEND~337/replay_arms_482.py`.

## The consumers of the claim and the state, each with one read-through (21)

The 11 backend consumers of `IB166-1_reader_record.json`, the backend and portal readers of `IB166-4_value_facts_readers.json`, and what the census here added (the narrative's own claim strings, the 49F gold's own `days_linked`, the portal tile and the holdings snapshot's claim). Cites resolve at the pin; the full text is in `IB167-2_release_counts.json`.

| cite | reads | read-through |
|---|---|---|
| `infra/aws/lambda/investor-reporting/performance/holdings_gold.py:296-300` | WRITES value_facts: start_value, end_value, days_linked, days_observed, days_excluded and the two new integers days_without_base and days_with_return_left_out (the two sum to days_excluded) | infra/aws/lambda/investor-reporting/performance/tests/test_chain_claim.py:100: the no-base arm reads (2, 0) and the left-out arms read (0, 1); test_chain_claim.py with test_partial_only_when_absence_holds.py run at the pin: 23 passed |
| `infra/aws/lambda/investor-reporting/performance/holdings_gold.py:313-318` | DECIDES the claim from the missing-trading-day list and days_with_return_left_out (C-CHAINCLAIM) and writes it to value_facts.claim | infra/aws/lambda/investor-reporting/performance/tests/test_chain_claim.py:109 (ALL-HOLDINGS-EXCLUDED reads inferred, the figure unchanged); and the 8-cell run over 30843 figures, figures_unchanged true |
| `infra/aws/lambda/investor-reporting/performance/holdings_gold.py:367` | RETURNS the same claim as the outcome's claim key | infra/aws/lambda/investor-reporting/performance/tests/test_holdings_gold_calendar_gap.py:92 (out['claim'] reads inferred on a missing day); test_holdings_gold_calendar_gap.py at the pin: 6 passed, 1 failed (the fallback-calendar test, which fails on the absent pandas_market_calendars and reads no claim) |
| `infra/aws/lambda/investor-reporting/performance/normalize.py:327` | copies the node's value_facts, claim and both counts included, into report.optional_facts.value_facts; sets supported from its presence (no member read) | infra/aws/lambda/investor-reporting/performance/tests/test_holdings_gold.py:402 (the _value_facts reader over the answer); test_holdings_gold.py at the pin: 23 passed |
| `infra/aws/lambda/investor-reporting/performance/orion_selected.py:177-178` | truthy test, then copies value_facts with period_start/period_end replaced; reads no claim or count (the copy keeps the claim and both new members) | code read; test_performance_adapters.py at the pin: 28 passed |
| `infra/aws/lambda/investor-reporting/performance/bd_adapter.py:192` | a writer's own guard on the Black Diamond path; writes value_facts without a claim and without the two integers, so its answers are unchanged | infra/aws/lambda/investor-reporting/performance/tests/test_performance_adapters.py:219 (value_facts from the vendor's end value); test_performance_adapters.py at the pin: 28 passed |
| `infra/aws/lambda/investor-reporting/performance/entry.py:279-286` | reads the absences and refusals lists only (never the claim or the counts) to choose PARTIAL or READY; this is why PARTIAL stays | infra/aws/lambda/investor-reporting/performance/tests/test_partial_only_when_absence_holds.py:68 (PARTIAL with the reader's real absences, READY with none); run at the pin: 23 passed |
| `infra/aws/lambda/investor-reporting/performance/entry.py:301` | returns the report with optional_facts.value_facts (claim and both counts) to the wire | infra/aws/lambda/investor-reporting/performance/tests/test_entry_selection.py:89 (PerformanceReport schema validation of the wire document); test_entry_selection.py at the pin: 39 passed |
| `infra/aws/lambda/investor-reporting/performance/retained.py:318` | persists the report; the calculation revision comes from lineage.source_revision, not from the claim | infra/aws/lambda/investor-reporting/performance/tests/test_retained_performance.py:300; test_retained_performance.py at the pin: 21 passed |
| `infra/aws/lambda/investor-reporting/reports/repository.py:202` | the stored revision is the sha256 of the whole record, report body included, so a changed claim is a new revision and never overwrites a stored one | code read only (no run) |
| `infra/aws/lambda/investor-reporting/_contracts/PerformanceReport.schema.json:328-340` | value_facts is an object or null and its other members stay open, so the claim and the two integers are admitted | infra/aws/lambda/investor-reporting/performance/tests/test_chain_claim.py:70 (calculate runs normalize.validate_report on every answer); run at the pin |
| `infra/aws/lambda/investor-reporting/ops/status.py:225` | treats PARTIAL as an answer-bearing state (business_date required); unchanged, PARTIAL stays | infra/aws/lambda/investor-reporting/ops/tests/test_status.py:102; ops/tests/test_status.py at the pin with PYTHONPATH=ycharts/generate: 23 passed (14 fail without that path on ModuleNotFoundError submission, a test-path matter) |
| `infra/aws/lambda/investor-reporting/_authz/served.py:169` | lists PARTIAL among the answer-bearing states; unchanged | infra/aws/lambda/investor-reporting/performance/tests/test_entry_selection.py:243 (state PARTIAL on the entry's answer); test_entry_selection.py at the pin: 39 passed |
| `infra/aws/lambda/investor-reporting/narrative/fixtures/performance_report_inf.json:442` | a recorded report fixture carrying a value_facts object without claim or counts; no narrative code reads value_facts | code read only (0 of the narrative package's python files name value_facts, row-331 census) |
| `infra/aws/lambda/investor-reporting/narrative/evidence.py:66` | the narrative packet writes its OWN claim strings on its own evidence rows; it reads no claim from a performance answer | code read only |
| `infra/aws/lambda/investor-reporting/_contracts/fixtures/PerformanceReport.valid.json:68` | contract fixture carrying value_facts null; the absent path | the _contracts suite at the pin: 203 passed, 2 failed (the two red-list tests of ADDENDUM 18), unchanged |
| `data/assets/scripts/gold/runners_49f/parity_period_returns.py:377` | found by census: the 49F gold's own days_linked column; it is not the reader's value_facts and carries no claim | code read only (not a consumer of the claim) |
| `portal/src/pages/InvestorReporting/contracts/adapt.ts:797-799` | PORTAL: reads value_facts.period_start, period_end and currency only to decide hasValues; reads neither claim, days_without_base nor days_with_return_left_out | code read; native Grep for the word claim over contracts/, render/performance/, tabs/reporting/, state/ of the portal tree in this worktree finds no read of a performance claim (row-334 record IB166-4: 39 of 1395 portal files name value_facts or a value member) |
| `portal/src/pages/InvestorReporting/contracts/wire/PerformanceReport.ts:60` | PORTAL wire type: value_facts is Readonly<Record<string, unknown>> or null, so the claim and the two integers pass as carried data | code read only (a bun run is the portal cell's, not this build's) |
| `portal/src/pages/InvestorReporting/tabs/reporting/PerformanceHeadline.tsx:110-111` | PORTAL tile renders beginningValue and endingValue (from start_value/end_value via the adapter); it renders no claim label, so the claim change shows no new text | code read only |
| `portal/src/pages/InvestorReporting/contracts/wire/HoldingsSnapshot.ts:73` | PORTAL: the one claim member in the portal's wire types belongs to the HOLDINGS snapshot, not to the performance report's value_facts | code read only |

No consumer reads the claim to change a decision: `entry.py` reads the absences only, the portal reads value_facts only for the window and the two value members, and every other path carries the claim as data.

## Direct-invoke proof, to run AFTER the apply (by `0.7.0_AE_CloudOps~IB2`, not by this worker)

The instrument is the one already signed for this function family: a direct `aws lambda invoke` of the DEPLOYED function with an API-shaped event for an Opal principal, using the function's own role (CTO ADDENDUM 3 path 1, as TO-IB-pr-368 used it), no new grant, a READ operation only. The same four arms:
1. an account whose only excluded days are no-base days (`NO-PRIOR-HOLDINGS` or `NON-POSITIVE-BASE` with `held_count` 0): claim `measured`, `days_without_base` > 0, `days_with_return_left_out` 0;
2. an account with an `ALL-HOLDINGS-EXCLUDED` day: claim `inferred`, `days_with_return_left_out` > 0;
3. an account with a `NON-POSITIVE-BASE` day whose prior day held a position row: claim `inferred`;
4. an unnamed status: claim `inferred`. The served gold may carry no account with an unnamed status; if none, arm 4 stays the offline replay above and the packet reads it UNEXERCISED against the served gold (ABSENT != EXERCISED-AGAINST).
Each arm is read BEFORE the apply (same shape, persisting nothing) and AFTER: the **figure of each is unchanged from before** (equal to the last digit; record the sha256 of the figure, not the figure), and the claim moves as stated. Account ids stay in the invoker's scratch and out of the repo. The apply order must name which read operation the invoke uses and whether it persists: the fresh path persists a retained report (`retained.py:318`), a persisted record carrying the new claim is a new revision and overwrites nothing, and a persist is a write the signer must see named, not assumed absent.

## Blast radius

- **Function:** `irpt-performance-adapter` only; no other function, layer, IAM, route, schedule, environment or table changes. **Member:** `holdings_gold.py` only (1 of 71).
- **Served effect:** on the MOVES accounts the claim reads `inferred` where it read `measured`; the two integers appear on every holdings-basis answer; PARTIAL stays; every figure is byte-for-byte the same number.
- **Never-widen:** this MOVES a served value (the claim), so it ships only under the pair below. It widens nothing: no account is added to any set, no firm gains a read, no state changes.

## The pair

Both halves sign the same facts: built `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=`, live `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=`, one changed member `holdings_gold.py`, and the MOVES table above (the table the pair is signed against). A half that signs a different sha256 or different moves counts is void.

- **COO half -- `2.0.0_SA_COO~P2`:** signs that the moves counts equal the CTO's v0.51 item 2 and that the apply order will carry the Branch A digest gate and the Branch B restore named above. Signed: ______________________  at: ____________
- **CTO half -- `1.0.0_SA_CTO~DELL2`:** signs the served change in words, the red list reading, and the choice of Branch A. Signed: ______________________  at: ____________

## Rows

`IRPT_BCKEND-D2-W337-S1` (the order names a READ file beside the reader record; the folder holds none; INERT), `IRPT_BCKEND-D2-W337-S2` (the source map's `holdings_gold.py` pin is stale until the apply order lands the re-pin; ARMED, disarm owner `2.0.0_SA_COO~P2`).

Files beside this packet: `IB167-2_release_census.json`, `IB167-2_release_counts.json`, `IB167-2_red_list.json`, `candidate_source_map_482.json`, and the writers (`make_candidate_map_482.py`, `replay_arms_482.py`, `make_records_482.py`, `make_packet_482.py`).
