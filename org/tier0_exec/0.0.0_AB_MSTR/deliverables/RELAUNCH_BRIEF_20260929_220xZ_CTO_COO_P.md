# Relaunch brief -- 1.0.0_SA_CTO and 2.0.0_SA_COO~P, 2026-09-29 ~22:0xZ (by 0.0.0_AB_MSTR)

Both sessions died around 21:35-21:50Z. Andrew presumes memory, not disk. Measured at 21:59Z: RAM 4.5 GB free of 31.7
GB, with WindowsTerminal holding 5.6 GB; C: 18.3 GB free. Your last commits: CTO 3c0958ba3f (21:32Z, MDPF_SECCLASS
coo_lane register); ~P 0dc3bee85e (21:34Z, drive log T21Z). Andrew's order:
`ANDREW_DIRECT_20260929_220xZ_WORKTREE_WIPE_ON_CLOSE_EDICT_AND_CTO_COO_P_RELAUNCH.md`.

## Trunk

- origin/CLOUD is 0c955d5493 (ls-remote). Local CLOUD is 38 ahead and 0 behind; the push waits on Andrew's word.
- In the last push (Andrew "aLL RECS APPROVED", LD-0613 Progress 31):
  - investor-reporting.tar.gz was minted live, ETag 5be5cc50, 19:45Z, with account_masks and ~M's import fix;
  - both restamped pins are live;
  - the S19 laptop prune is done (.git 3.1 -> 1.9 GB; the purged commits are gone).
- Transcripts steps 1 and 3 are on local CLOUD: 73896b6c42 and f13d9e9222 (bucket_provisioned true).
  - 2.0.0_SA_COO~D owes the portal firmDisplayNames restamp.
  - The next push re-deploys the bundle and pins with a comment-only restamp.
- Site Z's push hold is RELEASED for its CLOUD pushes only; its pre-rewrite branches stay merge-barred. Site Z's bus
  consumer looks down; the messages are queued.

## For 1.0.0_SA_CTO

- Your threads at the crash:
  - MDPF_SECCLASS L3/L4: PRD v0.1 is admitted, and the coo_lane is ~M (3c0958ba3f).
  - Canonical security table: DONE WHEN is confirmed by Andrew; the FWD-7/8 backend goes to ~M.
- You own the recurring pre-commit hang (your 103030). It happened twice, both in CVO sessions. MSTR's capture script
  is ready and runs before the next unstick; it writes org/mcp/hook-hang-capture.log.
- Landed: the cleanup-disk.ps1 fix 529f6b4689 (dirty worktrees go to review; no --force) and the naming-gate
  portal fix.
- NEW EDICT to consider for law: see Andrew's order above. When a COO closes an agent, it wipes that agent's worktree
  if everything is committed and landed. MSTR relayed it to the COO lanes; the CLAUDE.md text is yours.
- D10 stays empty by design (Andrew). The platinum/etfs remediation row waits on site Z's 41ba3f747f reaching laptop
  CLOUD, and site Z's push hold is now released.
- Please tell 0.7.0_AE_CloudOps that transcripts step 3 landed (f13d9e9222). MSTR cannot message Tier 2.

## For 2.0.0_SA_COO~P

- Your round-25 workers died with your session. Their worktrees hold UNCOMMITTED work, and nothing has touched it:
  - `C:/Users/AndrewBerman/Desktop/wk-irpt-p-85` [wk-IRPT_BCKEND-85]: 3 uncommitted files;
  - `C:/Users/AndrewBerman/Desktop/wk-irpt-p-86` [wk-IRPT_BCKEND-86]: 1 uncommitted file.
  They are TO-IB-pr-242 and pr-243, issued at 5be1e5e847. Re-spawn or finish them from those worktrees; do not
  re-issue blind.
- `wk-irpt-p-61` [wk-IRPT_BCKEND-61] is 2 ahead of CLOUD with 2 dirty: unlanded work of yours.
- Open deploy ledger: irpt-adapter-holdings-gold-49f-r3-20260929 (D1 closed @d39ef96d92; A1 open for the per-account
  AFTER read and Wednesday's producer fire). Others under org/critical_paths/.open_deploys/ carry your irpt-* names.
- Andrew's edict applies to you from now on: when a worker drains and its worktree is all committed and landed,
  remove the worktree and branch in the same act.
- Earlier today, MSTR force-removed no worktree of yours. irpt-smoke-p-backend-20260923 and irpt-p-publish-20260923
  were removed on Andrew's disk word; both were merged into CLOUD.
