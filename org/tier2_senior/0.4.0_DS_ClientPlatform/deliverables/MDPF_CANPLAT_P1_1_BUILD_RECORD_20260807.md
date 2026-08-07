# MDPF_CANPLAT.P1-1 — canonical gold spine: build record, classifications, confirmations

**TO:** `MDPF_CANPLAT.P1-1.canonical-gold-spine` @f123fbf6e (GO 2.0.0_SA_COO~Z 20260806T235814Z)
**Author:** `0.4.0_DS_ClientPlatform~Z` · 2026-08-07 · **Build commit:** `d136d5bb1` (wave 1, atomic across both trees); tests + this record follow in wave 2 (same session)
**Governing:** PRD @24d3eb2f8 · CONTRACT @a3106d585 (+@850075894 §B1 amendment) · adopted body @a6ae64326 under the 7 deltas

> §0 binds this record: shape work only; no semantic change; a number that surprised me is not a finding.

---

## 1. What landed (wave 1, @d136d5bb1)

ONE firm-parameterized path: `dim_mdpf_aggregate_aua_timeseries.build_firm_timeseries` —
one body, `FIRM_BUILD_CONFIG` rows, zero firm-name branches (AST-asserted in the test
suite, not grepped). The bespoke builders are dissolved; their names survive as
≤3-line delegators for the deployed-generation callers (R11 stays AE~Z's). Global stays
the fold, invoked exactly once. Cottonwood's L2 remains the declared `l1_feeder_prep`
family (F-2 vendor necessity, route_bindings row) — run IN the one Lambda sequence
(bdmp dim → composed slice → pair+sidecar), its composed artifact verified-not-composed
at the fold and canonically shaped like every sibling.

`mdpf_gold_consolidator.py` (mdpf-gold-lambda): A2 schedule-first handler (builds on
every invocation, trigger identity recorded, never marker-gated) · A3/A4 direct dated
hyphenated emission · A5 per-scope isolation · A6 manifest at
`portal/gold/mdpf/_manifests/{data-as-of}/{process-ts}.json` (grant live-simulated by
AE~Z) carrying roster+bindings sha256 · A7 preserved byte-for-byte in behavior (the
`mdpf_revamp` name is DELIBERATE — retirement SEQUESTERED by Andrew, pocketed brief
@76d4ba532) · A8 conditional immutable writes (`unchanged`/`conflict`, never a silent
overwrite) · A9/criterion-5 canonical calendar via `mdpf_calendar_binding` with the
standalone `assert_pmc_backend()` control.

## 2. Δ5 — the five §B3 fields: ALL FIVE RULED CANONICAL-FOR-ALL-FOUR

Classification only; nothing is deleted; every decision is L-1's one-schema law applied
with REAL per-scope semantics rather than null-stubs (arrays must satisfy the §B array
invariants, and each field has an honest per-firm derivation):

| field | ruling | firm-scope derivation (real, not stubbed) |
|---|---|---|
| `opal_aggregate_aua` | canonical-for-all | the SAME headline identity law as global: `model + non_model` where both present, else null (never 0). At firm scope this equals the firm headline (custody basis) by the W-2b identity. |
| `point_class` | canonical-for-all | any-cohort taint over the artifact's own provenance: measured / interpolated_estimate / absent. Genuinely load-bearing at cottonwood (the sanctioned backfill window is visible in-band). |
| `count_basis` | canonical-for-all | counts are never carried per-firm, so measured-where-present / absent-where-not — the Rows-5/6 legibility channel, uniform vocabulary with global. |
| `count_as_of` | canonical-for-all | the measured date itself where a count exists, null where not (per-firm counts never wear a foreign date). |
| `account_count_total_raw` | canonical-for-all | no carry-forward runs on a per-firm surface, so raw == served series — emitted anyway: "a carry-forward that erases its own input cannot be audited" generalizes, and uniform shape is the law. |
| `inflection_non_model_aua` | **NOT canonical** (pre-ruled, §B3) | firm-named field at global scope. **Still served** until Andrew rules retirement — enumerated as the ONE R2 ruled extra (`R2_RULED_EXTRAS`, citation carried in code). Not a deletion decision. |

**R2 note:** key-set identity is asserted with NO modulo clause; the single §B3-cited,
retirement-pending extra is enumerated with its citation and tolerated ONLY at its
served location. This is the contract's own row implemented, not a manufactured
carve-out; the sequence is shape decision → verified fold → retirement (Andrew's).

**One adjacent honest-absence decision (mine, recorded):** `partner_custody_total` at
GLOBAL scope emits null-per-date with an in-band meta note. The 2-firm sum is meta-only
by design (cottonwood's holdings leg deliberately does not fold into it) and NO RULED
BASIS exists for a global custody SERIES; minting one is a semantic ruling a shape
project must not make (§0). The firm-sum stays inspectable at
`meta.latest_cross_section`. If Andrew rules a basis, populating it is a one-line
change.

## 3. Δ6 — the four §C ⟨confirm⟩ rows

| module | contract inference | verdict |
|---|---|---|
| `mdpf_revamp_model_crosswalk.py` | PORT, "model-key mapping" | **CONFIRMED.** The single load-bearing crosswalk (model_id-keyed, raise-on-unknown F5); imported by the spine + account-distribution; ports as-is. |
| `stage_mdpf_revamp_trio.py` | RETIRE, "staging choreography the one path removes" | **CONFIRMED RETIRE.** Its three jobs (build trio via spine builders, byte-verified staging uploads, subprocess-run the derived dims) are all absorbed by the consolidator's in-process sequence. Repo file left in place and functional (delegators keep it running); its retirement is R11's evidence-gated act, AE~Z's. |
| `cottonwood_aua.py` | PORT, "cottonwood L1" ⟨confirm⟩ | **CORRECTED: NOT part of the Lambda closure.** It is OPAL_ASSETS C10 — the partner-day AUA cohort figure derived from `opal-data-cot` gold for the daily-AUA registry; nothing in the MDPF gold chain reads its output (the slice derives holdings totals itself from `blackdiamond/cottonwood/silver/fact_holdings`). Porting it into mdpf-gold-lambda would ADD a cross-firm-bucket read (opal-data-cot) the family deliberately excludes (firm-sep condition (i): no cot/bd bucket constant exists in the family). It stays a standalone script. |
| `build_dim_model_portfolio.py` | PORT, "cottonwood L1" ⟨confirm⟩ | **CONFIRMED.** THE declared L1 preparation (route_bindings `l1_feeder_prep`, the only declared row): silver→gold dim with value_date re-key inputs, blend decompose, strict-Opal filter, relationship-grain collapse. Runs first in the family sequence (criterion 8) inside the consolidator. |

`rebalancer_schemas.py` (silver-tier module imported into gold): ports with the family,
vendored + hash-tied in BUILD_MANIFEST per the adopted cross-domain row (AE~Z has it).

## 4. Coverage ratios — measured live 2026-08-07 ~0040Z, denominators printed

From the staged composed cottonwood artifact (`gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json`, as_of_last 2026-08-03):

- **I-2 / R5 / W-2: cottonwood `non_model_aua` populated 8 of 446 axis dates.**
  (Exactly the PRD §4 W-2 number.) NOT a derivation defect — the both-operand
  honest-None ternary holds where custody is absent; the custody leg (38/446) only
  recently began landing. **Acceptance stays COVERAGE with this denominator, never
  "non-null" (Guard 3 held: the ternary emits `else None`, and the CVO~Z G2 mutation
  fixture now includes the null→0 one-token mutant class at my request, 000529Z).**
- cottonwood custody: 38 of 446 · cottonwood model: 52 of 446.
- W-1 divergence confirmed live: `account_count_total` / `count_provenance` /
  `source_vintage_last` ABSENT from today's staged cottonwood artifact — the canonical
  shaper emits all three for every scope (cottonwood's count series = the DISTINCT
  population at its measured value_date, never a fanned by_model sum — LD-0330).

## 5. Tie-outs and exercised controls (wave 2 test suite, all green)

- **23/23 criterion tests pass** (`tests/test_canplat_p1_1.py`): Guard-3 ternary
  (null-not-zero on custody-gap AND model-gap legs), channel independence (each firm
  fails in turn; sibling builds on the TRUE canonical axis — the silent-re-axis defect
  is structurally gone because the axis derives from the DECLARED axis-source feed,
  never a sibling artifact), both roster readers fail closed (one test per reader,
  asserted on BEHAVIOR after a text-match false-positive on main()'s legitimate
  `return 3` exit code taught me the crude oracle was wrong), conditional writes
  (unchanged/conflict/written), key-set identity (pass/fail/ruled-extra), A4 grammar
  (dated, hyphenated, content-derived as-of; run-date refused), one-path AST assertion
  (zero firm-literal branches), delegator thinness.
- **Pinned calendar tie-out** (`tests/calendar_tieout.py`, criterion-5 ruling 3):
  T1 2027 coverage 10/10 on the canonical fallback (the shim's hole, asserted absent
  on the survivor) · T2 horizon guard (first uncovered year 2028 — a failing test now
  waits for the refresh instead of a silent every-weekday-trades regression) ·
  T3 falsifier fired and localized. Historical shim-vs-lib numbers (1096/0, 365/10)
  preserved in the harness header — not re-derivable after the shim's deletion.

## 6. Honest gaps — what this commit does NOT yet discharge

- **9c/R7 value-identity regression vs pinned VersionIds:** requires the QA comparison
  run against CVO~Z's committed canonicalisation + baseline (their G2). Not claimable
  from this box (pmc absent → `assert_pmc_backend` correctly refuses a QA-artifact
  build here — the control working, not a blocker). Runs with the first packaged QA
  cycle.
- **A2's infra half** (ScheduleExpression) and R13 (TF zero-diff) are AE~Z's P1-2/P2-1.
- **R1/R11/R12 and the CONTRACT §E adjudication** run on one unattended scheduled
  cycle, program-level, after AE~Z's package lands.
- **comp-validate (Phase 2 mandate):** no built artifact exists yet on this box; runs
  with the QA cycle. NOT signaling SAFE to anyone on this commit — nothing is deployed.
- **OWNTS repo copy** (`build_mdpf_etf_ownership_timeseries.py`) still imports the
  deleted shim: RETIRE-listed, zero estate readers, runs only from the untouched
  deployed prefix. Its repo copy is import-dead as of wave 1 — flagged here so R11's
  executor sees it stated, not discovered.

## 7. Deploy-sequencing (stated to AE~Z 001909Z, acknowledged 001942Z)

Nothing from this wave syncs to the EC2 prefixes (mdpf is deploy-gated; I performed no
gold-prefix cp). The package must carry `lib/trading_calendar.py` AS `trading_calendar.py`
at zip root (hash-tied) + `pandas_market_calendars<5` on the layer + `partner_roster.json`,
`route_bindings.yaml`, `mdpf_model_registry.json` adjacent (FLAT). The old chain keeps its
deployed generation until AE~Z's cutover; the bridge idles into a no-op when A4 lands.

## 8. Δ7 statement (required by the TO, stated plainly)

The surviving `fee_scope`/basis map (`FIRM_FEE_BASIS`) is **still builder-authored** —
a source literal, one copy instead of two, values unchanged (6/6). It is NOT declared
data; `meta.fee_basis_components` is its OUTPUT, not an independent declaration. The
migration to declared data is P2-1's config axis; nobody populates `firm_registry.json`
or the roster's empty `fee_scope` on this program's authority.
