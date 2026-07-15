# OPAL_ASSETS.V2-1 — ETF channel level-up to the C5 standard ("jazzed up and robust")

<issued_to>0.5.0_AE_OpalETL</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>pending</status> <!-- GO fired 2026-07-15 220354Z (COO, auto-fire clause on the GREEN 07-15 parity row) -->
<go>HARD GATE: tonight's 22:00Z first-fire proof (parity day-2 + first monolith bronze C4 AC1) lands and is reported CLEAN. COO issues the GO after reading that report. DO NOT touch the producer before its first monolith landing — parity evidence stays clean (CTO sequencing note, handoff 20260714T055215Z).</go>
<project>OPAL_ASSETS — V2 Phase I bronze close-out</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md §2.2 + §2 bar (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole</prd>

## THE GOAL
`etfs-netassets-daily` (954 lines) is BELOW the §2.4 C5 standard on exactly three CTO-source-read counts
(PRD §2.2). Close all three; nothing else in the script is in scope:
1. **No landed verify** — `_put_bytes` never reads back; written == call-succeeded, not landed (the C2
   write-count class). Build the set-identity landing guard: verdict on ListObjectsV2 landed bytes,
   shortfall AND surplus, RAISE loud.
2. **Manifest not persisted** — in-memory only. Land it per pull under `{source}/{scope}/meta/pulls/`
   (ruling 21 home; meta is NOT bronze, disjoint from guarded prefixes).
3. **urllib, zero retry** — one transient vendor hiccup degrades a tier. Replace with the
   requests+retry/backoff client pattern you built for C5 (reuse, do not re-derive).

KEEP what is already right (no-swallow writes, layout/header/values change detection that RAISES, the
source-tier ladder with degraded-tier reporting, fund-unavailable = hard fail, bronze/silver bucket
separation). The silver half stays writing the LEGACY bucket — correct during the parity window
(non-interference); its monolith-native parquet form is V2-8's, not yours.

## <compiler_tools_mandate>
PRD §2 bar col 3, verbatim: "IAM CLEAN (22a, 'no fucked up iams') — per producer role: live
`simulate-principal-policy` on the EXACT ARNs it writes/reads, ONE `--resource-arns` per call, positive
controls as SEPARATE invocations, negative controls = a firm bucket + the Door-6 sentinel key + an
out-of-scope monolith prefix. Recorded simulate outputs are the evidence; a comp-iam GREEN is not."
Every .py `from __future__ import annotations` (Rule 15). `.tools/commit-gate.sh` pre-commit.
comp-blast at authoring (COO, this TO): `comp-blast etfs-netassets-daily` -> no EXTRACTED downstream
edges (LOWER BOUND, not provably zero) — your changes are producer-side additive; re-check before any
change that alters an artifact KEY.
</compiler_tools_mandate>

## <cross_domain_coordination>
New-territory: additive only — guard + manifest + client swap inside the producer; no bucket/policy/
notification/schedule modification. Nothing writes `opal-data-inf/gold/meta/pipeline-complete.json`
(Door 6). The legacy CSV silver keeps serving until the ruled cutover (parity plan's own 3-day clock,
NOT V2's). Parity day-2/3 evidence ALWAYS outranks this TO.
</cross_domain_coordination>

## <acceptance_criteria>
1. Guard mutant transcript committed: shortfall + surplus + growth-boundary all RAISE (PRD V2-1 AC).
2. Manifest lands per pull under meta/pulls/ (listing-cited).
3. Next scheduled fire verified on landed bytes with the guard's OWN verdict (fire/run/land/verify,
   trading-calendar-resolved).
4. RAVC evidence to COO; CTO code-review gate on the producer diff before the deploy leg.
</acceptance_criteria>
