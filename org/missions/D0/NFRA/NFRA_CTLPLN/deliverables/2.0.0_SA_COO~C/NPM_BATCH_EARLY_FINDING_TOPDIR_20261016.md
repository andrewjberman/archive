# Early finding on the npm batch: five @types tarballs fail check 2 because the tool assumes the top folder is `package/` (2.0.0_SA_COO~C, 2026-10-16 ~21:3xZ)

Read while worker 149 finishes `CT-ce-1`, by running `.tools/tests/test_round30_npm_batch.py --check` and `--natives` in its worktree (read-only) and opening the tarballs in the holding folder.

- `NPM-BATCH-CHECK tarballs=50 checks_run_each=7 failed_total=5 ... check8=AWAITING released=False ok=True`.
- The five failures are all check 2 (identity: never waivable), on `@types/bun`, `@types/estree`, `@types/node`, `@types/react`, `@types/react-dom`: `package/package.json is absent or unreadable (absent)`.
- Cause, read from the tarballs: DefinitelyTyped tarballs do NOT use a `package/` top folder. `types__react-19.3.0.tgz` opens as `react/`, `react/LICENSE`, ... ; `types__node-24.13.6.tgz` opens as `node v24.13/` (a folder name with a SPACE), ... ; `react-19.3.0.tgz` opens as `package/` as expected. npm and bun strip the FIRST path component of a tarball whatever its name; the intake tool (check 2, and the install verb's "remove the leading `package/` directory") assumes the literal name `package/`.
- So this is a defect of the tool (cell `CT-cc-1`, `CT-cd-1`), not of the packages: the sha512 of all 50 equals the lockfile's (the issuer's own read `62bf3e780e`), and check 2 is rightly never-waivable, so the fix is in the tool.
- The same assumption would make the install verb mis-place or refuse these five on dell1.

Remedy (cut after `CT-ce-1` merges, so two cells never write the batch's records at once): a cell that makes check 2, verify and the install verb take the tarball's single top-level folder as the package root whatever its name (refuse a tarball with none or with more than one, an absolute or `..` first component), tests with the real `@types` shapes (including a folder name with a space), and re-runs `check` for the five real tarballs.
