# SEAM: cot pipeline bronze -> silver -> gold -> platinum (AUA) -- MACRO
**archetype:** DIAGNOSE
**by:** 0.7.0_AE_CloudOps | **date:** 2026-06-18 | **trigger:** Andrew "cot AUA most-recent data point is 10 days old, check the cloud now" + /seams

## Seam definition
- **Chain:** Black Diamond REST pull -> bronze -> silver -> gold -> platinum/firm served AUA.
- **Expected contract:** daily BD pull refreshes the served firm AUA (platinum/firm/header_metrics.json etc.); each layer triggers the next via an S3 sentinel + EventBridge.
- **Scale:** MACRO -> decomposed into 4 constituent seams below.
- **Ground truth observed:** served AUA frozen at data_as_of 2026-06-09 (= $362,626,488) while wall-clock is 2026-06-18 (9-day freeze).

## Constituent seams + 3-axis verdicts

### Seam 1: BD-REST(session-fetch) -> bronze
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | PASS | cot-bd-session-daily cron(02:00) -> cot-bd-session-trigger Lambda -> SSM opal-cot-bd-session-fetch -> bronze. bronze/2026-06-18/_BRONZE_COMPLETE.json (06-17 22:02, overall=success, 5 tables) -- daily through 06-18. |
| DECLARATIVE | PASS | wired as designed; rules ENABLED; CHAINFIX session-complete pattern correct (EC2 Command Status-change Notification + opal-cot-bd-session-fetch). |
| SEMANTIC | **FAIL** | The unrealized (holdings/AUA-basis) export is INTERNALLY frozen at 06-09: silver-run log 06-18 reads "Data date from Timestamps sheet: 2026-06-09" from UNREALIZED_DAILY_2026-06-18.xlsx -> writes silver/unrealized/2026-06-09.parquet. realized advances to 06-18; unrealized/holdings does NOT. Root (UNVERIFIED which): BD export asOfDate / the qt holdings-snapshot cadence (bbd50b358 "daily holdings snapshot qt1 226355 = AUA source"). |

### Seam 2: bronze -> silver  (cot-bronze-complete -> silver-run)
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | PASS | cot-bronze-complete rule -> trigger Lambda mode=silver-run -> SSM opal-cot-silver-run (06-18 02:02, Status=Success). |
| DECLARATIVE | PASS | manifests update daily; chain mode markers correct. |
| SEMANTIC | PARTIAL/FAIL | realized -> 06-18 (fresh); unrealized -> 06-09 (inherits seam-1 source freeze); transactions -> FROZEN (see seam 3 root). |

### Seam 3: silver -> gold  (silver_complete.json -> gold-run)  *** THE BREAK ***
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | **FAIL (carries nothing)** | silver_complete.json is NEVER written bucket-wide (0 objects). silver-run 06-18 ended: "WARN: silver sentinel NOT emitted -- 1 gated table(s) not processed-this-run within 12h: ['transactions(last_successful_run=None)']". So cot-silver-complete rule (suffix silver_complete.json -> mode=gold-run) matches 0 events -> gold-run NEVER fires -> gold/platinum frozen at 06-09. |
| (sharp test) | rule is CORRECT | aws events test-event-pattern on a synthetic silver_complete.json event = True; target Input = {"mode":"gold-run"}. => the WIRING is complete; the ONLY missing piece is the sentinel EMISSION. Fix = un-freeze the gated table, NOT fix the rule. |
| DECLARATIVE | PARTIAL | ADVI_COTETL.CHAINFIX TO honestly flagged "gold separately blocked" -- so the record wasn't lying. But the served AUA presents as current with NO staleness signal -> anyone reading it believes it's fresh (false). |
| ROOT CAUSE | -- | transactions silver merge-FROZE post-06-09: a duplicate 'Tax Status' xlsx header -> duplicate-label error. transactions silver SUCCEEDED through 06-09 (partitions 03-09..06-09 + cot_transactions.parquet all exist, dated 06-09), then stopped. The fail-closed sentinel gate (864139e7a: this-run-processed) correctly refuses to emit while transactions is stale -> gold starves. |

