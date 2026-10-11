<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e87b.bd-served-path-reach-three-file-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>20</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R20.md</decomp_doc> (declares SC-e-87; the ship is the issuer act that follows the drain, by a CloudOps lane under its pair).
<owned_cells>SC-e-87</owned_cells>
</decomp_ref>

  <objective>
    Ship BD's three served classify sites, ALONE and TOGETHER: s3://opal-data-bd/code/gold/D_04.client_portal_summary.py (ETag 23d2f2ae5797834638bbda5b9e5eb584 -> md5 304573cf55816ceaadfbae7bbce4c810), code/gold/C_06.client_mix_timeseries.py (d7eb83b655b63143c24552bdfff197ad -> 1aa6e3b555815417bb90c65db3f2152f) and code/gold/D_03.composition_artifacts.py (84f9bf8e9ececc0712b0a6e3f67694f4 -> 6238716b575174c65e6c077469a4fcbc). No other key moves; the SC-e-79 lib stays at eb9bb852.
  </objective>

  <context>
    Why this seat: 1.0.0_SA_CTO~DELL1 msg 1445 ruled that a CloudOps seat applies each SECCLASS deploy, under the halves' conditions.
    BOTH halves are SIGNED. Read them in full first and carry every condition:
    - The request: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_BD_SERVED_PATH_REACH_20261011.md
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_COO_HALF_SECCLASS_BD_SERVED_PATH_REACH_20261011.md (@c6202193c5), conditions 1-5
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_BD_SERVED_PATH_REACH_20261011.md (@20526c6cc7)
    The repo bytes at the cut are the drained code, `box/dell1` @f4f01cfb27 (code commit c5f6642240): D_04 md5 304573cf..., C_06 1aa6e3b5..., D_03 6238716b... .
    THE WINDOW MATTERS TONIGHT: the BD nightly fire starts 04:00Z and its logs land about 2h15m later, so the earliest ship is after that chain completes (~06:20Z). Leg P must read the data keys' VersionIds AFTER that fire and BEFORE the next one (23:00Z fallback, Mon-Sat; 04:00Z next day).
    The leg-G read is the issuer's and is stated net of C_06's total-vs-class-sum gap (row D1-S27; cell SC-e-88's cause: share rounding at 6 decimals, about $128 on $2.0B).
  </context>

  <the_act>
    0. On box/dell1 at or after this order's commit, read the halves. Measure the pre-act state: head-object ETag and VersionId of the three keys above (expect 23d2f2ae / d7eb83b6 / 84f9bf8e; VersionIds In6p3j24Ok0Vyi3LRitAAfGi0yNgcGWq, y1QO4QB9EeDDn4jVUL6k25ZGuhqifMdm, kAktHpSbSrN0xq0CqbIJS3eqL8F2jt6e) and of the watch set: EVERY key under code/gold/ in opal-data-bd, read pre and post (denominator printed). Any of the three keys not at its expected ETag is a STOP and a report.
    1. Window (COO condition 3): act only when no bd-gold-layer-runner instance is running, no gold/trigger-pending.json waits in opal-data-bd, and not inside a BD fire.
    2. Open ONE ledger entry, slug `secclass-e87-bd-served-path-reach-sc1-20261011`, with legs:
       - V: the step-0 reads;
       - P (COO condition 2), BEFORE the next BD fire: the current VersionIds of platinum/firm/mix_summary.json, gold/views/mix_daily_summary.json, gold/views/firm_composition.json and every gold/entities/clients/{rid}.json, written to org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E87_PREFIRE_VERSIONS_20261011.json with the count printed;
       - D: the ship;
       - G (COO condition 4): after the next scheduled BD fire, the issuer's read (2.0.0_SA_COO~M1 closes G; report when D closes).
       Name the rollback per key: copy each key's step-0 VersionId back over it; each data key to its leg-P VersionId.
    3. THE ACT: `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py data/black_diamond/scripts/gold/D_03.composition_artifacts.py`. Print the shipped member list it reports. Any member other than the three keys is a STOP: restore every moved key by its step-0 VersionId in the same session and report.
    4. Prove it with AC1. Re-read the watch set; a moved key outside the three is a STOP with the same-session restore. Close legs V, P and D. Leave G open for the issuer.
  </the_act>

  <bounds>
    - Three S3 keys move, named above. Nothing else: no lib, no _shared module, no other gold script, no data key, no Lambda, no table write.
    - No IAM change and no resource-policy change. A refusal is a report, not a workaround.
    - IAM-grant conditions (CTO msg 1445): a send that writes a firm bucket or assumes the 49F principal outside the runner's own job is told to the laptop first; every send to mdpf-daily-runner is reported after the fact with command id and purpose; 49F data never enters another firm's tree.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e87b.bd-served-path-reach-three-file-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; step 1 keeps it outside every BD gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped D_04 (e60b) and the lib (e79b) to these keys.
comp-adversary: RUN -- the named-ship set (no _shared member: three explicit paths); a fourth member is a STOP with same-session restore; an empty success is excluded because AC1 requires each served ETag to equal its repo md5 AND differ from its rollback ETag, with a discrimination control and a check that the lib did not move; a gold fire racing the ship is excluded by step 1.
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-87"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R20_CHECKS/e87_shipped_check.py</invocation><expect>E87-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (~03:5xZ): `E87-SHIPPED ok=False d04=23d2f2ae|304573cf|DIFF c06=d7eb83b6|1aa6e3b5|DIFF d03=84f9bf8e|6238716b|DIFF control=MATCH lib=unmoved`.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when leg D closes, or at a STOP, with:
    - step 0's reads and step 1's window read;
    - the safe-deploy lines and the shipped member list;
    - AC1's output and the watch-set re-read;
    - leg P's file path and count;
    - the ledger path, the proof instance, and the commit hashes with their measured push state.
  </report>

</task_order>
