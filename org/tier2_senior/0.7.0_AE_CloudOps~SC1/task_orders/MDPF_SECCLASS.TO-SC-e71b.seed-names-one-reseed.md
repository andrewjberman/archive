<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e71b.seed-names-one-reseed</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>12</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R12.md</decomp_doc> (declares SC-e-71): the release of cell `SC-e-71`. The build was merged to box/dell1 @021a6a33f7, and its release was ruled (a) at laptop cross-adjudication XA-20261009T034916Z-ccd1.
<owned_cells>SC-e-71</owned_cells>
</decomp_ref>

  <objective>
    Run ONE re-seed of etf-classifications from box/dell1 at or after 021a6a33f7, so the 12 seed-source names land clean on 15 rows with no class field moved.
  </objective>

  <context>
    Applier: a CloudOps seat (1.0.0_SA_CTO~DELL1 msg 1445). BOTH halves are SIGNED. Read them in full first and carry every condition:
    - COO half and request: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_SEED_NAMES_E71_20261009.md (its condition-1 census section is MET)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SECCLASS_SC_E71_SEED_NAMES_20261009.md (@d6c99a32d5, branch (a), conditions 1-4)
    - Cross-adjudication: XA-20261009T034916Z-ccd1, RULED (a) 03:54:27Z (`python .tools/xadj.py show --id XA-20261009T034916Z-ccd1`).
    Issuer's dry run at box/dell1 @021a6a33f7, ~04:0xZ: `rows to write: 15 of 197`; a CONFLICT block names exactly the 12 `name` fields (AAETX AMECX CAIBX CFIHX CLBAX FBALX FKIQX FTYPX KAGIX MDLOX SGIIX VTTHX); BLOCKED without the flag.
    The delta is signed for: on all 15 rows, `updated_by` becomes seed-script and `low_confidence` is removed; `name` becomes clean on the 12; no class field moves.
    Trap (row MDPF_SECCLASS-D1-S18): under --dry-run the script still prints "Items written: N". Read the WRITTEN/DRY RUN marker and the table, never that line.
  </context>

  <the_act>
    0. On box/dell1 at or after 021a6a33f7, read both halves and the XA ruling. Confirm `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/sc_r12_seed_names.py` reads `SEED-NAMES ok=True`.
    1. Snapshot (CTO condition 2): the snapshot org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E71_SEED_ROWS_SNAPSHOT_20261009.json exists. Re-read the 15 rows consistently and confirm each still equals its snapshot. A row that moved is a STOP and a report.
    2. Dry run: `python infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py --region us-east-1 --dry-run`. It must read `rows to write: 15 of 197`, with a CONFLICT block on exactly the 12 `name` fields. Any other field in CONFLICT is a STOP (condition 4).
    3. Open ONE ledger entry, slug `secclass-e71-seed-names-sc1-20261009`, with legs V (step 1), W (the run) and G (AC1 plus a second dry run reading 0 of 197). Name the rollback: put each snapshot item back with condition `updated_by = 'seed-script'`.
    4. THE ACT: `python infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py --region us-east-1 --accept-module-truth`. Exactly once.
    5. Prove it with AC1. A second `--dry-run` must read `rows to write: 0 of 197`. Close the entry and flip this order complete, with the proof instance in your deliverables.
  </the_act>

  <bounds>
    - One table, etf-classifications (us-east-1), and these 15 rows only. No S3 key, no Lambda, no other table.
    - No IAM change. A refusal is a report, not a workaround.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e71b.seed-names-one-reseed.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act. The seed script has no schedule, and it is the table's only seed-row writer.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes. This principal wrote etf-classifications rows tonight (e77 at 20:3xZ on 10-08).
comp-adversary: RUN -- the delta is measured per field (15 rows, 2 fields plus 12 names); a CONFLICT beyond the 12 names is a STOP; the D1-S18 dry-run print trap is named; an empty success is excluded because AC1 requires 12 of 12 names and updated_by on all 15.
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-71"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R13_CHECKS/e71_reseed_verify.py</invocation><expect>E71-RESEED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (~04:0xZ): `E71-RESEED ok=False rows=15 names_ok=0/12 class_moved=[]`, with updated_by still mdpf-secclass-remap-b on all 15.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes, or at a STOP, with:
    - step 1's re-read and step 2's dry-run lines;
    - the act's WRITTEN lines;
    - AC1's output and the second dry run's summary;
    - the ledger path and its close, the proof instance, and the commit hashes with their measured push state.
  </report>

</task_order>
