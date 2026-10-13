# Never-widen sign-off packet -- IB-pr-499: irpt-directory-search rebuilt so a tail query returns the ACCOUNT entry (row D2-S28)

Prepared by 0.9.0_WK_IRPT_BCKEND~349 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO-IB-pr-499 (CTO ROUND-171 ANALYSIS msg 6764, section 2 item 2; DSGN_IRPTV1 ROUND-31 ANALYSIS section 2a, row D2-S28; the order's AMENDMENT 1 on the latent attribute mismatch). **Nothing here was uploaded, applied or deployed.** BUILD_ONLY from a committed tree; offline replays on a SYNTHETIC directory; AWS reads only: the live zip through `aws lambda get-function` (Code.Location, then the zip GET), and S3 GET of each firm's landed directory pointer and directory object, read in memory, counts only. No Lambda was invoked, nobody signed in, no vendor was called. No client data is in this packet or its files: counts, sha256 and reason codes only.

**READ THIS FIRST.**

1. **The served change, in words.** A directory search whose query matches an account's TAIL (its masked discriminator, for example the last four digits) now returns that ACCOUNT's own entry, one per permitted account, each carrying that account's own mask. Two accounts sharing a tail give two entries (each its own account; masks that are identical read as ambiguous, as before). A pick of an ACCOUNT entry resolves to exactly that one account. Before the change a tail query matched only the relationship's entry-level mask, which is the HEAD account's mask, so a tail of a non-head account matched nothing and a tail of the head account returned the relationship entry. A NAME query is unchanged in result: the relationship entry is returned on a name match and still resolves to all of its accounts. No figure moves: this changes what a last-four search returns and how a pick resolves.
2. **Permission is unchanged; nothing is widened.** `project()` drops every entry with no permitted account, and `tail_account_entries()` synthesizes an entry only for an account that is both in the entry's account list and in the viewer's permitted set (handler.py, the `permitted`/`member` gate). A tail query for an account the viewer may not see matches nothing (the test file's arm 8). No account is added to any set, no firm gains a read, no route, schema or IAM changes.
3. **One member changes.** Built against live: 24 members each, 23 identical, **1 member differs: `handler.py`**. No member is in only one zip. The changed member's built sha256 equals the repo blob at the pin.
4. **The source map is NOT edited.** `handler.py` is a `files[]` member of `irpt-directory-search`, read from `infra/aws/lambda/investor-reporting/directory` at HEAD, so the real map builds it with no candidate map. The real `lambda-source-map.json` sha256 is `a8c55c584d0f346bbf552dad63871a040e8eb12a8774d613ccf160126b739987` before and after the builds (byte-identical).
5. **The latent attribute mismatch (AMENDMENT 1; row `IRPT_BCKEND-D2-W349-S1`).** The staged `_authz/served.py` (pin `74a62fb46c`) passes `load_report_owner` to `enforce.Enforcer`, whose staged pin (`f9a00f732c`) does not accept it. The LIVE zip carries the same line. It is unreachable from this function: `served.py` reaches the call only when `render_ports` is not None, and this function's entry never passes `render_ports` (the issuer read the entry and grepped the function's folder). The repair of that pin pair is a SEPARATE later cell, the issuer's; it is never repaired inside this release, because repairing it here would widen this release.

## Base, pin and the two zips

| item | value |
|---|---|
| base_commit (HEAD before the first commit of this session) | `f41501ab1d94db5d3009ded9c0e462909483475c` |
| pin_commit (the tree built from; `directory/` is byte-identical at `f91aedd1ef`) | `f41501ab1d94db5d3009ded9c0e462909483475c` |
| function | `irpt-directory-search` (`infra/aws/lambda/ci/lambda-source-map.json`, entry `irpt-directory-search`; its `source_dir` is shared with `irpt-directory-refresh`, which this release does NOT touch) |
| built sha256 (hex) | `ea1ac36d051602354cb5d25c238c66e11a2c228bb3757118eb7797ff07a9dac3` (CodeSha256 form `6hrDbQUWAjVMtdJcI4xm4RosIouzdXEY63eX/wep2sM=`), 194580 bytes |
| live sha256 (hex, `$LATEST`) | `4de7d5866192b42468ae0405ad01424b4955502fa95eb58961f754084131a9ee` (CodeSha256 form `TefVhmGStCRorgQFrQFCS0lVUC+pXrWJYfdUCEExqe4=`), last modified 2026-10-12T14:06:08Z, 193621 bytes; the downloaded `Code.Location` zip hashes to it |
| built twice, byte-identical | YES (two BUILD_ONLY packs; `cmp` identical; both sha256 `ea1ac36d...`) |
| changed members vs live | 1 of 24: `handler.py` |

| changed member | built member sha256 | repo blob sha256 at the pin | live member sha256 |
|---|---|---|---|
| `handler.py` | `d73af1c77aa3cd1d09ecaeb20ace35d776c98c88e15519236786a06725ad1387` | `d73af1c77aa3cd1d09ecaeb20ace35d776c98c88e15519236786a06725ad1387` | `3865775e75f812a9a513e1745b98dbce5ea94c9c717b2c6028a3084342b02987` |

Signature instrument `deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py`, run at its own path on each zip's own bytes:
- built: `signature_closure calls=40 checked=40 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=62 attr_mismatched=1`, with `ATTR_MISMATCH: served:856 calls enforce.Enforcer -- unknown keyword(s) ['load_report_owner']` (rc 1)
- live: the identical summary line and the identical ATTR_MISMATCH line (rc 1)

Signature mismatches: 0 on both zips. Attribute mismatches: 1 on built, 1 on live, the same line (built is not above live; every built line is a live line). This is the latent defect of point 5, not a new one.

## The REACH per firm (read-only; landed directory objects; counts only)

The landed directory of each firm was read the way `holdings_snapshot._directory_account_ids` reads it (the firm bucket from `hs.firm_bucket_map()`, `investor-reporting/directory/latest.json`, then the pointer's key), in memory. All three firms had a PROD landed directory. Counts are over the WHOLE landed directory, not per viewer.

| firm | landed | entries | entries_with_masks | accounts | accounts_tail_addressable_after |
|---|---|---|---|---|---|
| 49financial | PROD | 4732 | 4732 | 7688 | 7688 |
| cottonwood | PROD | 271 | 271 | 862 | 862 |
| inflection | PROD | 295 | 294 | 863 | 863 |

Reading the table: every account of the three landed directories carries a mask row, so each becomes tail-addressable as its own ACCOUNT entry. The one inflection entry without masks keeps its account head-addressable through its own entry, which the count includes. The count of accounts whose tail was already addressable at base (the head account of each masked relationship) is NOT measured by this build; the table is the whole addressable population, not the moved subset.

## Branch A -- land it (digest-gated, never a mint)

1. Open the NEVER-2 ledger entry first (`.tools/deploy_ledger.py open ...`) and commit its `.open_deploys` sentinel at once. It names EVERY task family that pulls this artifact: the function `irpt-directory-search` only. The sibling `irpt-directory-refresh` shares the `source_dir` but builds from its own files list and is not moved; the apply order must record that its artifact keeps its own `handler.py` bytes.
2. **START READ:** `aws lambda get-function` CodeSha256 must equal the live value above (`TefVhmGStCRorgQFrQFCS0lVUC+pXrWJYfdUCEExqe4=`). Anything else: STOP, no apply.
3. No source-map edit is needed (point 4). Re-run `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-directory-search` and compare the printed sha256 to `6hrDbQUWAjVMtdJcI4xm4RosIouzdXEY63eX/wep2sM=`. **ABORT on any difference: never upload a digest other than the one signed, never mint a new artifact in place of it.**
4. Then the same build without BUILD_ONLY (upload to `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-directory-search.zip`, verified by head-object), then the module's Terraform path (`infra/aws/terraform/investor-reporting/directory/lambda.tf`, module `irpt_directory_search`, `s3_object_version` and `source_code_hash` only; plan to a planfile showing 1 change and 0 to destroy; apply with `bash .tools/safe-apply.sh`). No IAM, route, schedule, layer, environment or table change.
5. **After:** live CodeSha256 equals `6hrDbQUWAjVMtdJcI4xm4RosIouzdXEY63eX/wep2sM=`; re-plan shows 0 changes; the census shows `changed_members` = `handler.py` against the pre-apply live zip; the direct proof below; close the ledger entry.

## Branch B -- restore the live version

- **What is restored:** the live code, CodeSha256 `TefVhmGStCRorgQFrQFCS0lVUC+pXrWJYfdUCEExqe4=` (hex `4de7d5866192b42468ae0405ad01424b4955502fa95eb58961f754084131a9ee`), last modified 2026-10-12T14:06:08Z. It equals the `artifact_sha256` recorded in the source map at HEAD.
- **Named and re-read at apply:** the S3 object version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-directory-search.zip` whose content sha256 equals the live value is NOT read by this build (an S3 version listing of the artifact bucket is outside this order's allowed calls). The apply worker names that version at Branch A step 2, BEFORE any upload, writes it into the ledger entry, and re-reads at restore time that the CodeSha256 is still the live value and that version is still addressable.
- **Rollback per key:** one key, `investor-reporting/irpt-directory-search.zip`: redeploy that S3 version through the same Terraform path (`s3_object_version` and `source_code_hash`), never a console edit and never `aws lambda update-function-code`; then CodeSha256 equals the live value above and the re-plan is 0 changes. Nothing else is moved, so nothing else is restored: no table, route, IAM or layer.
- **What the restore does to served values:** a tail query returns the relationship entry again (or nothing, for a non-head tail), as at base. No figure changed under either branch.
- **Trigger:** a 5xx or `TypeError` in the function's log group after the apply, a direct-invoke arm below that fails, or a figure that differs from its before-read: restore at once.

## The ADDENDUM 18 red list

`deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json` names two red tests: `_contracts/tests/test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve` and `...::test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]`. Its `target_prefixes` are `infra/aws/lambda/investor-reporting/_contracts/` and `docs/contracts/investor-reporting/`; its `red_test_operations` is `analysis-request-original`.

The changed member is `infra/aws/lambda/investor-reporting/directory/handler.py`. Intersection with the target prefixes: **0** (the member is under `.../investor-reporting/directory/`, not under `_contracts/` or `docs/contracts/`). Naming a red operation: **0** (the member's path names no operation). `handler.py` touches none of the red list's targets. STOP = **no** on this ground. The packet does not cite "suite green".

## The replay arms (offline, SYNTHETIC; four arms, built zip's `handler.py` against the live zip's, each imported in memory from its own zip)

Instrument: `deliverables/0.9.0_WK_IRPT_BCKEND~349/ib171_4_replay_reach.py` (the synthetic shapes of `directory/tests/test_tail_account_entry.py`, re-stated; `search()` and `resolve()` only; no Lambda invocation).

| arm | query shape | built verdict | live verdict | expected-diff |
|---|---|---|---|---|
| tail of a non-head account | tail of a non-head account | `account_entry` (1 result, kind ACCOUNT, resolves to that one account) | `no_match` | yes |
| shared tail | tail shared by two accounts of two entries | `two_account_entries` (2 results, kind ACCOUNT, each resolves to one account) | `no_match` | yes |
| name query | the relationship's name | `relationship_entry` (1 result, kind RELATIONSHIP) | `relationship_entry` | no (unchanged) |
| entry without masks | the tail of an entry with no `account_masks` | `unchanged` (the pre-existing entry id) | `unchanged` | no (unchanged) |

Also measured on the built zip: the relationship entry resolves to all three of its accounts (`relationship_reaches_all_accounts` true). The head-account tail arm of the test file (a tail equal to the head's mask returns the head ACCOUNT entry, not the relationship) is covered by the test file and was not a separate arm of this order.

## The consumers of the search results, each with one read-through (portal tree in this worktree, `portal/src/pages/InvestorReporting/`)

| cite | reads | read-through |
|---|---|---|
| `contracts/envelope.ts:187` | `'directory-search'` maps each element of `data` through `adaptDirectoryEntry` | read; the only adapter the search response reaches |
| `contracts/adapt.ts:630` | `wire.permitted_scope.scope_kind` gives the entry kind | read; the ACCOUNT synthesized entry carries `scope_kind` ACCOUNT, so it maps to kind `account` |
| `contracts/adapt.ts:631` | `wire.permitted_scope.scope_ids[0]` is the entry id the reader keeps | read; the reader reads NO `entry_id` member. For a synthesized ACCOUNT entry `scope_ids[0]` is that one account id, so two account entries of one shared tail carry two distinct ids |
| `contracts/wire/responses.ts:81-86` | the declared `DirectorySearchResponseWire`: `data` is `DirectoryEntryWire[]` | read; the declared envelope is rows with `permitted_scope`, not the function's `results[]` with top-level `entry_id` (see S2) |
| `header/search.ts:111-118` | `toOptionRow` copies `entry.entryId` and `entry.kind` into the search row | read |
| `header/search.ts:408` | `DirectorySearchRunner` calls `this.api.searchDirectory` (the one operation it may call) | read |
| `header/ClientSearch.tsx:53` | the combobox option `value` is `row.entryId` | read |
| `header/selectionRequest.ts:8-18` | a pick sends `scope_kind` and `scope_ids` built from the selection (ACCOUNT from `accountIds` when `narrowedToAccount`; CLIENT from `clientId`; RELATIONSHIP from `relationshipId`); it sends no `entry_id`; an ACCOUNT-kind row without `narrowedToAccount` throws at line 18 | read; a pick of a new ACCOUNT row takes the account path only when the narrowing is set, so the portal's own pick path is a consumer to watch at the apply |
| `tabs/analysis/GenerateComposer.tsx:83` | `api.searchDirectory` with `kinds: ['account']` | read; it lists ACCOUNT entries, which the change adds for tail matches only when the query is a tail (here the query is empty) |

Across the readers cited above, none reads a search result to decide a permission: the reader maps the scope, the pick sends account, relationship or client ids, and the server's resolve decides the set.

## Direct-invoke proof, to run AFTER the apply (by `0.7.0_AE_CloudOps~IB2`, not by this worker)

The instrument is a direct `aws lambda invoke` of the DEPLOYED function with an API-shaped `search` event for an Opal principal, using the function's own role, no new grant, a READ operation only: one search by an account tail, through the function's own handler, over a SYNTHETIC directory (opaque ids and made-up masks) so that no live data is read. The expected result is one ACCOUNT entry whose `permitted_account_count` is 1, and a `resolve` of its `entry_id` returns exactly that account. The apply order must name the operation and state that it persists nothing. The figure is not read by this arm; the sha256 of the response is recorded in the apply's scratch, not in the repo.

## Blast radius

- **Function:** `irpt-directory-search` only. No other function, layer, IAM, route, schedule, environment or table changes. **Member:** `handler.py` only (1 of 24).
- **Served effect:** a tail query returns ACCOUNT entries (one per permitted account); a pick of one resolves to that one account; a name query is unchanged in result; no figure moves.
- **Never-widen:** this MOVES a served behaviour (what a last-four search returns and how a pick resolves), so it ships only under the pair below. It widens nothing.

## The pair

Both halves sign the same facts: built `6hrDbQUWAjVMtdJcI4xm4RosIouzdXEY63eX/wep2sM=` (hex `ea1ac36d...`), live `TefVhmGStCRorgQFrQFCS0lVUC+pXrWJYfdUCEExqe4=` (hex `4de7d586...`), one changed member `handler.py`, the REACH table above, and the replay arms table above. A half that signs a different sha256 or different counts is void.

- **COO half -- `2.0.0_SA_COO~P2`:** signs that the built and live shas, the one changed member, and the reach counts equal this packet, and that the apply order carries the Branch A digest gate and the Branch B restore named above. Signed: ______________________  at: ____________
- **CTO half -- `1.0.0_SA_CTO~DELL2`:** signs the served change in words, the red-list reading, and the choice of Branch A. Signed: ______________________  at: ____________

## Rows

- `IRPT_BCKEND-D2-W349-S1` (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~P2`): the latent attribute mismatch, ruled by the issuer as AMENDMENT 1 (latent, unreachable here). It stays ARMED in the channel until its disarm owner disarms it; this build does not disarm it.
- `IRPT_BCKEND-D2-W349-S2` (OBSERVATION, INERT): the portal reader named in the order (`entry_id`) reads `permitted_scope.scope_ids[0]`, not an `entry_id` member, and the function's search result carries top-level `entry_id` and no `permitted_scope`; the route layer that reshapes one into the other is outside this order's paths and was not read.

Files beside this packet: `IB171-4_release_census.json`, `IB171-4_reach_and_arms.json`, `ib171_4_member_diff.py`, `ib171_4_replay_reach.py`, and the instance `IRPT_BCKEND.TO-IB-pr-499.directory-search-built-and-packet.proof_of_spec.json`.
