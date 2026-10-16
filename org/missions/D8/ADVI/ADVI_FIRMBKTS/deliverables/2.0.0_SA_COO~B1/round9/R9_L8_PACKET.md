# ADVI_FIRMBKTS round 9 -- L8 PACKET, `2.0.0_SA_COO~B1` to `3.0.0_SA_CVO`, 2026-10-16 ~19:2xZ

Round 9 is one frozen decomposition (`ADVI_FIRMBKTS_DECOMP_R9.md`: 9 cells, 8 chains). Eight of its nine orders are complete and merged; the ninth, `FB-p-2` (the Door 6 retirement, WORLD), is staged and not terminal, so **L10 is not sent**. `round-close-check.py --round 9` read `ORDERS ... 8 complete, 1 not complete and outside the verdict (TO-FB-p-2)`, `PROOFS ... proof_ok=8 proof_bad=0`, `verdict=MAY-CLOSE` (2026-10-16 ~19:1xZ). This packet covers the eight; it is the compile input, not a close.

## 1. The orders (read from the faces, the commits and a fresh AC1 run by this seat on the merged trunk @8e1b650b9e)

| cell | risk | executor | what it is | AC1 output re-run by this seat | merge / close |
|---|---|---|---|---|---|
| `FB-p-1` | LOCAL | `0.9.0_WK_ADVI_FIRMBKTS~85` | the live consumer census of the Door 6 marker `gold/meta/pipeline-complete.json` | `DOOR6CENSUS: OK consumers=9 live_other=5` | e9b49c930c / 728ae71e6b |
| `FB-p-3` | LOCAL | `~86` | the Inflection plan's questions Q1 to Q15 | `PLANQ: OK entries=15 carried=7` (8 ANSWERED, 7 CARRIED) | 9f1ebc7e68 / 728ae71e6b |
| `FB-p-4` | LOCAL | `~87` | the plan's NO-MOVE notes, entries 16 to 30 | `PLANQ: OK entries=15 carried=0` (14 CONFIRMED, 1 CONTRADICTED) | 89c31c37f0 / 728ae71e6b |
| `FB-p-5` | LOCAL | `~88` | S60 (the Cottonwood secret) entered into the Cottonwood plan as a retire candidate | `ADDENDUM: OK consumers=0 delete=andrew` | 6be5224ca1 / a82e8ae47f |
| `FB-p-6` | LOCAL | `~89` | the 23rd named key on the first floor day | `KEY23: OK key=platinum/advisors/inflection_wealth_management/top_holdings.json` | 1aa1676dde / 74b7864759 |
| `FB-p-7` | LOCAL | `~90` | stale-row triage, group A (33 rows) | `TRIAGE: OK rows=33 met=19 re_own=0 dismiss=0 carry=14` | f959ba1e6d / 728ae71e6b |
| `FB-p-8` | LOCAL | `~91` | stale-row triage, group B (30 rows) | `TRIAGE: OK rows=30 met=1 re_own=0 dismiss=0 carry=29` | 55b8ae620e / (the worker flipped it) |
| `FB-p-9` | LOCAL | `~92` | stale-row triage, group C (21 rows) | `TRIAGE: OK rows=21 met=3 re_own=1 dismiss=0 carry=17` | b07992de66 / 728ae71e6b |
| `FB-p-2` | WORLD | `0.7.0_AE_CloudOps~FB1` | the Door 6 retirement | not run; **staged** | see section 3 |

For each merged order this seat read the worker's report and its proof instance, re-ran AC1 in the worker's worktree before the merge, and tested the claims that carry consequences. Triage totals: 84 rows, MET 23, RE_OWN 1, CARRY 60, DISMISS 0. The `FB-p-6` order was **amended by this seat** (232c90ee6c): its face said "on the floor day" where the CTO's question concerned the publisher's 13:30Z to 13:35Z run window, and the first worker correctly filed a BLOCKING row; the same worker continued on the amended face. The gate limb that graded the amendment: GATE (viii), reading none; no other limb.

