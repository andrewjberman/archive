<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.LEADERBOARD-JOE-ABSENT</id>
    <project>ADVI_INFNNA</project>
    <title>INF_D_00c leaderboard.json missing Joe Brandenburg — debug D_00c filter/aggregation logic; conditional execution after ACCOUNT-ID-COERCE cascade re-run</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending-conditional</status>
    <priority>high</priority>
    <estimated_effort>~1-2h (if executed)</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 (approved COO recommended routing)</authorized_by>
    <execution_gate>OBSERVE after ACCOUNT-ID-COERCE cascade re-run completes. IF Joe present in leaderboard.json post-cascade → close as RESOLVED-BY-CASCADE (no execution). IF Joe absent post-cascade → execute this TO.</execution_gate>
  </metadata>

  <references>
    <ref type="parent_finding">DS~A Proposal-2 sweep 2026-05-11 — `decaaf523` session log surfaced leaderboard.json has 3 entries (Patrick, Peter, IWM); Joe Brandenburg absent</ref>
    <ref type="upstream_evidence_1">canonical_nna_2025-12-15.parquet contains Joe (2 rows, $11.5K net_nna)</ref>
    <ref type="upstream_evidence_2">nmec_nmnc_nna.json contains Joe (nmnc_aua=$12.99M, 13 new clients)</ref>
    <ref type="friday_baseline">REGISTRY ADVI_INFNNA states Friday cascade had: 4 advisors / $199.6M firm AUA / Joe $16.2M / 21 clients — current state has only 3 advisors / no Joe, so leaderboard got rewritten without Joe between Friday cascade close and 2026-05-11</ref>
    <ref type="affected_script">data/orion/scripts/gold/INF_D_00c.* (leaderboard derivation)</ref>
  </references>

  <context>
    Joe Brandenburg is present in canonical_nna parquets and in INF_D_08's nmec_nmnc_nna.json output. He is absent from INF_D_00c's leaderboard.json output. This is a D_00c-specific filter/logic divergence.

    **Three hypotheses (from DS~A):**

    1. **D_00c queries snapshot-date canonical_nna only** — reads only `canonical_nna_2026-05-07.parquet` rather than aggregating full historical. If Joe has no activity on the snapshot date, he gets dropped. Other advisors (Patrick/Peter/IWM) have activity that date.

    2. **D_00c has an explicit rep_id allowlist** — excludes rep_id=6 (Joe) by stale assumption, missed in the INFLECTION_REP_IDS={3,6,11,12} expansion from 2026-05-07 UAD-CREATOR work.

    3. **D_00c rep_bucket mismatch** — recall the 'advisor' vs 'individual' fix from `706ea757e` JOE-TXN cascade. D_00c might filter on rep_bucket and Joe's bucket is mis-mapped at the D_00c stage.

    **Conditional execution:** ACCOUNT-ID-COERCE cascade re-run may regenerate leaderboard.json from clean D_00c run. If D_00c was simply blocked behind cascade failure and the regenerated leaderboard contains Joe, this TO closes as RESOLVED-BY-CASCADE without execution. If Joe remains absent post-cascade, the bug is in D_00c logic (one of the 3 hypotheses above) and this TO executes.
  </context>

  <scope>
    <step>
      **GATE CHECK (entry condition):** ACCOUNT-ID-COERCE TO `5287179fb` MUST be complete with cascade re-run successful (37/37 OK). DO NOT begin this TO before that gate is met.

      Once gate met: read `platinum/firm/leaderboard.json` from S3. Count entries.
      - **Joe present** → status = `complete (resolved-by-cascade)`. Append closure note + ETag. RAVC.
      - **Joe absent** → continue to Step 2.
    </step>

    <step>
      Read INF_D_00c source. Identify the function that produces `leaderboard.json`. Trace the advisors[] array derivation.
    </step>

    <step>
      Spot-check input data: read input parquets used by INF_D_00c at the specific path D_00c reads from. Confirm Joe rows present in INPUT to D_00c. If absent in input: bug is upstream (extends back into D_08 or earlier — surface as separate finding).
    </step>

    <step>
      Test the 3 hypotheses systematically:

      **H1 (snapshot-date filter):** Search D_00c for `canonical_nna_{snapshot_date}` or `latest` parquet read. If D_00c reads only the snapshot-date parquet, change to historical aggregation (mirror INF_D_08 pattern).

      **H2 (rep_id allowlist):** grep D_00c for hardcoded `[11, 12]` or `INFLECTION_REP_IDS` literals. Verify it includes {3, 6, 11, 12} per UAD-CREATOR canonical.

      **H3 (rep_bucket mismatch):** Search D_00c for `rep_bucket ==` filters. Verify Joe's rep_bucket value at D_00c entry. Cross-reference with the `706ea757e` advisor↔individual fix.

      Output: identified root cause + 1-line fix.
    </step>

    <step>
      Apply minimal fix. Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00c.*.py`. All three checks (py_compile + ds-precommit-check + ruff) must exit 0.
    </step>

    <step>
      Re-run INF_D_00c. Verify output:
      - leaderboard.json has 4 advisors (Patrick, Peter, IWM, **Joe**)
      - Joe row has non-zero AUA + non-zero client count
      - Cross-reference with Friday's empirical: Joe $16.2M / 21 clients (allow ±5% for any data-state drift since Friday)
    </step>

    <step>
      Upload to platinum prefix. Capture ETag.

      Trigger DT 0.4 CF invalidation on `/api/scoped/advisor-intelligence/platinum/firm/leaderboard.json` (single-file, low cost).
    </step>

    <step>
      Commit + push. RAVC2 to COO with: SHA, ETag, before/after row spot-check, hypothesis-confirmed (which of H1/H2/H3), and CF invalidation ID.
    </step>
  </scope>

  <acceptance_criteria>
    1. **Gate check** performed — ACCOUNT-ID-COERCE cascade complete + leaderboard.json inspected.
    2. IF Joe present post-cascade: TO closes as `complete (resolved-by-cascade)` with ETag captured. NO Step 2+ execution.
    3. IF Joe absent post-cascade: continue execution.
    4. **Root cause identified** (one of H1 / H2 / H3, or documented other).
    5. **Pre-commit gate** PASS on D_00c edit.
    6. **leaderboard.json regenerated** with all 4 advisors; Joe AUA &gt; $0, Joe client count &gt; 0.
    7. **Empirical match within ±5%** of Friday baseline (Joe $16.2M / 21 clients).
    8. **CF invalidation** ID captured.
    9. **RAVC2 delivered** with hypothesis-confirmed metadata.
    10. **Root-cause class surfaced** (CTO addition 2026-05-11): in RAVC2, explicitly classify the root cause as one of:
        - `filter` (e.g., snapshot-date or temporal filter dropping Joe)
        - `allowlist` (rep_id or rep_bucket hardcoded list missing 6/individual)
        - `publisher` (advisor-publisher Lambda fan-out doesn't reach Joe)
        - `other` (with brief description)

        Pattern note: this is the 2nd Joe-rep_id=6 attribution bug in 1 week (after INFNNA.001 INFLECTION_REP_IDS expansion). If a 3rd Joe-bug surfaces within 2 weeks, COO will trigger `ADVI_INFJOEAUDIT` repo-wide audit project. Root-cause class enables sweep-detection across other downstream consumers in that class.
  </acceptance_criteria>

  <blocking>
    **Blocked by:** ACCOUNT-ID-COERCE TO `5287179fb` completion. Cannot begin Step 1 gate-check until cascade re-run completes.
  </blocking>

  <notes>
    Andrew direct routing 2026-05-11: approved conditional-execution pattern. Conditional execution saves DS effort if cascade re-run self-heals the leaderboard.

    The 3 hypotheses are non-exclusive — possible to have two simultaneous defects. Document all observations even if first-found hypothesis closes the bug.

    Visibility: this is a portal-visible correctness bug. Andrew aware. CF invalidation is required-not-optional once fix lands.
  </notes>
</task_order>
