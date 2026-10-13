# IRPT_ANLREQ release 21 -- the template reader r19.3 (the account-header allowlist), ONE window, TWO legs (resident, then `irpt-ycharts-generate`) -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No apply order exists and none is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-13. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Asked for by the CTO's round-21 analysis, section 3 items 1 and 4 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_21_20261013.md`). It follows the release-19 pair (`release19/NEVER_WIDEN_PAIR_ANLREQ_RELEASE19_READER_TWO_LEG.md`, blob 2140b9352c, both legs live) and carries rows `-S31` / `-S32` (the vocabulary and value backstop) to the release that was promised.

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened and re-ran its check and proof (named); RELAYED = carried by another seat; INFERRED = said so. A statement with none of these words is a plan.

## 1. What moves

ONE member in each leg: `intake/template_reader.py`, from sha256 `83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58` (`READER_VERSION irpt-template-reader.r18.1`, live in both places since release 19) to `a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35` (`irpt-template-reader.r19.3`; commit `55d1755d39`, the HEAD blob; MEASURED by `git show`). `intake/uploads.py` stays `176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea`, the bytes both legs hold now (MEASURED at HEAD; RECORD `AR-y-226`, `AR-y-227`, `AR-y-228`). Writers of the reader into a served package: **N = 2**, as in release 19 (the Lambda `irpt-ycharts-generate`, the resident builder), each read below.

## 2. Start state (all RECORD / MEASURED, re-read by the appliers at step 0)

