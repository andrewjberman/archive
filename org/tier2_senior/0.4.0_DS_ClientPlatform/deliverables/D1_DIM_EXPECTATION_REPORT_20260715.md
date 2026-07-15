# D1 dim build — PINNED EXPECTATION REPORT (pre-build gate)

**Author:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~16:4xZ
**Task:** `OPAL_ASSETS_49METATABLES.D1.bd-advisor-fee-dim-build` = **WS-B2**, the OPAL_CONSOLIDATION
P0 critical path (COO P0 wave 154910Z; unlocks WS-C2, the Andrew+CTO 49F runner architecture session).
**Binding records:** CTO dispatch 20260714T085454Z (scope a-d + ship gate) · PRD
`docs/architecture/OPAL_ASSETS_49METATABLES_PRD.md` §1 @ bd177ba0f · design of record
`OPAL_RUNNERS_JOINDIM2_BD_ADVISOR_FEE_TETHER_20260714.md` @ 2d2ffcd60 (+ tenancy addendum) ·
contract `OPAL_ASSETS_V2_LAMBDA_CONTRACT.md` v1.2.4 (ruling 21 meta home, 23 silver grammar,
26 emptiness) · family law: expectation-report-BEFORE-run (smartx trilogy pattern, CTO-affirmed).
**Discipline:** every number below was measured on the LANDED bronze bytes of the 2026-07-14
partition + the live 0833 silver + the live xref seed THIS SESSION (scratchpad scripts
`d1_ground_inputs.py`, `d1_ground_keys.py`, `d1_bridge_measure.py`, `d1_refresh_gain.py`,
`d1_expectation_pins.py`), BEFORE any converter code ran. The build run is measured against THIS file.

---

## 1. Input denominators (measured, partition 2026-07-14 — Apply B first fire 02:30:33Z)

| input | key | measured |
|---|---|---|
| allocation feed | `blackdiamond/49f/bronze/allocation_390224/2026-07-14/data.xlsx` | 30,541 rows × 92 cols; **6,154 distinct AccountID** (~5.0 portfolio-group rows/acct); sidecar `has_data_rows=1`, `as_of=2026-07-14`; pull_state floor 24,432 |
| fees feed | `blackdiamond/49f/bronze/fees_435407/2026-07-14/data.xlsx` | 1,208 rows × 34 cols; **310 distinct AccountID**; Trade Date range **03/25–04/02/2026** (= the Q2 quarterly billing window, NOT a rolling daily flow); floor 966 |
| template roster | `.../template_roster/2026-07-14/roster.json` | 47 templates (signal/ops, not dim input) |
| xref seed | `opal-data-bd/schwab/silver/account_xref/date=20260629/` | 7,486 rows; 6,997 digit `schwab_padded_id`; methods: direct_acct10 6,012 / fuzzy_last_name 654 / bd_only 489 / schwab_only 331 |
| 0833 acc universe | `opal-data-assets/schwab/08335338/silver/fact_acc/date=2026-07-14/` | **7,139 distinct account_id** (7,055 'O' + 84 'C') — the ship-gate denominator, same-vintage as the bronze |

## 2. Grain + key facts (measured)

- **Alloc grain = Portfolio Group × Account.** Account-grain attributes are stable within
  AccountID across an account's PG rows: exactly ONE account varies —
  `z0813542821` / acct 92264363 carries **two simultaneous fee schedules**
  ('49F - Flat 1' @100bps AND '49F - Flat 1.25' @125bps, duplicated across all 5 of its PG rows).
  Every other fee/role/split column: 0 accounts with within-account variation.
- **Keys:** alloc `AccountID` = BD z-id; alloc `Account Number` is BD-native (8-digit dominant,
  97.8% digit) — **NOT the Schwab number** in general; the xref bridge is load-bearing exactly as
  the design of record states. Fees `Account Number` IS the custodian number where linked
  (both bridge paths agree 199/199 where both present).
