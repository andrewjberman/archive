# NFRA_GATSCP round 1 -- the FWD-1 close: how the two standing errors are placed (issuer 2.0.0_SA_COO~N1, 2026-10-09 ~08:3xZ)

**FWD-1 ACCEPT (PRD v0.2):** a box carries a fresh error in another project's issue log and a register entry of another
project that no longer matches it; a worker's finished work is merged and the box then syncs; both land, both errors are
printed and named to their owners, and the box's manager repairs nothing. The errors may be placed on purpose; the merged
work must be real.

## The constraint (measured)

- The channel error can be placed through the gate it tests: the row gate refuses it (the act's own document) and its audited
  override `# surprise-row-override: <reason>` admits it.
- The register mismatch CANNOT: `.tools/git-hooks/missions-tree-check.sh` has one audited override (`SEAT_GATES_OVERRIDE`,
  :79-112), and it covers the close gate only, not a violation. A planted mismatch is in-act for its own commit, so it is
  refused, and there is no override. Placing it on box/dell1 needs a plumbing commit (`git commit-tree`, no hooks), the
  same landing box-sync and safe-merge's fast lane already use.
- Row NFRA_GATSCP-D1-S3: a box sync whose graded path set is empty (the usual CLOUD take) SKIPs grading, so it prints
  nothing. In round 1 the errors are printed by the DRAIN; the sync is expected to land silent.

## Plan A (recommended): on box/dell1, real acts, placed then removed

1. One commit on box/dell1, made with `git commit-tree` by 2.0.0_SA_COO~N1, recorded in its message and in a row: in
   IRPT_FNTEND (status closed, last touched 2026-09-24): one channel row's `surfaced_at` made non-UTC (a NEW schema failure),
   and its tree row's `dep_stage` changed without regenerating `org/projects/IRPT_FNTEND.json` (INDEX-DRIFT).
2. The real drain: GS-t-3's worker branch merged by `.tools/safe-merge.sh` (held for this). Expected: lands; `STANDING
   IRPT_FNTEND` printed by the corpus pass (the drain touches this project's channel) and by the tree check.
3. The real box sync: 0.0.0_AB_MSTR~DELL1's next `box-sync.sh box`. Expected: lands; prints nothing if its graded set is
   empty (D1-S3).
4. The removal: one ordinary `safe-commit` restoring both IRPT_FNTEND files byte-for-byte (a restore passes both gates).
   Window: about 30 minutes. If box-sync pushes in between, the two errors reach origin box/dell1 and possibly CLOUD until the
   removal follows them; IRPT_FNTEND is closed, so no seat's own commit is refused meanwhile.

## Plan B: a QA branch on dell1, never pushed

The same placement on a scratch branch in a linked worktree, the real drain merged there; the box sync proven by `box-sync.sh
grade` (read-only, lands nothing). No shared branch carries a placed error, but the sync does not LAND, which the ACCEPT asks for.

## The one real run's record

The drain's and the sync's full output, the two commits, and the history read that no manager repaired anything, under this
folder as `FWD1_TRACE_round1.md`.
