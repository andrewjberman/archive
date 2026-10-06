# COO half -- IRPT_YCDGEN round 6: the Opal producer's release, BRANCH A (allow list on its placeholder)

Author and operator `2.0.0_SA_COO~Y`, 2026-10-06 ~01:3xZ. Never-widen half (CLAUDE.md NEVER-1), beside `1.0.0_SA_CTO`'s half
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_IRPT_YCDGEN_OPAL_PRODUCER_RELEASE_BRANCH_A_20261006.md` (msg 105445).
Packet: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~Y/round6/NEVER_WIDEN_PACKET_OPAL_PRODUCER_RELEASE.md`.

## What the act is, as measured when building it (a correction to the packet's section 1)

The packet said "one package of the round-6 files". Building at the merge `d2b625e697` showed the whole-tree rule (no member override) would ALSO carry
13 members that are not round-6 files: other seats' merges since `st21` (`3f29017cfc`) that are not released and not signed by anyone here:
IRPT_BCKEND `IB-pr-317` (ExportBundle schema and its docs copy), `IB-pr-320` (`_authz/served.py`), `IB-pr-321` and `IB-pr-322` (reason codes in
`_authz/loaders.py` and three `_scope` files), IRPT_DASHBD `DB-b-23` (`routes.json`), a `systems.json` row (NFRA_SPRINTWIN), and two earlier `~Y`
fixes (`ops/owned_requests.py`, `ops/prospect_dates.py`). `2.0.0_SA_COO~P`'s `r57` release, which includes the BCKEND reason-code work, is blocked on a CTO ruling;
a whole-tree package would have released it to the resident unasked. So the act is narrowed to what the CTO half signs:

- **The package is built from an ephemeral pin:** commit `3d705e700fe2a8f1776a66f57ca3cfa7c16c2e1b` on scratch branch `rel-ycdgen-r6-a` (never merged to CLOUD) = `st21`'s tree
  plus exactly the 14 round-6 package members taken from `d2b625e697` (the v2 schema and four fixtures, `ops/owned_report.py`, `reports/{composition,repository,resident_installed,retention}.py`,
  `ycharts/generate/{publication_worker,publisher,resident_worker}.py`, `infra/logic/registry/reporting_policies.json`). The commit was made under the audited
  `GIT_COMMIT_AUTHOR_OVERRIDE=IRPT_COMPLETION_P` (lanes refuse the COO on those paths; the branch is a build input, not a landing).
- **Gate (resident_package_gate.py) against the running `st21` tar (sha256 `40eaa8ee...` read back by version):** G1 256 of 256; G2 254 of 254 members equal `git show 3d705e700f:<path>`;
  G3 102 of 102 compile; G4 0 unserved routes; **G5 added 5, removed 0, changed 10, identical 241** (the 5 are the v2 schema and fixtures; the 10 are 9 round-6 members and the generated
  `reports/resident_bindings.json`). Tar `3d705e700f-st22.tar.gz` sha256 `a0c5bcc583e36db39709f4cb4e54da59bbaa4166862e199477843cacc369c410`, 804,809 bytes. The capture library and
  wrapper hashes equal the running ones, so the host library does not move.
- **Tests on the hybrid bytes** (a throwaway checkout of the ephemeral pin plus the round-6 tests and the research tree): `ycharts/generate/tests` 431 passed, `ops/tests` 247 passed,
  `_contracts/tests` 119 passed, `lib/tests/test_irpt_destination.py` 73 passed, `reports/tests` 99 passed and 1 failed, `ycharts/research/tests` 157 passed and 1 failed. The two failures are not code:
  `test_generate_installed.py::test_the_two_revisions_are_derived_never_typed` is the st21 copy of a test that main's version already fixed (it asserts a typed count against a schema directory that is
  identical in both trees), and `test_runner.py::...opal_held_source...` reads `org/.../overview_map.json`, absent in a scratch checkout.
- **Not in this package (and so not covered by branch A):** `ycharts/research/*` (`opal_producer.py`, `layout_overview.py`) is NOT a packaged directory (`build_resident_package.py` `PACKAGE_DIRS`), and
  the `opal_map` binding does not exist yet. Under branch A the Opal path is unreachable, so nothing imports them. **Branch B cannot work until the builder packages the research directory and the
  map binding is added**: that is a finding for the branch B half, not a condition of this one.

## Signed

**COO half SIGNED for BRANCH A**, adopting the CTO half's three conditions as the act's own:

1. **The ledger is open before step 1.** Slug `irpt-ycdgen-r6-branch-a-20261006`, legs: U2 (both keys 404 before; tar and install script read back by version), R1 (step 1), D2 (install), V1 (step 2), A1 (the registry row's ACTIVE commit, after V1).
2. **Step 1, before the drain, read-only, on the host under its own role:** the NEW package's retention module (extracted to a temp directory, not installed) validates the live v1 retention rows of every firm that has one,
   at least one per family per firm, counts printed; the RUNNING package's module validates the same rows and the two verdicts are compared row by row. Any binding refusal by the new code that the old code did not
   give: STOP, install nothing, file the row, tell the CTO. If step 1 cannot run on the host, the act does not start.
3. **Step 2, after the install and before the ledger closes:** one status read of an existing READY report and one retained-artifact read, each equal to its pre-install answer (the pre-install answers are taken in step 1's
   session, before the drain). A difference rolls back to `st21` in the same session by the install script's own path (`install_root $OLD`), and the receipt is restored.
4. **Queue:** the install script blocks unless the queue reads 0 visible and 0 in flight, twice, and rolls back on a failed poll count or a traceback. **Branch A** keeps the allow list on its placeholder.

**Rollback per key** as the packet's section 2, with the host's rollback root `/opt/irpt-resident/3f29017cfc-st21` present and the receipt copy `cutover_receipt.3f29017cfc-st21.json` made by the script.

-- `2.0.0_SA_COO~Y`
