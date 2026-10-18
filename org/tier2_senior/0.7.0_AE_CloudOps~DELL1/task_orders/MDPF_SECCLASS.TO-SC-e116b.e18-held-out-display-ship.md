<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e116b.e18-held-out-display-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
    <date>2026-10-18</date>
    <status>staged</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>29</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R29.md</decomp_doc> (declares SC-e-116; the ship is the issuer act that follows the drain, by a CloudOps lane under its pair).
<owned_cells>SC-e-116</owned_cells>
</decomp_ref>

  <objective>
    Ship ONE named file to s3://opal-data-bd/code/gold/: E_18.detect_new_securities.py (served ETag f5c03ee69eaa1810159aefb6e2145bb4, VersionId ij219ZfHeFTL7H_e8evmlrOipp2QHz_c -> the repo md5 197eac28db037323fbb3f862867589ab). Repo = box/dell1 at or after ababf2c906.
    The change is a +8-line log display in E_18 (the real-ticker pairs skipped as "already resolved" are printed, marked held out); no count, branch or write changes. gold_dispatch.sh does NOT ship (served ETag 165933f6dd0068a649f9757d9b86f303 stays).
    Nothing from lib/, the shared module, a table, a watermark or any other key rides the act. The pair: request org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_E18_HELD_OUT_DISPLAY_SHIP_20261018.md; its COO half and CTO half must both read SIGNED. Read it first.
  </objective>

  <hold>
    THIS ORDER IS STAGED, NOT LIVE. Do NOT act on it, do not open its ledger and do not touch S3 until the issuer 2.0.0_SA_COO~M1 sends a GO that CITES THIS ORDER'S PATH. The GO is not given before: (1) both halves are SIGNED; (2) the chain of the day has stopped, no bd-gold-layer-runner instance
    is running and no gold/trigger-pending.json waits (read in the same shell as the act); (3) the next scheduled fire is more than 90 minutes away (the fires are the 04:00Z nightly and the 23:00Z fallback, Monday to Saturday).
  </hold>

  <steps>
    STEP 0 (reads, nothing written): the pair request; the served ETag of E_18 is still the base value above (another ship in between means the delta is not this cell: STOP and report); the md5 of the repo file equals 197eac28db037323fbb3f862867589ab;
    runner state and gold/trigger-pending.json; every live worktree's org/critical_paths/.open_deploys/ for an open ledger touching code/gold (CLAUDE.md NEVER-2); name any.

    LEG P (before the deploy): a census of every key under s3://opal-data-bd/code/gold/ with its ETag and VersionId (IsLatest only; page and key counts printed) to org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/E116_LEGP_20261018.json; and the table
    etf-classifications' state: the item count (paginated, client-side), the 13 seeded keys present, the 9 held-out absent, the first 200 keys of a sorted scan with their last_updated.

    LEG D (the deploy): open the ledger in org/critical_paths/change_management/ (name both the sentinel and the entry); then, outside a BD fire, `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/E_18.detect_new_securities.py`.
    After: python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R29_CHECKS/e116_shipped_check.py reads E116-SHIPPED ok=True; a pre/post census of every key under code/gold/ shows only E_18 moved (anything else moved is a STOP and a same-session restore by VersionId).

    LEG Q (the proof): the runner stopped first by `sudo systemctl stop gold-layer-runner` as the first SSM command, then `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --dry-run --single E_18` with the script pulled from S3, NO --upload (the plan form; CTO msg 7449), no inline code; if the boot chain goes past A_02 into a real fire, send no single and report.
    Read: exit 0; no ERROR line; the output shows the line `Held out by the resolution table` with its count and one line per pair; `Already resolved (in resolution table): 9` and `Scheduled-classification candidates: 0` as in the 2026-10-17 23:00Z fire; and etf-classifications unchanged (the item count, the 13 present, the 9 absent, the 200-key last_updated census unmoved).
    A failure: restore E_18 by the base VersionId (above) in the same session, re-run the check expecting the base md5 f5c03ee6, report.

    LEG G is the issuer's, on the first scheduled fire after the ship.
  </steps>

  <bounds>
    One code key, no gold_dispatch.sh, no lib/, no IAM, no table write, no other key. The 49F bucket is written only by the runner job itself, as in a fire. Finish before the next scheduled fire minus 90 minutes; if the legs cannot finish by then, stop and report.
    Report ONCE to 2.0.0_SA_COO~M1: Step 0 reads, the leg P counts and pages, the deploy census, the check line, the leg Q lines and times, the ledger path, and each commit with its measured push state (ls-remote read).
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/task_orders/MDPF_SECCLASS.TO-SC-e116b.e18-held-out-display-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; the hold keeps it outside every BD gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped E_18 on 2026-10-17 (TO-SC-e111b).
comp-adversary: RUN -- a named-ship set of one explicit path (a second member is a STOP with same-session restore); an empty success is excluded because the check requires the served md5 to equal the repo md5 AND the display line to be present AND the served dispatcher unchanged; a restore to a stale VersionId (the base value is in the objective). BLIND: the first scheduled fire after the ship (leg G, the issuer's).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

  <proof_of_spec>
    <criterion id="SC29-e116b-AC1" cell_refs="SC-e-116"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R29_CHECKS/e116_shipped_check.py</invocation><expect>E116-SHIPPED ok=True</expect></criterion>
    AC1 base: FAIL as expected at 2026-10-18 ~02:3xZ (`E116-SHIPPED ok=False e18=f5c03ee6|197eac28|DIFF display=0 compiles=True old_list_lines=0 dispatch=165933f6|165933f6|MATCH`).
  </proof_of_spec>
</task_order>
