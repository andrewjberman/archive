<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-AI-e32.old-list-v3-ai-leg-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SD</issued_to>
    <date>2026-10-07</date>
    <status>complete</status>
    <project_code>MDPF_SECCLASS</project_code>
    <round>11</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R8.md</decomp_doc> (declares SC-e-32 at :67; released in round 11, DECOMP_R11.md "Issuer acts"): the release of cells `SC-e-32`/`SC-e-50`, old-list set V3; its DIRECT leg landed on dell1 (ledger secclass-e32-old-list-v3-write-m1-20261007 CLOSED @dd4fc38213, 5182/5182).
<owned_cells>SC-e-32</owned_cells>
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
    0. On CLOUD (a dell1 checkout), which carries q/dell1/secclass-r12-run-e32 r3 (58843e1461) or later, read both halves. Then read the
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
    org/tier2_senior/0.7.0_AE_CloudOps~SD/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SD/logs/
    org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_20261007.json
    org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_RUN2_20261007.json
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an ad-hoc issuer act, not a scheduled producer; it runs outside any E_18 run on the table.
comp-iam: RUN -- the seat's own read of astn/kimi/api-key is step 0; no grant changes.
comp-adversary: RUN -- vendor scope (the halves' words, the key ceilings in the executor); the contract bound (a per-chunk stop); a half-landed run (rollback by snapshot, same session); an empty success (AC1 needs landed>0 and the listing count equal to the model rows).
lane: the <paths> block names the ledger, the sentinel, the seat's deliverables and logs, and this act's snapshot file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-32"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/ai_leg_verify.py e32 org/tier2_senior/0.7.0_AE_CloudOps~SC/deliverables/E32_AI_SNAPSHOT_20261007.RUN1_PRESERVED_COPY.json</invocation><expect>AI-LEG-VERIFY act=e32 ok=True</expect></criterion>
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

<!-- AMENDMENT 2 (issuer 2.0.0_SA_COO~M1, 2026-10-07 ~23:5xZ): RESUME after run 1 was killed by laptop memory (record
E32_AI_LEG_RUN1_KILLED_STATE_20261007.md @559feeeb5b: chunk 1 only, 187 of 2,291 landed, snapshot intact, nothing rolled back). -->
### AMENDMENT 2 -- resume (run 2)

1. Same head, same ledger entry `secclass-e32-ai-leg-i-20261007` (still OPEN). Log the kill and the resume in it.
2. Dry run first. Its INFO lines must read `direct_keys=0`, `ai_keys` = 2,291 minus the keys landed so far (2,104 at 23:55Z), and
   `to_model` equal to that `ai_keys`. Any other count is a STOP and a report.
3. The act runs with a NEW snapshot path: `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_AI_SNAPSHOT_RUN2_20261007.json`.
   The writer refuses an existing path. Run 1's snapshot stays the rollback input for the whole act: it holds every key that existed
   before any AI put, and the rollback deletes only this act's updated_by values.
4. To lower the cost of another kill, use `--chunk 100`. Each chunk is classified, put and listed before the next starts.
5. Completeness at close, beside AC1: run 1's sent keys plus run 2's `ai_to_model` equal 2,291. Each key is either landed (AC1
   `landed`) or named on an `UNRESOLVED` line in the run logs. Paste both counts into the ledger close.

### AMENDMENT 3 -- executor dell1 0.7.0_AE_CloudOps~SD, gated on the Dell key grant (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~00:4xZ)

Andrew-direct ~00:0xZ: "the whole point of the dell boxes is to run the heavy jobs there". Laptop CTO msg 106657 and CTO~DELL1 amend
914acafe20 move this act to a dell1 seat. GATE: start only after the Dell group can read astn/kimi/api-key. The grant cell runs at laptop
COO~C, and step 0's own secret read is the proof. Until then this order is pending and makes no model call.
Everything else is unchanged: the halves, the head (a dell1 checkout carrying run-e32 r5 or later), the bound, the chunking, the rollback
input, and the completeness at close. TO-AI-e32 continues ledger entry secclass-e32-ai-leg-i-20261007 (run 1 by laptop ~SC: 187 of
2,291). Add a "run 2 on dell1 ~SD" line to it; do not open a second entry. TO-AI-e49 opens its own entry, and only after TO-AI-e32 is complete.

### AMENDMENT 4 -- the run-1 snapshot is ~SC's preserved copy (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~01:4xZ; laptop CTO msg 106689)

Run 1's snapshot was written on the laptop, so the path E32_AI_SNAPSHOT_20261007.json named above does not exist on dell1. Its only true
copy is org/tier2_senior/0.7.0_AE_CloudOps~SC/deliverables/E32_AI_SNAPSHOT_20261007.RUN1_PRESERVED_COPY.json (origin CLOUD @2357504c40): 219,994 bytes, sha256 starting 5fd655e06f0b4a0e, 8,968 keys, taken 2026-10-07T21:26:24Z.
Read by the issuer on dell1 CLOUD at 01:4xZ.
- It is the rollback input for the whole act: --rollback --snapshot <that path>. Verify its sha256 prefix before any rollback.
- AC1 now reads it (the invocation above is re-pointed).
- Do NOT regenerate a run-1 snapshot on dell1. It would hold 9,155 keys and roll back nothing.
- Run 2 still writes its own new snapshot (amendment 2), and that one is never the rollback input.

### AMENDMENT (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~01:5xZ) -- seat-gate condition, per 1.0.0_SA_CTO~DELL1 ADDENDUM 1 @0d520d9d70 (row S68)

Before ANY write:
- Run the deploy tool's --dry-seat-gates (or an equivalent read-only gate pass).
- Any verdict=STOP, in any gate mode, or any target that this seat's principal has not been MEASURED able to write, means the act does
  not start. Report the action and resource the same hour.
- An act with more than one write target proves write access on EVERY target before the first write.
This does not change the halves; it is a precondition the CTO added to every act it signed.

### AMENDMENT 5 -- S66 verdict and the first-secret-read report (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~07:0xZ)

1. S66 (CTO round-12 addendum 1 @e5befb00f1 item 1): the close check is `R12_CHECKS/ai_leg_verify.py` at @cedc99ac58 or later. It
   reads ok only when landed + refused == planned. A partial leg reads ok=False, and that is not a pass.
2. Laptop 1.0.0_SA_CTO msg 106758 rule (2), relayed in 0.0.0_AB_MSTR~DELL1 msg 827: when the Dell secrets grant applies, report the
   step-0 FIRST read of astn/kimi/api-key to 0.0.0_AB_MSTR~DELL1 like a deploy: the secret name, this order's run, and the UTC time.
   It is reported, not approved. The grant's CTO half is @8c4fe4be88 and the grant is not yet applied.
No gate limb grades an amendment to an existing order.

### AMENDMENT 6 -- run 3 on dell1 under an outside wall-clock bound (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~13:1xZ; answers ~SD msg 894)

Run 2 hung for 38 min on its first vendor call and was killed at 13:04Z with ZERO rows landed. The secret read works, so this is not
authorization. `_shared/etf_classification_model.py` `default_send` does pass `urlopen(timeout=90)`, but that bounds each socket
operation and not the whole call, so a half-open or trickling response can stall past it. The run stays on dell1 (Andrew: the Dells
are the work horses), as RUN3 with its own snapshot path:
1. PROBE: one key, `--chunk 1`, under an outside `timeout 300`. If it does not print its chunk line, STOP: no second probe, no rollback
   needed, and report the probe's outcome with its socket state. The seat question then goes to 1.0.0_SA_CTO~DELL1.
2. If the probe lands, run the remainder with `--chunk 25`, under an outside watchdog that kills the run when no chunk line arrives for
   10 minutes. Then resume RUN3: the executor plans only keys still absent, so a resume is safe, and run 1 already resumed this way.
3. Every other condition is unchanged: the pre-write conditions, the seat-gate dry pass, the run-1 rollback input from amendment 4,
   the first-read report from amendment 5, and the close check `ai_leg_verify.py` (landed + refused == planned).
No gate limb grades an amendment to an existing order.

### AMENDMENT 7 -- throughput: --workers 4, a fresh snapshot per invocation, transport refusals re-planned (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~13:2xZ; answers ~SD msg 915)

The probe landed (vendor reachable; 2 keys written, model rows 200 -> 202, landed_outside_contract=0). The blocker is the rate: 30.1 s
per key, so the 2,102 remaining keys take about 17.6 h serially.
1. `--workers 4` (classify_many max_workers=4): about 4.4 h, and vendor concurrency stays moderate. Do not raise it without a new ruling.
   If the vendor answers rate-limited (HTTP 429) or repeated transport failures appear, drop to `--workers 2` and report.
2. `--chunk 25` under the 10-minute no-progress watchdog, resumed as amendment 6 says.
3. SNAPSHOT PATH: each invocation writes its own fresh snapshot, named `E32_AI_SNAPSHOT_20261008.RUN3_<HHMM>Z.json` with the launch
   time in UTC. An invocation's own snapshot is never the rollback input; the rollback input stays ~SC's preserved run-1 copy (amendment 4).
4. A refusal whose reason is a transport or vendor failure (timeout, HTTP error, rate limit, empty or malformed body) is NOT a final
   refusal. Those keys stay absent and are re-planned by the next resume. The close check counts as `refused` only model-stated
   refusals (out-of-vocabulary, low confidence under the contract). Report the refusal reasons by count at close.
No gate limb grades an amendment to an existing order.

### AMENDMENT -- round tag (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~14:3xZ; 1.0.0_SA_CTO~DELL1 msg 961, from 3.0.0_SA_CVO msg 960)

This order carried no <round> tag, so surprise-row-gate.py (TO_ROUND_RE, :1246; the count at :1276-1279) counted it against every
round's slug. It belongs to round 11 (decomp_ref DECOMP_R11.md), so <round>11</round> is added to its metadata. No other field changes.
Gate limb: none grades a metadata tag on an existing order; the surprise-row-gate reads it at the next slug.

### AMENDMENT 8 -- re-plan ONLY the 14 transport keys, through a subset set file (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~17:4xZ; answers ~SD msg 1014)

The 1326Z window closed EXACT at 2,291: 1,512 landed + 765 model-stated refused + 14 transport (KIMI_TIMEOUT). The runner plans on
absence, so a plain resume plans 779 keys (765 already answered + the 14). Do NOT re-send the 765.
1. From the preserved logs, take the 14 keys whose UNRESOLVED reason is a transport failure (the same set `ai_leg_verify.py
   --unresolved-log` counts as non-final). Write `E32_TRANSPORT14_SET_20261008.tsv` beside the RUN3 snapshots: the header plus the rows of
   `OLD_LIST_RECLASSIFY_SET_20261007.tsv` whose `shared_key` is one of the 14, byte-for-byte, no other rows. It is a subset of the signed
   set, so the signed halves still cover it.
2. Dry run with `--set <that file>`: it must read ai_keys=14 and direct=0. Any other count: stop and report, no write.
3. Write with `--set <that file> --workers 2 --chunk 25`, a fresh `E32_AI_SNAPSHOT_20261008.RUN4_<HHMM>Z.json`, same half and watchdog.
4. Close: 2,291 = landed + model-stated refused + transport, with the transport count from this window. A key that times out again
   stays transport; report it, do not loop.
The rollback input stays ~SC's preserved run-1 copy over the full set (amendment 4). No gate limb grades an amendment to an existing order.

### AMENDMENT 9 -- the last transport key, and the set name (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~18:0xZ; answers ~SD msg 1022)

RUN4 closed EXACT: 1,519 landed + 771 model-stated refused + 1 transport (NAME::BDPR3C6C, two timeouts) = 2,291.
1. SET NAME CORRECTED: amendment 8 step 1 named `OLD_LIST_RECLASSIFY_SET_20261007.tsv`; the order's set is
   `OLD_LIST_RECLASSIFY_SET_V3_20261007.tsv` (line 35). ~SD's subset cut from the V3 set is the correct one and stands.
2. ONE final attempt on NAME::BDPR3C6C: a 1-key subset of the V3 set (that key's rows only; dry run ai_keys=1), `--workers 1`, a fresh
   `RUN5_<HHMM>Z` snapshot. No further attempt after it, whatever it returns.
3. AC1 expectation, amended: `AI-LEG-VERIFY act=e32 ok=True`, OR `ok=False` whose ONLY problem is `refused_transport=1` on
   NAME::BDPR3C6C after step 2, with planned=2291 EXACT, problems=0 and multi_asset=0. That key then stays absent and is served by the
   fallback layers; it is recorded as transport-terminal in the close.
Then flip the order. No gate limb grades an amendment to an existing order.

### AMENDMENT 10 -- the face names the decomp that DECLARES the cell (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~18:2xZ; answers ~SD msg 1038, row D1-S10)

<decomp_ref> named DECOMP_R11 (the round that released the cells), whose id space is SC-e-65/66, so no proof-of-spec instance could join.
Shape (i) of row D1-S10: <decomp_doc> now DECOMP_R8.md, which declares SC-e-32, and <owned_cells> narrows to SC-e-32, the only cell
AC1 grades. SC-e-50 (DECOMP_R9, the census and set refresh) is not owned by this order; its output is the V3 set this order consumed.
<round>11</round> stays. Gate limb: to-pipeline-gate layer 1 grades the proof-of-spec instance at the flip; none grades this amendment.
