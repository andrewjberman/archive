# Reboot brief -- 0.4.0_DS_ClientPlatform~S -- 2026-10-01

Order: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261001_161xZ_DEVICE_SLOW_REBOOT_BRIEFS_AND_RESPAWN.md`
@`223a35bb6b`. Written for a successor that remembers nothing.

## 1. Identity

- Serial `0.4.0_DS_ClientPlatform~S`. Base folder `org/tier2_senior/0.4.0_DS_ClientPlatform/`
  (the lane folder `~S/` holds only `deliverables/`; logs go in the BASE folder's `logs/`).
- Project: `IRPT_DASHBD` workstream B round 1, issued by `2.0.0_SA_COO~P`.
- No FAST lease held. No cron armed. Event-driven via the inbox Monitor only.

## 2. Where the work stands

- **`IRPT_DASHBD.TO-DB-b-1` -- COMPLETE.** The 49 Financial reporting adapter emits gold
  `account_return_daily`: 559 date partitions, 1,105 account-days, six accounts,
  2024-07-08..2026-09-28, at
  `s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/`. Last landed:
  status flip @`c1c399af74`. DB-1-AC1/AC2/AC3 PASS; proof-of-spec VALID.
  Waits on nothing.
- **`IRPT_DASHBD.TO-DB-b-3` -- COMPLETE.** Tie-out against Black Diamond's own returns; the one
  gold write (`dim_return_method/method_version=1`, `tieout_tolerance_proposed` 0.037,
  `flow_convention` unchanged at END) landed 15:12:57Z. Flip @`38f828d708`. DB-3-AC1/AC2 PASS;
  proof-of-spec VALID. Waits on nothing.
- **Last commit of this seat: `e1b160d340`** -- the producer version that actually wrote the
  served method row, found uncommitted while writing this brief.
- Both task orders are terminal. **This seat holds no open task order.**

## 3. Open acts that must survive the reboot

- **Ledgers: NONE OPEN.** Both this seat's entries are CLOSED with their sentinels absent and
  their deletions committed:
  - `org/critical_paths/change_management/20261001T0904Z_irpt-dashbd-account-return-daily-49f-r1-20260930_deploy_completion.md`
    -- CLOSED 20261001T120358Z, 4 of 4 legs proven, nothing stranded.
  - `org/critical_paths/change_management/20261001T1504Z_irpt-dashbd-method-row-tieout-r1-20260930_deploy_completion.md`
    -- CLOSED 20261001T151522Z, 1 of 1 leg proven, nothing stranded.
  - Every other OPEN or HELD-STALE entry the ledger check prints belongs to another seat. Do not
    act on them.
- **Worktrees: NONE.** This seat worked in the shared tree throughout. `wk-irpt-dashbd-1` on the
  Desktop belongs to `0.9.0_WK_IRPT_DASHBD~1`, not to this seat.
- **Uncommitted work: NONE.** `git status --porcelain` is empty across
  `data/assets/scripts/gold/irpt_reporting/`, this seat's deliverables, `org/standards/`, and the
  `IRPT_DASHBD` tree. It was NOT empty when this brief was started -- see section 6.
- **Clocks: none.** No scheduled run belongs to this seat. The emitted gold is a round-1 QA
  thread, produced ad hoc; the all-accounts and scheduled production run is a later round.
- Nothing is half-landed. Both S3 write surfaces were read back after writing and proven under
  their ledger legs.

## 4. Owed

- **Owed TO this seat: nothing.** The last two conditions it named were met --
  `2.0.0_SA_COO~P` landed the account_return_daily contract 0.2.0 @`6a23aee53d` and the
  dim_return_method contract 0.2.0 @`9ff75db8f2`, each after independently recomputing the schema
  hash from the landed parquet rather than taking this seat's value.
- **Owed BY this seat: this brief and its path to `1.0.0_SA_CTO`** (msg 103898, relayed as msg
  103900). Nothing else.
- **Pending at `1.0.0_SA_CTO`** (routed, not owed by this seat): rows `IRPT_DASHBD-S9` and
  `IRPT_DASHBD-S10`, `disarm_owner 1.0.0_SA_CTO` -- the 3.70% tie-out tolerance and the
  flow-timing convention. The recommendation on both is AGAINST adopting them as measured; the
  rows carry the reasons.
- **Pending at Andrew** (one call, nothing blocked by it): FWD-8's own ACCEPT clause reserves to
  him whether a figure is defensible when a third of its served days carry no independent
  cross-check. Raised 2026-10-01 ~16:0xZ via `/open-calls`. No execution waits on it; the
  outcome's grade does.
- **No signed halves outstanding.** This seat signs none.

## 5. Relaunch

- **RESPAWN: NO, unless the CTO rules on rows S9/S10.** Both task orders are terminal, no ledger
  is open, nothing is owed to another seat, and the only follow-on work (re-running the tie-out on
  comparable day sets) is gated on a ruling that has not arrived. A seat respawned before that
  ruling has nothing it can advance.
- If respawned, the first three acts in order:
  1. `/watcher` once, then read the inbox and the delivery ledger for any ruling on S9/S10.
  2. Read this brief, then
     `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.md`
     -- one page, and it states what the tie-out does NOT establish.
  3. Only on a ruling: re-run the tie-out over comparable day sets, or take whatever the ruling
     names. Start no vendor call without Andrew's word for that call.
- `--say` hint: *"Read your reboot brief at
  org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/REBOOT_BRIEF_20261001_0.4.0_DS_ClientPlatform_S.md
  and then your inbox."*

## 6. Not done and not known

- **Found while writing this brief:** the producer was MODIFIED and uncommitted -- the branch
  placement that made the method-row write skip the inception scan. That is the version that
  actually wrote the served row, so an uncommitted tree plus a reset would have left the repo
  carrying a producer different from the one that produced served data. Committed at `e1b160d340`.
  The omission was mine; measuring section 3 is what caught it.
- **A residual I measured but did not explain: 1,498.38 dollars.** On account 0027265115 over
  2026-03-16..2026-08-28, Black Diamond's `netAdditions` is 1,044,598.9077 and this engine's net
  external flow is 1,043,100.5277. The same test on account 0076459710 matches to 0.0000, so the
  method is right and this one account has something unaccounted -- most likely an in-kind leg
  valued differently or a leg classed internal here that the vendor counts as an addition. Not a
  fee issue: the fee matches to the cent on both accounts.
- **Monthly and quarterly agreement against the vendor is NOT measured and cannot be from the
  landed responses.** Their endpoint returns period returns only -- no daily series -- and their
  data ends 2026-08-28 while the only Opal month that links with no withheld day is 2026-09.
  There is zero overlap. Answering it needs a vendor pull with month-end period ends, which is a
  vendor call and was not made.
- **What I believe but did not measure:** that the eight repairs made today are the whole set of
  arithmetic defects. Twelve review findings were triaged and five became rulings or amendments;
  nothing says a thirteenth does not exist.
