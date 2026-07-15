# COT Gold Runner Triage — OPAL_GLDRNS.C1 (read-only; findings to CTO)

**Author:** 0.4.0_DS_ClientPlatform~C · 2026-07-15 · TO: OPAL_GLDRNS.C1 (CTO GO 192303Z)
**Andrew steer (this session, verbatim):** *"i just want to assess if anything is outright broken, or if there are clear and easy wins we can take advantage of quickly ahead of the inevitable porting to the consolidated system in OPAL_CONSOLIDATED."*
**Method:** REUSED the existing /gold-runner-code-review fan-out over cot (CTO, 2026-07-07, `wf_61db2e92-8e9`, commit `68dfcd87d` — 39 reviews + 28 adversarial verifies in `org/tier1_exec/1.0.0_SA_CTO/deliverables/cot_gold_bughunt_reports/`; its FIX_LOG was an empty scaffold — the drive/triage had never been done). This document IS that drive, re-keyed to the REAL nightly chain, plus a delta review of the 6 scripts that pass missed or that changed since, plus live grounding on last night's run artifacts. No fan-out re-run (one was launched, then stopped on Andrew's steer: `wf_e7318c86-989`, partial, discarded).

**DENOMINATOR: 45 review targets** = 42 repo `.py` + 2 deleted-from-repo-but-still-on-S3 (C_00, C_02, fetched from `s3://opal-data-cot/code/gold/`) + 1 `.py.legacy`. Coverage: 39/45 via the 07-07 reports (all 28 material findings re-adjudicated here), 6/45 delta-reviewed this session (D_04 diff, C_00, C_02, A_05 light, gold_prof/runner-telemetry classification, legacy). Ground truth: SSM doc `opal-cot-gold-run` (infra/aws/terraform/cot-pipeline/ssm.tf), last night's full run log (`s3://opal-data-cot/logs/cot-exporter/gold-run/cot-gold-run-20260715-020325.log`), live S3 artifact probes, `comp-pipescript deployed --firm cot` (48 MATCH / 0 STALE), `comp-freshness chain cot`.

---

## 0. WHAT ACTUALLY RUNS (the load-bearing fact every record gets wrong)

The cot nightly is **NOT** `gold_dispatch.sh` (the 1,336-line bd-fork dispatcher every doc/census points at). It is the **inline 18-step chain in SSM doc `opal-cot-gold-run`**, fired by the 4-phase EventBridge state machine on the cot-exporter EC2:

```
required: A_00(--incremental) A_03 A_04 B_00(--force-recent-days 14) C_01 C_03 C_06(--incremental) D_00 D_00b
optional: A_01 A_02 A_05 C_04 C_05 D_01 D_02 D_03 D_04
never:    S_00 · B_01 B_01b B_02 B_03 (lots stack) · C_07 C_08 (advisor attribution/fee) · D_00c · C_00 C_02 (de-chained 06-22, .py deleted from repo)
```

Consequences of the never-runs, all verified live:
- No `holdings_lots`, no `lots_unrealized`, no `account_team`/`rel_architect_lookup`, no `advisor_fee_detail`, no `role_aua` snapshots, no `employee_leaderboard.json` (D_04 now synthesizes it), no `aua_certification`, empty `gold/.checkpoints/`. The nightly holds the portal up on an extensive **fallback lattice** (BD-native architect, headline-derived synth leaderboard, empty tax/fee/OFC panels) and exits 0.
- `gold_dispatch.sh` would FATAL on its own PHASE_D1/D2 gates (both gate prefixes are empty) — proof it never runs. Its freshness gates, EventBridge emission, checkpoints, telemetry wrappers, and post-chain recon/shadow harnesses are all **dead for cot**.
- The 07-07 review's `runs_in_incremental` fields and REGISTRY.md/README/pipescript-census narratives are keyed to the dispatcher — i.e., to a chain that doesn't exist. (The census itself is dated 2026-06-15, pre-rewire.)

---

## 1. OUTRIGHT BROKEN (live, confirmed, in the running chain)

