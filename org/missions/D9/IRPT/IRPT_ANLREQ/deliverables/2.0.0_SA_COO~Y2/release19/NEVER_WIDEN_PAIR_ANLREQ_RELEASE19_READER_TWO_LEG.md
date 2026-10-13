# IRPT_ANLREQ release 19 -- the template reader's release, ONE window, TWO legs (resident first, then `irpt-ycharts-generate`) -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No apply order exists and none is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-13. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Asked for by the CTO's round-19 analysis (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_19_20261013.md`
sections 1 to 4; msgs 6740, 6770, 6778). It disarms row `IRPT_ANLREQ-D2-W52-S33` (LIVE) and carries `-S35`.

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened; RELAYED = carried by another seat;
INFERRED = said so. A statement with none of these words is a plan, not a read.

## 1. What moves, in one paragraph

Two files, in two places, and nothing else: `intake/uploads.py` (sha256 `176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea`; today's `47f89e0b4660...`)
and `intake/template_reader.py` (sha256 `83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58`, `READER_VERSION irpt-template-reader.r18.1`; today's
`76795b75313b...`, which carries no `READER_VERSION`). The SAME two hashes are the moved members of both legs (RECORD: `AR-y-193`'s manifest and `AR-y-200`'s delta). Writers of those two files into a served package: **N = 2** -- the Lambda `irpt-ycharts-generate`
(the only function of 235 map entries that packages either, MEASURED by reading the map) and the resident package builder
`reports/build_resident_package.py`. Both are read below. Every other member of both packages stays at the bytes it has today.

## 2. Start state (the pinned pair is live in both places)

- **Lambda:** `irpt-ycharts-generate` CodeSha256 `NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM=`, LastModified 2026-10-12T14:13:41Z, 615247 bytes, 104 members
  (MEASURED 2026-10-13 ~04:3xZ: `get-function`, the zip downloaded and every member hashed). It is the package ADVI_FIRMBKTS act 4 deployed (ledger
  `20261012T1340Z_advi-firmbkts-fb-f-11-act4-irpt-leg-20261012`). S3 object `opal-313476888478-lambda-artifacts/investor-reporting/irpt-ycharts-generate.zip`
  version `_1MrCfPkpVkl7XDAC3NsbLhvIDvHBusc` (615247 bytes, 2026-10-12T13:50:27Z, latest; MEASURED). Its `uploads.py` is `47f89e0b4660...` and its
  `template_reader.py` is `76795b75313b...`: the same bytes as the pins the scratch run `AR-y-191` used as the start state (MEASURED by blob hash at
  `f09b802cdc` and `3f29017cfc`).
- **Resident:** root `0485393f3a-st32` (RECORD: YC2's st32 install, 2026-10-11). **The host was not read by this seat**; step 0 of the resident leg reads it.
- **Why the order of the legs matters (RECORD: `AR-y-191`, `reopen_matrix`, RUN in process):** an input stored by the pinned pair is accepted on re-open by
  the pinned pair (8 of 8) and by the moved pair (8 of 8); an input stored by the MOVED pair is REFUSED on re-open by the pinned pair
  (`TEMPLATE_ORIGINAL_BINDING`, 4 of 4). So the resident (which re-opens) moves FIRST: while the Lambda is still pinned it stores only pinned-stored inputs, which the moved
  resident accepts. The reverse order would let the moved Lambda store inputs the pinned resident refuses.
  A reader-only move (the reader without `uploads.py`) refuses all 8 pinned-stored inputs: that is why each leg moves BOTH files.

## 3. Artifacts, pins, rollback (per leg)

### 3a. Resident leg (applier: `0.7.0_AE_CloudOps~YC2`)

- **Tarball:** `irpt-resident-0485393f3a-r19.tar.gz`, sha256 `84df6479655c07ae6000af40404e53eb056b4c403aa9134bbe9c1521317d497a`, staged at
  `C:/dev/irpt-release-r19/` on dell2 (copy of `C:/dev/ar200-55-tarballs/two_member_clockheld.tar.gz`; MEASURED: `sha256sum`; extracted, its `SHA256SUMS` verifies, 297 members + the sums file).
  It is st32's recipe at st32's pin `0485393f3a` with ONLY `intake/uploads.py` and `intake/template_reader.py` taken from the release pin (RECORD: `AR-y-199` rebuilt all 298 st32
  members by name and content; `AR-y-200` delta, deliverable `RESIDENT_TWO_MEMBER_RELEASE.json`, drained @1f5fb3760f).
- **Delta against the st32 build, whole:** 298 compared, 294 unchanged, 4 differ -- the two reader members, `reports/resident_bindings.json` (only `provenance.member_overrides`;
  the bindings carry no root path), and `SHA256SUMS`; 0 only in either side; the minimal import set is EMPTY (51 import names resolve with st32 bytes).
- **Determinism:** two builds with the clock held to 2026-10-11T15:29:02Z: 298 of 298 files identical by name and sha256; the `tar.gz` hashes differ (gzip header clock), so the
  SHIPPED FILE is the control and its sha256 is the one above.
- **New root `/opt/irpt-resident/0485393f3a-r19`; rollback root `/opt/irpt-resident/0485393f3a-st32`** (the root running now; row `-S27`: the st32 script's own `OLD` is the st31 root and was changed).
- **Host script:** `deliverables/2.0.0_SA_COO~Y2/release19/resident_host_install_0485393f3a-r19.sh`, sha256 `8b53be1328f9ed20827e0118aee9c1b1b402d66b25d82a434275b1c83cfa57f0`, a copy of the
  st32 script (`resident_host_install_0485393f3a-st32.sh`) with 17 lines changed: the header comment, `NEW`, `OLD`, `WANT_TAR`, `written_by`, `ledger`. Every other line, including the
  17 member checks (MEASURED: all 17 hashes equal the extracted tarball's members), the library check, the empty-queue refusals (exit 20) and the automatic rollback to `$OLD`, is the st32 script's.
- **S3 object:** `ec2/investor-reporting-ycharts/resident/irpt-resident-0485393f3a-r19.tar.gz` in `opal-313476888478-lambda-artifacts` -- a NEW key; the applier proves it absent (`head-object` 404) before the upload and reads
  the sha256 back equal to the file.
- **Library and wrapper:** unchanged (`WANT_LIBRARY a1c28801...`, `WANT_WRAPPER 55ddb8f7...`). The host capture library is not moved by this release, so `W328-S1` (the repair lives in the host library) is not touched and `D2-S109`'s hold does not bite.

### 3b. Lambda leg (applier: `0.7.0_AE_CloudOps~AR2`, or whoever the CTO half names)

- **Function:** `irpt-ycharts-generate` (`module.irpt_ycharts_generate.aws_lambda_function.this`, `infra/aws/terraform/investor-reporting/ycharts/generate.tf`, role `irpt-ycharts-generate-role`). Writers of the function's code: **N = 1**
  (MEASURED: the source map's `tf_resource` for the entry; no other module names this function).
- **Build:** `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate` in a throwaway worktree DETACHED AT `5d8b0390ed` with the map patch
  `deliverables/0.9.0_WK_IRPT_ANLREQ~56/r19/RELEASE_MAP_PATCH_R2.diff` (git hash-object `df4d740e08c54566819a1b37942563df32f5a80e`) applied and uncommitted. A build from the trunk head is NOT the release: the head's map re-pins `loaders.py` (`0642c9d004` against the base's `69679b90e3`; `AR-y-193` `head_map_check`).
  Expected package: sha256 `6cd3c21b639ed6840cff3b638209ab7436dd97cdc202650470f9c1171963d919`, CodeSha256 (base64) `bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=`, 620712 bytes, 104 members (RECORD: `AR-y-201`, `LAMBDA_LEG_LIVE_REBASE.json`, drained @a011ddd400).
- **Why this build and not the one in `AR-y-193`:** `AR-y-193` pinned three native holds to commits older than what runs, because the census took the live natives from a record of 2026-10-11 and ADVI_FIRMBKTS act 4 replaced the package on 2026-10-12 (rows `IRPT_ANLREQ-D2-S66`, `-W56-S2`). `AR-y-201` re-read the live package from AWS and re-pinned the four holds to commits whose blobs equal the live members:
  `acceptance.py` and `submission_service.py` at `2f7cc7be42`, `durable_job.py` at `3acafb3f45`, `submission.py` at `1eed34a8c0` (each by blob sha256, MEASURED).
- **Control that the build is the live package plus two members:** the same base with ONLY the four hold rows builds CodeSha256 `NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM=` -- the live CodeSha256, byte for byte (RECORD: `AR-y-201`). The release differs from the live package in exactly `template_reader.py` and `uploads.py` (104 against 104 members, 0 only in either side).
  The applier's own build must print the expected CodeSha256 above; any other digest: ABORT before any upload, and compare member manifests (the record holds both).
- **Live / ROLLBACK object:** S3 version `_1MrCfPkpVkl7XDAC3NsbLhvIDvHBusc` of `investor-reporting/irpt-ycharts-generate.zip` (615247 bytes, CodeSha256 `NeAB50...`; MEASURED 2026-10-13 ~04:3xZ, latest). Rollback: copy that version onto the key (it is then the latest again) and a scoped apply, as the status release 5's rollback did; the digest is read back `NeAB50...`.
  The prior version `.epN9U3xZSMhU5WmEudwCrbjnydqg4N6` (2026-10-09, 614534 bytes) is NOT the rollback target: it is the package act 4 replaced.
- **Source map, in the close commit and not before:** `RELEASE_MAP_PATCH_R2.diff` applied to the trunk map (two reader pin moves, four added hold rows), plus the `artifact_*` and `last_deployed_*` record of the deploy. If the patch does not apply to the trunk map as it is, the applier resolves ONLY those six rows and stops on any other conflict. On rollback the six rows are not committed.
- **Terraform:** a scoped plan (`-target`) shows `Plan: 0 to add, 1 to change, 0 to destroy`, differing attributes `last_modified`, `s3_object_version`, `source_code_hash` only, environment equal (as act 4's L4 printed for the same function); `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.

## 4. Blast radius

### 4a. What a person meets (MEASURED offline, RECORD `AR-y-191`, run in process on Python 3.12)

| input | today (pinned pair) | after the moved pair |
|---|---|---|
| a two-account file (two account values in an account column) | NORMALIZED, no finding; two holdings with no account, total 300 (the sum across both) | NEEDS_CORRECTION, finding `ACCOUNT_COLUMN_SEVERAL_VALUES` |
| a file with a total row | NORMALIZED, three holdings (one named TOTAL), total 600 | NEEDS_CORRECTION, finding `TOTAL_ROW_PRESENT` |
| a one-account file, a repeated-header file, a two-sheet workbook (as the harness cases) | NORMALIZED | NORMALIZED (the same holdings); `HEADER_ROW_REPEATED` and `SHEETS_NOT_READ` are new findings for the cases that carry them |
| re-open of an input the PINNED pair stored | accepted | accepted (8 of 8) |
| re-open of an input the MOVED pair stored | -- | refused by the pinned pair (`TEMPLATE_ORIGINAL_BINDING`, 4 of 4); accepted by the moved pair |

- **Stored population (S35):** `TO-READS-Y9` (laptop, 2026-10-13T00:28:50Z): 56 stored template inputs (49financial 10, cottonwood 45, inflection 1), 0 turned back by the widened reader (r18.1), 0 unreadable.
  Step 0 re-counts at the window (R0d); a nonzero turned-back count stops the window.
- **Reach:** `irpt-ycharts-generate` ran 71, 70 and 12 invocations on 2026-10-10, 11 and 12 (partial) (MEASURED: CloudWatch `Invocations`, daily sum). Not every invocation is a template upload; 56 template inputs have been stored in total.
- **The first-hand effect of the release is a REFUSAL of files that were wrongly accepted.** Nothing a person already has is changed or deleted; no served output moves except the answer to a newly uploaded two-account or total-row file.

### 4b. The portal's readers of the upload door's answer (the defect release 5 of `irpt-status` was rolled back for)

RECORD, read by this seat from the committed records (`AR-y-202` `PORTAL_UPLOAD_ANSWER_READERS.json` @952de68f5d; `AR-y-203` `PORTAL_DEFER_SHAPE_READERS.json` @acfd654740), each re-run by this seat's check (`Y202-PORTAL-OK`, `Y203-DEFER-OK`) and proof (VALID):
- **Commits read:** portal `PROD` `37aa1247ee4ba487e5610dc5b78d65ae28468a99` and `DEV` `64980b4d3a1e11d8407b6a263ddcd5447dafaef2` (branch tips by `ls-remote`; the DEPLOYED bundles were not read).
- **17 readers** of the door's answer or the stored input's findings, run with bun against the portal's own functions: exact on the envelope keys and the `state` / `reason` members (`parseIrEnvelope` -> `adaptAnalysisUpload`, `envelope.ts` 246-273), open on finding words (shown as the server wrote them), tolerant on proxy codes and severity.
- **The body the deployed door serves for a template with an ERROR finding** is `_defer`'s (`uploads.py` 459-475: `reason` `TEMPLATE_FINDINGS`, findings with their correction words, `findings_total`, `template`). Built by importing the moved file's own `_with_correction_words` and constants, it was passed through the three readers that touch it at both commits: **36 of 36 RETURNED, 0 threw** (30 AFTER cases over 5 sheets, 6 BEFORE). The earlier cell's harness body (no `reason`) THREW at both commits on the key `reason` (rows `-W57-S1`, `-W57-S2`); that body is not what the deployed door serves (row `-W57-S3`), and the pair does not rest on it.
- **What a person sees (same at both commits):** `TOTAL_ROW_PRESENT` -- "Row 4: Row 4 is a total, not a holding. Remove the row and upload the file again; the report adds up your holdings itself."; `ACCOUNT_COLUMN_SEVERAL_VALUES` -- "Row 1: Column C holds more than one account, and one file can hold only one account. Split the sheet into one file per account (one account per file) and upload each file on its own."; `HEADER_ROW_REPEATED` -- "Row 3: Row 3 repeats the header row. Are the rows below it a second account? ...". `SHEETS_NOT_READ` is shown by NO reader (nothing refuses it and nothing shows it; row `-W57-S5`).
- **A difference between the two portal commits, named and not a refusal:** on PROD the ticket message reads "Review required: TEMPLATE_FINDINGS Nothing was filed." (the raw reason code), on DEV "Review required: the file needs a correction. Nothing was filed."; the finding lines carry the words on both. This is a client-facing page and this release does not change it (rows `-W58-S4`).
- **Not read:** the HTTP route (`upload_entry.handle`), the resident's resolution, the React render of any of these (READ at the cited lines, not rendered), the deployed bundles, and whether the owned-request view ever receives a door-shaped finding (that view reads no findings; the stored request's findings map takes `detail`, which the door's findings do not carry; row `-W57-S6`).
- **After-read C1 (the PROD readers on the LIVE body):** the first live body of each kind passes through `parseIrEnvelope` from the PROD commit and returns; if it throws, that is a stop (Branch: Lambda rollback), exactly as release 5's C1.

### 4c. Held at today's bytes and why (CTO rulings, analysis section 4)

- **Resident:** 294 of 298 members unchanged, named by the delta. The ones the CTO ruled on: `extract.py` (IRPT_BCKEND IB-pr-472) stays at st32 bytes, so the `SECTION_BOUNDS` switch is not reached and the extracted values do not move (RECORD: the member is among the 294 equal members; no before/after extraction read is owed because the member is unchanged);
  `ops/status.py`, `served.py`, `name_rulings.json` are not reached by the resident; `loaders.py` is equal to ADVI_FIRMBKTS act 4's release; `lib/opal_naming.py`, `firm_pages.json`, `scopes.json`, `exemptions.json` stay at st32 bytes (msg 6770). The 12 `ycharts/research` members of the full recipe are NOT added.
- **Lambda:** 102 of 104 members unchanged, by hash against the live package.
- **Not in this release (S31, S32):** the vocabulary widening and the value backstop are built later (`AR-y-194`, not cut) and ride the NEXT reader release by this same two-leg method. So THIS release does not close the class: a multi-account file whose account column is headed `Account Numbers`, `Subaccounts`, `Accnt`, `Account Nos`, `Account Seqno` or `Account Serial` is still accepted as one portfolio, exactly as today. The disarm of `-S33` covers the forms the r18.1 rule matches and no others.

## 5. Order of the window and the after-reads

Each read is recorded with its claim word; a missing read is `ABSENT`, and ABSENT is not EXERCISED.

**Step 0 (both appliers, within the hour before the first act):**
- R0a: this file and BOTH halves signed at the same blob; the applier's ledger entry opened (one per leg: `irpt-resident-r19-20261013`, `irpt-ycg-r19-reader-20261013`); no other open deploy entry names either surface (every live worktree read, per NEVER-2).
- R0b: the Lambda CodeSha256 reads `NeAB50...` and the S3 latest version is `_1MrCf...`. Otherwise ABORT: someone moved it after this file was written.
- R0c: the host: unit `irpt-analysis-resident.service` active on root `0485393f3a-st32`; library sha256 `a1c28801...`; wrapper `55ddb8f7...`; the rollback root exists; queue `irpt-generation` reads `0 0`.
- R0d: the stored-input recount (laptop `0.7.0_AE_CloudOps~ANL`, the `TO-READS-Y9` method): `turned_back` 0 of the count read; the number of inputs with a stored `reader_version` (expected 0). Otherwise STOP and bring the numbers to the CTO.

**Step 1, resident leg (`YC2`):** upload the tarball (new key), run the host script. Its own gates: empty queue (refuses and restores, exit 20), the 17 member checks, `node --check` of the library, the factory import, the unit restart, 30 seconds of polls with no traceback; any failure rolls back to `$OLD` automatically.
- P1: final `active`, polls in the last 30 s at least 1, tracebacks 0; the running root reads `0485393f3a-r19`.
- P2: at the running root `intake/uploads.py` sha256 `176682cb...` and `intake/template_reader.py` sha256 `83ab9b45...`; `READER_VERSION` reads `irpt-template-reader.r18.1`.
- P3: the host's regenerated `SHA256SUMS` lines for the 294 unchanged members equal the package's (host-added dependency files named, not compared); the cutover receipt names the new root and the manifest hash.
- P4: the queue is still `0 0` or any messages it holds are processed (a polled message after the cutover is the first work done by the moved resident).

**Step 2, Lambda leg (`AR2`):** build and compare (the expected CodeSha256), upload, scoped plan, `safe-apply`, ledger.
- L1: CodeSha256 reads `bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=`; the downloaded zip has 104 members; against the previous package exactly `template_reader.py` and `uploads.py` differ.
- L2: one invocation that carries no credentials: the refusal envelope equals the one read BEFORE the apply (status and body sha256).
- L3: the function's environment and role unchanged (the plan said so; read back one attribute list).

**Step 3, the door, live (S33):** ONE caller that can upload a template, with synthetic files only (the harness files of `AR-y-191`, no client data):
- D1: the two-account file answers NEEDS_CORRECTION with `ACCOUNT_COLUMN_SEVERAL_VALUES`; D2: the total-row file answers NEEDS_CORRECTION with `TOTAL_ROW_PRESENT`; D3: the one-account file answers NORMALIZED with the holdings and total the pinned pair gave; D4: re-open of one pinned-stored input is accepted (S35). A person looks at the page once for D1 and writes what the words say. **C1 (consumer):** the live bodies of D1 to D3 are passed through `parseIrEnvelope` from the portal PROD commit (the function, in a script; keys and counts recorded, no value): each returns; one throw is a stop and the Lambda rolls back.
- **OPEN FOR THE CTO HALF:** which caller and which firm, since each upload stores an input. This seat has no measured test profile to propose (the fences that blocked the synthetic TR-dp-24 request apply to uploads too, RECORD: the round-18 ruling); the pair authorizes no upload into a client's own firm, and the CTO half names the caller or says there is none. If no caller is named, D1 to D4 read `ABSENT`; the release stands, `-S33` is recorded RELEASED, NOT SHOWN LIVE, and stays on the CTO's list.

## 6. Both branches

- **All reads as expected:** close both ledgers (the record names each leg's last read and the window times); disarm `-S33` on D1 and D2 (or record RELEASED, NOT SHOWN LIVE); the map close commit; `-S35` answered by R0d and D4.
- **The resident leg fails:** the host script restores the old root itself; nothing else moved; the Lambda leg is NOT started. State: pinned in both places, as before.
- **The Lambda leg fails or any of L1 to L3 is false:** roll the Lambda back to `_1MrCf...` (above). The resident stays moved: the matrix says a moved resident accepts every input the pinned Lambda stores, so the mixed state (moved resident, pinned Lambda) is SAFE and is the state to wait in. No resident rollback is needed for a Lambda failure.
- **A defect found AFTER both legs are live, in either leg:** roll back the LAMBDA first, then the resident (a moved Lambda stores inputs the pinned resident refuses). Before the second rollback, count the inputs the moved pair stored (a laptop read: stored `reader_version` equal to `r18.1`, by firm): each is refused on re-open by the pinned pair with `TEMPLATE_ORIGINAL_BINDING`; none is lost, and the person uploads it again. The count goes in the record and to the CTO.
- **A person's report that a good file was turned back:** this is the value test's reason to exist (`-S31`, `-S32`): record the file's header words (no client data), roll nothing back for one report, and bring it to the CTO.

## 7. Limits named (accepted by the CTO, msg 6778, except where marked)

- **S25** (accepted): `uploads.py` declares 24 correction-word codes that `ops/status.py` at the held st32 bytes lacks. The resident does not reach `status.py`. MEASURED this session: the deployed `irpt-status` (CodeSha256 `JmOhV/ep4mR1mt2NKKqyUlohgO3mlDw1GEM4eAWYKdw=`, its `status.py` sha256 `cb3b2ea620...`) carries 4 correction words (`RESOLVE_PROVIDER_BUSY`, `RESOLVE_RETRY_EXHAUSTED`, `TICKER_DATA_NOT_ENTITLED`, `TICKER_NOT_FOUND`) and NONE of the 24: for those codes its `build_status_envelope` adds no `CORRECT` action (`status.py` lines 155-158: the words are looked up and the action is added only when found), so the status envelope shows the code without words. The all-eight status pair (`-W54-S5`) carries the current `status.py` to `irpt-status` as the fast follow.
- **S26** (accepted): the resident package carries none of the nine csv and xlsx fixtures the digest test reads; 5 of 5 pass with them restored; it touches no served path.
- **S27** (done): the rollback root is set in the host script.
- **Pinned door until the Lambda leg lands:** between Step 1 and Step 2 the Lambda still accepts two-account and total-row files as today (minutes). The window is short on purpose.
- **Not read by this seat:** the host (no ssh or SSM from this seat); the Lambda configuration beyond CodeSha256 and Code.Location; the portal PROD bundle as DEPLOYED (branch tips only); the words a person sees on the page for the codes (section 4b, if its cell reported).
- **Other maps:** the four native paths are also staged by three other map entries (`irpt-status`, `irpt-commentary-draft-store-lambda`, `irpt-commentary-composition-read-lambda`; row `-W56-S1`); this release does not touch them.

## 8. Owed before any apply order is cut

1. The CTO half on this file's blob, naming the caller for D1 to D4 and confirming the applier for the Lambda leg.
2. Andrew's word is NOT needed: no portal PROD push and no client-facing page changes in this release (the portal is read, not changed; section 4b states the PROD reader result).
3. R0a to R0d read as met at the window (they are the applier's step 0, not this seat's).
