<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.ACCOUNT-ID-COERCE</id>
    <project>ADVI_INFNNA</project>
    <title>account_id dtype drift fix — 6 INF gold scripts failing parquet write with ArrowTypeError; close instrumented cascade 84% → 100%</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>~30-45 min</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 + 1.0.0_SA_CTO concurrent</authorized_by>
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
</task_order>
