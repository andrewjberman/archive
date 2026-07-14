# OPAL_ASSETS_49METATABLES D3 — the 0833-native Group A: analysis + plan

**TO:** `OPAL_ASSETS_49METATABLES.D3.0833-groupa-analysis` (Andrew-named commission, CTO dispatch
`20260714T085509Z`; PRD §3 @ `bd177ba0f`) · **Author:** `0.6.2_AE_PartnerETL` · **Date:** 2026-07-14
~09:3xZ · **READ-ONLY** (analysis built nothing; converter lane runs parallel under its own ruling)

**Extraction methods + vintages (the W4 rider discipline — every measured claim below traces here):**
- **[M1]** live bronze bytes @ partition `20260713` (the current frontier, landed by this morning's
  exercised daily pull): `s3://opal-data-assets/schwab/08335338/bronze/{acc,fam,slm}/20260713/` +
  `s3://opal-data-assets/schwab/08242234/bronze/acc/20260713/`, pulled 2026-07-14 ~09:2xZ, parsed with
  `crs_reader.parse_crs` (T1 hard-raise; ACC tied 7,146/7,146) and `cs_reader.parse_cs` (width control
  6/6 on every row) — both readers @ `bc4110283` (HEAD). Scripts: session scratchpad `d3_measure*.py`.
- **[M2]** W4 census pair @ `b62919644` (column inventory JSON + 0824 census) and the 0833 sufficiency
  half (`0.4.0_DS`, measured 2026-07-14 ~03:15Z, partition `20260710`).
- **[M3]** dictionary v0.4 @ `8c2574c2e` (fact_/dim_ vocabulary + naming ruling) · casebook Entries 1–4
  @ `987b3f8f1` · V2-8 contract v1.1 @ `5e45d1896` · converter design doc + reader family @ `bc4110283`.

Presumption labels per the rlw precedent: **[MEASURED]** = from bytes with denominator ·
**[PRESUMED]** = consistent with bytes, semantics await the vendor FAM/SLM spec · **[INFERRED]** =
plausible, not load-bearing, no action may rest on it.

---

## 0. Headlines

1. **FAM/SLM is not a "person-name layer" — it is the ADVISOR-RELATIONSHIP layer.** Casebook Entry 1's
   framing ("person-name layer from FAM/SLM") is **REFUTED from the bytes** on the holder-name axis and
   **replaced with something more valuable**: per account, FAM carries the **FA-master grouping key
   (col_1), the rep name (col_3), the managing institution (col_2), and a household-level grouping id
   (col_6)** — the advisor-side identity W4 had marked "no parsed match — SOFT." Holder names add
   nothing over `acc` (col_5 is the account title, byte-redundant).
2. **The FAM col_1=`8242234` group (7,053 rows) is EXACTLY the 0824∩0833 account overlap — set-equal,
   symmetric difference 0 [MEASURED].** The two masters share 7,053 of their accounts (0833: 7,146,
   0824: 7,073 @ 20260713). The never-summed identity now has its account-level MECHANISM on the
   record: the books are two custody views over substantially one client population. Recorded as
   identity, per standing rule — no combined total computed, none implied.
3. **The Group-A join key is settled from the bytes:** `acc.account_id` is 10-digit, zero-padded,
   unique per partition [MEASURED 7,146/7,146]. FAM keys 8-digit (space-padded 9 in raw bytes), SLM
   9-digit (zero-padded) — zero-strip normalization joins **7,093/7,093 FAM rows into acc (100.0%)**.
   The zfill(10) rule 0.5.0 measured at 96.4% from the SmartX side is confirmed structurally from the
   acc side.
4. **FAM and SLM are content-identical [MEASURED]:** all five non-key columns identical on all 7,093
   common keys; deltas = padding convention + 1 near-blank SLM row. Two files, one table — and the
   **FAM==SLM cross-file identity is a free, real control** for a feed that has no T1 trailer.

## (a) The Group-A table set 0833 actually supports

| silver (fact_, per v0.4 naming) | gold projection it feeds | verdict |
|---|---|---|
| `fact_acc` (90 cols, grain=account [MEASURED unique 7,146/7,146]) | `dim_account` (casebook Entry 1) | **PRIMARY — confirmed from bytes** (§b1) |
| `fact_fam` + `fact_slm` (6 positional cols each) | the advisor-relationship + household columns of `dim_account`; a `dim_relationship` input | **UPGRADED** — advisor-side identity layer [PRESUMED semantics, MEASURED structure] |
| `fact_rps_s2` (34 cols, grain=account, rows==acc rows [M2]) | account balance dim/fact (A/B seam) | supported; converts as its own table (dictionary binding call) |
| `fact_sec` (69 cols, grain=security) | `dim_asset` | supported (Group B-adjacent dim; no Group-A blocker) |
| — nothing else — | | the other 14 types are B/C facts (events/lots/positions) or reader-variance backlog; no additional Group-A content found in the 18-type census [M2] |

