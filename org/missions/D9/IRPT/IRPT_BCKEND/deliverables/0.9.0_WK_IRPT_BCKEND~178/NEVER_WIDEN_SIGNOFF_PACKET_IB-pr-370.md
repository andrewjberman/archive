# Never-widen sign-off packet -- IB-pr-370 (E9): irpt-export-render packages the per-family policy revisions

Prepared by 0.9.0_WK_IRPT_BCKEND~178 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO~DELL2. Nothing in this packet was uploaded, deployed or applied: one
BUILD_ONLY run from a clean tree, one offline replay, AWS reads only. Census file: `IB83-1_e9_repin_census.json` (a byte-identical copy sits at
`IB83-1_repository_repin_census.json`, the name the order's check reads; row IRPT_BCKEND-D2-W178-S3). Model: `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-367.md` (~175).

## The pin

**Release pin P: `0a57f3c0e9ef89059827bbf888ecc9d5d61673e6`** (branch `wk-IRPT_BCKEND-178`, one commit, one file: `infra/aws/lambda/ci/lambda-source-map.json`, 8 lines in, 8 out).
Four `staged_from` rows of `irpt-export-render` moved in place, each to a commit whose blob was read, with the sha256 of that blob:

| packaged_as | old pin | new pin / sha256 | blob equals HEAD's |
|---|---|---|---|
| `repository.py` | `b13bab7495` | `2aa217ec58` / `f01fcf549e8e...` | yes |
| `composition.py` | `83e8b9577a` | `2aa217ec58` / `5b896004af77...` | yes |
| `infra/logic/registry/reporting_policies.json` | `c4fedd31c5` | `8530114ff9` / `407a80608dec...` | yes (and `fdc0a92a21`'s) |
| `lib/opal_naming.py` | `c4fedd31c5` | `b77e2af4d5` / `57db946ed7d5...` | no (HEAD adds naming work the function does not use) |

Why each is in the set (read in code):
- `repository.py` -- `ReportRepository.__init__(..., revisions=None)`; `persist` reserves `revisions[report_kind]` when the kind has one, and `get` re-checks against the
  retention reference's own revision (`_check_retention`). It adds no import. Without it a CUSTODY_REPORT is reserved under `irpt-x10-v1`, which registers no such family.
- `composition.py` -- defines `CUSTODY_POLICY_REVISION` and `additional_policy_revisions`; `submit_installed.py` (source dir, so already at HEAD in any build) does
  `from composition import CUSTODY_POLICY_REVISION`. The packaged composition at `83e8b9577a` lacks it, and also lacks the `revisions=` keyword the pinned repository takes.
  The old composition on the new repository would keep working; the new `submit_installed` on the old composition would not import.
- `reporting_policies.json` -- the `irpt-custody-x10-v1` row (E8, `8530114ff9`, state PENDING_ENFORCEMENT). The same blob carries two earlier riders: the
  `object` field on the served families and the `irpt-ycdgen-research-v1` ACTIVE row; no caller in this function requests either.
- `lib/opal_naming.py` -- NOT in the order's expected set. The packaged `c4fedd31c5` validator refuses the registry at `8530114ff9` ("reporting family metadata has an invalid
  field set"), so every `reporting_policy()` call -- `irpt-x10-v1` included -- would raise `ValueError`, and PERFORMANCE and ANALYSIS retention would be refused with the custody
  row. `b77e2af4d5` teaches the validator the `object` family key; the diff `c4fedd31c5..b77e2af4d5` touches reporting validation only. Row D2-W178-S1.
- Already right, not repinned: `retention.py` (`f60e6f1d2a` = HEAD), `entry.py` (`cf6839fe38`, routes `custody-report-read`), and the other registry rows (an offline probe at
  the built zip loads all three revisions, `irpt-x10-v1` ACTIVE with sha256 `e0046398e239...` unchanged).

## Census at P (`release-census.py irpt-export-render --pin 0a57f3c0e9`: built 64 members, live 64, `changed_members=5`)

| member | built | live | owner |
|---|---|---|---|
| `repository.py` | f01fcf549e8e | dbf128e96d73 | IB-pr-369 `2aa217ec58` |
| `composition.py` | 5b896004af77 | 6d2c3696d030 | IB-pr-369 `2aa217ec58` |
| `infra/logic/registry/reporting_policies.json` | 407a80608dec | 31aa483f578e | E8 `8530114ff9` |
| `lib/opal_naming.py` | 57db946ed7d5 | 4eb46f7059d7 | `b77e2af4d5` |
| `submit_installed.py` | 5140a8acaa86 | f7f2b60ed0d2 | IB-pr-369 `97e679c64f` (source dir, `files[]`) |

No rider: every member is intended and owned.

## BUILD_ONLY from a clean tree at P

`git status --porcelain` printed 0 lines at HEAD `0a57f3c0e9`; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-export-render` rc 0;
**built sha256 `PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0=`** (hex `3dbcaa987050a6be030bbeaab749e805fa2a29595ec9d35a27bb36aacc79993d`, 408932 bytes, 64 members).
`git status --porcelain` after: 0 lines. The kept `/tmp/lambda-artifact-irpt-export-render.zip` was removed afterwards. Nothing uploaded; `artifact_sha256` in the source map is untouched.

## Branch A (released)

- The function composes `irpt-custody-x10-v1` (the registry carries it), routes `custody-report-read`, and its repository names CUSTODY_REPORT with a per-family revision.
- What it does NOT yet do: retain or read a CUSTODY_REPORT. The registry row is PENDING_ENFORCEMENT and the packaged retention admits only an ACTIVE row (section below).
  Under Branch A alone a custody write or read is refused (`RetentionRefused: registered enforced policy required`), exactly as today but by a different message.
- PERFORMANCE and ANALYSIS retention and reads: unchanged in outcome (replay below: identical `result_sha256`, same `irpt-x10-v1` digest `e0046398e239...`).
- Opal principal / firm principal / anyone else: no new principal class, bucket, key prefix, route, IAM statement or function; five members of one existing function.
  Another firm's `custody-report-read` stays `OBJECT_NOT_COVERED` with no body (the repository raises `ReportDenied`, the Entry maps it).

## Branch B (rolled back)

- `irpt-export-render`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-export-render.zip` version
  **`fHVzTZi4vdHmRqcy0KK1hmrQ_dcT1QkO`** (latest at read time; 407653 bytes = the live CodeSize; written 2026-10-08T18:59:51Z), the zip whose `CodeSha256` is
  **`idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=`**. Read live this session (`get-function-configuration`, LastModified 2026-10-08T19:06:04Z): **unchanged** -- it is the
  IB-pr-368 result and has not moved since. A new upload makes a newer version, so rollback is a redeploy of THAT version through the Terraform deploy path, never a console edit.
- No route, IAM or data change to revert. Rolling back returns the function to the IB-pr-368 state (custody kind admitted, no per-family revision).

## Writers of each changed property

- `irpt-export-render` code zip (`CodeSha256`): the deploy path from the source map row only (`build-and-upload.sh` + Terraform `module.irpt_export_render`); 1 writer.
- The five packaged members: four staged rows at P (this order's one commit) plus the source-dir `submit_installed.py`; source authored under IB-pr-369 (~177), E8 (~M2) and X10 (CRO).
- The registry row's state (`PENDING_ENFORCEMENT` -> `ACTIVE`, with `enforcement_ref`): the registry file only (`infra/logic/registry/reporting_policies.json`), by a registry commit; the
  packaged copy is a second writer's product: a staged-row repin and a release. 2 writers of the packaged value.
- Retained custody report objects: `reports/custody_write.py` -> `ReportRepository.persist` (IB-pr-351), packaged by NO function today; caller IRPT_CUSTDY's producer. This release writes no data.

## The E8 status question, answered from the code

**Does the packaged code admit a `PENDING_ENFORCEMENT` policy row for retention, or only `ACTIVE`? Only ACTIVE.** `retention.py` `RetentionPolicy._registered()` returns a policy only when
`policy["state"] == "ACTIVE"` and the revision matches; `_policy()` repeats the state check and also requires `enforcement_ref` to be a 40-hex commit and `policy_sha256` to equal the
canonical digest. `lib/opal_naming.reporting_policy()` returns the PENDING row (so composition and `submit_installed.retained_reports` accept the revision and build the repository), and
`reporting_destination()` refuses a non-ACTIVE row ("enforcement is pending or disabled"). Measured at the built zip (`replay/built_run.json`, `custody.pending_persist`): a CUSTODY_REPORT
`persist` raises `RetentionRefused: registered enforced policy required`, and writes no custody blob or index row.

**How does `~M2`'s PENDING -> ACTIVE flip reach the function?** The registry is a staged file (`infra/logic/registry/reporting_policies.json`, packaged by its staged row), so the function reads
the registry bytes its zip was built with. The flip changes the row's `state` and `enforcement_ref`, which changes the row's `policy_sha256`; the function sees it only after **another repin of the
`reporting_policies.json` row to the flip commit and another release of the function** (one member; `lib/opal_naming.py` and the code need no change). Nothing else carries it: no environment
flag, no runtime registry read. No retained record can carry the PENDING digest (the write is refused), so the flip strands nothing. In an in-memory ACTIVE copy of the packaged row
(a simulation, not a release) the same built code retains and reads a CUSTODY_REPORT under `irpt-custody-x10-v1`, the retention row records that revision, ANALYSIS and PERFORMANCE stay on
`irpt-x10-v1` and still read, and another firm's `get` raises `ReportDenied` (OBJECT_NOT_COVERED at the route) with no body. A published custody report also needs accepted source evidence
(`retention_dependencies`), as ANALYSIS does. Row D2-W178-S2 (ARMED: the later order must sequence the ACTIVE row and its release before E2 and the after-reads).

## Regression arm for the release order (shaped like IB-pr-368 AMENDMENT 1)

`replay/replay_zip.py` (python `-I`, one process per zip, no network, no credentials; every module and the registry accessors are the zip's own). Unzip the LIVE zip and the BUILT zip into
two empty directories; then `python -I replay_zip.py live <live_dir> <snapshot> <live_run.json>` and `python -I replay_zip.py built <built_dir> <snapshot> <built_run.json>`.
Run here (committed in `replay/`, built from this session's `PbyqmHBQ...` zip against the live `idanP8nX...` zip):
- The LIVE code reserves one ANALYSIS and one PERFORMANCE fixture under `irpt-x10-v1`; both zips read them back with `repository.get`: both ok, neither raises nor refuses, **identical
  `result_sha256`** (ANALYSIS `a7a8ae48...`, PERFORMANCE `04afa6c7...`); policy digest `e0046398e239...` identical.
- Negative control: the stored `policy_sha256` of each report's retention row altered; both zips refuse (`RetentionRefused: retention binding changed`) for ANALYSIS and PERFORMANCE.
- Built-only: the custody arms above (PENDING refusal; simulated-ACTIVE round trip; other-firm refusal).
At the release order the arm is re-run against the zip actually uploaded, before the apply; any non-identical `result_sha256`, any raise on the x10 fixtures, or an unrefused negative control stops the apply.

## The two after-reads (the LATER order, after `~K2`'s E2 retains a real CUSTODY_REPORT)

Both are `custody-report-read` operations (`GET /api/scoped/investor-reporting/custody-report/{reportId}?revision=<revision>`).

1. **Opal read by ref returns it.** As an Opal principal, read one REAL CUSTODY_REPORT by reference; pass = HTTP 200, `report_kind` CUSTODY_REPORT, the requested `report_id` and `revision`,
   and the document. Also: live `CodeSha256` equals the deployed build's and `release-census.py irpt-export-render --pin <the deployed pin>` prints `changed_members=0`.
2. **Other-firm read is REFUSED.** As a principal of another firm, read the same reference; pass = `OBJECT_NOT_COVERED` and no body of the report.

Precondition (D2-W178-S2): the registry row is ACTIVE in the served function (the second repin and release) BEFORE E2 retains the report. Without it E2's persist is refused and there is nothing to read.
