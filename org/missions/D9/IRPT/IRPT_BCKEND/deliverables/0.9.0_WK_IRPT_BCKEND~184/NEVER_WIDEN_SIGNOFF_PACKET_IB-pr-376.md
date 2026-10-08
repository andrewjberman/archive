# Never-widen sign-off packet -- IB-pr-376: irpt-export-render packages persisted_by and the composition-hash binding of the Performance client statement (IB-pr-375)

Prepared by 0.9.0_WK_IRPT_BCKEND~184 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO~DELL2. Nothing here was uploaded, deployed or applied: one BUILD_ONLY run from a clean
tree, one offline replay, AWS reads only. Census file: `IB88-1_census.json`. Model: `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-370.md` (~178).

**Where the release goes: to `0.7.0_AE_CloudOps~DELL2` (Andrew-direct, msg 1756), the FUNCTION ONLY (`irpt-export-render`).** The route waits for the IAM leg
(separate pair, @77440a907b); this packet moves no route, IAM statement, bucket or key prefix.

## The pin

**Release pin P: `49bc13131d97addcbfadc468a9e47f934a173bec`** (branch `wk-IRPT_BCKEND-184`, one commit, one file `infra/aws/lambda/ci/lambda-source-map.json`, 2 lines in, 2 out).
One `staged_from` row of `irpt-export-render` moved in place:

| packaged_as | old pin | new pin / sha256 |
|---|---|---|
| `custody_write.py` | `d34a46f37d` (IB-pr-373) | `6a0226dc02fc5f2b6d9f33acf21a0971b89ae0e9` (IB-pr-375) / `17faecab6d36554250160db765e92c673e1f1b1592aab552196ac12ff34ffefc` |

Why only this row: IB-pr-375 (`6a0226dc02`) changed `export/custody_persist.py` (source dir, `files[]`, so a HEAD build carries it) and `reports/custody_write.py`
(staged, so it needed the repin). `export/entry.py` is byte-identical at `d34a46f37d` and `6a0226dc02` (sha256 `39c3ac4495a8...`), so its row stays. Every other row is untouched.

## Census at P (`release-census.py irpt-export-render --pin 49bc13131d`: built 66 members, live 66, `changed_members=2`)

| member | built | live | owner |
|---|---|---|---|
| `custody_persist.py` | e5189196c438 | dec22ae51b93 | IB-pr-375 `6a0226dc02` (source dir, `files[]`) |
| `custody_write.py` | 17faecab6d36 | 9e3aa49d485d | IB-pr-375 `6a0226dc02` (staged row, repinned at P) |

No rider: both members are intended and owned.

## BUILD_ONLY from a clean tree at P

`git status --porcelain` printed 0 lines at HEAD `49bc13131d`; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-export-render` rc 0;
**built sha256 `7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=`** (hex `ed3dbdc0f8736d4fc5949a5e4f730d489e631567049a2edbbc78922840a4ca7b`, 415060 bytes, 66 members).
`git status --porcelain` after: 0 lines; the kept /tmp zip was removed. Nothing uploaded; `artifact_sha256` in the source map is untouched.

## Branch A (released)

- Every custody record the guarded operation persists carries `persisted_by` (the VERIFIED caller's principal id, never a request field; a body field named `persisted_by` is refused by key
  name) and `composition_sha256` (the retained REQUEST_COMPOSITION artifact's content hash) in its provenance. Server keys win over any the caller's provenance names.
- A document that does not declare the matching `composition_sha256` (none, or another composition's) is refused with INVALID_INPUT before anything is written: **0 blobs, 0 index rows.**
  Evidence: `test_custody_writer_composed.py` 54 passed here (10 added by IB-pr-375: 5 persisted_by, 5 content-bound, one negative control each).
- The writes the persister reaches are unchanged in kind: the registry row `irpt-custody-x10-v1` is ACTIVE in the packaged registry (built replay: `registry_row_as_packaged.state` ACTIVE).
- PERFORMANCE and ANALYSIS retention and reads: unchanged in outcome (replay below). No new principal class, bucket, key prefix, route, IAM statement or function; two members of one existing function.
  Another firm's read stays refused with no body (`ReportDenied`, mapped to OBJECT_NOT_COVERED).

## Branch B (rolled back)

- `irpt-export-render`: redeploy the prior artifact -- S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-export-render.zip` version
  **`WiLXOyzMQ8_U42fSAeTIOwyMyw9.A9X3`** (latest at read time; 414177 bytes = the live CodeSize; written 2026-10-08T22:07:05Z), the zip whose `CodeSha256` is
  **`rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek=`** (IB-pr-374). Read live this session (`get-function-configuration`, LastModified 2026-10-08T22:11:43Z): unchanged; the downloaded
  version's sha256 equals that CodeSha256. A new upload makes a newer version, so rollback is a redeploy of THAT version through the Terraform deploy path, never a console edit.
- No route, IAM or data change to revert. Rolling back returns the function to records with no `persisted_by` and no content binding. Records written under Branch A keep their provenance keys; they
  are additive, and the rolled-back reader ignores them.

## Writers of each changed property

- `irpt-export-render` code zip (`CodeSha256`): the deploy path from the source map row only (`build-and-upload.sh` + Terraform `module.irpt_export_render`); 1 writer.
- `persisted_by` in a record's provenance: `custody_persist.custody_report_persist` only (the value is the verified principal id); `custody_write.persist_custody_report` stamps it. 1 caller, 1 stamper.
- `composition_sha256` in a record's provenance: the same single path, from `loaded["ref"]["sha256"]` of the retained request. The document's declared hash is compared, never stored in its place.
- Retained custody objects: `ReportRepository.persist`, reached through that Entry only. This release writes no data.

## Regression arm for the release order (IB-pr-374 form)

`replay/replay_zip.py` (python `-I`, one process per zip, no network, no credentials; every module is the zip's own). The LIVE zip is S3 version `WiLXOyz...` (sha256 `rNjtTwcm...`),
the BUILT zip is `7T29wPhz...`. Run here (outputs in `replay/`):
- The live code reserves one ANALYSIS and one PERFORMANCE fixture under `irpt-x10-v1`; both zips read them back with `repository.get`: both ok, none raised or refused, **identical
  `result_sha256`** (ANALYSIS `a7a8ae48...`, PERFORMANCE `04afa6c7...`); policy digest `e0046398e239...` identical.
- Negative control: the stored `policy_sha256` of each retention row altered; both zips refuse (`RetentionRefused: retention binding changed`) for ANALYSIS and PERFORMANCE.
- Built-only custody arm: packaged-registry round trip and other-firm refusal as in IB-pr-374 (see `replay/built_run.json`).
At the release order the arm is re-run against the zip actually uploaded, before the apply; a non-identical `result_sha256`, any raise on the x10 fixtures, or an unrefused negative control stops the apply.
The replay does not itself exercise `persisted_by` or the binding (the old fixtures call no custody persist); those are covered by the 54 passed tests above.
