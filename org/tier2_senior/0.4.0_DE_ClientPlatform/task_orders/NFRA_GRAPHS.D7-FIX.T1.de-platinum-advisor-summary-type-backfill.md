<to_id>NFRA_GRAPHS.D7-FIX.T1</to_id>
<project>NFRA_GRAPHS</project>
<title>D7-FIX T1 — PlatinumAdvisorSummaryRaw type interface backfill (typed_field_count=0 → all 16 fields typed)</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (D7 real_bug #1, 164849Z RAVC2)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete — 2026-06-12T~1800Z by 0.4.0_DE_ClientPlatform; commit 8b6a6466 (portal DEV)</status>
<priority>high — 4 components × 2 firms silently treating all platinum advisor data as `any`</priority>

<scope>
Update `PlatinumAdvisorSummaryRaw` (BD variant) and `getPlatinumAdvisorSummaryStaticInflectionRaw` / `InflecAdvisorBookRaw` (INF variant) in portal/src to type all S3 envelope fields.

Source of truth: pre-cached adapter-audit YAMLs:
- `org/modules/graph/adapter-audit/getPlatinumAdvisorSummary.yaml` — 16 top-level fields (active_since, advisor_key, book, book_name, clients, composition, data_as_of, fee_summary, firm_id, generated_at, headline, relationship_stacked_periods, role_breakdown, summary, tax_exposure, top_holdings) + nested subfields
- `org/modules/graph/adapter-audit/getPlatinumAdvisorSummaryStaticInflection.yaml` — INF variant; also has TYPE-ONLY fields (concentration, mix, mix_periods) typed but absent from S3 — these may be legacy or removed; confirm and annotate

Affected components (BD): AdvisorBookView, ClientsTab, AdvisorPublicProfile, DistributionTab.
Affected components (INF): same via StaticInflection variant.

Also fix the ClientsTab `advisorBookData` state var type mismatch while in that file (D7-FIX T2 — bundled if convenient; separate TO filed either way).

Acceptance: `comp-adapter-audit getPlatinumAdvisorSummary` shows typed_field_count > 0; `comp-transform schema-check AdvisorBookView` (and peers) shows no `MISSING` on the newly typed fields.
</scope>

<acceptance_criteria>
- typed_field_count > 0 for both BD and INF PlatinumAdvisorSummary raw interfaces
- comp-transform schema-check: no new MISSING fields introduced; existing MISSING cleared for the typed fields
- portal TypeScript compile clean (bun run typecheck or equivalent)
- RAVC2 to COO with commit hash
</acceptance_criteria>
