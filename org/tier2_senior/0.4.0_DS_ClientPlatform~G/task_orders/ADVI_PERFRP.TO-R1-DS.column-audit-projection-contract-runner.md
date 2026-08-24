# TO ADVI_PERFRP.TO-R1-DS — round 1, DS lane: the COLUMN AUDIT · the PER-CLIENT PROJECTION CONTRACT (the join) · the projection runner B3–B7 · the emitter half of the key family

<task_order id="ADVI_PERFRP.TO-R1-DS" project="ADVI_PERFRP">
<decomp_ref>workflows/atom_decomposition/runs/advi-perfrp/20260824T201222Z/DECOMP.md @1ce9b2d6bc — cells PRF-a-1, PRF-a-2, PRF-a-3, PRF-a-4, PRF-a-5, PRF-a-6, PRF-b-1, PRF-b-2, PRF-b-3, PRF-b-4, PRF-b-5, PRF-b-6, PRF-b-7, PRF-c-1 (emitter half), PRF-inv-2 (producer half), PRF-inv-3 (producer half), PRF-inv-5 (argument contract), PRF-inv-6.</decomp_ref>
<!-- ISSUER FIX 2026-08-24 ~22:4xZ on 0.7.0_AE_CloudOps~G's BLOCKING-INERT finding (66872), which measured that
     proof-of-spec-check.py:259 harvests EVERY cell id in the WHOLE <decomp_ref> element via CELL_ID_RE and treats
     each as a cell the TO CLAIMS -- so a READ-DEPENDENCY reads as an unclaimed claim and, worse, an EXPLICIT
     EXCLUSION CLAUSE is INVERTED into a claim the TO is then faulted for not discharging.
     THE FIX IS RELOCATION, NOT DELETION. Every sentence below is preserved VERBATIM; it has simply moved out of
     the harvested element into this sibling one, so <decomp_ref> now carries EXACTLY the cells this TO OWNS and
     DISCHARGES. Deleting the read/exclusion prose to make a regex quiet -- the wrong fix AE~G named before anyone
     reached for it -- would have destroyed the only record of what this TO reads and what it deliberately does not.
     The durable repair is the EXTRACTION (scope the harvest to the owned-cells clause), routed to CTO/the tooling
     lane; this element is forward-compatible with it. No acceptance row, criterion, cell_ref or attestation changed. -->
