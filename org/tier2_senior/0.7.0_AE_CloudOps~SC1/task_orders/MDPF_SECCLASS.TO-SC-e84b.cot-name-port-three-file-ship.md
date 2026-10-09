<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e84b.cot-name-port-three-file-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-09</date>
    <status>issued</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>17</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R17.md</decomp_doc> (declares SC-e-84; section "Issuer acts after the drain": the deploy, by a CloudOps lane under its pair, naming exactly three files).
<owned_cells>SC-e-84</owned_cells>
</decomp_ref>

  <objective>
    Ship the SC-e-84 COT NAME:: port: exactly three objects under s3://opal-data-cot/code/gold/ move to the repo bytes -- lib/etf_classifier.py (2fef39d1 -> aad03383), C_06.client_mix_timeseries.py (ea7e6700 -> 73e3949a), D_03.composition_artifacts.py (6f48eaf3 -> 30acf981). No other key moves.
  </objective>

  <context>
    Why this seat: 1.0.0_SA_CTO~DELL1 msg 1445 ruled that a CloudOps seat applies each SECCLASS deploy, under the half's conditions in the order.
    BOTH halves are SIGNED. Read them in full first and carry every condition:
    - The request with the COO half (conditions 1-4) and the transcribed CTO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_COT_NAME_PORT_20261009.md
    - The CTO half (conditions 5-6): org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SECCLASS_SC_E84_COT_NAME_PORT_20261009.md (@1a6daca8ab)
    The three files ship together: C_06 or D_03 without the lib passes asset_name= to a lib that rejects it, and the COT gold fire would fail.
    Named-file measure at the cut: `safe_deploy_core.shipped_artifacts_for(<the three paths>)` returns [] -- no _shared artifact rides.
    C_06's pre-act bytes (ea7e6700) are e67's shipped fix, whose ledger closed clean at the 2026-10-09 COT fire; the rollback keeps it.
  </context>

  <the_act>
    0. On box/dell1 at or after this order's commit, read both halves. Measure the pre-act state: head-object ETag and VersionId of the three keys (expect 2fef39d1 / ea7e6700 / 6f48eaf3; VersionIds MYI0nB3z..., 55IsnYrr..., vHHfV5Nd...) and of the watch keys code/gold/lib/_shared/etf_classification_scheduled.py and code/gold/E_18.detect_new_securities.py. A key not at its expected ETag is a STOP and a report.
    1. Window: act only outside a COT gold run. COT fires daily at 11:30Z (bronze, silver, then gold, which completes about 11:38Z). Check that no COT runner is running.
    2. Open ONE ledger entry, slug `secclass-e84-cot-name-port-sc1-20261009`, with legs:
       - V: the step-0 reads;
       - P (COO condition 2): BEFORE the next COT fire, the current VersionIds of platinum/firm/mix_summary.json, gold/views/mix_daily_summary.json and every gold/entities/clients/{rid}.json, written to org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E84_PREFIRE_VERSIONS_20261009.json with the count printed;
       - D: the ship;
       - G (COO condition 3, CTO conditions 5-6): after the next COT fire, the issuer's read (2.0.0_SA_COO~M1 closes G; report when D closes).
       Name the rollback per key: copy each key's step-0 VersionId back over it; each data key to its leg-P VersionId.
    3. THE ACT: `bash .tools/safe-deploy.sh --tree cot data/cot/scripts/gold/lib/etf_classifier.py data/cot/scripts/gold/C_06.client_mix_timeseries.py data/cot/scripts/gold/D_03.composition_artifacts.py`. Print the shipped member list it reports. Any member beyond the three is a STOP (COO condition 1): restore every moved key by its step-0 VersionId in the same session and report.
    4. Prove it with AC1. Re-read the watch keys of step 0; a moved watch key is a STOP with the same-session restore. Close legs V, P and D. Leave G open for the issuer.
  </the_act>

  <bounds>
    - Three S3 keys move, named above. Nothing else: no _shared module, no other gold script, no data key, no Lambda, no table write.
    - No IAM change and no resource-policy change. A refusal is a report, not a workaround.
    - IAM-grant conditions (CTO msg 1445): a send that writes a firm bucket or assumes the 49F principal outside the runner's own job is told to the laptop first; every send to mdpf-daily-runner is reported after the fact with command id and purpose; 49F data never enters another firm's tree.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e84b.cot-name-port-three-file-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; step 1 keeps it outside the 11:30Z COT gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped COT C_06 (e67, ea7e6700) at 2026-10-09T02:14:55Z.
comp-adversary: RUN -- the named-ship set measured by shipped_artifacts_for (no _shared member); a fourth shipped member is a STOP with same-session restore; a partial ship (lib absent) fails AC1 (moved must be 3 of 3); an empty success is excluded because AC1 requires each served ETag to equal its repo md5 AND differ from its pre-act ETag, with a discrimination control.
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-84"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R17_CHECKS/e84_shipped_check.py</invocation><expect>E84-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (~11:5xZ): `E84-SHIPPED ok=False moved=0 of 3 ... control=MATCH`.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when leg D closes, or at a STOP, with:
    - step 0's reads and step 1's window read;
    - the safe-deploy lines and the shipped member list;
    - AC1's output and the watch-key re-read;
    - leg P's file path and count;
    - the ledger path, the proof instance, and the commit hashes with their measured push state.
  </report>

</task_order>