- **Fee block grain attribution:** the account-section columns bind the dim —
  `Basis Points.1`, `Flat Fee.1`, `Fee Schedule Level.1`, `Fee Schedule Rate Type`,
  `Fee Schedule Type`, `Fee Schedule Description`, `Account Fee Schedule`, `Account Billable`
  (positional attribution per the probe template census: child=Account 70 dims; empirically
  account-stable per the measurement above).
- **`Manager` is structurally unpopulated in the 49f tenancy** ('No Manager Defined' × 6,154).
  Column kept per design (6 roles), lands 'Unassigned'.
- **Value pins (account grain):** Architect distinct 48 ('No Architect Value Assigned' 2,826;
  'None' 387 — both clean to 'Unassigned'); Implementor 144; Consultant 73; Local Ops 18;
  Additional Advisor 25. Basis Points.1: median 100, range [0,1125], zero 1,014.
  Flat Fee.1: ALL ZERO. Account Fee Schedule distinct 41 (top '49F - Flat 1' 3,230);
  Rate Type ∈ {Flat Rate, No Rate Type}; Fee Schedule Type = 'Total Value' × all;
  Billable 5,620 / Non-Billable 534. 5-role split-sum in [95,105]: 4,984/6,154; ==0: 701.
  One split outlier (Implementor 6090%) — **preserved as-is** (Andrew: "No Normalizing");
  split-sum gaps are G13-recon's to quantify, never the dim's to fix.

## 3. The bridge — measured pre-build (these ARE the bridge-proof expectations)

