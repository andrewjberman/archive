<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-AI-e32.old-list-v3-ai-leg-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SC</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (round 11), "Issuer acts": the release of cells `SC-e-32`/`SC-e-50`, old-list set V3; its DIRECT leg landed on dell1 (ledger secclass-e32-old-list-v3-write-m1-20261007 CLOSED @dd4fc38213, 5182/5182).
<owned_cells>SC-e-32, SC-e-50</owned_cells>
</decomp_ref>

  <objective>
    Run the AI leg of the e32 V3 old-list act: the existing runner (kimi-k3, name and key only) over the 2,291 old-list AI keys, in chunks of 250, bound by contract 0.8.0, landing new rows in `etf-classifications` by conditional put, and rewriting the AI listing per chunk.
  </objective>

  <context>
    Why this seat: dell1's principal is denied secretsmanager:GetSecretValue on astn/kimi/api-key (e32, 0 calls made). Laptop
    1.0.0_SA_CTO named the act for a laptop seat (msgs 106534, 106535); ~SC is a fresh lane (spawned 20:05Z, msg 623) because
    ~I holds IRPT_BCKEND orders (one project per Tier-2 seat). This act runs FIRST. TO-AI-e49 starts only after this order is complete.
    BOTH halves are SIGNED; read them in full first and carry every condition:
    - COO half (V3, with conditions 1-3) and the CTO half's record: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_OLD_LIST_RECLASSIFY_20261007.md
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e32_e50_OLD_LIST_V3_20261007.md (@8779dcc505)
    - Vendor word: Andrew-direct 2026-10-06 00:03Z, "RUn on the full old table" (up to 8,495 old-table rows).
  </context>

  <the_act>
    0. On the laptop's CLOUD, which carries q/dell1/secclass-r12-run-e32 r3 (58843e1461) or later, read both halves. Then read the
       secret once (a describe, or the runner's own get) with no model call. A refusal there is a REPORT, not a workaround.
    1. DRY RUN: `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R10_CHECKS/old_list_reclassify_write.py --set org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/OLD_LIST_RECLASSIFY_SET_V3_20261007.tsv`. It must read, on its first INFO line, direct_keys=0 ai_keys=2291 ... off_vocab=0, and on the second, `to_model=2291`. Its last
       line must be `RECLASSIFY-DRY-RUN` with no `-BAD`. That last line counts set ROWS by route (to_ai=2770 rows = 2,291 keys), not keys. Any other count is a STOP that goes back to the signers.
    2. Open ONE NEVER-2 ledger entry, slug `secclass-e32-ai-leg-i-20261007`, naming the table, the AI listing prefix, the snapshot path, and the
       rollback `old_list_reclassify_write.py --rollback --half <same> --snapshot org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_20261007.json` (deletes only keys absent from that snapshot that carry this run's updated_by values).
    3. THE ACT: `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R10_CHECKS/old_list_reclassify_write.py --set org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/OLD_LIST_RECLASSIFY_SET_V3_20261007.tsv --write --half org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_OLD_LIST_RECLASSIFY_20261007.md --snapshot org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_20261007.json --chunk 250`. Each chunk prints keys_sent, model_calls and landed_outside_contract. A STOP on a chunk is a rollback
       of this run (step 2's command), same session.
    4. Prove it (AC1) and close the entry with the `RECLASSIFY-WRITE` line and AC1's output. Flip this order complete, with the proof
       instance in your deliverables.
  </the_act>

  <bounds>
    - One table, `etf-classifications` (us-east-1), plus the AI listing object the runner rewrites. Nothing else. bd-securities is
      read only. No other model, and no payload field beyond name and key.
    - No package install or download. No IAM change: if the secret refuses, report it.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SC/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SC/logs/
    org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_20261007.json
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; it runs outside any E_18 run on the table.
comp-iam: RUN -- the seat's own read of astn/kimi/api-key is step 0; no grant changes.
comp-adversary: RUN -- vendor scope (the halves' words, the key ceilings in the executor); the contract bound (a per-chunk stop); a half-landed run (rollback by snapshot, same session); an empty success (AC1 needs landed>0 and the listing count equal to the model rows).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this act's snapshot file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-32"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/ai_leg_verify.py e32 org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_20261007.json</invocation><expect>AI-LEG-VERIFY act=e32 ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (missing_snapshot; with the DIRECT snapshot in its place, landed=0 and listing_count=None).

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes, or at a STOP, with:
    - step 0's secret read and step 1's dry-run line;
    - the per-chunk lines and the final RECLASSIFY-WRITE line;
    - AC1's output, the ledger path and its close, and the proof instance;
    - the commit hashes with their measured push state.
  </report>
</task_order>

<!-- AMENDMENT 1 (issuer 2.0.0_SA_COO~M1, 2026-10-07 ~22:5xZ): step 1 names the INFO lines as the key count. RULED CONTINUE on
~SC's dry-run report (direct=5532 to_ai=2770 is the row summary). Independent live read at 22:36Z: ai_leg_verify e32 planned=2291
landed=187 problems=0 multi_asset=0 listing_count=200=model_rows. -->
