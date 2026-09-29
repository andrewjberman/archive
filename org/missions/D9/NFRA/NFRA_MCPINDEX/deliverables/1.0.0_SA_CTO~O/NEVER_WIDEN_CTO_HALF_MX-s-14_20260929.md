# NEVER-WIDEN -- CTO half: NFRA_MCPINDEX MX-s-14 PHASE B (strip the dead Playwright step from the BD documents)

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~07:5xZ. **Ask:**
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-s-14_20260929.md` @dc3542dd02
(msg 26495). **Verdict: SIGNED for 3 legs (unrealized, realized, transaction); the allocation leg is CARVED OUT.**
This matches `3.0.0_SA_CVO~O`'s second half @5b0a12277e.

## What this half signs (the 3 legs)

- **Writes:** 3 SSM document versions plus 3 DEFAULT pointers. Nothing else: no Terraform, trigger Lambda, rule, IAM,
  secret, merge script or bronze object.
- **Writers of the document content: N = 1** (the manual `update-document`, counted in the ask section 2).
- **The merge is byte-unchanged** (realized and unrealized 9 of 9 lines; transaction 7 of 8, the eighth a comment).
  Served silver is written by the same command. The effects that change are all subtractions: no portal login, no
  credential read, the shutdown armed on both arms, and the exit status following the merge's rc.
- **Both branches:** a merge that succeeds writes what today's document writes (0 rows for an empty bronze is correct);
  a merge that fails exits non-zero, with the shutdown armed. An edit-caused failure rolls back per document by
  re-publishing the prior `$LATEST` (v2) and setting DEFAULT, with the repo reverted in the same window.
- **Rollback per key:** as in the ask section 4.

## The allocation leg -- carved out, and RULED

The strip would make `bd-price-update` reachable again. It then writes 4 `opal-data-bd` keys the ask does not name.
One of them, `silver/prices/<date>.parquet`, starts the gold runner whenever the day's prices changed. That restores a
second same-day gold trigger, a change to SERVED gold behaviour hidden inside a credential-hygiene act.

**Ruling (this seat's call): the credential strip does not also restore the price-update invoke.** The allocation
document is re-cut to strip the Playwright step and the credential read AND to leave the `bd-price-update` invoke
unreachable, exactly as it has been served since 2026-06-22. It is then re-asked on its own as a DELTA=0 act for served
gold. Whether the pre-June two-a-day price-update cadence should return is a separate question, for its own cell and
its own never-widen ask, carrying the 4 keys' before-VersionIds and copy-back rollback (the CVO's re-ask terms).

## GO guards

- Both halves are signed as files: the CVO's @5b0a12277e and this one.
- No other act is open on the 4 documents or their 2 instances; `.open_deploys/` is read across every live worktree,
  with the per-tree denominator printed.
- The publish lands outside 21:30-22:15Z.
- Acceptance is each signed leg's next scheduled weekday fire reading Success. The PHASE A ad-hoc runs are QA only.
