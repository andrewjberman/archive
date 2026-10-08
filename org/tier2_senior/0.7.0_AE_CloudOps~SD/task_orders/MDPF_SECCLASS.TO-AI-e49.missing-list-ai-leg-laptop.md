<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-AI-e49.missing-list-ai-leg-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SD</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>11</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R9.md</decomp_doc> (declares SC-e-49 at :58; released in round 11, DECOMP_R11.md "Issuer acts"): the release of cell `SC-e-49` (FWD-15); its DIRECT leg landed on dell1 (ledger secclass-e49-direct-leg-m1-20261007 CLOSED @f31f9d63bf, 278/278).
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

### AMENDMENT (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~01:5xZ) -- seat-gate condition, per 1.0.0_SA_CTO~DELL1 ADDENDUM 1 @0d520d9d70 (row S68)

Before ANY write:
- Run the deploy tool's --dry-seat-gates (or an equivalent read-only gate pass).
- Any verdict=STOP, in any gate mode, or any target that this seat's principal has not been MEASURED able to write, means the act does
  not start. Report the action and resource the same hour.
- An act with more than one write target proves write access on EVERY target before the first write.
This does not change the halves; it is a precondition the CTO added to every act it signed.

### AMENDMENT 4 -- S66 verdict and the first-secret-read report (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~07:0xZ)

1. S66 (CTO round-12 addendum 1 @e5befb00f1 item 1): the close check is `R12_CHECKS/ai_leg_verify.py` at @cedc99ac58 or later. It
   reads ok only when landed + refused == planned. A partial leg reads ok=False, and that is not a pass.
2. Laptop 1.0.0_SA_CTO msg 106758 rule (2), relayed in 0.0.0_AB_MSTR~DELL1 msg 827: when the Dell secrets grant applies, report the
   step-0 FIRST read of astn/kimi/api-key to 0.0.0_AB_MSTR~DELL1 like a deploy: the secret name, this order's run, and the UTC time.
   It is reported, not approved. The grant's CTO half is @8c4fe4be88 and the grant is not yet applied.
No gate limb grades an amendment to an existing order.

### AMENDMENT -- round tag (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~14:3xZ; 1.0.0_SA_CTO~DELL1 msg 961, from 3.0.0_SA_CVO msg 960)

This order carried no <round> tag, so surprise-row-gate.py (TO_ROUND_RE, :1246; the count at :1276-1279) counted it against every
round's slug. It belongs to round 11 (decomp_ref DECOMP_R11.md), so <round>11</round> is added to its metadata. No other field changes.
Gate limb: none grades a metadata tag on an existing order; the surprise-row-gate reads it at the next slug.

### AMENDMENT -- the face names the decomp that DECLARES the cell (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~18:2xZ; answers ~SD msg 1041, row D1-S10)

<decomp_doc> now DECOMP_R9.md, which declares SC-e-49; DECOMP_R11 only released it. <owned_cells> and <round>11</round> are unchanged.
Gate limb: to-pipeline-gate layer 1 grades the proof-of-spec instance at the flip; none grades this amendment.

### AMENDMENT -- throughput, as e32 amendments 6-7 (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~18:4xZ; answers ~SD msg 1047)

At the runner's default `--workers 1`, the 956 to_model keys take ~8 h at e32's measured 30.1 s/key. Switch the running window, and
resume (a resume plans only absent keys) with the following:
1. `--workers 4 --chunk 25` under the 10-minute no-progress watchdog, about 2 h. On HTTP 429 or repeated transport failures, drop to
   `--workers 2` and report. Do not raise it without a new ruling.
2. Each invocation writes a fresh snapshot, `E49_AI_SNAPSHOT_20261008.RUN<k>_<HHMM>Z.json`. The rollback input stays this order's
   first snapshot.
3. A transport or vendor failure (timeout, HTTP error, rate limit, empty or malformed body) is NOT a final refusal. That key stays
   absent and is re-planned. The close counts as `refused` only model-stated refusals, and reports reasons by count. At most one final
   1-key attempt per remaining transport key (e32 amendment 9). After it, a key that times out again is recorded as transport-terminal.
No gate limb grades an amendment to an existing order.

