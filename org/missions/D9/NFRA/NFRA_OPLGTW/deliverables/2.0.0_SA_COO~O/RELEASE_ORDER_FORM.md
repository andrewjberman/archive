# NFRA_OPLGTW -- the gateway RELEASE-ORDER FORM (issuer `2.0.0_SA_COO~O`)

The issuer cuts every opal-gateway release order (`OG-rl-*`) to this form. It records the steps rounds 14-17 proved and
two standing rulings:
- the CTO's R16 (CLOUD is the source of record; `ledger/ROUND_ANALYSIS.round17.md` s.3);
- R18's acceptance of row Z-W15-S51's remedy.

Sources: the r14-r17 release orders (`OG-rl-4`, `rl-5`, `rl-6`) and their rows.

## Phase A (pre-GO; read-only on the host; no upload)

1. **Live ref.** Confirm the manifest's `deployed_commit` by host md5. A mismatch STOPS.
2. **Release tree.** Cut a worktree on a NEW branch `rel-nfra-oplgtw-r<N>` at the live sha.
   - Carry ONLY the named cells' hunks, and prove each file's hunk set equals the cell's own diff.
   - Commit under R13 (a): the audited `GIT_COMMIT_AUTHOR_OVERRIDE`, a file list within the release set, and the
     audit-log line cited.
3. **Tests** on the release tree, each named file in its own process. Name the baseline failures.
4. **Rollback.** A worktree at the live sha, equal file by file to the live S3 artifact.
5. **BEFORE run.** On the host through the installed engine, with a synthetic principal and an in-memory grant: never a
   real identity, never a state-store write. Remove every host scratch copy.
   - **One host run at a time, each in its own scratch directory (row Z-W28-S9).** Name the scratch per run, for
     example `/tmp/og_<release>_<run id>`. Two runs sharing one scratch directory corrupt each other.
6. **Verify script.** Host `/health`, shipped md5 against the release list, the tool count, the `.env` key NAMES (and
   value hashes when the template changes), the AFTER arms, and the floor checks.
7. **PRE-GO CHECK EXERCISE (R18, row Z-W15-S51).** Run each new or reused criterion script ONCE against the release
   tree before GO.
   - Record its expected-PASS form and ONE negative control.
   - Run it again on any amendment, any `.env`-shape change, or any step-order change.
   - Check every criterion's literal output against the order's `<expect>` with `re.search`. A check whose output
     cannot match its expect is fixed BEFORE GO (rows S38, S42, S50).
7a. **ROUTE INVENTORY (R21, row Z-W22-S10).** A release that ADDS or REMOVES a route runs
    `tests/test_principal_cutover.py`'s ROUTE_CLASS inventory and `tests/test_data_entitlement_guard.py`'s route census
    on the release tree, each in its own process. Both must be green before GO.
8. **ANNOUNCE** with the blast radius, written for three halves: what moves, each property's writers counted, both
   branches, and the rollback per key.

## Phase B (GO only with CTO + COO + CVO halves SIGNED on the release sha)

9. Re-read live; if it moved, re-cut. Open the NEVER-2 ledger, with entry AND sentinel committed before the act.
10. Deploy through `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=<live full sha> HALT_ACK=1`.
    - **Deploy line:** from the release worktree,
      `DEPLOY_BASE_REF=<live full sha> HALT_ACK=1 AGENT_NAME=<worker serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
    - **DEPLOY IDENTITY (R35 part 2, rows Z-W28-S7, Z-S62).** The deploy presents the ISSUER's serial to the halt gate.
      In the deploy shell run `unset OPAL_AGENT_SERIAL`, and create no `org/mcp/sessions/` in the release tree. The gate
      then resolves the session's serial from the shared tree's session file (`org/XXX.md` step A.1, which the issuer
      writes at startup). A `[STOP]` addressed to the issuer halts the deploy. `AGENT_NAME` carries the worker's serial
      for the manifest attribution only.
      - Dry-run the gate read-only before the act: `halt_gate_resolve_serial` then `halt_gate_validate_serial`, rc=0.
      - Since OG-hg-1 (round 24) the gate also finds a worker's own order in the shared root, so a worker serial is
        admitted too. The issuer-serial route stays the form's route until a release has exercised the other.
    - **THE MANIFEST COMMIT (row Z-W28-S8).** The wrapper's own commit of `infra/aws/ec2/EC2_MANIFEST.json` is refused
      by the owned-paths lane gate after the deploy has landed. That is expected. The worker records the manifest by
      hand in its OWN worktree, on its worker branch, in the same commit as the deploy output. The issuer drains that
      branch. The wrapper's uncommitted edit stays in the throwaway release worktree.
11. Run the verify script IMMEDIATELY. On any failure: roll back, re-verify, and close ROLLED BACK.
    - A floor FAIL whose cause is a check constant is NOT a rollback trigger only when the same arm, re-run with the
      corrected constant, PASSes, and the deviation is recorded as a row.
12. Record the manifest by hand. Close the ledger. Run the criteria and check each against its `<expect>`. Write the
    proof. Flip the ONE `<status>` tag.

## Phase D -- DRAIN-BACK (R16)

13. After the post-act read, merge the release branch's gateway files back to CLOUD, so that CLOUD equals live plus the
    LISTED CLOUD-only pending items.
    - This is done through `safe-merge.sh` of a branch carrying exactly the release's files.
    - Record the before and after `git diff --stat <live sha> CLOUD -- infra/aws/ec2/opal-gateway`, which must equal the
      CLOUD-only list.
    - Update the CLOUD-only list (`deliverables/0.9.0_WK_NFRA_OPLGTW~22/LINEAGE_R18.json` from OG-ln-1 on): remove the
      items that shipped.

## Standing rules carried

- Never source `/opt/opal-gateway/.env` (row Z-S32).
- Never write a grant.
- **Operator-command output (row Z-W28-S2).** An order that runs `ops/schwab_entitlement_admin.py` redirects the
  output of `prepare()` and `activate` to the off-repo directory and prints only the operations line. The scope diff
  prints master account ids as dictionary keys. The order also names how it resolves the holder's pk: a read-only scan
  under the caller identity, because the operator role cannot run `dynamodb:Scan`.
- Halves name the blast radius, never the producer's decision.
- An Andrew-scope question (audience, grants) is routed to Andrew, never decided by a half.
