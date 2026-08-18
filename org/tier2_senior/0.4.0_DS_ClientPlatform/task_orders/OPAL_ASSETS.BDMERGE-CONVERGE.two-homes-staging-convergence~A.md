# TO OPAL_ASSETS.BDMERGE-CONVERGE — bd merge-daily-incremental two-homes CONVERGENCE: refresh the stale legacy staging copy to HEAD (CTO R-2)

<task_order id="OPAL_ASSETS.BDMERGE-CONVERGE" project="OPAL_ASSETS">
<issued_to>0.4.0_DS_ClientPlatform~A (DS lane per Rule 13; DS base double-booked through 08-21 — CTO routed to ~A)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T17:10Z</issued>
<dated>2026-08-21 — after your P3-close (08-20). NOT sooner by design: no bd-silver staging change near the 08-18 fixture or the first unattended P2 cycles.</dated>
<status>staged -- GO paired; nothing before 08-21</status>
<priority>P2 — a scheduled daily client-data producer runs 4 commits behind its own correctness guards; the convergence ends it without adjudicating the two-homes architecture</priority>
<authority>CTO ruling set @CTO_GATE_AND_RULING_SET_20260818_1700Z.md R-2 (adopting COO's rec exactly): near-term CONVERGENCE refresh; the legacy-EC2-leg retirement question stays foldered at P5-TEARDOWN. Finding: 0.8.0 DEPLOYCENSUS 160830Z (all reads live).</authority>
</task_order>

## Objective
Converge the two staging homes of ONE logical producer: refresh
`s3://opal-data-bd/scripts/merge-daily-incremental.py` (legacy EC2 path — pulled daily by the
21:53Z/22:00Z SSM docs) to repo HEAD `data/black_diamond/scripts/silver/merge-daily-incremental.py`,
making it byte-identical to the CURRENT home (`s3://opal-data-bd/code/silver/…`). This is a
CONVERGENCE (same bytes, both homes), not a new path and not an adjudication of which home is right —
that question rides P5.

## Compiler tools (three-phase)
Phase 1: `comp-pipescript io merge-daily-incremental --pipeline bd` (if registered; else say so) +
read the two SSM docs' pull lines (get-document) so the refresh hits the key they actually pull.
Phase 2: commit-gate on any repo touch (expect none — this is a staging upload of committed HEAD).
Phase 3: the criteria below.

## Cross-domain coordination
- shared_resource: bd silver outputs — DS base's bd platinum chain consumes them; MCP DS base before
  the upload (their T-B/INF windows are 08-19/20; 08-21 avoids both, confirm nothing moved).
- shared_resource: the fees leg — convert_fees_to_silver.py rides the same legacy path 1 commit
  behind but a DIFFERENT doc runs it; NOT in this TO's scope (state it, do not touch it).

## Acceptance criteria
- BM-1 CONVERGED: post-upload, sha256(scripts/ copy) == sha256(code/silver/ copy) == sha256(repo HEAD
  file), all three printed (safe-deploy lane discipline for the cp; upload-verify by hash re-read,
  never rc).
- BM-2 EXERCISED: the NEXT scheduled run (21:53Z/22:00Z 08-21) green ON THE NEW BYTES — the run's own
  log shows the stub-reject guard present/active (its log line or a grep of the pulled file on-box via
  SSM read-only), not merely rc=0.
- BM-3 ROLLBACK STATED: the pre-refresh staged bytes kept locally with sha256 (same-window revert).
- BM-4 proof instance VALID rc=0 positional: ids BM-1,BM-2,BM-3,BM-4.

<proof_of_spec>
  <expected_criteria>BM-1,BM-2,BM-3,BM-4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OPAL_ASSETS.BDMERGE-CONVERGE_PROOF_OF_SPEC~A.json</instance_path>
</proof_of_spec>

## Do not
- Do not touch the SSM docs, the EventBridge crons, or the Lambda home — bytes converge, mechanisms
  stand (retirement is P5's question). Do not touch the fees leg. Nothing before 08-21.

## Reporting
COO (cc CTO, DS base, 0.8.0, MSTR) at converged + at the exercised run. Surprise channel: one banked
line to COO. Session log with Compiler Tools section = deliverable.
