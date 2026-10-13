# Receipt: NFRA_DEVPLN.TO-DP-x-1 -- first chosen-set promote (0.4.0_DT_ClientPlatform, 2026-10-13)

**Shipped:** one feature, `cand/laptop/contributing-boxes` (docs file `CONTRIBUTING-BOXES.md`, class opal-internal), to portal PROD.
PROD `63c4f9e3` -> `10e7664d6c4824cb88f04acf47f06264345b5b8b` (origin ls-remote read). Release branch `release/20261013T205139Z`, taken onto PROD by `--ff-only`; parity diff against the release branch = 0 lines. `origin/DEV` was never merged into PROD.

**CI:** run 38466864693 "Deploy to Production", status completed, conclusion success; the only workflow on that sha. Tag `portal-v2.1.214` peels to `10e7664d`.

**Precondition (step 1):** `git log origin/DEV --format=%B | grep -c "Feature: cand/laptop/contributing-boxes"` printed 1; DEV was `24877b67`.

**Builder lines (verbatim):**
```
RELEASE-CHECK features=1 first_parent_commits=1 unapproved=0
PROMOTE-LIST branch=cand/laptop/contributing-boxes class=opal-internal by=1.0.0_SA_CTO row=laptop-20261013T200117Z-9e8a pages=portal/CONTRIBUTING-BOXES.md (a docs file in the portal repo root; no page a user opens)
PROMOTE-CLIENT-FACING count=0
RELEASE result=READY reason=- branch=release/20261013T205139Z base=63c4f9e35f259ad76071b1099aeb9dddb150409f head=10e7664d6c4824cb88f04acf47f06264345b5b8b
```
`PROMOTE-CLIENT-FACING count=0`: the push law (a client-facing PROD change waits on Andrew) does not apply; page class opal-internal.

**Measurements after the push (step 4, verbatim):**
- `git -C portal rev-list --count origin/PROD..origin/DEV` = 8 (the 7 unapproved IRPT_ANLREQ commits `62d455f5 9ef6a359 923f7d69 794b7df4 73d8d3a4 0101dd66 a577cba5`, plus the integrator's merge `24877b67` of the feature)
- `git -C portal rev-list --count origin/DEV..origin/PROD` = 1 (the release merge `10e7664d`; DEV holds its own merge of the same feature, as the order's preflight predicted)
- `git -C portal log -1 --first-parent --format=%B origin/PROD`:
```
merge feature cand/laptop/contributing-boxes into release/20261013T205139Z

Feature: cand/laptop/contributing-boxes
Approved-By: 1.0.0_SA_CTO @laptop-20261013T200117Z-9e8a
```
The trunks differ by exactly the expected set; no surprise row.

**Ledger:** `devpln-r2-chosen-set-promote-20261013` opened at start, three legs (PROD commit, CI, tag) proven, CLOSED.
**Proof of spec:** DPx1-AC1 PASS, DPx1-AC2 PASS, instance VALID (rc=0).
**Teardown:** worktree deregistered (`worktree prune`); the directory `.runtmp/portal-promote-20261013T205302Z` persists on the Windows long-path error, gitignored and inert. Main portal tree on DEV `24877b67`.
**Side note (earlier whole-DEV promote today, not this one):** 18 files in the main portal tree read as modified with an empty diff and hashes equal to HEAD; reset to HEAD after a hash check, so the DEV fast-forward could run. The tree was clean for this promote.
