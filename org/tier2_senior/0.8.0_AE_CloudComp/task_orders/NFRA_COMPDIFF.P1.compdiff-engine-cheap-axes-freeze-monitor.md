# TASK ORDER — NFRA_COMPDIFF.P1

<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>HIGH (within prevention-tier) — Andrew-direct, born from the inf-AUA freeze. The P1 FREEZE-MONITOR is the standing guard against the value-froze-while-mtime-advanced class that bit us 3x today (cot/bd/inf). Sequences BEHIND the live priorities (it's prevention, not a fire) — start as you clear the S5 wrapper / post-#1.</priority>
<date>2026-06-29</date>

## Context

CTO authored + handed off NFRA_COMPDIFF (docs/architecture/NFRA_COMPDIFF_PRD.md, NFRA_COMPDIFF.json, REGISTRY) for P1-P3 decomposition. comp-diff is THE MISSING LENS: every existing tool checks the WRAPPER (mtime/existence/size), not the MOTION (is content genuinely changing). So a value can FREEZE while its timestamp keeps advancing — invisible. We hit that EXACT bug 3x TODAY: cot (canonical-seal), bd (xref), inf (the served AUA frozen at a 06-27 snapshot, re-stamped data_as_of=today, caught by Andrew Mon not by any alarm Sat). comp-diff x-rays any producer/consumer across all axes — each with a last-GENUINELY-changed content-fingerprint — and diffs vs a temporal anchor; the derived FROZEN-BUT-FRESH flag IS the 3x bug.

You are the natural P1 owner: you just built the Trino federation + used the S3 header_metrics.json VERSION-HISTORY to pin the inf freeze — i.e. you've already hand-run the exact value-motion check this engine automates, on the exact artifact class (served platinum/firm/*.json). Best-positioned.

## Objective

Ship the comp-diff ENGINE + resource model + temporal anchors + the CHEAP already-retained axes + THE FREEZE-MONITOR over served platinum/firm/*.json. P1 closes today's open class (frozen-but-fresh) with a standing guard.

## Scope — P1

1. **ENGINE + resource model + temporal anchors.** A resource (producer/consumer/artifact) x a set of AXES, each axis carrying a last-GENUINELY-changed content-fingerprint + a diff-vs-anchor (anchor = prior snapshot / N-days-ago / last-known-good). The derived **FROZEN-BUT-FRESH** flag = content-fingerprint stale while the wrapper (mtime/version-count/data_as_of) advanced. Conform to CTO's fixed drift-record contract (the unified board comp-drift/comp-diff share) + the vintage-primary / marker-oracle freshness-semantics (NOT newest-by-timestamp — the seam-5/6 finding: newest-S3-metadata != catalog-current; ground the AUTHORITATIVE current pointer).
2. **CHEAP already-retained axes** (no new infra — read what's already versioned): code (git), config (git), output-value (S3 object version-history — the header_metrics.json axis you used; parquet content-fingerprint), schema (parquet/declared-schema), freshness (existing comp-freshness surface), edges (graph). Each axis emits its last-genuinely-changed fingerprint + the diff.
3. **THE FREEZE-MONITOR (the P1 PREVENTION deliverable — priority-within-P1).** A standing monitor over served `platinum/firm/*.json` (+ the served-artifact class generally): for each served value-bearing field (e.g. total.aua), track the content-fingerprint across the S3 version-history; FROZEN-BUT-FRESH (value byte-identical across >=2 data_as_of advances, impossible on a live recompute) -> ALERT to the opal-critical-surface SNS (the COO SQS channel). This would have fired Sat 06-27 on the inf freeze. Wire it to the SAME critical-surface channel the COO /drive poll reads. Apply the abandoned-vs-genuine + premature disposition (don't false-fire on a deliberately-static field — declare the value-bearing fields).

## Shared dependencies (coordinate — do NOT duplicate)

- **SHARED P1 dep w/ NFRA_COMPDRIFT: the dynamic-prefix-read EXTRACTION enhancement.** INF_D_00's holdings/prefix read was INVISIBLE to the extractor -> the graph couldn't point at the freeze. ONE extraction-enhancement serves BOTH comp-diff (edge axis + --upstream) and comp-drift. Owner = the comp-tools/graph lane; coordinate with 0.7.0_AE + base-DS (who knows INF_D_00's reads). Sequence it as a shared P1 item — flag me to assign the single owner so it's not double-built.
- **SHARED Trino-query module (P3, but build-aware now): `.tools/_trino_fed.py`** — 0.8.0 already landed it (commit 7ed48fdc2) as the reusable in-VPC run-task->REST->CloudWatch substrate, per CTO's S5 ruling. comp-diff's output-value/schema axis for LAKEHOUSE data (P3) calls the SAME module — do NOT rebuild. NO persistent endpoint (SCTY-gated).

<compiler_tools_mandate>
- Reuse `.tools/_trino_fed.py` (the shared substrate) for any lakehouse-data axis; do not rebuild the transport.
- Conform to CTO's fixed drift-record contract (unified board) + vintage-primary freshness-semantics (ground the authoritative current pointer, not newest-by-timestamp).
- from __future__ import annotations; ds-commit-gate clean; no emojis/non-ASCII (CloudWatch-safe).
- Verify the freeze-monitor against a REAL served artifact (NEVER#7): replay the inf 06-27 freeze signature (or a constructed frozen-but-fresh fixture) -> confirm it ALERTS; confirm a genuinely-moving value does NOT false-fire.
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: PRD owner + the drift-record contract + arch-gate. RAVC the P1 build.
- 0.7.0_AE_CloudOps: the comp-tools/graph lane — co-owns the shared dynamic-prefix-read extraction (P1 shared dep) + the eventual P2 comp-drift orchestrator wiring.
- 0.4.0_DS_ClientPlatform (base-DS): knows INF_D_00's reads (the extraction-blind-spot source) + is fixing the inf freeze now — coordinate the freeze-monitor's served-field declaration.
- 3.0.0_SA_CVO: verifies the freeze-monitor fires on the real signature (NEVER#7).
</cross_domain_coordination>

<acceptance_criteria>
1. ENGINE + resource model + temporal anchors built, conforming to the fixed drift-record contract + vintage-primary semantics; FROZEN-BUT-FRESH flag derived correctly.
2. The cheap already-retained axes (code/config/output-value/schema/freshness/edges) each emit a last-genuinely-changed fingerprint + diff-vs-anchor.
3. THE FREEZE-MONITOR over served platinum/firm/*.json wired to the opal-critical-surface SNS -> COO SQS; VERIFIED it fires on the inf 06-27 frozen-but-fresh signature + does NOT false-fire on a genuinely-moving value (CVO co-verifies, NEVER#7).
4. The 2 shared deps coordinated (the extraction-enhancement single-owner assigned via COO; the _trino_fed module reused, not rebuilt). RAVC me + CC CTO + MSTR with the P1 engine + the freeze-monitor live.
</acceptance_criteria>

## Note
PREVENTION, not a fire — sequence behind the live priorities (the inf freeze itself is being fixed by base-DS now). But the FREEZE-MONITOR is the high-value standing guard against the class that bit us 3x today — it's the P1 priority-within-P1. P2 (heavier axes iam/infra/existence/size + --upstream cascade) + P3 (federation axis + comp-which promotion + nightly-sweep) follow as separate TOs. Decomposition brief: this TO's sibling. Do not self-wind to "tonight" — start as the S5 wrapper clears.
