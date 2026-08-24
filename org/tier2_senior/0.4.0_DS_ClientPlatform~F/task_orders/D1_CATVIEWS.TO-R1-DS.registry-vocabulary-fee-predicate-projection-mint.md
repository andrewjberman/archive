# TO D1_CATVIEWS.TO-R1-DS — round 1, DS lane: the registry VOCABULARY (view tree) · the per-firm FEE PREDICATE · the `category_views` PROJECTION MINT · producer RESOLUTION · the Cottonwood DONE row

<task_order id="D1_CATVIEWS.TO-R1-DS" project="D1_CATVIEWS">
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md @469a9e9868 (+ s.4a post-cert amendment) — cells D1-h-r1, D1-h-r2, D1-h-r3, D1-h-r4, D1-h-c1, D1-h-c2, D1-h-c3, D1-h-p2, D1-b-1, D1-d-1, D1-e-1, D1-e-2, D1-e-3, D1-inv-1, D1-inv-2, D1-inv-3, D1-inv-4 (emit half), D1-a-1 (the BUILT registry module -- DISCHARGED here by AC1's self_test + F5 mutants, so it is DECLARED rather than merely read)</decomp_ref>
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
<decomp_context>(D1-a-1 moved into the owned clause above: a criterion discharges it, so declaring it as a mere read would understate what this TO is accountable for.) Constrained by boundaries D1-g-1, D1-g-2. NOT in this TO: D1-f-1 (the 15/85 node — CTO remit), every D1-h-v*/D1-h-p1/D1-c-* cell (the DE lane's TO-R1-DE).</decomp_context>

<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` cert @60d4e2f1b4 (28/28 declared = mentioned, both differences empty; NOT-YET-EVALUABLE criteria→cells recorded as its own state). One P1 sizing correction (r4) is absorbed in the decomp's s.4a and in Half 1 below. If a surprise item returns DECOMP-INVALIDATING, the ISSUER re-derives these premises — the executing seat does not adjudicate that.</certification>
<issued_to>DS-class (data plane / gold producer, `data/mdpf/**` under Rule 13). **SEATED: `0.4.0_DS_ClientPlatform~F` (MSTR 66470, spawned 2026-08-24 ~20:24Z, D1_CATVIEWS ONLY).** ONE PROJECT PER INSTANCE (Andrew-direct @b705331f7d): this lane holds no other pipeline project's TOs.</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>Spawn call routed to MSTR SAME-TURN as the cut (66463). Start condition = SEATED (the registry module is BUILT; nothing here waits on another lane). If this class goes dark mid-execution the spawn call re-routes to MSTR same turn — a naming obligation, not a discovery.</seating_trigger>
<placement>LAPTOP (Rule 26; D1 is laptop-ruled). Every apply/deploy in this TO runs on THIS device under the normal wrappers — nothing ferried.</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-24T20:2xZ</issued>
<status>ACTIVE</status>
<priority>P1 — Andrew's "beeline" (2026-08-24 ~12:4xZ) + the Monday push order: D1 is IMMEDIATE TERM (Cottonwood's Opal-Advised assets untracked → Global held up by proxy). Front of this lane's queue — it IS this lane's queue.</priority>
<scope_guard>ONE PROJECT. This TO qualifies EXACTLY the cells in `<decomp_ref>` and nothing else — no D3, no ETFS, no MDPF backlog, no base-seat heap. Anything adjacent that looks worth doing: ONE LINE to CVO's channel (`3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/D1_CATVIEWS/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580)), no action, keep working. Class {OBSERVATION, BLOCKING} × standing {ARMED, INERT}; only BLOCKING routes to the issuer same turn; ARMED names a disarm owner.</scope_guard>
<authority>PRD `docs/architecture/D1_ASSET_CATEGORY_VIEWS_PRD.md` s.8 (stage-2) + **s.8.6 (the view tree, Andrew-direct ~18:5xZ, verbatim in `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260824_D1_VIEW_TREE_L0_L1_L2_CLIENT_MODELS_SMAS_ALTERNATIVES.md`)** + run row RV1. The 08-19 taxonomy gate (`org/tier1_exec/1.0.0_SA_CTO/deliverables/D1_TAXONOMY_GATE_RULING_20260819.md`) is NOT re-opened (D1-g-1): the view tree is a DISPLAY axis over the same stored 5-enum.</authority>
<proof_of_spec>
  <!-- ISSUANCE half (COO): the criterion-id set, each with cell_refs -- CVO's alignment check is a JOIN on these.
       COMPLETION half (assignee): a schema-valid instance at instance_path, validated BEFORE any status flip.
       INVOCATION IS POSITIONAL (no --expected-criteria flag):
         python .tools/proof-of-spec-check.py <instance>.json D1R1DS-AC1,D1R1DS-AC2,D1R1DS-AC3,D1R1DS-AC4,D1R1DS-AC5,D1R1DS-AC6,D1R1DS-AC7,D1R1DS-AC8,D1R1DS-AC9
       CHECK THE RC (0 VALID / 1 INVALID / 2 usage), never the output string; the 2-arg form returns rc=0 with COVERAGE UNCHECKED -- pass the ids. -->
    <criterion id="D1R1DS-AC1" cell_refs="D1-h-r1, D1-a-1"/>
    <criterion id="D1R1DS-AC2" cell_refs="D1-h-r3"/>
    <criterion id="D1R1DS-AC3" cell_refs="D1-h-r4, D1-e-1, D1-e-2, D1-e-3, D1-inv-1"/>
    <criterion id="D1R1DS-AC4" cell_refs="D1-h-c1, D1-h-c2"/>
    <criterion id="D1R1DS-AC5" cell_refs="D1-h-r2"/>
    <criterion id="D1R1DS-AC6" cell_refs="D1-b-1, D1-h-c3, D1-inv-3"/>
    <criterion id="D1R1DS-AC7" cell_refs="D1-h-p2, D1-inv-2, D1-inv-4"/>
    <criterion id="D1R1DS-AC8" cell_refs="D1-d-1"/>
    <criterion id="D1R1DS-AC9" cell_refs="D1-b-1"/>
  <expected_criteria>D1R1DS-AC1,D1R1DS-AC2,D1R1DS-AC3,D1R1DS-AC4,D1R1DS-AC5,D1R1DS-AC6,D1R1DS-AC7,D1R1DS-AC8,D1R1DS-AC9</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~F/deliverables/D1_CATVIEWS.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells in this TO: 17 criterion-bearing (+ D1-a-1 as a read input); criteria: 9; every criterion carries ≥1 cell_ref; every one of the 17 cells is reachable from ≥1 criterion (r1 AC1 · r2 AC5 · r3 AC2 · r4 AC3 · c1/c2 AC4 · c3 AC6 · p2 AC7 · b-1 AC6/AC9 · d-1 AC8 · e-1/e-2/e-3 AC3 · inv-1 AC3 · inv-2 AC7 · inv-3 AC6 · inv-4 AC7). Unmapped cells: 0. Untraceable criteria: 0.</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP — YOUR FIRST ACT, BEFORE ANY BUILD

Run these live and put what they returned in your first report. **A TO can lie about its own state** (three same-day specimens on 08-21); re-grounding at pickup is the fix that worked every time.

| # | Premise this TO rests on | The oracle that would FALSIFY it |
|---|---|---|
| O-1 | The registry is BUILT: 14 members, 9 view nodes | `python data/mdpf/scripts/gold/mdpf_category_registry.py` → `DENOMINATOR: 9 declared view nodes`, 14 members |
| O-2 | `category_views` is a PURE MINT — nothing emits it | `comp-find -i category_views data/` → the single hit is the registry's doc comment (`mdpf_category_registry.py:45`) |
| O-3 | Cottonwood's fee flag is LIVE and THREE-valued | `sed -n 126,137p data/cot/scripts/gold/D_05.supervised_split.py` → `unflagged` bucket present |
| O-4 | Inflection has NO fee-taking flag under that token | `comp-find -i supervised data/inf` → 0 hits / 230 files (a TOKEN zero — your c2 census widens it) |
| O-5 | Insurance has ZERO registered members (the two planes coincide today) | `members_for('Insurance')` → `[]` |
| O-6 | "Opal Fixed Income" is a REAL live model on the BD/assets plane, absent from the MDPF registry | `sed -n 15,17p data/assets/scripts/gold/build_dim_model_portfolio.py` (present) AND `comp-find -i 'fixed income' data/mdpf` (0/60) |

## THE FINDING THAT SHAPES THIS TO (decomp s.2 — read it before you size anything)

**His Client L1 split ("Client Supervised / Client Unsupervised … solely a function of assets the advisors take fees on") is a per-ACCOUNT predicate. The Client node's substrate in the MDPF contract is a (firm × date) RESIDUAL** (`docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md:113-116`; `mdpf_aggregate_aua.py` docstring). **A per-account predicate cannot partition a firm-level residual.** So Halves 2–3 are not a rename of the Advised/Residual nodes — they require an ACCOUNT-GRAIN client feed per firm, and whether that exists is a per-firm fact you MEASURE (c1, c2), never assume.

## Half 1 — `D1-h-r1`, `D1-h-r3`, `D1-h-r4`: THE REGISTRY VOCABULARY (a DATA edit, never code)

- **r1** `VIEW_TREE` gains `Client > Supervised` and `Client > Unsupervised` (his labels, verbatim). `Insurance` **STAYS** in `VIEW_TREE` + `TOP_LEVEL_PEERS` (the gold plane partitions five ways) and gains a **view-plane exclusion flag** — a NEW field on that node, not a deletion. `self_test` prints 11 nodes; F5 still raises on a node outside the tree.
- **r3** SMA L1 nodes = SMA members carrying a `strategy_id`. Measured: `{divz, pfoe, muni, tax}` = **his four, verbatim**; `idvz` / `pfde` (`strategy_id` None — the RULED pending state from Q1) roll into the SMAs L0 total with NO L1 node. "Maybe others will eventually be added" = a registry row + a `strategy_id`, zero code. **Do not add nodes for idvz/pfde** — that question (Q-h1) is at Andrew via CTO; if he says six, it is two `strategy_id` registrations.
- **r4 (SIZING CORRECTED BY CVO P1 — decomp s.4a):** registry Custom = 3 members, **all `served=False`**, and his example *"Opal Fixed Income"* is absent from the MDPF registry — **but it IS a real, live Opal model on the BD/assets `dim_model_portfolio` plane** (`build_dim_model_portfolio.py:15-17`, diagnosed `0.7.0_AE_CloudOps~Z` @924c3b669). **Reconcile the Custom set against that in-estate authority NOW, through Half 4 (surface (e)) — do NOT wait on the per-Partner rulesets.** Every Opal model on `dim_model_portfolio` that is not Primary is a Custom member (registry edit, data-driven) or is explicitly excluded with the reason printed. The gap, if any remains, is DISCLOSED for the L2 panel, never padded.

## Half 2 — `D1-h-c1`, `D1-h-c2`, `D1-h-c3`: THE FEE-TAKING PREDICATE, PER FIRM (measure first)

- **c1** Account-grain client feed per firm — cot: EXISTS (`account_performance` + `accounts_dimension_latest`, read by `D_05`); 49F: BD `Account Supervised` at allocation grain (`bd49f_fact_allocation.py:112`) — **on the BD plane, not the SmartX MDPF plane** (`wsb_49f_smartx_model_aua.py`); the SmartX↔BD/Schwab account join is **D3's EXACT-JOIN precondition, not yours to build** — if 49F's split cannot be computed without it, print that and mark 49F's predicate `pending D3 join`; inf: UNMEASURED → your census. Print per firm: row count at account grain with a fee-flag column, or ABSENT.
- **c2** The predicate itself — cot: `account_supervised ∈ {Supervised, Unsupervised, unflagged}` (LIVE); 49F: `account_supervised` is a **SLEEVE** split (`bd49f_dim_portfolio_group.py:197` — one account can carry both sleeves; (account, sleeve) grain, aggregated up, printed); ⛔ **inf: DELIVERED AND CORRECTED BY YOU (66722) — NOT DARK.** `is_fee_earning` at ACCOUNT grain (`orion_billing_dim.py:14`; consumed `INF_D_00c:340,1431`), 911/911 accounts on the live 08-24 partition, TRUE 789 / FALSE 122, and the firm already splits fee_earning_aua / non_fee_earning_aua by it. The widened census resolved as **NOT A ZERO**; the two negative-fee refund accounts stay INSIDE Unsupervised per the firm's own ruled derivation — do NOT invent a third bucket inf does not have. The `ending_mv_status` axis you flagged (93 zero-contradicted-by-billing-activity) is NOT yours: surfaced, not chased.
- **c3 THE THIRD VALUE.** His L1 is two-valued; cot's flag is three-valued. `unflagged` is emitted as a THIRD, LABELLED bucket (label "Unflagged — not in the attributes pull"; Q-h3 lets him rename it), **never folded into either fee bucket and never dropped** — folding silently moves AUA across a fee line. Assert `supervised + unsupervised + unflagged == Client` per firm, to the cent, printed.

## Half 3 — `D1-h-r2` + `D1-b-1` + `D1-h-p2` + the emit-half of `D1-inv-2/3/4`: THE PROJECTION MINT

- **r2 DECISION RULE (fixed by the decomp; you MEASURE, you do not adjudicate):** per firm where the predicate exists, compare the fee-split partition of Client against the arithmetic Advised/Residual split. Print a table {equal / differs / predicate-absent} with row counts. **Equal on every firm → one axis, two names → RENAME** (Advised/Residual collapse into Supervised/Unsupervised). **Differs on any firm → two axes**: the VIEW renders fee-taking (his word binds the view); Advised/Residual stays a gold/registry axis NOT rendered at L1. Either branch leaves his word binding.
- **b-1** The consolidator emits `category_views` — per node: member list + AUM rollup + as-of; **plus** the L1/L2 sub-nodes: `Client > Supervised / Unsupervised / Unflagged` where the predicate exists and an explicit `predicate: "unavailable"` marker where it does not (the DE lane renders that marker as "fee split unavailable" — NEVER as `Unsupervised = 0`); `Models > Custom` member rows (L2); SMA L1 nodes per r3; the **view-plane flag** on Insurance. Legacy `non_model` fields **BYTE-UNCHANGED** (inv-3). Membership resolves ONLY through the registry (inv-1: `grep -L PRIMARY_MODEL_KEYS` over the vocabulary-carrying set is your oracle).
- **p2 + inv-4 (emit half) + inv-2** — print BOTH sums per firm: gold plane five peers == `total_aua`; view plane rendered L0 == `total_aua − Insurance`. **THE EMIT-TIME GUARD (decomp s.4a, CTO-confirmed 66460): assert `Insurance == 0` on the view plane and REFUSE THE EMIT the day it is not, printing the offending member — the registry's F5 shape (raise, never fold). Not an alarm, not a monitor: a producer assert.** Exercise it: a fixture with one insurance member → the emit REFUSES. Cross-project edge: `ADVI_INSURE`'s first-insurance-member cell carries the observed trigger "D1 p2/inv-4 re-verified with Insurance > 0" — that is INSURE's TO, not yours; you own the guard.

## Half 4 — `D1-e-1`, `D1-e-2`, `D1-e-3`, `D1-inv-1`: PRODUCER RESOLUTION (the hand maps resolve THROUGH the registry)

Full measurement: `org/tier1_exec/2.0.0_SA_COO/deliverables/D1_CATVIEWS_STAGE3_SURFACE_E_ENUMERATION_PREP.md`. Three axis values, seven instances: **e-1 per-FIRM (live)** `build_cottonwood_mdpf_slice.py` `CANONICAL_KEY` / `INCOME_NON_MODEL_NAMES` / `PENDING_RULING` (+2 importers) → resolve through `mdpf_category_registry.resolve()`; the LOUD guard stays (unknown still raises), the map it checks is the ONE registry. **e-2 per-VINTAGE (backfill)** — `ECLIPSE_NAME_TO_KEY` · `LEGACY_NAME_TO_MODEL_KEY` · `MODELNAME_TO_KEY` · `MODEL_SERIES_TO_KEY`: ⛔ **a STANDING CAUTION, not a remedy — a backfill may legitimately need its era's vocabulary; their disposition is the cell's QUESTION. Measure (does each still have a live consumer? does routing it through the registry change any historical figure?) and print; do NOT route them blindly.** **e-3 per-SERVED-ARTIFACT** `SERVED_MODEL_NAME` ×2 · `INFLECTION_MODEL_KEYS` · `ROSTER_MODEL_NAME` — the `dim_mdpf_aum_timeseries.py` five keys are character-for-character `PRIMARY_MODEL_KEYS` **arrived at by hand**: make them READ the registry (inv-1) so a sixth archetype cannot silently diverge. The `SERVED_MODEL_NAME` 7-vs-5 pair is **NOT a defect** (each documents its difference at the definition site; decomp s.2(e)) — do not re-file it.

## Half 5 — `D1-d-1`: THE COTTONWOOD DONE ROW (after b-1)

Measure Custom / Client from cot BD data at relationship grain; the measured values REPLACE the ~$7M Custom / ~$30M Client ESTIMATES in the PRD s.6.5 (they are Andrew's own figures, marked INFERRED in the run). Print measured vs estimate.

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding (Rule 22a) |
|---|---|---|---|
| **D1R1DS-AC1** | `VIEW_TREE` = 11 nodes incl. `Client > Supervised` / `Client > Unsupervised` (his labels); Insurance retained with a view-plane exclusion flag; `self_test` rc=0; F5 raise on an unknown node EXERCISED | D1-h-r1, D1-a-1 | EXERCISED |
| **D1R1DS-AC2** | SMA L1 node set == `{m.member_id for m in members_for('SMA') if m.strategy_id}` == {divz, pfoe, muni, tax}; idvz/pfde un-noded; a new SMA appears with a registry row + `strategy_id` and NO code change (fixture) | D1-h-r3 | EXERCISED |
| **D1R1DS-AC3** | Custom set reconciled against `dim_model_portfolio` (every non-Primary Opal model registered or excluded with reason, printed); the seven hand-map instances resolve through the registry (e-1 routed; e-2 DISPOSITIONED with measurements, not blindly routed; e-3 reads `PRIMARY_MODEL_KEYS`); `grep -L PRIMARY_MODEL_KEYS` over the vocabulary set printed with its denominator | D1-h-r4, D1-e-1, D1-e-2, D1-e-3, D1-inv-1 | SOURCE + EXERCISED |
| **D1R1DS-AC4** | Per-firm table printed: account-grain client feed {cot / 49F / inf} × predicate {column, grain, value set} — cot LIVE three-valued; 49F sleeve-grain on the BD plane (or `pending D3 join`); inf MEASURED after a WIDENED census (denominator printed) | D1-h-c1, D1-h-c2 | LIVE STATE |
| **D1R1DS-AC5** | The r2 decision table {equal / differs / predicate-absent} per firm with row counts, and the branch taken (RENAME vs TWO AXES) stated with the measurement that chose it | D1-h-r2 | EXERCISED |
| **D1R1DS-AC6** | `category_views` emitted with L0/L1/L2 sub-nodes, the labelled third bucket (`supervised + unsupervised + unflagged == Client` to the cent), `predicate: "unavailable"` where absent, the Insurance view-plane flag; legacy `non_model` BYTE-UNCHANGED (byte-diff printed) | D1-b-1, D1-h-c3, D1-inv-3 | EXERCISED |
| **D1R1DS-AC7** | Both sums printed per firm (gold five-peer == `total_aua`; view L0 == `total_aua − Insurance`); every L1 set sums to its L0 parent; **the `Insurance == 0` emit guard EXERCISED with a mutant fixture → emit REFUSES** | D1-h-p2, D1-inv-2, D1-inv-4 | EXERCISED |
| **D1R1DS-AC8** | Cottonwood Custom / Client MEASURED at relationship grain, printed beside the ~$7M / ~$30M estimates | D1-d-1 | LIVE STATE |
| **D1R1DS-AC9** | `comp-pipescript io <script> --pipeline mdpf` run on the consolidator (COLUMN GAPS + portal consumers read); commit-gate PASS; Rule 15; `safe-commit.sh` under your author line; proof instance VALID rc=0 positional | D1-b-1 | SOURCE |

## Law that binds this build (not preference)
Rule 13 (DS owns `data/mdpf/scripts/gold/*.py` commit→QA-deploy; `safe-deploy` gate) · Rule 14/14a (commit-gate; `safe-commit.sh -F`) · Rule 15 · Rule 17 (silver untouched — everything here is gold) · **NEVER build an alert/monitor** (the emit guard is a producer assert, which is the sanctioned shape) · **no shadow paths** — build correctly and port · NEVER#1 as-of discipline (T-1, trading calendar) · no non-ASCII in anything that runs on AWS · Build Ladder (rung 2 first: the registry mechanism, the crosswalk, `D_05`'s predicate read).

## Status + reporting
**Status is CELL-level** — flip cells in a `<cell_status>` block on this file as each lands (proof instance + status flip = ONE atomic delivery, in the same commit). Report to COO at each cell flip with the commit hash + push state ("LOCAL @hash, rides integration" — never bare "landed"); cc `3.0.0_SA_CVO` at AC6 and AC7 (the certifier reads the proof instance, not the message). Surprises: `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/D1_CATVIEWS/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580) (CVO mans + files the channel). **Nothing on any subject to `4.0.0_SA_CRO*` this session** (Andrew-direct ~19:3xZ, three terminals).
