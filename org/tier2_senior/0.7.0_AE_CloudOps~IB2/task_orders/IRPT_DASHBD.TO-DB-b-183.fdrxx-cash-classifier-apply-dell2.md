<task_order>
  <metadata>
    <id>IRPT_DASHBD.TO-DB-b-183.fdrxx-cash-classifier-apply-dell2</id>
    <issued_by>2.0.0_SA_COO~D2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-14</date>
    <status>complete</status>
    <project_code>IRPT_DASHBD</project_code>
  </metadata>
<risk>WORLD</risk>
<round>98</round>
<workstream>B</workstream>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP.md</decomp_doc> section 100 (round 98), issuer cell `DB-b-183`, FWD-8 class label and FWD-21.
<owned_cells>DB-b-183</owned_cells>
</decomp_ref>

  <objective>
    Apply the FDRXX -> CASH classifier release: ONE S3 object, `s3://opal-data-bd/code/gold/lib/etf_classifier.py`, from the live bytes (sha256 `d2e6aa88086ce9741feb3bf4df22b84996d37906730710c9d1fc79029b874250`, S3 version `0jhXHH7axm_H934t5s5gVDVNJ6Y_WqI.`)
    to the committed bytes of `e340e07f4e` (sha256 `e7385264668e9bf746aeab809c8ff0a869f9091685f86751b1679dfc6ddd81ba`, 19,496 bytes), by `.tools/safe-deploy.sh data/black_diamond/scripts/gold/lib/etf_classifier.py`
    (explicit-files mode). You are the applier the pair names (COO half condition 6: an AE seat, not a worker). Nothing served changes by the upload itself.
  </objective>

  <context>
    READ ALL THREE FILES WHOLE BEFORE STEP 0, the files and not this restatement, and say so in the ledger's opening entry:
    - Packet: org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_FDRXX_CASH_CLASSIFIER.md, sha256
      `cfc1dd8d01206badc657bbf17c46653482149c1904b708bd002ba1ff172b1fe6` (re-hash it; any other bytes are not covered: STOP).
    - COO half (SIGNED): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_FDRXX_CASH_CLASSIFIER_COO_HALF.md (its section 6 is the seven conditions; they are your steps below).
    - CTO half (SIGNED @d3b576bb67): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_FDRXX_CASH_CLASSIFIER_CTO_HALF.md. The CTO ACCEPTED the C_06 history discontinuity (past dates stay fixed_income, new dates become cash; the rollback is PARTIAL for C_06) and the silver legacy blend label; CASH_USD is NOT in this release.
    Your model is the REFRESH-style apply orders: org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_DASHBD.TO-DB-b-165.thresholds-file-swap-apply-dell2.md (same ledger and record discipline; this release is an S3 object, no Lambda, no Terraform).
    The code is committed and tested: `data/black_diamond/scripts/gold/lib/etf_classifier.py` at `e340e07f4e`, test file `data/black_diamond/scripts/gold/tests/test_etf_classifier_cash_type.py` (37 pass across the four classifier test files).
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry with `python .tools/deploy_ledger.py open`, slug `bd-gold-etf-classifier-cash-type-20261014`, pinned to the packet's sha256, and COMMIT it at once (the entry and `org/critical_paths/.open_deploys/<slug>.json`), and again after each leg. Legs: L1 git (the pin), L2 s3-prefix and verify (the object and the read-back), and L3, which stays OPEN for the issuer: the first D_04 run after the upload read (COO half condition 7).
    1. BEFORE reads, each printed: (a) the live object by `aws s3 cp` to a scratch file then sha256: MUST equal `d2e6aa88...`, else STOP; `head-object` for its S3 version id (record it as `before.version_id`, and as `rollback_version_id`); `get-bucket-versioning` MUST read `Enabled`. (b) Read EVERY live worktree's `.open_deploys/` (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator; an open entry on the BD gold tree is a STOP (record `open_entries_on_bd_gold_tree`). (c) NOT WHILE A GOLD CHAIN RUN IS IN FLIGHT: read the BD gold chain's running state by its instrument (the state machine or the scheduled run record the packet's section 3 names; name the instrument you used in `chain_in_flight_instrument`), and the schedules' next fires (silver 22:10/22:40 M-F, S3 events on silver/prices, nightly cron(0 23 ? * MON-SAT *)). A run in flight is a STOP; wait for it to end and re-read, do not race it.
    2. Re-hash the packet (`packet_rehashed`); `git show e340e07f4e:data/black_diamond/scripts/gold/lib/etf_classifier.py | sha256sum` MUST equal `e7385264...` (`new_bytes_pin_commit` `e340e07f4e`). The file you upload must be THAT content: round 99 (`DB-b-185`, the CASH_USD cell) changes the same file on a later commit, so the shared tree's file may no longer equal the pin by the time you run. If it differs from `e7385264...`, do NOT upload from it: make a detached worktree at `e340e07f4e` (`git worktree add --detach <path> e340e07f4e`), confirm the file there hashes to `e7385264...`, and run step 3 and step 4's `safe-deploy.sh` from that worktree (explicit file, same command), then remove the worktree. Any other inequality is a STOP. (AMENDMENT 1, issuer 2.0.0_SA_COO~D2, 2026-10-14; no gate limb graded: a modification of an order with no placeholders.)
    3. Tests and an import smoke at the pinned bytes, BEFORE the upload: the four classifier test files plus `test_etf_classifier_cash_type.py`, under `python -I` from files: 37 or more pass, none fail; and an import smoke of the module (`import` only, no AWS call). Record `tests_before_upload` {passed, failed, import_smoke}. Any failure is a STOP.
    4. THE ONE UPLOAD: `.tools/safe-deploy.sh data/black_diamond/scripts/gold/lib/etf_classifier.py` (explicit files; no `--all`, no `main()` upload, no other file). Record `upload` {command (exactly `safe-deploy.sh data/black_diamond/scripts/gold/lib/etf_classifier.py`), rc, readback_ok (the tool's ETag/SHA read-back at `e7385264...`), pipescript_deployed_match (`comp-pipescript deployed` MATCH for this file)}, and `after` {sha256, version_id} read back by your own `aws s3 cp` and `head-object`. A read-back that is not `e7385264...`: ROLL BACK (step 6) and report.
    5. Close L1 and L2 and leave L3 OPEN. Write the record, the proof-of-spec instance, validate it with `python .tools/proof-of-spec-check.py <instance> DB98-1-AC1` BEFORE you flip this order, then report ONCE to `2.0.0_SA_COO~D2`: the before reads, the chain state, the tests, the upload, the read-back, the ledger entry, any row id. The issuer reads the first D_04 run (L3) and closes the ledger.
    6. ROLLBACK (only on a failed read-back or a step-4 error): copy the recorded prior S3 version back onto the same key (`copy-object` with `--copy-source <bucket>/<key>?versionId=<before.version_id>`), read the same sha256 back (`d2e6aa88...`), record `rollback`, close the ledger, report. A rollback needs no further word. Once a consumer has run under the new bytes the rollback is PARTIAL for C_06 (the pair says so): do NOT roll back after a run for that reason alone; report instead.
  </steps>

  <bounds>
    ONE object, ONE release. No full rebuild, no manual `--full`, no `main()` upload, no job or state-machine start, no DynamoDB write, no S3 delete (prior versions stay; the immediate prior version is the rollback target), no other key uploaded, no Terraform, no Lambda update, no IAM or schedule change. No Bloomberg, vendor or Black Diamond API call, no secret read. Deletes are Andrew's. The Cottonwood copy, the partners Lambda's classifier and the Investor Reporting holdings snapshot path are NOT covered by this pair. Any divergence the pair does not name is a STOP and a row (the investigation file below), not a judgment call. Safe-deploy may print a HALT-GATE notice: read each notice, take `HALT_ACK=1` only if none names this object or carries a [STOP].
  </bounds>

  <write_surface>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/bd_gold_classifier_cash/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_DASHBD.TO-DB-b-183.fdrxx-cash-classifier-apply-dell2.md
  </write_surface>

<proof_of_spec>
  <criterion id="DB98-1-AC1" cell_refs="DB-b-183"><invocation>python "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r98/p98_round98.py" . DB98-1-AC1</invocation><expect>DB98-1-AC1 PASS</expect></criterion>
</proof_of_spec>
DB98-1-AC1 -- the classifier release is live as ONE object at the packet's bytes: before and after sha256 and S3 version ids recorded and different, the rollback version recorded, versioning Enabled, the explicit-files safe-deploy call at rc 0 with read-back and deployed MATCH, 37 or more tests passing and an import smoke before the upload, no chain run in flight (instrument named), no open entry on the BD gold tree, the ledger's L1 and L2 closed and L3 open, no rollback, nothing else moved (every not_done count zero), and no served value changed by the upload. The record is `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/bd_gold_classifier_cash/APPLY_RECORD.json` with keys packet_sha256, object, objects_uploaded, bucket_versioning, before {sha256, version_id}, after {sha256, version_id}, rollback_version_id, upload, tests_before_upload, preconditions {chain_in_flight, chain_in_flight_instrument, worktrees_read, open_entries_on_bd_gold_tree, packet_rehashed, new_bytes_pin_commit}, ledger {slug, legs_closed, legs_open}, rollback, not_done {jobs_run, dynamodb_writes, deletes, other_keys_uploaded, terraform_applied, full_rebuild}, served_values_changed_by_the_upload. Base: FAIL (no record). The instance goes at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/bd_gold_classifier_cash/IRPT_DASHBD.TO-DB-b-183.proof_of_spec.json`.

<preflight>
comp-blast: DECLARED-NOT-APPLICABLE the pair's radius names one S3 object; the packet counted what moves (17 canonical rows, a floor of 20 served positions) and the consumers
comp-iam: DECLARED-NOT-APPLICABLE no grant, action or role statement changes; the pair reads none
comp-routes: DECLARED-NOT-APPLICABLE no route
comp-schedule: DECLARED-NOT-APPLICABLE the schedules are unchanged; the first D_04 run after release is the open ledger leg L3
comp-cache: DECLARED-NOT-APPLICABLE no CloudFront or cache surface
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; DB98-1-AC1 base: FAIL as expected (no record), the green arm PASS and the failing arms FAIL on synthetic records
</preflight>

# pipeline-override: an APPLY order to a dell2 cloud-ops seat for one issuer cell (DB-b-183: one S3 object under a signed never-widen pair, applier named by the pair's condition 6); not a worker cell.
</task_order>
