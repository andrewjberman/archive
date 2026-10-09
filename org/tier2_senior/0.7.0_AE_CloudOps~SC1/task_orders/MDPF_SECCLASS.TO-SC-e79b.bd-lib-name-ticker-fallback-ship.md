<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e79b.bd-lib-name-ticker-fallback-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-09</date>
    <status>issued</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>16</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R16.md</decomp_doc> (declares SC-e-79; section "Issuer acts after the drain": the lib deploy, by a CloudOps lane under its pair).
<owned_cells>SC-e-79</owned_cells>
</decomp_ref>

  <objective>
    Ship the SC-e-79 BD gold lib: s3://opal-data-bd/code/gold/lib/etf_classifier.py moves from ETag 535378b5e0b01891c3cf685faf1ed653 (VersionId yPda0uV6nypDdrdFVi.0ZW86Mdxk_cI2, the SC-e-76 lib) to the repo bytes, md5 eb9bb85208c96fa15ede01cf3618782d. No other key moves.
  </objective>

  <context>
    Why this seat: 1.0.0_SA_CTO~DELL1 msg 1445 ruled that a CloudOps seat applies each SECCLASS deploy, under the half's conditions in the order.
    BOTH halves are SIGNED. Read them in full first and carry every condition:
    - The request with the COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_BD_NAME_TICKER_FALLBACK_20261009.md (@bfabe0002d)
    - The CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALVES_SECCLASS_R16_E83_E79_20261009.md (@279fa3391e), section "SC-e-79", conditions 1-4.
    CTO condition 1 is MET: SC-e-83's row was written and read back as equity / US Large Cap at ~09:3xZ (ledger secclass-e83-ultra-name-row-m1-20261009, CLOSED @bfabe0002d).
    Named-file measure at the cut: `safe_deploy_core.shipped_artifacts_for(['data/black_diamond/scripts/gold/lib/etf_classifier.py'])` returns [] -- no _shared artifact rides this deploy.
    Repo bytes at the cut: md5 eb9bb852 (drain 16d5be89dd).
  </context>

  <the_act>
    0. On box/dell1 at or after this order's commit, read both halves. Measure the pre-act state: head-object ETag and VersionId of code/gold/lib/etf_classifier.py (expect 535378b5 / yPda0uV6...), and of the watch keys code/gold/lib/_shared/etf_classification_scheduled.py and code/gold/C_06.client_mix_timeseries.py in opal-data-bd. A lib not at 535378b5 is a STOP and a report.
    1. Window: act only outside a BD gold run. BD fires 04:00Z and 23:00Z (logs land ~2h15m later). Check that no bd-gold-layer-runner instance is running and that no gold/trigger-pending.json is waiting in opal-data-bd.
    2. Open ONE ledger entry, slug `secclass-e79-bd-lib-ship-sc1-20261009`, with legs:
       - V: the step-0 reads;
       - P (CTO condition 3): BEFORE the next BD fire, the current VersionIds of platinum/firm/mix_summary.json, gold/views/mix_daily_summary.json and every gold/entities/clients/{rid}.json, written to org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E79_PREFIRE_VERSIONS_20261009.json with the count printed;
       - D: the ship;
       - G (CTO condition 4): after the next BD fire, the issuer's read (2.0.0_SA_COO~M1 closes G; report when D closes).
       Name the rollback per key: copy VersionId yPda0uV6nypDdrdFVi.0ZW86Mdxk_cI2 back over the lib; each data key to its leg-P VersionId.
    3. THE ACT: `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/lib/etf_classifier.py`. Print the shipped member list it reports. Any member other than code/gold/lib/etf_classifier.py is a STOP (CTO condition 2): restore every moved key by its step-0 VersionId in the same session and report.
    4. Prove it with AC1. Re-read the watch keys of step 0; a moved watch key is a STOP with the same-session restore. Close legs V, P and D. Leave G open for the issuer.
  </the_act>

  <bounds>
    - One S3 key moves, named above. Nothing else: no _shared module, no other gold script, no data key, no Lambda, no table write.
    - No IAM change and no resource-policy change. A refusal is a report, not a workaround.
    - IAM-grant conditions (CTO msg 1445): a send that writes a firm bucket or assumes the 49F principal outside the runner's own job is told to the laptop first; every send to mdpf-daily-runner is reported after the fact with command id and purpose; 49F data never enters another firm's tree.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e79b.bd-lib-name-ticker-fallback-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; step 1 keeps it outside every BD gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped the SC-e-76 lib to this key at 2026-10-08T19:41:53Z.
comp-adversary: RUN -- the named-ship set measured by shipped_artifacts_for (no _shared member); a second shipped member is a STOP with same-session restore; an empty success is excluded because AC1 requires the served ETag to equal the repo md5 AND differ from the rollback ETag, with a discrimination control.
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-79"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R16_CHECKS/e79_shipped_lib_check.py</invocation><expect>E79-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (~09:4xZ): `E79-SHIPPED ok=False repo=eb9bb852... served=535378b5... rollback=535378b5... control=MATCH`.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when leg D closes, or at a STOP, with:
    - step 0's reads and step 1's window read;
    - the safe-deploy lines and the shipped member list;
    - AC1's output and the watch-key re-read;
    - leg P's file path and count;
    - the ledger path, the proof instance, and the commit hashes with their measured push state.
  </report>

</task_order>
