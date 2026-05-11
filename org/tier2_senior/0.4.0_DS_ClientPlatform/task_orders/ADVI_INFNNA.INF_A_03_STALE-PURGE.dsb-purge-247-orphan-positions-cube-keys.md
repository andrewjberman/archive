<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.INF_A_03_STALE-PURGE</id>
    <project>ADVI_INFNNA</project>
    <title>One-shot purge of 247 stale orphan parquets in s3://opal-data-inf/gold/positions_cube/ (2019-09-17 → 2020-05-25)</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>low</priority>
    <estimated_effort>~10 min (enumerate + confirm + delete + verify)</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 — "GO on all 4 in your recommended sequence"</authorized_by>
    <execution_gate>BLOCKED by INF_A_02_RETIRE completion. Sequence #4 of 4. Note: S3 deletion = destructive but reversible (versioning if enabled); requires explicit confirmation of 247-key list before rm.</execution_gate>
  </metadata>

  <references>
    <ref type="parent_audit">A-GROUP-AUDIT findings doc Finding #4 — 247 stale legacy parquets in gold/positions_cube/ pre-2020-05-26</ref>
    <ref type="affected_path">s3://opal-data-inf/gold/positions_cube/{2019-09-17..2020-05-25}.parquet</ref>
    <ref type="evidence">aws s3 ls s3://opal-data-inf/gold/positions_cube/ — 2,425 total objects; current INF_A_03 code path writes 2,178 (silver/transactions earliest 2020-05-26 → today). Delta of 247 = pre-2020-05-26 orphans from a prior run before silver was clipped.</ref>
  </references>

  <context>
    INF_A_03.positions_cube.py current MIN_OUTPUT_DATE='2019-09-01' is dead code — `target_dates` is computed from `max(MIN_OUTPUT_DATE, str(min_date))` where `min_date` is `txns['trade_date'].min()` = 2020-05-26 today. So the code-path produces target_dates starting at 2020-05-26.

    But `gold/positions_cube/` has 2,425 daily parquets; the 247 in 2019-09-17 → 2020-05-25 are leftover from when bronze had 2019-era data. They each weigh ~3,259 bytes (essentially-empty stubs).

    Three failure modes if left in place:
    1. Downstream B/C/D scripts that iterate `gold/positions_cube/` may waste compute on empty-stub days (depends on script behavior — most clip to silver/transactions date range first, but worth verifying via `comp-blast`).
    2. Storage cost (negligible — 247 × 3KB = ~750KB).
    3. Investigative noise (analysts wondering why we have 2019 cube data when silver only goes back to 2020-05).

    **DESTRUCTIVE OPERATION** — `aws s3 rm` on production gold artifacts. Per CLAUDE.md autonomy section: "deleting S3 objects" is NOT pre-authorized. Requires Andrew or COO explicit approval before execution.
  </context>

  <scope>
    <step>
      Enumerate the 247 keys: `aws s3 ls s3://opal-data-inf/gold/positions_cube/ | awk '$4 < "2020-05-26.parquet"' > /tmp/stale_cube_keys.txt`. Verify count = 247 (or close — exact count is empirical).
    </step>

    <step>
      Spot-check 3 keys for size + last-modified to confirm orphan status: should be ~3,259 bytes, last-modified 2026-04-27 17:42:20 (matches the original full-history build batch).
    </step>

    <step>
      `comp-blast gold/positions_cube` to enumerate downstream consumers; verify none of them iterate-by-listing the prefix (vs iterate-by-date-range from a known min-date). If any do iterate-by-listing, FLAG before proceeding — purge could break their date assumptions.
    </step>

    <step>
      **Approval gate:** before destructive op, send MCP message to 2.0.0_SA_COO with key list + comp-blast results. Wait for explicit GO. Do NOT proceed without it.
    </step>

    <step>
      On GO: `aws s3 rm s3://opal-data-inf/gold/positions_cube/<key>` for each of the 247 keys. Use `--dryrun` first to print what will be deleted; capture output. Then run for real.
    </step>

    <step>
      Verify post-purge: `aws s3 ls s3://opal-data-inf/gold/positions_cube/ | wc -l` = 2,178 (or expected count). Spot-check first remaining key is `2020-05-26.parquet`.
    </step>
  </scope>

  <acceptance_criteria>
    1. 247 stale keys enumerated + spot-checked.
    2. comp-blast confirms no downstream consumer iterates by listing.
    3. Explicit COO/Andrew GO captured in session log before destructive op.
    4. `aws s3 rm` dry-run output captured.
    5. Real purge executed; post-count = 2,178 (or expected).
    6. First remaining key = `2020-05-26.parquet`.
    7. Session log captures all of the above + commit SHA (if any code changes — likely none, just S3 hygiene).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>`comp-blast gold/positions_cube`</run><expect>Enumerate consumers; verify none iterate-by-listing.</expect></step>
    </phase>
    <phase id="3" when="after destructive op">
      <step><run>`aws s3 ls s3://opal-data-inf/gold/positions_cube/ | wc -l`</run><expect>2,178 (or empirical post-purge count).</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None code-wise. Loosely bundled with INF_A_03_PARALLEL-EXPAND — could be done first as cleanup, or after. No technical dependency.
  </dependencies>

  <safety_note>
    `aws s3 rm` on production gold artifacts is DESTRUCTIVE per CLAUDE.md autonomy boundary. MUST get COO + Andrew GO before execution. Bundle the 247-key list in the GO request for explicit visibility.
  </safety_note>

  <next>On purge: gold/positions_cube/ shape matches code-path expectations. No functional change downstream (consumers should already date-clip).</next>

  <draft_note>
    Authored DRAFT by 0.4.0_DS_ClientPlatform~B 2026-05-11 per COO idle-time suggestion + AC9 scope-creep guard. Awaiting COO ratification + dispatch.
  </draft_note>
</task_order>
