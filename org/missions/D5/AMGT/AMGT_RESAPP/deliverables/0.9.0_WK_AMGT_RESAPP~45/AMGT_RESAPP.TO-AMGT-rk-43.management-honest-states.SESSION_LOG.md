# Session log -- 0.9.0_WK_AMGT_RESAPP~45 on AMGT-rk-43

Worktree `/c/tmp/wk-amgt-14-45`, branch `wk-amgt-14-45`, cut from SITEZ HEAD `047aee5478`.
Portal worktree `/c/tmp/wk-amgt-14-45/portal`, at DEV `625a0888` (found DETACHED HEAD --
see row `AMGT_RESAPP-Z-W45-S2`; a local branch `wk-amgt-14-45-portal` was created after the
portal commit to preserve it).

## Order of acts

1. Bar: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-45`; `org/`, `.tools/`,
   `lib/research/api/`, `portal/src/pages/SecurityAnalysis/` all present -> TREE-OK.
2. Read both never-widen halves (COO/CTO) for `AMGT-rk-43` -- both on file, both SIGNED.
3. AC1 (pre-act count bar): 12 objects, 5 zero-officer, 7 with officers, ceo_split
   CONFIRMED 1 / NOT_SEARCHED 7 / SEARCHED_NOTHING_FOUND 4 (the live split differs from the
   order's own narrative prediction of "4 SEARCHED_LINKS_UNREADABLE" -- traced to a data-
   vintage gap, filed as row `AMGT_RESAPP-Z-W45-S1`).
4. Adapter single-writer queue check: `git log --oneline $(git merge-base HEAD SITEZ)..SITEZ
   -- lib/research/api lib/research/checkface infra/aws/lambda/research/scoped_amgt_api
   infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh` printed NOTHING (checked
   twice: once before editing, once immediately before the build).
5. Snapshotted working-tree bytes of `scoped_amgt.py`, `ExecManagementTab.tsx`, `types.ts`
   to `.scratch/snapshot/` before editing (both repos).
6. Rewrote `ceo_profile_reading()` and `read_management()` in `lib/research/api/scoped_amgt.py`
   per section 1(a)/1(b) of the order. `python -m py_compile` OK.
7. AC2 (planted-negative fixtures via `_LocalPoolClient`): 4 of 4 assertions pass.
8. Portal: `portal/node_modules` was a MALFORMED junction (fsutil-confirmed doubled drive
   prefix `C:\C:\Users\...`) so `tsc` was absent -- ran `bun install --frozen-lockfile`
   (the order's own authorized exception), which surfaced the junction problem in the
   first place (row `AMGT_RESAPP-Z-W45-S2`). Rewrote `types.ts` (six-value union,
   `absent_because`, typed `LushaEnrichment`) and `ExecManagementTab.tsx` (`CeoProfile`,
   `ManagementBody`, `OfficerRow`).
9. AC3: `tsc -b` exit 0, no errors; six-value/absent_because/ZERO_OFFICERS/NOT-ATTEMPTED
   counts all present; stale sentence count 0.
10. Committed the adapter (`d12311bcea`), then opened the change-management ledger entry
    (`0c1280ce8f`) with pre-act measurements (never-widen hashes, queue check, pre-act
    CodeSha256/VersionId, bucket versioning, rollback mechanism) BEFORE the first live act.
11. Build: `build-and-upload-scoped-amgt.sh` -- uploaded, VersionId `YKlIrprMi5gbGTGDkBRddTpI2KwdmW1U`.
12. Apply: fresh worktree had never run `terraform init` (environment gap, row `W45-S2`) --
    initialized via the cached provider plugin dir. First `safe-apply` attempt hit a
    HALT-GATE (unrelated CRO-brief backlog messages) needing `HALT_ACK=1`. Second attempt
    (with `HALT_ACK=1`) failed to render ANY plan because `.build/chatter-axis-producer.zip`
    (an unrelated resource's build artifact) did not exist in this fresh worktree -- ran
    `infra/aws/terraform/harvest/lambda_src/build_zip.py` once (row `W45-S2`). Third attempt
    succeeded: `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`
13. Verified: post-act `get-function-configuration` CodeSha256 matches uploaded sha exactly;
    targeted 0-diff replan "No changes."; 13 of 13 GET routes (BA_US_Equity) -> 200, LOST=[].
14. AC4: ASML_NA_Equity flips SERVED->ABSENT/ZERO_OFFICERS; NU_US_Equity SERVED/NOT_SEARCHED
    with the correct reason; SAP_GY_Equity unchanged SERVED/CONFIRMED.
15. Closed the change-management ledger entry with the full proof string; `deploy_ledger.py
    close` removed the sentinel.
16. Committed the portal edit (`796f5c9c`, landed in the then-detached HEAD; branch
    `wk-amgt-14-45-portal` created immediately after to anchor it).
17. `python -m ruff check` clean; `pytest lib/research/api/tests/` 158 passed, 2 failed --
    both asserting the SUPERSEDED sentence-parsed ceo_profile_reading contract this order
    replaces by design (row `AMGT_RESAPP-Z-W45-S3`; the tests directory is outside this
    order's `<paths>`).
18. Filed three surprise rows (`W45-S1`, `W45-S2`, `W45-S3`), each its own commit.
19. Wrote and validated this proof-of-spec instance.

## Surprises filed

- `AMGT_RESAPP-Z-W45-S1` (OBSERVATION/INERT): 4 of 12 served objects carry
  `ceo_public_profile.absence_class: null` on an ABSENT+query-set object whose basis text
  describes the CANNOT_SAY case -- a data-vintage gap, read honestly as UNREADABLE_OBJECT.
- `AMGT_RESAPP-Z-W45-S2` (OBSERVATION/INERT): three worktree-provisioning gaps (malformed
  portal node_modules junction, detached-HEAD portal worktree, missing terraform
  init/.build artifact), all repaired locally, none widening this order's own surface.
- `AMGT_RESAPP-Z-W45-S3` (OBSERVATION/INERT): 2 of 160 pre-existing unit tests assert the
  superseded contract; outside this order's `<paths>` to fix.
