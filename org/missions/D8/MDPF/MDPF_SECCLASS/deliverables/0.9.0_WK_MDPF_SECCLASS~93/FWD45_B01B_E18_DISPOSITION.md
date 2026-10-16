# FWD-4 / FWD-5 disposition: B_01b and E_18 uses of the old list `bd-securities`

**Order:** MDPF_SECCLASS.TO-SC-e103 (round 26, cell SC-e-103) | **Worker:** 0.9.0_WK_MDPF_SECCLASS~93 | **Issuer:** 2.0.0_SA_COO~M1
**Base:** box/dell1 @ d63495282e | **Change to code:** none (this record only)
**Method:** read both scripts in full; read `gold_dispatch.sh` chain and phase blocks; read the shared module's `default_bd_securities_lookup`, `classify_asset_class` and `plan_rows`; read five live `etf-classifications` rows by `get_item` and count NAME:: keys by paginated scan (boto3, read-only). Every census below prints its denominator.

## a. Line table

The 24 lines are the live matches of `bd-securities`, `BD_SECURITIES_TABLE` or `bd_securities` (case-insensitive) in the two scripts, at d63495282e: 7 in B_01b (366 lines in the file), 17 in E_18 (339 lines in the file).

| Line | Class | Replacement |
|---|---|---|
| B_01b:3 | DOC | nothing: the line goes with B_01b (module docstring) |
| B_01b:6 | DOC | nothing: the line goes with B_01b (module docstring) |
| B_01b:42 | WRITE | nothing: the constant goes with B_01b (its uses are the writer at lines 255 and 330 only) |
| B_01b:138 | DOC | nothing: the line goes with B_01b (normalize_key docstring) |
| B_01b:156 | DOC | nothing: the line goes with B_01b (scan_existing_keys docstring) |
| B_01b:255 | WRITE | nothing: the handle goes with B_01b (feeds the scan at 256 and the put at 330) |
| B_01b:257 | READ-KNOWN-SET | nothing: the log line goes with B_01b (reports the size of the known set read at 256) |
| E_18:2 | DOC | nothing: the line goes (module docstring rewritten to name etf-classifications) |
| E_18:4 | DOC | nothing: the line goes (module docstring rewritten to name etf-classifications) |
| E_18:10 | DOC | nothing: the line goes (docstring; the name-prefix read it describes is removed, see E_18:218) |
| E_18:13 | DOC | nothing: the line goes (docstring quotes the retirement ruling; kept as a pointer in the rewrite) |
| E_18:14 | DOC | nothing: the line goes (docstring; this script already writes no stub to the old table) |
| E_18:44 | READ-KNOWN-SET | etf-classifications: the constant goes; the known set comes from existing_tickers in the scheduled module (already called at E_18:288) |
| E_18:119 | DOC | nothing: the line goes with load_known_tickers, which is replaced by existing_tickers |
| E_18:151 | DOC | nothing: the line goes with _scan_db_asset_names (no etf-classifications attribute carries asset_name_raw) |
| E_18:176 | DOC | nothing: the line goes (normalize_key docstring; the function stays and its docstring is rewritten) |
| E_18:196 | READ-LOOKUP | nothing: the name leaves the import list together with the lookup call at E_18:291 |
| E_18:214 | READ-KNOWN-SET | etf-classifications: the handle goes; its readers are replaced by existing_tickers (E_18:215) and removed (E_18:218, name-prefix) |
| E_18:256 | DOC | nothing: the comment goes with the name-prefix block (E_18:257-265) |
| E_18:267 | DOC | nothing: the comment is rewritten to point at the canonical conditional put |
| E_18:280 | DOC | nothing: the comment is rewritten; the absence test it describes is existing_tickers (E_18:288) |
| E_18:291 | READ-LOOKUP | nothing: the argument goes; plan_rows skips every ticker etf-classifications already carries (scheduled module lines 530-531), so a get_item on etf-classifications here always returns None |
| E_18:310 | DEAD | nothing: the message goes (it names a stub write the script no longer makes) |
| E_18:332 | DOC | etf-classifications: the --upload help is rewritten to name the canonical conditional put |

Reads the census does not carry as a line: the name-prefix read is made by `_scan_db_asset_names` (E_18:156-171, called at E_18:218). Those lines do not name the table, so the pattern set cannot hold a READ-NAME-PREFIX row for them. They are recorded in the investigation file as row MDPF_SECCLASS-D1-W93-S3.

## b. What etf-classifications carries

Five rows read by `get_item` (table `etf-classifications`, us-east-1):

