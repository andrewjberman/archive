<task_order>
<metadata>
  <to_id>ADHC_BDTSCLB.001</to_id>
  <project>ADHC (FIX-class hardening — no new project code, per CTO ruling 2026-06-03T1443Z)</project>
  <title>AE: make D_02 the single writer of bd advisor timeseries — remove build_advisor_timeseries from bd-portal-advisor-publisher (latent dual-writer clobber of 49F fee-split + NNA-mode fields)</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>1.0.0_SA_CTO (GO 2026-06-03T1443Z) — surfaced by DS 0.4.0 W2b + AE investigation</issued_by>
  <issued_date>2026-06-03</issued_date>
  <status>superseded</status>
  <superseded_note>SUPERSEDED 2026-06-03 — handed to 0.6.0_AE_PartnerETL (stand-down 145059Z); authoritative TO = 0.6.0 ADHC_BDTSCLB.001 COMPLETE (bd-v2.25.0, AC4 CVO-GREEN 2183b0524, .002 decommission). This 0.7.0 draft was stale-drift.</superseded_note>
  <priority>HIGH — protects ALREADY-SHIPPED 49F NNA-mode fee toggle (nna_canonical_fee_paying) + the incoming W2b total_aua_fee_paying. Land BEFORE/WITH W2b so the new field is born on the single-writer pipeline (CTO sequencing).</priority>
</metadata>

<scope>
## Problem (verified, not asserted — CTO superset-gate discipline)

The served `platinum/advisors/{id}/timeseries.json` (49F/BD) is bridged by D_04.client_portal_summary.py:725-729 from `gold/entities/advisors/{id}/timeseries.json` (snake_case key, s3_layout.advisor_timeseries_key). That gold key has TWO writers:

1. **D_02.advisor_client_detail.py** -> RICH (envelope {advisor_id,advisor_name,data_as_of,data}; per-row date/total_aua/cum_inflows/cum_outflows/nna PLUS architect/consultant/implementor/local_ops/addl per-role aua, *_fee_paying/_no_fee, nna_canonical, nna_canonical_fee_paying, inflows/outflows_canonical[_fee_paying], market_growth, synthetic_correction). Authoritative.
2. **bd-portal-advisor-publisher build_advisor_timeseries** (lambda_function.py:647, CALLED LIVE :1147) -> SIMPLE (same envelope; per-row only date/total_aua/cum_inflows/cum_outflows/nna). Writes `gold/advisors/{snake}/timeseries.json` then via the GLDRST dual-write (`_dual_write_key`, lambda:72-77, marked "Remove after .010") ALSO writes `gold/entities/advisors/{snake}/timeseries.json` — i.e. D_04's read key. `_advisor_id` snake_cases ('Travis Penfield'->'travis_penfield'), so the dual-write collides with D_02's snake_case key. (The Title-Case dirs under gold/advisors/ are STALE pre-snake-case leftovers, not current output — red herring.)

bd-portal-publisher fan-out-invokes bd-portal-advisor-publisher async on EVERY publish (lambda:1965). So the publisher's SIMPLE version is written to D_04's read key on every publish.

**Clobber:** masked TODAY only by cascade ordering (gold chain D_02 -> D_04 runs before the portal-publish fan-out fires the publisher; D_04 reads D_02's fresh rich gold). ANY ordering where the publisher's simple gold-write precedes a D_04 read -> served loses ALL rich fields = the SHIPPED 49F NNA-mode nna_canonical_fee_paying toggle AND the incoming W2b total_aua_fee_paying. This is the ADVI_DWSPLT dual-writer class (CTO).

INF is NOT affected: there the publisher IS the sole timeseries builder (DS's INF F11 fix correctly lives in the Lambda). BD differs because D_02 owns it.

## Fix (CTO-approved)
Remove `build_advisor_timeseries` (the :1147 call + the function) from bd-portal-advisor-publisher -> D_02 = sole gold producer of bd advisor timeseries; D_04 bridge unchanged. (Equivalent narrower fix = drop the timeseries case from `_dual_write_key` :74-75; CTO approved the function removal, which also stops the orphan gold/advisors/{snake}/timeseries.json write.) Confirm build_advisor_mix_timeseries / book.json dual-writes are NOT in scope (only the timeseries clobber).

## HARD GATE — superset proof before cutover (CTO)
- [x] FIELD-LEVEL (done): publisher envelope == D_02 envelope; publisher's 5 row fields {date,total_aua,cum_inflows,cum_outflows,nna} are a strict subset of D_02's row fields (verified vs live gold/entities/advisors/abby_horton/timeseries.json, 763 rows, 32 keys incl all 5).
- [ ] ADVISOR + ROW COVERAGE: D_02 enumerates >= the publisher's advisor set, and D_02's per-advisor date range >= the publisher's. Pre-cutover: D_04 enumerates served advisors from gold/entities/advisors/*/book.json (D_02 output) -> served set == D_02 set. Post-deploy: CVO served-parity (below) is the binding coverage proof.
- If any publisher field/advisor/date is NOT covered by D_02 -> STOP, do not cut over, BLOCKED-ASK with the gap.

<acceptance_criteria>
- [ ] AC1 — build_advisor_timeseries call (:1147) + function removed; no other publisher behavior changed (mix_timeseries, book, summary, etc. untouched). py_compile + ds-commit-gate pass.
- [ ] AC2 — Superset proof complete (field [done] + advisor/row coverage) BEFORE cutover.
- [ ] AC3 — Deploy: build-and-upload.sh -> source-map -> commit -> plan -> safe-apply (HALTGT) -> 0-diff -> comp-pipescript deployed MATCH -> comp-iam (expect no delta) -> tag bd-pipeline-v{next} + push --follow-tags.
- [ ] AC4 — POST-DEPLOY CVO served-parity: after the publisher no longer writes the timeseries key, run a full bd publish + confirm served platinum/advisors/{id}/timeseries.json retains ALL advisors, ALL dates, ALL rich fields (nna_canonical_fee_paying + W2b total_aua_fee_paying) with values matching D_02 -> proves D_02-sole-writer fully covers. (CVO independent verify.)
- [ ] AC5 — RAVC2 to CTO + COO with the proof + deploy evidence.
</acceptance_criteria>

## Sequencing (CTO)
Land this hardening BEFORE/WITH the W2b 49F gold run (DS D_02->D_04) so total_aua_fee_paying is born on the single-writer pipeline. W2b PROD run path = option (b) RAVC2-ACK-to-AE (AE owns the PROD EC2 bring-up + D_02->D_04, no publisher between) per DS 144443Z.

<compiler_tools_mandate>
- Before: comp-pipescript io / source-trace (done); comp-blast bd-portal-advisor-publisher build_advisor_timeseries (confirm no other consumer of the removed write).
- Before commit: ds-commit-gate (py edit on Lambda source).
- After: comp-pipescript deployed MATCH; comp-iam service bd-portal-advisor-publisher (expect no delta — removal only).
</compiler_tools_mandate>
<cross_domain_coordination>D_02/D_04 (DS-owned gold) — read-only dependency, no edit. W2b run (DS) sequenced after this. bd-portal-publisher fan-out (unchanged). Coordinate the post-deploy full-publish with DS/CVO for AC4 parity.</cross_domain_coordination>
</scope>
</task_order>
