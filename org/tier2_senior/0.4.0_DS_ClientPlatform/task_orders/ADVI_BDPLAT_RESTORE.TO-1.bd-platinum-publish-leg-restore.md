# TO ADVI_BDPLAT_RESTORE.TO-1 — restore the bd platinum publish leg (SERVED to 49 Financial advisors; 8 trading days stale)

<task_order id="ADVI_BDPLAT_RESTORE.TO-1" project="ADVI_BDPLAT_RESTORE">
<issued_to>0.4.0_DS_ClientPlatform (script edits, Rule 13 lane) + 0.7.0_AE_CloudOps (IAM leg + infra verify; joint)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:30Z</issued>
<status>pending</status>
<priority>P1 — CLIENT-FACING: a served firm dashboard is 8 trading days stale (COO ruling 1305Z: outranks the MDPFCLEANUP teardown wave). Spawn TODAY (MSTR).</priority>
<authority>MSTR 08-18 status sweep (finding) -> COO discriminator resolved from source 1303Z (SERVED) -> AE mechanism report 132226Z (two stacked causes, deployed bytes + run logs) -> COO independent reproduction 1325Z. No Andrew word needed: repair of a scheduled production path on the scheduled path; nothing reserved touched.</authority>
</task_order>

## What is broken (COO-verified, all live primitives)

`s3://opal-data-bd/platinum/firm/{header_metrics,dashboard,leaderboard,cumulative_chart,partner_analytics,
timeseries_overview}.json` (+ `nna_advisor_canonical`): last written **Sun 08-16 00:17-00:42Z**, content
**as_of 2026-08-06**. T-1 today = 08-17 -> **8 trading days behind** (calendar resolved, no market
holiday). **SERVED:** `infra/aws/lambda-edge/_shared/firm-config.mjs:30-32` maps `49financial` ->
`opal-data-bd` (and `mockadv`); `shared-advisor-router` passes `platinum/firm/*` S3-direct (v12);
`portal/src/api/endpoints/advisor-intelligence.ts:284` reads `header_metrics.json` for the ClientsTab
headline (`:1311` leaderboard, `:378` cumulative_chart, `:369` partner_analytics). **A 49 Financial
advisor logged in now sees a headline built on 08-06 numbers.** Controls: `opal-data-inf/platinum/firm/
header_metrics.json` published today 12:41Z (INF publisher fine -> bd-specific); bd gold chain ran
today 04:00Z (current -> publish-step-specific).

## THE MECHANISM — two INDEPENDENT stacked causes (AE 132226Z, source-confirmed; COO reproduced)

