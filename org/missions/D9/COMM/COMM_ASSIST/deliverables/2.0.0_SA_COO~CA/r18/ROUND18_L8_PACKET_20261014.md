# COMM_ASSIST round 18 -- L8 packet (issuer 2.0.0_SA_COO~CA, laptop, 2026-10-14 21:4xZ)

**Reader:** `3.0.0_SA_CVO~L` (L8 compile and the L10 slug). Round 18 = the CTO's round-17 analysis `ledger/ROUND_ANALYSIS.round17.md` (msg 109054) over PRD v0.7, carried through v0.8, v0.9 and v0.10 (FWD-13 added on Andrew's word), decomposition `decompositions/COMM_ASSIST_DECOMP.round18.md` with ten amendments.
`round-close-check --round 18`: orders=14, proofs structurally OK, judgment=0, verdict **MAY-CLOSE** (re-read 21:47Z with all 14 complete). Every order of the round is terminal. This round has no judgment criterion, so there is nothing for L9 to grade; the compile and the slug are the CVO's.

## What the round delivered (all LOCAL on `box/laptop` unless a line says CLOUD; the issuer read each LIVE item itself after the seat or worker reported)

| item | state | read by the issuer |
|---|---|---|
| the SMS ingress mark (W10-S2): `ingress_mark.py`, the dispatch gate with three modes, all four producer sites stamped | merged `0ca94ce0b6` (CA-j-1) | `check_j1_mark` 9/9, flow set green |
| the mark's secret shell, read grant, `INGRESS_MARK_MODE` variable | merged `38ce5a7981` (CA-j-2) | `check_j2_tf` 7/7 |
| deploy 1: the secret (value out of band, never read), the code, `record` mode | ledger `comm-assist-r18-deploy` CLOSED @1daa4a97ce | `check_j3_live` PASS by the issuer; evidence scanned: no secret |
| the key narrowed: a resource policy denying `GetSecretValue` to all but the execution role (CTO call 97c6) | merged `3af44d523b` (CA-j-7); ledger `comm-assist-r18-key-deploy` CLOSED @df7f6f6c55 | `check_j8_live` PASS: role allowed, both Dell users `explicitDeny` by simulation against the live policy |
| the mark valid 4 hours, the single-use record held by age with no count cap, refusals record kind and tag (CTO call 847f; the queue redelivers after 3600 s) | merged `afa8752f44` (CA-j-9); ledger `comm-assist-r18-fresh-deploy` CLOSED @0a79b22d2a | `check_j9_fresh` 7/7, `check_j10_live` PASS |
| the flip to `enforce`: environment only, built package equal to the live one byte for byte, off the trunk until the apply | pin `8c5e0b278e`; applied 15:07:01Z; ledger `comm-assist-r18-enforce-deploy` CLOSED @4dddae3aad; CA-j-17's branch merged `0774100edc` so the trunk equals AWS | `check_j5_live` PASS; REAL RUN (a) `check_j5_forged` ok (a forged unmarked `sms.reply` to a `probe:` object refused, recorded, no side effect); REAL RUN (b) Andrew's real tagged reply at 15:32:43Z accepted and acted on, marks 8 to 9, 0 unmarked |
| the forwarder creates `answers/` and its subfolders (D2-S1) | merged `0f09e35281` (CA-j-4) | `check_j4_dirs` 3/3 |
| FWD-13, the assistant half: a metadata-only mention record and considered-mail log (CTO call 608c) | merged `ca76b8b225` (CA-j-12); deployed (CA-j-14), ledger `comm-assist-r18-records-deploy` CLOSED @025e948c4d | `check_k1_records` 8/8, `check_k3_live` PASS, dead-letter queue 0/0/0 before and after |
| FWD-13, the reader half: `mentions.json` and `mail_log.json` beside `drafts.json` | merged `0ea947e32d` (CA-j-13); picked up on dell2 (CA-j-15, crossbox XB-7d4f closed both halves) | `check_k2_reader` 7/7; the dell2 seat's read of the live folder: six sources, both new files `absent` (nothing recorded yet), clean |
| agentbus item 4 (no unstamped LDO-001 sender) | CLOSED: the first real LDO-001 send after the stamp deploy, the J359 offer at 15:32:58Z, received stamped (MSTR msg 109186) | MSTR's cross-box read |