- **Lambda:** `irpt-ycharts-generate` CodeSha256 `hpNfkhLtLRl0e9TFL+Vdr5kilZ1W8bN3GKMhlzmVXgg=`, 621567 bytes, 104 members, S3 latest version `ennO07toFOYlPWM64JC4MS9g.bVRr7fW` of 52 (MEASURED by this seat and by `AR-y-228`, 2026-10-13 ~15:5xZ). This is release 20's package (served.py status rule) on release 19's reader.
- **Resident:** root `0485393f3a-r19` (release 19's, the tarball `irpt-resident-0485393f3a-r19.tar.gz`, sha256 `84df6479655c07ae6000af40404e53eb056b4c403aa9134bbe9c1521317d497a`). The host was not read by this seat; step 0 reads it.
- **Order of the legs (RECORD `AR-y-226`, `REOPEN_AND_EFFECT.json`, run in process on the two reader files from git; check `Y226-EFFECT-OK`, proof VALID):** stored by r18.1 and re-opened by r19.3: 5 of 5 accepted; stored by r19.3 and re-opened by r18.1: 5 of 5 accepted; same-reader cells 5 of 5. No refusal in any cell, so a mixed state (one leg moved) is SAFE in either direction. The release-19 asymmetry (4 of 4 refused) belonged to the uploads/binding change and does not recur because `uploads.py` is unchanged. **Limit:** 5 inputs per cell (6 of 11 cases are turned back at the door and store nothing), below the 8 the order asked (row `W70-S2`). The sequence is nevertheless resident first, then Lambda: the resident re-opens, so it moves first, as in release 19, at no cost.

## 3. Artifacts, pins, rollback

### 3a. Resident leg (applier `0.7.0_AE_CloudOps~YC2`)

- **Tarball:** `irpt-resident-0485393f3a-r193.tar.gz`, sha256 `bb1f774922e05abada3895ad3c45c6ea131c688ffebf3f211209aa9d3d7c7fbc`, staged at `C:/dev/irpt-release-r193/` (MEASURED: this seat copied it from `C:/dev/ar227-71/tarballs/` and re-hashed both copies). It is the release-19 tarball with ONLY `intake/template_reader.py` replaced (RECORD `AR-y-227`, `RESIDENT_ONE_MEMBER_RELEASE.json`, drained @b26dc1f451; check `Y227-RESIDENT-OK`, proof VALID).
- **Delta against the release-19 tarball, whole:** 3 of 298 members differ -- `intake/template_reader.py`, `reports/resident_bindings.json` (only `provenance.member_overrides`; the bindings carry no root path) and `SHA256SUMS`; no member added or removed; determinism 298 of 298 files identical across two builds (the `tar.gz` hash is the shipped-file control).
- **New root `/opt/irpt-resident/0485393f3a-r193`; rollback root `/opt/irpt-resident/0485393f3a-r19`** (the root running now).
- **Host script:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~71/r21/resident_host_install_0485393f3a-r193.sh`, sha256 `edd10a4bf5af03c8ed109f83ccc5ffbe9654edde7dac9a71e189d952d812603c`, also staged at `C:/dev/irpt-release-r193/`. It is release 19's script (sha256 `8b53be13...`, checked by the worker) with 4 hunks: `NEW`, `OLD`, `WANT_TAR`, the ledger name and the header, plus ONE added member check for `intake/template_reader.py` (release 19's script had none for the reader member, row `W71-S4`); 18 member checks, all equal to the tarball's members (RECORD). Every gate of release 19's script stands: empty-queue refusal (exit 20), the member checks, `node --check` of the library, the factory import, the unit restart, 30 s of polls with no traceback, automatic rollback to `$OLD`.
- **S3 object:** `ec2/investor-reporting-ycharts/resident/irpt-resident-0485393f3a-r193.tar.gz` in `opal-313476888478-lambda-artifacts` -- a NEW key; the applier proves it absent (`head-object` 404) and reads the sha256 back equal to the file.
- **Library and wrapper:** unchanged (`WANT_LIBRARY a1c28801...`, `WANT_WRAPPER 55ddb8f7...`).

### 3b. Lambda leg (applier `0.7.0_AE_CloudOps~AQ2`)

- **Function:** `irpt-ycharts-generate` (`module.irpt_ycharts_generate.aws_lambda_function.this`, `infra/aws/terraform/investor-reporting/ycharts/generate.tf`). Writers of its code: **N = 1** (the source map's `tf_resource`, as in release 19).
- **Build:** `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate` in a throwaway worktree DETACHED AT `4067c2dd5b` (guard: `git show 4067c2dd5b:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` = 8, printed before each build) with ONE map patch applied uncommitted: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~72/r21/RELEASE_MAP_PATCH_R3.diff` (git hash-object `5be34a0f17006dba3e7c3ac3cb171437a63cc6dd`). The patch is the release-20 `irpt-ycharts-generate` map change (the `served.py` row, pin `564e6048`) PLUS the one r19.3 hunk: the reader pin to `55d1755d39` AND its declared sha256 together (the builder refuses a pin whose blob differs from the declared hash, row `W72-S1`). It is the diff of the worker's release worktree, so it replaces the release-20 diff, it is not applied after it. The no-move control is the same base with the release-20 diff `irpt-ycharts-generate.release.diff` (git hash-object `3b85d26d1f`, in `deliverables/0.9.0_WK_IRPT_ANLREQ~64/r20/` or `~61/r20/`) alone.
- **Expected package:** CodeSha256 `TU9m6Bivz32whSIQ7HvEbnPhw5W33+UVZTqtgXRaP3E=`, 624069 bytes, 104 members; against the live package exactly `template_reader.py` differs (RECORD `AR-y-228`, `LAMBDA_LEG_R193.json`, drained @f187d007c1; check `Y228-LAMBDA-OK`, proof VALID). The no-move control (same base, release-20 diff only) reproduces the live `hpNfkhLt...` byte for byte. Any other digest from the applier's own build: ABORT before any upload and compare member manifests.
- **Upload.** The real upload is the same script WITHOUT `BUILD_ONLY`, from the same worktree, only after the digest equals the expected value. **The script's verify step is fixed in `AR-y-229` (@25e92d4daa) and its live proof is open** (see section 7): until the second scratch-key arm (`TO-SCRATCH-R21b`) reads clean, the applier reads the uploaded object back by VersionId and sha256 itself (as release 20 did) and treats a script exit 1 after a good upload as the known defect, never as a failed upload.
- **Rollback object:** S3 version `ennO07toFOYlPWM64JC4MS9g.bVRr7fW` of `investor-reporting/irpt-ycharts-generate.zip` (the live package, CodeSha256 `hpNfkhLt...`). Rollback: copy that version onto the key, scoped plan, `safe-apply`, read `hpNfkhLt...` back.
- **Source map, in the close commit and not before:** the reader row only (pin and sha256), plus the `artifact_*` and `last_deployed_*` record. On rollback it is not committed.
- **Terraform:** a scoped plan (`-target`) shows `Plan: 0 to add, 1 to change, 0 to destroy`, attributes `last_modified`, `s3_object_version`, `source_code_hash` only, environment equal; `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.

## 4. Blast radius -- what a person meets (RECORD `AR-y-226`, 32 header and harness cases run through BOTH readers; MEASURED offline)

| input | today (r18.1) | after (r19.3) |
|---|---|---|
| a two-account file whose account column is headed `Accnt`, `Acct Alias` or `Primary Acct` (two identifier-like values) | NORMALIZED, no finding (two holdings, no account, the sum across both) | NEEDS_CORRECTION, `ACCOUNT_COLUMN_SEVERAL_VALUES` |
| the same under `Acct` or `Account Number` | NEEDS_CORRECTION (already) | NEEDS_CORRECTION |
| a one-account file whose column is headed by an attribute of an account (16 constructed headers: `Acct Market Value`, `Acct CUSIP`, `Acct Lot`, `Accnt Value`, `Acct Status`, `Acct Type`, `Acct Name`, `Acct Holder`, `Acct Balance`, `Acct Opened`, and the CVO's six neighbours `Acct Cost Basis`, `Acct Gain`, `Acct Weight`, `Acct Description`, `Acct Currency`, `Acct Custodian`) | NORMALIZED | NORMALIZED (none turned back) |
| the harness cases (two-account csv, total row, repeated header, two-sheet workbook, brokerage two-account, one-account sheets) | as today | the same outcome in all 11 |
| re-open of any stored input | accepted | accepted (matrix above) |

- **A header the allowlist does not name is NOT turned back, whatever its values** (the CTO's round-21 ruling): `Acct Ref Ext` is the worked case, pinned by a test. So the class is not closed by this release: a two-account file under a header with an unlisted word is still accepted as one portfolio. The forms the earlier pair named (`Account Numbers`, `Subaccounts`, `Account Nos`, `Account Seqno`, `Account Serial`) were NOT re-run by this seat in this round (the allowlist cell's controls name its own positives and negatives; these forms are not among them). They stay as the earlier pair described them unless the CTO half says otherwise.
- **The first-hand effect is a REFUSAL of files that were wrongly accepted.** Nothing a person already has is changed or deleted; no served output moves except the answer to a newly uploaded file of the three header forms above.
- **Portal readers of the door's answer (release 19 section 4b):** the finding codes and correction words are the same codes as release 19 (`ACCOUNT_COLUMN_SEVERAL_VALUES` is released already); this release adds no code, so the 17 readers and the 36-of-36 result stand by reference (RECORD, `PORTAL_UPLOAD_ANSWER_READERS.json`, `PORTAL_DEFER_SHAPE_READERS.json`, portal commits as release 19 read them). Not re-run by this seat for this release; the after-read C1 below re-reads the live bodies.
- **Stored population:** 56 stored template inputs (49financial 10, cottonwood 45, inflection 1) at 2026-10-13T00:28:50Z under r18.1, 0 turned back (RELAYED, `TO-READS-Y9`). **r19.3 has not been run on the stored population** (the allowlist cell read no client headers); step R0d does it.

## 5. Order of the window and the after-reads

Each read carries its claim word; a missing read is `ABSENT`, and ABSENT is not EXERCISED.

**Step 0 (both appliers, within the hour before the first act):**
- R0a: this file and BOTH halves signed at the same blob; one NEVER-2 ledger per leg (`irpt-resident-r193-20261013`, `irpt-ycg-r193-reader-20261013`); no open deploy entry in any live worktree names either surface (every worktree read).
- R0b: the Lambda CodeSha256 reads `hpNfkhLt...` and the S3 latest version `ennO07to...`; otherwise ABORT.
- R0c: the host: unit `irpt-analysis-resident.service` active on root `0485393f3a-r19`; library `a1c28801...`; wrapper `55ddb8f7...`; the rollback root exists; queue `irpt-generation` reads `0 0`.
- R0d: the stored-input recount with the r19.3 reader, `TO-READS-Y9` / `-Y10` method (counts and dates only, by tenant code; the number of inputs with a stored `reader_version`). It needs `kms:Decrypt` on the IRPT key, which dell2 does not hold (RELAYED, the Y10 order); **it runs on a Dell CloudOps lane once the Dell identities' grants land (`2.0.0_SA_COO~C`, round 12), never on a laptop seat (Andrew-direct, msg 6938).** `turned_back` 0 of the count read; any non-zero stops the window and goes to the CTO. If no Dell lane can run it at the window, R0d reads ABSENT and **the window does not open unless the CTO half says to proceed on ABSENT** (see section 8).

**Step 1, resident leg (`YC2`):** upload the tarball (new key), run the host script. P1: final `active`, polls in the last 30 s at least 1, tracebacks 0; the running root reads `0485393f3a-r193`. P2: at the running root `intake/template_reader.py` sha256 `a61cd0c6...` and `intake/uploads.py` sha256 `176682cb...`; `READER_VERSION` reads `irpt-template-reader.r19.3`. P3: the regenerated `SHA256SUMS` for the unchanged members equals the package's. P4: the queue is `0 0` or its messages are processed.

**Step 2, Lambda leg (`AQ2`):** build and compare (expected CodeSha256), upload, read back by VersionId and sha256, scoped plan, `safe-apply`, ledger. L1: CodeSha256 reads `TU9m6Bivz32whSIQ7HvEbnPhw5W33+UVZTqtgXRaP3E=`; the zip has 104 members; against the previous package only `template_reader.py` differs. L2: one invocation without credentials: the refusal envelope equals the one read BEFORE the apply (status and body sha256). L3: environment and role unchanged.

**Step 3, the door, live (`-S33`, release 19 section 5 step 3):** ONE caller that can upload a template, synthetic files only: D1 a two-account file under `Accnt` (and, if the caller can, `Acct Alias`) answers NEEDS_CORRECTION with `ACCOUNT_COLUMN_SEVERAL_VALUES`; D2 a one-account file under `Acct Market Value` answers NORMALIZED; D3 the harness one-account file answers NORMALIZED with the holdings and total the pinned pair gave; D4 re-open of one r18.1-stored input is accepted. **C1 (consumer):** the live bodies of D1 to D3 pass through `parseIrEnvelope` from the portal PROD commit; one throw is a stop and the Lambda rolls back. **OPEN FOR THE CTO HALF, as in release 19:** which caller and which firm, since each upload stores an input; this seat has no measured test profile to propose and the pair authorizes no upload into a client's own firm. With no caller named, D1 to D4 read `ABSENT`, the release stands and the earlier rows are recorded RELEASED, NOT SHOWN LIVE.

## 6. Both branches

- **All reads as expected:** close both ledgers; disarm `IRPT_ANLREQ-D2-W52-S33` and `-S31`/`-S32` on D1/D2 (or record RELEASED, NOT SHOWN LIVE); the map close commit; `-S35` answered by R0d and D4.
- **The resident leg fails:** the host script restores `$OLD` itself; the Lambda leg is NOT started; state: r18.1 in both places.
- **The Lambda leg fails or L1 to L3 is false:** roll the Lambda back to `ennO07to...`. The resident stays moved: the matrix shows a mixed state is safe (5 of 5 in both directions), so it is the state to wait in.
- **A defect found AFTER both legs are live:** roll back the Lambda first, then the resident; no input stored by r19.3 is refused by r18.1 (matrix), so no stored-input count is owed before the second rollback.
- **A person's report that a good file was turned back:** record the file's header words (no client data), roll nothing back for one report, bring it to the CTO. This is the allowlist's reason to exist: it turns back only the headers it names.

## 7. Limits named

- **Not read by this seat:** the host (no ssh or SSM from this seat); the Lambda configuration beyond CodeSha256 and Code.Location; the portal PROD bundle as deployed; the stored population under r19.3 (R0d); real client headers (none were read; the controls are constructed).
- **The ci script's live proof is open.** `TO-SCRATCH-R21` (the first live run) FAILED on the old fix (a shim WARN line on stderr was merged into the compared value); the second fix is drained (@25e92d4daa) and its live arm `TO-SCRATCH-R21b` is cut but not reported. If it has not read clean at the window, section 3b's rule stands (read back by VersionId and sha256; a script exit 1 after a good upload is the defect, not a failed upload).
- **Test caveats of the resident build** (RECORD `AR-y-227`): the reader's tests on the extracted package read 135 passed, 2 failed; both failures are the CTO-accepted limits from release 19 (S26: nine fixtures not packaged; S25: the held `ops/status.py` lacks 24 correction words the release `uploads.py` declares). The stored-input contract test needs the repository object store to read one commit (`GIT_DIR`); five tests fail without it. The run is therefore not purely against the extracted package (rows `W71-S2`, `W71-S3`).
- **5 inputs per matrix cell**, not 8 (row `W70-S2`).
- **Unchanged and still open from release 19:** S25, S26 as above; the PROD portal's raw-reason-code ticket message (a client-facing page this release does not change).

## 8. Owed before any apply order is cut

1. The CTO half on this file's blob, naming (a) the caller for D1 to D4 (or none), (b) the applier of the Lambda leg (`AQ2` here), and (c) **whether the window may open with R0d ABSENT**: the recount needs a Dell lane with `kms:Decrypt`, whose grants land with `2.0.0_SA_COO~C` round 12. This seat's recommendation: **R0d is a hard gate** (a turned-back stored input is the one outcome this release must not cause), so the window waits for the grant; the apply orders are cut when the CTO half is in the tree and the recount lane exists.
2. Andrew's word is NOT needed: no portal PROD push and no client-facing page changes in this release.
