# Never-widen sign-off packet -- IB-pr-510: one minimal holdings package per firm (live bytes plus the two merged changes)

Prepared by 0.9.0_WK_IRPT_BCKEND~362 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO IRPT_BCKEND.TO-IB-pr-510 (round 177, workstream ~P; CTO round-177 analysis section 2 item 1; RE 6858 and 6859). **Nothing here was uploaded, applied, deployed or invoked.** BUILD ONLY: scratch rebuilds from the live objects, offline extraction and import, and AWS reads only (head-object, list-object-versions, one get-object of each pinned live version to scratch). No AWS write, no SSM command, no host start, no Lambda invoke. No client data is in this packet or its files: code members, counts, sha256 and VersionIds only.

The apply is GATED by the host's next SCHEDULED Online. No seat starts the host for it, and no seat applies it before both halves of the pair are signed at the current bytes.

## READ THIS FIRST

1. **The served change, in words, per firm (the order's description, with the members measured).**
   - **49financial** (replaces `holdings_49f.py`, `holdings_snapshot.py`, `HoldingsSnapshot.schema.json`):
     - (a) TEMP FILE: the 49F builder removes the Tax-snapshot temp file it creates, on return and on raise (`holdings_49f.py` `build_49f_meshed`, `finally`, commit 135fc3509e); `retained_capture` removes its own temp file when the write fails (`holdings_snapshot.py`, commit 135fc3509e). A file the operator names through `IRPT_49F_TAX_MEMBERSHIP_SNAPSHOT` is never removed.
     - (b) ACCOUNT ID: each 49F ACCOUNT node carries an additive `account_id` member, the directory's opaque id, written only when the directory yields exactly one candidate key (`holdings_49f.py` `build_49f_actual`, `_node(..., account_id=member)`, and `holdings_snapshot.py` `_node`, commit 7ace854890). The schema copy gains the optional ACCOUNT property `account_id` (string) with `additionalProperties` still false. The order states that the serving function passes the member through (round 173) and the builder validates it (round 174); those rounds were not re-read here.
     - (c) NO FIGURE MOVES (the order's statement). This build wrote no figure and no account.
   - **inflection** (replaces `holdings_inf.py`, `holdings_snapshot.py`):
     - (a) TEMP FILE: the Eclipse capture temp file is removed whether the read returns or raises (`holdings_inf.py` `build_inf_meshed`, commit aa5778d962), and `retained_capture` removes its own temp file on a failed write (`holdings_snapshot.py`, commit 135fc3509e only).
     - (b) No schema change, no account member. No figure moves.
   - **cottonwood**: NOT IN THE APPLY. `build_cot` reaches neither `retained_capture` nor the 49F `account_id` path, so its plan is `needs: []` and no allowed hunk applies to it. Its package is NOT rebuilt and NOT uploaded: the candidate package is the live object (candidate sha256 equal to the live object sha256 `3f2e738f...`), `members_replaced` is empty, and the member diff is empty (unchanged 45 of 45). The issuer's amendment of check IB177-1-AC1 (delivered to the worker's branch at `be8bd99362`) grants exactly this, and AC1 PASSes on it. Row IRPT_BCKEND-D2-W362-S1 (BLOCKING when filed) is kept as filed; the amendment is row IRPT_BCKEND-D2-W362-S4. No step of Branch A or Branch B touches the cottonwood key.
2. **What is NOT in any candidate.** The four other commits that touch `holdings_snapshot.py` (69679b90e3, 3a5e564561, e2021e6a5d, 6c962b0a52), the `rebalancer_schemas.py` import of `opal_strategy_matcher`, `lib/opal_naming.py`, the registries and `data/firm_registry.json` are at today's live bytes. Measured: the 49financial and inflection candidates of `holdings_49f.py` and `holdings_inf.py` equal the HEAD blobs at 6bff46497833 and 064a701c36a3 (the live members differ from HEAD only by the allowed commits there).
3. **The four unattributed members, carried UNCHANGED** (the census flagged them, row IRPT_BCKEND-D2-W361-S5): `infra/logic/registry/reporting_policies.json` (49financial only) and `infra/logic/registry/resources.json` (49financial, inflection, cottonwood). Named in the tables below by path and sha256.
4. **Schema line endings (row IRPT_BCKEND-D2-W362-S3).** The live schema copy is CRLF on every line (1322 of 1322). The candidate keeps CRLF, so the four lines added by 7ace854890 are CRLF in the candidate. The apply does not convert line endings; a conversion to HEAD's LF happens only if the pair signs it.
5. **Metadata restamp (row IRPT_BCKEND-D2-W362-S2).** The live objects carry S3 metadata `members-sha256` and `member-count` (44). The candidate's stamps are in the tables below; the apply restamps them, for each replaced package, at Branch A step 4. The order's own Branch A text does not name the restamp (row S2); this packet does.

## Base, live objects and candidate packages

Live reads (2026-10-13, read only). Each live object's VersionId was confirmed as `IsLatest` by `s3api list-object-versions` (49financial 10 versions listed, inflection 10, cottonwood 9; no delete marker). Each pinned object was downloaded to scratch and its sha256 equals the census (IB176-1, committed at 2a16f74311).

| firm | bucket / key | live ETag | live object sha256 (rollback) | rollback VersionId (live object) | candidate package sha256 | built twice identical | members replaced | member diff vs live |
|---|---|---|---|---|---|---|---|---|
| 49financial | opal-data-49financial / `irpt/49financial/code/gold/investor-reporting-holdings.tar.gz` | `"8b482c8db26c2e913aeee72023bacc7e"` | `fe4000cbd31aaee971793854ad6cf26bc7b2d9a37a484e953896a09084f02f2e` | `fMLoOI6a8ZwNFWZCJjjP90ZadyRg9nFg` | `f945da680596607ed152c4bc321c06b2b2b98908383279b67a4fb16758de8534` | YES (two packs, same bytes; the committed packer reproduces them) | 3 | changed: HoldingsSnapshot.schema.json, SHA256SUMS, holdings_49f.py, holdings_snapshot.py; unchanged 41 of 45 |
| inflection | opal-data-inflection / `irpt/inflection/code/gold/investor-reporting-holdings.tar.gz` | `"5daec38f0fbd604c65a770ce08029c67"` | `7036a650703a04b18bcf251717c1310fc5553c817eb9d7ce34ec34ed678c9718` | `qR5sZza4EjUT_cbGA5hLo0ar6zu2NfpI` | `8709a0d5fd7b44e24cec91905837323d56091f59d6efaecdef7af7ea53c965c7` | YES (two packs, same bytes) | 2 | changed: SHA256SUMS, holdings_inf.py, holdings_snapshot.py; unchanged 42 of 45 |
| cottonwood | opal-data-cottonwood / `irpt/cottonwood/code/gold/investor-reporting-holdings.tar.gz` | `"01387cef54b9e15e10023f05029e357d"` | `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901` | `oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_` | = live object (not rebuilt; no member replaced) | not applicable | 0 (NOT IN THE APPLY; package unchanged, candidate = live) | changed: none; unchanged 45 of 45 |

Candidate S3 metadata to restamp: 49financial `members-sha256` `97515201fe83bdeca1f47c788f2d701d8c1b975a25f42fb4f6601ed2dd6c1aee`, `member-count` 44; inflection `members-sha256` `14f55af02989ae7f262759c20b0d4666cd7f535ca74b173d5457df67c2befb9f`, `member-count` 44. (Live: 49financial `73f33c3c59b77528c6eaaa56799e9c55f570a7adac23a0c6bcd12e66fe343a81`; inflection `0b1a3bf7077865054a330ba9360521425f6299bb1bb970766023d2011d70a093`.)

## The member diff, per replaced member (sha256; the stored live and candidate files are in this folder under live/ and candidate/)

| firm | member (repo path) | live sha256 | candidate sha256 | commits applied | hunk offsets (zero fuzz; context matched) |
|---|---|---|---|---|---|
| 49financial | holdings_49f.py (`data/assets/scripts/gold/investor_reporting/`) | `401a36ff675a4e0637b4e1de6baa2aeca5a1e64ec473336fac950f65b8f8f08d` | `6bff46497833123e08ceabd660d7139c3605b7937522eee019a741c17666f741` (= HEAD blob) | 135fc3509e, 7ace854890 | 135fc hunk 2 at offset -31; 7ace hunks at +1, +1, +1 |
| 49financial | holdings_snapshot.py (`data/assets/scripts/gold/investor_reporting/`) | `24c6ea6e1b8db2914a721a003768ca005878a1e3c9b12b5f1865171c69b5a42b` | `5651000b002f50051d4f2c8176ac4d2cfe5dd9265d8c9d3784d0cd0f4f585ed1` | 135fc3509e, 7ace854890 | 135fc at -5; 7ace at 0 |
| 49financial | HoldingsSnapshot.schema.json (`docs/contracts/investor-reporting/v1/`) | `1a5290be6cf177023bf3e182fcc7c121faae3bcdc913f37d0afab66a0505506c` | `953d319e9b97c71cb9fcf51951d975e15faa5b911496fe897ecad8d8037b1e61` | 7ace854890 | +1 (CRLF kept, row W362-S3) |
| inflection | holdings_inf.py (`data/assets/scripts/gold/investor_reporting/`) | `a897083fb744a602349cba69847af60a7fd62b66f9044d6202f1e72d67db529c` | `064a701c36a3fa0b7bee40aaaf2893ac3d78296ac116726f03bce7ec32c9cb0f` (= HEAD blob) | aa5778d962 | 2 hunks at 0 |
| inflection | holdings_snapshot.py (`data/assets/scripts/gold/investor_reporting/`) | `dfa017b824c1aba5c1107e53ef4811edaba93b2b7903c140208e41ab8866262a` | `ff35d4fb0595bb17c95bc2580926e992056e8e583c753fd8af610acdd0f62f7f` | 135fc3509e only | 135fc at -22 |

The candidate differs from its live member only by lines the named commits changed in that path: the order's check IB177-1-AC2 re-derives this from git and reads PASS over 5 of 5 replaced members (`p177_cells.py . IB177-1-AC2`, rc 0).

Stored files (code only): `live/<firm>/<name>` and `candidate/<firm>/<name>` in this folder. Packages are rebuilt by `pack_candidate_package.py` from the live object plus `candidate/<firm>/`; the rebuild reproduces the packages' sha256 above.

## Scratch install (built candidates, extracted to fresh scratch directories)

- `sha256sum -c SHA256SUMS`: 49financial 44 of 44 OK (rc 0); inflection 44 of 44 OK (rc 0).
- `python -I` import of `holdings_snapshot`, `holdings_49f`, `holdings_inf` with the extracted paths first: OK for both trees.
- 49financial temp-file probe (extracted modules, stub S3): raise_leaves 0, return_leaves 0, operator_file_kept true. Control on the LIVE 49financial modules: raise_leaves 1, return_leaves 1, operator_file_kept true (the probe does detect the leak).

## Branch A -- land it (apply at the host's next SCHEDULED Online; digest-gated, never a mint)

Gate: the host's next scheduled Online only. No seat starts the host. Two firms, one at a time, 49financial first, then inflection. COTTONWOOD IS NOT IN THE APPLY: its package is unchanged (candidate equal to the live object), so no step below writes its key.

1. Open the NEVER-2 ledger entry under `org/critical_paths/change_management/` before any write, naming both keys and the rollback VersionIds.
2. START READ for each firm: `head-object` ETag must equal the live ETag above and VersionId the rollback VersionId above; download that VersionId to scratch; its sha256 must equal the live object sha256. Anything else: STOP, no apply.
3. Rebuild the candidate: `python -I pack_candidate_package.py <firm> <live tar> candidate/<firm> <out>`; its sha256 must equal the candidate package sha256 above. ABORT on any difference.
4. Upload with `s3api put-object` to the same key (`--server-side-encryption AES256`, `--metadata members-sha256=<candidate stamp>,member-count=44`); the live VersionId is the rollback and is named in the ledger entry before the write.
5. Read back: `head-object` must show a NEW VersionId, the candidate ETag, the candidate metadata; a download of the new version must hash to the candidate package sha256. Only then the next firm.

## Branch B -- restore the live version (rollback, per key)

- **What is restored:** the live object of each firm, by its named VersionId (49financial `fMLoOI6a8ZwNFWZCJjjP90ZadyRg9nFg`, inflection `qR5sZza4EjUT_cbGA5hLo0ar6zu2NfpI`), sha256 `fe4000cb...` and `7036a650...`.
- **How:** `s3api copy-object` from `<bucket>/<key>?versionId=<rollback VersionId>` to the same key, with `--server-side-encryption AES256` and `--metadata-directive REPLACE` carrying the live metadata (members-sha256 `73f33c3c...` / `0b1a3bf7...`, member-count 44). Then `head-object` ETag must equal the live ETag and the download's sha256 the live object sha256.
- **Per key:** one key per firm; nothing else moves, so nothing else is restored.
- **Trigger:** a refresh failure at `refresh_dispatch.py` (`sha256sum -c` at :67), a 5xx or `TypeError` in the function's log group after the apply, or a figure that differs from its before-read. Restore at once, then re-read.

## The order of the act and the first read after the apply

1. 49financial: START READ, rebuild, put-object, read back (Branch A 1 to 5). Then the first read below.
2. inflection: the same five steps.
3. The first read after the apply, on the host at its scheduled Online: the leftover temp-file COUNT only (counts, no names of client content): files matching `*-taxsma_workbook_projected_snapshot.json` in the host's temp folder (49financial), and `*-membership_map.json` (inflection). A non-zero count is reported; a person deletes any file found. No seat deletes them.
4. The first refresh's `sha256sum -c` read at `refresh_dispatch.py` on each firm.

## The four unchanged members (carried byte-identical; named by path and sha256)

- 49financial: `infra/logic/registry/reporting_policies.json` sha256 `fa392b10b6646cb78fd6ed2c11fefac895a32b84a68313f9f64441d1169f2766`
- 49financial: `infra/logic/registry/resources.json` sha256 `cc945e084ce5ee41826235eaaa8f974fffe5a3c29b9172d9ed921971c1cccff9`
- inflection: `infra/logic/registry/resources.json` sha256 `cc945e084ce5ee41826235eaaa8f974fffe5a3c29b9172d9ed921971c1cccff9`
- cottonwood: `infra/logic/registry/resources.json` sha256 `cc945e084ce5ee41826235eaaa8f974fffe5a3c29b9172d9ed921971c1cccff9`

## Blast radius

- **Objects:** `irpt/49financial/...` in opal-data-49financial and `irpt/inflection/...` in opal-data-inflection. Cottonwood: none.
- **Members:** 49financial 3 of 45, inflection 2 of 45 (plus SHA256SUMS in each).
- **Served effect:** per READ THIS FIRST item 1; no figure moves by the order's statement; 49F ACCOUNT nodes gain an additive `account_id`.
- **Never-widen:** additive only (one optional property on ACCOUNT nodes, and the temp-file removal). Nothing in the candidate narrows an admitted set.

## The pair

Both halves sign the same facts: the two candidate package sha256 values above, the live object sha256 values above, the rollback VersionIds, the members replaced, and the served change in READ THIS FIRST item 1. A half that signs different sha256 values or omits item 1 (a) to (c) is void.

- **COO half -- 2.0.0_SA_COO~P2:** signs the served change above, the cottonwood disposition (NOT IN THE APPLY; package unchanged; the amended AC1), the metadata restamp (row W362-S2), the CRLF choice (row W362-S3), and that Branch A carries the digest gate, the Branch B restore and the scheduled-Online gate. Signed: ______________________  at: ____________ (UNSIGNED)
- **CTO half -- 1.0.0_SA_CTO~DELL2:** signs the served change in words, the cottonwood disposition (NOT IN THE APPLY, as above), and the choice of Branch A. Signed: ______________________  at: ____________ (UNSIGNED)

## Rows (surprise channel, INVESTIGATION_v1.md)

- `IRPT_BCKEND-D2-W362-S1` -- AC1 needs a non-empty allowed replaced set per firm; the order's rule gives cottonwood nothing. BLOCKING when filed, INERT; resolved for cottonwood by the issuer's amendment of AC1 (row `IRPT_BCKEND-D2-W362-S4`).
- `IRPT_BCKEND-D2-W362-S4` -- the issuer's amendment of IB177-1-AC1 applied on the worker's branch; cottonwood is NOT IN THE APPLY. OBSERVATION, INERT.
- `IRPT_BCKEND-D2-W362-S2` -- the Branch A apply omits the S3 metadata restamp. OBSERVATION, INERT.
- `IRPT_BCKEND-D2-W362-S3` -- the live schema copy is CRLF end to end; the candidate keeps CRLF. OBSERVATION, INERT.

Files beside this packet: `IB177-1_candidate_packages.json` (the record), `pack_candidate_package.py` (the deterministic packer), `live/<firm>/` and `candidate/<firm>/` (the replaced members).