### AMENDMENT -- PAUSE at the next chunk boundary for Andrew's alternatives rule (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~19:0xZ; 1.0.0_SA_CTO~DELL1 msg 1062)

Andrew-direct ~19:0xZ, VERBATIM: "Hedge funds, private funds, real estate funds, all of this falls to Alternatives." Record:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_190xZ_HEDGE_PRIVATE_REAL_ESTATE_FUNDS_ARE_ALTERNATIVES.md`. The CTO
ruled that it binds this run's instructions. The model prompt (`_shared/etf_classification_model.py` `build_prompt`, :86-99) does not
state it.
1. Let the running chunk finish, then stop the run. Do not start the next chunk. Record the landed / refused / remaining counts.
2. Resume only when this order carries a further amendment naming the prompt commit that states the rule. A resume plans only absent
   keys, so nothing landed is lost.
3. Report, read-only, EVERY model-landed row in etf-classifications (e32 and e49 alike, about 1,532 model rows; per 1.0.0_SA_CTO~DELL1
   msg 1066) whose name reads as a hedge, private or real estate fund and whose class is not alternatives. Give key, name and class, as a
   TSV in your deliverables. Do not rewrite them; they are remapped under the D1-S11 fix's pair.
No gate limb grades an amendment to an existing order.

### AMENDMENT -- RESUME on the prompt that states Andrew's rule (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~19:3xZ; answers ~SD msg 1067)

The prompt commit is SC-e-78 @1748729797, merged on dell1 @dd6fa463d5. `build_prompt` now reads "Hedge funds, private funds and real
estate funds are all alternatives." `R15_CHECKS/sc_r15_prompt_rule.py` reads PROMPT-RULE ok=True, and the _shared suite 356 passed.
1. Before the first chunk, confirm the runner imports that module from this tree (`git log -1 --format=%h --
   infra/aws/lambda/v2_portal/_shared/etf_classification_model.py` reads 1748729797 or a descendant). Run sc_r15_prompt_rule.py once and
   record its line.
2. Resume with `--workers 2 --chunk 25` under the watchdog. The 17 transport failures in 200 keys (8.5 pct) fired amendment 7's
   drop-to-2. Write a fresh RUN snapshot as before.
3. The step-3 read of earlier landed rows is superseded by SC-e-77's REMAP scan, which covers every model-landed row. Do not repeat it.
4. Close as the throughput amendment says: model-stated refusals by count; at most one final 1-key attempt per remaining transport
   key.
No gate limb grades an amendment to an existing order.

### AMENDMENT -- back to --workers 4: concurrency is not the transport cause (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~20:0xZ; answers ~SD msg 1127)

Measured transport failures:
- 2 workers: 11 in 150 keys, 7.3 pct.
- 4 workers: 17 in 200 keys, 8.5 pct.
They are indistinguishable, so amendment 7's drop-to-2 premise reads false. 2 workers costs 371 s per chunk against 195 s.
At the next chunk boundary, return to `--workers 4 --chunk 25`. Transport keys stay re-planned, with at most one final 1-key attempt
each. Drop to 2 only on an HTTP 429, not on the transport rate. No gate limb grades an amendment to an existing order.

### AMENDMENT -- exclude the twice-refused FINAL keys from every plan (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~20:3xZ; answers ~SD msg 1133)

`E49_TWICE_REFUSED_FINAL_20261008.json` (~SD deliverables) lists 47 keys. Each was model-refused in run 2 and again in run 3 under the
SC-e-78 prompt, so it is FINAL per msg 1100. The runner plans on absence, so it re-asked them on every restart.
1. `R12_CHECKS/e49_ai_write.py` gains `--exclude <json>`. It drops those keys from the plan only, never from the rollback.
2. Dry run at ~20:3xZ with `--exclude` on that file:
   `E49-AI-DRY-RUN ... present_now=309 excluded_final=43 to_model=709 runner_direct=0 ... ok=True`.
   The other 4 of the 47 have landed since the file was written.
3. At the next chunk boundary, resume with `--exclude org/tier2_senior/0.7.0_AE_CloudOps~SD/deliverables/E49_TWICE_REFUSED_FINAL_20261008.json`
   plus `--workers 4 --chunk 25`. At close, the excluded keys count as model-stated refused.
No gate limb grades an amendment to an existing order.

