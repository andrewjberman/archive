# TRIAL-1 — Suite-gate coverage census: the 79 test files outside the commit gate

**Agent:** `0.8.0_AE_CloudComp~A`  
**Brief:** `org/tier1_exec/3.0.0_SA_CVO/deliverables/NFRA_SCRIPTGEN.TRIAL-1.BRIEF-PARKED.suite-gate-census-mandated-tooluse.md` @07d5e79278  
**GO:** Andrew-direct, 2026-08-06 ~2145Z, verbatim: *"This is your task : @07d5e7927 — org/tier1_exec/3.0.0_SA_CVO/deliverables/NFRA_SCRIPTGEN.TRIAL-1.BRIEF-PARKED.suite-gate-census-mandated-tooluse.md"*  
**Scope:** read-only. No edit to the gate, the tests, or `.tools/`. **This is a recommendation, not a change.**

---

## Denominator (re-derived, not carried forward)

| measured | value | how |
|---|---|---|
| test files in `org/modules/graph/tests/` | **93** | `comp-find --name 'test_*.py' …` DENOMINATOR line |
| files the gate runs | **14** | `WATCH_GLOBS` = 10 literals + `test_pipescript_*.py` → 4 |
| **files outside the gate** | **79** | set difference, all 14 confirmed present in the 93 |

Matches the brief's figures exactly; no re-derivation note needed.

## Rollup

| STATUS | n |   | VERDICT | n |
|---|---|---|---|---|
| LIVE (collects + passes) | 61 |   | ENROLL | 61 |
| RED (collects, fails) | 15 |   | LEAVE-OUT | 16 |
| BROKEN (does not deliver tests) | 1 |   | RETIRE | 2 |
| ORPHANED | 2 |   | | |
| **UNRESOLVED engines** | **0** |   | | |

**Every one of the 79 carries all four fields. Zero blanks, zero `UNRESOLVED` engines** — not because `UNRESOLVED` was disallowed, but because six derivation channels between them resolved every file. Each engine is derived from an **import or a call**, never from the filename.

---

## The census

`ENGINE` = what the file actually imports/loads/invokes. `STATUS` = exercised via `python -m pytest <file> -q`, rc and counts recorded. `EVIDENCE` = the line that settled ENGINE.