| # | What | Evidence | Blast |
|---|---|---|---|
| B1 | **A_00 incremental corrodes the served accounts dimension nightly** — the holdings-snapshot union re-injects the whole book with nulled txn-metadata, and `merge_incremental` overwrites established accounts' fields | verify_09 (confirmed critical, live-served 07-07: 13 corrupted) + **my 07-15 re-probe: 38 null-name-WITH-first_txn_date (growing ~3.5/day), 122 blank client_state, tax_status 844/844 'taxable', qualified_flag 844/844 False** | Every consumer of account_name/tax_status/client_state/qualified_flag: D_00 clients_tab, D_02 books, D_04 summaries, any tax split |
| B2 | **D_01 CLA (NMNC/NMEC lifecycle) served numbers are wrong two independent ways**: (a) `period_nna = daily − daily` where cumulative intended (verify_21, confirmed high); (b) weekend period-start → `fillna(0)` → period values inflate to inception-cumulative, ~2–4x today (verify_20, confirmed high) | Both confirmed at source + reachability; served in `platinum/firm/partner_analytics_{quarterly,monthly,annual}.json`; FE consumes via shared PartnerAnalytics.tsx (nmncBucketing) | CLA sub-views + segment ranking (GEO cohort + firm totals; ADV cohort already empty for cot) |
| B3 | **C_05 crashes every night** (swallowed as `optional`): holdings_lots never existed in cot v1, the lots_unrealized fallback tracebacks → exit 1 → **tax view never built; D_02 confirms "tax panels empty" nightly** | 07-15 nightly log lines 674–695, 944 | Cost-basis/tax panels served empty |
| B4 | **OFC (office) views empty every night**: `gold/dimensions/dim_advisor_office.csv` never uploaded to opal-data-cot (the deps-yaml precondition that never bound); D_00b/D_01 log "OFC view will be empty" ×4 | 07-15 log lines 798–799, 845–846, 875–876, 906–907 | timeseries/analytics OFC cohorts |
| B5 | **D_01 silently skips whole quarters**: `role_aua` snapshots missing for every period anchor (C_01b never ran) → "No client/account performance data for 2026-03-31/2025-12-31/2024-12-31 — skipping period" | 07-15 log lines 848–919 | Historical periods absent from served partner analytics |
| B6 | **The validation layer validates nothing while silver/allocations is frozen (07-08, the known cot snapshot freeze)**: C_04 SKIPs nightly and prints OK (PASS=0 SKIP=1); D_04's out-of-scope + c1_recovered steps skip; WP-10b recon harness doesn't run at all (dispatcher-only); and the recon harness itself is presence-only (verify_26/27: drift thresholds are dead code) | 07-15 log lines 593–594, 1648, 1653; verify_26/27 | No instrument currently fails on cot staleness/drift. NOTE: allocations freeze itself is the KNOWN tracked item (memory: cot snapshot-zero-row 2026-07-09) — close nothing on it here |

Also live-but-bounded: D_02 fee_summary null (no fee data exists for cot — expected), B3 team_attribution ERROR → empty for every client (C_07 never ran), platinum content sits ~2 trading days behind the silver frontier (B_00 wrote through 07-13 while silver holdings had 07-14 — cadence question for CTO, not adjudicated here).

## 2. EASY WINS (ranked; low effort × high value, worth taking BEFORE the OPAL_CONSOLIDATION port)

