# FIND_INSURE.029 — Phase 2B chassis-pre-stage (AE 0.7~B)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.7 §4 Phase 2B (post-ws CTO REPAIR-AMENDMENT ship `0d75ba5fe`)
**Pod:** 0.7.0_AE_CloudOps~B
**Lane:** AE_CloudOps ~B (Phase 2B Bβ Bright Data fallback + multi-board EventBridge + IAM/secrets)
**Issued to:** 0.7.0_AE_CloudOps~B
**Author:** 2.0.0_SA_COO 2026-05-27T~23:48Z (cycle 166 — audit-trail TO per AE 0.7~B BLOCKED-ASK 23:42Z + ws COO DISPOSITION 23:44Z Option (b))
**Sizing:** ~1-2h wall (3 TF chassis files + tag bump + safe-apply + RAVC2)
**Authority anchor:** Andrew 23:25Z parallelize directive + AE 0.7~B BLOCKED-ASK 23:42Z + ws COO disposition 23:44Z OPTION (b) CHASSIS-PRE-STAGE + LD-0090 ALWAYS-PROCEED

<status>pending</status>

## Objective

Pre-stage 3 empty Terraform chassis files for Phase 2B job-postings channel infrastructure. Zero per-board specifics; comment-block patterns describing per-board append discipline. Tag `imo-pipeline-phase2b-v0.0.0` chassis-pre-fill anchor. Manifest v0.1 fill (DS~D's `.028` AC2 + AC3 ratify on per-board Stage Bα/Bβ routing) triggers per-board module append into these chassis files instead of net-new file authoring — collapses per-board ship cycle by ~5min/board at fill moment.

## Acceptance criteria

- **AC1.** `infra/aws/terraform/imo-pipeline/phase2b-secrets.tf` authored:
  - 6 placeholder secret namespace slots mirroring existing `job_board_placeholder` pattern from `secrets.tf:58`
  - Comment-block at top documenting per-board append pattern + namespace allocation discipline
  - No actual secret values (OOB per AE 0.7 standard)
- **AC2.** `infra/aws/terraform/imo-pipeline/phase2b-eventbridge.tf` authored:
  - Orchestrator-side `find-insure-job-posting-fanout` rule scaffold (per-board scheduled rules added via append)
  - Comment-block at top describing per-board permission append pattern
  - Wildcard permission rule confirmation (per `eventbridge.tf:29` pattern; no per-rule permission needed for additional rules)
- **AC3.** `infra/aws/terraform/imo-pipeline/phase2b-lambdas.tf` authored:
  - Header comment-block describing per-board module append pattern (lambda module per board, taking shared chassis-defined IAM role)
  - No actual Lambda module declarations (those land per-board at manifest v0.1 fill)
- **AC4.** `infra/aws/terraform/imo-pipeline/phase2b-iam.tf` (NEW; not in your BLOCKED-ASK list but structurally needed) — OR fold IAM additions into existing `iam.tf` per your judgment. If new file: per-board IAM policy append pattern + comment-block. If folding: add `find-insure-job-posting-fanout-*` rule-pattern allowance to existing IAM policy.
- **AC5.** `terraform plan` clean on chassis files (no 0-diff drift; chassis files are scaffolding, no live resources beyond the orchestrator-side eventbridge rule which may show as new resource).
- **AC6.** `terraform apply` via `.tools/safe-apply.sh` (per CLAUDE.md Rule 18 HALTGT checkpoint discipline) — orchestrator-side fan-out rule deployed; per-board rules deferred to per-board append cycles.
- **AC7.** Tag `imo-pipeline-phase2b-v0.0.0` per CLAUDE.md Rule 6 git-tag-after-deploy + `git push --follow-tags`.
- **AC8.** Source-map update at `infra/aws/lambda/ci/lambda-source-map.json` IF any new Lambda chassis added (likely no Lambdas this cycle — chassis is TF-only).
- **AC9.** `comp-iam gaps` confirms no MISSING IAM permissions for any orchestrator-side rule + delete-restrict on chassis files matches existing `iam.tf:172` pattern.
- **AC10.** RAVC2-Request to ws COO with chassis evidence + tag confirmation + plan output excerpt + apply 0-diff verification + safe-apply HALTGT checkpoint logs.

## Dependencies

- **AE 0.7~B SPAWN-ACK** 23:38Z — completed; you're LIVE per broker
- **ws COO disposition 23:44Z** — OPTION (b) CHASSIS-PRE-STAGE ratified
- **PRD `docs/architecture/FIND_INSURE.md` v0.7** — `0d75ba5fe`; §4 Phase 2B narrative + REPAIR-AMENDMENT closures
- **CVO Mode B `810211e17`** — §Phase 2B SURVEY-STAGE classification (your chassis pre-stages substrate ahead of per-board execution)
- **DS~D `.028` Phase 2B multi-board architecture survey** — your chassis design is INFORMED by DS~D's per-board AC1 classification + Stage Bα/Bβ routing AC3 + per-board parser system AC2. Coordinate with DS~D: read their in-flight artifacts (AC1 + AC2 + AC3 shipped per their broker summary; AC4 in-flight) before chassis file authoring.
- **NO HAR dependency** — chassis is board-agnostic; per-board content fills at manifest-v0.1 moment
- **NO Bα HAR-supply gate** — Bβ chassis is independent of Bα Andrew HAR supply per your BLOCKED-ASK §"Standing posture" analysis

## Sequencing

1. ~5min: read DS~D's in-flight .028 artifacts (3 of 4 shipped per broker; AC4 imminent)
2. ~15min: author `phase2b-secrets.tf` chassis + comment block
3. ~15min: author `phase2b-eventbridge.tf` chassis + orchestrator-side rule + comment block
4. ~10min: author `phase2b-lambdas.tf` header + comment block
5. ~10min: author/decision on `phase2b-iam.tf` per AC4 disposition
6. ~5min: `terraform plan` + clean diff verification
7. ~5min: `.tools/safe-apply.sh` (HALTGT checkpoint)
8. ~5min: tag bump + push --follow-tags
9. ~5min: comp-iam gaps verification
10. ~10min: safe-commit.sh + RAVC2-Request

**Total ETA:** ~1.5-2h wall

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.029 — Phase 2B chassis pre-stage shipped` to ws COO. CC ws CTO + ws CVO. Body: commit hash + tag confirmation + plan/apply outputs + safe-apply HALTGT logs + comp-iam confirmation + sister-coord acknowledgment with DS~D (their .028 informing your chassis decisions).

## Sister coord

- **DS~D `.028` Phase 2B multi-board architecture survey** — your chassis design pattern is informed by DS~D's per-board classification + Stage routing matrix; coordinate at AC1-3 review moment
- **AE 0.7~A `.008` Stage 2 + `.024` telemetry + `.007` AC7 sister-deploy** — your chassis tag bump `imo-pipeline-phase2b-v0.0.0` is INDEPENDENT of AE 0.7~A's `imo-pipeline-v0.X.Y` tag chain; no conflict
- **AC-T2 SPA escape-valve sister-coord** (per my 23:44Z disposition §2) — separate from this chassis; AE 0.7~B optional fold-in of `scraping_browser1` v0.3.0 (source pre-build `40b18d724`) per your judgment + cycle timing

## Compiler tools mandate

- **Before edit:** `comp-blast` on any node touched (chassis files won't blast much; orchestrator-side rule has Lambda-target dependency)
- **Before commit:** `.tools/ds-commit-gate.sh` N/A (TF-only, not Python); standard tflint if available
- **After apply:** `comp-iam gaps` per AC9; `comp-pipescript deployed` N/A (no Lambda code)

## Cross-domain coordination

- DS~D `.028` AC2 per-board parser pattern + AC3 Stage routing → your chassis comment-blocks reflect their pattern
- ws CTO PRD v0.7 §4 Phase 2B narrative → your chassis files reference v0.7 PRD section
- ws CTO future REPAIR-AMENDMENT cycles → your chassis files survive amendments (chassis is abstraction layer)

## Notes

- Per LD-0090 ALWAYS-PROCEED + Andrew 23:25Z parallelize directive — chassis-pre-stage is structurally additive forward motion; reversible if per-board manifest discloses chassis design needs refactor
- Per AE 0.7~B BLOCKED-ASK §"Suggested unblocker class" — `architectural` need ratified via this TO authoring
- Per [[feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch]] — chassis-pre-stage is the canonical pattern for substrate-pre-positioning ahead of gate-flip moments
- Per CLAUDE.md Rule 18 HALTGT checkpoint — safe-apply discipline mandatory for terraform apply; pre-push hook fires HALTGT

— ws COO /drive cycle 166 — AE 0.7~B audit-trail TO 2026-05-27T~23:48Z
