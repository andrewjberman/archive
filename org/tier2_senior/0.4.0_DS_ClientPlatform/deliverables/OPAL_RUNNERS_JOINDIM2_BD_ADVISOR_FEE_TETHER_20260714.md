# JOIN DIM 2 — the ONE scoped BD advisor/fee dim (design note, read-only)

**Author:** 0.4.0_DS_ClientPlatform, 2026-07-14 ~08:2xZ
**Commission:** Andrew-named via CTO 20260714T075142Z ("DS can probably figure out the black diamond
adv metadata thing"); bounded by the Andrew 03:57Z ruling — *"If we have to hit one scoped dim table
daily from Black Diamond, so be it, I can live with that."* ONE dim, daily; NOT BD-back-in-the-pipeline.
**Fills:** `docs/architecture/OPAL_RUNNERS_49F_SILVER_DATA_DICTIONARY.md` §4's four cells (@ 7295323d4);
feeds §5's advisor-role rows. CTO folds on landing (his 081051Z).
**Method:** every claim below is grounded on SOURCE the way the dispatch ordered — the dim builders I
authored (`data/canonical/schwab/silver/build_dim_advisor_role.py` @ HEAD 7d3e0b72c-era tree,
`build_dim_advisor_fee.py` same tree), the legacy readers' ACTUAL usage (A_01/A_02/C_07/C_08 source
read this session), and the canonical gold consumers (G11/G13 source read). comp-pipescript io on A_01
returned no static I/O (dynamic key construction — its WARN is honest); the source reads below are the
grounding. Read-only throughout; nothing here builds anything.

---

## Cell 1 — MINIMAL COLUMN SET (from what the readers actually consume, nothing more)

Three BD-side sources feed the layer today; every consumed column enumerated:

**(a) BD allocations feed** (`opal-data-bd/silver/allocations/<date>.parquet`) — the ROLE + SPLIT facts:
`account_id` (BD z-id, the feed's key), `architect`, `implementor`, `consultant`, `local_ops`,
`additional_advisor`, `architect_split_pct`, `implementor_split_pct`, `consultant_split_pct`,
`local_ops_split_pct`, `additional_advisor_split_pct`, `house_split_pct`.
(5 named split-model roles + house; `manager`/`money_manager` carry NO split — measured, not assumed.)

**(b) BD fees feed** (`opal-data-bd/silver/fees/<date>.parquet`, the Fees_OpalCapital_Daily report) —
the advisory RATE schedule: `account_number` (BD-native key — NOTE: a DIFFERENT key than (a)'s z-id),
`basis_points`, `flat_fee`, `account_fee_schedule`, `fee_schedule_rate_type`, `fee_schedule_type`
(fee basis, e.g. "Total Value"), `account_billable`, `billing_account_custodian`.

**(c) the account_xref bridge** (`opal-data-bd/schwab/silver/account_xref/date=*/`): `bd_account_id`,
`bd_account_number`, `schwab_padded_id`, `bd_architect`, `bd_manager`. **The key duality in (a)/(b) is
load-bearing:** allocations bridges on `bd_account_id`, fees bridges on `bd_account_number` — the xref
must carry BOTH or one feed strands.

**The ONE dim's column set** (account grain, PK = Schwab `account_id` 10-digit padded string):

| group | columns | source |
|---|---|---|
| key + bridge echo | account_id (PK); bd_account_id, bd_account_number (audit echo) | xref |
| roles | architect, manager, implementor, consultant, local_ops, additional_advisor | alloc feed (+ xref architect/manager as the coherence pair, flag-not-overwrite per the TO-7 pattern) |
| splits | {architect,implementor,consultant,local_ops,additional_advisor}_split_pct, house_split_pct | alloc feed; curated-override layer wins per (account,role) with per-role `{role}_split_source` provenance (exists today, Andrew-curated CSV) |
| fee schedule | annual_fee_bps, annual_fee_pct, flat_fee, fee_schedule, fee_rate_type, fee_basis, billable, billing_custodian | fees feed |
| SCD2 | effective_from, effective_to, is_current | maintained by the dim process |
| provenance | roles_source, roles_source_as_of, fee_source, fee_source_as_of, xref_source_as_of, schema_version | stamped per row |

**Deliberately NOT in the dim:** `money_manager` (SmartX/custodian-side — Schwab-native, rides the
Schwab spine); per-trade commissions/costs (TCF -> `fact_billing`, Schwab-native — see anti-pathology
(e)); C_07's Layer-2/3 relationship-rollup + architect-inference (an OPAL derivation — gold-side,
labeled, the `architect` vs `architect_no_infer` precedent); any normalization of split sums (Andrew
verbatim 2026-06-29: *"No Normalizing, whatever they have is what it is"* — the gap is G13-recon's to
quantify, never the dim's to fix).

**One open semantic (named, not guessed):** Andrew's list includes advisor *"type"*. The fee-side
types (`fee_rate_type`, `fee_basis`) are covered above; **no current reader consumes an advisor-TYPE
field** (person-level classification). If "type" means the role taxonomy itself, it is covered by the
6 role columns; if it means something else (e.g. W-2 vs 1099 advisor class), that field exists in no
feed we read today — needs Andrew's word, one line.

## Cell 2 — THE JOIN KEY: account-x-period CONFIRMED; txn-grain REFUTED as a dim requirement

CTO's prior is **confirmed from the legacy readers' actual usage**:

- **C_08** (fee efficiency, the sharpest consumer) computes per (account, date):
  `implied_daily_fee = AUA * fee_bps/10000/252 * split_pct/100` — its joins are NNA-by-account-by-date
  x splits-SCD2 x rates-SCD2, i.e. **(account_id, date) resolved against [effective_from,
  effective_to]**. No txn-id, no cusip, anywhere in the role/fee path.
- **C_07 / G11 / G13** consume roles+splits at plain ACCOUNT grain.
- The txn-id+cusip+date tuple matters only inside NNA/flow CLASSIFICATION — which on the 0833 spine is
  **Schwab-native** (TRN carries its own transaction identity and date). A flow row joins the dim by
  (account, date-in-period); it never needs a BD transaction key. **Forging a BD txn join key would
  import the A_01 pathology through the front door** (cell 4a).

**Therefore the key is:** BD account (both BD-native keys) <-> Schwab account number via the xref
bridge class, SCD2 on effective period. The xref is the third input with its own freshness contract:
seeded from today's `account_xref`, refreshed as accounts open (daily ACC on the Schwab side + BD
account identity on the pull side); **unbridged rows REPORTED, never silently dropped** (both existing
builders already hold this line — the report count is the guard).

## Cell 3 — GRAIN + FRESHNESS: SCD2 account x effective-period, maintained by daily snapshot-diff

- **Grain:** SCD2, account x effective-period — CTO's prior confirmed, and it is the A_02 pattern
  (snapshot-diff change detection: close the open period, open a new one when the
  role/split/rate tuple changes) **generalized to the full tuple**, explicitly NOT the A_01 pattern
  (txn replay). Roles change slowly (legacy A_00 carries 5 roles forward; fee feed measured
  account-stable at 1/5400 same-day variation) — most days the diff is empty and "daily" costs one
  pull + one no-op diff.
- **What "daily" means:** pull the two BD reports once per day (one process, one landing manifest,
  one V2-6 `backfill-status.json` update — the meta layer this morning's V2-6 built exists for
  exactly this); diff against current-open periods; serve the current-row view as the daily dim
  partition; retain full SCD2 history.
- **The emptiness contract (ruling 26), with LIVE evidence it is real:** BD `silver/allocations`
  partitions from 06-26 onward are measured frozen/EMPTY — my role builder already skips them as an
  honest fallback (`latest_allocations`, "skip the frozen/empty 06-26+ partitions"). The daily dim
  process must state: whole-feed empty = IMPOSSIBLY-EMPTY -> fail loud, do NOT roll the dim, do NOT
  advance vintages (a rolled vintage over an empty pull is a false freshness claim).
- **Account-absent-from-a-NON-empty feed** is the subtler mode (the LD-0292 vanishing-row class): the
  dim CARRIES the account's open period + flags it `absent_from_feed_since=<date>`, surfaces after a
  named TTL (propose 5 trading days) — never an immediate silent close (a BD report hiccup would mass-
  close periods), never an indefinite silent carry (how $528mm walked out of `held_by_partner`).

## Cell 4 — ANTI-PATHOLOGY: what would tempt a re-derive, named

a) **Transaction replay (the A_01 pathology itself).** BD txn rows embed advisor/split fields, and the
   ONLY role history predating the daily feeds lives there — that is the standing temptation. Rule:
   the dim's history ACCRUES FORWARD from daily facts; if pre-feed history is ever wanted, it is a
   ONE-TIME, labeled, Andrew-ruled import — never a standing derivation, never silently mixed with
   fact-sourced periods (`period_source='txn-replay-import'` if it ever happens).