| measurement | value |
|---|---|
| alloc accounts bridged via xref seed (`bd_account_id`) | **5,138 / 6,154 (83.5%)** |
| direct-acct10 refresh gain (unbridged acct-number zfill(10) ∈ universe) | **+198** (0 sid collisions) |
| ...of which the sid is held by a STALE seed row (BD re-keyed the account; old z-id absent from today's feed) | 181 |
| **post-refresh alloc-side coverage** | **5,336 / 6,154 (86.7%)** |
| **post-refresh universe-side coverage (THE ship-gate number)** | **5,296 / 7,139 (74.2%)** |
| bridged but not in 07-14 universe (kept, reported) | 40 |
| unbridged after refresh (REPORTED, never dropped) | **818** = 448 digit-number (non-0833: other-master/other-custodian) + 370 non-digit (held-away-class) |
| universe accounts with NO dim row (the runner's fee-attribution gap) | expected ≈ **1,843** |
| fees-feed containment | 264/310 in alloc; **46 fees-only** (April billing, absent from today's alloc snapshot → NO dim row, reported) |

## 4. Outputs the build must land (contract grammar, ruling 23/21)

1. **`blackdiamond/49f/silver/dim_advisor_fee_role/date=2026-07-14/data.parquet`** — the ONE dim.
   PK `account_id` (10-digit padded string). Pinned schema v1.0 (38 cols): key+echo
   (account_id, bd_account_id, bd_account_number) · 6 roles ('No X Value Assigned'/'None'→
   'Unassigned') · 6 split pcts float64 · 5 per-role `{role}_split_source` ('bd-allocation-feed'
   unless curated-override; override CSV currently 0 rows = honest no-op) · fee block
   (annual_fee_bps, annual_fee_pct, flat_fee, fee_schedule, fee_rate_type, fee_basis,
   fee_schedule_level, billable, billing_custodian←fees-feed nullable) · flags
   (fee_schedule_conflict, architect_matches_xref) · SCD2 (effective_from='2026-07-14',
   effective_to=null, is_current=true — feed-floor start, forward accrual per PRD §5.2 default) ·
   provenance (period_source='daily-feed', roles_source='bd-49f-allocation-390224',
   roles_source_as_of, fee_source, fee_source_as_of, bridge_method, bridge_as_of,
   absent_from_feed_since=null, schema_version='1.0').
   **EXPECT rows = 5,336 exactly** (independent re-derivation of §3 on the same bytes;
   structural band [5,000, 6,154]; PK unique HARD).
2. **`blackdiamond/49f/silver/dim_account_xref/date=2026-07-14/data.parquet`** — the refreshed
   bridge, feed-driven: ONE row per BD account in today's feeds (alloc ∪ fees).
   **EXPECT rows = 6,200** (6,154 + 46). Columns: bd_account_id (PK), bd_account_number,
   bd_original_account_number, schwab_account_id (nullable), match_method
   ('seed-xref'|'direct-acct10'|'unresolved'), match_as_of, in_0833_universe, account_is_open,
   feed_seen_date, schema_version. Unresolved rows STAY IN THE TABLE (the unbridged census is
   IN-BAND). Supersede semantics: a direct-acct10 match on a re-keyed account binds the NEW z-id;
   the stale seed row is not carried (seed contributes mappings, not rows).
3. **Manifest** `blackdiamond/49f/meta/conversions/{run_id}.json` — written ONLY after
   listing-verified landing; carries input denominators, bridge census (all §3 numbers as
   measured by the run), conflict count, floors checked, and the bridge-proof block.

## 5. Hard gates wired into the converter (refuse loud, land nothing)

(a) whole-feed empty → RAISE `ImpossiblyEmptyFeed` naming the feed (ruling 26; never roll
vintages); (b) rows < pull_state ratchet floor (24,432/966) → RAISE; (c) sidecar
`has_data_rows`≠1 or as_of≠partition → RAISE; (d) PK duplicate → RAISE; (e) fee-schedule
conflict handling: deterministic **highest-bps + `fee_schedule_conflict=true` + loud report +
manifest count** (design-of-record precedent from `build_dim_advisor_fee.py`; the atom-family
conflict-RAISE ruling is NAMED to CTO as tension — see §7 finding f); (f) writes via
`lib/stream_parquet.py` (atomic + ETag-verified); landing acceptance = **ListObjectsV2**
key+ETag+size, never HeadObject; manifest only after verify.

## 6. SCD2 day-2+ (code present, synthetically tested — n=1 partition reality)

Snapshot-diff ONLY (the five anti-pathologies hold): tuple change → close open period
(effective_to = prev day), open new (effective_from = as_of). Account absent from a NON-empty
feed → carry open period + `absent_from_feed_since=<date>`, surface after 5 trading days TTL,
never auto-close, never indefinite silent carry. Whole-feed empty never reaches the diff (gate a).
Mutant tests: forced tuple-change closes+opens; absent-account carries+flags; empty-feed raises;
conflict flags; PK dup raises.

## 7. Named findings routed to CTO with the build report (none block the build)

(a) **fees_435407 is a QUARTERLY BILLING WINDOW feed** (Trade Date 03/25–04/02), not the
account-grain daily rate report the June-era design assumed — the RATE SCHEDULE therefore
sources from the ALLOC account-section fee block (full 6,154 coverage), and the fees feed
contributes billing ids only (310 accounts, nullable) + is fact_billing-class material for the
runner (anti-pathology e). This is a bytes-grounded deviation from design cell 1(b)'s source
table, same columns. (b) **181 BD re-keyings**: seed-xref rows whose z-id no longer exists in
the feed while the account (same custodian number) reappears under a new z-id — the refresh
binds the new z-id; xref refresh is therefore SUPERSEDE, not append. (c) **z0813542821 dual
fee schedule** (Flat 1 vs Flat 1.25) — resolved deterministic-highest-bps + flagged.
(d) **~1,843 universe accounts carry no BD dim row** — the fee-attribution gap number the
runner architecture session needs (composition: BD book gap + 818 unbridged).
(e) **Manager structurally unpopulated** in 49f tenancy. (f) **Conflict-resolution tension**:
design-of-record deterministic-pick vs the atom-family conflict-RAISE ruling — implemented per
design of record (a daily dim that RAISES on one BD-side dual-schedule account is DOWN every
day until BD cleans it); CTO may overrule to RAISE.