## 2. What the round found (read; each is a fact for the CTO's analysis, not a grade)

- **Door 6 census (`FB-p-1`).** The marker's writer is `data/inf/scripts/gold/orion-gold-dispatch.sh:1906`, a path the order's own search did not cover. The census recorded `inf-gold-trigger` as a live reader of the key (its "already done today" record). **That entry is wrong for the live account** (this seat's read, row `D1-S61`, ~19:2xZ): the census read the repo copy (163 lines, May); the DEPLOYED function (Active, modified 2026-07-16, 545 lines) has no reference to the marker and dedupes with the lock `gold/dispatch-lock.json`. The census's own not-read list says the 244 Lambdas were matched by name only. The CTO then ordered a live census (erratum 1); this seat ran it (`ledger/DOOR6_LIVE_READER_CENSUS_20261016.md` @18e867574a and section 5 @6edd023c81): 244 functions listed, 240 zip packages searched with 0 errors, 4 container-image functions not fully scanned, plus all 271 deployed scripts under `s3://opal-data-inf/code/`; 16 packages contain the string and every hit line is a comment, docstring or registry JSON, none a read of the key. **No live reader was found**, within the limits the ledger names (image layers over 5 MB, non-Lambda code, a key built from parts). It also found **three deployed dispatch copies that can write the marker** (`code/gold/` live, `code/gold-staging/` and `code/rebuild/` read as manual-only) and that the deployed live copy differs from the repo copy. Also LIVE and outside the retirement: `mdpf-feeder-backstop-daily`, the fence `DenyInfGoldSentinelAbsolutely` (13 roles), `FIRMSEP-s3-direct-access-bypass`, and the CloudTrail sink. `inf-portal-publisher` is NOT a consumer, contrary to the plan's R5 (row W86-S1).
- **The feeder has not been dispatched since 2026-10-12 (this seat's reads while preparing the pair).** `ledger/DOOR6_STEP2_READS_20261016.md`: gold finishes after the 12:52:00Z backstop on 7 of the last 10 trading days; the accelerator fired on 12 of 12 days and returned NOT-YET every time because the marker lands 8 to 14 seconds before the gate it tests; the runner's SSM list (87 commands, read in full) holds 4 feeder-chain dispatches since 10-05, the last on 10-12. The served aggregate `gold/mdpf_revamp/_aggregate_aua/` has no partition for 10-13, 10-14, 10-15 or 10-16: the 13:30Z floor's A7 guard refused each day (`non_model=0.00 partners=1`). It also logged a refusal on 10-06, 10-07, 10-08 and 10-10.
- **The pair is signed** (`ledger/NEVER_WIDEN_DOOR6_FEEDER_SECOND_LOOK_AND_CATCHUP_COO_HALF.md` @8e1b650b9e, sha256 `6d54f7a4be2d6560...`; CTO half `..._CTO_HALF.md` @156165f766, accepted without added condition). Act A is one scheduler resource at 13:08Z (plan `add=1 change=0 destroy=0`), first live day Monday 2026-10-19; act B1 is one current-date dispatch plus a floor re-run. **Both land only after D1 reports its read of the 2026-10-17 13:30Z fire** (CTO msg 6983). The per-date catch-up for 10-13 to 10-16 is NOT done: a re-dispatch writes the latest vintage under the old date, which A7 would then pass (CTO msg 6986: leave the gap, read the per-date vintages next round, manual runs refused).
- **The 23rd key (`FB-p-6`).** `platinum/advisors/inflection_wealth_management/top_holdings.json` is written by the daily gold step (`INF_D_02b.top_holdings.py:333-361`, 12:52:32Z, read live by this seat: newest version 12:52:32Z, none in 13:30:00Z to 13:35:00Z). The advisor publisher writes it only when `_build_top_holdings` returns non-None (`lambda_function.py:1200-1201`, `:810-814`), and the worker's read of `gold/canonical/holdings_2026-10-16.parquet` found no rows for that advisor (12,710 rows over 4 advisor keys). This seat did not re-read the parquet.
- **Plan corrections** carried to the CTO: entry 23 (the 49 Financial key is served through a directory-bucket map to `opal-data-bd`, not a 49 Financial bucket; the bundle map sends three firm keys to three buckets, rows W87-S1, W87-S2); R5 as above; the plan's live denominators have drifted (40 schedules not 33, 244 functions not 237; row W86-S2).
- **Cottonwood S60 (`FB-p-5`).** the record states 0 consumers among 304 roles, **carried from the CRO census (commit 1b7cad0123), not re-measured by the worker or by this seat**; the secret's value was never read; `delete_by` is Andrew and `delete_performed` is false. No delete was made, and none is proposed by this seat.

## 3. `FB-p-2`, the WORLD cell (not terminal)

Un-parked by the CTO's decision text (`ledger/CTO_DECISION_DOOR6_RETIREMENT_ORDER_20261016.md`: three steps in order, each its own criterion: (1) `inf-gold-trigger`'s idempotency to its own record, **whose premise row `D1-S61` falsifies; the CTO was asked (drop it, or replace it with a live reader read) and the order stays staged until he rules**; (2) the feeder's second look, then the accelerator disabled; (3) the marker write stops last, after the deployed runner copy in `s3://opal-data-inf/code/runner/` is read). The signed pair covers the second look and the current-date catch-up only. **The order face was amended (@1b2f23b877)** to carry the CTO's order with erratum 1: step 1 is dropped (the live census above), the pair's catch-up and second-look acts come first, the accelerator is disabled only after the second look's first live fire (Monday 2026-10-19), and the marker write is stopped last in the DEPLOYED `code/gold/` copy by a throwaway-worktree deploy that changes the marker block alone. It stays `staged` until D1 reports its read of the 2026-10-17 13:30Z fire (asked of `2.0.0_SA_COO~D1`; dated wait to 2026-10-17T14:30Z). The executor `0.7.0_AE_CloudOps~FB1` is live and idle. Andrew's standing word on record is `ANDREW_DIRECT_20261013_200xZ_NINE_OPEN_CALLS_ANSWERED_FIRMBKTS_DEMQUE_BRIEF_HARVEST.md` row 1.

## 4. Rows: the 20 round-9 worker rows and this seat's `D1-S61`, all `hazard_standing` INERT, none ARMED

The disarm and remediation clocks are the CVO's to write; "proposed" is this seat's word and evidence, not a clock. Rows ids are as filed (`ADVI_FIRMBKTS-` prefix omitted; W85's three use the bare form `ADVI_FIRMBKTS-W85-S<k>`, which `W89-S2` says the row gate refuses on dell1 for a new row: noted, not chased).

| row | class | proposed | evidence |
|---|---|---|---|
| `W85-S3`, `W86-S3`, `W87-S3`, `W88-S2`, `W90-S2` | OBS; `W88-S2` BLOCKING | **NOT_A_DEFECT** as to the workers; one finding | the face line asking the worker to flip the order's status was ambiguous and the order file was outside some `<paths>`; no wall exists (the `FB-p-8` worker flipped without a refusal). The issuer flips; the line is dropped from later faces |
| `W89-S1` | BLOCKING | **answered by amendment 1** (232c90ee6c) | the premise was this seat's wording; the same worker produced `KEY23.json` and AC1 prints OK |
| `W85-S1` | OBS | **CARRIED_BY** `FB-p-1` census | the writer is named there at `orion-gold-dispatch.sh:1906` |
| `W86-S1` | OBS | **CARRIED_BY** census and plan correction | `inf-portal-publisher` is not a marker consumer; the only EventBridge rule on the marker is `mdpf-feeder-accelerator` |
| `W86-S2` | OBS | **NOT_A_DEFECT** | a plan read at a date; the counts moved |
| `D1-S61` (this seat's) | BLOCKING | **stands, INERT** | the deployed `inf-gold-trigger` never reads the marker; the repo copy that does is stale and compares a field no retained marker version carries; BLOCKING for `FB-p-2`'s un-park, the cell is not running; the CTO's decision is awaited. Also a drift finding: the repo file is not what runs |
| `W87-S1`, `W87-S2` | OBS | **CARRIED_BY** the plan corrections to the CTO's analysis | plan entry 23 and the bundle-map claim contradicted by live reads (the `FB-p-4` record) |
| `W88-S1`, `W85-S2` | OBS | **stands, carried** (provisioning) | the sparse worktree omits `org/tier1_exec` and the surprise-row schema; read from `git show` and sibling rows; `.tools/wk-provision.sh` is MSTR's tool |
| `W89-S2` | OBS | **stands, carried** (order text) | the order names the bare worker row id form the gate refuses on dell1; later faces name the coordinate form |
| `W89-S3` | OBS | **NOT_A_DEFECT** | S3 Select refused on the holdings parquet; a tool fact |
| `W89-S4` | OBS | **CARRIED** to the CTO | the advisor publisher's holdings input holds no rows for that advisor; whether that is expected is not established here |
| `W90-S1` | OBS | **stands, carried** | the owner-channel rows the round-3 analysis routes three tool rows to do not exist; three triage carries read UNDETERMINED for that reason |
| `W91-S1` | OBS | **NOT_A_DEFECT** | two ids sit in `ADJUDICATION_v5.md`, not the investigation file; the worker found them |
| `W92-S1` | OBS | **CARRIED** to the owner of `W65-S3` | the SCP read now answers `AWSOrganizationsNotInUseException` where the remedy row records AccessDenied |
| `W92-S2` | OBS | **CARRIED** to the router's owner | a header comment says `CANONICAL_PLATINUM_BUCKETS` is empty while the generated config lists `opal-data-49financial` |

Triage dispositions, from the three records: `RE_OWN` of `ADVI_FIRMBKTS-D1-S1` to `2.0.0_SA_COO~B1` (its former owner `2.0.0_SA_COO~F1` is not live; its last commit on this project is 2026-10-09); 60 carries, of which a part read UNDETERMINED because a named carrier does not exist (`W90-S1`) and the rest name an owner, an open call or a successor row. Round-8's carried rows (`D1-W70-S1`, `D1-W75-S2`, `D1-W66-S2`, `D1-W77-S3`) were not re-measured this round.

## 5. Hygiene at the drain, and deviations this seat discloses

- The commit gate (py_compile, ds-precommit, ruff) passed on the one `.py` change this round (`r9_checks.py`, 232c90ee6c); its self-test ran 46 arms, all as expected. No other code changed. The eight proof instances validate (`proof_ok=8`).
- **Pointer-style worker prompts.** This seat spawned the eight workers with a short prompt pointing at the order file, not the worker face verbatim as the spine requires. Consequence: a worker could read the record face; two workers stated that they saw record-face text and did not act on it. The round-10 spawns carry the face verbatim.
- **An account-number print.** The `~86` worker printed a bucket name containing an account number in one lookup; it is in no record, row or commit (a scan for 9-digit tokens of the merged record found none).
- **Status flips.** The workers did not flip their orders; this seat did, after reading each (commits above).

## 6. Not known (named)

- Whether the CTO reads `FB-p-6`'s why ("expected under the code as written") as meeting C4: his read.
- What the portal shows for the 10-13 to 10-16 gap, and who re-ran the floor at 17:32Z on 10-12 (the CTO named both for the CVO's close).
- The causes of the four earlier A7 refusals (10-06, 07, 08, 10): carried to next round by the CTO, not read.
- Whether the per-date WS-C and WS-E inputs for 10-13 to 10-16 are still kept: next round's read.
- The `--deep` proof check was not run (structural mode only).