### Seam 4: gold -> platinum (served AUA JSONs)
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | PASS-when-run | gold->platinum produced all platinum/firm/*.json when gold last ran (06-09). Starved since (seam 3). |
| DECLARATIVE | **FAIL** | firm_id mislabel: platinum/firm/dashboard.json + mix_summary.json + timeseries_overview.json carry firm_id="49financial" (cot data in the cot bucket); only header_metrics.json correctly says "cottonwood". |
| SEMANTIC | **FAIL** | served AUA $362,626,488 is internally consistent across 3 artifacts BUT data_as_of=2026-06-09, 9 days stale, served as current with no freshness guard. mix_summary equity+FI (~$43.9M) does not reconcile to total.aua ($362.6M) -- classified-subset, not total (don't read as AUA). |

## Overall verdict: BROKEN@MECHANICAL (seam 3, weakest-seam-binds) + SEMANTIC (seam 1 source-freeze, seam 4 staleness) + DECLARATIVE (seam 4 firm-id)

## Knowledge-parity delta
- BELIEVED: "daily BD pulls -> fresh cot AUA." TRUE: daily pull lands bronze, but the gold/platinum AUA has been frozen 9 days; fresh bronze piles up unused.
- A FIX IS ALREADY COMMITTED+DEPLOYED (06-18 ~09:05 EDT) but UNVERIFIED (not yet exercised by a nightly): db9521f3c (transactions header-mangle un-freeze) + 864139e7a (sentinel gate-semantics) + b09296f08 (sentinel emission); deployed code/silver/cot_silver_merge.py (S3 06-18 09:05). The 06-18 02:02 UTC nightly PREDATED it. First real test = 06-19 02:00 UTC nightly. Committed+deployed != verified.

## Fix legs (for the COTETL PRD/TO breakout -- routed to CTO)
- L1: VERIFY the transactions-unfreeze end-to-end on the 06-19 nightly (transactions silver succeeds -> silver_complete.json emits -> gold-run fires -> fresh gold/platinum). If it doesn't self-resolve, manual chain-run + root-cause why.
- L2: BD unrealized/holdings SOURCE date-freeze (06-09) -- the AUA basis. Investigate BD export asOfDate / holdings-snapshot cadence; fix so the basis advances (else AUA stays ~06-09 even post-chain-unblock).
- L3: cleanup firm_id="49financial" mislabel in cot gold/platinum generation.
- L4: freshness/staleness ALERT so a silent multi-day AUA freeze is LOUD (ties to F-1 opal-critical-surface-alerts SNS-egress, currently broken).
- L5: comprehensive end-to-end re-verify + an AUA-freshness guard on the served artifact.

## Residual / unknowns
- Whether the 06-19 nightly self-resolves L1 (UNVERIFIED until it runs).
- Exact origin of the unrealized 06-09 source-freeze (BD-account snapshot vs export asOfDate) -- UNVERIFIED, L2.
- Whether transactions is correctly in the sentinel gate's required-set vs should be exempt (snapshot-first design) -- CTO/DS call; moot if the un-freeze holds.

## Compiler Tools
| run | result |
|---|---|
| aws s3 ls/cp (cot layers, served JSONs, manifests, SSM log) | localized freeze: bronze fresh / gold+platinum 06-09 |
| aws events list-rules/list-targets/describe-rule/test-event-pattern | seam-3 rule CORRECT, target mode=gold-run, sentinel never emitted |
| aws lambda get-function-configuration + logs filter-log-events | trigger fires session/bronze/silver, no gold-run step |
| aws ssm get-command-invocation (silver-run 06-18) | the smoking gun: "silver sentinel NOT emitted -- transactions(last_successful_run=None)" + "Data date 2026-06-09" |
| git log (cot silver) | fix committed db9521f3c 06-18 09:04 EDT, deployed S3 09:05, post the 02:02 nightly |
