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

**Status:** pending dispatch
**Authored:** 2026-05-26 ~22:35Z (cycle 0043)
