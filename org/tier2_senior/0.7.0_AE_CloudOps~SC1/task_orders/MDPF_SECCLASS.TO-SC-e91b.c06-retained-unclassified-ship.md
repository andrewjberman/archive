<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e91b.c06-retained-unclassified-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-12</date>
    <status>complete</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>21</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R21.md</decomp_doc> (declares SC-e-91; the ship is the issuer act that follows the drain, by a CloudOps lane under its pair).
<owned_cells>SC-e-91</owned_cells>
</decomp_ref>

  <objective>
    Ship C_06 ALONE: s3://opal-data-bd/code/gold/C_06.client_mix_timeseries.py (ETag 8e1b350fc55607bddd1ac84329cb1a98 -> md5 2e35d043163cc18b135d7698cf11dc56). No other key moves: not D_04, not D_03, not the lib, not any data key by this act.
  </objective>

  <context>
    Why this seat: 1.0.0_SA_CTO~DELL1 msg 1445 ruled that a CloudOps seat applies each SECCLASS deploy, under the halves' conditions.
    BOTH halves are SIGNED. Read them in full first and carry every condition:
    - The request (with its Reach section): org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_C06_RETAINED_UNCLASSIFIED_20261012.md
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_COO_HALF_SECCLASS_C06_RETAINED_UNCLASSIFIED_20261012.md (@ac447d74cf), conditions 1-7
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_SECCLASS_C06_RETAINED_UNCLASSIFIED_20261012.md (the outcome is the Reach range; beyond either bound is a STOP and a rollback)
    The repo bytes at the cut are the drained code, `box/dell1` at or after e270f70be4 (code commit a9f4bac7b5): C_06 md5 2e35d043163cc18b135d7698cf11dc56. Work from a checkout at or after that commit.
    What the act does NOT do: it moves no unclassified dollar outside a relationship's stored top-10 holdings list; the expected move is the RANGE $0 to $653,857.12 at as_of 2026-10-09 and $0 to $629,530.89 at 2026-10-08, never the $966,285.46 classifier total.
    THE WINDOW: fires are `bd-gold-trigger` launches (04:00Z nightly, 23:00Z fallback Monday to Saturday, and event-driven launches such as 2026-10-12T00:18Z). Leg P must read the data keys' VersionIds AFTER the last fire and BEFORE the next one; read the runner state in the SAME shell as the deploy.
    Today the SERVED C_06 is the ADVI FB-f-9 mode-move object (ETag 8e1b350f, VersionId 5xAeM.OWYUSxd7gHYSF6SKmR.ZTmo.PP, 2026-10-12T06:18:21Z), not the SC-e-87 object the request's older text cites; D_04 (9d083669), D_03 (bd9bbe4b) and the lib (e714dc50) were re-shipped by that move.
    The leg-G read is the issuer's and has two reads (COO condition 5): the retained-date range at 2026-10-09 and 2026-10-08, and the SECOND fire's idempotence (0 relationship keys rewritten).
  </context>

  <the_act>
    0. On box/dell1 at or after this order's commit, read the halves. Measure the pre-act state: head-object ETag and VersionId of code/gold/C_06.client_mix_timeseries.py (expect 8e1b350f; VersionId 5xAeM.OWYUSxd7gHYSF6SKmR.ZTmo.PP; any other value is a STOP and a report: the delta is then not this cell) and of the watch set: EVERY key under code/gold/ in opal-data-bd, read pre and post (denominator printed).
    1. Window (COO condition 3): act only when no bd-gold-layer-runner instance is running, no gold/trigger-pending.json waits in opal-data-bd, and not inside a BD fire. Read both in the same shell as the deploy.
    2. Open ONE ledger entry, slug `secclass-e91-c06-retained-unclassified-sc1-20261012`, with legs:
       - V: the step-0 reads;
       - P (COO condition 2), BEFORE the next BD fire: the current VersionIds of platinum/firm/mix_summary.json, gold/views/mix_daily_summary.json, gold/views/firm_composition.json, every gold/entities/clients/{rid}.json and {rid}_views.json, and the legacy gold/client_timeseries/{rid}.json copies, written to org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E91_PREFIRE_VERSIONS_20261012.json with the page count and key count printed (paginate to exhaustion, IsLatest only);
       - D: the ship;
       - G (COO conditions 4 and 5, CTO condition 1): after the first scheduled BD fire, the issuer's reads (2.0.0_SA_COO~M1 closes G; report when D closes). Report the first fire's C_06 wall time and the chain's launch-to-stop from the runner telemetry as soon as that fire ends.
       Name the rollback: the C_06 object by its step-0 VersionId; each data key to its leg-P VersionId.
    3. THE ACT: `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py`. Print the shipped member list it reports. Any member other than the one key is a STOP: restore every moved key by its step-0 VersionId in the same session and report.
    4. Prove it with AC1. Re-read the watch set; a moved key outside the one is a STOP with the same-session restore. Close legs V, P and D. Leave G open for the issuer.
    5. STOP rule carried from the halves: if the first fire's chain runs more than 30 minutes longer than the 04:00:46Z fire's launch-to-stop (about 2h19m), or a retained date's Unclassified falls beyond the Reach bound, the issuer says so and you restore the C_06 object by VersionId in that session (the data keys by leg P's VersionIds), reporting to 2.0.0_SA_COO~M1 with 1.0.0_SA_CTO~DELL1 copied.
  </the_act>

  <bounds>
    - One S3 key moves, named above. Nothing else: no lib, no _shared module, no other gold script, no data key by this act, no Lambda, no table write.
    - No IAM change and no resource-policy change. A refusal is a report, not a workaround.
    - IAM-grant conditions (CTO msg 1445): a send that writes a firm bucket or assumes the 49F principal outside the runner's own job is told to the laptop first; every send to mdpf-daily-runner is reported after the fact with command id and purpose; 49F data never enters another firm's tree.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e91b.c06-retained-unclassified-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; step 1 keeps it outside every BD gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; the same deploy path shipped D_04, C_06 and the lib to these keys (e60b, e79b, e87b).
comp-adversary: RUN -- the named-ship set (one explicit path, no _shared member); a second member is a STOP with same-session restore; an empty success is excluded because AC1 requires the served ETag to equal the repo md5 AND differ from the rollback ETag, with a discrimination control; a gold fire racing the ship is excluded by step 1; a ship on a base other than 8e1b350f (another deploy moved C_06 since) is excluded by step 0; the retained pass moving more than the Reach range is excluded by the issuer's leg-G read and the STOP rule. BLIND: the first fire's wall time (the pass reads about 3,793 relationship JSONs, 4.77 GB).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-91"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R21_CHECKS/e91_shipped_check.py</invocation><expect>E91-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (2026-10-12 ~10:0xZ): `E91-SHIPPED ok=False c06=8e1b350f|2e35d043|DIFF control=MATCH d04=same d03=same`.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when leg D closes, or at a STOP, with:
    - step 0's reads and step 1's window read;
    - the safe-deploy lines and the shipped member list;
    - AC1's output and the watch-set re-read;
    - leg P's file path and key and page counts;
    - the ledger path, the proof instance, and the commit hashes with their measured push state.
    Then, after the first BD fire that follows the ship, report that fire's C_06 wall time and chain launch-to-stop.
  </report>

</task_order>
