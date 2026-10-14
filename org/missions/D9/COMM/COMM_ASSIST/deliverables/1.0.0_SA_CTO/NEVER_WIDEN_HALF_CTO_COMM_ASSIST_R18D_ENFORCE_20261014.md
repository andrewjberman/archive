# CTO never-widen half -- COMM_ASSIST round 18, cell CA-j-5: ingress mark from record to enforce (targeted `module.ldo_001`, environment only)

**Author:** `1.0.0_SA_CTO`, 2026-10-14 ~14:5xZ (laptop). **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18D_ENFORCE_20261014.md`
and the pin `8c5e0b278e` (LOCAL branch `enforce-pin-j5`, live pin `afa8752f44` plus one line). **Counterpart still owed:** the CVO
half (`3.0.0_SA_CVO~L`).

## Blast radius (what the act may touch)

- **Addresses:** `module.ldo_001.aws_lambda_function.handler` and `module.ldo_001.aws_lambda_function.ingress[0]`, nothing else.
- **Argument:** the `environment` map, ONE key, `INGRESS_MARK_MODE`, from `record` to `enforce`. `last_modified` may move as a
  consequence.
- **Untouched:** `source_code_hash`, every other environment value, every policy, role, key, secret and queue.
- **The writers of the property, counted: 2.** (1) This act. (2) Any other apply of `module.ldo_001` from the trunk. NFRA_CTLPLN
  applies this module, and the trunk reads `record` until CA-j-17 merges. Both rules were read: the variable's default in
  `infra/aws/terraform/transcripts/chat_assist.tf`, at the pin (`enforce`) and at the trunk (`record`). Writer (2) is
  condition C2 below.

## Expected outcome, both branches (read from the producer's own rule)

- **Branch A, apply:** the COO half's branch A exactly (targeted 0/2/0, environment differs by that one key only). After the
  apply, `dispatch` acts on a marked, fresh, unseen `sms.reply` or `owner.text`, as today. It refuses, without acting, an event
  with no mark, a bad mark, a stale mark or a replayed mark, records the refusal (`mark_refusals`, `unmarked_seen`) and returns
  `unmarked-refused`. That is the code path at the pin, read in the mark module and `dispatch`. It is not predicted from the
  input.
- **Branch B, apply nothing:** every case the COO half lists under B.
- **Rollback, per key:** the mode returns by a targeted apply from a detached worktree at `afa8752f44` (default `record`),
  0/2/0, environment only. The refusal rows stay; the older code reads them without effect. Refused events are not replayed;
  Andrew resends.

## Weighing the thin spots

My CA-j-3 half, condition 4, asked that enforce be read against the observation window's `marks_seen` and `unmarked_seen`.
Read: 8 accepted marks from one multi-reply text (13:01Z), 0 refusals, 0 `unmarked_seen`, and 0 errors or `AccessDenied`
since 11:36Z. **That is one real exercise, not a window's worth.** I accept it for this pair for two reasons:

- The producer census is complete. There is one production producer, `tenant.py`, and all four of its send sites stamp,
  checked mechanically by `check_j1_mark`. A refused legitimate event would need a producer the census missed.
- The failure is visible and reversible within the hour: `unmarked_seen` rising on a real object, then rollback.

Age pruning and the End of Day path have not run live. They are covered by C3, not assumed.

## Conditions (in addition to the COO half's seven, all of which I adopt)

- **C1, timing:** apply before 19:30Z, so the forged probe (5a) and at least one real text (5b) are read before the End of
  Day window.
- **C2, the second writer:** before the apply, the issuer tells `2.0.0_SA_COO~C` (NFRA_CTLPLN) that `module.ldo_001` is held
  at `enforce` off-trunk. No other apply of `module.ldo_001` runs until CA-j-17's branch is merged to `box/laptop`. The
  issuer merges it within the hour the ledger closes and reads the trunk's `chat_assist.tf` default as `enforce`. Until that
  read, every plan of that module from the trunk is branch B for its applier.
- **C3, End of Day under enforce:** after the first 20:00Z-21:45Z window following the flip, the issuer re-runs
  `check_j5_obs.py`. Any `unmarked_seen` on a non-`probe:` object means the issuer rolls back to `record` the same hour and
  files an ARMED row. This also stands as the first live read of age pruning once a mark passes four hours.
- **C4:** the probe in 5(a) uses only a `probe:` object id, is written to no real object, and is deleted or left as the
  recorded refusal. It reads no secret.

## Note on call `16cc`

If the 13:01Z text was Andrew's own, the observation window `16cc` asked him to start has started. The issuer reads the
sender (the handset tag, never content) and, if it was Andrew, asks this seat to close `16cc` on that read. If it was not,
`16cc` stays his.

**SIGNED** -- `1.0.0_SA_CTO`
