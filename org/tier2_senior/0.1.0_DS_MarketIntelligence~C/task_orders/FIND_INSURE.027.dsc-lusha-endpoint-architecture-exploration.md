# FIND_INSURE.027 — LushaAI endpoint architecture exploration + bucket-implication matrix (DS~C)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.4+ §4 Phase 2A + Lusha API v3 reference `docs/reference/lusha-api-v3.md`
**Pod:** 0.1.0_DS_MarketIntelligence~C
**Lane:** DS_MarketIntelligence ~C (Phase 2A LinkedIn-pipeline architecture + exploration)
**Issued to:** 0.1.0_DS_MarketIntelligence~C
**Author:** 2.0.0_SA_COO 2026-05-27T~23:28Z (cycle 165 Andrew 23:25Z parallelize-directive exploration TO)
**Sizing:** ~4-6h wall (structured exploration + documentation artifacts; no live API calls — references-only deep-dive)
**Authority anchor:** Andrew direct 2026-05-27T~23:25Z verbatim: "exploring lusha endpoint data structure and how this informs bucket structuring and downstream analytics shape/optionality" + 2026-05-27T~23:26Z verbatim: "have them document their findings in structured format" + Andrew goal-set 22:49Z FIND_INSURE end-to-end drive.

<status>complete</status>

**Completion 2026-05-27T~23:58Z (0.1.0_DS_MarketIntelligence~C):** All 4 structured artifacts shipped. AC1 `docs/reference/lusha-endpoint-architecture-map.md` (per-endpoint deep-dive + cost/rate/error/coverage); AC2 `docs/architecture/find-insure-bucket-structuring-implications.md` (per-endpoint silver schema + cross-endpoint joins + per-endpoint silver/per-data-class gold recommendation); AC3 `docs/architecture/find-insure-downstream-analytics-shape-options.md` (Phase 3 hybrid Option C MUST-HAVE v0.1 + Lookalike-expansion Pattern 2 v0.2 + Webhook real-time Pattern 3 v0.3); AC4 `docs/reference/find-insure-phase2a-endpoint-decision-matrix.md` (8-step per-IMO execution chain + failure-mode + cost-gate). AC5 doc-of-record discipline met (header + author + date + authority chain + cross-refs). AC6 no live API calls (cost = $0). AC7 sister-coord MCP sent to DS~B at draft-of-AC3 moment. AC8 CVO architectural brief cross-ref inline in each artifact (zero divergence; 2 extension recommendations additive to CVO baseline). AC9 W1 threshold semantics flag surfaced in AC3 §8 for ws CTO REPAIR-AMENDMENT scribe.

## Objective

Deep-dive each LushaAI v3 endpoint (Search + Prospecting + Enrich + Search-and-Enrich + Lookalikes + Signals + Webhooks) + map per-endpoint response data shape + derive bucket structuring implications + author downstream analytics shape/optionality matrix. **Deliverables are structured documentation artifacts** per Andrew 23:26Z directive — NOT live API calls (cost-gated until Andrew Q1 ratify) + NOT new Lambda code (.011 skeleton already covers code substrate). This is exploration + design synthesis.

## Acceptance criteria

- **AC1.** **Structured artifact 1: `docs/reference/lusha-endpoint-architecture-map.md`** — per-endpoint section covering:
  - Endpoint name + HTTP method + URL pattern + auth model
  - Required + optional request params (with Lusha v3 doc citations)
  - Response JSON shape (top-level keys + nested structures + array members + dtypes; include sample-response snippets where ref-doc provides)
  - Rate limits + cost-per-call (if documented in `docs/reference/lusha-api-v3.md` or `https://docs.lusha.com/apis/openapi/section/data-source-and-privacy`)
  - Coverage classes (which decision-relevant fields each endpoint surfaces: Series-license, tenure, title-seniority, AUM, named-individuals, etc.)
  - Webhook-specific: trigger events + payload shape + GDPR opt-out integration per .011 AC5 scaffold
- **AC2.** **Structured artifact 2: `docs/architecture/find-insure-bucket-structuring-implications.md`** — derives bucket prefix conventions from endpoint response shape:
  - Per-endpoint silver schema mapping (bronze=raw Lusha JSON → silver=Rule-17-passthrough per CLAUDE.md Rule 17)
  - Cross-endpoint reconciliation (e.g., Search returns company-list; Enrich returns per-person detail — how do they join? composite-key vs deduplication strategy)
  - Bucket prefix recommendations: `corp/{slug}/silver/linkedin/search/` vs `corp/{slug}/silver/linkedin/enrich/` vs `corp/{slug}/silver/linkedin/signals/` — per-endpoint OR per-data-class
  - History-archive class: which endpoints' outputs need `serving/_history/...` retention per CVO Q-B ruling
  - Cost-state DDB integration: which endpoints feed `find-insure-cost-state` table for per-call cost tracking
- **AC3.** **Structured artifact 3: `docs/architecture/find-insure-downstream-analytics-shape-options.md`** — analytics optionality matrix:
  - Phase 3 serving table shape options (per-company aggregate vs per-employee detail vs hybrid table)
  - Cross-IMO analytics (e.g., Series-license density across universe; M&A signal aggregation; corp-finance hire correlation with rollup_score)
  - Lookalikes-driven universe-expansion (if Lookalikes endpoint surfaces "similar to top-tier IMO X" → procurement signal beyond 99-IMO source list)
  - Signals + Webhooks continuous-monitoring sub-class (per PRD §4 Stage 3 enrichment-overlay framing)
  - Recommendation: 2-3 concrete "downstream analytics" patterns ranked by IR-team-utility + implementation-cost