## Rows

- **ARMED, closed by the issuer's disarm with evidence:** `COMM_ASSIST-W10-S2` (R-12: both real runs above; the key readable only by the execution role). Residual in PRD v0.8: an administrator can rewrite the key's policy, a recorded management write.
- **ARMED, standing:** `COMM_ASSIST-W21-S1`: the commit gate's client-data check cannot run on this box (the hashed account-id list is absent), so EVERY commit from the laptop is unchecked for client account ids. The issuer measured the CA-j-2 commits by hand; the box-level absence stands with the box manager. `COMM_ASSIST-C-S5` is disarmed in the issuer's record (R-8); its channel row closes at your compile.
- **Worker and seat rows, all ruled** in `r18/ISSUER_RULINGS.md` (INERT or resolved). Two were BLOCKING and resolved: W19-S2 (a sibling test outside the grant) and W25-S1, whose defect was the ISSUER's (a check tested by absolute path, so it tested the unpatched reader).
- **Issuer defects named for you in one place:** the H1 check test, the first CA-j-17 pin built on a trunk carrying another project's registry file, the imprecise "one multi-reply text", two ack slips (`r18/ISSUER_RULINGS.md`, last section).

## Not exercised, stated plainly

- **The C3 read (CTO condition C3), read by the issuer at 21:46Z, after the first End of Day window (20:00Z-21:45Z) under `enforce`: CLEAN.** `check_j5_obs`: scanned=747, state_rows=11, marks_ok=10, unmarked=0, no refusal of any reason; the issuer's forged `probe:` row counted apart. The 10th mark is the End of Day object `eod:2026-10-14`, mark time 20:29:42Z, accepted under `enforce` with `unmarked_seen` 0 (a per-object read of the table, mark values not printed). So the End of Day producer ran live under `enforce` and was accepted. Of the 10 marks, 8 are from 13:01Z (record mode, the natural text and its re-sends), one is the 15:32Z tagged reply, one is the End of Day; no rollback to `record` was owed.
- **The live evidence for `enforce` is two real events** (the 15:32Z tagged reply and the 20:29Z End of Day); the 13:01Z natural text ran in `record`. The handler's confirm path (`on_owner_reply`, Andrew's `#1`) has not run live. The age pruning of the single-use record has not run live either: the 13:01Z marks are now more than 8 hours old and still held, because the prune runs on a write to that object and none has touched them since.
- **FWD-13's exercise (CA-j-16)** needs muse's own three pieces (a scheduled read of the folder, an alert ledger, a wake mechanism: Andrew's and muse's to build; the issuer's thread with muse recommends a 5-minute read inside the 30-minute bound) and one real `@mention` and one real C-MAIL mail from Andrew's calls `44eb` and `e435`. No row of either record exists yet on live traffic: a real mail at 15:5xZ was not considered (its body did not name him) and no mention has arrived. The records are exercised by the served-code probe and the unit tests only.
- **FWD-6 and FWD-7's real muse acts** (the one-sitting call `8f2b`) are Andrew's. **FWD-12** waits on a period Andrew names. Kimi keeps drafting until FWD-12 retires it (call 87a2, answered).
- The CVO's carried FWD-11 point: the snippet scrub is a pattern scrub, not a guarantee.

## Enrichment candidates for the CTO's round-19 analysis (this seat's reading; the CTO writes the list)

1. **FWD-13's exercise** and muse's build (the muse side is outside this seat's reach).
2. The mail object holds ONE `pending` draft, so a newer considered mail still REPLACES the older draft in the assistant (the log now shows that it happened; it does not restore the draft). A list of pending mail drafts is the product fix.
3. `CA-j-18`, not cut (no outcome to serve): the stale mail test scripts (4 cases of `test_inbound_mail.py`, 1 arm of `test_inbound_mail_draft.py`; the live mail path works).
4. The standing hazard that NFRA_CTLPLN also applies `module.ldo_001`: the trunk's default must equal AWS. A check that compares the trunk's mode default with the live environment at every deploy would turn the hold I asked for into a mechanism.
5. The box manager's hashed account-id list (W21-S1).
6. FWD-12 after a period Andrew names.
