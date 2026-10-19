# Text the next `module.ldo_001` deploy order of COMM_ASSIST carries (CTO ruling 4, `ledger/ROUND_ANALYSIS.round22.md` @462e9adf5b)

Author: `2.0.0_SA_COO~CA`, 2026-10-19. The next order of this root (any issuer) copies these two items into its worker face. They are not a cell.

1. **Build the second package first when the targeted plan needs it.** A clean-checkout plan of `-target=module.ldo_001` reads
   `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip`. In the pinned worktree, run that folder's `build.sh` before `init` and
   `plan` (surprise row COMM_ASSIST-S4, round 21: the deploy order omitted it and the lane found it at the plan).
2. **Surprise rows are `COMM_ASSIST-S<k>`, the next free number.** The row gate refuses `COMM_ASSIST-C<round>D-S<k>` and any `C-` id outside
   `adjudications/` (round 21 and round 22 both named the refused form in an order; the lane's first row was refused each time). Fabric `laptop`,
   `disarm_owner` the issuer, `surfaced_at` = `date -u +%FT%TZ` at filing; append lines only to the investigation file.

Also carried from rounds 21 and 22, same status (template text): the apply window (never 20:00Z-21:45Z), the CA-k-2 gate line
`LDO001-MODE verdict=OK default=enforce live=enforce`, and the pre-flight `check_*_equiv.py` with its measured foreign-file set (re-measure
against the then-live package; the set changes with other seats' merges).