b) **Reverse-engineering splits from billed dollars.** Splits are FACTS from the feed + the curated
   override layer. A split-sum that doesn't close is G13-recon's to quantify (the dedicated
   "money not accounted for" surface), never solved by inference.
c) **House/placeholder inference.** '49F House' and 'Unassigned' are dim VALUES, kept as-is; C_07's
   Layer-2/3 inference stays gold-side and labeled (`architect_no_infer` is the canonical
   attribution source per ADVI_NNAATTR F-0 — the dim must not pre-bake what that invariant unbakes).
d) **Master mixing.** The dim is scoped per master; 0824 and 0833 never share rows, never sum
   (standing identity law). Whether 0824's book carries the same BD advisor model is an OPEN cell —
   do not clone the 0833 design onto 0824 without measuring its feeds.
e) **TCF conflation.** Per-trade execution cost is Schwab-native `fact_billing`; the dim carries the
   advisory RATE schedule only. Pulling BD billing DOLLARS into the dim would duplicate a
   Schwab-native fact under a BD vintage — two numbers, one name, downstream picks wrong.

## Wiring options (CTO binds; both keep "ONE dim, hit daily" true)

- **Option T — transition (runs today):** the two canonical builders already produce this layer from
  the legacy-bucket feeds (dim_advisor_role v2.0 + dim_advisor_fee v1.0, consumed by G11-G13). Merging
  fee columns into the role build makes them the literal ONE table with near-zero new code. Physical
  home stays `opal-data-bd/canonical/...` (the legacy tree).
- **Option M — monolith-native (the greenfield target, recommended):** the Andrew-ordered daily BD
  REST pattern lands the two reports RAW under the monolith's grammar
  (`blackdiamond/<49f-scope>/bronze/{allocations,fees}/{date}/` — 17a byte-passthrough), one converter
  maintains the ONE silver dim (`{source}/{scope}/silver/dim_advisor_fee_role/`, hive `date=`
  partitions per ruling 23, SCD2 columns in-table) with a landing guard + per-pull manifest + V2-6
  `backfill-status.json` at the ruling-21 meta home. A_00 reads it via the dictionary. The builders'
  logic transfers nearly verbatim (same author, same cleaning rules); Option T keeps serving existing
  surfaces until the ruled cutover.
- **Either way, ONE daily BD touch:** one pull process, two report endpoints, one manifest, one guard
  — "hit one scoped dim table daily" is satisfied at the process boundary, which is where the 03:57Z
  ruling draws the line (NOT BD-back-in-the-pipeline).

## Open cells (owners proposed)

1. Andrew's advisor-"type" semantics (one line from Andrew; see cell 1).
2. 0824's BD advisor model — measure before cloning (DS, gated on the 0824 runner scope).
3. Pre-feed role-history disposition — wanted at all? (Andrew/CTO; default = forward-accrual only.)
4. xref refresh ownership + cadence in the monolith form (DS proposes: the same daily pull process,
   unbridged-report as its guard).
5. The BD allocations feed's frozen-empty state post-06-26 — the daily pull needs the feed itself
   healthy or the REST pattern replaces it at the source (0.7.0/CTO at the daily-REST design).
