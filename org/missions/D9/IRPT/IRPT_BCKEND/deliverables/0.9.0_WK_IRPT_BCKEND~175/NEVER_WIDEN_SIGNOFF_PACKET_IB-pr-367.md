# Never-widen sign-off packet -- IB-pr-367 (E7 part 1): irpt-export-render packages a repository.py whose KINDS carries CUSTODY_REPORT

Prepared by 0.9.0_WK_IRPT_BCKEND~175 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO~DELL2. Nothing in this packet was uploaded, deployed or applied: one
BUILD_ONLY run from a clean tree, AWS reads only. Census file: `IB80-1_repository_repin_census.json` (same folder).
Model: `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md` (~171).

## The pin

**Release pin P: `a0d8d4943f68c2032488cc6b46b8a30e708e5adc`** (branch `wk-IRPT_BCKEND-175`, one commit, one file: `infra/aws/lambda/ci/lambda-source-map.json`,
4 lines in, 4 out). In function `irpt-export-render`, two `staged_from` rows moved from `83e8b9577a` to the commits whose blobs equal HEAD's:

| packaged_as | old pin / sha256 | new pin / sha256 |
|---|---|---|
| `repository.py` | `83e8b9577a` / `f255335b...` (KINDS = PERFORMANCE, ANALYSIS) | `b13bab749568b0fb03035f784c25d160af57adc4` / `dbf128e96d73...` (KINDS = PERFORMANCE, ANALYSIS, CUSTODY_REPORT) |
| `retention.py` | `83e8b9577a` / `bdd74e5f...` | `f60e6f1d2a980efe227f0805e677ccf652e54992` / `f7540e355241...` |

Why `retention.py` is in the set (read in code, not guessed): `repository.py@b13bab7495` `_check_retention` calls
`retention.reference(owner, family, logical_id, revision)` with the revision a retained reference carries, and every retained reference carries one. The packaged
`retention.py@83e8b9577a` defines `reference(owner, family, logical_id)` (three arguments), so with the new repository alone every retained read, PERFORMANCE and ANALYSIS
included, would raise TypeError. `retention.py@f60e6f1d2a` is the change that takes the fourth argument; it imports only names the new repository defines.
Not repinned, and why: `composition.py` (the HEAD change adds an optional keyword; the packaged one calls the repository without it, which is valid), `entry.py` (already at
`cf6839fe38`, which routes `custody-report-read`), `opal_naming.py`, `custody_read.py` / `retained_export.py` / `submit_installed.py` (source-dir `files[]`, read at the pin).
`reporting_policies.json` is NOT repinned: see the open finding below.

## Census (`release-census.py irpt-export-render --pin a0d8d4943f`: built 64 members, live 64, `changed_members=2`)

