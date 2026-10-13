# Never-widen sign-off packet -- IB-pr-515: irpt-directory-search rebuilt against its CURRENT live bytes (REFRESHED; supersedes IB-pr-499's packet, row D2-S28)

Prepared by 0.9.0_WK_IRPT_BCKEND~365 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO-IB-pr-515 (round 181, workstream ~P, decomposition cell IB-pr-515, CTO RE 7037: "round 181 = the directory-search apply, step 0 reads which home it reads; no home moves"). **Nothing here was uploaded, applied or deployed.** BUILD_ONLY from the committed tree at base 8168a663b8; the live zip read through `aws lambda get-function` (Code.Location, then a GET to scratch); the landed directory objects read by GET only (`aws s3api get-object` to scratch, counts only); the function configuration and the role's inline policies read by GET. No Lambda was invoked, nobody signed in, no vendor was called, no source map was written. No client data is in this packet or its tracked files: counts, sha256 and reason codes only.

**READ THIS FIRST.**

0. **Why this packet is refreshed.** The IB-pr-499 packet (`deliverables/0.9.0_WK_IRPT_BCKEND~349/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-499.md`) pinned the live zip at CodeSha256 `TefVhmGStCRorgQFrQFCS0lVUC+pXrWJYfdUCEExqe4=` (hex `4de7d586...`, last modified 2026-10-12T14:06:08Z). That live digest is STALE: the status-rule release (ledger `irpt-status-rule-all-eight-20261013`) redeployed `irpt-directory-search` at 2026-10-13T12:34:28Z. The CURRENT live CodeSha256 is `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=` (hex `b6faec43...`, 194476 bytes). The IB-pr-499 digest gate would STOP on it. This packet rebuilds the candidate against the current live bytes and supersedes IB-pr-499's live side and its Branch A digest gate. Its served change is unchanged from IB-pr-499.

