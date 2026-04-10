<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-tax-exposure</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>complete</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Add a `tax_exposure` field to the `PlatinumAdvisorSummary` payload produced by the D_04 platinum publisher (and served by the `getPlatinumAdvisorSummary` Lambda path). The shape must match the existing `AdvisorBookResponse.tax_exposure` that is already consumed by `ClientsTab.tsx` on the admin book drill, so the new `AdvisorBookView` (shipped in .001) can render `TaxCostBasisPanel` on the non-admin Profile→Book toggle without bespoke field mapping. This is Wave 1, parallelizable with .001 and .002.
  </objective>

  <context>
    RD's AdvisorBookView.tsx (new file in .001) suppresses the tax panel today with `const tax = null` because `PlatinumAdvisorSummary` (from `getPlatinumAdvisorSummary`) doesn't carry book-level `tax_exposure`. Today that data only lives on the admin path's `AdvisorBookResponse` (used by ClientsTab L2 drill), which is served by a different Lambda endpoint entirely.

    Required shape (from RD briefing §5.4):
    ```typescript
    tax_exposure: {
      taxable: number
      taxable_pct: number
      tax_deferred: number
      tax_deferred_pct: number
      tax_free: number
      tax_free_pct: number
      capital_gains_ttm?: number
    }
    ```

    The pct fields are the three category $ values as fractions of total AUA (sum ~= 1.0 modulo rounding). `capital_gains_ttm` is optional — include it if it can be computed cheaply from existing sources, otherwise leave it off.

    Upstream source: likely the silver holdings + holding tax taxonomy tables that the admin `AdvisorBookResponse` already consumes. Check `data/black_diamond/scripts/gold/D_04.*` (platinum publisher) or `B_00.canonical_holdings.py` for how tax classification is currently done at the client-book level. The per-advisor rollup should aggregate across the advisor's full book (all clients, all accounts).

    Frontend follow-up (in the scope of .001 or a trivial .001-addendum): replace `const tax = null` with the live value in `AdvisorBookView.tsx`, the `{tax && <TaxCostBasisPanel>}` render lights up automatically.

    This TO is strictly additive. The new field must not alter any existing `PlatinumAdvisorSummary` consumer. All existing fields remain unchanged.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - `comp-blast getPlatinumAdvisorSummary` — identify the full consumer chain: D_04 publisher → platinum/advisors/{id}/summary.json → Lambda handler → frontend types. Confirm every consumer.
    - `comp-blast tax_exposure` — identify every existing producer and consumer of the tax_exposure shape. Confirm the admin `AdvisorBookResponse.tax_exposure` is the canonical shape and locate its producer (likely D_03 or D_04, or a client-book-level script in the gold chain).
    - `comp-pipescript io D_04.*` — capture current inputs and outputs of the D_04 platinum publisher. The new `tax_exposure` field must be producible from the same inputs without adding new silver reads.
    - Read the existing `AdvisorBookResponse.tax_exposure` production code (wherever it lives — likely a helper in a D_0X script or a shared lib module). Reuse the computation, do not re-derive.

    Phase 2 (before committing):
    - `comp-transform fields getPlatinumAdvisorSummary` — verify the new `tax_exposure` field appears in the type and is renderable from `AdvisorBookView.tsx`.
    - `python -m py_compile` on all modified Python files.
    - Run D_04 locally (dev transactions if available, or --dry-run if supported) against a known advisor. Verify the tax_exposure output matches the same advisor's admin `AdvisorBookResponse.tax_exposure` within rounding tolerance. If the two differ by more than $0.01 on any category, investigate before committing.

    Phase 3 (after committing, before gold run):
    - `comp-pipescript io` on the modified D_04 — confirm the new field is registered in the pipescript catalog.
    - `comp-blast` re-run — confirm no new downstream edges appeared unexpectedly.
    - Diff-before-ship: run the modified D_04 against a known production snapshot, compare the `platinum/advisors/{id}/summary.json` files before and after. Expected diff: new `tax_exposure` key added to every advisor summary. No other field changes.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `data/black_diamond/scripts/gold/D_04.*` (platinum publisher) — DS owns this script and the `PlatinumAdvisorSummary` output contract.
    shared_resource: `portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx` — RD authored in .001. Once .003 lands in the gold run, RD or DE makes a one-line frontend change (`const tax = null` → `const tax = summary.tax_exposure`) in a follow-up. This follow-up is NOT scoped to .003; DS does not touch frontend code.
    shared_resource: Existing `AdvisorBookResponse.tax_exposure` producer — DS reuses the computation logic. Do not re-derive from scratch.
    last_write_owner: 0.4.0_DS_ClientPlatform for D_04 and any shared tax-computation helper.
    required_action: "DS writes + ships the D_04 change + S3 deploy. A gold run is required to land the new field in platinum/advisors/{id}/summary.json files. DS coordinates with AE 0.6.0 / 0.7.0 on the gold re-run (can be folded into the next scheduled run — no dedicated run required)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **D_04 produces `tax_exposure`:** Every `platinum/advisors/{advisor_id}/summary.json` carries a `tax_exposure` key with the shape defined in §context. For advisors with zero holdings, the values are zero (not null, not absent — render-safe zero).
    2. **Shape matches admin path:** The field layout is byte-identical to the existing `AdvisorBookResponse.tax_exposure` used by ClientsTab.tsx L2 admin drill. Use the same producer helper if one exists; do not fork the implementation.
    3. **Pct fields sum to ~1.0:** For each advisor with non-zero AUA, `taxable_pct + tax_deferred_pct + tax_free_pct ≈ 1.0 ± 0.001`. Any advisor outside tolerance is flagged in the session log.
    4. **capital_gains_ttm decision:** Include the optional `capital_gains_ttm` field if it can be computed from existing silver/gold inputs without new queries. Otherwise document the exclusion in the session log with rationale (keep the type optional in the frontend so it can be added later).
    5. **Diff-before-ship:** Run modified D_04 against the latest production platinum snapshot. Diff the resulting `platinum/advisors/*/summary.json` files. Expected: exactly one key added, zero other changes. Log the diff summary (advisor count, categories breakdown, outlier list) in the session log.
    6. **Spot-check against admin path:** Pick 3 known advisors (Sam Owens, Alex Bright, one more from the Pod4 test set). Compare the new `tax_exposure` values against the admin `AdvisorBookResponse.tax_exposure` for the same advisor. Must match within $0.01 on every category.
    7. **No regression on other fields:** All existing `PlatinumAdvisorSummary` fields are unchanged byte-for-byte. Verified by the diff-before-ship.
    8. **Compile + commit + push + S3 deploy:** `python -m py_compile` clean. Commit with `--author=0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>`. Push to CLOUD. Upload modified `data/black_diamond/scripts/gold/D_04.*` (and any helper) to `s3://opal-data-bd/code/gold/`. Etag parity verified (local md5 == S3 etag).
    9. **Gold run coordination:** Send a broker message to 0.6.0_AE_PartnerETL or 0.7.0_AE_CloudOps requesting the next gold run pick up the new D_04. Do not trigger the gold runner directly unless Andrew says to.
    10. **Session log:** Documents the source-of-truth helper (reused or authored), the diff-before-ship output, the three-advisor spot-check, the `capital_gains_ttm` decision + rationale, commit SHA, S3 etag, and the Compiler Tools section.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.* (platinum publisher for advisor summary)</file>
      <file action="modify or reference">Existing tax-exposure helper (likely in a gold lib module or the admin AdvisorBookResponse producer)</file>
      <file action="reference">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx — frontend consumer (RD/DE follow-up, NOT scoped here)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Use the existing admin-path `AdvisorBookResponse.tax_exposure` computation. Do not re-derive. The two paths must produce identical values for the same advisor — any divergence is a bug.</requirement>
    <requirement id="2">The new field must be strictly additive. No changes to any existing `PlatinumAdvisorSummary` field. Verified by diff-before-ship.</requirement>
    <requirement id="3">Run the diff-before-ship harness BEFORE committing. If any advisor shows unexpected changes in non-tax-exposure fields, investigate and fix before shipping.</requirement>
    <requirement id="4">Do NOT trigger the gold runner in this TO. The new field lands on the next scheduled gold run (bd-gold-layer-runner at 22:00 UTC) unless AE/Andrew explicitly calls for a manual trigger. Send a broker message to AE so the team knows the change is staged.</requirement>
    <requirement id="5">Do NOT touch frontend code. `AdvisorBookView.tsx` already handles the `tax === null` case gracefully (suppresses the panel). Once the new field lands in the gold run, RD or DE makes the one-line `const tax = summary.tax_exposure` follow-up in a separate pass.</requirement>
    <requirement id="6">Follow the standard DS deploy protocol: code → commit (author attribution) → push CLOUD → S3 sync → etag parity scan. DS owns the full deploy cycle per `feedback_ds_commits_ae_deploys.md`.</requirement>
    <requirement id="7">`py_compile` is mandatory before S3 upload per `feedback_compile_before_upload.md`. Catches missing imports that would otherwise break the gold runner on first invocation.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">D_04 and any shared helper modified, committed on CLOUD with RD-style author attribution `--author=0.4.0_DS_ClientPlatform`.</deliverable>
    <deliverable type="s3_upload">Modified scripts uploaded to `s3://opal-data-bd/code/gold/`. Etag parity verified.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/advi_profil_003_tax_exposure.md` with diff-before-ship output, three-advisor spot-check, capital_gains_ttm decision, commit SHA, S3 etag, and Compiler Tools section.</deliverable>
    <deliverable type="message">Broker message to 0.6.0_AE_PartnerETL announcing the staged change and requesting gold-run pickup on the next scheduled run.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT re-derive the tax_exposure computation. Reuse the existing admin-path helper.</rule>
    <rule>Do NOT trigger the gold runner yourself. Announce the change and let the next scheduled run pick it up, or let AE/Andrew decide on a manual trigger.</rule>
    <rule>Do NOT touch any frontend code. Scope is strictly backend.</rule>
    <rule>Do NOT commit without running py_compile and diff-before-ship. Both are mandatory gates.</rule>
    <rule>Do NOT include PII in the log or in the gold-run diagnostic output.</rule>
  </do_not>
</task_order>