- `IEFA`: asset_class, classified_by, instrument_kind, last_updated, management_style, name, sector, sub_asset_class, ticker, updated_by.
- `DIVZ`: the same ten attribute names as IEFA.
- `IDVZ`: the same ten attribute names as IEFA.
- `NAME::CRUISECAM INTERNATIONAL INC SHS`: asset_class, classified_by, identifier_namespace, last_updated, name, sub_asset_class, ticker, updated_by.
- `NAME::STATE STREET SPDR S P GLOBAL NATURAL RESOURCES ETF`: the same eight attribute names as the CRUISECAM row.

No row carries `asset_name_raw`. The `name` attribute is a display name (for example "iShares Core MSCI EAFE ETF"; for the NAME:: rows "Cruisecam International Inc.").

NAME:: count (paginated scan, `Select=COUNT`, `FilterExpression=begins_with(ticker, :p)`): **5673 rows over 3 pages** (ScannedCount summed to 11362). Full-table count for context: **11362 rows over 3 pages**.

From these rows only:
- **Known tickers (E_18 load_known_tickers): YES.** The key is the ticker or the NAME:: key, and existing_tickers already scans it.
- **Name-prefix resolution of a truncated name: NO.** No row carries `asset_name_raw`. The NAME:: keys hold an upper-cased, 80-character-cut name, which is not the lower-cased form _scan_db_asset_names compares; ticker rows hold only the display name.
- **The lookup (get_item by ticker, returning asset_class and sub_asset_class): YES in shape,** since both attributes are present on all five rows. Under the E_18 candidate flow it returns nothing (see section e).

## c. Callers of default_bd_securities_lookup

Census: `comp-find` 'default_bd_securities_lookup', **22 hit(s) across 7203 file(s) scanned** (corpus=all). Bands: DEF=1, SURFACED=5, CONFIG=1, DOC=15. The code callers are three lines in two files:

1. `data/black_diamond/scripts/gold/E_18.detect_new_securities.py:196`: import into the from-import list. No call on this line.
2. `data/black_diamond/scripts/gold/E_18.detect_new_securities.py:291`: `bd_securities_lookup=default_bd_securities_lookup(BD_SECURITIES_TABLE)` passed to plan_rows. plan_rows calls classify_asset_class, which takes the row's asset_class and sub_asset_class as the first classification source (tagged `legacy-fork`), ahead of GICS and Schwab.
3. `infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py:651`: the module's own CLI builds the lookup only when `--legacy-fork-table` is given. Census for `legacy-fork-table|legacy_fork_table`: **8 hit(s) across 7207 file(s)**; the only code hit is the module's own argparse, so no caller passes the flag and this path is unused.

The definition is at `infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py:595`.

## d. The chain

- `CHAIN_CANONICAL="B_00 B_01 B_01b E_18 B_02 B_03 C_00 C_01 C_02 C_04"` (gold_dispatch.sh:162). PHASE_B3 runs B_01b (:576-578), PHASE_B3b runs E_18 non-fatally (:582-584), PHASE_B4 runs B_02 (:586-587).
- The gold_dispatch.sh comment at :562 says B_02 reads the bd-securities table that B_01b writes. The B_01b docstring (:7-8) says C_00 and later read a fully populated classification table.
- Census: `comp-find --files 'bd-securities' data/black_diamond/scripts/gold/` returned **48 hit(s) across 128 file(s)**. The named files are B_01b, E_18, B_01, build_canonical_prices_v2, gold_dispatch.sh, lib/etf_classifier.py, lib/s3_layout.py and three tests.
- Native search of the gold folder for `bd-securities|bd_securities|BD_SECURITIES|etf_classifier|classify_new` (same folder, full output): B_02.canonical_lots.py has **no match**. A search of B_02 for `classif|dynamodb|Table(|etf-` returned no matches. The non-B_01b/E_18 mentions of bd-securities are comments or docstrings: B_01.holdings_lots.py:3009-3011, build_canonical_prices_v2.py:398, lib/s3_layout.py:303, and lib/etf_classifier.py:89, which states that the module never opens bd-securities.
- B_03, C_00, C_01, C_02 and C_04 name no bd-securities read. The ones that import lib/etf_classifier read etf-classifications.

So the gold_dispatch.sh comment at :562 is stale.

B_02-READS-BD-SECURITIES: no

## e. Decisions

DECISION-B_01b: RETIRE-FROM-CHAIN