| # | FILE | ENGINE (from imports/calls) | STATUS | VERDICT | EVIDENCE | rc / result |
|---|---|---|---|---|---|---|
| 1 | `test_adapter_audit.py` | `org/modules/graph/adapter_audit_cli.py` **(MISSING)**<br>`.tools/portal-hooks/d1_adapter_threading_gate.py` | **ORPHANED** | **RETIRE** | `test_adapter_audit.py:23 (pathdiv -> MISSING)` | 2 — 1 error in 0.29s |
| 2 | `test_surface_check_negative_control.py` | `.tools/comp-surface-check` **(MISSING)**<br>`.tools/safe-commit.sh` | **ORPHANED** | **RETIRE** | `test_surface_check_negative_control.py:40 (literal -> MISSING)` | 2 — 1 error in 0.24s |
| 3 | `test_comp_system_metrics.py` | `org/modules/graph/comp_system.py` | **BROKEN** | **LEAVE-OUT** | `test_comp_system_metrics.py:25 (import)` | 5 — no summary |
| 4 | `test_compwhich_toolpass_rules.py` | `.tools/comp-which` | **RED** | **LEAVE-OUT** | `test_compwhich_toolpass_rules.py:2 (literal)` | 1 — 1 failed, 26 passed, 1 xpassed in 34.84s |
| 5 | `test_e413_dual_basis_preservation.py` | `org/modules/graph/comp_msbeff_rebaseline.py`<br>`org/modules/graph/comp_output_contract.py`<br>`org/modules/graph/comp_log_auto.py` | **RED** | **LEAVE-OUT** | `test_e413_dual_basis_preservation.py:51 (pyliteral)` | 1 — 8 failed, 11 passed in 0.49s |
| 6 | `test_e41_verdict_derivation_mutants.py` | `org/modules/graph/comp_output_contract.py`<br>`org/modules/graph/manifest_check_cli.py`<br>`data/inf/scripts/gold/whatever.py` **(MISSING)**<br>`org/modules/graph/comp_log_auto.py` | **RED** | **LEAVE-OUT** | `test_e41_verdict_derivation_mutants.py:55 (pyliteral)` | 1 — 7 failed, 5 passed in 0.35s |
| 7 | `test_e42_fail_kind_separation.py` | `org/modules/graph/comp_output_contract.py`<br>`org/modules/graph/comp_log_auto.py` | **RED** | **LEAVE-OUT** | `test_e42_fail_kind_separation.py:54 (pyliteral)` | 1 — 10 failed, 2 passed in 0.38s |
| 8 | `test_extract_iam_sovereign_guard.py` | `org/modules/graph/extract_iam.py`<br>`data/black_diamond/scripts/gold/A_00.py` **(MISSING)**<br>`data/canonical/schwab/silver/build_dim_account.py`<br>`data/inf/scripts/gold/A_00.py` **(MISSING)**<br>`data/cot/scripts/gold/A_00.py` **(MISSING)** | **RED** | **LEAVE-OUT** | `test_extract_iam_sovereign_guard.py:24 (pathdiv)` | 1 — 4 failed, 3 passed in 0.28s |
| 9 | `test_graphreach_discrimination.py` | `org/modules/graph/compproof/tool_probe.py`<br>`org/modules/graph/compproof/tool_corpus.py` | **RED** | **LEAVE-OUT** | `test_graphreach_discrimination.py:20 (pathjoin)` | 1 — 1 failed, 6 passed in 0.30s |
| 10 | `test_iam_resource_verdicts.py` | `org/modules/graph/extract_iam.py` | **RED** | **LEAVE-OUT** | `test_iam_resource_verdicts.py:63 (import)` | 1 — 1 failed, 43 passed in 32.39s |
| 11 | `test_indexer_bd_content_exclusion.py` | `org/modules/graph/trace_graph.py`<br>`org/modules/graph/extract_s3.py`<br>`org/modules/graph/extract_pipeline.py`<br>`org/modules/graph/sovereign_held.py`<br>`data/black_diamond/scripts/gold/A_00.accounts_dimension.py`<br>`data/black_diamond/scripts/gold/lib/s3_layout.py`<br>`data/black_diamond/scripts/silver/build_silver.py` **(MISSING)**<br>`data/inf/scripts/gold/INF_00.control.py` **(MISSING)**<br>`data/inf/scripts/gold/x.py` **(MISSING)** | **RED** | **LEAVE-OUT** | `test_indexer_bd_content_exclusion.py:29 (import)` | 1 — 2 failed, 1 passed in 0.49s |
| 12 | `test_kuzu_discrimination.py` | `org/modules/graph/compproof/tool_probe.py` | **RED** | **LEAVE-OUT** | `test_kuzu_discrimination.py:21 (pathjoin)` | 1 — 1 failed, 7 passed in 0.38s |
| 13 | `test_lambdamap.py` | `org/modules/graph/lambdamap_cli.py` | **RED** | **LEAVE-OUT** | `test_lambdamap.py:20 (import)` | 1 — 2 failed, 11 passed in 0.40s |
| 14 | `test_manifest_check_completeness_direction.py` | `.tools/comp-manifest-check`<br>`org/modules/graph/tests/_p4_probe_exempt.py` **(MISSING)**<br>`org/modules/graph/manifest_check_cli.py`<br>`data/inf/scripts/gold/x.py` **(MISSING)**<br>`org/modules/graph/foo.py` **(MISSING)**<br>`data/inf/scripts/gold/oldocs/run.py` **(MISSING)** | **RED** | **LEAVE-OUT** | `test_manifest_check_completeness_direction.py:56 (pathdiv)` | 1 — 2 failed, 6 passed in 37.37s |
| 15 | `test_manifest_check_completeness_members_fire.py` | `org/modules/graph/manifest_check_cli.py` | **RED** | **LEAVE-OUT** | `test_manifest_check_completeness_members_fire.py:59 (pathdiv)` | 1 — 2 failed, 7 passed in 19.23s |
| 16 | `test_output_contract.py` | `org/modules/graph/comp_output_contract.py`<br>`org/modules/graph/comp_log_auto.py`<br>`org/modules/graph/manifest_check_cli.py` | **RED** | **LEAVE-OUT** | `test_output_contract.py:18 (import)` | 1 — 15 failed, 22 passed in 2.00s |
| 17 | `test_routes_comment_blindness.py` | `org/modules/graph/extract_ts_source.py`<br>`org/modules/graph/extract_routes.py` | **RED** | **LEAVE-OUT** | `test_routes_comment_blindness.py:18 (import)` | 1 — 1 failed, 6 passed in 0.28s |
| 18 | `test_tool_graph_coupling_diff.py` | `org/modules/graph/comp_toolgraph.py` | **RED** | **LEAVE-OUT** | `test_tool_graph_coupling_diff.py:19 (import)` | 1 — 1 failed, 6 passed in 1.16s |
| 19 | `test_blast_discrimination.py` | `org/modules/graph/compproof/tool_probe.py` | **LIVE** | **ENROLL** | `test_blast_discrimination.py:21 (pathjoin)` | 0 — 6 passed in 0.08s |
| 20 | `test_blast_exit_code_contract.py` | `org/modules/graph/cli.py`<br>`org/modules/graph/comp_blast_universe.py` | **LIVE** | **ENROLL** | `test_blast_exit_code_contract.py:42 (pathdiv)` | 0 — 6 passed, 1 skipped in 44.35s |
| 21 | `test_blast_kuzu_projection.py` | `org/modules/graph/cli.py`<br>`org/modules/graph/trace_graph.py`<br>`zz_blast_overlay_fixture.py` **(MISSING)**<br>`org/modules/graph/comp_ladder.py`<br>`org/modules/graph/comp_blast_universe.py` | **LIVE** | **ENROLL** | `test_blast_kuzu_projection.py:27 (pathdiv)` | 0 — 21 passed in 117.03s (0:01:57) |
| 22 | `test_blast_overlap_pairwise.py` | `org/modules/graph/cli.py`<br>`org/modules/graph/comp_blast_universe.py` | **LIVE** | **ENROLL** | `test_blast_overlap_pairwise.py:43 (import)` | 0 — 8 passed in 22.90s |
| 23 | `test_boundary_report_conformance.py` | `org/modules/graph/boundary_report.py` | **LIVE** | **ENROLL** | `test_boundary_report_conformance.py:23 (import)` | 0 — 24 passed in 0.10s |
| 24 | `test_cache_cli.py` | `org/modules/graph/cache_cli.py` | **LIVE** | **ENROLL** | `test_cache_cli.py:24 (pathdiv)` | 0 — 22 passed in 0.22s |
| 25 | `test_census_substrate.py` | `org/modules/graph/census_substrate.py`<br>`org/modules/graph/comp_iam_census.py` | **LIVE** | **ENROLL** | `test_census_substrate.py:25 (import)` | 0 — 6 passed in 0.08s |
| 26 | `test_comp_aws_cert_mutants.py` | `org/modules/graph/comp_aws_cli.py`<br>`.tools/comp-aws` | **LIVE** | **ENROLL** | `test_comp_aws_cert_mutants.py:38 (pathdiv)` | 0 — 23 passed in 6.17s |
| 27 | `test_comp_constants_complete.py` | `org/modules/graph/comp_constants_complete.py` | **LIVE** | **ENROLL** | `test_comp_constants_complete.py:22 (import)` | 0 — 16 passed in 0.18s |
| 28 | `test_comp_constants_sovereign_guard.py` | `org/modules/graph/comp_constants_cli.py`<br>`safe_const.py` **(MISSING)**<br>`data/black_diamond/scripts/x.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_comp_constants_sovereign_guard.py:72 (import)` | 0 — 19 passed in 13.70s |
| 29 | `test_comp_dispatch.py` | `org/modules/graph/comp_dispatch.py` | **LIVE** | **ENROLL** | `test_comp_dispatch.py:20 (pathdiv)` | 0 — 7 passed in 0.09s |
| 30 | `test_comp_dispatch_bd_hold.py` | `.tools/comp-dispatch`<br>`org/modules/graph/comp_dispatch.py`<br>`gold_dispatch.sh` **(MISSING)**<br>`data/black_diamond/scripts/x.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_comp_dispatch_bd_hold.py:1 (literal)` | 0 — 4 passed in 0.07s |
| 31 | `test_comp_freshness_sovereign_guard.py` | `.tools/comp-freshness` | **LIVE** | **ENROLL** | `test_comp_freshness_sovereign_guard.py:27 (pathdiv)` | 0 — 8 passed in 1.10s |
| 32 | `test_comp_keys.py` | `org/modules/graph/comp_keys.py` | **LIVE** | **ENROLL** | `test_comp_keys.py:19 (import)` | 0 — 8 passed in 0.10s |
| 33 | `test_comp_learns_score.py` | `org/modules/graph/comp_learns_score.py` | **LIVE** | **ENROLL** | `test_comp_learns_score.py:19 (import)` | 0 — 9 passed in 3.36s |
| 34 | `test_comp_parity.py` | `org/modules/graph/comp_parity_cli.py` | **LIVE** | **ENROLL** | `test_comp_parity.py:9 (import)` | 0 — 14 passed in 0.08s |
| 35 | `test_comp_recognizers_bd_hold.py` | `org/modules/graph/comp_recognizers_code.py`<br>`org/modules/graph/comp_recognizers_config.py`<br>`data/black_diamond/scripts/x.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_comp_recognizers_bd_hold.py:33 (pyliteral)` | 0 — 6 passed in 0.14s |
| 36 | `test_comp_route.py` | `org/modules/graph/comp_route.py` | **LIVE** | **ENROLL** | `test_comp_route.py:24 (import)` | 0 — 13 passed in 0.09s |
| 37 | `test_comp_tool_health_symmetric_preventive.py` | `org/modules/graph/comp_tool_health.py` | **LIVE** | **ENROLL** | `test_comp_tool_health_symmetric_preventive.py:22 (pathjoin)` | 0 — 3 passed in 0.07s |
| 38 | `test_comp_types_index_idempotent_and_fallback.py` | `org/modules/graph/types_cli.py` | **LIVE** | **ENROLL** | `test_comp_types_index_idempotent_and_fallback.py:35 (pathjoin)` | 0 — 2 passed in 12.04s |
| 39 | `test_comp_validate_bd_hold.py` | `org/modules/graph/validate_cli.py`<br>`org/modules/graph/sovereign_held.py`<br>`data/black_diamond/x.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_comp_validate_bd_hold.py:30 (pathjoin)` | 0 — 11 passed in 0.14s |
| 40 | `test_comprail_sovereign_held.py` | `.tools/_comprail.py`<br>`data/black_diamond/scripts/gold/synth.py` **(MISSING)**<br>`data/canonical/schwab/silver/synth.py` **(MISSING)**<br>`data/inf/scripts/gold/synth.py` **(MISSING)**<br>`data/cot/scripts/gold/synth.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_comprail_sovereign_held.py:24 (import)` | 0 — 7 passed in 10.47s |
| 41 | `test_coverage_check_selfcheck_nonvacuous.py` | `org/modules/graph/comp_coverage_check.py` | **LIVE** | **ENROLL** | `test_coverage_check_selfcheck_nonvacuous.py:32 (pathdiv)` | 0 — 14 passed in 6.43s |
| 42 | `test_cycle_a1_gate_feed_readonly.py` | `org/modules/graph/comp_tool_health_gate.py`<br>`org/modules/graph/compproof/tool_probe.py` | **LIVE** | **ENROLL** | `test_cycle_a1_gate_feed_readonly.py:21 (pathjoin)` | 0 — 3 passed in 0.11s |
| 43 | `test_cycle_a_ensure_fresh_wire.py` | `org/modules/graph/comp_tool_health.py`<br>`org/modules/graph/compproof/tool_corpus.py`<br>`org/modules/graph/compproof/tool_probe.py` | **LIVE** | **ENROLL** | `test_cycle_a_ensure_fresh_wire.py:23 (pathjoin)` | 0 — 8 passed in 0.10s |
| 44 | `test_e5_estate_conformance_suite.py` | `.tools/msys_argv_guard.py` | **LIVE** | **ENROLL** | `test_e5_estate_conformance_suite.py:38 (import)` | 0 — 11 passed, 1 xfailed in 148.38s (0:02:28) |
| 45 | `test_e5_recall_standard_arity_limits.py` | `org/modules/graph/boundary_report.py` | **LIVE** | **ENROLL** | `test_e5_recall_standard_arity_limits.py:45 (import)` | 0 — 10 passed in 0.11s |
| 46 | `test_e6r8_route_run_conversion.py` | `org/modules/graph/comp_log_auto.py` | **LIVE** | **ENROLL** | `test_e6r8_route_run_conversion.py:65 (pyliteral)` | 0 — 9 passed in 0.17s |
| 47 | `test_effective_feed_unknown_never_false.py` | `org/modules/graph/comp_tool_health.py` | **LIVE** | **ENROLL** | `test_effective_feed_unknown_never_false.py:28 (pathjoin)` | 0 — 4 passed in 0.07s |
| 48 | `test_extract_assets.py` | `org/modules/graph/trace_graph.py`<br>`org/modules/graph/extract_assets.py`<br>`probe.py` **(MISSING)**<br>`broken.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_extract_assets.py:17 (import)` | 0 — 10 passed in 0.40s |
| 49 | `test_failure_class_hardening.py` | `org/modules/graph/extract_iam.py`<br>`org/modules/graph/extract_validate.py`<br>`org/modules/graph/incrparity_core.py`<br>`org/modules/graph/pii_cli.py` | **LIVE** | **ENROLL** | `test_failure_class_hardening.py:26 (import)` | 0 — 27 passed in 0.59s |
| 50 | `test_freshness_partition_key_anticorrelated.py` | `.tools/comp-freshness` | **LIVE** | **ENROLL** | `test_freshness_partition_key_anticorrelated.py:64 (pathdiv)` | 0 — 8 passed in 1.00s |
| 51 | `test_graphuni_headpin_d4.py` | `org/modules/graph/graph_cache.py`<br>`org/modules/graph/cli.py`<br>`org/modules/graph/trace_graph.py` | **LIVE** | **ENROLL** | `test_graphuni_headpin_d4.py:27 (import)` | 0 — 2 passed in 86.13s (0:01:26) |
| 52 | `test_iam_census_vintage.py` | `org/modules/graph/comp_iam_census.py`<br>`org/modules/graph/extract_iam.py`<br>`org/modules/graph/iam_cli.py` | **LIVE** | **ENROLL** | `test_iam_census_vintage.py:44 (import)` | 0 — 12 passed in 20.94s |
| 53 | `test_iam_role_label_collision.py` | `org/modules/graph/extract_iam.py` | **LIVE** | **ENROLL** | `test_iam_role_label_collision.py:30 (import)` | 0 — 3 passed in 0.14s |
| 54 | `test_iam_role_name_from_local.py` | `org/modules/graph/extract_iam.py` | **LIVE** | **ENROLL** | `test_iam_role_name_from_local.py:36 (import)` | 0 — 5 passed in 0.12s |
| 55 | `test_iam_scan_scope_multiroot.py` | `org/modules/graph/extract_iam.py` | **LIVE** | **ENROLL** | `test_iam_scan_scope_multiroot.py:28 (import)` | 0 — 3 passed in 0.15s |
| 56 | `test_iam_svc_coverage.py` | `org/modules/graph/extract_iam.py` | **LIVE** | **ENROLL** | `test_iam_svc_coverage.py:43 (import)` | 0 — 37 passed in 0.11s |
| 57 | `test_manifestcheck_discrimination.py` | `org/modules/graph/compproof/tool_probe.py` | **LIVE** | **ENROLL** | `test_manifestcheck_discrimination.py:19 (pathjoin)` | 0 — 4 passed in 0.12s |
| 58 | `test_passcraft_anti_harness.py` | `org/modules/graph/comp_passcraft.py`<br>`.tools/comp-freshness`<br>`org/modules/graph/cse_schema.py` | **LIVE** | **ENROLL** | `test_passcraft_anti_harness.py:19 (import)` | 0 — 22 passed in 0.19s |
| 59 | `test_pii_masking_reachability.py` | `org/modules/graph/pii_cli.py`<br>`pseudonymizer.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_pii_masking_reachability.py:25 (pathdiv)` | 0 — 4 passed in 0.12s |
| 60 | `test_pii_sweep_denominator.py` | `org/modules/graph/pii_cli.py` | **LIVE** | **ENROLL** | `test_pii_sweep_denominator.py:19 (pathdiv)` | 0 — 3 passed in 0.11s |
| 61 | `test_platinum_nested_keys.py` | `org/modules/graph/platinum_cli.py` | **LIVE** | **ENROLL** | `test_platinum_nested_keys.py:31 (import)` | 0 — 8 passed in 0.14s |
| 62 | `test_prod_write_guard.py` | `org/modules/graph/prod_write_guard.py` | **LIVE** | **ENROLL** | `test_prod_write_guard.py:31 (pathjoin)` | 0 — 6 passed in 0.08s |
| 63 | `test_pulse_map_autorefresh.py` | `org/modules/graph/comp_pulse.py` | **LIVE** | **ENROLL** | `test_pulse_map_autorefresh.py:20 (import)` | 0 — 6 passed in 0.10s |
| 64 | `test_registry_held_rows.py` | `org/modules/graph/registry_cli.py` | **LIVE** | **ENROLL** | `test_registry_held_rows.py:19 (pathdiv)` | 0 — 4 passed in 0.09s |
| 65 | `test_residue_detector.py` | `org/modules/graph/residue_cli.py`<br>`covering.py` **(MISSING)**<br>`blind.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_residue_detector.py:18 (import)` | 0 — 12 passed in 0.09s |
| 66 | `test_routable_check_fires.py` | `.tools/comp-which-routing-test.py`<br>`.tools/comp-routable-check` | **LIVE** | **ENROLL** | `test_routable_check_fires.py:2 (literal)` | 0 — 5 passed in 0.07s |
| 67 | `test_routes_trace_discriminates.py` | `org/modules/graph/routes_cli.py`<br>`org/modules/graph/extract_routes.py` | **LIVE** | **ENROLL** | `test_routes_trace_discriminates.py:39 (import)` | 0 — 36 passed in 1.55s |
| 68 | `test_routes_unresolved_not_none.py` | `org/modules/graph/pii_cli.py`<br>`org/modules/graph/routes_cli.py`<br>`org/modules/graph/extract_routes.py`<br>`org/modules/graph/extract_transforms.py` | **LIVE** | **ENROLL** | `test_routes_unresolved_not_none.py:35 (import)` | 0 — 8 passed in 0.42s |
| 69 | `test_sfn_asl_walker.py` | `org/modules/graph/comp_aws_cli.py` | **LIVE** | **ENROLL** | `test_sfn_asl_walker.py:25 (import)` | 0 — 3 passed in 0.07s |
| 70 | `test_shell_guard_discrimination.py` | `org/modules/graph/shell_cli.py`<br>`bare.sh` **(MISSING)**<br>`guarded.sh` **(MISSING)**<br>`which_guard.sh` **(MISSING)**<br>`clean.sh` **(MISSING)**<br>`data/black_diamond/scripts/held.sh` **(MISSING)**<br>`org/mcp/local.sh` **(MISSING)**<br>`data/black_diamond/x.sh` **(MISSING)**<br>`org/mcp/x.sh` **(MISSING)** | **LIVE** | **ENROLL** | `test_shell_guard_discrimination.py:36 (pathdiv)` | 0 — 15 passed in 0.12s |
| 71 | `test_sovereign_held.py` | `org/modules/graph/sovereign_held.py`<br>`data/black_diamond/scripts/gold/x.py` **(MISSING)**<br>`data/canonical/schwab/silver/build_dim.py` **(MISSING)**<br>`data/inf/scripts/gold/x.py` **(MISSING)**<br>`data/cot/scripts/gold/x.py` **(MISSING)**<br>`data/black_diamond/scripts/x.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_sovereign_held.py:21 (pathjoin)` | 0 — 8 passed in 0.07s |
| 72 | `test_surfacecheck_discrimination.py` | `org/modules/graph/compproof/tool_probe.py` | **LIVE** | **ENROLL** | `test_surfacecheck_discrimination.py:21 (pathjoin)` | 0 — 8 passed in 0.07s |
| 73 | `test_symbols_extraction_ast_not_text.py` | `org/modules/graph/comp_symbols.py`<br>`fixture_symbols.py` **(MISSING)**<br>`org/modules/graph/__nonexistent_zzz__.py` **(MISSING)** | **LIVE** | **ENROLL** | `test_symbols_extraction_ast_not_text.py:2 (literal)` | 0 — 9 passed in 0.08s |
| 74 | `test_tagauthz_verdict_bites.py` | `.tools/comp-tagauthz.py` | **LIVE** | **ENROLL** | `test_tagauthz_verdict_bites.py:22 (pathjoin)` | 0 — 2 passed in 0.07s |
| 75 | `test_tool_probe_discrimination.py` | `org/modules/graph/compproof/tool_probe.py` | **LIVE** | **ENROLL** | `test_tool_probe_discrimination.py:55 (import_module)` | 0 — 31 passed, 6 warnings in 0.13s |
| 76 | `test_tooltip_canonical_exclusion.py` | `org/modules/graph/tooltip_cli.py` | **LIVE** | **ENROLL** | `test_tooltip_canonical_exclusion.py:22 (pathdiv)` | 0 — 6 passed in 0.15s |
| 77 | `test_trace_blast_xref_notfound_is_loud.py` | `org/modules/graph/cli.py` | **LIVE** | **ENROLL** | `test_trace_blast_xref_notfound_is_loud.py:49 (import)` | 0 — 6 passed in 61.31s (0:01:01) |
| 78 | `test_transform_annotated_usememo_rendered_detection.py` | `org/modules/graph/extract_transforms.py` | **LIVE** | **ENROLL** | `test_transform_annotated_usememo_rendered_detection.py:44 (pathdiv)` | 0 — 5 passed in 0.10s |
| 79 | `test_vectorize_audit_ascii.py` | `org/modules/graph/vectorize_audit_cli.py` | **LIVE** | **ENROLL** | `test_vectorize_audit_ascii.py:20 (import)` | 0 — 3 passed in 0.12s |

