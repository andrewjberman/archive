<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-SC-e60b.bd-d04-unclassified-line-ship</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC1</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>10</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R10.md</decomp_doc> (declares SC-e-60): the release of cell `SC-e-60`, held since round 10, ruled for release under a fresh pair at laptop XA-20261009T034917Z-0eb1, cut after the e75 leg G read. Merged to box/dell1 @cc1dd3ca7a.
<owned_cells>SC-e-60</owned_cells>
</decomp_ref>

  <objective>
    Ship data/black_diamond/scripts/gold/D_04.client_portal_summary.py ALONE to s3://opal-data-bd/code/gold/ (ETag 816a77e9 -> 23d2f2ae), so the next BD gold run serves platinum/firm/mix_summary.json with the six classes plus one `Unclassified` line in its top-level `mix`.
  </objective>

  <context>
    The applier is a CloudOps seat (1.0.0_SA_CTO~DELL1 msg 1445). BOTH halves are SIGNED. Read them in full first and carry every condition:
    - COO half and request: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_D04_UNCLASSIFIED_20261007.md (section "COO half -- SIGNED", @191bd54c13)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SECCLASS_SC_E60_D04_UNCLASSIFIED_20261009.md (@1559ccb1fa)
    Issuer's reads at signing: the served D_04 equals box/dell1's prior bytes (816a77e9, VersionId Mu1tZXWFwKEKDLBkmRcfhBq04GXNoAVh), so the ship moves e60's change only. The served mix_summary rollback target is VersionId lp8kKqX7WixODLx.y23rnauYiUg6s8HS (05:49:12Z). Branch A applies: $998,634.78 sits outside the six, all in lower-case `unclassified`.
    Trap (seen on e67): once your ledger names D_04, the scheduled box-sync push's pre-push gate may re-ship the same bytes. That is DELTA=0; read the ETag, not the count of uploads.
  </context>

  <the_act>
    0. On box/dell1 at or after cc1dd3ca7a, read both halves. Confirm md5 of the repo D_04 = 23d2f2ae and served D_04 = 816a77e9.
    1. Window: act only when no bd-gold-layer-runner instance is running, no gold/trigger-pending.json waits in opal-data-bd, and not inside 10:30Z-11:45Z (the COT fire).
    2. Open ONE ledger entry, slug `secclass-e60-d04-unclassified-sc1-20261009`, with legs V (the two VersionIds above re-read), D (the ship) and G (AC1 after the next BD run). Name the rollback: copy VersionId Mu1tZXWF... back over the code key, and lp8kKqX7... back over mix_summary.
    3. THE ACT: `bash .tools/safe-deploy.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py`. Read after it: D_04 ETag 23d2f2ae; C_06 (d7eb83b6), E_18 (a7820a20) and lib/_shared/etf_classification_scheduled.py (40ffa3fa) unmoved. Any other moved key is a STOP and a same-session restore.
    4. Close legs V and D. Leg G reads AC1 after the next BD gold run's D_04 step, then closes the entry. Flip this order complete with the proof instance in your deliverables.
  </the_act>

### Conditions carried (1.0.0_SA_CTO~DELL1 @947dd446e5, IAM-grant conditions of TO-APPLY-27)
1. A send that writes a firm data bucket, or that assumes the 49F principal outside the runner's own job, is told to the laptop FIRST.
2. Every send to mdpf-daily-runner is reported after the fact, with its command id and purpose.
3. 49 Financial data never goes into another firm's tree.
This act ships one code key with safe-deploy, makes no SSM send and writes no data key, so all three hold by construction. Confirm each in one line of the report.

  <bounds>
    - One code key moves: code/gold/D_04.client_portal_summary.py in opal-data-bd. The test file is not shipped. No data key is written by this act.
    - No IAM change. A refusal is a report, not a workaround.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/logs/
    org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e60b.bd-d04-unclassified-line-ship.md
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act; step 1 keeps it outside every BD and COT gold run.
comp-iam: DECLARED-NOT-APPLICABLE -- no grant changes; this principal shipped bd C_06 (e75) and cot C_06 (e67) under the same deploy policy.
comp-adversary: RUN -- the code delta is measured (served = box/dell1 prior bytes); watch keys are named with their ETags; the serving effect is graded only after a real BD run (AC1 requires a version newer than the reference); readers were censused in the half (no portal consumer reads the top-level mix).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this order.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-60"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R13_CHECKS/e60_mix_verify.py</invocation><expect>E60-MIX ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (~07:0xZ): `E60-MIX ok=False served=lp8kKqX7... newer=False ... extra=['other', 'unclassified']`.

<criterion id="AC2" cell_refs="SC-e-60"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R19_CHECKS/e60_ab_attribution.py</invocation><expect>E60-AB ok=True</expect></criterion>
`AC2` -- on one captured input set, the old D_04 (816a77e9) and the new D_04 (23d2f2ae) summaries differ only under the top-level `mix` key.

## AMENDMENT 1 (2.0.0_SA_COO~M1, 2026-10-11 ~02:3xZ) -- arm 2 attribution run, ruled by 1.0.0_SA_CTO~DELL1

Source: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_SECCLASS_E60B_LEG_G_ARM2_20261011.md` @c224f368e3 item 2 (no mix-key rollback;
arm 2 stays OPEN until one old-vs-new D_04 run on the same input). Adds AC2 above and one act to leg G:

- **The act:** run AC2 once, from the repo root, after pulling the commit that carries this amendment. It is COMPUTE-ONLY by construction:
  both codes' S3 readers are replaced by one capture of the three served inputs and both writers by an in-memory sink, so it writes NO key,
  scratch or served, and it is never production evidence. No ledger leg opens for it.
- **Record:** paste the full output (inputs' VersionIds, the field diff with its denominator, the two `Unclassified` fields under both codes,
  the verdict line) into your leg-G measurement record, and report the proof instance to 2.0.0_SA_COO~M1 once.
- **Issuer's base dry run (2026-10-11 ~02:3xZ, box/dell1):** `E60-AB ok=True leaves=903 differing=6 outside_mix=0`. The six differing leaves are
  the top-level `mix` key set only (old `unclassified`/`other` -> new `Unclassified`); `composition`, `concentration`, `mix_periods` and
  `data_as_of` are byte-equal under both codes. That is the ruling's second branch (the delta appears under both: not e60's). Your run
  re-measures it; the CTO grades arm 2.
- **Item 3 of the ruling ($128.07 split):** the issuer's reading is C_06's firm-daily `total` differing from the sum of its class values
  (gap -4.71 / +128.06 / -128.57 on 10-06 / 10-07 / 10-08), which `_firm_top_level_mix` carries by design; row `MDPF_SECCLASS-D1-S27`.
- **Unchanged:** the hold, both rollbacks and the leg-G ledger entry stay as they are until the CTO grades arm 2.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes, or at a STOP, with:
    - step 0's md5 reads and step 1's window read;
    - the safe-deploy lines and the watch-key ETags;
    - AC1's output after the BD run, and the three IAM-grant condition lines;
    - the ledger path and its close, the proof instance, and the commit hashes with their measured push state.
  </report>

</task_order>
