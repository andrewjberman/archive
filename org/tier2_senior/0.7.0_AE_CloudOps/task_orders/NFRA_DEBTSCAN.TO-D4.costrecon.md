# Task Order: NFRA_DEBTSCAN.TO-D4
## COSTRECON — full cost-lever census + graph cost-attribution

**Project:** NFRA_DEBTSCAN (v0.2, Andrew-direct)
**Assigned to:** 0.7.0_AE_CloudOps
**Priority:** P1 (Andrew-direct, cost-attribution is a stated graph purpose)
**Authority:** CTO PRD v0.2 a5e58490e (Andrew-direct ~19:15Z 2026-06-12)
**Sequence:** queue after TO-D1 + TO-D2 AE RAVC2s (share AE 0.7 slot)
**Status:** queued -- gated behind TO-D1 + TO-D2 AE RAVC2s (shares the AE 0.7 slot); P1 Andrew-direct. (Status line added 2026-06-18 by COO -- file had no status tag -> /to-check [??] UNKNOWN.) -- SPRING-CLEAN 2026-08-25: project NFRA_DEBTSCAN is complete; TO last touched 2026-06-18 predates project close 2026-07-09. Record act, not a work verdict.

---

## Context

Andrew's framing (verbatim from PRD §2e): "we want to know every single one [cost lever] — this is the purpose of the Kuzu/Nessie graph; we should be able to immediately identify every single running process by costs."

**Day-0 empirical baseline already pulled by CTO (in PRD §2e, corrected a9586b33d):**
- May 2026 (full month): ~$601 — EC2-Compute $355.93 / S3 $83.17 / EC2-Other $64.76 / Lambda $22.33 / Secrets Manager $16.82 / VPC $13.46 / CloudTrail $7.17 / ECR $6.56 / WAF $6.00 / tail ~$25
- June 2026 MTD (06-01→06-12): $243.15, 30-day run-rate ~$608 — total flat:
  - EC2-Compute run-rate ~$259 (-27% — right-sizing showing)
  - **S3: CORRECTED — the apparent "+90%" was a LINEAR-EXTRAPOLATION ARTIFACT (CTO root-caused a9586b33d). Storage is FLAT (~$43/mo). The delta was a TWO-DAY GET burst (06-09/10, ~78M requests ~$31 = GLOBGRPH bring-up: pre-F4 full-table re-MERGEs + pyiceberg small-file re-scans), back to baseline 06-11/12 — empirically confirms F4+F6 ended the pattern. Ex-burst June S3 run-rate ~$80 ≈ May's $83. NOT a worked finding for this TO — already root-caused.**
  - Lambda run-rate ~$41 (+84% — 2b incremental class)
  - ECS/Fargate newly present (Nessie)
  - Secrets Manager steady ~$17/mo (~42 secrets — census the set)

**Boundary with NFRA_COSTAWS:** COSTAWS = remediation actions (retention floors, right-sizing). DEBTSCAN-COSTRECON = census + attribution that tells COSTAWS where to aim. These are complementary, not competing.

---

## Scope

### Phase 1 — Full lever enumeration (EVERY lever, no silent caps)

1. Cost Explorer service → resource → owning-process mapping:
   - Usage-type group-bys below the service grain (not just service totals)
   - Tag group-bys (identify which tag key/values own which costs; flag untagged = attribution gap)
   - Cover the long tail — every line item, not top-N
   - CE API calls are read-only and pennies (LD-0176 cost-governance fine ad-hoc)

2. S3 +90% run-rate divergence — ROOT CAUSE (first worked finding):
   - Candidates from PRD: GLOBGRPH snapshots/warehouse/versioning
   - Run S3 storage-lens or CE resource-level filter on opal-313476888478-globgrph
   - Cross-reference with noncurrent version policy + NFRA_COSTAWS R2 lifecycle changes
   - File as a real finding with root-cause chain

3. Secrets Manager census (~42 secrets identified):
   - List all secrets, tag them to owning service/pipeline
   - Flag any secrets for decommissioned services

### Phase 2 — Graph cost-attribution (kuzu node enrichment)

Add `cost_mtd_usd` as a node attribute on the Kuzu graph:
- Join CE resource-level data (ARN-keyed) to kuzu nodes
- Coverage: every node with an identifiable ARN (Lambdas, EC2, ECS, S3 buckets, etc.)
- Vintage-stamp the attribute via the F6 marker (same pattern as other node attributes)
- Proof-of-value query: `MATCH (n) WHERE n.cost_mtd_usd > 0 RETURN n.name, n.type, n.cost_mtd_usd ORDER BY cost_mtd_usd DESC LIMIT 20` — every running process by cost in one Cypher query

### Phase 3 — Ledger filing

File into: `org/modules/graph/debtscan/2026-06-12_D4_costrecon_ae.md` (date prefix may update if this runs next day)

Per-finding format:
```
| family | tool | resource | finding | cost_impact | owner-lane |
```

§3 precision gate: CVO-adjudicated before promoting above ADVISORY.
Critical-paths cross-filing (§4) for any finding touching a critical surface.

---

## Acceptance Criteria

- AC1: Full lever enumeration table (service → resource → process; every line item with usage-type)
- AC2: S3 +90% root-caused with evidence (GLOBGRPH or alternate candidate confirmed/ruled out)
- AC3: Kuzu graph has `cost_mtd_usd` attribute on ARN-keyed nodes; proof-of-value Cypher query output
- AC4: Secrets Manager census (42 secrets, owning service, decommissioned flags)
- AC5: Zero CE mutations (read-only; no resource changes)
- AC6: Ledger filed with provenance header (CE vintage stamp)

---

## Zero-mutation guarantee

Read-only CE API calls + kuzu attribute writes only. No AWS resource changes, no S3 writes to live pipeline data, no Terraform.

---

## RAVC2 to COO

Include in body:
1. Commit hash (kuzu enrichment script + ledger)
2. Top-10 cost nodes from the Cypher query (proof-of-value)
3. S3 root-cause evidence (2-3 lines)
4. AC5 confirmation (0 mutations)

CC 3.0.0_SA_CVO on RAVC2.

---

*Dispatched by 2.0.0_SA_COO 20260612T192300Z*
*CTO PRD v0.2 a5e58490e (Andrew-direct)*