1. **Fix A_00 incremental** (stops B1 at the root): in `_run_incremental`, restrict the snapshot-union `_extra` to account_ids NOT already in the existing dimension (or make the overwrite loop preserve non-null existing values). One function; then one `--full` rebuild to repair the book. *The single highest-value fix in the estate.*
2. **Delete C_06's dead read of `client_performance.parquet`** (1 line, verify_23): the value is never used, its producer C_02 is deleted, and the frozen 06-22 artifact is the only thing between the nightly and a required-step abort. This is a lit fuse next to the cleanup crew.
3. **Re-add the `account_id` string-cast in `cot_silver_merge.py`** (1 line, from verify_17): disarms the confirmed-critical B_01 lots-wipe booby-trap and fixes ID-dtype hygiene for every consumer.
4. **Guard B_00's snapshot columns** (`units`/`market_value`/`account_id`/`asset_name` — mirror the existing `ticker` guard; verify_04+07): converts a vendor header drift from chain-abort/silent-$0-AUA into a loud skip. Few lines.
5. **De-chain or skip-clean C_05** (its inputs structurally don't exist in cot v1): 1-line SSM edit (AE) or an early clean exit; pairs with a CTO decision on what the tax panel should show for cot (see D2).
6. **Upload the office dim (or drop OFC for cot)**: `dim_advisor_office.csv` → `s3://opal-data-cot/gold/dimensions/` un-empties B4 immediately (AE data task); for a single-office firm, dropping OFC is equally defensible — either ends the nightly ERROR noise.
7. **Suppress or fix CLA for cot** (B2): proper fix = thread the trading-day-fallback start + windowed canonical NNA into `build_cla_view` (medium); pragmatic pre-port = stop emitting `views['cla']` for cot (small). Recommend pragmatic unless CLA is actively used by the client.
8. **Purge the resurrection booby-traps**: delete dead `C_00/C_02.py` from `s3://opal-data-cot/code/gold/` and align `gold_dispatch.sh` with the SSM chain — or retire the dispatcher from the cot tree entirely. Today a well-meaning `--chain canonical` would run dead lots-FIFO producers and **overwrite served-adjacent `client_performance.parquet` with the $44M-undercount model**, plus fire the wrong-firm wires it still carries (`comp-freshness chain bd` gate; EventBridge `Source=bd-pipeline.gold-chain`, which the live `exec-summary-trigger` rule matches with no detail filter → a hand-run cot chain triggers the **49F** exec-summary Lambda; telemetry labeled `bd-gold-layer-runner`).
9. **Records hygiene** (cheap, prevents the next wrong-chain review): fix `gold_pipeline_deps.yaml` stale key (`B_00.hybrid_price_fill.py` — precondition never binds), delete/rewrite `README_BUILD_SEQUENCE.md` (bd-era 00–12 chain), REGISTRY.md D-group row (says D_00..D_03; D_04 exists; route map still lists `gold/artifacts/*` family), delete `05_build_client_performance.py.legacy`, update the pipescript census narrative (says the nightly is `gold_dispatch.sh --chain full`).

## 3. TRASH vs USEFUL (efficacy, consumer-anchored)

**USEFUL — the actual load-bearing spine (keep; this is what the port should carry):**
`cot_silver_merge` → **A_00, A_03, A_04, B_00 (snapshot-first branch), C_01, C_03, C_06, D_00, D_00b, D_01, D_02, D_03, D_04** — all consumer-anchored to served platinum keys the Cottonwood tenant reads (pipescript `advi-cot`: platinum/firm/*, platinum/advisors/*, platinum/clients/*, platinum/accounts/*). A_01/A_02 run as no-op-ish optionals (no fee data); A_05 is a data-layer geo dim (not FE-served, optional). E-group + validators = ad-hoc diagnostics toolkit: **keep** (with E_21's cross-dating defect on `--date`, verify_24, noted before anyone trusts it for reconciliation).

**TRASH (dead weight in the cot tree — retirement candidates):**
| Item | Why dead | Action |
|---|---|---|
| `C_00/C_02.py` on S3 code/gold/ | de-chained 06-22, repo-deleted, outputs frozen 06-22 | purge from S3 (easy win 8) |
| `gold_dispatch.sh` (for cot) | nightly never touches it; carries wrong-firm wires + dead gates/checkpoints/emissions | align-or-retire (CTO ruling) |
| `gold_prof.py`, `runner-telemetry.py` | only invoked by the dead dispatcher; SSM chain calls `python3.11 $script` bare | retire with dispatcher decision |
| `run_gold_layer.sh`, `ssm-run-gold.sh` | bd-era orchestrators, superseded by the SSM doc | delete on next touch |
| `05_build_client_performance.py.legacy` | dead file | delete |
| `README_BUILD_SEQUENCE.md` | documents a pipeline that never existed for cot | delete/rewrite |
| S_00 `build_canonical_prices_v2.py` + `silver/prices/canonical_prices.parquet` for cot | frozen 06-09; snapshot-first B_00 prices from BD-reported MV ("skipping positions-FIFO", nightly log) | retirement candidate — confirm no E-diagnostic dependency, then drop from cot |
| `diag_gold_silver_recon.py` + `gldinc_p1_shadow.py` (for cot) | wired only in the dead dispatcher post-chain; and recon is presence-only (dead thresholds) | fold intent into the port's validation design |

**DORMANT BOOBY-TRAPS (not broken today because their path never runs — but confirmed-critical the day someone runs it):** B_01 lots wipe via silver account_id dtype (verify_17, critical), C_07 unconditional KeyError crash — `account_is_open` never produced by cot silver (verify_19, critical, empirically never-landed output), B_01b DynamoDB/watermark defects (verify_06/08), B_02 (verify_12), C_08 (verify_25). **Anyone "just running the lots stack" for cot walks into all of these at once.** They are port-time design inputs, not pre-port fixes.

## 4. DESIGN ITEMS (port-time decisions for OPAL_CONSOLIDATION — not pre-port patches)

- **D1 — The cot data-availability contract**: cot has no Schwab feed, no fee data, no reliable lots, one synthesized advisor. The lots/tax/attribution stack (B_01–B_03, C_05, C_07, C_08, D_00c) is structurally unfeedable. The consolidated port should scope cot to the snapshot-first spine (holdings-snapshot → AUA/NNA/mix/summaries) and EXPLICITLY declare tax/fee/attribution out-of-scope-until-data — not carry six scripts of crash-fallback lattice.
- **D2 — Tax panel story**: C_05/D_02 tax panels have never had cot data. Decide: hide the panel for cot, or source cost-basis from BD snapshot fields if they exist.
- **D3 — role_aua/period anchors**: backfill once (run C_01b under supervision) vs accept missing historical quarters vs port-time re-derivation. Affects B5.
- **D4 — `account_is_open` in cot silver**: root of the C_07 crash; a silver schema decision (cot silver never emits it), not a gold patch.
- **D5 — Validation that can fail**: C_04 SKIP-as-OK, presence-only recon, optional-step crash-swallowing (C_05 failed 3+ weeks with zero alarms), `exit 0` on a night with 40+ WARN/ERROR lines. The port needs per-step verdicts surfaced, not a chain exit code.
- **D6 — Platinum cadence**: content as_of tracks 07-13 while silver holdings had 07-14 at run time; T-1 vs T-2 expectation should be pinned per trading-calendar law (measured observation only; NOT a staleness claim — allocations freeze is separately tracked).

## 5. NAMED FINDING (Andrew-parked — carried, not fixed)

- **cot leaderboard 1Y = 363-day window (SERVED)** — carried per TO + memory anchor (`project_cot_leaderboard_1y_363day_window_anchor`). Surface note: D_00c (the fee-gated leaderboard producer) is dormant for cot; since 07-15, D_04 synthesizes `platinum/firm/leaderboard.json`/dashboard employee_leaderboard with a single `1Y` window from advisor books + firm headline (nightly log: "SYNTHESIZED ... $433,747,822, 221 clients, 844 accounts"). Any 1Y-window fix belongs to whichever producer survives the port.

## 6. PER-SCRIPT TRIAGE TABLE (denominator 45)

| Script | Nightly? | Pattern | Efficacy | Material verdict |
|---|---|---|---|---|
| cot silver → (context) `cot_silver_merge.py` | silver chain | S | useful | 1-line ID-cast easy win (verify_17 root) |
| build_canonical_prices_v2.py (S_00) | NO | S-prep | **inert for cot** (frozen 06-09; B_00 skips FIFO) | retire-candidate; verify_02 medium moot for cot |
| A_00.accounts_dimension | YES (required, --incremental) | A-dim | useful/critical-path | **B1: confirmed critical, LIVE + growing** |
| A_01.advisor_assignments | YES (optional) | A-dim | near-no-op (no data) | clean-ish (1M/2L, none material) |
| A_02.fee_rate_history | YES (optional) | A-dim | no-op (no fee data; output absent) | highs refuted (verify_01/03) |
| A_03.positions_cube | YES (required) | A-dim | useful (unit spine) | mediums only; allocations-signal WARN is the known freeze |
| A_04.client_dimension | YES (required) | A-dim | useful | mediums only |
| A_05.assets_dimension | YES (optional) | A-dim | data-layer, not FE-served | delta-reviewed light: post-B_00 read, optional/non-gating per ssm.tf; keep |
| B_00.canonical_holdings | YES (required) | B-canonical | **the AUA spine** | verify_04+07 highs: guard cluster = easy win 4 |
| B_01 / B_01b / B_02 / B_03 | NO (v1 skip) | B-canonical | unfeedable (no lots data) | dormant booby-traps (verify_17/06/08/12); port-time D1 |
| C_00.canonical_performance (S3-only) | NO (de-chained) | C-activity | dead; outputs frozen 06-22 | purge from S3; delta-review notes: rc=0-on-missing-input + orphan-drop + aua_residual-labeled-NNA (moot if purged) |
| C_01.canonical_nna | YES (required) | C-activity | useful (NNA source of truth) | mediums only (dedup WARN has observability) |
| C_01b.role_aua_backfill / C_01c.role_aua_flow_join | NO | C-activity | never ran (role_aua empty) | D3 decision; C_01b high (dormant) |
| C_02.client_performance (S3-only) | NO (de-chained) | C-activity | dead; artifact frozen 06-22 **but still read by C_06** | purge AFTER easy win 2; delta-review notes: gate-artifact writer role now vacant (aua_certification empty ties to B6) |
| C_03.account_performance | YES (required) | C-activity | useful (firm-AUA derivation) | high refuted; mediums carried in 07-07 report |
| C_04.validate_aua | YES (optional) | validator | **decorative while allocations frozen** (SKIP→OK) | B6/D5 |
| C_05.client_tax_liability | YES (optional) | C-activity | **crashes nightly; output never built** | B3 → easy win 5 + D2 |
| C_06.client_mix_timeseries | YES (required, --incremental) | C-activity (writes some portal-facing JSONs — known C→D pattern deviation, REGISTRY-documented) | useful | **easy win 2 (lit fuse)**; watermark restatement-blindness class noted |
| C_07.advisor_attribution / C_08.advisor_fee_efficiency | NO (v1 skip) | C-activity | unfeedable; C_07 has never landed output | verify_19 critical (dormant) / verify_25 (dormant); D1/D4 |
| D_00.portal_aggregates | YES (required) | D-publisher | useful (headline/clients_tab/filters/snapshots) | mediums only |
| D_00b.portal_timeseries | YES (required) | D-publisher | useful | B4 (OFC empty) = easy win 6 |
| D_00c.portal_leaderboard | NO (fee-gated) | D-publisher | superseded by D_04 synth | retire-or-revive at port (§5) |
| D_01.partner_analytics | YES (optional) | D-publisher (computes business numbers — pattern deviation, justified pre-port) | useful | **B2 (CLA ×2 confirmed) + B5** = easy win 7 + D3 |
| D_02.advisor_client_detail | YES (optional) | D-publisher | useful (books/details) | high refuted; empty tax/fee/team panels = upstream (B1/B3/D1) |
| D_03.composition_artifacts | YES (optional) | D-publisher | useful | high refuted; non-architect comp skipped (upstream C_07) |
| D_04.client_portal_summary | YES (optional) | D-publisher (synth = justified deviation) | useful; synth leaderboard LIVE + correct 07-15 | delta-reviewed: sound; note hardcoded `cottonwood_capital_advisors` id must match D_02 book_key (string coupling) |
| validate_sl_nightly_gate / validate_platinum_consistency | NO (ad-hoc only; "nightly" in name is aspirational) | validator | keep as toolkit | verify_28 low; D5 |
| diag_gold_silver_recon / gldinc_p1_shadow | NO (dispatcher-only) | diagnostic | not running for cot | verify_26/27 mediums; fold into D5 |
| gold_prof / runner-telemetry | NO (dispatcher-only) | support-infra | dead for cot | retire with dispatcher |
| E_00/E_01/E_18/E_20–E_24 | NO (ad-hoc) | diagnostic | keep (toolkit) | E_21 cross-dating (verify_24 high, diagnostic-tier) |
| 05_build_client_performance.py.legacy | NO | dead-file | trash | delete |

## 7. INSTRUMENT / RECORD NOTES (for CTO; found in passing, grounded)

1. `comp-pipescript deployed`'s denominator is the LOCAL tree → S3-only scripts (deleted C_00/C_02) are invisible to it; "48 MATCH, 0 STALE" while dead code sits deployed. Sweep also leaves `code/diag/` UNCOVERED (its own honest flag).
2. `comp-pipescript deployed <script>` + `comp-freshness chain bd` still SKIP on the 2026-07-09 bd sovereign-hold flag — that hold was **lifted completely** (Andrew-direct 07-14); the instruments carry a stale prohibition.
3. pipescript `advi-cot` census (2026-06-15) still narrates `gold_dispatch.sh --chain full` as the nightly — pre-rewire; the 07-07 review inherited this error into every `runs_in_incremental` field.
4. This triage supersedes nothing in the CTO reports folder — the granular per-agent reports remain the finding source; FIX_LOG there remains empty by design (fixes are a separate gated wave per TO).

## Compiler Tools

| Tool | Use | Result |
|---|---|---|
| comp-pipescript deployed (sweep + --firm cot + per-script) | repo-vs-deployed reconciliation | cot 48 MATCH/0 STALE; exposed local-denominator blindness + stale bd-hold flag |
| pipescript advi-cot | estate thread + consumer anchors | served-key map; census narrative found stale (dispatcher) |
| comp-freshness chain cot / bd | freshness config coverage | cot chain exists (dispatcher gates on bd's = wrong-firm, dormant); platinum 2td-behind reading |
| comp-grep ×5 | EventBridge source consumers, role_aua, validators invokers, portal CLA/nmnc | exec-summary-trigger collision confirmed; validators ad-hoc-only; FE nmnc consumption confirmed |
| comp-to | session TO context | OPAL_GLDRNS.C1 |

*(comp-pipescript io per-script was planned for the fix wave, not run — no code lands from this TO; consumer anchors came from pipescript + REGISTRY + the live nightly log instead.)*
