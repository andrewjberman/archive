# Task Order: ADVI_DEMOV1.011 — `_snapshot_clean_pass2_subpaths()` generalization

**TO ID:** ADVI_DEMOV1.011
**Status:** DISPATCHED 2026-05-27T~08:50Z
**Project:** ADVI_DEMOV1 (F2-cutover-envelope-discharged; this is post-close durable structural-fix per PRD v0.1.4 §3.6 amendment)
**Owner:** 0.4.0_DS_ClientPlatform~D (default per DS~D 0838Z standing posture + LD-0027 SPAWN-WITH-DIRECTION arc continuity; base-lane fallback acceptable if ~D capacity-constrained)
**Coordinated with:** 0.7.0_AE_CloudOps (IAM terraform-apply Phase 2 coordination), 1.0.0_SA_CTO (PRD v0.1.4 §3.6 spec author + REPAIR-AMENDMENT scribe)
**Dispatching exec:** 2.0.0_SA_COO
**Authority chain:** ws CVO `42333ed49` /verify-channel CORROBORATE (b)-class clean → ws CTO `bcc4cb142` PRD v0.1.4 §3.6 REPAIR-AMENDMENT → ws COO cycle 146 dispatch
**RAVC2 ETA:** ~2-3h wall (DS edit + ds-commit-gate + comp-pipescript deployed MATCH + AE IAM terraform-apply Phase 2 + Fire-N empirical-validation cycle)

## Provenance

- **Why this TO exists:** ADVI_DEMOV1.007 commit `3cffa512b` introduced `_snapshot_clean_advisors_subpath()` per LD-0055 advisors/ accumulation finding. The implicit assumption — "only advisors/ subpath needs cleaning across re-runs" — failed empirically during F2 cutover (F1 z-shape → F2 OPAL###### schema rev exposed symmetric accounts/-subpath accumulation; Fire 6 + Fire 7 both surfaced `format_anomaly_count=193064` from ~3000 residual F1 z-folders × ~64 z-id refs/file amplification).
- **PRD spec:** docs/architecture/ADVI_DEMOV1.md §3.6 `bcc4cb142` REPAIR-AMENDMENT (durable structural-fix shipped 2026-05-27T~06:08Z; this TO is the impl carrier).
- **Tactical bridge in place:** `ca12fecfe` `pii_leak_scan.py --f1-residue-tolerance 250000` flag bridged Fire 7 to PASS-with-WARN close; this TO removes the need for the tolerance flag going forward (post-impl: anomaly_count → 0 deterministically on clean transform run).
- **F2 AC6 status:** CLOSED ~08:32Z via tactical bridge; this TO is the durable structural fix anticipating future schema-revs.

## Acceptance Criteria

### AC1 — Function refactor + symmetric subpath coverage

- Replace `_snapshot_clean_advisors_subpath()` with `_snapshot_clean_pass2_subpaths()` in `data/demo/scripts/transform/demo_transform.py`
- **Subpath list derived from `prefixes` argument** — same arg drives PASS 2 writes (single source of truth; avoids per-subpath maintenance drift)
- Symmetric coverage in PRD §3.6 spec: advisors/ + accounts/ + clients/ + firm/ (4 subpaths; verify against current `prefixes` invocation usage)
- Schema-version-mismatch detection gates the destructive sweep (do NOT blow away current-format files when schema unchanged; only delete on detected schema-rev)
- Preserve existing advisors/-only behavior as the schema-unchanged degenerate case (backward-compatible default)

### AC2 — IAM scope extension + terraform 0-diff verify

- Update `infra/aws/terraform/shared-infra/demo-transform.tf` IAM policy:
  - Rename `SnapshotCleanAdvisorsDest` Sid → `SnapshotCleanPass2Subpaths`
  - Per-subpath resource ARNs (preserve no-wildcard-widening discipline): `arn:aws:s3:::opal-data-demo/platinum/advisors/*` + `accounts/*` + `clients/*` + `firm/*`
  - Coordinate with AE 0.7 for `safe-apply` execution (CLAUDE.md Rule 9 — Terraform owns infra; this terraform change is infra-class; AE-lane apply per Rule 9)
- AE 0.7 verifies `terraform plan` 0-diff post-apply (CLAUDE.md Rule 2 commit-before-apply discipline)

### AC3 — Empirical validation via clean transform + scan

- Re-run `demo_transform.py` on demo bucket (post-IAM-apply for the new IAM scope to be effective)
- AE 0.7 dispatches via standard `demo-transform-runner` EC2_MANIFEST + SSM
- Run `pii_leak_scan.py` against post-transform bucket WITHOUT the `--f1-residue-tolerance` flag (this is the test that PRD §3.6 spec is correct)
- **Expected R5:** `leak_count=0` AND `format_anomaly_count=0` AND scan exit 0 (strict PASS, no WARN)
- Failure to reach strict PASS (leak>0 OR anomaly>0) = re-open investigation; route via BLOCKED-ASK to COO

### AC4 — Tactical-flag removal

- Once AC3 passes strict, remove the `--f1-residue-tolerance` flag default from `pii_leak_scan.py` default invocation (per `ca12fecfe` commit body: "auto-restore post-.011")
- Flag remains in argparse for future schema-revs (banking pattern preservation per `feedback_ravc2_pass_with_warn_via_tolerance_flag_preserves_regression_sentinel`)
- Default behavior reverts to strict (no tolerance; anomaly_count > 0 BLOCKs)

## Coordination

- **Phase 1 (DS edit ~30-60min):** DS~D authors AC1 + AC4 source-edit; ds-commit-gate clean; safe-commit; push CLOUD; `comp-pipescript deployed MATCH` verify
- **Phase 2 (AE IAM ~10-20min):** AE 0.7 applies terraform AC2 per safe-apply; 0-diff verify
- **Phase 3 (Fire-N empirical ~90-120min):** AE 0.7 dispatches transform re-run + scan; collects R5 evidence
- **Phase 4 (RAVC2 ~5min):** DS~D + AE 0.7 RAVC2-Request to COO with evidence; COO ratifies + closes .011

## Out-of-scope (carry-forward to other TOs)

- `ADVI_DEMOV1.012` PASS-2 completion-gate instrumentation (CTO carve-or-fold ratify pending; orthogonal mechanism class — coverage-completeness vs PII-leak-gate)
- Demo-bucket-completion (~46% F2 coverage from Fire 4 truncation) — naturally addressed when AC3 transform re-runs cleanly with extended executionTimeout
- F1 retire-via-AE-AC5-closure (AE-lane scope per cycle 130 §6b commitment)
- SSM logs/ IAM subpath gap (AE-lane infra option-ii fold per cycle 145 ACK)

## Banking observations to anchor on RAVC2 close

- `feedback_repair_amendment_implementation_cycle_validates_b_class_corroborate_clean` — .011 ship validates ws CVO `42333ed49` (b)-class CORROBORATE-clean verdict empirically; reusable pattern for future REPAIR-AMENDMENT class cycles
- `feedback_tactical_flag_bridge_removed_post_durable_structural_fix` — AC4 anchor empirically: tactical `--f1-residue-tolerance` flag served its purpose during Fire 7 (cycle 137-145 bridge) + retired cleanly post-.011 ship without permanent gate weakening (banking pattern for "tactical-flag-bridge-to-durable-fix" lifecycle)
- `feedback_prefixes_arg_as_single_source_of_truth_for_pass2_subpaths` — derive-from-prefixes design pattern over per-subpath enumeration; avoids future drift when new subpaths added

— ws COO 2.0.0_SA_COO authored cycle 146
2026-05-27T~08:50Z
