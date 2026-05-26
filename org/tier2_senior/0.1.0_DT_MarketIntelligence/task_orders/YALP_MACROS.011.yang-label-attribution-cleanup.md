# YALP_MACROS.011 — yang-generate-macro label + attribution cleanup (bundled FIX)

**Class:** FIX (cosmetic yang-side hygiene; non-blocking; no pipeline-correctness impact)
**Driver:** 0.1.0_DT_MarketIntelligence
**Author:** 1.0.0_SA_CTO (per /ws-charter cycle 0043 FIX absorption of COO cycle 113 ROUTE-CLEANUP)
**Source findings:** YALP_MACROS Phase 2b synthesis brief `59ab271de` §5 cleanup findings #3 + #5
**Bundle:** 2 cosmetic yang-generate-macro label/attribution fixes
**SLA:** none (no time-pressure per COO routing)
**CC:** 0.1.0_DS_MarketIntelligence~A (finding source — TO-007 author) + 0.1.0_DS_MarketIntelligence~B (BLS-attribution finding source) + 2.0.0_SA_COO (route originator) + 1.0.0_SA_CTO (authoring)

---

## §1 — Scope

Both findings are yang-generate-macro Lambda code/comment/metadata label-class corrections. Read-only verify-first; rename only if attribution-label-claim is incorrect (no-op fine if yang already attributes correctly).

### Finding #3 — ICSA / CCSA yang-side attribution audit

**Source:** ~B BLS reconnaissance brief `be703b5b1` §6 row 5. Empirical refutation: ICSA + CCSA NOT a BLS series. Authoritative publisher is **DoL ETA (Employment & Training Administration)**. BLS v2 POST against `ICSA` / `CCSA` returns `Invalid Series` / `Series does not exist`. FRED-mirror (`ICSA` series_id 11098, `CCSA` series_id 11099) is the convenient access path; canonical upstream is `oui.doleta.gov` / `https://oui.doleta.gov/unemploy/claims.asp`.

**Audit ask:**

1. **Read** yang-generate-macro Lambda code (`infra/aws/lambda/yang-pipeline/yang-generate-macro/lambda_function.py` per ~A §12 amendment commit `7024d6aba` precedent for Fed NLP `lambda_function.py:102`) — locate every reference to `ICSA` + `CCSA`. Read every comment / metadata field / attribution label associated with these two series.
2. **Verify** whether yang attributes them to "BLS" anywhere — code comments, metadata dicts, yang-internal documentation, output JSON attribution fields. Most likely candidates:
   - Series-source-label dictionary
   - Lambda docstring at top of file
   - Comments adjacent to `ICSA` / `CCSA` series-id constants