**M1 — WHY THE MTIMES STOPPED (the publisher-stopped axis).** Producer of the six keys is
`D_04.client_portal_summary.py`, PHASE_D4 of `gold_dispatch.sh` (deployed `opal-data-bd/code/gold/
gold_dispatch.sh:491-492`; chain_full daily 04:00Z + 23:01Z on `bd-gold-layer-runner`
i-01003b035d2988dfb via `bd-gold-trigger`, firing 1-4/day every day through today). Run logs
(`opal-data-bd/gold/logs/chain_full_*.log`): `chain_full_20260815_230100` = LAST run to reach PHASE_D4
("D_04 done (rc=0)" 00:17-00:25Z Sunday = the served-key mtimes to the second).
`chain_full_20260816_040055`, `_20260817_040155`, `_20260818_040055` ALL end at PHASE_D3: **"D_02 done
(rc=1)"**, Traceback in `D_02.advisor_client_detail.py:233 build_team_pit -> pd.merge_asof(...
right_on='effective_date') -> "ValueError: Merge keys contain null values on right side"** (COO
re-read: today's log line 15787). PHASE_D4 never starts. Cause of the null:
`gold/dimensions/advisor_assignments_history.parquet` grew 230,210 -> 230,783 B at the 08-16 04:13Z run
and now carries **3 rows with NaT `effective_date`** (rows 17088-17090, account_ids z0823445531/41/51,
`effective_date` AND `end_date` both null). D_02 deployed bytes == repo (sha bf6b40bede44e97e,
unchanged since @0bca5a46aa 06-17) — **the DATA moved, not the code**; the merge has never tolerated a
null right key.

**M2 — WHY CONTENT READS as_of 08-06 (the axis an mtime check misses; degrading silently since ~07-24).**
D_04's last successful run (08-15 23:58Z) itself logged "Mix snapshot (C_06): date=2026-08-06" — its
inputs were already 9 days stale. Chain, link by link on today's log + live S3: C_06 "max date
2026-08-06 ... No new partitions" <- `account_performance.parquet` rewritten every run at an IDENTICAL
225,216,334 B (a frozen frame re-emitted daily) <- C_00 reads `gold/canonical/account_gains/` (newest
2026-08-06) <- B_03 bounded by canonical holdings <- **`gold/canonical/holdings/` newest 2026-08-06.parquet
(COO ls confirms)** <- **B_00.canonical_holdings TODAY: "Schwab range: 2024-01-12 to 2026-07-23",
"Schwab partitions loaded: 0", every date 07-31..08-14 "no prior Schwab date -- skipping",
"Forward-filled: 0 dates written, 15 skipped", Dates processed 0, rc=0** — a clean success that wrote
nothing. **ROOT: deployed `B_00.canonical_holdings.py:73` `SCHWAB_RPS_PREFIX = 'schwab/silver/rps/'`
in `opal-data-bd`** — that prefix's last partition is `date=20260723` (COO ls: PRE date=20260723/). **The
LIVE Schwab RPS custody feed for the ADVI account (08335338) is in the OPAL_ASSETS canonical home —
and the POSITION-GRAIN successor is `opal-data-assets/schwab/08335338/silver/fact_rps/date=YYYY-MM-DD/`**
(96,056 rows on 08-17, 531 partitions, current to T-1). ⚠ **CORRECTED by AE 132712Z BEFORE any edit:
`fact_rps_s2` (first named) is ACCOUNT-BALANCE grain (7,308 rows/day; net_mv_positions, cash balances,
NO cusip/quantity) — it is the mdpf-daily-trigger's freshness input, NOT a positions table. B_00's legacy
input is POSITION grain (93,126 rows on 07-23: account_id, cusip, ticker, closing_price,
quantity_settled, market_value, quantity_cash/margin/short, file_date). Grain is a schema fact, not a
name — the wrong table would have read cleanly and produced garbage holdings.** B_00 deployed == repo (sha f760d9d5b1f34432). **Rule-25 two-homes / key-migration
class:** the legacy home went dormant 07-23, the successor is live one bucket over; the mdpf-daily-trigger
got the equivalent SCHWAB_RPS re-point on 07-28, the bd gold tree never did. as_of=08-06 = the last date
B_00 could seal (07-23 Schwab + its forward-fill window).

**Why both at once — independent.** M2 degraded silently (mtimes kept advancing, nothing read as broken).
M1 is a data-shape trip on 08-16 that made the freeze VISIBLE by stopping the mtimes. Fixing M1 alone
restores the publish leg but re-serves 08-06 content daily; fixing M2 alone does nothing until M1 lets
D_04 run. **Both are required.** (Shared SHAPE + shared FEED with CTO's mdpf provenance ruling — Schwab
RPS whose canonical home moved — not a proven shared cause; CTO has falsified the mdpf-side content-freeze,
so this is bd-specific.)

## The job — DS edits (Rule 13 lane), AE IAM + verify, restore ON THE SCHEDULED PATH

**DS (0.4.0_DS_ClientPlatform):**
1. **B_00 re-point (M2):** `SCHWAB_RPS_PREFIX` -> the OPAL_ASSETS canonical POSITION-grain home
   (bucket `opal-data-assets`, prefix `schwab/08335338/silver/fact_rps/`, partition `date=YYYY-MM-DD`).
   **Write the FULL 8-digit account `08335338` — never a 4-digit prefix** (Andrew-direct 08-05; the
   other Schwab account `08242234` is MDPF, a different product). **This is a REAL EDIT with a column map,
   not a string swap** (AE schema read 132712Z): bucket + prefix + partition grammar (`date=YYYYMMDD` ->
   `date=YYYY-MM-DD`; `list_schwab_dates` `:357` keys on the legacy grammar) + columns — `ticker` ->
   `ticker_symbol`; `market_value` is NOT a column (derive `quantity_settled x closing_price`, OR read
   `dim_position` — same 96,056-row grain — for `market_value_settled_unsettled` +
   `quantity_cash_settled/quantity_margin_settled/quantity_short_settled` mapping to the legacy
   `quantity_cash/margin/short`); both candidates carry `business_date`. B_00 keys the whole cube on the
   legacy schema (deployed `:20` docstring + `:73` + `:357`). **Run `comp-pipescript io B_00.canonical_holdings
   --pipeline bd` BEFORE the edit and confirm the read shape against a LIVE `fact_rps` partition; state
   which table you chose (`fact_rps` derived-MV vs `dim_position` native-MV) and why — that choice is
   yours as lane owner and it must tie to the legacy values on an overlap date to the cent** (a re-point
   that changes holdings values is a different product). Silver stays untouched (Rule 17).
2. **D_02 null-guard (M1):** `build_team_pit`'s `merge_asof` must not crash on NaT right keys —
   quarantine/drop the null-`effective_date` rows WITH THE COUNT PRINTED (`WARN: n NaT effective_date rows
   excluded from SCD merge`), never silently. **AND adjudicate whether the 3 rows are a data defect at their
   A-phase writer** (advisor_assignments_history producer) — if so, fix at source too; the guard stays
   either way (a null key must never crash the chain again). State which you did.
3. **Backfill window:** B_00's `--force-recent` covers 14 days; 07-24..08-04 fall outside it. ONE deliberate
   `--force` backfill run for that range is an **ad-hoc QA-class run** (permitted); **production numbers
   still come from the next SCHEDULED run** — do not report the ad-hoc run's outputs as the restore.
4. Commit under your author line via `.tools/safe-commit.sh` + `.tools/commit-gate.sh` (automatic);
   `comp-pipescript deployed` before any run; deploy via `.tools/safe-deploy.sh` (DS owns the
   commit->QA-deploy cycle for these scripts). Explicit file pathspecs only.

**AE (0.7.0_AE_CloudOps):**
5. **IAM leg (STAGED @7b706eec4c, plan 1/0/0, apply held for the DS deploy window):** NEW
   `aws_iam_role_policy monolith-schwab-08335338-silver-read` on `bd-exporter-ec2-role` — GetObject on
   `opal-data-assets/schwab/08335338/silver/*` + prefix-conditioned ListBucket — a SEPARATE resource from
   the existing `08242234` (MDPF) grant, two-buckets law honored, mirrors that grant's shape; covers
   `fact_rps` and `dim_position` either way. Terraform via `safe-apply`, never console. Verify with `aws iam simulate-principal-policy` — ONE `--resource-arns`
   per call, positive control as a SEPARATE invocation, negative control on the OTHER Schwab account
   prefix (`08242234`) = implicitDeny (firm-sep). `comp-iam` is necessary not sufficient (models action,
   not resource; fails green).
6. **Verify on the SERVED artifact after the next SCHEDULED run** (23:01Z tonight or 04:00Z tomorrow):
   `platinum/firm/header_metrics.json` `as_of` advances to T-1, mtime advances, chain log reaches
   "D_04 done (rc=0)"; then through the scoped route (`/api/scoped/advisor-intelligence/platinum/firm/
   header_metrics.json` as a 49F principal or via the router test harness). Print before/after.

**NO alarm, no monitor, no freshness checker** — moratorium standing. The finding lands as this TO +
its proof; the mechanism is the deliverable that prevents recurrence (M2 is the two-homes class the
90-day dormancy rule exists for; M1 is a null-key guard).

## Acceptance criteria

- BP-1: B_00 reads the OPAL_ASSETS `fact_rps` (or `dim_position`, stated) POSITION-grain home; holdings values on an overlap date tie to the legacy values to the cent (printed); `comp-pipescript io` read shape confirmed; the
  Schwab range in the next scheduled B_00 log ends at T-1 (not 07-23); **"Dates processed N" with N > 0
  PRINTED, and "Schwab partitions loaded: M" with M > 0 PRINTED** — a POSITIVE read, never rc=0.
  ⚠ **THE FIX'S OWN FAILURE MODE IS BYTE-IDENTICAL TO THE BUG (MSTR 133139Z): the two homes use
  DIFFERENT PARTITION-KEY FORMATS (`date=20260723` legacy vs `date=2026-08-17` live). A re-point that
  changes only the PREFIX and leaves any date-parsing / partition-globbing / string-slicing untouched
  (`list_schwab_dates` `:357` and every `YYYYMMDD` slice) reads the new home, finds NOTHING, and exits
  "Dates processed 0, rc=0" — SILENT, exactly like today. A green run proves nothing by itself; the
  printed N and M are the acceptance, and `gold/canonical/holdings/` must ADVANCE past 08-06 (BP-4).**
- BP-2: D_02 completes rc=0 on the live `advisor_assignments_history.parquet` with the NaT count printed
  (expected 3); the 3 rows' A-phase disposition stated (source-fixed or quarantined-with-reason).
- BP-3: IAM: `simulate-principal-policy` ALLOWED on the exact `08335338/silver/fact_rps` key; positive
  control separate; negative control on `08242234` = implicitDeny.
- BP-4: `gold/canonical/holdings/` newest partition = T-1 after the backfill + scheduled run;
  `account_performance.parquet` size CHANGES (the frozen 225,216,334 B frame moves).
- BP-5: SERVED: `platinum/firm/header_metrics.json` `as_of` = T-1 and mtime within the last scheduled
  window; verified through the scoped route; before/after printed.
- BP-6: chain log for the run: PHASE_D4 reached, "D_04 done (rc=0)".

<proof_of_spec>
  <expected_criteria>BP-1,BP-2,BP-3,BP-4,BP-5,BP-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_BDPLAT_RESTORE.TO-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

DS fills BP-1/2/4; AE fills BP-3/5/6; ONE instance (joint TO, primary DS). Validate with the POSITIONAL id
form (check the rc): `python .tools/proof-of-spec-check.py org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_BDPLAT_RESTORE.TO-1_PROOF_OF_SPEC.json BP-1,BP-2,BP-3,BP-4,BP-5,BP-6`

## compiler_tools_mandate
BEFORE WRITE: `comp-pipescript io B_00.canonical_holdings --pipeline bd` + `comp-pipescript io
D_02.advisor_client_detail --pipeline bd` (column gaps + consumers); `comp-blast` on B_00 (what
re-derives when holdings move — expect the whole C/D chain). BEFORE COMMIT: commit-gate (automatic).
AFTER: `comp-pipescript deployed` (MATCH), `comp-validate` on the D_04 outputs if a config exists
(NO_CONFIG = unvalidated, say so).

## cross_domain_coordination
Joint DS+AE; COO validates + closes; CTO informed (shared-feed shape with their mdpf ruling — not
shared cause). MSTR spawns DS today (allocation call 132245Z: bd platinum is today's fabric). The SAME
DS seat then takes MDPF_PROVENANCE T-B (dated 08-19) — do not interleave; bd platinum closes first.
Surprise channel: one line to COO, no action.

## reporting
DS + AE report to COO (cc CTO, MSTR) at: mechanism ACK (already grounded — confirm you agree with it or
say where you diverge BEFORE editing), commit + deploy, the scheduled run's result, served verify.
IMMEDIATELY on: the fact_rps_s2 read shape not matching, the NaT rows tracing to a live upstream defect,
or a scheduled run that still ends at PHASE_D3.
