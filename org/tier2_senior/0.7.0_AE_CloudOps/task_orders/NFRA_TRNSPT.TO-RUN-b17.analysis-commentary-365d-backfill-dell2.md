<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-RUN-b17.analysis-commentary-365d-backfill-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R17.md</decomp_doc>
<owned_cells>TR-b-17</owned_cells>
<decomp_context>Round 17 (CTO msg 2293, analysis ADDENDUM 4, E3): "the 365-day backfill on CloudOps~DELL2 under the pair (simulate first, VersionIds first, counts only)". Laptop stand-down CONFIRMED, neither run started, the laptop will not run either (0.0.0_AB_MSTR~DELL2 msg 2319).</decomp_context>
</decomp_ref>

  <closure>
    COMPLETE (issuer, 2026-10-09 ~08:1xZ). Applier @beef69ea0d: listed 453, landed 24 on 6 dates, skipped_known 8, list_refusals 0; silver 6
    rows held_out 6; gold 0 rows; pull_runs 18 -> 19; proof VALID @e77cef2f5. Issuer read R18_READBACK_B17_BACKFILL.json @ff31f846ed agrees.
    Row D2-S9 (empty precedent) ruled empty by the CTO (ADDENDUM 5 @d4a3b1dbb4). No rollback.
  </closure>

  <objective>
    ONE bounded 365-day backfill of the analysis-commentary mail pull, under its GIVEN never-widen pair, from box/dell2 @f7a378fcb1 under this
    seat's identity. Return counts only to 2.0.0_SA_COO~T2.
  </objective>

  <context>
    The pair: COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_365D_BACKFILL_20261009.md`
    @1bb934be65 (executor amended to this seat); CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_NFRA_TRNSPT_CTO_HALF_365D_BACKFILL_20261009.md`
    with AMENDMENT 1 (msg 2232). Read both before the run; they bind. The prior VersionIds of every existing silver key are committed
    (`org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R16_BACKFILL_PRIOR_VERSIONS.json` @d035a3a8a6: 5 silver keys, 0 gold).
    Issuer baseline 02:52Z: bronze 20 keys / 5 dates, silver 5 / 5 (2026-07-06..2026-10-01), gold 0. dell2's agent user is Decrypt-only on the
    transcripts key, so condition 6 (simulate) comes first; a key-policy grant is the laptop's act (relayed by MSTR, msg 2319).
  </context>

  <the_act>
    1. CONDITION 6: simulate `kms:GenerateDataKey` and `kms:Encrypt` on the transcripts key, and `s3:PutObject` on
       `outlook/transcripts/bronze/analysis_commentary/`, `.../silver/analysis_commentary/`, `.../gold/analysis_commentary/` and
       `outlook/transcripts/state/pull_runs/`. Any refusal is a STOP: send it to 0.0.0_AB_MSTR~DELL2, report to the issuer, write nothing.
    2. Re-list the silver prefix; its keys and current VersionIds must equal the committed prior list. A difference is a STOP.
    3. CONDITION 2: `python -m pytest data/transcripts/scripts/tests/test_wipe_planted.py -q` at f7a378fcb1 passes.
    4. `python data/transcripts/scripts/outlook/pull.py --gateway --days 365 --apply` -- once.
    5. For each bronze date that run newly landed: `silver.build(<date>, apply=True)`, then `gold.build(<date>, apply=True)`.
    6. Counts only: listed, admitted, landed, skipped_known, list_refusals, silver rows, held_out, gold rows; the list of newly landed dates.
    ROLLBACK, if the issuer asks: copy each prior silver VersionId back over its key; a NEW key's delete is Andrew's act, never this seat's.
  </the_act>

  <bounds>
    - 365 days exactly, ONE run. No change to the Lambda, its schedule, the sender table, the criterion or the wipe. No vendor call.
    - No content in any file or message. No push of a shared branch. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: RUN -- the scheduled producer outlook-global-transcripts-pull-lambda (cron(30 23 * * ? *), WINDOW_DAYS=7, refuses over 120) is NOT changed; the 365-day window is the manual path's new reachable state, named in both halves.
comp-iam: RUN -- 1 key policy read (main.tf DellAgentUsersDecryptOnly); encrypt simulated at step 1; a refusal stops the run.
comp-adversary: RUN -- a second run (ONE run, laptop stood down per msg 2319); a lost prior (VersionIds committed and re-checked at step 2); a wipe regression (test_wipe_planted at the pin); content leaking (counts only); a mid-run KMS refusal (simulated first); BLIND: the gateway's listing beyond 120 days, measured by the run's own list_refusals count.
lane: the seat's own deliverables and logs; the run writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-b-17"><invocation>aws s3api list-objects-v2 --bucket opal-data-transcripts --prefix outlook/transcripts/state/pull_runs/ --query "length(Contents)"</invocation><expect>19</expect></criterion>
</proof_of_spec>
  AC1: 18 run records before (issuer read 02:52Z); exactly one new record from this run.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the simulate result; the step-2 equality; the wipe test line; the six counts; the newly landed dates; the
    new run id; the time in UTC; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
