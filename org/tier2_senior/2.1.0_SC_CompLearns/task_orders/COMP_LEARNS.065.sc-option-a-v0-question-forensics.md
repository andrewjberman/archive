<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-065-sc-option-a-v0-question-forensics</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — concurrent with .064; informs iter-7 strategy (CTO Option A diagnostic)</priority>
  </metadata>

  <references>
    <ref type="cto_ruling">MCP from 1.1.0_SA_CTO, subject: CLICK CLASSIFICATION RULING — 20260427T124801Z (§3 Option A spec)</ref>
    <ref type="champion">comp/targets/dev-click-001/champion.json — sha 7beb09b, pm=0.1180, baseline_commit=f80cf4b0</ref>
    <ref type="h3_baseline">comp/results/dev-click-001/h3_baseline/h3_v2_result.json — 8/11 (72.7%); improvable: q02, q03, q11</ref>
    <ref type="cache">comp/bench/cache.py — scorecard cache lookup mechanism</ref>
  </references>

  <objective>
    Read-only diagnostic. No new scoring run. Identify which specific question(s) the v0 champion random_unique_win
    scored that the full-source baseline misses.

    ## Context

    v0 champion (sha 7beb09b) has ab_lift=0.0909 (1/11). The champion achieved this by random_unique_win on 1
    question that the baseline missed. H3-v2 baseline (8/11) already captures the 8 stable-correct questions.
    The 3 improvable questions are: q02, q03, q11.

    iter-6 (Option D) targets q03 specifically (class hierarchy disambiguation). The CTO needs to know whether
    the v0 champion's random win was q03 — which would mean dispatch_class body nodes partially address class
    hierarchy — or q02/q11, which would shift iter-7 toward numerical fact nodes.

    ## Diagnostic steps

    1. Read `comp/targets/dev-click-001/champion.json` to confirm sha 7beb09b and baseline_commit f80cf4b0.

    2. Locate the v0 champion scorecard. Two lookup paths:
       a. `comp/targets/click/scorecards/7beb09b_*.json` — glob for this sha prefix
       b. If not in scorecards dir, load via `comp/bench/cache.py` using sha 7beb09b and
          baseline_commit f80cf4b0

    3. From the scorecard, read the per-question results. Identify which question(s) the champion got CORRECT
       that the H3-v2 baseline (8/11) missed.

       The H3-v2 baseline correct questions are in `comp/results/dev-click-001/h3_baseline/h3_v2_result.json`.
       Compare champion per-question results against the baseline per-question results.

       Which of q02, q03, q11 did the champion get correct that the baseline missed?

    4. For that question, read the judge's response to assess reproducibility:
       - Is this a genuine knowledge gain (the compiler context caused the judge to reason correctly)?
       - Or is this a random hit (the judge's response is ambiguous, unstable, or format-matched by luck)?

    5. Report to CTO (1.1.0_SA_CTO) directly via MCP with:
       - Which QID the v0 champion won (answer: one of q02, q03, q11 — or none if the win was
         from a question already in the baseline-correct set)
       - The judge response text for that question (brief excerpt)
       - Reproducibility assessment: genuine / probable-luck / ambiguous
       - Brief note: does this suggest dispatch_class body nodes address q03 (class hierarchy), or
         a different surface?

    MCP CTO directly per CTO ruling. CC COO (2.1.0_SA_COO) with same content.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before diagnostic">
      <step>
        <run>ls comp/targets/click/scorecards/ | grep "7beb09b"</run>
        <expect>One file: 7beb09b_*.json present. If absent, use cache.py lookup.</expect>
        <if_mismatch>Try: python -c "from comp.bench.cache import ScorecardCache; c=ScorecardCache(); print(c.lookup('7beb09b', 'd869779f'))" from feature_clb root. MCP COO if cache miss.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after diagnostic (no commit required — read-only)">
      <step>
        <run>N/A — read-only diagnostic. No code changes. No commit required.</run>
        <expect>MCP to CTO and COO with findings.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Read-only diagnostic. No shared artifact writes. Concurrent with .064 (no sequencing constraint).</note>
    <shared_artifacts>None — reads only.</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Champion scorecard located (file or cache lookup).
    2. Per-question comparison performed: H3-v2 baseline vs champion correct sets.
    3. QID of the v0 random_unique_win identified (or confirmed none of q02/q03/q11 if the win was elsewhere).
    4. Reproducibility assessed from judge response text.
    5. MCP to 1.1.0_SA_CTO with findings (QID + judge response excerpt + reproducibility call).
    6. CC MCP to 2.1.0_SA_COO with same content.
    7. Session log with Compiler Tools section.
    8. No new scoring run. No code changes. No commits unless SC finds a caching discrepancy requiring a fix.
  </acceptance_criteria>

  <dependencies>
    - No upstream gate. Concurrent with .064.
    - .064 must complete before SC runs the iter-6 scoring (separate future TO); this .065 is diagnostic only.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - Read-only session. No commits expected unless a cache discrepancy requires a patch.
    - No emojis.
    - Report directly to CTO + CC COO per CTO spec.
  </operational_notes>

  <closeout>
    - flip TO status to complete
    - MCP 1.1.0_SA_CTO with findings (QID + judge response excerpt + reproducibility call)
    - CC MCP 2.1.0_SA_COO
    - session log
  </closeout>
</task_order>