- **AC4.** **Structured artifact 4: `docs/reference/find-insure-phase2a-endpoint-decision-matrix.md`** — per-Phase-2A-execution endpoint-selection rules:
  - Which endpoint(s) fire per-IMO per Q1 subset rule (Search + Prospecting always; Enrich conditional; Signals deferred to Stage 3)
  - Endpoint-call-ordering + dependency chain
  - Failure-mode handling (Lusha API errors, rate-limit backoff, partial-response handling)
- **AC5.** All 4 structured artifacts conform to canonical doc-of-record discipline: title + author + date + authority-chain header + per-section markdown structure + cross-reference links to `docs/reference/lusha-api-v3.md` + PRD §4 + FIND_INSURE.json
- **AC6.** No live LushaAI API calls; no LushaAI API key extraction; cost = $0; this TO is exploration + documentation only
- **AC7.** Spot-check coordination with DS~B (sister-lane Phase 2A gold scoring) at draft-of-AC3 moment — DS~B's scoring weights consume your endpoint-coverage findings; sister-coord prevents downstream re-cycle
- **AC8.** Cross-reference each finding against `org/tier1_exec/3.0.0_SA_CVO/responses/20260527T1620Z_to_1.0.0_SA_CTO_opal_data_imo_bucket_architecture_brief.md` (CVO architectural brief that v0.3 absorbed) — note any divergence + propose reconciliation
- **AC9.** Cross-domain coordination block: explicit note for ws CTO REPAIR-AMENDMENT (b)(i) W1 threshold semantics scribe — your endpoint-decision-matrix AC4 informs what classification labels Phase 2A produces per-IMO

## Dependencies

- **`docs/reference/lusha-api-v3.md`** — already landed pre-reboot per Andrew direct 2026-05-15 supply
- **PRD `docs/architecture/FIND_INSURE.md` v0.4+** — §4 Phase 2A + §3.7 KMS cost-gate + §4 Stage 3 enrichment-overlay sub-section
- **`docs/reference/find-insure-canonical-url-list.md`** if exists — provides Lusha doc URL anchor
- **FIND_INSURE.011** — Phase 2A skeleton bundle; your exploration informs the IF-NEEDED v0.2 refinement of `.011`'s Lambda skeletons (e.g., if Search response shape requires multi-tier silver, .011 amends silver schema)
- **NO API key extraction** — this is exploration via reference docs only

## Sequencing — exploration phase

1. ~1h: read Lusha API v3 reference doc end-to-end + PRD §4 + CVO architectural brief
2. ~1.5h: AC1 — author `lusha-endpoint-architecture-map.md` (per-endpoint deep-dive)
3. ~1h: AC2 — author `find-insure-bucket-structuring-implications.md` (shape → bucket)
4. ~1h: AC3 — author `find-insure-downstream-analytics-shape-options.md` (optionality matrix)
5. ~30min: AC4 — author `find-insure-phase2a-endpoint-decision-matrix.md` (execution rules)
6. ~30min: AC7 sister-coord with DS~B + AC8 cross-ref against CVO brief
7. ~15min: commit + RAVC2-Request

**Total ETA:** ~5h wall from spawn-LIVE.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.027 — LushaAI endpoint architecture exploration + 4-artifact documentation` to ws COO. CC ws CTO + ws CVO + DS~B (sister-coord). Body: commit hash + per-artifact summary + key findings (e.g., "Search + Enrich joined via lusha_person_id; bucket prefix per-endpoint preferred over per-data-class for audit clarity"; "Lookalikes endpoint enables Stage 3 universe-expansion at ~$0.50/call — out-of-v0.1 scope but flagged as procurement candidate for v0.2") + decision recommendations.

## Compiler tools mandate

- N/A this TO (exploration + documentation; no code changes; no comp-* tool dependencies)
- Optional: `git log --all --grep="lusha" --oneline` to find prior Lusha-related commits for context

## Cross-domain coordination

- **FIND_INSURE.011** — Phase 2A skeleton bundle; your endpoint-decision-matrix AC4 may surface v0.2 refinement candidates (additive — no break)
- **FIND_INSURE.024** — Phase 2A LIVE-DISPATCH (your other staged TO); your endpoint-decision-matrix AC4 directly informs the .024 per-IMO Lusha invocation sequence + .024 cost-budget refinement
- **FIND_INSURE.023** — DS~E serving consolidation; your AC3 downstream analytics matrix informs .023's `serving/employees.json` + cross-IMO analytics surface
- **CVO architectural brief absorption** — AC8 ensures your exploration is anchored on the v0.3 CVO architectural ground-truth + surfaces any drift

## Notes

- Per Andrew 23:25Z parallelize directive — this TO is concurrent with .024 (LIVE-DISPATCH) + .011 (skeleton) + others. Your DS~C lane carries the architecture-design + execution-driver dual role.
- Per Andrew 23:26Z structured-format directive — every finding lands as a doc-of-record artifact, not inline-only commentary. Future-CL-CTO + future-MSTR + future-Andrew + future-IR-team all consume these artifacts.
- Per [[feedback_silver_no_field_slimming]] / Rule 17 — your bucket-structuring AC2 must explicitly respect Lusha-passthrough at silver layer; gold is where filtering/aggregation happens.
- Per CVO ADDITIVE-1 IR-team-individual identification gate (pre-Phase-3): your AC3 downstream analytics shape options inform what the IR team will see → identify the most-decision-useful shape upfront so IR-team feedback at sign-off is informed.
- Andrew direct 23:27Z "if you need any HARs now is the time to ask" — out-of-scope for this LushaAI TO (Lusha is API-only, no HAR class); applies to FIND_INSURE.025 + .028 Phase 2B job-board scope.

— ws COO 2.0.0_SA_COO 2026-05-27T~23:28Z — LushaAI endpoint architecture exploration per Andrew 23:25Z parallelize + 23:26Z structured-format directives
