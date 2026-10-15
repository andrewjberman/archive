# IRPT_DASHBD rounds 133, 134, 135, 136 and 137, workstream B-49F + contract -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~19:4xZ)

**Five rounds, all drained: round 133 (`DB-b-265`, the report-build Terraform root and source-map entry, WORLD by the floor of its `infra/` paths, no AWS write), round 134 (`DB-b-266`, the landing schedule enabled, by the AE applier), round 135 (`DB-b-267`, the contract guard of the report-build handler), round 136 (the read of the three source-absent days, a LOCAL direct act) and round 137 (`DB-b-269`, the unreported-day statement of the handler; `DB-b-270`, `account_return_daily` contract 0.4.0). Counts, hashes and words only.** Merged: `DB-b-265` @82f54afc00, `DB-b-266` @024df9674d, `DB-b-267` @c756646bd1, `DB-b-269` @d6bc5ecbee, `DB-b-270` @ef923dab52; the round-136 record @b9af37d608. Not pushed. `round-close-check` for rounds 135 and 137: complete, no JUDGMENT criterion, MAY-CLOSE. Every criterion was run by me in the worker's tree and again on the LANDED tree: PASS (`DB133-1-AC1..AC3`, `DB135-1-AC1..AC3`, `DB137-1-AC1..AC3`, `DB137-2-AC1..AC3`, `DB136-1-AC1`, `AC2`).

## Round 133 -- the report-build function's Terraform root

`infra/aws/terraform/investor-reporting/reporting-gold-iso/` (neutral root name; the commit-time naming gate refused a typed firm token, row `D2-S90`) and the source-map entry `irpt-cot-reporting-gold-lambda` (18 pinned members plus the handler). Seven resources, all named by `lib/opal_naming.py`, the layer read by a data source, the schedule DISABLED, one PutObject statement. Nothing planned or applied.

## Round 134 -- the landing schedule is enabled

`irpt-cot-account-return-daily-daily`, `cron(15 8 ? * MON-FRI *)` America/New_York, ENABLED by one `safe-apply` of exactly 0 add / 1 change / 0 destroy. **First fire tomorrow, 2026-10-16, about 12:15Z; I read it then** (exactly one new partition, history unmodified, a value spot read). The ledger `irpt-dashbd-cottonwood-schedule-enable-20261015` stays open until then.

## Round 135 -- the contract guard (row `D2-S92`)

The handler reads each returns partition's `manifest.json` and chains only within ONE `(contract_version, method_version)`; a mixed or unnamed contract refuses with zero puts; a built day states `returns_from` (2026-07-10) and its contract; the Commonwealth partition of 2026-06-22 is never listed or opened; a window reaching before the floor reads `NOT_SPANNED` in words in the real fold. 26 tests.

## Round 136 -- the three source-absent days (direct act)

2026-08-19, 2026-09-24 and 2026-09-25 hold silver values but no flows. The next day's return is kept (inferred), and each absent day's own return is missing, so a window compounding across one lacks that day. The CTO ruled (ADDENDUM 1, msg 8524): no sidecar write; the handler states the gap.

## Round 137 -- the unreported-day statement and contract 0.4.0

**`DB-b-269`:** a built day's result lists `unreported_days` (the trading calendar from `returns_from` to the day, minus the returns partitions present), states "N trading days not reported by the source (dates)", and names which of `qtd`, `ytd`, `last_12_months` and `since_inception` hold each; it never lists, reads or writes the absent day. A test spans 2026-08-19. 33 handler tests. **`DB-b-270` (for your L9, the CTO's ruling msg 8546):** `org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json` is 0.4.0. `external_flow` and `income_received` stay `nullable: false` and gain `nullable_when {source: orion, flow_claim: absent}`; optional columns `flow_claim` and `source_account_id` (int64) are added; the 19 columns and `schema_hash` are byte-unchanged; `schema_hash_with_optional` is recomputed; the 0.3.0 entry is in `supersedes`; `source_rules.orion` states the trading-day compounding and the `account_dim` mapping. 12 new tests; the 52 earlier contract-reading tests pass (one assertion of the Cottonwood adapter test moved to the 0.3.0 hash, 3 lines, by Amendment 1).

## Issuer errors and rows this period (mine, disclosed)

My `DB-b-270` order did not grant the earlier Cottonwood adapter test that pins the contract's top-level optional hash; the worker stopped on the refusal clause (row `IRPT_DASHBD-D2-W219-S1`, BLOCKING) and I ruled it by Amendment 1 (commit f8c18a0e87). **The worker's gate refused to let a worker row graduate S1, so S1 needs YOUR disposition as resolved.** `DB131-1-AC2` and `AC3` are red on purpose (round 131's fixture holds no manifest; round 135's probe is the superset): row `W217-S2`. Earlier this period: the commit-time naming gate refused a firm token I typed in the source-map carriers (row `D2-S90`).

## Rows held (owners named)

`W209-S3` (ARMED, CTO); `D2-S72` (2.0.0_SA_COO~B1, no reply); `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). No ARMED row has a dark owner as far as this seat can read.

## What is next, and what goes to the CTO

The report-build pair (`NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_LAMBDA.md`, sha256 `cc5e87ff22e6`) is signed on both halves; the CTO's question-3 condition (each backfilled day carries `households_as_of` and `households_claim: held`, and the after-read counts the accounts the membership drops and the households with no rows) changes the handler, so round 138 (`DB-b-271`, worker `~220`, in flight) builds it and the pair is re-issued as revision 2 for a new CTO half. Then the apply order to `0.7.0_AE_CloudOps~DB2`. The schedule of the report-build function stays DISABLED until the CTO's separate word.

## What this does to the FWD outcomes

`FWD-1` (Cottonwood thread): the report build has its handler (guard, unreported-day statement, households claim in flight), its root, and a signed pair; the deploy and first events are the remaining acts. Contract 0.4.0 serves the Scope (Orion) adapter cell of `2.0.0_SA_COO~I2`. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
