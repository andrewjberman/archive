# Never-widen sign-off packet -- IB-pr-373 (E10 recut): irpt-export-render persists the Performance client statement through the guarded Entry, owner and accounts derived server-side, and carries the ACTIVE registry row

Prepared by 0.9.0_WK_IRPT_BCKEND~181 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO~DELL2. Replaces `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-372.md` (branch `wk-IRPT_BCKEND-180`, never drained). Nothing in this packet was
uploaded, deployed or applied: offline tests, one BUILD_ONLY run from a clean tree, one offline replay, AWS reads only. Census file: `IB86-1_e10_census.json`. In prose the report is the
"Performance client statement" (the quarterly client export of Performance, adding holdings, activity and fees); the code ids are unchanged: CUSTODY_REPORT, `irpt-custody-x10-v1`, `custody-report-read`.

## The pin

**Release pin P: `9238309ecacede4d3f71a366cf8e12772eafd3eb`** (branch `wk-IRPT_BCKEND-181`, one commit, one file: `infra/aws/lambda/ci/lambda-source-map.json`, 12 lines in, 4 out).
The code commit it packages is `d34a46f37d493e5abc63490249de8f679ac64b14` (entry.py, submit_installed.py, custody_persist.py, custody_write.py, routes.json, the test). In the `irpt-export-render` entry, in place:

