# Task Order: NFRA_GLOBGRPH.TO-MAINT
## Nightly Iceberg maintenance — compaction + expire_snapshots + retention (closes never-built Item-1 leg)

**Project:** NFRA_GLOBGRPH
**Assigned to:** 0.7.0_AE_CloudOps
**Priority:** LOW-normal — ride the back of AE 0.7 queue (behind TO-D4 COSTRECON + TO-D1 iteration + COSTAWS W3/W4/W5)
**Authority:** CTO PRD v0.4.4 §3 + Andrew-ratified retention policy (29b36516b — docs/reference/record-retention-policy-v1.md)
**Boundary note:** TO-D4 COSTRECON *censuses/attributes* the Iceberg-maintenance gap (revised item b); THIS TO *implements* the remediation. Clean census-vs-action split.

---

## Context

The Item-1 "nightly Iceberg maintenance" leg was never built — only an ECR image expiry rule exists in globgrph TF. Per-commit metadata/data files grow unboundedly (3,096 already). This is the durable fix for the June 9-10 ~78M-GET burst class (small-file re-scan amplification). **Retention length is NOT the lever — file count is.** Compaction bounds file count; retention is a separate SOC-2 policy tier.

---

## Scope (derive_runner, post-marker-stamp step, best-effort/loud-fail — the marker-stamp pattern)

1. **Small-file COMPACTION + manifest rewrite** — bounds file count (the fix for the GET-amplification class).

2. **expire_snapshots + orphan-file cleanup** — `>=24h` grace cutoff (NEVER races 2b commits or in-flight canonical rebuilds); NEVER touches what the F6 marker references; orphan cleanup also sweeps c454b6cd-class artifacts.

3. **RETENTION = 13 months Nessie/Iceberg** — audit-baseline tags age out with their files; `>13mo` time-travel = tarball restore (indefinite tier). `snapshots/` prefix gets NO lifecycle expiry (policy: indefinite).

4. **Container rebuild to activate** — same sensitivity as prior globgrph deploys: land BEFORE a nightly or explicitly after (sequencing per the 240164dc precedent — do not land mid-nightly).

---

## Acceptance Criteria

- (a) post-maintenance file count BOUNDED + MEASURED (before/after on the warehouse prefix)
- (b) canonical rebuild + AC3-class diff STILL PASS on the maintained warehouse (maintenance doesn't move served numbers)
- (c) ONE tarball-restore drill proving `>retention` time-travel works (policy operating-rule 1 DEMONSTRATED, not assumed — natural verify-channel item, CC CVO)
- (d) maintenance failure-injection → derive STILL LANDS, loud log (best-effort, never blocks the marker-stamp)
- Compiler mandate: comp-kuzu smoke pre/post + F6 marker pin VERIFIED UNCHANGED by maintenance

---

## Binding policy constraint

Policy doc rule 3 (docs/reference/record-retention-policy-v1.md) BINDS: any future retention change amends the policy doc BEFORE the infra change. This TO implements the v1 policy as-written (13mo Nessie/Iceberg, indefinite snapshots/, 14d noncurrent unchanged).

---

## Zero-mutation note

This TO DOES mutate infra (compaction rewrites Iceberg files, expire_snapshots deletes expired snapshots) — but ONLY within the >=24h grace + never-touch-marker-referenced guards. It is NOT a read-only sweep. All deletes are policy-bounded + marker-protected. Standard Terraform-for-infra + container-rebuild-to-activate deploy path (Rule 1 — TF is the only Lambda/container deploy mechanism).

---

## RAVC2 to COO

1. Commit hash(es) + container rebuild confirmation (CodeBuild id, ECR tag)
2. Before/after file count on warehouse prefix (AC-a)
3. Canonical rebuild + AC3-diff result (AC-b)
4. Tarball-restore drill output (AC-c) — CC CVO
5. Failure-injection log excerpt (AC-d)
6. comp-kuzu pre/post smoke + marker-pin-unchanged proof

CC 1.0.0_SA_CTO + 3.0.0_SA_CVO on RAVC2.

---

*Dispatched by 2.0.0_SA_COO 20260612T194400Z*
*CTO PRD v0.4.4 §3 + retention policy 29b36516b (Andrew-ratified)*
