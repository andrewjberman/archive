<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e111b.e18-repoint-ship-recut</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
    <date>2026-10-17</date>
    <status>staged</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>28</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R28.md</decomp_doc> (item 3 of the round: the E_18 repoint ship, the re-cut of TO-SC-e108b; the cell it ships, SC-e-108, drained in round 27 @d812b466fd).
<owned_cells>SC-e-108</owned_cells>
</decomp_ref>

  <objective>
    RE-CUT 2026-10-17 of TO-SC-e108b (superseded @178b4c02ed, never shipped, withdrawn from round 27 on 1.0.0_SA_CTO~DELL1 msg 7422 and re-homed to round 28, msg 7425). The order, its steps and its bounds are the e108b ones; only the hold and the round differ. The signed pair halves cite e108b by its earlier paths; the bytes they price are unchanged (measured 2026-10-17: the repo md5 of both files equals the built values, the served ETags of both keys are still the base values).
    Ship TWO named files to s3://opal-data-bd/code/gold/: E_18.detect_new_securities.py (served ETag a7820a205692444dadb59e526200bff6, VersionId wb5QYkh7QEfrvMEscg.EgAui0MeBaNwB -> the repo md5 f5c03ee69eaa1810159aefb6e2145bb4)
    and gold_dispatch.sh (served ETag 882a910b27d1a855c5d31547eb44f3a1, VersionId .bNYVetB5sGV8bZki7EgXBfChCH_uPyE -> the repo md5 165933f6dd0068a649f9757d9b86f303). Repo = box/dell1 at or after d812b466fd. Then prove it (one E_18 dry run on the runner).
    Nothing from lib/, the shared module, a table, a watermark or any other key rides the act. The pair: request org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_E18_REPOINT_SHIP_20261016.md
    (sha256 527a2fbc29d19abd0262054546bc86eed7ba26881b142b865cf9a7a61e763b0f); CTO half SIGNED (org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_E18_REPOINT_SHIP_20261016.md @d245ef138e); COO half SIGNED
    (org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_COO_HALF_SECCLASS_E18_REPOINT_SHIP_20261016.md). Read all three first.
  </objective>

  <hold>
    THIS ORDER IS STAGED, NOT LIVE. Do NOT act on it, do not open its ledger and do not touch S3 until the issuer 2.0.0_SA_COO~M1 sends a GO that CITES THIS ORDER'S PATH. The GO is not given before:
    (1) both halves are SIGNED (they are) and 1.0.0_SA_CTO~DELL1 has said they stand for this re-cut; (2) the seed order TO-SC-e107b is done and read (E107-SEEDED ok=True) and leg G of the seed is read (rows MDPF_SECCLASS-D1-S50, MET on the canonical object); the S48 hazard is disarmed (row D1-S51); (3) the chain of the day has stopped, no bd-gold-layer-runner instance
    is running and no gold/trigger-pending.json waits (read in the same shell as the act).
  </hold>

  <steps>
    STEP 0 (reads, nothing written): the three documents above; the served ETags of both files are still the base values (another ship in between means the delta is not this cell: STOP and report); the md5 of both repo files equals the two built values;
    runner state and gold/trigger-pending.json; every live worktree's org/critical_paths/.open_deploys/ for an open ledger touching code/gold (CLAUDE.md NEVER-2); name any.

    LEG P (before the deploy): a census of every key under s3://opal-data-bd/code/gold/ with its ETag and VersionId (IsLatest only; page and key counts printed) to org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/E111_LEGP_20261017.json; and the table
    etf-classifications' state: the 13 seeded keys present, the 9 held-out absent, the first 200 keys of a sorted scan with their last_updated.

    LEG D (the deploy): open the ledger in org/critical_paths/change_management/ (name both the sentinel and the entry); then, outside a BD fire, `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/E_18.detect_new_securities.py` and
    `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/gold_dispatch.sh`. After: python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R27_CHECKS/e108_shipped_check.py reads E108-SHIPPED ok=True;
    a pre/post census of every key under code/gold/ shows only these two moved (anything else moved is a STOP and a same-session restore by VersionId).

    LEG Q (the proof, Branch 1): the runner procedure of TO-SC-e97b amendments 2 to 4 applies unchanged: the runner service stopped first by `sudo systemctl stop gold-layer-runner` as the first SSM command, then
    `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single E_18` with the script pulled from S3 and NO --upload (E_18 has no --dry-run; the dispatcher strips --upload for it), no inline code; if the boot chain goes past A_02 into a real fire, send no single and report.
    Read: exit 0; no ERROR line; the nine held-out tickers (BALCX, CIMAX, DODBX, FSNQX, HBLFX, JBAWX, KAMIX, PCEF, TRRNX) reported unresolved; and etf-classifications unchanged (the 13 present, the 9 absent, the 200-key last_updated census unmoved).
    A failure: restore both files by VersionId (the base values above) in the same session, re-run the check expecting the base, report.

    LEG G is the issuer's, on the first scheduled fire after the ship.
  </steps>

  <bounds>
    Two code keys, no lib/, no IAM, no table write, no other key. The 49F bucket is written only by the runner job itself, as in a fire. Finish before the next scheduled fire minus 90 minutes (the fires are the 04:00Z nightly and the 23:00Z fallback Monday to Saturday);
    if the legs cannot finish by then, stop and report. Report ONCE to 2.0.0_SA_COO~M1: Step 0 reads, the leg P counts and pages, the deploy census, the check line, the leg Q lines and times, the ledger path, and each commit with its measured push state (ls-remote read).
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/task_orders/MDPF_SECCLASS.TO-SC-e111b.e18-repoint-ship-recut.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; the hold keeps it outside every BD gold run and after the seed's read.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped C_06 (e102b) and the BD gold code before.
comp-adversary: RUN -- the named-ship set (two explicit paths, no lib/ or _shared member); a third member is a STOP with same-session restore; an empty success is excluded because the check requires the served ETag to equal the repo md5 AND the old-list lines to read 0; a restore to a stale VersionId (the base values are in the objective); two served causes in one fire (the hold). BLIND: the first scheduled fire after the ship (leg G, the issuer's), the readers outside the BD chain (named in the request).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

  <proof_of_spec>
    <criterion id="SC28-e111b-AC1" cell_refs="SC-e-108"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R27_CHECKS/e108_shipped_check.py</invocation><expect>E108-SHIPPED ok=True</expect></criterion>
    AC1 base: FAIL as expected at 2026-10-17 ~08:3xZ (the same line) (`E108-SHIPPED ok=False e18=a7820a20|f5c03ee6|DIFF dispatch=882a910b|165933f6|DIFF e18_old_list_lines=17 dispatch_syntax=0 chain=False`).
  </proof_of_spec>
</task_order>
