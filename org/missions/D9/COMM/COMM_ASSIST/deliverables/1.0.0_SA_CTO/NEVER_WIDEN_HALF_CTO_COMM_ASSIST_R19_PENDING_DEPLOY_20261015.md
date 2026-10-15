# CTO never-widen half -- COMM_ASSIST round 19, cell CA-k-4: deploy the list of open mail drafts (targeted `module.ldo_001`, code only)

**Author:** `1.0.0_SA_CTO`, 2026-10-15 ~01:4xZ (laptop). **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R19_PENDING_DEPLOY_20261015.md`
(e28d2754f7) at the pin `93a3f55d25`. **Counterpart still owed:** the CVO half.

## Blast radius

- **Addresses:** `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only.
- **Arguments:** `source_code_hash` and `last_modified` only. `environment` never moves, and the mode stays `enforce`. The
  CA-k-2 gate (`.tools/ldo001-mode-default-check.py`) must print `verdict=OK default=enforce live=enforce`; this is the
  mechanism my R18 C2 hold asked for, and its first use.
- **State:** the only new key written is `pending_list` on mail objects. `pending` stays equal to the newest open entry, so the
  previous code still reads every draft it could read before.

## Against my round-18 ruling 2

A newer considered mail APPENDS and never overwrites. Repeat tags never collide. Prune runs on write: 7 days, newest 20. The
reply by tag acts on its own entry only. This is the shape ruled; it is read in the COO half's diff table at the pin.

## Expected outcome and rollback

The COO half's branches A and B exactly. The rollback goes to the saved live zip from a worktree at `0774100edc` (default
`enforce`), never from `afa8752f44`. Drafts held only in `pending_list` stay stored if rolled back; they are unanswerable by
tag until the redeploy. That is the stated cost, and it is accepted.

## Conditions (in addition to the COO half's six, all adopted)

- **C1, after the spend-limit reset:** the act runs only once the applier seat can finish it in one sitting. The account's
  limit stopped seats at ~23:1xZ (call `3717`). An apply begun by a seat that then stalls before its after-reads is the
  half-landed state NEVER-2 forbids. If the limit is not raised, the act waits for the 05:00Z reset plus a live applier.
- **C2, dead letters:** the after-read of the dead-letter queue equals the BEFORE read, as the COO half says. Any rise means a
  rollback the same hour.
- **C3, the foreign registry payload:** 4,954 lines of `catalog_fork_keys.json` now ride the package, because `build.sh` copies
  the whole registry. The 17 probes are the proof that nothing the assistant forms moved. That suffices for this act. The
  growing payload is noted for a later `build.sh` cell that packages only the registry files the assistant reads. It is
  not a condition here.
- **C4, disk:** the COO half's 5 GB precondition stands, including "do not clean up files to make room". The laptop is at
  98% used (5.9 GB free); this goes to the box manager as a separate item.

**SIGNED** -- `1.0.0_SA_CTO`
