# IB-cw-3 -- who reads the Cottonwood client key, and what a re-key moves (read only)

Worker 0.9.0_WK_IRPT_BCKEND~459, worktree wk-IRPT_BCKEND-459, base HEAD 66ac649890. No AWS call, no S3 read or write, no Lambda invoke, no SSM command, no source change. Output: IBcw3_findings.json (14 readers plus R15, see section 3).

## 1. Search run (Grep tool, worktree-rooted paths)

Terms, one alternation pattern: `client_id|entry_key|relationship_id|account_ids|directory\.json|hmac_list_forms`. The order's `ids.client_id` term is a sub-match of `client_id` and was not run as a separate pattern. Searched terms in the census: client_id, entry_key, relationship_id, ids.client_id, account_ids, directory.json, hmac_list_forms.

Census (Grep reports no scanned-file count, so files_scanned is the tracked-file count of the same five scopes from git ls-files; the Grep count is files with at least one hit):

| scope | files with a hit | occurrences | tracked files in scope |
|---|---|---|---|
| data/assets/scripts/gold/investor_reporting | 28 | 244 | 54 |
| infra/aws/lambda/investor-reporting | 219 | 1165 | 811 |
| lib | 4 | 8 | 945 |
| infra/logic | 3 | 5 | 33 |
| docs | 115 | 349 | 1480 |

Totals: files_with_hits 369, files_scanned 3323.

Targeted passes (Grep, content mode, line numbers): entry_key, hmac_list_forms, emit_hmac_list, carry_forward_removed, relationship_id, client_id, account_ids, retained over directory_runner.py; _entry_key, SsmBuildDispatcher, bundle_uri over refresh.py; the same key-term pattern over the lambda's directory/ and export/ folders (*.py; test hits were seen and not counted as readers). Line numbers were read with Read at the cited lines and each cited line was hashed with the checker's own rule (strip, sha256 of UTF-8).

## 2. Hits judged NOT readers of the directory client key (one line each)

- directory_runner.py 529 (`_entry` mints `client_id` from `client_raw`): a WRITER. It is where a re-key originates; see section 4.
- directory_runner.py 832 and 840 (`build_cot` calls `_entry` with the relationship id, or with the account id for account-only rows): writers of the key, cited in section 4.
- directory_runner.py 974-977 (`source_raw_keys_cot`): a source reader; its account-id branch is why an account-level key stays in the source set (section 4).
- refresh.py 929-930 (copies the build's `source_client_ids` into `landed`): a pass-through copy, no decision on the key.
- directory/handler.py 138-148 (`project`): entitlement filters on `ids.account_ids` only; reads no client key.
- directory/tests/* and data/.../tests/*: TEST fixtures that pin the readers above; not readers of served data.
- refresh.py 1145-1146: counts keys already covered by R15 and by the disappearance rule; not a separate reader.
- export/bundle.py 111 and export/retained_export.py 355: the filled-report pin's `client_id`; same key-space question as R14, not read beyond the line.
- holdings_snapshot.py, holdings_49f.py, holdings_inf.py, inf_positions.py, the holdings/ and holdings_refresh/ Lambdas: the holdings lens and the other firms' builders; not read for this order (NOT READ).
- lib/silver_ids.py, lib/research/harvest/store.py, lib/tests/test_opal_naming_keyfill.py, lib/opal_data_harvest fixture: matched the terms; not read beyond the match.
- infra/logic/registry/key_rulings.json, name_rulings.json, catalog_fork_keys.json: registry rulings text, not code.
- docs/ (115 files, incl. docs/contracts/investor-reporting/v1/DirectoryEntry.schema.json): documents and contract schemas, not readers.

## 3. Readers (findings file)

Kinds: REFRESH_COMPARE 4 (R01, R02, R03, R15); PAGE 2 (R04, R05); API 2 (R06, R07); RUNNER 4 (R08, R09, R10, R11); HMAC_LIST 2 (R12, R13); EXPORT 1 (R14). Total 15 readers.

rekey_effect per reader: KEY_CHANGES_ENTRY_REMAINS 6 (R01, R04, R05, R08, R11, R15); ENTRY_LOST 5 (R02, R03, R06, R09, R10); NONE 3 (R07, R12, R13); UNKNOWN 1 (R14). The findings file is authoritative.

Required kinds present: REFRESH_COMPARE (R01 at refresh.py 421), HMAC_LIST (R12 at directory_runner.py 1130), RUNNER (R08 at directory_runner.py 926; R09 at 998; R10 at 1282).

## 4. What a re-key does, traced (the mechanism the readers share)

- The key of an entry is `ids.client_id` for every entry (`_entry`, directory_runner.py 529, minted from `client_raw`); `ids.relationship_id` is added only when the raw relationship is real (532-533).
- `build_cot` (directory_runner.py 803-806) routes a row with a real Relationship ID to a relationship entry whose client key is minted from the RELATIONSHIP raw id (832). A row with the vendor no-relationship sentinel is an account-only entry whose client key is minted from the ACCOUNT raw id (834-841, the line 840 call). So an account moves from an account-level key to a relationship-level key when its row gains a real Relationship ID; `ids.account_ids` is unchanged, which is the re-key the order defines.
- `source_raw_keys_cot` (974-977) puts BOTH the relationship raw ids and the account raw ids into the source set, and `source_client_ids` (980-982) mints both as client keys. So the old account-level key is still in the source after the re-key, and the runner's carry test (998) HOLDS it rather than carrying it; run_firm (1282) then refuses the landing. This is the guard premise, and it is the locus described in surprise row IRPT_BCKEND-D2-W459-S1.
- HMAC: `_HMAC_RAW_KEYS` is filled from the account rows (`_entry` line 499) and `hmac_list_forms` hashes those raw account keys and the minted account ids (1121-1133). No client key is an input, so the HMAC list does not move on a re-key of an unchanged account set.
- Refresh: `_entry_key` (refresh.py 421) is the same key rule as the runner's `entry_key` (926); a re-key makes the old key disappear and the new key appear for the same account ids (refresh.py 427, 495).

## 5. Release path (release_path)

refresh.py 714: the SSM build script runs `aws s3 cp <bundle_uri> $W/bundle.tar.gz`. `bundle_uri` is set in `SsmBuildDispatcher.__init__` (refresh.py 768, from IRPT_DIRECTORY_BUNDLE_URI) and passed to `runner_script` (849). The script extracts the bundle repo-shaped (720) and runs `python3 $R/directory_runner.py --firms <firm> --upload` (739). A changed directory_runner.py reaches the build host only through a new bundle object at that URI. The writer of that bundle object was NOT found in this worktree (Grep for bundle.tar.gz and IRPT_DIRECTORY_BUNDLE_URI under .tools and infra returned only readers and tests): see surprise row IRPT_BCKEND-D2-W459-S2.

## 6. NOT READ

- The portal is a separate repository (submodule). It is NOT READ here; the worktree shows the submodule pointer as modified (`M portal`), which this order did not touch. No portal reader is named.
- No served directory object, no S3 object, no AWS state, no SSM document: none read (grant).
- The bundle object's writer (section 5).
- The base checkout was read only for the surprise-row schema: the worktree's org/surprise_channel directory is tracked but absent on disk (sparse), so the schema was read at the base path org/surprise_channel/schemas/investigation_item.schema.json (surprise row IRPT_BCKEND-D2-W459-S3).
- The Cottonwood-scoped reading covers the shared `_entry` and `build_cot` code; the 49F and INF builders reach the same readers but were not traced.
- No test was run; readers are classified from code, not from behaviour.