---

## Criterion 4 — the filename shortcut, measured

The forbidden shortcut is `test_<x>.py` → `<x>.py`. Applied to all 79:

| outcome | n | share |
|---|---|---|
| shortcut lands on the **real** engine | 10 | 13% |
| shortcut lands on a **real but wrong** file | 0 | 0% |
| shortcut resolves to **nothing at all** | 69 | 87% |

**The shortcut is not mostly-wrong — it is mostly-INAPPLICABLE.** For **69 of 79 (87%)** the name maps to no file whatsoever, so an ENGINE derived from the name would not be a bad guess, it would be an *invention*. It is never actively misleading in this corpus (0 cases). That is the empirical case for criterion 4, and it is a different case than the brief assumed.

**Where the names DO mislead is about SHAPE, not engine** — see `test_comp_system_metrics.py` below.

---

## Findings

### F1 — `test_comp_system_metrics.py` is not a pytest file at all (NEW; not disclosed)

It carries **zero** `def test_*` / `class Test*`. It defines its own `check(name, got, want)` (`:31`) and runs under `if __name__ == "__main__":` (`:169`). `pytest` collects **0 tests, rc=5** — a true rc, confirmed without a pipe (a piped `echo $?` reports `tail`'s rc and reads as a clean 0; that trap is live here).

**Why it matters more than a broken file:** a BROKEN file fails loudly. This one is a battery whose name claims coverage, which delivers none, and which no runner would ever surface — it cannot redden, so it can never report the decay it was written to catch. **It is exactly the F9 class the gate exists to kill, sitting outside the gate.**

**Denominator for the class: 1 of 93.** I checked every file in the directory, not just the 79 — it is isolated, not systemic. It is the only zero-test file in the tree.

### F2 — the brief's disclosed specimen does not hold (REFUTED)

The brief states, as its one proof-of-existence: *"`test_boundary_report_conformance.py` loads `residue`. Nothing in its name says so."*

**It does not.** Line 23 is `import boundary_report as B` — name and engine **match**. The only occurrence of `residue` in the file is line 29, `"tool": "comp-residue"`, a string inside test fixture data. The author flagged their scan as a crude import regex with known false positives; this is one, and they pre-authorised this correction (*"yours is the measurement and mine was never one"*).

**The trap class is real even though the specimen is not** — see F3.

### F3 — the real name-vs-engine specimens (stronger than the disclosed one)

- **`test_blast_discrimination.py` does not exercise `comp-blast`.** It `importlib`-loads `org/modules/graph/compproof/tool_probe.py` (`:21`) and stubs the tool out entirely with `runner=lambda q, to: (out, rc)` (`:34`). A staged change to `comp-blast` **should not** run it; a change to `tool_probe.py` **must**. Six batteries share this engine.
- **`test_e42_fail_kind_separation.py` → `comp_output_contract.py`** (`:54`), **`test_e413_dual_basis_preservation.py` → `comp_msbeff_rebaseline.py`** (`:51`), **`test_e6r8_route_run_conversion.py` → `comp_log_auto.py`** (`:65`). None of these engines is guessable from the filename.

### F4 — I reproduced the author's own error class, and caught it (method note)

My first mismatch metric reported **62 of 79** name/engine disagreements (**60** after a later fix). It was a crude bidirectional substring test and both readings were **junk** — discarded, not published as a finding. My extractor separately mis-resolved `test_comp_keys.py` to `__init__.py` because it read only `node.module` on an `ImportFrom` and ignored the imported name; that single artifact would have been published as *"1 actively-misleading file"* had I not verified it. **Both were caught by checking a specimen before publishing a count** — the same discipline that falsified F2. A count is not a measurement until you have looked at one of its members.

---

## Criterion 3 — actionable enrollment map

Every `ENROLL` row's engine, ready to drop into `WATCH_EXACT` without further research. **61 batteries across 56 distinct engines.**

| engine (the `WATCH_EXACT` line) | batteries it should trigger |
|---|---|
| `org/modules/graph/compproof/tool_probe.py` | `test_blast_discrimination.py`, `test_cycle_a1_gate_feed_readonly.py`, `test_cycle_a_ensure_fresh_wire.py`, `test_manifestcheck_discrimination.py`, `test_surfacecheck_discrimination.py`, `test_tool_probe_discrimination.py` |
| `org/modules/graph/extract_iam.py` | `test_failure_class_hardening.py`, `test_iam_census_vintage.py`, `test_iam_role_label_collision.py`, `test_iam_role_name_from_local.py`, `test_iam_scan_scope_multiroot.py`, `test_iam_svc_coverage.py` |
| `org/modules/graph/cli.py` | `test_blast_exit_code_contract.py`, `test_blast_kuzu_projection.py`, `test_blast_overlap_pairwise.py`, `test_graphuni_headpin_d4.py`, `test_trace_blast_xref_notfound_is_loud.py` |
| `org/modules/graph/pii_cli.py` | `test_failure_class_hardening.py`, `test_pii_masking_reachability.py`, `test_pii_sweep_denominator.py`, `test_routes_unresolved_not_none.py` |
| `.tools/comp-freshness` | `test_comp_freshness_sovereign_guard.py`, `test_freshness_partition_key_anticorrelated.py`, `test_passcraft_anti_harness.py` |
| `org/modules/graph/comp_blast_universe.py` | `test_blast_exit_code_contract.py`, `test_blast_kuzu_projection.py`, `test_blast_overlap_pairwise.py` |
| `org/modules/graph/comp_tool_health.py` | `test_comp_tool_health_symmetric_preventive.py`, `test_cycle_a_ensure_fresh_wire.py`, `test_effective_feed_unknown_never_false.py` |
| `org/modules/graph/trace_graph.py` | `test_blast_kuzu_projection.py`, `test_extract_assets.py`, `test_graphuni_headpin_d4.py` |
| `org/modules/graph/boundary_report.py` | `test_boundary_report_conformance.py`, `test_e5_recall_standard_arity_limits.py` |
| `org/modules/graph/comp_aws_cli.py` | `test_comp_aws_cert_mutants.py`, `test_sfn_asl_walker.py` |
| `org/modules/graph/comp_dispatch.py` | `test_comp_dispatch.py`, `test_comp_dispatch_bd_hold.py` |
| `org/modules/graph/comp_iam_census.py` | `test_census_substrate.py`, `test_iam_census_vintage.py` |
| `org/modules/graph/extract_routes.py` | `test_routes_trace_discriminates.py`, `test_routes_unresolved_not_none.py` |
| `org/modules/graph/extract_transforms.py` | `test_routes_unresolved_not_none.py`, `test_transform_annotated_usememo_rendered_detection.py` |
| `org/modules/graph/routes_cli.py` | `test_routes_trace_discriminates.py`, `test_routes_unresolved_not_none.py` |
| `org/modules/graph/sovereign_held.py` | `test_comp_validate_bd_hold.py`, `test_sovereign_held.py` |
| `.tools/_comprail.py` | `test_comprail_sovereign_held.py` |
| `.tools/comp-aws` | `test_comp_aws_cert_mutants.py` |
| `.tools/comp-dispatch` | `test_comp_dispatch_bd_hold.py` |
| `.tools/comp-routable-check` | `test_routable_check_fires.py` |
| `.tools/comp-tagauthz.py` | `test_tagauthz_verdict_bites.py` |
| `.tools/comp-which-routing-test.py` | `test_routable_check_fires.py` |
| `.tools/msys_argv_guard.py` | `test_e5_estate_conformance_suite.py` |
| `org/modules/graph/cache_cli.py` | `test_cache_cli.py` |
| `org/modules/graph/census_substrate.py` | `test_census_substrate.py` |
| `org/modules/graph/comp_constants_cli.py` | `test_comp_constants_sovereign_guard.py` |
| `org/modules/graph/comp_constants_complete.py` | `test_comp_constants_complete.py` |
| `org/modules/graph/comp_coverage_check.py` | `test_coverage_check_selfcheck_nonvacuous.py` |
| `org/modules/graph/comp_keys.py` | `test_comp_keys.py` |
| `org/modules/graph/comp_ladder.py` | `test_blast_kuzu_projection.py` |
| `org/modules/graph/comp_learns_score.py` | `test_comp_learns_score.py` |
| `org/modules/graph/comp_log_auto.py` | `test_e6r8_route_run_conversion.py` |
| `org/modules/graph/comp_parity_cli.py` | `test_comp_parity.py` |
| `org/modules/graph/comp_passcraft.py` | `test_passcraft_anti_harness.py` |
| `org/modules/graph/comp_pulse.py` | `test_pulse_map_autorefresh.py` |
| `org/modules/graph/comp_recognizers_code.py` | `test_comp_recognizers_bd_hold.py` |
| `org/modules/graph/comp_recognizers_config.py` | `test_comp_recognizers_bd_hold.py` |
| `org/modules/graph/comp_route.py` | `test_comp_route.py` |
| `org/modules/graph/comp_symbols.py` | `test_symbols_extraction_ast_not_text.py` |
| `org/modules/graph/comp_tool_health_gate.py` | `test_cycle_a1_gate_feed_readonly.py` |
| `org/modules/graph/compproof/tool_corpus.py` | `test_cycle_a_ensure_fresh_wire.py` |
| `org/modules/graph/cse_schema.py` | `test_passcraft_anti_harness.py` |
| `org/modules/graph/extract_assets.py` | `test_extract_assets.py` |
| `org/modules/graph/extract_validate.py` | `test_failure_class_hardening.py` |
| `org/modules/graph/graph_cache.py` | `test_graphuni_headpin_d4.py` |
| `org/modules/graph/iam_cli.py` | `test_iam_census_vintage.py` |
| `org/modules/graph/incrparity_core.py` | `test_failure_class_hardening.py` |
| `org/modules/graph/platinum_cli.py` | `test_platinum_nested_keys.py` |
| `org/modules/graph/prod_write_guard.py` | `test_prod_write_guard.py` |
| `org/modules/graph/registry_cli.py` | `test_registry_held_rows.py` |
| `org/modules/graph/residue_cli.py` | `test_residue_detector.py` |
| `org/modules/graph/shell_cli.py` | `test_shell_guard_discrimination.py` |
| `org/modules/graph/tooltip_cli.py` | `test_tooltip_canonical_exclusion.py` |
| `org/modules/graph/types_cli.py` | `test_comp_types_index_idempotent_and_fallback.py` |
| `org/modules/graph/validate_cli.py` | `test_comp_validate_bd_hold.py` |
| `org/modules/graph/vectorize_audit_cli.py` | `test_vectorize_audit_ascii.py` |

### The cost the gate owner needs before deciding

**Enrolling all 61 would put 563 s (9.4 min) of pytest on a commit that touches every engine.** The distribution is extremely skewed — 4 batteries carry ~7 of those minutes:

| battery | wall |
|---|---|
| `test_e5_estate_conformance_suite.py` | 148.4s |
| `test_blast_kuzu_projection.py` | 117.0s |
| `test_graphuni_headpin_d4.py` | 86.1s |
| `test_trace_blast_xref_notfound_is_loud.py` | 61.3s |
| `test_blast_exit_code_contract.py` | 44.4s |
| `test_blast_overlap_pairwise.py` | 22.9s |
| `test_iam_census_vintage.py` | 20.9s |
| `test_comp_constants_sovereign_guard.py` | 13.7s |
| `test_comp_types_index_idempotent_and_fallback.py` | 12.0s |
| `test_comprail_sovereign_held.py` | 10.5s |
| `test_coverage_check_selfcheck_nonvacuous.py` | 6.4s |
| `test_comp_aws_cert_mutants.py` | 6.2s |
| `test_comp_learns_score.py` | 3.4s |

A realistic commit stages one or two engines, not all 56, so the *typical* cost is a few seconds — but the tail is real and it is the gate owner's call, not mine. **I am not recommending a tier split, a timeout, or a subset; I am handing over the numbers that decision needs.** Widening the gate is the owner's scoping call (brief, explicit scope bound).

---

## What I did NOT do

- Did not edit the gate, enroll anything, or touch `.tools/`.
- Did not fix the two disclosed BROKEN files, or F1.
- Did not decide whether the gate should widen.

**Grounding:** engines derived at working tree `HEAD`; pytest exercised 79/79 files this session; `comp-find` denominator 93 re-measured, not carried from the brief.