1. **The served change, in words.** A directory search whose query matches an account's TAIL (its masked discriminator, for example the last four digits) returns that ACCOUNT's own entry, one per permitted account, each with that account's own mask. Two accounts sharing a tail give two entries. A pick of an ACCOUNT entry resolves to exactly that one account. Before the change a tail query matched only the relationship's entry-level mask (the head account's mask), so a tail of a non-head account matched nothing. A NAME query is unchanged in result: the relationship entry is returned and still resolves to all of its accounts. No figure moves: this changes what a last-four search returns and how a pick resolves.

2. **Permission is unchanged; nothing is widened.** `project()` drops every entry with no permitted account, and the tail-entry synthesis emits an entry only for an account that is both in the entry's account list and in the viewer's permitted set. No account is added to any set, no firm gains a read, no route, schema, environment, table, layer or IAM change.

3. **One member changes.** Built against the CURRENT live: 24 members each, 23 identical, **1 member differs: `handler.py`**. No member is in only one zip. The changed member's built sha256 equals the repo blob's at the pin (`8168a663b8`).

4. **The source map is NOT edited.** `handler.py` is a `files[]` member of `irpt-directory-search`, read from `infra/aws/lambda/investor-reporting/directory` at HEAD. The real `infra/aws/lambda/ci/lambda-source-map.json` sha256 is `82fc86efa59cbe8b8f514e2659f065b705ca9a80ee21a0a564a47afa2e9c365a` before the builds and after them (identical).

5. **The latent attribute mismatch (row `IRPT_BCKEND-D2-W349-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2; not disarmed here).** The staged `_authz/served.py` passes `load_report_owner` to `enforce.Enforcer`, whose staged pin does not accept it. The CURRENT live zip carries the same line, now at `served:876` (it read `served:856` at IB-pr-499, because the status-rule release changed the shared `served.py` on both sides). It is unreachable from this function, which never passes `render_ports`. It is not repaired in this release.

## Base, pin and the two zips

| item | value |
|---|---|
| base_commit (HEAD before the first commit of this order) | `8168a663b8c4766e43606eb86fea15e4894a1ea4` |
| pin_commit (the tree built from) | `8168a663b8c4766e43606eb86fea15e4894a1ea4` |
| function | `irpt-directory-search` (`infra/aws/lambda/ci/lambda-source-map.json`, entry `irpt-directory-search`; `artifact_sha256` `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=`, `last_deployed_commit` `1b88b22dea`, `last_deployed_at` 2026-10-13T12:34:28Z) |
| built sha256 (hex) | `ad71c30f3fd9858da9645b8b0dcacf8ac02cebd22e4ddea9f11c1f97186fc32c` (CodeSha256 form `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=`), 195435 bytes |
| live sha256 (hex, `$LATEST`, CURRENT) | `b6faec43ec3cdb48e9d69c6252862b8622826465675625136c1b0351b2441b7c` (CodeSha256 form `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=`), last modified 2026-10-13T12:34:28Z, 194476 bytes; the downloaded `Code.Location` zip hashes to it and equals the source map's `artifact_sha256` |
| built twice, byte-identical | YES (two BUILD_ONLY packs; `cmp` identical; both sha256 `ad71c30f...`) |
| changed members vs CURRENT live | 1 of 24: `handler.py` |

| changed member | built member sha256 | repo blob sha256 at the pin | CURRENT live member sha256 |
|---|---|---|---|
| `handler.py` | `d73af1c77aa3cd1d09ecaeb20ace35d776c98c88e15519236786a06725ad1387` | `d73af1c77aa3cd1d09ecaeb20ace35d776c98c88e15519236786a06725ad1387` | `3865775e75f812a9a513e1745b98dbce5ea94c9c717b2c6028a3084342b02987` |

Signature instrument `deliverables/0.9.0_WK_IRPT_BCKEND~365/signature_closure_attr.py` (copy of the `~278` instrument), run on each zip's own bytes:
- built: `signature_closure calls=40 checked=40 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=62 attr_mismatched=1` with `ATTR_MISMATCH: served:876 calls enforce.Enforcer -- unknown keyword(s) ['load_report_owner']` (rc 1)
- CURRENT live: the identical summary line and the identical ATTR_MISMATCH line (rc 1)

Signature mismatches: 0 on both zips. Attribute mismatches: 1 on built, 1 on live, the same line; built is not above live and every built line is a live line. This is the latent defect of point 5.

## Step 0 -- which directory home the function reads (READ ONLY; `directory_home` in `IB181-1_step0_and_replay.json`)

- **Function reads:** `IRPT_DIRECTORY_BUCKET_MAP` gives 49financial = `opal-data-bd`, cottonwood = `opal-data-cot`, inflection = `opal-data-inf`; `IRPT_DIRECTORY_PREFIX` gives `investor-reporting/directory`; the handler reads `<prefix>/latest.json` then the pointer's key (handler.py:52-53, :466).
- **Role grants:** `irpt-directory-role` inline policy `irpt-directory-policy` grants `s3:GetObject` on `opal-data-inf`, `opal-data-cot` and `opal-data-bd` under `investor-reporting/directory/*`. No attached managed policy.
- **Builder reads:** `holdings_snapshot.firm_bucket_map()` gives the same three buckets, and `_directory_account_ids` reads `investor-reporting/directory/latest.json` (PROD_PREFIX `holdings` mapped to `directory`), then the pointer's key. This is the read behind the 7639-of-7640 `account_id` snapshot (row `IRPT_BCKEND-D2-W364-S1`).
- **Result: MATCH = true.** Both homes are the same bucket and prefix per firm. No home moves in this release.
- **The canonical address.** The `address()` home `opal-data-49financial` (the observation W364-S1) is read by neither the function nor the builder. It is NOT adopted here (CTO RE 7037; its migration is its own project, rule 30 / R19).
- **The apply STOPS at its own step 0 until the CTO rules** only if the function's home and the builder's home ever differ. They do not today, so step 0 passes on this ground. The apply still waits on the ledger sequencing below.

## The open ledgers naming the function (sequencing; `open_ledgers_naming_the_function`)

- Thirty-five ledgers under `org/critical_paths/change_management/` name `irpt-directory-search`; **all 35 read CLOSED** at this HEAD. The two latest are `20261013T1225Z_irpt-status-rule-all-eight-20261013` (CLOSED 20261013T141000Z; the release that moved the live bytes; its control REPORT lines name the function) and `20261013T1521Z_irpt-status-rule-exercise-20261013` (CLOSED 20261013T154403Z).
- **One STALE OPEN marker.** `org/critical_paths/.open_deploys/irpt-status-rule-exercise-20261013.json` reads `OPEN` in the HEAD of two worktrees (`wk-irpt-anlreq-73`, `wk-irpt-dashbd-137`; blob `6fc2e06d`), while its change_management ledger reads CLOSED. Per the NEVER-2 law this proves only that those devices did not see completion. Row `IRPT_BCKEND-D2-W365-S1` is filed.
- No other open deploy marker names the function. The marker `irpt-s335-retry-schedule-20261005.json` (OPEN on two trees) names `irpt-directory-refresh-retry-daily`, a different function that shares the `source_dir`.
- **Sequencing:** the apply waits on (b) the exercise ledger's marker CLOSED, measured at apply time by the artifact (`git -C <tree> ls-tree -r HEAD org/critical_paths/.open_deploys/` over every live worktree, the marker's status read), and on the all-eight ledger staying CLOSED. An act that names a file another open deploy order names waits for that ledger to read CLOSED.

## The REACH per firm (read-only; landed directory objects; counts only)

The landed directory of each firm was read the way `holdings_snapshot._directory_account_ids` reads it (PROD prefix, `latest.json`, then the pointer's key), from GET-only scratch copies. All three firms had a PROD landed directory. Counts are over the WHOLE landed directory, not per viewer.

| firm | landed | entries | entries_with_masks | accounts | accounts_tail_addressable_after |
|---|---|---|---|---|---|
| 49financial | PROD | 4738 | 4738 | 7694 | 7694 |
| cottonwood | PROD | 271 | 271 | 870 | 870 |
| inflection | PROD | 295 | 294 | 863 | 863 |

Every account of the three landed directories carries a mask row except the one inflection entry without masks, which keeps its account head-addressable through its own entry. The counts moved from IB-pr-499's read (49financial 4732 entries, 7688 accounts; cottonwood 862 accounts) because the landed directories were re-published. The count of accounts whose tail was already addressable at base is NOT measured here; the table is the whole addressable population.

## The four replay arms (offline, SYNTHETIC; built `handler.py` against CURRENT live, each imported in memory from its own zip)

Instrument: `deliverables/0.9.0_WK_IRPT_BCKEND~365/ib181_replay_reach.py` (the synthetic shapes of `directory/tests/test_tail_account_entry.py`; `search()` and `resolve()` only; no Lambda invocation).

| arm | built verdict | CURRENT live verdict | expected-diff |
|---|---|---|---|
| tail of a non-head account | `account_entry` (1 result, kind ACCOUNT) | `no_match` | yes |
| shared tail | `two_account_entries` (2 results, kind ACCOUNT) | `no_match` | yes |
| name query | `relationship_entry` (1 result, kind RELATIONSHIP) | `relationship_entry` | no (unchanged) |
| entry without masks | `unchanged` (the pre-existing entry id) | `unchanged` | no (unchanged) |

The relationship entry resolves to all three of its accounts on the built zip (`relationship_reaches_all_accounts` true).

## Branch A -- land it (digest-gated, never a mint; NOT to be run by this worker)

1. **Gates before any act.** (a) The COO half and the CTO half both signed at THIS packet's bytes (section "The pair"); (b) the exercise ledger's marker reads CLOSED at apply time, measured by the artifact (open-ledger sequencing above); (c) step 0 reads MATCH at apply time. Any gate failing: STOP, no apply.
2. Open the NEVER-2 ledger entry first (`.tools/deploy_ledger.py open ...`) and commit its `.open_deploys` sentinel at once. It names EVERY task family that pulls this artifact: the function `irpt-directory-search` only. The sibling `irpt-directory-refresh` shares the `source_dir` but builds from its own files list and is not moved.
3. **START READ:** `aws lambda get-function` CodeSha256 must equal `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=`. Anything else: STOP, no apply.
4. Re-run `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-directory-search` and compare the printed sha256 to `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=`. ABORT on any difference: never upload a digest other than the one signed.
5. Then the same build without BUILD_ONLY (upload to `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-directory-search.zip`, verified by head-object), then the module's Terraform path (`infra/aws/terraform/investor-reporting/directory/lambda.tf`, module `irpt_directory_search`, `s3_object_version` and `source_code_hash` only; plan to a planfile showing 1 change and 0 to destroy; apply with `bash .tools/safe-apply.sh`). No IAM, route, schedule, layer, environment or table change.
6. **After:** live CodeSha256 equals `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=`; re-plan shows 0 changes; the census shows `changed_members` = `handler.py` against the pre-apply live zip; the direct proof below; close the ledger entry.

## Branch B -- restore the live version

- **What is restored:** the CURRENT live code, CodeSha256 `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=` (hex `b6faec43ec3cdb48e9d69c6252862b8622826465675625136c1b0351b2441b7c`), last modified 2026-10-13T12:34:28Z. It equals the `artifact_sha256` recorded in the source map at HEAD.
- **Named and re-read at apply:** the S3 object version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-directory-search.zip` whose content sha256 equals the live value is NOT read by this build (an S3 version listing is outside this order's allowed calls). The apply worker names that version at Branch A step 3, BEFORE any upload, writes it into the ledger entry, and re-reads at restore time that the CodeSha256 is still the live value and that version is still addressable.
- **Rollback per key:** one key, `investor-reporting/irpt-directory-search.zip`: redeploy that S3 version through the same Terraform path (`s3_object_version` and `source_code_hash`), never a console edit and never `aws lambda update-function-code`; then CodeSha256 equals the live value above and the re-plan is 0 changes. Nothing else is moved.
- **What the restore does to served values:** a tail query returns the relationship entry again (or nothing, for a non-head tail), as at base. No figure changed under either branch.
- **Trigger:** a 5xx or `TypeError` in the function's log group after the apply, a direct-invoke arm below that fails, or a figure that differs from its before-read: restore at once.

## The red list

`deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json` names two red tests: `_contracts/tests/test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve` and `...::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]`. Its `target_prefixes` are `infra/aws/lambda/investor-reporting/_contracts/` and `docs/contracts/investor-reporting/`; its `red_test_operations` is `analysis-request-original`. The one changed member, `infra/aws/lambda/investor-reporting/directory/handler.py`, intersects those target prefixes in **0** places and names a red operation in **0** places. STOP on this ground = no.

## The consumers of the search results (one read-through each, at HEAD 8168a663b8; portal tree `portal/src/pages/InvestorReporting/`)

| cite | reads | read-through |
|---|---|---|
| `contracts/envelope.ts:187` | `'directory-search'` maps each element of `data` through `adaptDirectoryEntry` | read; the only adapter the search response reaches |
| `contracts/adapt.ts:630-631` | `permitted_scope.scope_kind` gives the kind; `permitted_scope.scope_ids[0]` is the entry id | read; a synthesized ACCOUNT entry carries its one account id there |
| `contracts/wire/responses.ts:81-86` | the declared `DirectorySearchResponseWire.data` is `DirectoryEntryWire[]` | read; the declared envelope is rows with `permitted_scope`, not the function's top-level `entry_id` (point S2 below) |
| `header/search.ts:111-118` | `toOptionRow` copies `entry.entryId` and `entry.kind` | read |
| `header/search.ts:408` | `DirectorySearchRunner` calls `this.api.searchDirectory` | read |
| `header/ClientSearch.tsx:53` | the combobox option `value` is `row.entryId` | read |
| `header/selectionRequest.ts:8-18` | a pick sends `scope_kind` and `scope_ids` (ACCOUNT from `accountIds` only when `narrowedToAccount`); an ACCOUNT-kind row without narrowing throws at line 18 | read; the portal's pick path for a new ACCOUNT row is the consumer to watch at the apply |
| `tabs/analysis/GenerateComposer.tsx:83` | `api.searchDirectory` with `kinds: ['account']` | read; the query is empty there, so no tail match changes it |

No consumer reads a search result to decide a permission: each maps the scope, and the server's resolve decides the set.

## Direct-invoke proof, to run AFTER the apply (by `0.7.0_AE_CloudOps~IB2`, not by this worker)

A direct `aws lambda invoke` of the DEPLOYED function with an API-shaped `search` event for an Opal principal, the function's own role, no new grant, a READ operation only: one search by an account tail, over a SYNTHETIC directory (opaque ids and made-up masks), so no live data is read. Expected: one ACCOUNT entry whose `permitted_account_count` is 1; a `resolve` of its `entry_id` returns exactly that account. The apply order names the operation and states that it persists nothing. The response sha256 is recorded in the apply's scratch, not in the repo.

## Blast radius

- **Function:** `irpt-directory-search` only. **Member:** `handler.py` only (1 of 24).
- **Served effect:** a tail query returns ACCOUNT entries (one per permitted account); a pick of one resolves to that one account; a name query is unchanged in result; no figure moves.
- **Never-widen:** this MOVES a served behaviour (what a last-four search returns and how a pick resolves), so it ships only under the pair below. It widens nothing.

## The pair

Both halves sign the same facts: built `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=` (hex `ad71c30f...`), CURRENT live `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=` (hex `b6faec43...`), one changed member `handler.py`, the REACH table above, and the four-arm table above. A half that signs a different sha256 or different counts is void.

- **COO half -- `2.0.0_SA_COO~P2`:** signs that the built and live shas, the one changed member, the reach counts and the step-0 result equal this packet, and that the apply order carries the Branch A gates and the Branch B restore named above. Signed: ______________________  at: ____________
- **CTO half -- `1.0.0_SA_CTO~DELL2`:** signs the served change in words, the red-list reading, and the choice of Branch A. Signed: ______________________  at: ____________

Both halves are UNSIGNED at the time of writing. The apply is gated by (a) both halves signed at this packet's bytes, (b) the exercise ledger's marker CLOSED and the all-eight ledger CLOSED (open-ledger sequencing above), (c) step 0 MATCH at apply time.

## Rows

- `IRPT_BCKEND-D2-W349-S1` (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~P2`): the latent attribute mismatch. Stays ARMED; this build does not disarm it.
- `IRPT_BCKEND-D2-W365-S1` (OBSERVATION, INERT): the stale OPEN marker of the exercise ledger on two worktree HEADs against its CLOSED change_management ledger. The apply measures the artifact before it waits on that ledger.
- `IRPT_BCKEND-D2-W349-S2` (OBSERVATION, INERT, carried): the portal reader names `entry_id`; the function's search result carries top-level `entry_id` and no `permitted_scope`. The route layer that reshapes one into the other is outside this order's paths and was not read.

Files beside this packet: `IB181-1_release_census.json`, `IB181-1_step0_and_replay.json`, `ib171_4_member_diff.py` (copy), `ib181_replay_reach.py`, `signature_closure_attr.py` (copy), and the instance `IRPT_BCKEND.TO-IB-pr-515.directory-search-recensus-against-current-live-and-packet.proof_of_spec.json`.