| member | state | owner |
|---|---|---|
| `repository.py` | changed (built dbf128e96d73, live f255335beb26) | IB-pr-336 (`b13bab7495`: KINDS gains CUSTODY_REPORT; same blob carries `f60e6f1d2a`'s policy-revision binding) |
| `retention.py` | changed (built f7540e355241, live bdd74e5f9b90) | YCD-l-6 (`f60e6f1d2a`: retention resolves the policy from the reference) |

No rider: both members are repinned on purpose. No other member differs from the live zip.

## BUILD_ONLY from a clean tree at P

`git status --porcelain` printed 0 lines at HEAD `a0d8d4943f`; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-export-render` rc 0;
**built sha256 `idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=`** (hex `89d6a73fc9d7fe6a9a43e14818663a013e177bf27172438cdcdd2b5b08af4a1f`, 407653 bytes, 64 members).
The built zip's `repository.py` reads `KINDS = ("PERFORMANCE", "ANALYSIS", "CUSTODY_REPORT")` and its `entry.py` routes `custody-report-read`. `git status --porcelain`
after the build: 0 lines (no residue to remove). Nothing uploaded; the source map's `artifact_sha256` is untouched.

## Branch A (released)

- Opal principal (staff): can read ONE retained CUSTODY_REPORT by reference through `custody-report-read` and receives that report and revision (same authorization as the export
  submit, `retained_export.resolve`). Today the route exists (IB-pr-364) but the packaged repository refuses the kind; this release lifts that refusal.
- Firm principal: reads a CUSTODY_REPORT only inside its own firm and covered accounts; another firm, or an uncovered account, answers `OBJECT_NOT_COVERED` with no body.
- Anyone else: unchanged (refused at the scoped-API boundary).
- Retained PERFORMANCE and ANALYSIS reads: unchanged in outcome (their references carry `irpt-x10-v1`, ACTIVE and unchanged); the retention code is only newer.
- What does NOT widen: no new principal class, bucket, key prefix, route, IAM statement or function; two members of one existing function.

## Branch B (rolled back)

- `irpt-export-render`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-export-render.zip` version
  **`FHKz88vjxHfi5uqADSw5GlQq8IULm615`** (latest at read time, 2026-10-08T17:18:27Z, 407094 bytes = the live CodeSize), the zip whose `CodeSha256` is
  **`03p2eIEKU9iSIOe5GYDbkbisapqAjULUyAPA/Wcxrfc=`**. Read live this session (`get-function-configuration`, LastModified 2026-10-08T17:22:16Z): **unchanged** since the order was cut.
  A new upload makes a newer version, so rollback is a redeploy of THAT version through the Terraform deploy path, never a console edit.
- No route, IAM or data change to revert. Rolling back returns the owner read of a CUSTODY_REPORT to DEPENDENCY_UNAVAILABLE.

## Writers of each changed property

- `irpt-export-render` code zip (`CodeSha256`): the deploy path from the source map row only (`build-and-upload.sh` + Terraform `module.irpt_export_render`); 1 writer.
- `repository.py` and `retention.py` as packaged: the two staged rows at P (this order's one commit); source authored under IB-pr-336 (~138) and YCD-l-6 (~3).
- Retained custody report objects (the data the read returns): written only by `reports/custody_write.py` -> `ReportRepository.persist` (IB-pr-351), packaged by NO function today;
  its caller is IRPT_CUSTDY's producer. This release writes no customer data.

## OPEN FINDING that gates after-read 1 (row IRPT_BCKEND-D2-W175-S1)

`infra/logic/registry/reporting_policies.json` row `irpt-x10-v1` (ACTIVE, 13 families) registers NO `CUSTODY_REPORT` family, at the pinned `c4fedd31c5` and at HEAD. Under the enforced
retention (`composition.build_retained_repositories`), `ReportRepository.persist` reserves retention for family = the report kind and `get` re-checks it; `RetentionPolicy._policy` then raises
"unregistered retention family". So this release makes the packaged code name the kind, but no CUSTODY_REPORT can be retained or read through the enforced repository until a policy row
carries the family (a registry change: CRO lane; it needs its own enforcement revision). No repin of any commit at or before HEAD can add it, so it is not part of this release set.
The signer decides whether to release this pair first (harmless; the read keeps failing closed) or to hold it for the registry row.

## The two after-reads (after release, by the later release order)

Both are `custody-report-read` operations (`GET /api/scoped/investor-reporting/custody-report/{reportId}?revision=<revision>`).

1. **Opal read by ref returns it.** As an Opal principal, read one REAL CUSTODY_REPORT by reference; pass = HTTP 200, `report_kind` CUSTODY_REPORT, the requested `report_id` and `revision`,
   and the document. Also: live `CodeSha256` equals `idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=` and `release-census.py irpt-export-render --pin <the deployed pin>` prints `changed_members=0`.
2. **Other-firm read is REFUSED.** As a principal of another firm, read the same reference; pass = `OBJECT_NOT_COVERED` and no body of the report.

Which seat produces the real CUSTODY_REPORT for after-read 1: IRPT_CUSTDY, `2.0.0_SA_COO~K2`, its cell E2 (the producer that calls `custody_write.persist_custody_report`).
Order: (a) the registry family row for CUSTODY_REPORT (finding above) is in the served policy; (b) this release (build, upload, deploy) lands; (c) E2 retains one real CUSTODY_REPORT
and hands back its report_id and revision; (d) the later release order runs after-read 1 then after-read 2 against that reference. E2 waits on (b) and, per the finding, on (a).
