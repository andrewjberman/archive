<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-20</date>
    <status>draft</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — low impact, quick close. Can run fully parallel to FIX-TO 1 / 2 / 3A (different file, different S3 surface).</priority>
    <bug_reference>Bug 5 per SYNTHESIS/bug_attribution.md — nna_atomic/ missing 2026-04-14 partition. D_00c + D_02 misattribute Apr 14 NNA to prior-day partition.</bug_reference>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 1 — path sub-class, tail case)</ref>
    <ref type="handoff">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md §FIX-TO 5</ref>
    <ref type="attribution">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md Bug 5</ref>
    <ref type="upstream-mcp">CTO 20260420T134734Z</ref>
  </references>

  <objective>
    Run C_01 (canonical_nna) with an explicit Apr 14 target to write the missing `gold/canonical/nna_atomic/2026-04-14.parquet` partition. Verify the partition is present in both `nna/` and `nna_atomic/` after the run (gap-parity check). No code changes expected — this is a targeted backfill invocation.
  </objective>

  <scope>
    **Defect (verbatim from bug_attribution.md Bug 5):**
    `gold/canonical/nna_atomic/2026-04-14.parquet` is absent. D_00c and D_02 NNA calculations for April 15 windows attribute the prior-day partition to April 13 instead of April 14 (Apr 14 never written). Apr 14 NNA unallocated.

    **Root cause:** C_01 backfill design stopped at Apr 13 when T1 backfill ran on Apr 16.

    **Fix surface:**
    Invoke `C_01.canonical_nna` with `--date 2026-04-14` (or whatever date-target flag C_01 exposes). No script modification expected. If C_01 doesn't accept a single-date backfill flag, consult C_01's CLI surface and either (a) use an existing range flag (`--start 2026-04-14 --end 2026-04-14`) or (b) MCP COO before adding a CLI flag (scope expansion).

    **Verification:**
    After the run, verify both:
    - `s3://<gold-bucket>/gold/canonical/nna/2026-04-14.parquet` present (if not already)
    - `s3://<gold-bucket>/gold/canonical/nna_atomic/2026-04-14.parquet` present
    Row counts should be non-zero and consistent with the 2026-04-13 + 2026-04-15 partitions (gap-parity).

    **OUT OF SCOPE:**
    - Any broader backfill of other missing dates (if discovered, file separate TO)
    - Any C_01 code modification beyond minimal CLI flag handling (if needed)
    - Any nna_atomic/ schema changes (that is Option B follow-up, not here)
    - D_00c / D_02 re-run coordination (may be needed but is a separate closeout action)
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-run diligence">
      <step>
        <run>aws s3 ls s3://&lt;gold-bucket&gt;/gold/canonical/nna_atomic/ | grep 2026-04-1</run>
        <expect>Confirm Apr 13 and Apr 15 partitions present; Apr 14 absent. Also check `nna/` for the same window — document actual state (is `nna/2026-04-14.parquet` also absent?).</expect>
        <if_mismatch>If state doesn't match bug_attribution.md claim, MCP COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>python data/black_diamond/scripts/gold/C_01.canonical_nna.py --help (or inspect CLI at top of file)</run>
        <expect>Identify the exact flag shape for targeting a single date. Document it in fix_to_5_evidence.md.</expect>
        <if_mismatch>If no single-date or start/end flag exists, MCP COO before modifying C_01.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed C_01.canonical_nna</run>
        <expect>Confirms bd-gold-runner has current C_01 code. Status MATCH.</expect>
        <if_mismatch>STALE/MISSING = coordinate deploy before running the backfill.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="run + post-run verification">
      <step>
        <run>Invoke C_01 with explicit Apr 14 target via bd-gold-trigger or appropriate path (follow standard DS gold-script run cycle).</run>
        <expect>C_01 completes; writes `gold/canonical/nna_atomic/2026-04-14.parquet` (and `nna/2026-04-14.parquet` if C_01 produces both).</expect>
        <if_mismatch>Any error = capture run log + escalate to COO.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://&lt;gold-bucket&gt;/gold/canonical/nna/ + /nna_atomic/ for 2026-04-14</run>
        <expect>Both partitions present (or `nna/2026-04-14.parquet` also present if it was also missing).</expect>
        <if_mismatch>Missing = run didn't write. Investigate C_01 output/log.</if_mismatch>
      </step>
      <step>
        <run>pyarrow read row count + columns for new partition vs Apr 13 and Apr 15 neighbors</run>
        <expect>Non-zero rows; column set consistent; row count in the same order of magnitude as neighbors.</expect>
        <if_mismatch>Zero rows or schema drift = partition unusable; escalate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>s3://&lt;gold-bucket&gt;/gold/canonical/nna_atomic/2026-04-14.parquet</path>
      <description>Newly written Apr 14 partition. Plus `nna/2026-04-14.parquet` if absent.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX5/fix_to_5_evidence.md</path>
      <description>
        Pre-run S3 listing (proving gap), C_01 CLI flag used, run log summary, post-run S3 listing (proving fill), row count + schema comparison against Apr 13 + Apr 15 neighbors.
      </description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Pre-run S3 state documented (Apr 13 present, Apr 14 absent, Apr 15 present) in both `nna/` and `nna_atomic/`
    - [ ] C_01 invocation uses existing CLI flag (no script modification) OR, if flag must be added, COO+CTO escalated first
    - [ ] Apr 14 partition present post-run in `nna_atomic/` (and `nna/` if it was also missing)
    - [ ] Row count non-zero and consistent with neighbor partitions
    - [ ] Schema matches neighbor partitions
    - [ ] Downstream D_00c + D_02 re-runs (if required by production date) are coordinated with COO
  </acceptance_criteria>

  <guardrails>
    - **A→D-rerun-sensitive writes pre-flag:** per `feedback_ad_rerun_sensitive_preflag_before_s3_write.md`, writing a new canonical_nna partition IS an A→D-rerun-sensitive write. Pre-flag COO + CTO BEFORE the C_01 invocation — even with this TO as authority. 60-sec don't-object window.
    - **No scope creep:** single missing date fill only. If other dates are also missing, document in evidence file and file separate TO — do NOT expand this run.
    - **No schema changes** to nna_atomic/ (Option B follow-up owns that).
    - **Standard gold-script deploy + run cycle** (DS owns end-to-end).
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - SYNTHESIS/coo_handoff.md §FIX-TO 5
       - SYNTHESIS/bug_attribution.md Bug 5
       - C_01.canonical_nna.py CLI surface (top of file / argparse section)
       - data/black_diamond/diagnostics/STAUDT/layer_C/ (any relevant C-layer audit evidence)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min
    - Phase 0 gate: MCP COO with CLI flag + pre-run S3 state before invoking C_01
    - Pre-S3-write pre-flag: 60-sec heads-up to COO + CTO before `aws s3 cp` or bd-gold-trigger
    - RAVC step 4: MCP COO with post-run S3 listing + row/schema check
  </completion_protocol>
</task_order>