## (b) Per-table: source columns → flow, grain, controls, freshness

### b1. `fact_acc` → `dim_account` [M1 unless noted]

- **Identity/entity:** `account_id` (10-digit zero-padded string — NEVER Int64), `mstracct_number`
  (single value `0008335338` — the master, constant), `account_title_line_1..3` (title 100.0%
  populated), `taxpayer_{first,middle,last}_name` (**6,729/7,146 = 94.2% — exactly the IND count**;
  taxpayer names are an IND-only field), `organization_primary_name` (**417/7,146 = 5.8% — exactly
  TRUST 260 + ORG 157**), `custtype_code` (IND/TRUST/ORG), `acct_regis` (CO/RH/RO/IN/JT/... 10+ codes),
  `primary_contact` (99.0%, 4,025 distinct — client-side contact, not a rep), `alias_name` (18.4%).
- **Status/dates:** `account_status` **O=7,062 / C=84 [MEASURED]** — closure is a STATUS FACT, exactly
  as Entry 1 R2 claimed; now byte-confirmed. `date_opened` 100.0% (min `19920123`, max `20260713`) —
  custodian-carried start date exists; Entry 1's "first-seen fallback" is the fallback, not the norm.
  `date_of_birth` 99.0%. `ssn_tin_number` **0.0% populated** — masked out of CRS delivery (but see
  col_6, §b2/§d).
- **Managed-program (the D2 seam columns):** `managed_account_money_manager` 6,936/7,146 = 97.1%
  populated — `SmartX Advisory Solutions` **6,930**, `Opal Capital LLC` 4, `PIMCO` 2;
  `managed_account_investment_strategy` (9 distinct; `SMArtX - All Cap Strategy` 6,924);
  `mngdacct_pltfrmcd` = `MAM` wherever populated.
- **Address:** city/state/zip ~100% — the passthrough requirement (lossy-ACC scar) is satisfiable.
- **Flow:** bronze zip-in-zip → `fact_acc` passthrough-complete parquet (pinned schema, T1-tied,
  dedup+dtype only) → gold `dim_account` daily snapshot upsert per Entry 1. **Grain: account.**
- **Controls:** T1 reconciliation (hard-raise, exercised on every parse this analysis ran) · row-count
  vs prior partition drift guard (converter framework) · at gold: the Entry-1 guards stand as written.
