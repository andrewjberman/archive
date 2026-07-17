# NFRA_COMPSIMILAR Phase-1 -- derive-at-scan corpus: STATUS + landing ask

**Author:** 0.8.0_AE_CloudComp · **Date:** 2026-07-17 · **Gate:** CTO arch-gate PASS @c3aa13d05
**PRD:** `docs/architecture/NFRA_COMPSIMILAR_PRD.md` (CTO-promoted) · **Engine home:** `org/modules/graph/debtscan/`

## What was built (the non-gated Phase-1 slice)
`summary_corpus.py` -- the **derive-at-scan** resource-summary corpus (CTO ruling 1: corpus v1 =
derive-at-scan). Synthesizes a per-ARN **functional summary** from the live graph (`comp-kuzu`):
`node_type + layer + edge neighborhood (producers/consumers/wiring)`. Reuses `dup_scan.BM25`
(Andrew engine intent). Table-independent + projection-independent by construction -- it needs
neither the gated Iceberg table nor the gated Kuzu projection to stand up.

**Runtime home:** `org/modules/graph/debtscan/summary_corpus.py` (colocated with `dup_scan.py`,
per PRD 4.1 "engine reuse lives at the debtscan home"). This folder holds the durable authored
copy under my lane; the runnable copy is in the working tree at the debtscan home.

## Evidence (grounded, this session)
- **commit-gate**: CLEAN (py_compile + ds-precommit + ruff py39).
- **`--self-test` (offline mutant gate)**: **PASS 4/4** --
  M1 corpus-collapse (name-same/purpose-diff -> LOW, score 0.0);
  M2 functional-twin (name-diff/purpose-same -> HIGH, score 1.0);
  M3 blind-row (no edges -> UNKNOWN-thin);
  M4 name-exclusion (own name absent from BM25 tokens).
- **Live `--build`** (graph vintage: graph_nodes 1.6h, Nessie HEAD current):
  **1894 ARN resources / 1550 summarized / 344 UNKNOWN-thin / 39 hold-marked** (matches the
  assessment's 1,894 ARN-bearing). Coverage denominator prints on every run.
- **Live `--neighbors arn:aws:s3:::opal-data-inf`**: opal-data-cot 0.911, opal-market-data-v2
  0.818, opal-data-smartx-v2 0.781, ... -- correct "does-the-same-JOB" signal. (opal-data-cot
  scoring high is EXPECTED: firm-separated data buckets do the same job; the Phase-2 `supersede`
  join adds the cross-firm suppressor + heat-divergence, so this does NOT false-flag as superseded.)

## Controls carried (PRD 5 -- controls, not care)
- **Corpus-collapse**: the BM25 document EXCLUDES the resource's own name (else comp-similar just
  re-runs comp-dups). Sourced from the edge neighborhood + type; neighbor names are functional context.
- **Blind-row / UNKNOWN-is-a-band**: a resource below the purpose-token floor is THIN=UNKNOWN
  (no twin *known*), never "unique"; coverage denominator is printed every run.
- **NO Description fallback** (CTO binding ruling 1): a thin summary stays UNKNOWN-band, never
  Description-patched (that re-opens the S3/DDB blindness).
- **Hold-aware**: `_HELD_RX` reused verbatim from `comp_debris` -- held/frozen/sovereign names marked.

## Held (gated -- NOT attempted this session)
- **`resource_summaries` Iceberg table**: held for CTO plan-gate on the pure-add NEW-TERRITORY TF
  diff (ruling 2b). OPAL_TAXONOMY-conformant from birth, no freshness-twin. Spec follows.
- **Kuzu LEFT-JOIN projection**: HARD DEPENDENCY on NFRA_KUZUSPLIT (ruling 2a) -- must compose with
  both full-projection AND incremental MERGE/DETACH-DELETE without dropping the editorial layer.
  Held until the KUZUSPLIT driver is assigned. Spec follows.

## The landing ask (CTO) -- owned-paths ANY_EXEC lane
`org/modules/graph/` is the ANY_EXEC lane (CTO/COO/CVO); my AE commit is correctly blocked --
the same reason you promoted the PRD under your author. Pick one (your call):
- **(a)** land the tested working-tree file `org/modules/graph/debtscan/summary_corpus.py` under
  your author (PRD-promotion precedent); or
- **(b)** grant NFRA_COMPSIMILAR a project-scoped, **grantor-landed** carve-out under
  `org/modules/graph/debtscan/` for the comp-similar files (`summary_corpus.py`,
  future `comp_similar*.py`, `.tools/comp-similar`) -- mirrors the yang-pipeline
  code-owner-gets-scoped-infra precedent (SoD: I do not commit my own grant) -- so I land
  Phase-1/2 directly.

Registration invariant (`comp-manifest-check`) binds on the executable landing (Phase 2) -- not yet due.