<decomp_context>Constrained by boundaries PRF-g-1..g-4 and the FIXED table (s.11 #1–#14). NOT in this TO: every PRF-d-* cell (TO-R1-DE), PRF-c-2/c-3 + the IAM halves (TO-R1-AE), PRF-e-1 / PRF-f-1 (CVO-owned).</decomp_context>

<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` cert @62598c1bfb (36/36; no P1; s.11 FIXED 14/14 covered). Q-p1/Q-p2/Q-p3 CONFIRMED by the PRD author (CTO 66460) and Q-p1 independently re-derived by CVO. If a surprise item returns DECOMP-INVALIDATING, the ISSUER re-derives these premises.</certification>
<issued_to>DS-class (gold producer, `data/assets/scripts/gold/runners_49f/**` under Rule 13). **SEATED: `0.4.0_DS_ClientPlatform~G` (MSTR 66575, spawned 2026-08-24 ~21:0xZ, ADVI_PERFRP ONLY).** ONE PROJECT PER INSTANCE (@b705331f7d).</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>Spawn call routed to MSTR same turn (66493). Start = SEATED: the live canonical plane exists (P1); first act = `PRF-a-1`. Dark mid-execution → MSTR same turn.</seating_trigger>
<placement>LAPTOP (Rule 26; D2 is laptop-ruled). Nothing ferried.</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-24T20:3xZ</issued>
<status>ACTIVE</status>
<priority>P1 — the PURPOSE project of the 49F sub-program (finding 3); wave-2 first in CTO's dispatch order (PERFRP → INSURE → STITCH-A).</priority>
<scope_guard>ONE PROJECT. Exactly the cells above. ⛔ **Do NOT build the plan's ~50-column `fact_account_return_daily`** (CTO ruling Q-p1: YAGNI; it would build ADVI_PERFORMANCE's unbuilt Phase-2 table inside PERFRP). ⛔ **Do NOT disambiguate / schedule the `account_gains / account_performance / client_performance` wrapper trio** (Q-p2: off this path). ⛔ **Do NOT brief the plan's author** — the `ADVI_PERFORMANCE_E2E_STANDARDIZATION_PLAN_20260806.md` is REUSED AS AN ARTIFACT; any method extension you need (netting rule, new/lost definition, the residual identity) is drafted by you and RULED by CTO, certified by CVO (s.11 #13). Surprises → `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/ADVI_PERFRP/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580), one line, keep working. **Nothing to `4.0.0_SA_CRO*` this session.**</scope_guard>
<authority>PRD `docs/architecture/ADVI_PERFRP_PRD.md` v0.3 s.4 / s.6 / s.8 / **s.11 (rulings, FIXED)** / s.12 (partner bindings) + s.13 premise correction (CTO, on Q-p1) + run P1–P16. Andrew-direct finding 3 (verbatim, PRD s.0) + "approved all" (~18:5xZ).</authority>
<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json PRFR1DS-AC1,...,PRFR1DS-AC14 ; check the rc. -->
    <criterion id="PRFR1DS-AC1" cell_refs="PRF-a-1"/>
    <criterion id="PRFR1DS-AC2" cell_refs="PRF-b-1"/>
    <criterion id="PRFR1DS-AC3" cell_refs="PRF-a-2"/>
    <criterion id="PRFR1DS-AC4" cell_refs="PRF-a-3"/>
    <criterion id="PRFR1DS-AC5" cell_refs="PRF-a-4, PRF-b-4"/>
    <criterion id="PRFR1DS-AC6" cell_refs="PRF-a-5, PRF-b-6"/>
    <criterion id="PRFR1DS-AC7" cell_refs="PRF-a-6"/>
    <criterion id="PRFR1DS-AC8" cell_refs="PRF-b-2, PRF-inv-6"/>
    <criterion id="PRFR1DS-AC9" cell_refs="PRF-b-3"/>
    <criterion id="PRFR1DS-AC10" cell_refs="PRF-b-5"/>
    <criterion id="PRFR1DS-AC11" cell_refs="PRF-b-7, PRF-inv-3"/>
    <criterion id="PRFR1DS-AC12" cell_refs="PRF-inv-5"/>
    <criterion id="PRFR1DS-AC13" cell_refs="PRF-c-1, PRF-inv-2"/>
    <criterion id="PRFR1DS-AC14" cell_refs="PRF-b-1"/>
  <expected_criteria>PRFR1DS-AC1,PRFR1DS-AC2,PRFR1DS-AC3,PRFR1DS-AC4,PRFR1DS-AC5,PRFR1DS-AC6,PRFR1DS-AC7,PRFR1DS-AC8,PRFR1DS-AC9,PRFR1DS-AC10,PRFR1DS-AC11,PRFR1DS-AC12,PRFR1DS-AC13,PRFR1DS-AC14</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~G/deliverables/ADVI_PERFRP.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells in this TO: 18 (a-1..a-6, b-1..b-7, c-1, inv-2, inv-3, inv-5, inv-6); criteria: 14; every criterion ≥1 cell_ref; every cell reachable (a-1 AC1 · a-2 AC3 · a-3 AC4 · a-4 AC5 · a-5 AC6 · a-6 AC7 · b-1 AC2/AC14 · b-2 AC8 · b-3 AC9 · b-4 AC5 · b-5 AC10 · b-6 AC6 · b-7 AC11 · c-1 AC13 · inv-2 AC13 · inv-3 AC11 · inv-5 AC12 · inv-6 AC8). Unmapped 0; untraceable 0.</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP — YOUR FIRST ACT

| # | Premise | Oracle that would FALSIFY it |
|---|---|---|
| O-1 | The live canonical plane = 8 tables; `fact_account_return_daily` and `twr_periods` ABSENT | `aws s3 ls s3://opal-data-49financial/gold/advi/canonical/` `# rail-checked: presence census for TO-R1-DS O-1` → 8 prefixes, neither name present |
| O-2 | `twr_daily` = 9 columns (`r_net`, `r_gross` + provenance) | one-partition schema read (latest `date=`) via pyarrow |
| O-3 | The gains trio lands NOWHERE (excluded by determination) | `sed -n 44,52p data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py` + `aws s3 ls .../gold/advi/` `# rail-checked` → 4 prefixes, none for the trio |
| O-4 | Schwab silver lots + txn tables PRESENT (names only) | `aws s3 ls s3://opal-data-assets/schwab/08335338/silver/` `# rail-checked` → fact_uln/ult/upn/upt/rld/trn 6/6 |
| O-5 | ⛔ **CORRECTED (AE~G 66679): NOT 11.** The publisher's pre-state is **12 emitter entries / 15 EMIT twin objects / 10 live objects**; the three grains are distinct and the criterion is baselined on the DERIVED line, not a literal | `grep -c '"script":'` (=12, ENTRIES) **AND** `d_publisher_port.py:566-568`'s printed derived denominator (twins + entries) — quote both, never one as the other |
| O-6 | `dim_account` (a00) holds Schwab-08335338 accounts ONLY; `dim_account_xref` exists BD-side | a00 partition read + the xref's home per STITCH s.11 #2 |

## THE DECISION YOU EXECUTE (decomp s.2.0; CTO-confirmed Q-p1; CVO re-derived)

The projection **CONSUMES THE LIVE CANONICAL TABLES** joined at `(account_id, business_date)` — `canonical_valuation` (value/accrual), `flow_ledger` classes (EXTERNAL · INTERNAL · FEE-MANAGEMENT · FEE-ADMIN → contributions / withdrawals / fees / intra-relationship transfers), `nna_canonical` (headline NNA), `twr_daily` (`r_net` served, `r_gross` stored) — and **IMPORTS** the existing pure cores (`c03_nna.build_nna_atomic`, `c00_account_gains.SB_INCOME` / the identity) for income and the residual market gain. **Every plan column with no live source is DECLARED ABSENT in the contract, listed against the contract version — never silently filled.**

## Cells

- **`PRF-a-1` COLUMN AUDIT (first act):** the plan's 8 column groups (`ADVI_PERFORMANCE_E2E_STANDARDIZATION_PLAN_20260806.md:172-198`) → live source or DECLARED-ABSENT. Print: plan columns N / mapped M / absent K, **N = M + K**. This table is `b-1`'s input and the contract's absent-list.
- **`PRF-b-1` THE CONTRACT (the join DE builds against):** level tree {relationship → account → class} × periods **{QTD, YTD, 1Y, 3Y, SI, custom(start,end)}** (R-p1; as-of default T-1) × the s.6.4 figure set under our names, with `heldEntirePeriod / daysHeld / returnsAnnualized`; intra-relationship netting from `flow_ledger` INTERNAL; **SI = from the Schwab floor, labelled "since 2024-07-08"** (s.11 #10). ⛔ **The contract carries a `contract_version`, and every DECLARED-ABSENT column is listed against it** (CTO ruling 66489 on CVO's seam — DE's renderer asserts the version it built against). Commit the contract SKELETON first (the DE lane's start condition is that OBSERVED commit), then the emitter.
- **`PRF-a-2`** the gains identity `d_aua == nna + income − fees_tax + market_growth` asserted **to the cent on your own output** per account-window; cores IMPORTED, never copied (Build Ladder rung 2; the estate's copied-taxonomy drift is a named defect class).
- **`PRF-a-3`** classification coverage: `dim_asset_classification` (a07) × `canonical_positions` — print positions MV total / classified / residue; **the residue is NAMED** ("To Be Classified"-class), never folded.
- **`PRF-a-4` → `PRF-b-4` GAIN/LOSS, LAST (s.11 #5):** census the six silver tables FIRST (partition coverage, date range, row counts, columns; the lots→positions MV tie-out with its residual printed), THEN the lots projection (unrealized ST/LT, realized, cost basis).
- **`PRF-a-5` + `PRF-b-6`** Book membership = the D contract's TAGGED-BOOK view (an account once per advisor; NON-ADDITIVE across roles — plan s.3.4; R-p5) — the same set `d07 leaderboard` publishes for that advisor+window; the four KPIs (Market Value; Management Fees = FEE-MANAGEMENT; Relationships new/lost from a01 first/last-seen in window; Net Flows in/out/net split new/lost/existing) + the client table, as rollups of `b-1`.
- **`PRF-a-6`** roster completeness: a00 ∪ `dim_account_xref` → accounts in xref-not-a00 emit as **known-not-held with custodian** (Fidelity / position-only), never omitted, never zeroed (Q-p3: a JOIN, not a classification). Print a00 / xref / xref-not-a00 counts.
- **`PRF-b-2` + `PRF-inv-6`** performance series: geometric link of `r_net` (served) / `r_gross` (stored); UNCOMPUTABLE subperiods propagate as flags, never zeros; **served window % == Π(1+r_net)−1 over `twr_daily`; a summed-return mutant FAILS the check.**
- **`PRF-b-3`** allocation snapshot + drift by class with `allocationOfTotal / allocationOfParent`; Σ class MV == level MV; drift(as-of, as-of) == 0.
- **`PRF-b-5`** transactions: `fact_trn` + `a05_ref_txn_classification` → a **PER-RELATIONSHIP, PAGED key**; a request without a relationship key **REFUSES**; `hasMoreResults` present; type filter is client-side (s.11 #6).
- **`PRF-b-7` + `PRF-inv-3`** the windowed rollup law (plan s.3.4: parent `$` = Σ child `$`, parent denominator = Σ child denominators, window % geometric) implemented **ONCE** as one shared function used at every level and by `b-6`; `comp-find` shows one definition; recompute relationship→account on your own output and print. **Never advisor→firm** (R-p5).
- **`PRF-inv-5` (argument contract)** `firm` is a REQUIRED argument with NO default; no-firm invocation → REFUSE rc≠0; reads only its own firm's trees, writes only its own firm's keys (the IAM half is TO-R1-AE's).
- **`PRF-c-1` (emitter half) + `PRF-inv-2`** each served leaf is an emitter script registered as an `EMITTERS` entry in `d_publisher_port.py` (the AE lane wires the publisher/IAM half); **never-blend**: a fixture relationship carrying one `ADVI_INSURE` row yields byte-equal PERFRP figures with and without it (CVO owns the standing control; you exercise it once here).

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **PRFR1DS-AC1** | Column audit printed: plan N / mapped M / absent K, N = M + K; sources named per column | PRF-a-1 | LIVE STATE |
| **PRFR1DS-AC2** | Contract committed (skeleton first, then full) with `contract_version`, the absent-column list against it, R-p1 periods, the SI label, netting rule stated; `proof-of-spec` positional ids | PRF-b-1 | SOURCE |
| **PRFR1DS-AC3** | Gains identity asserted to the cent on the projection's output; cores IMPORTED (grep shows imports, no copied bodies) | PRF-a-2 | EXERCISED |
| **PRFR1DS-AC4** | Classification coverage printed (total / classified / residue) with the residue NAMED | PRF-a-3 | LIVE STATE |
| **PRFR1DS-AC5** | Six-table census printed BEFORE the lots projection; lots→positions tie-out with residual; Gain/Loss delivered LAST | PRF-a-4, PRF-b-4 | LIVE STATE + EXERCISED |
| **PRFR1DS-AC6** | Book view relationship set == leaderboard set for a sampled advisor+window; four KPIs + client table emitted as rollups of b-1 | PRF-a-5, PRF-b-6 | EXERCISED |
| **PRFR1DS-AC7** | Roster counts printed (a00 / xref / xref-not-a00); known-not-held rows emitted with custodian, never zero | PRF-a-6 | EXERCISED |
| **PRFR1DS-AC8** | Served window % == Π(1+r_net)−1; gross stored; zero-BMV fixture renders the flag; the summed-return mutant FAILS | PRF-b-2, PRF-inv-6 | EXERCISED (mutant) |
| **PRFR1DS-AC9** | Σ class MV == level MV; drift(as-of, as-of) == 0 | PRF-b-3 | EXERCISED |
| **PRFR1DS-AC10** | Per-relationship paged key; no-key request REFUSES; `hasMoreResults` present | PRF-b-5 | EXERCISED |
| **PRFR1DS-AC11** | ONE rollup function (comp-find: one definition); relationship→account recompute printed; advisor→firm NEVER computed | PRF-b-7, PRF-inv-3 | SOURCE + EXERCISED |
| **PRFR1DS-AC12** | No-firm invocation REFUSES rc≠0; firm-pinned reads/writes only (path census printed) | PRF-inv-5 | EXERCISED |
| **PRFR1DS-AC13** | ⛔ **DENOMINATOR CORRECTED 2026-08-24 ~21:5xZ on `0.7.0_AE_CloudOps~G`'s finding (66679) — "11 + N" WAS STALE AND WOULD HAVE PASSED A MECHANICAL CHECK WHILE BEING FALSE.** Measured pre-state: **12 emitter ENTRIES / 15 EMIT TWIN OBJECTS / 10 LIVE objects** — three grains, and the old wording mixed them (its named oracle `grep -c '"script":'` counts ENTRIES while the criterion said TWINS: Rule 24(ii), two grains on one axis). **Baseline on the publisher's OWN derived denominator, `d_publisher_port.py:566-568`, which is computed from the dict and cannot go stale — print it before and after and name your N new leaves.** Plus: never-blend fixture byte-equal | PRF-c-1, PRF-inv-2 | EXERCISED |
| **PRFR1DS-AC14** | `comp-pipescript io <script> --pipeline bd` on each new script; commit-gate PASS; Rule 15; `safe-commit.sh` under your author line; proof instance VALID rc=0 positional | PRF-b-1 | SOURCE |

## CVO-owned commitments recorded here (NOT this lane's): `PRF-e-1` the parity harness on `b-1`'s FIRST emission (report rides the DEV render, no gate); `PRF-f-1` the HAR/PII repo control; the standing `inv-2` control. You trigger them by reporting the first emission to CVO.

## Law that binds
Rule 13 (DS lane, `safe-deploy` gate; the deploy home is the bd tree — `comp-pipescript deployed`) · 14/14a · 15 · 17 (silver untouched) · NEVER#1 (T-1, trading calendar) · **no alerts/monitors** · **no shadow paths** · Build Ladder rung 2 (the cores, the crosswalk, the publisher mechanism, the plan as artifact) · no non-ASCII on AWS.

## Status + reporting
Cell-level `<cell_status>` on this file; proof instance + flip = one commit. Report to COO at each flip (hash + push state, never bare "landed"); cc `3.0.0_SA_CVO` at AC2 (the contract) and at the FIRST EMISSION (their harness fires on it); cc the DE and AE PERFRP lanes at AC2 (their start conditions). Surprises: `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/ADVI_PERFRP/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580).