- **Freshness:** daily; rides the scheduled REST pull (0833 09:45Z / 0824 10:15Z, both exercised, run
  manifests measured under `_ops/daily_pull/runs/`), windowed to the trading frontier (manifest
  `trading_frontier=2026-07-13` on the 07-14 run — NEVER#1-correct by construction).

### b2. `fact_fam` / `fact_slm` → the advisor-relationship + household layer [M1]

- **Measured structure (mechanical col_1..col_6, naming ruled):**
  - `col_1` — 7-digit, 19 distinct over 7,093 rows. **[MEASURED] the `8242234` group == the 0824∩0833
    account overlap set exactly** (7,053 rows, sym-diff 0); a second 49F group `8403355` (18 rows,
    institution `49 FINANCIAL`); the 17 remaining groups are 1–3-account stragglers under
    trustee/recordkeeper institutions (Schwab Trust Bank, T. Rowe Price, Ascensus, Hewitt, Standard).
    **[PRESUMED] col_1 = the FA-master / relationship-master account number** (FAM ≈ "financial
    advisor master"). This makes col_1 the **cross-master bridge column** — the only place the
    0824↔0833 relation is written in bytes we hold.
  - `col_2` — institution name, varies BY col_1 group [MEASURED]: `49 WEALTH MANAGEMENT LLC` 7,055 +
    `49 FINANCIAL` 18 = 99.7% under the two 49F entities. **[PRESUMED] the managing/advisory
    institution of the relationship** — the bytes now lean advisor-firm, against the W4 open question
    (custodian names appear only on the 17 straggler groups, which look like external
    trustee/recordkeeper arrangements). Still awaits the spec for the label.
  - `col_3` — **9 distinct rep-shaped names** (20-char truncated); **0.6% surname collision with
    holder names** [MEASURED 41/6,675] and populated on TRUST/ORG rows where no taxpayer name exists
    (417/417) → **NOT the account holder. [PRESUMED] the rep/advisor of record** (1:1 with col_1
    groups; 19 (col_1,col_3) pairs).
  - `col_4` — the Schwab account number. FAM raw width 9 space-padded / SLM zero-padded [MEASURED on
    raw bytes]; zero-strip → **joins acc 7,093/7,093 (100.0%)**; unique per file (grain=account).
  - `col_5` — **the account title: 7,093/7,093 prefix-match vs `acc.account_title_line_1`
    [MEASURED]** (30-char truncated). Redundant with acc — and therefore a per-row cross-file
    consistency control, free.
  - `col_6` — 9-digit id, 4,190 distinct; accounts-per-value 1–10 with one 69-account entity cluster
    (all one title) [MEASURED]. **[PRESUMED] a household/tax-entity-level grouping id — plausibly the
    TIN** (9 digits; `acc.ssn_tin_number` is delivered masked). **Treated as SENSITIVE pending the
    spec** — see §d.
- **Flow:** bronze CS zip → `fact_fam` / `fact_slm` passthrough parquet (CS path landed @ `bc4110283`;
  every row `UNVERIFIED_BY_T1` per contract rider) → gold: `dim_account` gains
  fa_master/rep/institution/household columns [PRESUMED names await spec]; `col_6` seeds the
  `dim_relationship` household reconstruction as a CANDIDATE grouping key (vs. the title/address
  heuristics the canonical seed uses — strictly stronger if the spec confirms it).
- **Controls (no T1 exists — three real substitutes, all exercised in this analysis):**
  (1) uniform width 6/6 every row (reader hard-raise); (2) **FAM==SLM cross-file identity** — content
  equality on all shared keys (any divergence beyond padding = a vendor-drift finding, converts to a
  guard cheaply); (3) **join-coverage vs `fact_acc`** — FAM keys ⊆ acc ids held at 100.0% @ 20260713;
  a drop below ~99% flags. These belong in the converter/A_00 guard set.
- **Coverage [MEASURED]:** FAM covers 7,061/7,062 open accounts (the 1 miss: a SIMPL IRA opened
  2023-06-15, money_manager blank) + 32/84 closed; the 53 acc-not-in-FAM rows are 52 old closures
  (opened 2022-12-30..2023-11-14) + that 1 open. **A_00 law: unmatched rows are REPORTED with count,
  never dropped** (same rule as D1's bridge).
- **Freshness:** daily CS file (`CS071326` = 2026-07-13), same delivery as the CRS types.

### b3. `fact_rps_s2` (account balance) [M2]

34 cols, grain=account (7,144 @ 20260710 == acc row count that day); identity echo (account_id, title,
regis, type) + balance fields (`net_credit_debit`, `cash_balance_settled_only`, `mkt_value_long/short`,
`eqty_*`, margin fields, `bank_sweep_ibf`, `bank_cash`). Converts as its OWN table (the silent-drop
scar); T1-tied via the parent file. Gold: the A/B balance seam — `dim_account` does NOT absorb balances
(they are facts, daily grain); A_00 may echo nothing from it. Daily cadence.

### b4. Freshness law for all of Group A

Per-type floors bind history questions: `acc`/`rps`/`trn`/U-series/`fam`/`slm` begin **2024-07-08**;
`rld`/`tcf` reach 2023-07-12; the 257 pre-floor objects are the separate Glacier leg [M2 + landing
facts @ `adea13886`]. `rlu`/`rtu` monthly, `rly`/`rty` quarterly — absence at daily grain is cadence,
not staleness (NEVER#1 discipline).

## (c) The SEAMS to D1 and D2 — key columns, from the bytes

- **Spine key (both dims):** `acc.account_id`, 10-digit zero-padded string [MEASURED]. Everything
  joins the spine by zero-strip (or equivalently zfill(10)) normalization: FAM 8-digit space-padded,
  SLM 9-digit zero-padded, SmartX `account_number` 8-digit (HAR `26881039`).
- **D2 (SmartX model dim):** join `allocation_account_map.account_number.zfill(10) == acc.account_id`
  — 0.5.0's 96.4% measurement is now structurally confirmed from the acc side; the residual re-measure
  should run against a FRESH `fact_acc` partition (his banked plan) and the residual will include the
  210 money_manager-blank accounts [MEASURED] that are presumably outside the managed book.
  **Reconciliation edges [MEASURED]:** `managed_account_money_manager` (`SmartX Advisory Solutions`
  6,930), `managed_account_investment_strategy`, `mngdacct_pltfrmcd=MAM` — and the FAM
  col_1=`8242234` membership (== the 0824 overlap), which should approximate join-dim-1's covered set:
  **a three-way coverage triangle (acc marker × join-dim-1 membership × FAM group) that flags
  asymmetries in either dim, free.**
- **D1 (BD advisor/fee dim):** the 0833-side key is `acc.account_id`; DS's xref bridges it to
  `bd_account_id`/`bd_account_number`. **Bridge denominator [MEASURED @ 20260713]: 7,146** (per D1's
  AC: "the full 0833 account universe of that day"). **New cross-check edge from this analysis:** FAM
  col_3 (rep, 9 names) vs the BD architect/rep roles — name-grain, 20-char truncated, so a CONTROL
  (flag disagreement counts), never a key. And per-account FAM coverage (100% of open accounts but
  ONE) means D1 can also cross-check its own unbridged report against FAM membership.
- **Cross-master identity (feeds the D1-D4 convergence):** 0833∩0824 = 7,053 accounts [MEASURED],
  written in bytes as FAM col_1. Whatever the §4 architecture does with 0824 later, the runner's
  0833 spine already CONTAINS the overlap population; the never-summed rule stays load-bearing at
  gold exactly as at bronze.

## (d) Gaps, three ways

**Needs the vendor FAM/SLM spec (unchanged owner: Andrew/0.6.2 to source):**
1. Column names/semantics for col_1/col_2/col_3/col_6 — the [PRESUMED] labels above are structural
   presumptions, not names. Mechanical col_1..col_6 ships meanwhile (ruled).
2. Whether the spec carries a row-count/control field (W4 §8 standing note) — if not, the FAM==SLM
   identity + acc-join-coverage controls (§b2) are the permanent substitutes.
3. Whether FAM vs SLM are DEFINED to be identical (two views of one table) or can legitimately
   diverge — determines whether the identity check is a hard guard or a drift flag.

**Needs Andrew:**
4. Pre-floor history (PRD §5.2 — unchanged; default feed-floor start stands).
5. **col_6 sensitivity ruling:** if col_6 is the TIN, `fact_fam`/`fact_slm` carry a 9-digit tax id in
   silver under passthrough-complete law (acc's own `ssn_tin_number` arrives MASKED — the vendor
   chose to mask one and not the other, if the presumption holds). Passthrough says keep bytes;
   serving/exposure policy is a sovereign/CTO call. Flagged, not adjudicated.
6. Advisor-"type" semantics (PRD §5.1 — unchanged; FAM col_3 gives rep NAME, still not a "type").

**Buildable now (no external dependency):**
7. `fact_acc`, `fact_fam`, `fact_slm`, `fact_rps`+`fact_rps_s2` converters — readers landed
   (`bc4110283`), framework routes all of them; remaining V2-8 deltas are schemas/manifest/guard/
   packaging (in flight under the existing GO).
8. The A_00 script itself, fixture-tested against the W4-measured shapes (casebook Entry 1's own
   note: none of the build gates block WRITING the script).

## (e) Converter build order → unblock A_00

A_00's dictionary-row inputs are `fact_acc` + `fact_fam`/`fact_slm` (+ join dims outside my lane).
Order that unblocks it fastest, schema-pinning in the same sequence:

1. **`fact_acc`** — the spine; A_00's primary input; also D1's bridge denominator + D2's residual
   re-measure both WANT a fresh fact_acc partition (two downstream lanes unblocked by one table).
2. **`fact_fam` + `fact_slm`** — CS path already landed; wiring + schema only. With (1), the whole
   §b2 control triangle becomes exercisable.
3. **`fact_rps` + `fact_rps_s2`** — same file, one converter pass; opens the B_00 valuation seam
   (casebook next entries) and the balance facts.
4. `fact_sec`, `fact_trn` — dim_asset + the event spine.
5. The lot family (`uln`/`ult`/`rld`/`rlu`/`rly`/`rtu`/`rty`/`upn`/`upt`) — B_02/C tier.
6. Reader-variance backlog (`tcf`/`tcfx`/`tnn`) — no A_00 dependency; tcf matters later for deepest
   history (2023-07 floor).

All under the ruled gates (nothing here changes them): V2-7 container apply (CTO), converter
code-review (CTO), first-conversion signoff (AC-3), DS same-day diff review, `fact_{type}` naming
(AMENDMENT-3; silver_key one-place change landing with DS).

## Casebook Entry 1 — filled and amended (the commissioned verdict)

**CONFIRMED from bytes:** `acc` is a daily full account file including closed accounts (84 C rows
present) · closure is a status fact · registration/address/entity columns all populated at the rates
in §b1 · `date_opened` is custodian-carried at 100% · the daily-snapshot-upsert design is sound on
this grain (account_id unique per partition).

**AMENDED:** the "FAM/SLM person-name layer" input line should read **"FAM/SLM advisor-relationship
layer"** — it contributes fa_master/institution/rep/household columns [PRESUMED names], NOT holder
names (holder identity is complete in `acc`: taxpayer names for IND, organization_primary_name for
TRUST/ORG, title lines for all). col_6 is a candidate household key for the dim_relationship
derivation, pending spec. The §b2 controls (FAM==SLM identity, acc-join coverage) belong in A_00's
guard list alongside the Entry-1 guards.

---

*Read-only: no writes to any bucket, no converter run, no registry edit. Every count above is
enumerated (denominator printed at run time in `d3_measure*.py`); nothing sampled. Reserved words
used only on source-confirmed claims.*
