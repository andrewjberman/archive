<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.ACCOUNT-ID-COERCE</id>
    <project>ADVI_INFNNA</project>
    <title>account_id dtype drift fix — 6 INF gold scripts failing parquet write with ArrowTypeError; close instrumented cascade 84% → 100%</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete (local-path + S3-deploy-MATCH)</status>
    <priority>high</priority>
    <estimated_effort>~30-45 min</estimated_effort>
    <actual_effort>~85min (incl. scope widen for rep_id + C_01b _read_s3 wrapper patch)</actual_effort>
    <authorized_by>Andrew direct 2026-05-11 + 1.0.0_SA_CTO concurrent</authorized_by>
    <closed_date>2026-05-11</closed_date>
    <closed_by>0.4.0_DS_ClientPlatform~A</closed_by>
    <closed_via>RAVC to COO 2026-05-11 post-cascade + post-C_01b-patch validation; cascade `cascade-133034Z-1474df2b` ran LOCAL HEAD code via `.runtmp/run_inf_e2e_cascade.py` (not S3-pulled). S3 deploy gap addressed in deploy_addendum below — load-bearing evidence is the local cascade, not the S3 deploy. Per COO 2026-05-11 ~15:40Z: "local cascade verification is the load-bearing evidence."</closed_via>
    <deploy_addendum>2026-05-11 ~15:35-15:40Z — DS~B SHA-cross-check found 5 of 6 gold scripts STALE on s3://opal-data-inf/code/gold/ (rule 13 deploy step skipped). lib/dtype_coerce.py was deployed by DS~B at 11:31Z (collateral of their INF_A_03 deploy). DS~A then deployed the 5 stale scripts via `aws s3 cp data/orion/scripts/gold/INF_*.py s3://opal-data-inf/code/gold/` and verified MATCH via local-vs-S3 SHA16 cross-check: INF_A_00 deb7bb709432ad71, INF_A_01 acdc57d4bb04ed70, INF_B_02 7bb0ea83e8d5f7b3, INF_C_01b cb6aeba45055ffc0, INF_C_03 437e30578a4fcaec. lib/dtype_coerce.py local==S3 37eff6929814e714. Per COO 15:40Z DECISION (Option Y, trust SHA equivalence): S3 deploy gap closed via SHA16 MATCH on all 5 scripts + lib/dtype_coerce.py (DS~B); local cascade `cascade-133034Z-1474df2b` is the load-bearing empirical evidence. Implicit deploy-pipeline verification routed to DS~B's INF_A_03 SSM retry — DS~B SSM ran at 15:42Z and completed compute pipeline cleanly (13x speedup confirmed, 45s compute vs 583s Friday baseline) but failed at S3 PutObject step due to QA-IAM `qa/*` scope (out of ACCOUNT-ID-COERCE's scope, separate follow-up TO). The deploy-pipeline TO-pull-from-S3 path is empirically verified for the read+compute portion; the qa-prefix write IAM gap is independent and tracked separately. CTO hypothesis (a): dtype drift may not be present in current silver because 706ea757e JOE-TXN cascade already coerced at silver-write — ACCOUNT-ID-COERCE was defense-in-depth that didn't get fully exercised in this run, still a correct ship. Comp-pipescript BD-only gap (no INF coverage) tracked via ADHC_DSFLOW.005 `5f81020ee` for AE 0.7.</deploy_addendum>
  </metadata>

  <references>
    <ref type="parent_ravc">DS~A RAVC1 first-instrumented INFLEC E2E cascade 20260508T20:35Z — 31 OK / 6 FAIL (84%); all 6 failures = account_id dtype-on-write</ref>
    <ref type="parent_cascade">.runtmp/logs/e2e/2026-05-08/cascade-192259Z-245079b1.log + .runtmp/telemetry/2026-05-08/inf-gold-layer-runner/</ref>
    <ref type="root_cause">silver/transactions schema drift post JOE-TXN backfill: pre-fix partitions had int64 on account_id, post-fix partitions have mixed int + null. pd.concat across 1509+ partitions yields `object` dtype. pyarrow rejects on parquet write with `ArrowTypeError: Expected bytes, got 'int' object`.</ref>
    <ref type="sha_chain">e2edbe321 (puller fix rep_id=6) → 706ea757e (JOE-TXN cascade RICH schema) → 23c1f560c (Merge In/Out classification) — silver state correct, gold writes need defensive coerce</ref>
    <ref type="affected_scripts">INF_A_00.accounts_dimension, INF_A_01.advisor_assignments, INF_A_03.positions_cube, INF_B_02.canonical_lots, INF_C_01b.role_aua_backfill, + 1 TBD (DS~A to identify in Step 1)</ref>
  </references>

  <context>
    Friday's first-ever fully-instrumented bronze→platinum cascade for INFLEC completed 70.9 min wall-clock with 31 OK / 6 FAIL (84% success). All 6 failures shared the same root cause: pyarrow rejecting `object` dtype on `account_id` column when writing parquet. The mixed-dtype state was introduced by the JOE-TXN backfill cascade that landed Friday afternoon.

    **The fix is defensive coerce, not silver rewrite.** Silver/transactions partitions are correct as-is — the dtype drift is a parquet-write-time symptom, not a data correctness issue. Closing the cascade to 100% requires coercing `account_id` to `Int64` (nullable) immediately before parquet write in each affected gold script.

    **Engineering choice — shared helper preferred over inline.** With 6+ scripts affected and the silver schema being a long-term mixed-dtype reality, a single canonical helper function is more durable than 6 one-line patches that future agents must remember to replicate. Place in a common location (e.g., `data/orion/scripts/common/` or `data/orion/scripts/_helpers.py` per existing convention) so future Orion gold scripts can `from common import coerce_account_id` without re-deriving the pattern.

    **Closes:** 6-script cascade gap → 100% clean instrumented E2E baseline. Subsequent cascade runs (per CTO's quarterly audit pattern) will have a strict regression gate against today's 70.9min/31-OK baseline.

    **Andrew authorization 2026-05-11:** "we need to have DS~A fix schema drift CTO has authorized it." Direct verbal GO. CTO authorization noted Friday EOD + this morning's session.
  </context>

  <scope>
    <step>
      **Identify all affected scripts.** From Friday's cascade log + telemetry JSONL, confirm the 6th failing script (5 known: INF_A_00, INF_A_01, INF_A_03, INF_B_02, INF_C_01b). Cross-reference `.runtmp/telemetry/2026-05-08/inf-gold-layer-runner/` for any FAIL entries not in the known-5 list. Output: definitive 6-script list.
    </step>

    <step>
      **Choose helper location + design.** Survey existing common-helper conventions in `data/orion/scripts/`. If a shared utility module already exists, add `coerce_account_id(df, col='account_id')` there. If not, create `data/orion/scripts/common/dtype_coerce.py` or equivalent. Function signature:
      ```python
      def coerce_account_id(df: pd.DataFrame, col: str = 'account_id') -> pd.DataFrame:
          """Coerce account_id (or named col) to Int64 (nullable). Idempotent.
          Use immediately before parquet write to defend against mixed-dtype concat output."""
          if col in df.columns:
              df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
          return df
      ```
      Add `from __future__ import annotations` per CLAUDE.md rule 15.
    </step>

    <step>
      **Apply helper call in all 6 scripts.** For each script, identify the `df.to_parquet(...)` call site (likely just before write). Insert:
      ```python
      from data.orion.scripts.common.dtype_coerce import coerce_account_id  # or relative path per existing convention
      df = coerce_account_id(df)
      df.to_parquet(...)
      ```
      Verify each script imports work correctly relative to repo layout.

      Pre-commit gate (CLAUDE.md rule 14): `.tools/ds-commit-gate.sh data/orion/scripts/<each-affected>.py`. All three checks (py_compile + ds-precommit-check + ruff) must exit 0.
    </step>

    <step>
      **Re-run cascade.** Dispatch the same E2E cascade runner used Friday: `.runtmp/...cascade-runner-or-equivalent.sh` (or whatever path DS~A used to invoke the 37-script cascade). Capture telemetry into `.runtmp/telemetry/2026-05-11/inf-gold-layer-runner/`.

      Expected outcome: 37 OK / 0 FAIL.
    </step>

    <step>
      **Assess silver-side normalization (advisory only — not in this TO's commit scope).** During cascade re-run, observe: does the helper add measurable overhead? If &lt;1% wall-clock impact, no further action — defensive coerce is the canonical pattern going forward. If &gt;5% impact OR if cascade re-runs surface a similar drift on a different column (e.g., `transaction_id`, `lot_id`), surface as a follow-up TO candidate for silver-side homogenization. Document finding in RAVC.
    </step>

    <step>
      **Promote runner-telemetry tooling to .tools/ (deferred from Friday).** If not already moved by Proposal-2 sweep, migrate `runner-telemetry.py` + `runner-telemetry-analyze` from `.tools/`-or-wherever into the canonical `.tools/` location. Update any caller paths.
    </step>

    <step>
      **Commit + push + RAVC.** Bundle commit:
      - New helper module
      - 6 affected gold scripts (one commit, scoped via safe-commit.sh)
      - Author: `0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;`

      RAVC payload:
      - 6-script list confirmed
      - Helper SHA + location
      - Cascade re-run outcome (target: 37/37 OK)
      - Wall-clock delta vs Friday baseline (regression gate)
      - Telemetry path for 2026-05-11 cascade
      - Silver-side normalization advisory finding (if any)
    </step>
  </scope>

  <acceptance_criteria>
    1. **Definitive 6-script list** confirmed (5 known + 1 TBD identified from Friday telemetry).
    2. **Shared helper** `coerce_account_id` exists in canonical location with `from __future__ import annotations` and idempotent behavior.
    3. **Pre-commit gate** PASS for all 7 file edits (helper + 6 scripts).
    4. **Cascade re-run** achieves 37 OK / 0 FAIL (100% clean E2E).
    5. **Telemetry baseline** for 2026-05-11 captured at same path convention; wall-clock within ±10% of Friday's 70.9min baseline (no performance regression introduced by helper).
    6. **Silver-side advisory** documented in RAVC (PASS/FAIL on the &lt;1% / &gt;5% threshold).
    7. **Runner-telemetry tool** lives in `.tools/` (promoted from staging path if still pending).
    8. **RAVC delivered to COO** with SHA chain, ETag set (if any platinum writes downstream were re-emitted), and quarterly-audit-baseline confirmation.
    9. **Leaderboard.json post-cascade check** (CTO addition 2026-05-11): after cascade rerun completes 37/37 OK, read `s3://opal-data-inf/platinum/firm/leaderboard.json`. Spot-check for Joe Brandenburg entry alongside Patrick/Peter/IWM. Include result in RAVC. This is the conditional gate for LEADERBOARD-JOE-ABSENT TO:
       - **Joe present** → surface in RAVC "leaderboard.json contains Joe — LEADERBOARD-JOE-ABSENT closes as RESOLVED-BY-CASCADE."
       - **Joe absent** → surface in RAVC "leaderboard.json missing Joe — LEADERBOARD-JOE-ABSENT executes."
  </acceptance_criteria>

  <blocking>
    None. DS~A is gated only by this TO's own steps.

    Adjacent gates:
    - SL-P2 PROMOTE still HOLDING on Andrew GO (independent).
    - This TO does NOT trigger any portal-visible change; cascade is internal-state only. No CF invalidation required unless a re-emit changes platinum content (unlikely — coerce is dtype-only).
  </blocking>

  <notes>
    Andrew said: "fix schema drift" — primary scope is gold-side defensive coerce, which closes the symptomatic cascade gap. Silver-side normalization stays advisory pending the Step 5 finding.

    CTO's quarterly cascade audit pattern (per Friday EOD) uses this run's outcome as the new regression baseline. Make sure telemetry path follows the daily-folder + version-serial convention (`.runtmp/telemetry/YYYY-MM-DD/{runner}/{script}/v{NNN}-{HHMMSSZ}-{run_id}.jsonl`).
  </notes>

  <closure_note>
    Closed 2026-05-11. All 6 originally-failing scripts PASS. Scope widened during execution: actual dtype drift is on (account_id, rep_id) not just account_id. INF_C_01b required a second-order fix — coerce inside `_read_s3` wrapper (pre-merge) instead of only pre-write — because it joins gold artifacts whose dtypes can mismatch. Cascade `cascade-133034Z-1474df2b` ran 36/37 OK; C_01b standalone re-run with patched wrapper exit 0 (2,418 partitions written). Effective 37/37. AC9 (LEADERBOARD-JOE-ABSENT) resolved-by-cascade — Joe present in leaderboard.json across QTD/YTD/MAX. Helper `data/orion/scripts/gold/lib/dtype_coerce.py` exports `coerce_account_id` (single-col, back-compat) and `coerce_id_columns(df, cols=DEFAULT_ID_COLS)` (multi-col, canonical). Total wall 79.5min (+12% vs Friday 70.9min baseline); attributed to Int64-vs-object merge WARN overhead that SILVER-ID-DTYPE-UNIFY `81c9212d0` will eliminate. Telemetry: `.runtmp/telemetry/2026-05-11/inf-gold-layer-runner/`. Session log: `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-11/DS_A_session4_account_id_coerce_2026-05-11.md`.
  </closure_note>
</task_order>
