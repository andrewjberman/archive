<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_RPBKTPI.001</id>
    <project>ADVI_RPBKTPI</project>
    <title>INF_B_00 accounts_v2 point-in-time join fix — leaderboard period_start_aua + lifecycle_aua unblocker</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Phase 0 RAVC3 from DS~C 20260505T170029Z surfaced single-callsite fix; Phase 1 GO dispatched same turn -->
    <priority>high</priority>
    <estimated_effort>~1.5-2h DS~C (1h code + 0.5h gate + 0.25h deploy + 0.25h MATCH/RAVC); AE chain trigger separate</estimated_effort>
  </metadata>

  <references>
    <ref type="phase_0_evidence">DS~C RAVC3 to COO 20260505T170029Z — full callsite audit (7 callsites, 1 MUST FIX, 6 KEEP @latest), per-callsite verdicts, recommended fix architecture, effort estimate. **This RAVC3 IS the technical spec for Phase 1.**</ref>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v7 line 213 — ADVI_RPBKTPI follow-on entry; line 120 — visual manifest (leaderboard GRO Peter Lee +4213.9% / Patrick Scanlan +7522.3% absurd %); line 122 — lifecycle_aua all-zero per advisor</ref>
    <ref type="root_cause_trace">DS~D HISTBF post-mortem §3 (matrix line 213) confirmed `latest_accounts_v2_key()` L162-172 returns `keys[-1]` always; HISTBF.004 rewrote 1998 holdings_*.parquet on correct positions_mv silver but did not fix accounts_v2@latest join</ref>
    <ref type="downstream_note">INF_I_D03 L560-565 override workaround becomes no-op after this fix — flag for Phase 2 cleanup TO</ref>
  </references>

  <context>
    INF_B_00.canonical_holdings.py L162 defines `latest_accounts_v2_key()` returning `keys[-1]` (latest partition unconditionally). Called via `load_accounts_v2()` at L177, which is invoked once at L277 in main() BEFORE the per-date snapshot loop. The same `accounts` DataFrame is then reused for every `build_snapshot(snap_date_str, accounts)` call (L281-282).

    Result: every historical snapshot's `rep_bucket` field reflects today's advisor attribution, not the rep mapping that existed AT snap_date_str. Manifests visually as leaderboard MAX-window `period_start_aua: null` + absurd `aua_growth_pct` (Peter Lee +4213%, Patrick Scanlan +7522%).

    DS~C Phase 0 RAVC3 confirmed: this is the SOLE callsite that needs fixing. 6 other `latest_accounts_v2_key`-equivalent patterns across data/orion/ are correctly @latest (cumulative chart aggregation, NMNC inception dates, ETL on today's TRN, manual API current-state pulls).

    Phase 1 fix architecture per RAVC3 §(c):
    1. New `list_accounts_v2_dates() -> dict[str, str]` — analogous to existing `list_positions_mv_dates()`; 1 S3 list call returns `{date_str: s3_key}`.
    2. New `accounts_v2_key_for_snap(snap_date_str, available_dict) -> str` — in-memory lookup `max(d for d in available if d <= snap_date_str)`; fallback to oldest if snap predates all partitions.
    3. Refactor `load_accounts_v2()` to accept `key: str` param.
    4. Move `load_accounts_v2()` call inside the per-date loop with point-in-time key.

    ~15-20 lines of new/changed code, confined to INF_B_00.canonical_holdings.py. No other scripts modified in this Phase.

    **S3 partition reality:** only 2 accounts_v2 partitions exist (2026-04-28, 2026-04-29). Practical impact for snaps before 2026-04-28 = fallback to oldest (Apr-28), same as current @latest behavior pre-Apr-28. Fix's point-in-time precision grows as accounts_v2 silver feed accumulates daily partitions.
  </context>

  <phase id="1" when="before any code edit">
    <step>
      <run>cat data/orion/scripts/gold/INF_B_00.canonical_holdings.py | sed -n '160,180p;275,285p' — confirm current state of L162 (`latest_accounts_v2_key` def), L177 (`load_accounts_v2` def), L277 (pre-loop call), L281 (build_snapshot call)</run>
      <expect>Code shape matches DS~C Phase 0 RAVC3 description: function definitions and pre-loop call structure as enumerated.</expect>
      <if_mismatch>If code has diverged from RAVC3 description: re-run Phase 0 callsite audit. Surface to COO before proceeding.</if_mismatch>
    </step>
    <step>
      <run>grep -n "list_positions_mv_dates" data/orion/scripts/gold/INF_B_00.canonical_holdings.py — find existing pattern to model new helpers on</run>
      <expect>≥1 existing reference to `list_positions_mv_dates()` in INF_B_00 — that function's signature and S3-listing pattern is the template for new `list_accounts_v2_dates()`.</expect>
      <if_mismatch>If `list_positions_mv_dates` not in INF_B_00: search broader (`data/orion/`); use whichever similar S3-date-listing helper is most similar to the new helper's intent.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implement fix">
    <step>
      <run>Edit data/orion/scripts/gold/INF_B_00.canonical_holdings.py: (1) add `list_accounts_v2_dates()` helper modeled on `list_positions_mv_dates()`; (2) add `accounts_v2_key_for_snap(snap_date_str, available)` lookup; (3) refactor `load_accounts_v2(key)` to accept key param (remove internal key-discovery); (4) in main() loop, call `load_accounts_v2(accounts_v2_key_for_snap(snap_date_str, ...))` per snap.</run>
      <expect>~15-20 lines new/changed. Old `latest_accounts_v2_key()` at L162 may stay (still used by 1 internal callsite check) or be deleted if fully obsolete. Existing `load_accounts_v2()` callers updated to pass key explicitly.</expect>
      <if_mismatch>If refactor reveals additional internal callers of `load_accounts_v2()` not in RAVC3 audit: handle them locally if scope is identical (same point-in-time semantics needed); surface to COO if any callsite needs different behavior.</if_mismatch>
    </step>
    <step>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_B_00.canonical_holdings.py</run>
      <expect>Exit 0 — py_compile + AST scanner + ruff all PASS. Script must have `from __future__ import annotations` as first import (per CLAUDE.md rule 15 + ADHC_DSFLOW.004).</expect>
      <if_mismatch>Fix all errors. Common gotchas: missing `from __future__ import annotations`, undefined names from incomplete refactor, ruff target-version py39 mismatch.</if_mismatch>
    </step>
    <step>
      <run>Dry-run verification — run INF_B_00 locally for two snap dates that should now produce different rep_bucket values: e.g., 2026-04-28 and 2026-04-29. Compare emitted parquet rep_bucket distribution. (If local execution not feasible, document the test-plan for QA-runner phase.)</run>
      <expect>Per-snap rep_bucket values now reflect point-in-time accounts_v2 partition; differ between two test dates if accounts_v2 changed advisor attribution between Apr-28 and Apr-29.</expect>
      <if_mismatch>If rep_bucket identical across two dates: either (a) accounts_v2 didn't change advisor attribution between those dates (legitimate; verify via direct silver read), or (b) fix didn't take effect (re-check call-site refactor).</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after fix lands locally — commit + deploy">
    <step>
      <run>git add data/orion/scripts/gold/INF_B_00.canonical_holdings.py + commit via .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_C &lt;0.4.0_DS_ClientPlatform_C@opal.agent&gt;" -m "fix(INF_B_00): point-in-time accounts_v2 join — ADVI_RPBKTPI.001 Phase 1" -- data/orion/scripts/gold/INF_B_00.canonical_holdings.py</run>
      <expect>Clean commit; safe-commit.sh PASS (no contamination from unrelated working-tree files); pre-commit hook PASS (owned-paths allows DS~C to commit data/orion/scripts/gold/).</expect>
      <if_mismatch>If owned-paths blocks: surface to COO; this is in DS~C scope per data/orion/scripts/gold ownership.</if_mismatch>
    </step>
    <step>
      <run>git push origin CLOUD &amp;&amp; aws s3 cp data/orion/scripts/gold/INF_B_00.canonical_holdings.py s3://opal-data-inf/code/gold/ &amp;&amp; comp-pipescript deployed INF_B_00</run>
      <expect>Push succeeds; S3 upload confirms; comp-pipescript deployed returns MATCH.</expect>
      <if_mismatch>STALE → re-upload until MATCH. MISSING → check S3 path / IAM. If push fails: pull --rebase + retry.</if_mismatch>
    </step>
    <step>
      <run>SSM dispatch INF_B_00 + downstream chain (INF_B_01, INF_I_D02, INF_I_D02b, INF_I_D03, INF_D_*) on inf-gold-qa-runner via aws ssm send-command. Use `OUTPUT_PREFIX=qa/` per feedback memory feedback_ssm_output_prefix_env.md.</run>
      <expect>SSM CommandId returned; status InProgress → Success within reasonable time. Poll `aws ssm get-command-invocation` until terminal state.</expect>
      <if_mismatch>Failed/Cancelled/TimedOut → pull stdout + stderr; diagnose; surface to COO. Do NOT auto-retry without instruction.</if_mismatch>
    </step>
    <step>
      <run>Empirical verification post-chain: aws s3 cp s3://opal-data-inf/qa/platinum/firm/leaderboard.json - | jq '.windows.MAX.entries[] | {advisor_id, period_start_aua, aua_growth_pct, lifecycle_aua}'</run>
      <expect>MAX-window period_start_aua now non-null for all 4 advisors (was null pre-fix); aua_growth_pct in plausible range (single-digit to low-triple-digit %, not +4213%); lifecycle_aua decomposition non-zero for at least one advisor.</expect>
      <if_mismatch>If period_start_aua still null: fix didn't propagate or downstream chain didn't re-run all dependent scripts. Check INF_I_D02 leaderboard output specifically.</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="after Phase 3 verification — RAVC4 to COO">
    <step>
      <run>RAVC4 MCP to 2.0.0_SA_COO with: (a) commit hash, (b) S3 MATCH evidence, (c) SSM CommandId + final status, (d) before/after leaderboard period_start_aua + aua_growth_pct table for all 4 advisors, (e) downstream notes (INF_I_D03 L560-565 workaround now no-op — flag for Phase 2 cleanup TO).</run>
      <expect>RAVC4 delivered. ADVI_RPBKTPI.001 ready for COO close. AE 0.6.1 PROD-trigger gate (if QA-PASS confirmed) sent separately by COO/AE.</expect>
      <if_mismatch>If RAVC4 has remediation gaps: cite explicitly so COO can author Phase 2 follow-up TO.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**No DS-side overlap.** DS~A on AUDIT-007 (active_since/radial_12m read), DS~B on AUDIT-003 (silver assets rep_id=6), DS~D on AUDIT-008 (AUA strip stale). All distinct artifacts/scripts.</coord>
    <coord>**INF_I_D03 follow-on:** the L560-565 advisor_key override workaround in INF_I_D03 becomes a no-op after this fix. Do NOT touch INF_I_D03 in this TO — flag for Phase 2 cleanup TO. Composition.json regen happens via the chain re-run, not via INF_I_D03 code change.</coord>
    <coord>**AE 0.6.1 / 0.7.0 PROD trigger:** QA-runner SSM dispatch + verification is DS~C scope (per CLAUDE.md rule 13). PROD chain trigger after QA-PASS RAVC4 ACK is AE scope (`bd-gold-trigger` analog for inf-pipeline if it exists, otherwise AE 0.6.1 owns Inflection PROD trigger). DS~C does NOT trigger PROD.</coord>
    <coord>**RPBKTPI Phase 2 (cleanup):** INF_I_D03 L560-565 workaround removal queued as separate TO once Phase 1 RAVC4 confirms fix lands. No work on it this Phase.</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      <reason>Code patch changes the point-in-time semantics of accounts_v2 join. All historical snapshots produced by INF_B_00 since pipeline inception are pre-patch — they reflect today's rep_bucket attribution, not point-in-time. Downstream artifacts (INF_I_D02 leaderboard, INF_D_* per-advisor summaries) were derived from pre-patch holdings and carry the same defect.</reason>
      <s3_prefix_globs>
        <glob>s3://opal-data-inf/qa/silver/canonical_holdings/*</glob>
        <glob>s3://opal-data-inf/qa/platinum/firm/leaderboard.json</glob>
        <glob>s3://opal-data-inf/qa/platinum/advisors/*/summary.json</glob>
        <glob>s3://opal-data-inf/qa/platinum/advisors/*/book.json</glob>
      </s3_prefix_globs>
      <verification>aws s3 ls each prefix post-chain; confirm LastModified &gt; Phase 3 commit timestamp; spot-check leaderboard.json for non-null period_start_aua per Phase 3 verification step.</verification>
      <downstream_consumer_freshness_gate>FE consumers of leaderboard.json (BooksTab N1 leaderboard panel) read QA artifacts on the qa/* path during this Phase; PROD propagation is Phase 5 (post-RAVC4 PROD chain trigger by AE).</downstream_consumer_freshness_gate>
    </reprocess_required>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before writing fix">
      <step>
        <run>comp-pipescript io INF_B_00</run>
        <expect>Same WARN: "dynamic key construction detected; no static S3 paths indexed" output that DS~C captured in Phase 0 RAVC3. Acknowledge limitation; manual review per RAVC3 is the substitute.</expect>
        <if_mismatch>If comp-pipescript now succeeds with full I/O (improved indexing): use it; otherwise rely on Phase 0 manual analysis.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_B_00.canonical_holdings.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix per gate output; re-run.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + S3 upload">
      <step>
        <run>comp-pipescript deployed INF_B_00</run>
        <expect>MATCH.</expect>
        <if_mismatch>STALE → re-upload until MATCH.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript postdeps INF_B_00</run>
        <expect>List of required post-steps for INF_B_00 (downstream chain). Use to confirm SSM dispatch covers full chain (INF_B_01 → INF_I_D02 → INF_I_D02b → INF_I_D03 → INF_D_*).</expect>
        <if_mismatch>If postdeps surfaces additional required scripts not in the SSM dispatch: extend SSM scope before triggering.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Phase 1+2 executed: code patch lands per RAVC3 architecture (4 changes: 2 new helpers + load_accounts_v2(key) refactor + per-loop call). ds-commit-gate exit 0.</criterion>
    <criterion id="AC2">Phase 3 commit + push + S3 upload + comp-pipescript deployed MATCH.</criterion>
    <criterion id="AC3">SSM chain dispatch on inf-gold-qa-runner: terminal status Success; full chain INF_B_00 → INF_I_D02 → INF_D_* re-emits.</criterion>
    <criterion id="AC4">Empirical leaderboard MAX-window: period_start_aua non-null for all 4 advisors; aua_growth_pct in plausible single-to-triple-digit range (no +4213% / +7522% absurd values).</criterion>
    <criterion id="AC5">Session log includes Compiler Tools section with all comp-* runs + outputs + verdicts per SESSION_LOG_STANDARD.md.</criterion>
    <criterion id="AC6">RAVC4 to COO with full evidence package per Phase 4 step.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T17:05:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Phase 0 RAVC3 accepted in full — single-callsite verdict, fix architecture, effort estimate all sound. Begin Phase 1 immediately. Standing by for RAVC4 (Phase 3 evidence + Phase 4 verification). AE 0.6.1 PROD trigger handled separately post-QA-PASS.</message>
  </go_signal>
</task_order>
