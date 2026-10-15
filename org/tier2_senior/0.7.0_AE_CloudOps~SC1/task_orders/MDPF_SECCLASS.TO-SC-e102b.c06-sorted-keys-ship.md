<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e102b.c06-sorted-keys-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-14</date>
    <status>complete</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>25</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R25.md</decomp_doc> (declares SC-e-102; the ship is the issuer act that follows the drain, by a CloudOps lane under its pair).
<owned_cells>SC-e-102</owned_cells>
</decomp_ref>

  <objective>
    Ship ONE named file: s3://opal-data-bd/code/gold/C_06.client_mix_timeseries.py, served ETag f847d8d105025ffbee94b1aa5092faf6 (VersionId jGO15I3AZTATLbGxE3_36dKm86wuggDK) -> the repo md5
    f884f28ddcaeda891dc67958210e88ad (box/dell1 at or after b5f6b816a4; the whole delta is one line: sort_keys=True in _write_mix_summary). Then prove it (leg Q', two C_06 singles on unchanged
    inputs). Nothing from lib/, D_03, D_04, a table, a watermark or any other data key rides the act. The pair: request
    org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_C06_SORTED_KEYS_20261014.md; CTO half SIGNED @29827be5eb
    (org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_C06_SORTED_KEYS_20261014.md, conditions C1 and C2); COO half in the sibling file, signed after the re-base read. Read all three first.
  </objective>

  <hold>
    THIS ORDER IS STAGED, NOT LIVE. Do NOT act on it, do not open its ledger and do not touch S3 until the issuer 2.0.0_SA_COO~M1 sends a GO that CITES THIS ORDER'S PATH. The GO is not given before:
    (1) the COO half is SIGNED; (2) tonight's 23:00Z scheduled fire (2026-10-14) has stopped and the issuer has read it with r25_rebase_read.py (so two served causes never share a fire, CTO condition C1);
    (3) the dell1 restart at 21:00Z has happened (CTO condition C2); (4) no bd-gold-layer-runner instance is running and no gold/trigger-pending.json waits (read in the same shell as the act).
  </hold>

  <steps>
    STEP 0 (reads, nothing written): the three documents above; the served C_06 ETag is still f847d8d1 (another ship in between means the delta is not this cell: STOP and report); runner state and
    gold/trigger-pending.json; head-object of one canonical key (advi/49financial/platinum/firm/mix_summary.json in opal-data-49financial) to prove this seat can READ the 49F bucket. Read every live worktree's
    org/critical_paths/.open_deploys/ (git worktree list --porcelain, then ls-tree) for a ledger opened before the 21:00Z restart and not closed (CLAUDE.md NEVER-2); name any that touches C_06 or the mix families.

    LEG P (before the deploy): the current VersionIds, IsLatest only, pages and key counts printed, to org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E102_LEGP_20261014.json, of: the mix daily summary
    (canonical bucket opal-data-49financial, key from lib/platinum_dest.py source()); firm_mix_views_daily.json and its legacy alias; every advisor mix_daily.json (56) and each legacy alias; platinum/firm/mix_summary.json.
    Derive every key with lib/platinum_dest.py source() and list_target(); type none. Also save the live body of the mix daily summary beside it.

    LEG D (the deploy): open the ledger in org/critical_paths/change_management/ (name both the sentinel and the entry); then, outside a BD fire, `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py`.
    After: the served ETag equals f884f28ddcaeda891dc67958210e88ad; a pre/post census of every key under code/gold/ shows only C_06 moved (anything else moved is a STOP and a same-session restore by VersionId).

    LEG Q' (the proof, Branch 1 of the request; the runner procedure of TO-SC-e97b amendments 2 to 4 applies unchanged: runner stopped first by `sudo systemctl stop gold-layer-runner` as the first SSM command, then
    `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single C_06` with the script pulled from S3, no inline code; if the boot chain goes past A_02 into C_06 it is itself a fire: send no single and report).
    (a) Read the mix daily summary's VersionId IMMEDIATELY before run 1 (CTO condition C1: that is the restore target, never an older one) and save its body.
    (b) Run 1, C_06 alone, outside any scheduled fire window. Read: the mix daily summary parses EQUAL to the saved body (canonical-JSON equality, XA-20261014T113939Z-a304); its body md5 equals the md5 of
        json.dumps(json.loads(body), sort_keys=True, separators=(',', ':')); the C06-ROLLING-REDERIVE line reads relationships_rewritten=0 keys_written=0; the other C_06-written keys keep their ETags
        (same key set, every ETag equal; a new VersionId with an equal ETag is reported, not a delta).
    (c) Run 2, C_06 alone: the mix daily summary's ETag equals run 1's (byte determinism).
    (d) Any parsed-content difference in (b), or any other key's ETag differing: restore the mix daily summary to the VersionId of (a) in the same session, stop, report; the code stays deployed only if the issuer says so.
        A failure of the sorted-bytes or determinism read with equal content is a REPORT, not a harm: say so and wait.

    LEG G is the issuer's, on the first scheduled fire after the ship (D_03 families and D_04's object, per the request's Branch 2).
  </steps>

  <bounds>
    No other code key, no lib/, no IAM, no table. The 49F bucket is written only by the runner job itself, as in a fire. Finish before the next scheduled fire minus 90 minutes (the fires are the 04:00Z nightly and the 23:00Z
    fallback Monday to Saturday); if the legs cannot finish by then, stop and report. Report ONCE to 2.0.0_SA_COO~M1: Step 0 reads, leg P counts and pages, the deploy census, the run-1 and run-2 lines and times,
    the key counts, the ledger path, and each commit with its measured push state (ls-remote read).
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e102b.c06-sorted-keys-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; the hold keeps it outside every BD gold run and after the 23:00Z fire's read.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped C_06 to this key (e91b, e97b).
comp-adversary: RUN -- the named-ship set (one explicit path, no _shared or lib member); a second member is a STOP with same-session restore; an empty success is excluded because AC1 requires the served ETag to equal the repo md5 AND differ from the rollback ETag; a restore to a stale VersionId (CTO C1: the VersionId read immediately before run 1); two served causes in one fire (the hold). BLIND: D_03 and D_04's first fire after the ship (leg G, the issuer's).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

  <proof_of_spec>
    <criterion id="SC25-e102b-AC1" cell_refs="SC-e-102"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R25_CHECKS/e102_shipped_check.py</invocation><expect>E102-SHIPPED ok=True</expect></criterion>
    AC1 base: FAIL as expected at 2026-10-14 ~13:0xZ (`E102-SHIPPED ok=False c06=f847d8d1|f884f28d|DIFF control=MATCH dispatch=same d03=same d04=same mds_sorted=False`). After leg Q' it also prints mds_sorted=True.
  </proof_of_spec>
</task_order>
