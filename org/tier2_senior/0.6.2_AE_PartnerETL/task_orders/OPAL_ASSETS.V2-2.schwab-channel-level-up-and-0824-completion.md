# OPAL_ASSETS.V2-2 — Schwab channel level-up + 0824 completion

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<go>Half (a) is ALREADY ARMED (your existing remap-on-pull-terminal plan, unchanged — this TO does not re-order it). Half (b) is new material: begin when (a) is landed or during armed-wait idle hours.</go>
<project>OPAL_ASSETS — V2 Phase I bronze close-out</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md §2 bar + V2-2 (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole</prd>

## THE GOAL — both master folders wrap per the §2 four-column bar
**(a) 0824 completion (armed, unchanged):** 0824 remap on pull-terminal (now ~5,928/5,966) + 13c 3-tier
verify + per-master live exercise. Your existing sequence stands verbatim.
**(b) si2 puller level-up (new):** the 0833/0824 puller is MID vs the C5 standard (PRD §1: 13c +
session-lock + T1-ruled, but NO set-identity landing guard, NO persisted manifest). Add:
- set-identity landing guard — shortfall AND surplus, verdict on ListObjectsV2 landed bytes, mutant
  transcript committed (the C2 lesson: assert DISTINCT LANDED KEYS / set-identity, never a write tally).
- persisted per-pull meta manifest under `{source}/{scope}/meta/pulls/` (ruling 21 home).
KEEP: 13c 3-tier copy verify, session-lock, T1 recon stays a SILVER-parser control (not bronze's job).

## SEQUENCING (unchanged, explicit)
0824-terminal -> per-master exercise + 0824 remap -> V2-3 deletion chain (Andrew GO -> your temp grant
[at CTO's gate now, routed 05:58Z] -> delete off EXACT key list @ 2cc0f8fee -> guard re-run, baseline
2,269 -> 0) -> (b) level-up whenever it fits without delaying the above.

## <compiler_tools_mandate>
PRD §2 bar col 3, verbatim: "IAM CLEAN (22a, 'no fucked up iams') — per producer role: live
`simulate-principal-policy` on the EXACT ARNs it writes/reads, ONE `--resource-arns` per call, positive
controls as SEPARATE invocations, negative controls = a firm bucket + the Door-6 sentinel key + an
out-of-scope monolith prefix. Recorded simulate outputs are the evidence; a comp-iam GREEN is not."
Every .py `from __future__ import annotations` (Rule 15). `.tools/commit-gate.sh` pre-commit.
Denominators enumerated AT RUN TIME (13b), never quoted from a doc.
</compiler_tools_mandate>

## <cross_domain_coordination>
New-territory: additive only. The reap role is SEPARATE (opal-c2-orphan-reap-role); the remap role stays
delete-incapable — that property is preserved, never amended. Nothing touches INF/bd/cot planes. Nothing
writes the Door-6 key. Glacier 257 stays background fill (Andrew: holds up nothing).
</cross_domain_coordination>

## <acceptance_criteria>
1. Both master folders (schwab/08335338, schwab/08242234) wrap per the §2 bar — all four columns green,
   each cell cited to a live primitive (listing/simulate/schedule+landed-bytes).
2. Guard mutant transcripts committed for the puller (shortfall + surplus + collision).
3. Manifest lands per pull; listing-cited.
4. RAVC evidence to COO at each gate (as you already do).
</acceptance_criteria>
