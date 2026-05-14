<task_order>
  <metadata>
    <id>ADVI_INFFIN.003</id>
    <slug>dsc-inf-emit-batch</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P0 — bundles 3 surfaces (#2 P1 + #6 P0 + #8 P0) sharing upstream gate (silver/billing/ + per-account is_fee_paying flag); critical-path for Phase 2 RD wiring (.006) + AE chain (.007)</priority>
    <sla>~4-6h wall; ships standalone (no dep on .004 DS~A directory OR .005 DS~B 49F audit); .005 audit shape informs .003 schema normalization but can land in parallel with surface ship</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief, commit e7965874b)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13 — DS~A/~B/~C/~D all 4 sub-lanes available (overrides session-scope 'base DS only' for INFFIN scope)</ref>
    <ref type="cross_link">Sibling: .001 RD UI parity batch + .002 RD advisor-context + .004 DS~A directory artifact + .005 DS~B 49F audit (parallel investigation; informs schema normalization) + .006 RD Phase 2 (dispatch_held; gated on this ship) + .007 AE 0.6.1 chain + billing backfill (dispatch_held; gated on this ship)</ref>
    <ref type="andrew_directives">"There is no reason we should ever be displaying null for an account, it's either 0 or a fee" / "Look at 49 Financial ADVI page for reference, we had figured it out mostly for their book" / "Keep shapes similar across 49F and Inflection"</ref>
    <ref type="rule_17">CLAUDE.md Rule 17 strict — silver tier dedup + type standardization only; field-pruning + null-handling + business-row-filtering belong in gold. This TO is gold-tier emit; null-elimination + fee-split + per-HH stacking all permitted at gold</ref>
    <ref type="adjacent_ship">DS~C earlier ships: 52478bb3a + d12598087 + 14c54aec2 (Lambda v1.7.54 fixes) + 0997324d6 (per-advisor relationship_since); all empirically validated through chain #27 post-fire</ref>
  </references>

  <context>
    Three surfaces from Andrew's evening walkthrough share upstream gate (per-account `is_fee_paying` flag from silver/billing/) + share the same DS~C gold-emit lane.

    **Surface #2 — Continuous-ADV-L1 right partition stub: stacked top-N HHs + Other.** Page: AdvisorIntelligence → Distribution → Segment Analytics. View: Continuous/ADV/AUA/Quarter/1Y, drilled into Peter Lee (L1). Symptom: placeholder text "peter lee — Relationship-level timeseries coming soon"; left rail shows 4 static "Client 1 / Client 2 / Client 3 / Client 4" stub entries. Expected: stacked timeseries (bar or area) over selected Window × Interval; stacks = top N pseudonymized HHs in Peter Lee's book + "Other" aggregate. Mirrors GEO-L1 (state drill) top-N-cities + Other pattern. Use existing `enforceTop9Other` helper.

    Investigation hint: does `s3://opal-data-inf/platinum/advisors/{id}/timeseries.json` already contain per-HH per-period AUA series? If yes → pure RD. If no → DS~C extends `data/orion/scripts/gold/INF_D_02.advisor_client_detail.py` `build_advisor_books()` (or sibling) to add `relationship_stacked_periods[]` block (top N HH + Other per period).

    **Surface #6 — Fee Summary panel: blank top half + per-account FEE/TOTAL(BPS)/SPLIT(BPS) all null.** Page: AdvisorIntelligence → Books → Advisor → Client L3 → Fee Summary panel.

    Symptoms:
    - A (presentation): top half of panel empty (49F's FeeSummary renders headline "Client Fee" + per-role row breakdown there)
    - B (data): every row in Accounts Summary shows `—` for FEE / TOTAL (BPS) / SPLIT (BPS); two accounts (166, 477) red-flagged with warning icons + reduced AUA cells — likely surfacing data-quality gap
    - C (cohort): NNA (YTD) shows `+$0` for all 4 accounts; possible sanity issue but plausible if Roth + IRA had no mid-year flows

    Andrew rules:
    - "We should have figured out billing at this point including backfill billing... There is no reason we should ever be displaying null for an account, it's either 0 or a fee."
    - "DS can look into implementation for 49 as well to try and keep shapes similar." (Cross-firm parity)

    DS~C investigation: per-account fee emit in `INF_D_02.build_advisor_books` (or wherever account-level fees join in gold). Confirm `clients[].accounts[].fee_*` fields populated. If silver/billing/ is sparse, walk back the pipeline. Cross-check 49F's BD-pipeline billing emit shape for parity (via .005 DS~B audit deliverable).

    **Null-elimination rule (Andrew directive):**
    - Literal `0` / `$0` / `0 bps` → display as such (real-zero semantic)
    - `null` → bug; route back to fix the emit
    - `"no_structure"` sentinel for legitimate absence → tooltip explaining structural reason; NEVER `null` → `—` rendering

    **Surface #8 — Fee-Paying / No-Fee / All toggle reactive across AdvisorPublicProfile (incl. Lifetime Activity).** Page: AdvisorIntelligence → AdvisorPublicProfile (Inflection) — Executive Summary + Flows + Fee + Lifetime Activity.

    Symptoms:
    - A: toggle wired but `AUA Growth`, `Fee-Earning AUA`, `Non-Fee AUA` rows show `—`
    - B: Lifetime Activity chart displays banner "Fee-split data unavailable — showing aggregate" (backend doesn't ship per-fee-status timeseries)
    - C: `Avg Fee Rate: 102.5 bps` indicates SOME billing data exists, but partitioning aggregation missing across rest of metrics

    Andrew rule: "When you click the fee versus no fee versus combined toggles, you should see accounts and clients and aua and nna numbers all changing based on the aua cohort. This fee or no fee or combined designation should adjust all numbers displayed in AdvisorPublicProfile, including lifetime activity chart."

    Required per-period split: `aua_fee_paying / aua_no_fee`, `accounts_fee_paying / accounts_no_fee`, `clients_fee_paying / clients_no_fee`, `new_clients_*`, `nna_*`, `inflows_*`, `outflows_*`. Plus Lifetime Activity split bars.

    Prerequisite: per-account `is_fee_paying` flag must be reliable upstream — same dependency as Surface #6 (silver/billing/ + Inflection billing logic).

    **Consolidation rationale:** Surfaces #6 + #8 share upstream gate (silver/billing/ + is_fee_paying flag). Surface #2 is separable but DS~C lane fits naturally (same script INF_D_02.advisor_client_detail.py + sibling for per-HH timeseries). Batch all three for DS~C context efficiency.
  </context>

  <objective>
    Land three DS~C INF-side gold emits in a single coherent authoring pass:

    1. **Surface #2 per-HH stacked timeseries** in advisor book.json or sibling — top N HHs in advisor's book + "Other" aggregate per period (Quarter × 1Y window). Pseudonymized display_name only.
    2. **Surface #6 per-account fee emit** — `clients[].accounts[].fee_*` fields populated; null-elimination rule (literal `0` OR fee value OR `"no_structure"` sentinel with explanation; NEVER `null`). Red-flag account 166/477 structural condition surfaced in sentinel.
    3. **Surface #8 fee-paying split parallel fields** — per-period `aua_fee_paying / aua_no_fee` + `accounts_fee_paying / accounts_no_fee` + `clients_fee_paying / clients_no_fee` + `new_clients_*` + `nna_*` + `inflows_*` + `outflows_*` parallel-emitted; Lifetime Activity split bars.

    Schema parity with 49F informed by .005 DS~B audit (lands in parallel). When .005 ships, normalize Inflection schema to share field names with 49F (one shared FE accessor across both partners).

    Rule 17 strict applies: this is gold-tier work where null-handling + business-derives are permitted; never apply at silver.
  </objective>

  <scope>
    <surfaces>
      <surface id="2">Per-HH stacked timeseries (top N HHs + Other per period in advisor's book)</surface>
      <surface id="6">Per-account fee emit + null-elimination + red-flag sentinel</surface>
      <surface id="8">Fee-paying / No-Fee parallel-split timeseries fields across AdvisorPublicProfile metrics</surface>
    </surfaces>
    <files>
      <file action="investigate">data/orion/scripts/gold/INF_D_02.advisor_client_detail.py — `build_advisor_books()` per-account fee fields current shape</file>
      <file action="investigate">data/orion/scripts/silver/ (or wherever) — silver/billing/ partition horizon + per-account billing semantic</file>
      <file action="investigate">data/orion/scripts/gold/INF_D_05*.py — Lifetime Activity timeseries emit (advisor-level)</file>
      <file action="investigate">s3://opal-data-inf/platinum/advisors/{id}/timeseries.json — per-HH per-period AUA series existence (Surface #2 gate)</file>
      <file action="modify">data/orion/scripts/gold/INF_D_02.advisor_client_detail.py — add `relationship_stacked_periods[]` block (Surface #2) + per-account fee fields with null-elimination (Surface #6) + fee-paying split parallel fields (Surface #8)</file>
      <file action="modify_or_extend">data/orion/scripts/gold/INF_D_05*.py — Lifetime Activity fee-paying split bars emit (Surface #8 Lifetime Activity portion)</file>
      <file action="cross_reference_only">.005 DS~B 49F BD-pipeline audit output — feeds normalization decisions for schema parity</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Surface #6 + #8 upstream gate: confirm silver/billing/ partition horizon. Is `inf-billing-daily` Lambda backfilled to sufficient horizon for QTD/YTD/Max windows? Inspect S3 partitions; cross-check with comp-pipescript deployed for billing pipeline state.</description>
      <expect>Either silver/billing/ horizon is sufficient (proceed with gold emit) OR gap surfaced → ROUTE TO .007 AE 0.6.1 for backfill Lambda dispatch.</expect>
      <if_mismatch>If silver/billing/ gap surfaces, MCP COO with details; .007 AE 0.6.1 dispatch_held=true unblocks on this signal.</if_mismatch>
    </step>
    <step>
      <description>Surface #6 per-account fee emit: investigate `INF_D_02.build_advisor_books()` current shape. Are `clients[].accounts[].fee_*` fields already attempted but failing JOIN? Or never emitted? Walk back the pipeline to identify gap.</description>
      <expect>Gap location identified — either silver/billing/ sparse, JOIN logic missing, or business-derive needed.</expect>
    </step>
    <step>
      <description>Surface #6 red-flag accounts (166, 477): identify structural condition. What makes those accounts different? (transfer-only? legacy contract? IRA without RIA structure?) Document for sentinel emit.</description>
      <expect>Structural condition documented; sentinel value defined (e.g., `fee_structure: "transfer_only"` or similar).</expect>
    </step>
    <step>
      <description>Surface #2 per-HH timeseries existence: empirical S3 inspection of `s3://opal-data-inf/platinum/advisors/{id}/timeseries.json` for all 4 advisors. Does the file contain per-HH per-period AUA series, or only advisor-aggregate?</description>
      <expect>If per-HH already present → confirm to RD-B (.002) for pure-FE consumption. If only advisor-aggregate → DS~C extends INF_D_02 (or sibling) to add `relationship_stacked_periods[]` block.</expect>
    </step>
    <step>
      <description>Surface #8 fee-paying split: investigate AdvisorPublicProfile data accessor. What field shape does FE expect? Per-period partition fields parallel to existing aggregate? Or filterable view with `is_fee_paying` flag on each row?</description>
      <expect>Schema shape decided — parallel-fields preferred (e.g., `aua_fee_paying / aua_no_fee`) for FE simplicity vs filterable.</expect>
    </step>
    <step>
      <description>Cross-link with .005 DS~B 49F audit: check if .005 has shipped audit deliverable. If yes → align INF schema to 49F field names. If no → emit INF native schema first; revisit normalization when .005 lands. Coordinate via COO if normalization requires INF rename.</description>
      <expect>Either aligned-with-49F at first ship OR rename-on-.005-ship plan.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Surface #6 per-account fee emit: add `clients[].accounts[].fee_*` fields to `build_advisor_books()`. Null-elimination rule strict:
- Real-zero → emit `0` / `0.0` (literal)
- Legitimate absence → emit sentinel `fee_structure: "no_structure"` (or appropriate) with explanation field
- NEVER emit `null` for any fee field</description>
      <expect>Every Inflection account emits non-null fee fields OR documented sentinel.</expect>
    </step>
    <step>
      <description>Surface #6 red-flag sentinel: for accounts 166 + 477 (and any other structurally-different accounts), emit sentinel with `fee_structure_reason` field explaining the structural condition (e.g., "Account in transition / no current fee schedule"). FE can render the warning icon + tooltip explaining.</description>
      <expect>Red-flag accounts carry sentinel + explanation; no silent `null`.</expect>
    </step>
    <step>
      <description>Surface #8 fee-paying split: emit per-period parallel fields. Required fields:
- aua_fee_paying / aua_no_fee
- accounts_fee_paying / accounts_no_fee
- clients_fee_paying / clients_no_fee
- new_clients_fee_paying / new_clients_no_fee (Surface #3 cross-link)
- nna_fee_paying / nna_no_fee
- inflows_fee_paying / inflows_no_fee
- outflows_fee_paying / outflows_no_fee
Per period (Quarter window canonical; extend to other windows if FE needs).
Apply at gold tier per Rule 17 strict.</description>
      <expect>Parallel-fields emitted for all AdvisorPublicProfile metrics; aggregate fields preserved bit-for-bit (additive contract).</expect>
    </step>
    <step>
      <description>Surface #8 Lifetime Activity split bars: extend INF_D_05* (or wherever Lifetime Activity timeseries emit lives) to add per-fee-status split bars. FE removes "Fee-split data unavailable — showing aggregate" banner once data lands.</description>
      <expect>Lifetime Activity emit carries split bars; FE banner can retire.</expect>
    </step>
    <step>
      <description>Surface #2 per-HH stacked timeseries: extend INF_D_02 (or sibling) to add `relationship_stacked_periods[]` block in advisor book.json. Per period: top N HHs (use enforceTop9Other helper pattern) + "Other" aggregate. Pseudonymized `display_name` only — no cleartext HH names (PII gate; same as earlier ADV-NNA fix).</description>
      <expect>Block emitted per period; PII enforced; left rail legend matches stacks (not static stubs).</expect>
    </step>
    <step>
      <description>Schema parity normalization (post .005 DS~B audit): if .005 audit deliverable lands during this TO authoring, align INF field names to share with 49F where shape matches. Document any divergences requiring rename or FE adapter via COO.</description>
      <expect>Where 49F + Inflection have identical fee-split semantic, share field names. FE accessor becomes shared.</expect>
    </step>
  </phase>

  <phase id="3" when="empirical-validation">
    <step>
      <description>Rule 17 verify: no silver-tier modifications introduced. All emits are at gold tier (INF_D_02 + INF_D_05*). Silver/billing/ + silver/api_dims/accounts_v2/ unchanged.</description>
      <expect>Silver scripts untouched; gold-only changes.</expect>
    </step>
    <step>
      <description>Null-elimination smoke: after chain fires (via .007 AE 0.6.1), confirm zero `null` fee fields across all 4 Inflection advisors' book.json. Every account has either real-zero, real-value, or sentinel.</description>
      <expect>Zero `null` fields; sentinel coverage for legitimate absences documented.</expect>
    </step>
    <step>
      <description>Cross-firm parity (post .005 ship): visual diff Inflection vs 49F field names — share where semantic matches.</description>
      <expect>Schema parity achieved or divergence documented.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1 (Surface #2): `relationship_stacked_periods[]` block in advisor book.json emit per period (Quarter × 1Y); top N HHs + "Other" aggregate; PII-pseudonymized display_name only.
    AC2 (Surface #6 data): per-account fee fields populated for all Inflection accounts; null-elimination rule held (literal `0` OR fee value OR sentinel; NEVER `null`).
    AC3 (Surface #6 red-flag): accounts 166 + 477 carry sentinel + `fee_structure_reason` field explaining structural condition.
    AC4 (Surface #8 parallel fields): per-period `aua_fee_paying/aua_no_fee` + `accounts_*` + `clients_*` + `new_clients_*` + `nna_*` + `inflows_*` + `outflows_*` emitted for all advisors; aggregate fields preserved bit-for-bit (additive contract on existing 86+ downstream consumers).
    AC5 (Surface #8 Lifetime Activity): split bars emitted in INF_D_05* (or wherever); FE banner can retire post-ship.
    AC6 (Rule 17 strict): no silver-tier modifications; all null-handling + business-derives at gold.
    AC7 (Schema parity): cross-link with .005 DS~B audit shape; Inflection schema aligned to 49F field names where semantic matches. If .005 ships post-this-TO, normalization round-trips (rename via follow-on commit if needed).
    AC8 (Empirical post-chain): chain #28+ fires (via .007 AE 0.6.1) populate the new fields; zero `null` validation passes.
    AC9: ds-commit-gate PASS (py_compile + AST + ruff py39 + Rule 15 `from __future__ import annotations`).
    AC10: safe-deploy cycle complete (commit → push → S3 upload → comp-pipescript deployed MATCH).
    AC11: MCP RAVC2 to COO with per-surface evidence + .007 chain-fire unblock signal.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-pipescript io INF_D_02 (column gaps + portal consumers); comp-blast INF_D_02 + INF_D_05* (blast radius); comp-validate gold_validate_config.yaml against fresh artifact post-chain</phase_1>
    <phase_2>ds-commit-gate.sh on every Python edit; py_compile + AST undefined-name + ruff py39 + Rule 15 `from __future__ import annotations`</phase_2>
    <phase_3>safe-deploy SHA-MATCH post-push; post-chain empirical (null-elimination smoke)</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    DEPENDENCIES:
    - silver/billing/ partition state → Phase 1 step 1 verify; if gap surfaces → ROUTE TO .007 AE 0.6.1 (dispatch_held)
    - .005 DS~B 49F audit shape → informs schema normalization; can land in parallel (rename via follow-on commit if needed)

    GATES:
    - .006 RD Phase 2 wiring (dispatch_held=true) UNBLOCKS on this ship + .007 AE chain fire
    - .007 AE 0.6.1 chain + billing backfill (dispatch_held=true) UNBLOCKS on this ship signal

    PARALLEL ACTIVITY:
    - .001 RD UI parity batch (parallel; no FE-side conflict on these surfaces)
    - .002 RD advisor-context wiring (parallel; Surface #3 cross-link on .002 — DS~C advisor-scoped NNA shape; investigate field path overlap with .002 in Phase 1 step 2 of .002)
    - .004 DS~A directory artifact (independent; Surface #4 contingent if RD-B routes there)
    - .005 DS~B 49F audit (parallel investigation; informs this TO's schema normalization)

    NO PORTAL: this is pure DS gold-emit; portal change in .006 Phase 2.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <chain_fire_required>
      Gold-emit changes; chain fire required to materialize new fields in platinum. .007 AE 0.6.1 handles chain dispatch post-this-ship.
    </chain_fire_required>
    <potential_backfill>
      If silver/billing/ historical gap surfaces in Phase 1 step 1, inf-billing-daily Lambda backfill required. AE 0.6.1 owns the Lambda dispatch + backfill run per .007 scope.
    </potential_backfill>
  </data_reprocess_scope>

  <deliverables>
    1. Surface #2: `relationship_stacked_periods[]` block in INF_D_02 (or sibling); top N HHs + Other; PII-pseudonymized
    2. Surface #6: per-account fee fields + null-elimination + red-flag sentinel
    3. Surface #8: fee-paying split parallel fields across advisor metrics + Lifetime Activity split bars
    4. Schema parity with 49F (when .005 audit lands; rename via follow-on commit if needed)
    5. Single or multiple commits under 0.4.0_DS_ClientPlatform~C author
    6. ds-commit-gate PASS + safe-deploy SHA-MATCH
    7. Session log with per-surface evidence + .007 chain-fire unblock signal
    8. MCP RAVC2 to COO post-AC1-11 PASS
  </deliverables>

  <ravc>
    DS~C RAVC2 to COO post-AC1-11 PASS. COO unblocks .006 RD Phase 2 (dispatch_held=true) + .007 AE 0.6.1 chain + billing backfill (dispatch_held=true). Post-.007 chain fire, .003 post-chain empirical (AC8 null-elimination smoke) closes final acceptance.
  </ravc>

  <notes>
    **Per DE brief consolidation note (#6 + #8):** these two surfaces share upstream gate (silver/billing/ + is_fee_paying flag). Author in single DS~C TO. Surface #2 batched because same DS~C lane + same script INF_D_02 (or sibling).

    **Andrew session-scope override:** DS~A/~B/~C/~D all 4 sub-lanes authorized for INFFIN scope (overrides "base DS only" session-scope directive). DS~C is the primary INF-side gold emit lane; DS~A handles isolated directory artifact (.004); DS~B handles cross-firm 49F audit (.005); DS~D not on critical path.

    **Class-A vs Class-B gate observation from earlier session:** ds-commit-gate catches Class-A latent bugs (undefined names, missing imports); chain run catches Class-B partial-refactor leaks (consumer signature mismatch). Both apply to this TO — atomic-bundle ship gets both gates.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"` per agent commit identity protocol.

    **Critical-path note:** this TO is on the Phase 2 critical path. .006 RD Phase 2 + .007 AE 0.6.1 both gate on .003 ship signal. Prioritize.
  </notes>
</task_order>
