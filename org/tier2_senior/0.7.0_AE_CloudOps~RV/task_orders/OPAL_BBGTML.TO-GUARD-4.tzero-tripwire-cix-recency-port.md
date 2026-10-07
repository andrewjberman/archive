<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-GUARD-4.tzero-tripwire-cix-recency-port</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~RV</issued_to>
    <date>2026-10-07</date>
    <status>pending -- issued 2026-10-07 ~10:1xZ on CTO fix-route ADDENDUM 7 @58e472b0b6 (msg 30773), row OPAL_BBGTML-Z-S12</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: outside the canonical pipeline -- a seat act on a closed project (OPAL_BBGTML) on 1.0.0_SA_CTO~Z's fix route, ADDENDUM 7 @58e472b0b6; ONE cell (GUARD-4); the order is the LD-0529 carrier, not a round; it BUILDS ON A BRANCH and merges nothing

  <objective>
    Close the hand-run half of gap 2 that row OPAL_BBGTML-Z-S12 (your row, @c405c95512) found: publish_to_portal.py runs the
    TZERO copy of the tripwire, and that copy lacks the per-series custom CIX recency check GUARD-3b put in the tplus1 copy.
    The CTO ruled the smallest route: port the same limb into the tzero copy, and nothing else.
  </objective>

  <context>
    THE SPEC is ADDENDUM 7 of org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_INDEX_BENCHMARK_FIX_ROUTE_20261006.md
    (@58e472b0b6). Read it in full first; where this order and the addendum differ, the addendum wins.
    THIS ORDER BUILDS AND PROVES ON A BRANCH. IT DOES NOT MERGE. The tzero copy is a third file under integrations/bloomberg/,
    and Andrew's lift of his no-modify order covers the two GUARD-3 edits only. The merge is the deploy and it waits on
    Andrew's word, which the CTO has put to him. A branch in a linked worktree does not touch the shared working tree, so
    building it is not a deploy.
    No Bloomberg call, no Terminal sign-in, no pull, no publish: the proof reads objects that already exist.
  </context>

  <the_act>
    Work in your OWN linked worktree cut from the shared tree's HEAD (it must carry the merged GUARD-3b bytes, merge
    80bcd69f78). Edit nothing in the shared tree.

    CELL GUARD-4 -- integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py.
    1. Port the per-series custom CIX recency limb as GUARD-3b landed it in
       integrations/bloomberg/pipeline/tplus1/tools/bbg_pkl_tripwire.py: the same function body, the same recognition rule
       read from the PKL (never a typed list of names), the same printed denominator, the same FAIL through the copy's
       existing fail path. Where the tzero copy's surrounding code differs (its as-of, its fail helper), wire the limb to
       the tzero copy's OWN as-of and fail path and say in your report exactly which lines differ from the tplus1 limb and why.
    2. Nothing else in the file changes. The two copies stay two files.
    3. Before editing, read how the tzero copy resolves its as-of date. If it is not the same date the tplus1 copy grades
       against, STOP the edit, file a row, and report: a recency check graded against a different as-of is a different check.

    THE PROOF (a script under your deliverables folder; it imports the edited tzero module from your worktree and writes
    nothing to S3), on the same two real pulls your GUARD-3b proof used:
    - the 2026-10-06 12:29Z pull (s3://opal-data-portal-v2/benchmarks/data_20261005_v1.pkl, VersionId
      fPWS_TCLSvx2dW9SZGDl3hcQL735m5XJ): FAIL, naming the 7 series at 2026-09-29, with the denominator printed;
    - the 2026-10-07 01:26Z re-pull (you located it at benchmarks/data_20261007_v1.pkl): PASS;
    - SPX (not a custom series): unaffected on both;
    - THE NEGATIVE CONTROL: the same two reads against the tzero copy AT ITS PARENT COMMIT read PASS on the frozen pull.
      That is the difference the port makes; a proof without it shows only that the new code runs.

    THE LANDING IS NOT IN THIS ORDER.
    1. Commit the one edit and the proof on your branch (one commit for the cell, one for the proof and report).
    2. Do NOT merge, do NOT run safe-merge, do NOT open a NEVER-2 entry: no deploy is being made.
    3. Leave the worktree and the branch in place and name both in your report.
  </the_act>

  <bounds>
    - Exactly ONE file under integrations/bloomberg/ is edited, on the branch: the tzero tripwire. Not publish_to_portal.py,
      not the tplus1 copy, not the battery, not either README or docstring claim about which copy is production.
    - NO merge into the shared tree. NO Bloomberg call, sign-in, pull, publish, S3 write or schedule change.
    - Until this lands, ADDENDUM 7 binds by reading: nobody hand-runs publish_to_portal.py without first running the tplus1
      tripwire on the same files and reading its exit code.
    - A surprise is a row in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (id OPAL_BBGTML-Z-S<k>, disarm_owner
      2.0.0_SA_COO~Z); keep working.
  </bounds>

  <paths>
    integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py
    org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~RV/logs/
    org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="GUARD-4"><invocation>python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard4_tzero_tripwire_proof.py; echo "exit=$?"</invocation><expect>run from the worktree: the 2026-10-06 12:29Z pull reads FAIL naming 7 series at 2026-09-29 with the denominator of custom CIX series printed; the 2026-10-07 01:26Z re-pull reads PASS; SPX PASS on each; the parent-commit copy reads PASS on the frozen pull (the negative control); a last line GUARD-4: PASS; and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="GUARD-4"><invocation>git diff --stat HEAD~2 HEAD -- integrations/bloomberg/ | tail -1</invocation><expect>run on the branch after the two commits: exactly 1 file changed under integrations/bloomberg/, the tzero tripwire</expect></criterion>
</proof_of_spec>

  <report>
    Report to 2.0.0_SA_COO~Z ONCE, as a deliverable file: each criterion's output, the branch name and its two commits, the
    worktree path, the lines where the tzero limb differs from the tplus1 limb and why, how the tzero copy resolves its as-of,
    and the sentence "NOT MERGED". Leave the status flip to the issuer. Your TO-GUARD-3 report 2 (the 11:00Z and 11:30Z live
    reads) is unchanged by this order and comes first if the two collide in time.
  </report>
</task_order>
