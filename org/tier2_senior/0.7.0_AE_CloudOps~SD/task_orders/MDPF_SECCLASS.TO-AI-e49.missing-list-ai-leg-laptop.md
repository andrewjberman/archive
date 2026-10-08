<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-AI-e49.missing-list-ai-leg-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SD</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (round 11), "Issuer acts": the release of cell `SC-e-49` (FWD-15); its DIRECT leg landed on dell1 (ledger secclass-e49-direct-leg-m1-20261007 CLOSED @f31f9d63bf, 278/278).
<owned_cells>SC-e-49</owned_cells>
</decomp_ref>

  <objective>
    Run the AI leg of SC-e-49: the existing runner (kimi-k3, name and key only) over the three firms' missing-list AI keys (1,061 distinct keys, at most 1,172), in chunks of 250, bound by contract 0.8.0, by conditional put, rewriting the AI listing per chunk.
  </objective>

  <context>
    Why this seat: dell1's principal is denied secretsmanager:GetSecretValue on astn/kimi/api-key (e32, 0 calls made). Laptop
    1.0.0_SA_CTO named the act for a laptop seat (msgs 106534, 106535); ~SC is a fresh lane (spawned 20:05Z, msg 623) because
    ~I holds IRPT_BCKEND orders (one project per Tier-2 seat). This act runs SECOND: start only when MDPF_SECCLASS.TO-AI-e32 reads complete.
    BOTH halves are SIGNED; read them in full first and carry every condition:
    - COO half (with conditions): org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_FWD15_AI_20261007.md
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e49_FWD15_AI_RUN_20261007.md (@6eab3cda67)
    - Vendor word: laptop 1.0.0_SA_CTO msg 106533, on Andrew-direct 2026-10-07 ~18:3xZ item 4 ("The Dell Boxes have vendor
      egress as needed"): the keys are covered, at most 2,344 calls.
  </context>

  <the_act>
    0. On CLOUD (a dell1 checkout), which carries q/dell1/secclass-r12-run-e32 r3 (58843e1461) or later, read both halves. Then read the
       secret once (a describe, or the runner's own get) with no model call. A refusal there is a REPORT, not a workaround.
    1. DRY RUN: `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e49_ai_write.py`. It must read `E49-AI-DRY-RUN ... runner_direct=0 ... ok=True`, keys=1061, with to_model at or under 1,049 (the e32 act lands up to 157 of these keys first, and the runner skips a present key).
    2. Open ONE NEVER-2 ledger entry, slug `secclass-e49-ai-leg-i-20261007`, naming the table, the AI listing prefix, the snapshot path, and the
       rollback `e49_ai_write.py --rollback --write --snapshot org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E49_AI_SNAPSHOT_20261007.json` (deletes only keys absent from that snapshot with updated_by mdpf-secclass-model).
    3. THE ACT: `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e49_ai_write.py --write --half org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_FWD15_AI_20261007.md --cto-half org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e49_FWD15_AI_RUN_20261007.md --snapshot org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E49_AI_SNAPSHOT_20261007.json --chunk 250`. Each chunk prints keys_sent, model_calls and landed_outside_contract. A STOP on a chunk is a rollback
       of this run (step 2's command), same session.
    4. Prove it (AC1) and close the entry with the `E49-AI-WRITE` line and AC1's output. Flip this order complete, with the proof
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
    org/tier2_senior/0.7.0_AE_CloudOps~SD/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SD/logs/
    org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E49_AI_SNAPSHOT_20261007.json
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; it runs outside any E_18 run on the table.
comp-iam: RUN -- the seat's own read of astn/kimi/api-key is step 0; no grant changes.
comp-adversary: RUN -- vendor scope (the halves' words, the key ceilings in the executor); the contract bound (a per-chunk stop); a half-landed run (rollback by snapshot, same session); an empty success (AC1 needs landed>0 and the listing count equal to the model rows).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this act's snapshot file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-49"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/ai_leg_verify.py e49 org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E49_AI_SNAPSHOT_20261007.json</invocation><expect>AI-LEG-VERIFY act=e49 ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (missing_snapshot; with the DIRECT snapshot in its place, landed=0 and listing_count=None).

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes, or at a STOP, with:
    - step 0's secret read and step 1's dry-run line;
    - the per-chunk lines and the final E49-AI-WRITE line;
    - AC1's output, the ledger path and its close, and the proof instance;
    - the commit hashes with their measured push state.
  </report>
</task_order>

### AMENDMENT 3 -- executor dell1 0.7.0_AE_CloudOps~SD, gated on the Dell key grant (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~00:4xZ)

Andrew-direct ~00:0xZ: "the whole point of the dell boxes is to run the heavy jobs there". Laptop CTO msg 106657 and CTO~DELL1 amend
914acafe20 move this act to a dell1 seat. GATE: start only after the Dell group can read astn/kimi/api-key. The grant cell runs at laptop
COO~C, and step 0's own secret read is the proof. Until then this order is pending and makes no model call.
Everything else is unchanged: the halves, the head (a dell1 checkout carrying run-e32 r5 or later), the bound, the chunking, the rollback
input, and the completeness at close. TO-AI-e32 continues ledger entry secclass-e32-ai-leg-i-20261007 (run 1 by laptop ~SC: 187 of
2,291). Add a "run 2 on dell1 ~SD" line to it; do not open a second entry. TO-AI-e49 opens its own entry, and only after TO-AI-e32 is complete.
