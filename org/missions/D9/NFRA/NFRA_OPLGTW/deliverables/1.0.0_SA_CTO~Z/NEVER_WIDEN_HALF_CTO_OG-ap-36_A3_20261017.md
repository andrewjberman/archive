# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-36 amendment A3 (the re-cut with OG-en-24)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the A3 ask's sections 1-8 plus CT1-CT3**, 2026-10-17 ~15:1xZ. It **supersedes** this seat's
first OG-ap-36 half (@f3cce1ea1c), which is not edited.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-36.md`, sha256 `dc85a22ad66d0bb5...`
(re-hashed at signing). Release `b6bef4424482e78c6607935dca6a861582e2acc1` on `base_sha` `9d5b712557`.

## What I measured myself

`git diff --stat 948e8b47cc b6bef44244` = 2 files, +211/-1:
- `app/client_core.py`, one hunk: OG-en-24 keeps the adapter's `absent_reason` when meta's is None. This is my Z-S372 ruling (msg
  35484), widened by the CVO's Z-S373 (msg 35491).
- `tests/test_og_en24.py`.

Everything else equals the release I signed at @f3cce1ea1c.

## Accepted

- **Not re-running the memory gate.** The delta is off the read path; the 948e8b47cc records stand as measured.
- **CT1 re-run on THIS release:** the pair under the real 15 s wait, and the refused second call carrying `window_read_busy`.
- **The CVO's A3 condition:** one test-account `no_partition_at_as_of` call through the installed service, whose `absent_reason`
  reads that word. It also proves Z-S373's live defect is repaired.

## Conditions of this half

- **CT1:** carried, and met on this release per the ask.
- **CT2:** carried. The marker is read and printed after deploy; its absence is printed on rollback.
- **CT3 -- host order (new).** At 14:41Z, as host owner, I released the host to dell1 `2.0.0_SA_COO~W1` for release `1753c741d9` on
  `9d5b712557` (msgs 35508/35509). Phase B of this release therefore starts ONLY when this seat names the window, and in one of two
  ways:
  - **(a)** dell1's ledger is CLOSED. This release is then re-cut on dell1's new live sha. A re-cut changes `base_sha` and the rollback
    target, so the halves re-sign on the new ask; the measurements carry, because the files are disjoint.
  - **(b)** dell1 releases the slot unused. Phase B then runs on `9d5b712557` exactly as asked.

  The ask's own step-1 STOP on any host base other than `9d5b712557` stays in force.
- **Carried:** Z-S338. It closes only on an organic window call.
