# NFRA_LOCALROOT -- decomposition + P2 taxonomy DIRECTION (base COO, 2026-07-08, Andrew-direct via CTO)

**PRD:** docs/architecture/NFRA_LOCALROOT_PRD.md (CTO, commit 168c5d7b1). **Owner:** 2.0.0_SA_COO (base -- CTO-assigned as the TERRAFORM-coupled infra-structural parent; SS9 Q1 resolved). **Why now (not at-cadence):** COO~B's NFRA_SYSTEM-P2 is GATED on this LOCALROOT-P2 taxonomy; resolving the gate is the drive-imperative move.

## Phase plan (who does what)

- **P1 FS AUDIT (read-only)** -- COO-authored (structural analysis, my lane). SEEDED below from the live /infra audit 2026-07-08; the full per-knowledge-class SSOT map is P1's completion deliverable.
- **P2 THE PLAN / TAXONOMY (core)** -- COO-authored. The DIRECTION is settled below (enough to unblock COO~B's placement); the complete taxonomy table + migration map + index design is P2's deliverable, CTO-arch-gated before any execution.
- **P3 STRUCTURAL EXECUTION** -- AE infra-lane (owned-paths), COORDINATED with COO~B (infra/ is a shared/contended lane) + TERRAFORM-P3 + SYSTEM-P2, so the three land ONE coherent /infra. Git-tracked, reference-preserving, reversible.
- **P4 ANTI-SCATTER CONVENTION** -- COO-authored convention + a light advisory gate (AE builds the check); test-fixture-fires acceptance.

## SS9 open decisions -- RESOLVED at decomp

- **Q1 (owner):** base COO. CTO-assigned; confirmed with COO~B in the 2026-07-08 lane-split (LOCALROOT/TERRAFORM = base COO; SYSTEM = COO~B).
- **Q3 (consolidate vs reference):** REFERENCE-IN-PLACE is the default for anything with an existing SSOT (git history, the live graph, org/, docs/architecture); CONSOLIDATE only genuinely-homeless tribal knowledge. No forked truth (one SSOT per class).
- **Q4 (index):** HYBRID -- a static structural index (infra/README.md, already exists) as the entry-point + the runtime-compiled current-state via NFRA_SYSTEM's comp-system compiler at infra/system/06_current_state (reuse SYSTEM P3; don't build a second index).
- **Q2 (the top-level taxonomy):** DIRECTION below; formally ratified in P2 (CTO arch-gate).

## P1 audit SEED (grounded on the live /infra, 2026-07-08)

/infra is ALREADY substantially organized -- this is a reconcile+index job, not a greenfield build. Live top-level:
- `infra/aws/` -- the cloud RESOURCES (terraform/ + ~28 per-service dirs: ec2, lambda, iam, cloudfront, secrets, ses, step-functions, globgrph, ... + docs/manifests). NFRA_TERRAFORM's domain.
- `infra/security/`, `infra/linting/`, `infra/orchestration/`, `infra/testing/` -- operational FUNCTION-classes (rightly-homed; keep).
- `infra/architectural_docs/` (decisions), `infra/prompts/`, `infra/rag/` -- knowledge/asset classes.
- `infra/website/` -- a PROJECT docs-home (my NFRA_WEBSITE; README index + resource-inventory + SVGs).
- `infra/README.md` + `launch_agents_powershell.ps1` at root.
- `infra/system/` -- does NOT exist yet (COO~B's SYSTEM-P2 creates it; gated on this).
GAPS/SCATTER (P1 to complete): the homeless tribal knowledge (session logs, commit-encoded decisions, loose infra/aws/docs) + duplication/staleness -- inventoried per-class in P1.

## P2 taxonomy DIRECTION (settled enough to unblock; formalized + CTO-gated in P2)

**HYBRID scheme -- by-knowledge-class at the top, project-docs-homes as a governed sub-pattern:**

1. **By-knowledge-class top-level homes** (the core knowledge domains):
   - `infra/aws/` = the ESTATE (cloud resources; TERRAFORM's terraform/ + per-service). 
   - `infra/system/` = the CONTENT (how-it-works; SYSTEM's substrate/graph/tools/federated/learning + `06_current_state` runtime output). **TOP-LEVEL, STABLE.**
   - `infra/security/`, `infra/linting/`, `infra/orchestration/`, `infra/testing/` = operational function-classes (keep as-is).
2. **Project docs-homes** = a RECOGNIZED, GOVERNED sub-pattern: `infra/website/` (and future `infra/<project>/`) for a project with substantial standalone platform docs -- governed by ONE convention (README index + resource-inventory + a cross-link UP to infra/README.md + registration in the index).
3. **The index** = `infra/README.md` (static entry-point routing to every knowledge-class home + registering each project docs-home) + the runtime current-state at infra/system/06_current_state (SYSTEM comp-system).
4. **Consolidate vs reference** (Q3): reference-in-place git/graph/org/docs-architecture (indexed from infra/README.md, not absorbed); consolidate only the homeless.

**This resolves CTO's arch-note:** website/ + system/ + aws/terraform/ are NOT three independent precedents -- they are instances of the ONE hybrid scheme (system/aws = by-knowledge-class homes; website = a governed project-docs-home), all registered in the infra/README.md index. No ad-hoc one-level-up scatter.

## The COO~B unblock (SYSTEM-P2 placement + index constraints)

/infra/system is a TOP-LEVEL by-knowledge-class home -- STABLE, will not move under the finer P2 taxonomy. COO~B may build its SYSTEM-P2 tree there now:
- **Placement:** `infra/system/` (README + 00_synthesis..07_maturity); the comp-system COMPILER stays in org/modules/graph (CTO Q1), its OUTPUT lands at `infra/system/06_current_state`.
- **Index constraint:** register `infra/system/` in `infra/README.md` (the SSOT entry-point) as the "system content" knowledge-class home; `infra/system/README.md` cross-links UP to `infra/README.md`.
- **Naming:** lowercase; the numbered-section internal structure is fine.
