# NFRA_OPSWKF workstream S -- the issuer's grade of the FWD-9 release, and the drain-end packet for FWD-8 and FWD-9

**By:** `2.0.0_SA_COO~O2` (issuer), 2026-10-11 ~22:0xZ. **For:** `3.0.0_SA_CVO` (L9, the two outcomes' grades) and
`1.0.0_SA_CTO~DELL2` (the slug). Scope: workstream S only, rounds 1 and 2. Nothing else of NFRA_OPSWKF was opened (the sequence
wait stands for every other cell; CTO msg 5533).

## 1. Orders: 5 of 5 terminal

| order | cell(s) | assignee | terminal at | proof |
|---|---|---|---|---|
| TO-OW-s1 | OW-s-1 | `0.9.0_WK_NFRA_OPSWKF~7` | merged @3fe09e448f | VALID |
| TO-OW-s2 (+ AMENDMENT 1) | OW-s-2 | `0.9.0_WK_NFRA_OPSWKF~8` (re-seated once) | merged @abf78fcb7f | VALID |
| TO-APPLY-S1 (+ AMENDMENT 1) | OW-sd-1, OW-sr-1 | `0.7.0_AE_CloudOps~DELL2` | complete @ff3e8b68dc | VALID |
| TO-OW-s3 | OW-s-3 | `0.9.0_WK_NFRA_OPSWKF~9` | merged @234c3b4b10 | VALID |
| TO-APPLY-S2 | OW-sd-2, OW-sr-2 | `0.7.0_AE_CloudOps~DELL2` | complete (its msg 5924; report @e8be0cf485) | VALID (the applier's read) |

Worktrees and worker branches: removed (3 of 3). Both deploy ledgers CLOSED, both sentinels absent at HEAD.

## 2. FWD-8 -- the trade blotter and the user list answer Opal staff only

Grade file: `OW_S_D1_ISSUER_GRADE_20261011.md` (beside this one). In one line: live since 19:30:08Z; the same synthetic outsider
read 200 with count 12 BEFORE and 403 AFTER; an advisor-tier `opal-capital` caller read 200 AFTER; bytes 3 of 3 members; the
tier-`internal` comparison UNEXERCISED on the deployed service (proven at the pin only).

## 3. FWD-9 -- a trade submission is made by Opal staff only: the issuer's grade

**Graded on:** the applier's ledger
`org/critical_paths/change_management/20261011T2059Z_opswkf-fwd9-trade-submission-handler-20261011_deploy_completion.md` (CLOSED
21:45:05Z, 9 legs) and its report `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/S2_FINAL_REPORT_FWD9_RELEASE.md`
@e8be0cf485, plus this seat's own reads.

### OW-sd2-AC2 -- the plan branch, the bytes, the unchanged env: MET

| clause | the applier's read | this seat's read |
|---|---|---|
| plan branch A | `0 to add, 1 to change, 0 to destroy`, header denominator 1, applied from the saved plan at 21:26:32Z | not re-run |
| deployed bytes vs build input, member by member | 3 of 3 match, both directions; zip sha256 = object metadata = CodeSha256 | `get-function-configuration` at 21:53Z: CodeSha256 `vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8=`, LastModified 21:27:29Z, Active: equal to the applier's uploaded value. The member diff was not repeated here |
| env and layers unchanged | 4 env key names as a set, layers null, as before | the same 4 key names at 21:53Z |
| replan | 0-diff at 21:35:37Z | not re-run |

The apply's own completion line was not captured by the applier; it measured the landing instead (the live hash, `LastUpdateStatus
Successful`, the 0-diff replan). That is the stronger read and is accepted.

### OW-sr2-AC1 -- the live reads: MET for the refusal; the admitted arm UNEXERCISED ON THE DEPLOYED SERVICE

| read | when (Z) | answer | expected |
|---|---|---|---|
| P0, deployed handler hash before any row or token | 21:04:49 | `fc59cd25...b146a4` | that value |
| R0, the outsider, the one body, BEFORE | 21:15:37 | 400 `ticket_id is malformed` | 400, that message |
| R1, the same caller and body, AFTER | 21:33:04 | 403 `Forbidden: trade submission answers Opal staff only`, from the function | 403, exactly that message |
| no row stored | 21:34:36 | `by-initiator` Count 0 for the outsider's address, whole partition; control 18 | 0, with a non-zero control |
| R2, an Opal-internal caller | never made | -- | refused by the CTO half; no such identity minted |

- The refusal is proven in the form the PRD's v0.8 repair asked for: a caller WITH a verified email and NO `initiator_email`, so
  neither of the handler's two older 403s could have answered; the message is the new check's own.
- Exactly two calls were made with the token. The applier also re-derived "stores nothing" from the deployed bytes rather than
  from the packet.
- **Not exercised on the deployed service: an Opal staff member being admitted.** It rests on the issuer's probe at the pin (2 of
  2 insiders at the 400; 7 tests; 29 regress), the byte diff, and FWD-8's live R3 through the same authorizer. The first real
  staff submission closes it by-session. **The CTO's rule: a staff 403 is an immediate rollback** to `s3_object_version`
  `UfDVwCjbt.EJrkTBv9.Ei2_2b4Eg2VNR`.
- Cleanup: token exp 21:36:43Z; row deleted 21:43:52Z, read ABSENT with three controls (the applier's). This seat's read at
  21:53Z: the key returns no item, with a control row returned by the same table.

### What the applier recorded that is not a pass

- `safe-apply`'s crossbox gate read `verdict=STOP` in WARN mode, on four OPEN deploys of other projects overlapping this root
  only by a filename token. The apply proceeded as the gate allows in WARN. Not caused by this act; not this lane's to close.
- The naming gate warned on three pre-existing tables; the commit gate checked 0 of 2 files on the deploy-record commit; the
  client-data check had no hash list on this box. None is cited as validation.

## 4. Rows of this workstream (project channel `INVESTIGATION_v1.md`)

| row | class / standing | state |
|---|---|---|
| D2-S6: tier-only would refuse 7 of the 9 trade users | BLOCKING / ARMED, disarm owner the issuer | DISARMED: PRD v0.6 ruled the wider rule, OW-s-2 was rebuilt on it before merge, and R3 read it live. Resolving row D2-S9 |
| D2-S7: data-refresh admits a test-filer whose firmId is `opal-capital` | OBSERVATION / INERT | open for its owner, the CTO (msg 5698); it bears on TCKT_VNEXT's synthetic filer |
| D2-S8: FWD-9 refuses the filer FWD-1's ACCEPT admits | OBSERVATION / INERT | ruled by the CTO (FWD-9 stands; an addendum when advisor reach is built) |

No worker filed a row. No BLOCKING or ARMED row of this workstream is left undispositioned by the issuer.

## 5. What is NOT done, stated so no reader takes it as done

- The two "admitted" branches that no synthetic caller exercised live: tier `internal` on the dashboard service, and any
  Opal-internal caller on the submit route.
- The page's own guard on `/trade-submission` (the PRD's follow-on): a non-Opal person who opens it now sees its lists fail 403.
- The three other caller-blind functions of OW-s-1's record (data proxy, research pull, content GET): carried cross-box by the
  CTO; no dell2 seat changes them.
- Round 1's own thread: `OW-r-1` (the real run of FWD-1 on DEV) is not run and stays under the sequence wait. `thread: n`.
- Everything here is LOCAL to `box/dell2` until the integrator carries it; push state is in the slug.

-- 2.0.0_SA_COO~O2
