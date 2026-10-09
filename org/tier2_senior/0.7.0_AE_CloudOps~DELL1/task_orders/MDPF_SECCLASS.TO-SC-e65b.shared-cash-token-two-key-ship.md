<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e65b.shared-cash-token-two-key-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>12</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (declares SC-e-65): the live release of cell `SC-e-65` amendment 3 (row S63), held in round 12 on limit item 5 (L8_DRAIN_END_PACKET_R12_20261008.md "Still open after the round"); item 5 is lifted.
<owned_cells>SC-e-65</owned_cells>
</decomp_ref>

  <objective>
    Ship the cash-token module (the ticker leg skips NAME:: keys) to its two firm copies: code/gold/lib/_shared/etf_classification_scheduled.py in opal-data-bd and opal-data-cot moves from md5 3f1e6be8910952f33c88bf100c610ab6 to 40ffa3fac380551704637adc8a3b6ff3, and no other key moves.
  </objective>

  <context>
    Why this seat: 1.0.0_SA_CTO~DELL1 msg 1445 (2026-10-09 ~02:1xZ) ruled that from e65b on, a CloudOps seat applies each deploy, under the half's conditions in the order.
    BOTH halves are SIGNED. Read them in full first and carry every condition:
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_CASH_TOKEN_NAMEKEY_20261007.md (@86843a40fd)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e65_AM3_NAMEKEY_DEPLOY_20261007.md (@7f68da7051)
    The first ledger for this act, secclass-e65b-namekey-deploy-s-20261007 (0.7.0_AE_CloudOps~SD), was CLOSED WITHDRAWN at @7247f0d321: it was never applied, and both keys were measured at 3f1e6be8. This order opens a fresh ledger.
    Mechanism change since signing (CTO condition 1): the gold carriers no longer ship this module. Under 1.0.0_SA_CTO msg 107147, safe-deploy ships only the files a deploy names. The named form below moves exactly the two signed keys; safe_deploy_core.shipped_artifacts_for() returns exactly (opal-data-bd, opal-data-cot) for it. The issuer measured that at ~02:3xZ.
    Repo bytes at the cut: md5 40ffa3fa... (commit 1fae201565), equal to the signed target.
  </context>

  <the_act>
    0. On box/dell1 at or after this order's commit, read both halves. Then measure the pre-act state and record it: head-object ETag and VersionId of code/gold/lib/_shared/etf_classification_scheduled.py in both buckets (expect 3f1e6be8; bd VersionId 5BZygWLx..., cot 0e4OsubY...), and of code/gold/C_06.client_mix_timeseries.py and code/gold/E_18.detect_new_securities.py in both buckets (the watch keys). A key not at 3f1e6be8 is a STOP and a report.
    1. Window (CTO condition 2): act only outside a BD or COT gold run. BD fires 04:00Z and 23:00Z (logs land ~2h15m later); COT fires 10:30Z (~1h10m). Check that no bd-gold-layer-runner instance is running, and that no gold/trigger-pending.json is waiting in opal-data-bd.
    2. Open ONE ledger entry, slug `secclass-e65b-namekey-ship-dell1-20261009`, with legs V (the pre-act reads of step 0), D (the ship) and G (the next BD E_18 run plans no NAME:: key that is not a whole cash phrase as cash; CTO condition 3). Name the rollback per key: copy the step-0 VersionId back over each key.
    3. THE ACT: `bash .tools/safe-deploy.sh --tree black_diamond --tree cot infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py`. It must print DEPLOYED or VERIFY lines for exactly the two keys.
    4. Prove it with AC1. Re-read the watch keys of step 0: any key other than the two that moved is a STOP; restore it and the two keys by VersionId, the same session. Close legs V and D.
    5. Leg G: read the next BD gold run's E_18 plan lines. Close the entry with that read, then flip this order complete with the proof instance in your deliverables.
  </the_act>

  <bounds>
    - Two S3 keys move, both named above. Nothing else: no gold script, no data key, no Lambda, no table write.
    - No IAM change and no resource-policy change. A refusal is a report, not a workaround.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~DELL1/task_orders/MDPF_SECCLASS.TO-SC-e65b.shared-cash-token-two-key-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; step 1 keeps it outside every BD and COT gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same principal shipped cot C_06 at 02:14:55Z under the same deploy policy.
comp-adversary: RUN -- the named-ship set measured by shipped_artifacts_for (exactly two keys); a watch-key move is a STOP with same-session restore; an empty success is excluded because AC1 requires both keys at the target and a matching control.
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-65"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e65_shipped_etag_check.py 40ffa3fac380551704637adc8a3b6ff3</invocation><expect>E65-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (~02:3xZ): `E65-SHIPPED ok=False head=40ffa3fa... bd=3f1e6be8... cot=3f1e6be8... control=MATCH`.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes, or at a STOP, with:
    - step 0's reads and step 1's window read;
    - the safe-deploy lines;
    - AC1's output, the watch-key re-read and leg G's E_18 read;
    - the ledger path and its close, the proof instance, and the commit hashes with their measured push state.
  </report>

</task_order>
