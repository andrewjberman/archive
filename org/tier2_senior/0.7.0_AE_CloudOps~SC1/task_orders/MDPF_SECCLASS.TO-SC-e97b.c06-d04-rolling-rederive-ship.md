<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e97b.c06-d04-rolling-rederive-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>23</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R23.md</decomp_doc> (declares SC-e-97; the ship is the issuer act that follows the drain, by a CloudOps lane under its pair).
<owned_cells>SC-e-97</owned_cells>
</decomp_ref>

  <objective>
    Ship TWO named files, together, in one act: s3://opal-data-bd/code/gold/C_06.client_mix_timeseries.py (ETag 2e35d043163cc18b135d7698cf11dc56 -> md5 f847d8d105025ffbee94b1aa5092faf6) and s3://opal-data-bd/code/gold/D_04.client_portal_summary.py (ETag 9d083669159ee8875b6489dea4fb2e37 -> md5 43a5d613ca9292329278573038f14158). No other key moves: not D_03, not the lib, not gold_dispatch.sh (the rule's runtime source, ETag f568d11bbf074aaec8f06a01ee13dd2e must read the same after), not any data key by this act.
  </objective>

  <hold>
    THIS ORDER IS STAGED, NOT LIVE. Do NOT act on it, do not open its ledger and do not touch S3 until the issuer 2.0.0_SA_COO~M1 sends a GO that CITES THIS ORDER'S PATH. The GO is not given before: (1) the ledger secclass-e91-c06-retained-unclassified-sc1-20261012 is CLOSED (the issuer's two reads of SC-e-91's first fires, so two causes never share one fire); (2) both halves are signed on the radius at or after 2e8d5c96ef (COO half addendum 1; CTO half addendum 2, msg 4367); (3) the issuer has read the bars and the advisor table into leg P's file. You MAY, before the GO, read the halves, re-read step 0 on the live keys without writing anything, prepare the leg-P enumerator and pick the window; reporting a step-0 read before the GO is welcome.
  </hold>

  <context>
    Why this seat: 1.0.0_SA_CTO~DELL1 msg 1445 ruled that a CloudOps seat applies each SECCLASS deploy under the halves' conditions. Read both halves in full first and carry every condition:
    - The request (the radius: per-date firm total and AUA, added and dropped relationships, advisors, bars): org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_C06_ROLLING_REDERIVE_20261012.md, with the committed tables in org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R23_RADIUS/
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_COO_HALF_SECCLASS_C06_ROLLING_REDERIVE_20261012.md (conditions 1-8 and addendum 1 conditions 9-12)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_C06_ROLLING_REDERIVE_20261012.md (its conditions and addendum 2: post-act every date's served total equals the AUA within rounding, else STOP and rollback)
    The repo bytes at the cut are the drained code, box/dell1 at or after 2e8d5c96ef: C_06 md5 f847d8d105025ffbee94b1aa5092faf6 and D_04 md5 43a5d613ca9292329278573038f14158. Work from a checkout at or after that commit.
    What the act does: C_06 re-derives, on every fire, the 15 window dates 2026-09-25..2026-10-09 (B_00's own --force-recent-days 14 window, read from the sibling gold_dispatch.sh) and writes restated_through; D_04 passes it through into platinum/firm/mix_summary.json. Expected effect on the NEXT fire: 3,274 of 3,793 relationship JSONs rewritten (13,096 keys, about 8.9 GB), the firm total moves on 14 of 15 window dates (the request's table), the AUA does not move, no advisor key is dropped.
    THE WINDOW: fires are bd-gold-trigger launches (04:00Z nightly, 23:00Z fallback Monday to Saturday, and event-driven launches). Leg P must read the data keys' VersionIds AFTER the last fire and BEFORE the next one; read the runner state in the SAME shell as the deploy. Other firms' launches of the same runner (for example advi-49f-gold-dispatch) count as fires for this purpose only if C_06 ran; read the runner's C_06 telemetry, do not assume.
    The leg-G read is the issuer's (COO half conditions 6 and 9-10, CTO conditions): per-date totals equal the AUA, the bars' totals and classes, the advisor table, restated_through, the second fire's idempotence (0 relationship keys rewritten).
  </context>

  <the_act>
    0. After the GO, on box/dell1 at or after 2e8d5c96ef, read the halves. Measure the pre-act state: head-object ETag and VersionId of code/gold/C_06.client_mix_timeseries.py (expect 2e35d043; VersionId zjQmOYVVYTSGOWLFQ0P33vVeWkwp4_eT) and code/gold/D_04.client_portal_summary.py (expect 9d083669; VersionId ap.CyBT8aJijz5kWFsSNjEFU99itbXED) and code/gold/gold_dispatch.sh (expect f568d11bbf074aaec8f06a01ee13dd2e). Any other value is a STOP and a report: the delta is then not this cell. Also read EVERY key under code/gold/ in opal-data-bd, pre and post (denominator printed).
    1. Window (COO condition 4): act only when no bd-gold-layer-runner instance is running, no gold/trigger-pending.json waits in opal-data-bd, and not inside a BD fire. Read both in the same shell as the deploy.
    2. Open ONE ledger entry, slug secclass-e97-c06-d04-rolling-rederive-sc1-20261012, with legs:
       - V: the step-0 reads;
       - P (COO condition 3), BEFORE the next BD fire: the current VersionIds of platinum/firm/mix_summary.json, gold/views/mix_daily_summary.json, gold/views/firm_composition.json, gold/artifacts/firm_mix_views.json, gold/artifacts/firm_mix_views_daily.json, every gold/entities/advisors/{id}/mix.json, mix_daily.json and mix_timeseries.json, every gold/entities/clients/{rid}.json and {rid}_views.json, and the legacy gold/client_timeseries/{rid}.json copies, written to org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E97_PREFIRE_VERSIONS_20261012.json with the page count and key count printed (paginate to exhaustion, IsLatest only); and the live bodies of platinum/firm/mix_summary.json and gold/artifacts/firm_mix_views.json saved beside it (the before side of the bars);
       - D: the ship;
       - G (COO conditions 5, 6, 9, 10 and the CTO's): after the first scheduled BD fire that RUNS C_06, the issuer's reads (2.0.0_SA_COO~M1 closes G; report when D closes). Report the first fire's C_06 wall time and the chain's launch-to-stop from the runner telemetry as soon as that fire ends, and the C06-ROLLING-REDERIVE and C06-ROLLING-RULE-UNREADABLE lines of its log.
       Name the rollback: both code objects by their step-0 VersionIds; each data key to its leg-P VersionId.
    3. THE ACT: `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py` and `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py` as ONE act under one ledger (D_04 first or second, back to back, no fire between: the window read in step 1 holds across both). Print the shipped member list each reports. Any member other than the two keys is a STOP: restore every moved key by its step-0 VersionId in the same session and report.
    4. Prove it with AC1. Re-read the watch set; a moved key outside the two is a STOP with the same-session restore. Close legs V, P and D. Leave G open for the issuer.
    5. STOP rule carried from the halves: if the first fire's chain runs more than 30 minutes longer than the pre-ship chain (the 04:00:46Z fire's launch-to-stop was at least 7,766.7 s, about 2h19m; use the SC-e-91 first fire's if it is read by then), or any window day's served firm total differs from the AUA by more than $1.00, or an advisor key is dropped, the issuer says so and you restore BOTH code objects by VersionId in that session (the data keys by leg P's VersionIds), reporting to 2.0.0_SA_COO~M1 with 1.0.0_SA_CTO~DELL1 copied.
  </the_act>

  <bounds>
    - Two S3 keys move, named above. Nothing else: no lib, no D_03, no _shared module, no other gold script, no gold_dispatch.sh, no data key by this act, no Lambda, no table write.
    - No IAM change and no resource-policy change. A refusal is a report, not a workaround.
    - IAM-grant conditions (CTO msg 1445): a send that writes a firm bucket or assumes the 49F principal outside the runner's own job is told to the laptop first; every send to mdpf-daily-runner is reported after the fact with command id and purpose; 49F data never enters another firm's tree.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e97b.c06-d04-rolling-rederive-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; step 1 keeps it outside every BD gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped D_04, C_06 and the lib to these keys (e60b, e79b, e87b, e91b).
comp-adversary: RUN -- the named-ship set (two explicit paths, no _shared member); a third member is a STOP with same-session restore; an empty success is excluded because AC1 requires BOTH served ETags to equal their repo md5s AND differ from the rollback ETags, with a discrimination control; a gold fire racing the ship is excluded by step 1; a ship on a base other than 2e35d043 and 9d083669 (another deploy moved a key since) is excluded by step 0; gold_dispatch.sh moving (the rule's source) is a STOP in AC1; the window re-derive moving a total without a source is excluded by the issuer's leg-G read and the STOP rule. BLIND: the first fire's wall time on the runner (the dry run was from a laptop), and whether the runner has gold_dispatch.sh beside C_06 (the fail-closed branch makes an absent file a no-op, which the issuer reads from the C06-ROLLING-RULE-UNREADABLE line).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-97"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R23_CHECKS/e97_shipped_check.py</invocation><expect>E97-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (2026-10-12 ~13:5xZ): `E97-SHIPPED ok=False c06=2e35d043|f847d8d1|DIFF d04=9d083669|43a5d613|DIFF control=MATCH dispatch=same d03=same`.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when leg D closes, or at a STOP, with:
    - step 0's reads and step 1's window read;
    - the safe-deploy lines and the shipped member list of each;
    - AC1's output and the watch-set re-read;
    - leg P's file path and key and page counts;
    - the ledger path, the proof instance, and the commit hashes with their measured push state.
    Then, after the first BD fire that runs C_06 following the ship, report that fire's C_06 wall time, the chain's launch-to-stop and its C06-ROLLING-REDERIVE line.
  </report>

</task_order>