| change | old | new / sha256 | blob equals HEAD's |
|---|---|---|---|
| `files[]` | -- | adds `custody_persist.py` (source dir) and `custody_write.py` | -- |
| `files[]` member `submit_installed.py` (source dir, rides the pin's tree) | -- | blob at P = `d34a46f37d`'s | yes |
| staged row `custody_write.py` (NEW, `reports/custody_write.py`) | -- | `d34a46f37d` / `9e3aa49d485d...` | yes |
| staged row `entry.py` | `cf6839fe38` | `d34a46f37d` / `39c3ac4495a8...` | yes |
| staged row `infra/logic/registry/reporting_policies.json` | `8530114ff9` | `b4d98a4fe3` / `dc0eccfde861...` | yes |

`lib/opal_naming.py` is NOT repinned (`b77e2af4d5`, packaged under E9). The registry diff `8530114ff9 -> b4d98a4fe3` is exactly two lines (`state`, `enforcement_ref` of the custody row); every other row is byte-identical.
The BUILT zip's own `opal_naming.reporting_policy("irpt-custody-x10-v1")` returns `state ACTIVE`, `enforcement_ref 0a57f3c0e9...`, `policy_sha256 11db343844ea...`; `irpt-x10-v1` still reads with sha256 `e0046398e239...` (replay below).

## The trigger, and why it is the only one

**The persist is reachable ONLY through the guarded Entry of `irpt-export-render`: a DECLARED route row plus an operation behind the existing CUSTOM portal authorizer, as `custody-report-read` is.**
Route `POST /api/scoped/investor-reporting/custody-report` (`docs/contracts/investor-reporting/v1/routes.json`, status DECLARED, cell IB-pr-373) -> operation `custody-report-persist` in `entry.py` ->
`custody_persist.custody_report_persist`. `entry.py` carries no `irpt_custody_persist` path and no marked-event branch (IB-pr-372's direct-invoke event, in which the caller asserted the principal and accounts, is removed; test and replay arm below show a marked event is refused like any other event, reason `CONTRACT_VERSION`, nothing written).

**Authentication** (nothing new; the same guard every route has): the edge validator and the CUSTOM authorizer; then the Entry's contract-version check, the VERIFIED firm header (absent -> `NOT_AUTHORIZED`), the firm binding (another firm's header or a body restating another firm -> `FIRM_BINDING`),
and the Enforcer's scope. Only then the operation, which takes the principal from `ports["principal"]` = `InteractiveAccess.current` over the verified headers -- never from the body -- and **refuses any principal that is not `OPAL_GLOBAL`** (`NOT_AUTHORIZED`)
before it reads anything: a custody submission is itself an Opal act (`custody-owner-v1` requires an `OPAL_GLOBAL` submitter), so the write is Opal-only, stricter than the read.

**Why (a) and not (b), a schedule.** IRPT_CUSTDY PRD hop S07 wires the render on the export path. The unit of work is one retained custody submission, named by reference by an Opal operator (or the producer acting as one); there is no server-held index of
"submissions awaiting a report" for a schedule to read, so an in-function schedule would have nothing to scan, and its resource (an EventBridge rule plus a lambda permission, Terraform) is outside this grant. The route is the lighter, already-guarded path. No schedule is created.

## The server-side source of the owner and accounts

The request carries exactly three keys: `retained_request` (`{"artifact_id": "ART-<64 hex>"}`), `document` (the report's content) and `provenance` (optional). **Any other key -- owner, principal, account_ids, account_set_id, tenant, firm_id, permitted_account_set, retention_dependencies, request_ref -- is refused `INVALID_INPUT` by name and nothing is written.**
The owner and the account set come from the producer's own retained request:
- The retained request is the custody submission's frozen composition: the `REQUEST_COMPOSITION` artifact `submit_service` retains (`irpt-analysis-composition.v1`, resolved owner `custody-owner-v1`, source lane `CUSTODY`).
- It is loaded BY REFERENCE through the artifact repository (`ports["artifacts"]`, new in `submit_installed.compose`, same table, bytes and authorizer as `reports`) under `retained_export.authorizer(principal, scope.permitted_account_set)` -- **the rule `custody-report-read` reads under**: the caller is in the owner's firm and the caller's CURRENT scope covers every account on the request.
- The owner is the owner the repository ADMITTED from the stored record (firm, principal, `account_set_id`, `account_ids`, ...), checked equal to the composition's frozen owner and to `custody-owner-v1`; another family, another lane or another owner schema is refused by name.
- The report's identity (`request_ref`) is the artifact id; its provenance carries the artifact id and sha256 beside the caller's provenance (the server's keys win).
- **Accepted source evidence (row D2-W180-S1):** the ACTIVE family is accepted-only, so the persist passes `retention_dependencies=[the request artifact's own retention_ref]`, taken from the artifact the repository returned (`custody_write.persist_custody_report` gained an optional `retention_dependencies` parameter, nothing else changed). The repository verifies it (live, ACCEPTED, same principal): a request not yet promoted refuses `accepted dependency required`, nothing is written.
- The report is read back under the same principal before the answer; the answer is the reference (kind, id, revision, sha256), never the document. The stored owner is the retained request's creator, not the persisting operator.

## Census at P (`release-census.py irpt-export-render --pin 9238309eca`: built 66 members, live 64, `changed_members=5`)

| member | state | built | live | owner |
|---|---|---|---|---|
| `entry.py` | changed | 39c3ac4495a8 | b32032d38b94 | this cell `d34a46f37d` |
| `infra/logic/registry/reporting_policies.json` | changed | dc0eccfde861 | 407a80608dec | E8 ACTIVE flip `0c35aeeaa8`, merged `b4d98a4fe3` |
| `submit_installed.py` | changed | aa7f2dd306d2 | 5140a8acaa86 | this cell `d34a46f37d` |
| `custody_persist.py` | added | dec22ae51b93 | - | this cell `d34a46f37d` |
| `custody_write.py` | added | 9e3aa49d485d | - | this cell `d34a46f37d` (writer from IB-pr-351) |

No rider: every member is intended and owned. `composition.py`, `repository.py`, `retention.py`, `retained_export.py`, `custody_read.py`, `interactive_access.py` and `lib/opal_naming.py` are unchanged against live (E9 already carries them).

## BUILD_ONLY from a clean tree at P

`git status --porcelain` printed 0 lines at HEAD `9238309eca`; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-export-render` rc 0;
**built sha256 `rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek=`** (hex `acd8ed4f072686935d1d457b55c3b57113dc0b5c07680366d6820ff97bdfe849`, 414177 bytes, 66 members). `git status --porcelain` after: 0 lines.
The kept `/tmp/lambda-artifact-irpt-export-render.zip` was copied to scratch and removed. Nothing uploaded; `artifact_sha256` in the source map is untouched.

## Branch A (released: function, then route)

Order, as IB-pr-363/364 ordered: (1) the IAM leg below; (2) upload the built zip and apply `module.irpt_export_render` (0 destroy), live `CodeSha256` must equal the built sha256, export root re-plan `No changes`; (3) ONLY THEN apply the api root, which adds ONE route
(`aws_apigatewayv2_route` for `POST /api/scoped/investor-reporting/custody-report`, derived from the routes.json row), 0 destroyed, api root re-plan `No changes`, route listed on api `7k3ed8px20`, an unauthenticated POST refused 401.
- The function accepts the persist only through the guarded Entry and retains a CUSTODY_REPORT under `irpt-custody-x10-v1` (ACTIVE, 2555-day accepted ceiling, accepted-only), readable by `custody-report-read` by reference.
- Until the route is applied nothing can reach the operation over HTTP; with the function applied and the route not, HTTP behaviour is byte-for-byte the same (the three export routes and `custody-report-read` resolve as before). No data is written by the release.
- PERFORMANCE and ANALYSIS retention and reads: unchanged (replay below: identical `result_sha256`, same `irpt-x10-v1` digest).
- Opal principal / firm principal / anyone else: no new principal class, bucket, key prefix or function; one new route on an existing API, five members of one existing function. Another firm's `custody-report-read` stays `OBJECT_NOT_COVERED` with no body (replay: `ReportDenied: report unavailable`, `body_returned false`).
- **Precondition, row IRPT_BCKEND-D2-W181-S1:** the role of `irpt-export-render`, as Terraform declares it, holds no `dynamodb:PutItem`/`UpdateItem` on the requests table, no S3 write on the custody-report prefix and no S3 read of the request-composition prefix. Until an IAM leg applies those (its own sign-off, not this cell), the operation fails closed (nothing written) and the first after-read cannot pass. That leg is owed before step (3).

## Branch B (rolled back)

- `irpt-export-render`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-export-render.zip` version
  **`LefrKSE11JIR93JOh.1RP5cSIUrqKfI_`** (latest at read time; 408932 bytes = the live CodeSize; written 2026-10-08T20:13:51Z), the zip whose `CodeSha256` is
  **`PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0=`**. Read live this session (`get-function`): `CodeSha256` PbyqmHBQ..., `LastModified` 2026-10-08T20:18:09Z, and the downloaded live zip hashes to the same value -- **unchanged**,
  the IB-pr-371 result. A new upload makes a newer version, so rollback is a redeploy of THAT version through the Terraform deploy path, never a console edit.
- The route: remove the routes.json row (or revert its commit) and apply the api root; one `aws_apigatewayv2_route` destroyed, nothing else. Roll the route back FIRST when both legs landed (a route to a function that lacks the operation answers `UNSUPPORTED_OPERATION`, harmless but untidy).
- No IAM or data change in this cell to revert. Rolling back returns the function to the E9 state (custody kind admitted, per-family revision composed, registry row PENDING_ENFORCEMENT, no persist operation).
- Any Performance client statement retained between the release and the rollback stays in its bucket and index; the rolled-back function cannot read it (the row is PENDING there), so Branch B is taken before E2a retains one, or with the retained set counted first.

## Writers of each changed property

- `irpt-export-render` code zip (`CodeSha256`): the deploy path from the source map row only (`build-and-upload.sh` + Terraform `module.irpt_export_render`); 1 writer.
- The five packaged members: this cell's two commits (`d34a46f37d` code, `9238309eca` pin) plus the staged blobs they name; authored under IB-pr-351 (writer), E8 (~M2, registry) and this cell.
- The registry row's state (`PENDING_ENFORCEMENT` -> `ACTIVE`): the registry file only (`infra/logic/registry/reporting_policies.json`), by a registry commit (`0c35aeeaa8`); the packaged copy is a staged-row repin and a release. 2 writers of the packaged value.
- Retained CUSTODY_REPORT objects (blob + index row + retention row): `ReportRepository.persist` reached ONLY through `custody_persist.custody_report_persist` (the guarded operation); `reports/custody_write.py` has no other caller in the tree, and
  `ycharts/generate/custody_submission.py` writes artifacts (REQUEST_COMPOSITION, NORMALIZED_PORTFOLIO), never a report. After the release, 1 writer path; the producer that calls it (IRPT_CUSTDY E2a) is a caller, not a writer.
- The route `POST .../custody-report`: the api root's `routes.tf` from the routes.json row only; 1 writer.

## Regression arm for the release order (shaped like IB-pr-368 AMENDMENT 1, IB-pr-370 and IB-pr-372)

`replay/replay_zip.py` (python `-I`, one process per zip, no network, no credentials; every module and the registry accessors are the zip's own). Unzip the LIVE zip and the BUILT zip into two empty
directories; then `python -I replay_zip.py live <live_dir> <snapshot> <live_run.json>` and `python -I replay_zip.py built <built_dir> <snapshot> <built_run.json>`.
Run here (committed in `replay/`, the BUILT zip `rNjtTwcm...` against the LIVE zip `PbyqmHBQ...`, downloaded and hash-checked):
- The LIVE code reserves one ANALYSIS and one PERFORMANCE fixture under `irpt-x10-v1`; both zips read them back with `repository.get`: both ok, neither raises nor refuses, **identical `result_sha256`**
  (ANALYSIS `a7a8ae48...`, PERFORMANCE `04afa6c7...`, the same values as the E9 and IB-pr-372 replays); policy digest `e0046398e239...` identical.
- Negative control: the stored `policy_sha256` of each report's retention row altered; both zips refuse (`RetentionRefused: retention binding changed`) for ANALYSIS and PERFORMANCE.
- Built-only arms of the guarded operation, against the registry row AS PACKAGED (ACTIVE; no simulated row): (C1) a retained custody submission is persisted by a DIFFERENT Opal operator, `stored_owner_equals_retained_request_owner true`, the report depends on the request's retention ref, its retention row records `irpt-custody-x10-v1`, an Opal-style
  `retained_export.resolve` by reference returns the document (`document_equal true`), another firm gets `ReportDenied`, `body_returned false`; (C2) a caller-supplied `owner`, `principal`, `account_ids` or `account_set_id` is refused `CustodyPersistRefused` by key name, 0 custody blobs; (C3) the retained request not yet accepted: `RetentionRefused: accepted dependency required`, 0 blobs;
  (C4) the custody row absent from the registry: `RetentionRefused: unregistered retention family`, 0 blobs; (C5) NEGATIVE CONTROL, the composition removed (a repository built without the custody revision): `RetentionRefused: unregistered retention family`, 0 blobs;
  (C6) a firm-advisor principal: `CustodyPersistNotOpal`, 0 blobs; (C7) the zip's own `entry.py` (flat layout, cold-start import works): `ROUTES[POST .../custody-report] = custody-report-persist`, five operations, the IB-pr-372 marked event answered `ok false`, reason `CONTRACT_VERSION`, no data, 0 blobs; `entry.py` does not contain `irpt_custody_persist`.
At the release order the arm is re-run against the zip actually uploaded, before the apply; any non-identical `result_sha256`, any raise on the x10 fixtures, or an unrefused negative control stops the apply.

Offline negative controls on the tests (in tree, 44 tests in `test_custody_writer_composed.py`, never committed mutants): removing the Opal check fails 2; letting extra request keys through fails 9; dropping the retained request's retention ref from the persist fails 23; letting the caller's principal id stand in the owner fails 26; dropping the custody-submission check fails 3; restored, 44 pass.

## The two after-reads (the LATER order, after IRPT_CUSTDY E2a retains one real Performance client statement through this operation, and after the IAM leg)

Both are `custody-report-read` operations (`GET /api/scoped/investor-reporting/custody-report/{reportId}?revision=<revision>`).

1. **Opal read by ref returns it.** As an Opal principal, read the REAL CUSTODY_REPORT E2a retained, by reference; pass = HTTP 200, `report_kind` CUSTODY_REPORT, the requested `report_id` and `revision`, and the document.
   Also: live `CodeSha256` equals the deployed build's and `release-census.py irpt-export-render --pin <the deployed pin>` prints `changed_members=0`.
2. **Other-firm read is REFUSED.** As a principal of another firm, read the same reference; pass = `OBJECT_NOT_COVERED` and no body of the report.
3. (the trigger's own arms, same order) an unauthenticated `POST .../custody-report` is refused 401 at the edge; an Opal POST naming a retained custody submission returns the reference and no document.

Preconditions the producer and the release owe: E2a must retain a custody submission and have it promoted (accepted) before it persists (else refused by name, nothing written); the IAM leg (row D2-W181-S1); and a ruling on whether the report content should be bound to the retained request (row D2-W181-S2: the document is the one caller-supplied value; the persister's identity is in the Lambda log and CloudTrail, not the record).