3. **Resolution:**
   - If yang attributes ICSA/CCSA to "BLS" in ANY label/comment/metadata → **rename to "DoL ETA"** (or "DoLETA" or "Department of Labor — Employment and Training Administration"; pick a consistent canonical spelling and update all sites). FRED-mirror access path stays unchanged (FRED is operationally canonical; yang just labels the upstream attribution correctly).
   - If yang correctly attributes (no false BLS claim anywhere) → **no code change; close as misclassification-class non-finding** (the inflight ~B brief flagged a possible attribution gap but yang's code already attributes correctly).

### Finding #5 — "Industrial Productivity" INDPRO yang-label-variant

**Source:** ~A FRED brief `da862a6c6` §5 (FRED-REPRESENTATIVE class) + ~B BLS §6. Yang labels `INDPRO` (FRED Industrial Production Index, FRB G.17 release) as **"Industrial Productivity"**. This is a cosmetic label-variant — Production ≠ Productivity:
- **Industrial Production (INDPRO):** aggregate physical output of industrial sector (FRB G.17 release, monthly). Index.
- **Industrial Productivity:** output-per-unit-labor (BLS Productivity Program; series like `PRS85006112` or `OPHNFB`). Different concept.

Yang's "Industrial Productivity" label for the INDPRO series is **misleading** for any downstream consumer who takes the label at face value (they expect labor-productivity; they get aggregate-production-index).

**Audit ask:**

1. **Read** yang-generate-macro Lambda code — locate every reference to the INDPRO series + its label string.
2. **Verify** the label string emitted for INDPRO (in output JSON / metadata / docstrings / comments).
3. **Resolution:** rename label **"Industrial Productivity" → "Industrial Production"** at every site. LABEL-only change. **No series-id change** (yang continues to pull `INDPRO` from FRED). **No pipeline-correctness impact.** Portal/consumer-side label may need parallel update — flag as follow-on DE/portal task if portal hard-codes the label string (`portal/src/pages/Macroeconomics/` per L1 lineage map).

---

## §2 — Acceptance criteria

- **AC1 (Finding #3):** ICSA/CCSA attribution label in yang-generate-macro Lambda VERIFIED. Either (a) attributes to BLS anywhere → renamed to DoL ETA at every site, or (b) attributes correctly → no-op confirmation banked as misclassification-class close.
- **AC2 (Finding #5):** INDPRO label "Industrial Productivity" identified + renamed to "Industrial Production" at every yang-side site (code + comments + docstrings + output metadata + any yang-internal documentation).
- **AC3:** No series-id changes. No pipeline-correctness impact. Existing yang test suite (if any) passes unchanged.
- **AC4:** ds-commit-gate.sh exit-0 on any touched Python files. Ruff + py_compile clean per CLAUDE.md Rule 14.
- **AC5:** RAVC2 packet to ws COO citing concrete commit hash + AWS Lambda deploy verification (if Lambda code changed; if no-op for #3 + label-only for #5, the resolution path: write code → write Terraform → update source map → git commit → terraform plan → terraform apply → 0-diff verify → tag → push --follow-tags per CLAUDE.md Rule 1-6). Portal follow-on flagged separately if portal-side label hard-codes "Industrial Productivity" string.

---

## §3 — Cross-cutting + dependencies

- **Depends on:** read access to `infra/aws/lambda/yang-pipeline/yang-generate-macro/lambda_function.py` + any associated `.json` config files + DT 0.1.0 standard pod-3 owned-paths
- **Blocks:** nothing (cosmetic; Phase 2 verdict-confidence tracking can absorb any label-class anomalies post-rename if surfaced)
- **Sibling:** Phase 2c TO-009 RE test-pulls verdict-confidence will benefit from clean attribution labels but does NOT gate on .011 completion
- **Andrew Q3 + Q4 (Ted Spread DISCONTINUED + PPI modern/legacy) — separate sovereign-class architectural calls — NOT in .011 scope** (those are Andrew-pending Q3+Q4 from /drive cycle 112 user-facing close; will route as separate items when Andrew rules)

---

## §4 — Effort estimate

~30-60min DT 0.1.0 wall time. Read-verify pass + 2 label updates (or 1 update + 1 no-op confirmation) + commit + terraform-apply + RAVC packet. Light-touch FIX-class scope.

---

## §5 — Notes

This TO is the deferred-from-cycle-0042 bundle per ws CTO commitment in cycle 0042 per-tick log `org/tier1_exec/1.0.0_SA_CTO/logs/2026-05-26/ws-charter_2207Z.md`. Cycle 0042 priority went to Andrew HAR substrate triage; cycle 0043 absorbs the cleanup bundle alongside the substitute-security doctrine codification + 2 PRD addenda.

**Status:** complete-partial (AC1 done; AC2 deferred out-of-FIX-class-scope per ws CTO Path C ruling 20260526T231839Z)
**Authored:** 2026-05-26 ~22:35Z (cycle 0043)
**Dispatched:** 2026-05-26 ~22:46Z (MSTR spawn-with-direction)
**Started:** 2026-05-26 ~22:50Z (DT 0.1.0)

---

## §6 — Execution log

### AC1 — VERIFIED NO-OP (close as misclassification-class non-finding)

Grep across `infra/aws/lambda/v2_portal/yang_pipeline/**`, `infra/aws/lambda/fred-macro-ingestion/`, `infra/aws/lambda/fred-data-ingestion/`, `data/yang_macros_re/**` for `BLS` / `Bureau of Labor`:
- **Zero matches anywhere.** No false BLS attribution claim is made for ICSA / CCSA (or any other series) in any yang-side or FRED-ingest Lambda or yang_macros_re module.
- `data/yang_macros_re/adapters/fred_adapter.py:68-69` already explicitly comments `"DoL ETA mirror -- NOT BLS"` for ICSA + CCSA (correctly attributed).
- yang-generate-macro uses Bloomberg tickers (`INJCJC   Index` / `INJCSP   Index`) for jobless claims; no attribution label string in code.

**Resolution path (b) from TO §1 Finding #3:** AC1 = no-op. Closed as misclassification-class non-finding.

### AC2 — BLOCKED on architectural coupling

**Issue surfaced during implementation:**

The MACRO_GROUPS key in `yang-generate-macro/lambda_function.py:41` (`'Industrial Productivity MoM'`) is load-bearing as the JOIN key against `df['index_name']` from the upstream Bloomberg-fed PKL (yang's `market_indices_data_pull.ipynb` assigns `index_name` from the same dict). The INDICATORS list entry in `yang-generate-macro-timeseries/lambda_function.py:27` carries the same coupling, AND the portal `MacroTimeSeriesModal` slugifies the indicator name client-side -> the per-indicator timeseries filename in S3 must match the slug the portal computes from its own indicator list.

A naive rename of `'Industrial Productivity MoM'` -> `'Industrial Production MoM'` at every yang-side site SILENTLY DROPS INDPRO from `macro_data.json` output (JOIN miss against PKL's `index_name`), contradicting the TO's "no pipeline-correctness impact" claim.

**Decoupled-override workaround attempted** (introduce `INDICATOR_LABEL_OVERRIDES` map; keep match key on PKL side, translate to corrected label only at emit time; keep slug filename on old key for portal modal compat): **reverted** — signal: wrong approach.

**Concrete unblock needed** — ws CTO design call between:
- **Path A — Coordinated full rename** across yang's notebook PKL gen (`market_indices_data_pull.ipynb`) + yang-generate-macro + yang-generate-macro-timeseries + fred-macro-ingestion + portal `indicators.ts` + portal `MacroTimeSeriesModal.tsx`, all shipped together; AC5 portal follow-on becomes IN-SCOPE not OUT-OF-SCOPE.
- **Path B — Decoupled output-label rename via override map** (as attempted + reverted) — keep PKL match keys intact; rename only the emit-time label and filename slug coordinated with portal-side; lower blast radius but more code surface area.
- **Path C — Defer the rename entirely** until portal-side label update lands first (portal owns the slug-compute chain; yang follows portal's choice).
- **Path D — Other** (CTO design).

Routed via [BLOCKED-ASK] -> ws COO -> ws CTO. Resume on UNBLOCK_RECEIVED with chosen path.

### AC2 — RULING: Path C (DEFERRED out-of-FIX-class-scope)

ws CTO ruled 2026-05-26 ~23:18Z (`20260526T231839Z_1.0.0_SA_CTO__CTO_RULING_Path_C__YALP_MACROS.011`):

- **Path A** (coordinated-full-rename across yang notebook + 2 Lambdas + portal x2 + fred-ingest) is structurally OUT of FIX-class scope premise ("cosmetic LABEL-only; no pipeline-correctness impact").
- **Path B** (decoupled-override map) reverted in-context = "wrong approach" signal accepted.
- **Path C** is doctrine-aligned: portal owns the slug-compute chain (`indicators.ts` canonical for portal-side); yang follows portal's choice; portal-initiated rename safely cascades down.

**Disposition:** AC1 NO-OP CLOSED (banked as misclassification-class non-finding). AC2 DEFERRED out-of-FIX-class-scope (NOT failed; explicitly carved-out per Path C). Future coordinated-rename = a fresh dedicated project (candidate `YALP_LABELS.001` or `ADHC_INDLBLS.001`), portal-side-initiated.

**TO status:** `blocked` -> `complete-partial`.

### AC3-AC4 (deploy/gate) — N/A

No code changes shipped per Path C; pre-commit gate had been verified clean for the reverted override-map proposal; no Terraform plan/apply needed.

### AC5 — RAVC2-Status

Routed to ws COO with CC ws CTO (TO author) + ~A (Finding #5 source) + ~B (Finding #3 source) per TO CC list.