No later step reads what B_01b writes. B_02 names no bd-securities read and no classification read (section d). Every later reader goes through lib/etf_classifier, which reads etf-classifications and never opens bd-securities. E_18 already writes new tickers into etf-classifications through the scheduled module (E_18:291-297). Within the gold folder, B_01b's put at :330 is the only write path to bd-securities: E_18 has no put_item, update_item, batch_writer or delete_item. The OpenAI call (B_01b:280-300) therefore produces rows that no chain step reads. The rule for this decision is met on both conditions. Caveat: today E_18 takes a new ticker's class from the bd-securities row (decision E_18 below), so retiring B_01b stops that feed from growing. The E_18 decision removes that input, so the two decisions are consistent.

DECISION-E_18: OTHER:repoint the known set to etf-classifications; remove, not repoint, the lookup at E_18:291 and the name-prefix read at E_18:214-218 and 256-265

The known-set read repoints: existing_tickers already scans etf-classifications keys, and the NAME:: rows are in that scan (5673 of 11362 rows, section b). The lookup cannot repoint. plan_rows skips every ticker the canonical table already carries (scheduled module lines 530-531) before it calls classify_asset_class. A get_item on etf-classifications for any candidate therefore returns None. A repointed lookup is a no-op. Removing the lookup is a real behaviour change: E_18 would stop writing canonical rows for tickers whose only class source is the old list. Under the module's own rule such a ticker is listed as unresolved, not guessed, so round 27 must state this consequence to the CVO. The name-prefix read cannot repoint either, because no etf-classifications row carries asset_name_raw. Its removal moves names from the prefix-resolved count into the unresolved count and changes no canonical write by itself.

## f. What round 27 builds

1. **Take B_01b out of the chain.** Files: `data/black_diamond/scripts/gold/gold_dispatch.sh` (CHAIN_CANONICAL, CHAIN_HOLDINGS_SEED, GROUP_B, the PHASE_B3 block and the B_01b row). Check: parse the CHAIN_CANONICAL assignment and assert it equals `B_00 B_01 E_18 B_02 B_03 C_00 C_01 C_02 C_04`.
2. **Repoint E_18's known set and remove its lookup and name-prefix read.** Files: `data/black_diamond/scripts/gold/E_18.detect_new_securities.py` (load_known_tickers, _scan_db_asset_names, the handle at :214, the lookup argument at :291, the import at :196, the prefix block at :256-265, the docstrings and the --upload help). Check: a stub-table harness in the style of `data/black_diamond/scripts/gold/tests/test_thread_trace.py` runs E_18 and records zero calls naming `bd-securities`.
3. **Retire the B_01b file and its carriers.** Files: `data/black_diamond/scripts/gold/B_01b.classify_new_securities.py` (delete), `data/black_diamond/scripts/gold/README_BUILD_SEQUENCE.md`, `data/black_diamond/scripts/gold/manifests/data_lineage.json`, and the B_01b watermark entry in `data/black_diamond/scripts/gold/lib/s3_layout.py` (line 303) if no other reader remains. Check: the comp-find census of `data/black_diamond/scripts/gold/` for `B_01b|classify_new` returns zero live code lines, with its denominator printed.
4. **Remove the shared lookup and its CLI flag.** Files: `infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py` (default_bd_securities_lookup, the --legacy-fork-table argument and its use at :651). This is a shared module in another owner's lane, so the issuer must grant it. Check: `comp-find` 'default_bd_securities_lookup' returns zero code hits (only prose), and the module's `--firm ... --dry-run` CLI still runs.
5. **Rewrite the stale claims.** Files: `data/black_diamond/scripts/gold/gold_dispatch.sh` (the comment at :562, which says B_02 reads bd-securities), and the B_01b docstring (:7-8) if B_01b survives in any form. Check: the census of `gold_dispatch.sh` for `bd-securities` returns zero matches.
6. **The FWD-4 standing check.** Files: `data/black_diamond/scripts/gold/tests/test_no_bd_securities_reader.py` (new). It asserts that no live code line in the gold tree names `bd-securities`, `BD_SECURITIES_TABLE` or `bd_securities`, and it covers the name-prefix reads that the pattern cannot see (see row MDPF_SECCLASS-D1-W93-S3). Check: `python -m pytest data/black_diamond/scripts/gold/tests/test_no_bd_securities_reader.py -q` passes after items 1-5. FWD-5 (deleting the table) is not in this list. It waits until the reads are zero and Andrew gives his word.

## Measured numbers

- Live line count: B_01b 366 lines (7 matches); E_18 339 lines (17 matches); total 24.
- NAME:: rows in etf-classifications: 5673 over 3 pages; full table 11362 over 3 pages.
- Callers of default_bd_securities_lookup: 3 code lines in 2 files; census denominator 22 hits / 7203 files.
- Gold folder census for bd-securities: 48 hits / 128 files; B_02 matches: 0.
