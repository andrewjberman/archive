<!-- DRAFT, NOT AN ORDER (2026-10-11 ~19:3xZ, 2.0.0_SA_COO~R1). Written for round 96 and refused by the issuance gate (ONE ISSUER PER ROUND: round 96 already had its issuance); parked here for the round the CTO's round-96 analysis cuts. At the cut: set <round>, the slot and worktree numbers, re-run the checks at the then-base, and re-read the round-95 notes (the checks r95_classification_census.py and r94_display_name.py were re-based to 'no field of the TABLE row is served'). -->

# AMGT_RESAPP task order -- `AMGT-bc-2` -- A LISTING WHOSE TABLE ROW IS WITHHELD SERVES ITS OWN MODEL BLOCK'S GICS SECTOR, WITH THE SOURCE NAMED

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D5/AMGT/AMGT_RESAPP/decompositions/AMGT_RESAPP_DECOMP.md</decomp_doc>
<owned_cells>AMGT-bc-2</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_AMGT_RESAPP~393</issued_to>
<issued_by>2.0.0_SA_COO~R1</issued_by>
<to_id>AMGT_RESAPP.TO-AMGT-bc-2.a-withheld-listing-serves-its-own-model-block-sector-with-the-source-named</to_id>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a serve-time rule and its tests, no schedule.
comp-iam: DECLARED-NOT-APPLICABLE -- r96_sector_serve_census.py --where local reads the crosswalk, the classifications table (GetItem), the stored model blocks (S3 GET) and the handler's own stored reads with the caller's own credentials (GET only).
comp-adversary: RUN at the cut -- r96_sector_serve_census.py --where deployed FAILs K1-K4 at the live base (SAN FP's ranked row 67, rank series and chatter rows serve no sector; CSL AU asked by ticker serves 'CSL Ltd' with a null classification) and PASSes K5, K6; against a throwaway candidate (--where local) 6 of 6 with 2 ranked rows, 2 rank series and 3 chatter rows serving 'Health Care' from the model block and 186 and 186 control rows unchanged; r95_classification_census.py and r94_display_name.py (their arms re-based to "no field of the TABLE row is served") PASS at the base and against the candidate.
EGRESS CLASS, declared: NONE (S3 and DynamoDB GETs by the census; no Bloomberg, vendor, SEC or model call).
</preflight>

**Your worktree:** `C:/dev/wk-resapp-393` (branch `wk-AMGT_RESAPP-393`, cut from the issuance commit). Work and commit only there. The shell's working directory resets between calls: start EVERY shell call with `cd C:/dev/wk-resapp-393`; a call that starts elsewhere resolves `git rev-parse --show-toplevel` to the base checkout and answers for the wrong tree.

## 1. THE CELL -- `AMGT-bc-2` (round 96, decomposition s.104)

CTO~DELL1 round-95 analysis item 1, after `AMGT-bc-1` read SECTOR-SERVED: the listing's own stored model block (`derived/model_block/<security_key>/<newest>/model_block.json`, a `figures[]`
record whose `mnemonic` is `GICS_SECTOR_NAME`, `value` e.g. 'Health Care', `source` bloomberg-dapi) carries the sector for `SAN_FP_Equity` and `CSL_AU_Equity`, the two listings whose
classifications-table row names another company and is withheld since round 95 (`AMGT-aa-2`, `names_read.names_disagree`). Serve that sector in the places the table's classification
was withheld, with its source named. Do exactly this in `scoped_amgt.py` and `monthly_chatter.py` (do NOT touch `_classification_for_ticker`, the table read or `names_read.py`):

1. `scoped_amgt.py`: add `_listing_sector(security_key) -> Optional[Dict[str, Any]]`: read the key's newest stored model block with the existing `_read_model_block_pool(security_key)`
   (it returns the block and its record; use its own vintage stamp, the object folder `YYYYMMDDTHHMMSSZ`, as `sector_as_of`), find the `figures[]` record whose `mnemonic` equals
   `GICS_SECTOR_NAME` with a non-empty string `value`, and return `{"asset_class": None, "sub_asset_class": None, "sector": <value>, "sector_source":
   "model_block.GICS_SECTOR_NAME", "sector_as_of": <vintage>}`. Absent, empty, or ANY exception (a failed read): return None (a read that fails is never a guess: the row stays
   withheld). No other field of the block is read or served. A key that is not a string returns None.
2. `scoped_amgt._drop_disagreeing_table_names(rows)`: for a withheld row (the branch `AMGT-aa-2` added), after nulling, when `_listing_sector(row["security_key"])` returns a
   dict set the row's `classification` to it, `sector` to its `sector` and `sector_reason` to None; otherwise leave the round-95 values (null with the reason).
3. `scoped_amgt._rank_series_names(tickers)`: for a withheld entry set `classification` to `_listing_sector(key)` (the key is the one the lookup already resolved) and
   `classification_reason` to None when it returns a dict; otherwise the round-95 values. `read_rank_series` already copies `classification_reason` onto the series (a None is copied
   as null, present only on a series that was withheld).
4. `monthly_chatter.py`: the collected-chatter row whose table name disagrees (the branch `AMGT-aa-2` added) serves `classification` `scoped_amgt._listing_sector(key)` and
   `classification_reason` None when it returns a dict, else the round-95 pair.
5. Tests: add `lib/research/api/tests/test_sector_from_model_block.py` (pure; replace `_read_model_block_pool`, `_crosswalk_names`, `_classification_for_ticker`,
   `_covered_bloomberg_index` and `_measured_ticker_index` with fixtures as `test_classification_withheld.py` does): one test per place, one for the block with no
   `GICS_SECTOR_NAME`, one for a failed read (stays withheld with the reason) and a control that a row whose table name AGREES keeps its table classification byte-equal.
   The two existing tests that pin "a withheld entry's classification is None" call the real reader: in `test_classification_withheld.py` and in
   `test_names_read_agreement.py` (the D10 test) replace `_read_model_block_pool` with a stub returning no block, so the round-95 reading they assert is still the one under test.

The overlay and the other per-security routes still serve no classification (`r96_sector_serve_census.py` K6 guards that). Nothing is served until `AMGT-bc-4`'s redeploy.

Stamp any surprise row's `surfaced_at` with `date -u +%FT%TZ` at filing. Rows: id form `AMGT_RESAPP-D1-W393-S<k>`, `disarm_owner` `2.0.0_SA_COO~R1`.

## 2. BOUNDS

1. Write only the paths below. No deploy, no store write, no schedule, no SEC, vendor, model or Bloomberg call (no `bloomberg_health`, no `reference_data`); no S3 delete, ever.
2. No `bun`, `npm` or `pip install`. The checks' S3 and DynamoDB reads (GET only) are permitted; nothing else is fetched.
3. Standing: no push of shared branches.
4. Edit the named product files minimally: do not reformat them and touch no function the cell does not name.
5. `names_read.py` and `_classification_for_ticker` are not touched; no sector is served for a row that AGREES with the registered name, or whose block holds no `GICS_SECTOR_NAME`.

## 3. SURFACES

<paths>
lib/research/api/scoped_amgt.py
lib/research/api/monthly_chatter.py
lib/research/api/tests/test_sector_from_model_block.py
lib/research/api/tests/test_classification_withheld.py
lib/research/api/tests/test_names_read_agreement.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~393/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

## 4. PROOF OF SPEC (literal; timeout 900)

<proof_of_spec>
  <criterion id="AC1" cell_refs="AMGT-bc-2"><invocation>cd C:/dev/wk-resapp-393 &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round96_prep/checks/r96_sector_serve_census.py" --where local; echo "exit=$?"</invocation><expect>the two withheld listings and their model-block GICS_SECTOR_NAME values printed (SAN_FP_Equity and CSL_AU_Equity, 'Health Care'); PASS K1 (ranked rows), PASS K2 (rank series), PASS K3 (collected chatter, three windows), PASS K4 (asked by ticker), PASS K5 (186 ranked rows and 186 series unchanged), PASS K6; arms passed 6 of 6; R96 SECTOR SERVE CENSUS: YES; and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="AMGT-bc-2"><invocation>cd C:/dev/wk-resapp-393 &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round95_prep/checks/r95_classification_census.py" --where local &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round94_prep/checks/r94_display_name.py" &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round94_prep/checks/r94_name_census.py" --where local; echo "exit=$?"</invocation><expect>no field of the TABLE row is served and the names are unmoved: R95 CLASSIFICATION CENSUS: YES (6 of 6), R94 DISPLAY NAME: YES (12 of 12) and R94 NAME CENSUS: YES (C1, C3, C4 at 0); and exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="AMGT-bc-2"><invocation>cd C:/dev/wk-resapp-393 &amp;&amp; PYTHONPATH="$(pwd)" python -m pytest lib/research/api/tests --ignore=lib/research/api/tests/test_print_format_rich.py -q -p no:cacheprovider; echo "exit=$?"</invocation><expect>the control: the new test file and every other test of lib/research/api/tests pass (no failed, no error); and exit=0</expect></criterion>
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Commit in your worktree via `.tools/safe-commit.sh --author "0.9.0_WK_AMGT_RESAPP~393 <0.9.0_WK_AMGT_RESAPP~393@opal.agent>" -F <msgfile> -- <paths>`
(message file written with the Write tool, never a shell heredoc; confirm with `git log -1`). Write any python or multi-line file with the Write tool. Instance at
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~393/AMGT_RESAPP.TO-AMGT-bc-2.a-withheld-listing-serves-its-own-model-block-sector-with-the-source-named.proof_of_spec.json`
with `to_id` equal to the `<to_id>` line above, character for character. The recorded invocations equal the order's text above (a path you substituted is a row, not a rewrite).
Run `python .tools/proof-of-spec-check.py <instance>` on the committed bytes and report its verdict line. Do not stage `portal`.
Report once:
- the commit hash;
- every criterion's output lines;
- the diff of each edited product file, in full;
- any row.

The `<status>` flip is the issuer's.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES:** CTO~DELL1 round-95 analysis item 1 and ADDENDUM 1 (msg 4080): "bc-2 rides the redeploy that carries AMGT_CORPUS's /13 files: one redeploy, two pairs, each admitted by blob, which also retires the scratch pin. If that has not happened by round 96's close, ship on a scratch pin parented on b3512d18fb plus only bc-2's files, under its own pair; a pin from 15b7af1601 again is refused." This order is the CODE (LOCAL until `AMGT-bc-4`). READ: the sector is served from the listing's own stored model block, source named (`model_block.GICS_SECTOR_NAME`, `sector_as_of` the block's vintage); asset class and sub-asset class are NOT claimed (null). CSL AU's block ends 2026-09-30 (bc-1 S3 row): its `sector_as_of` says so. Checks re-based BEFORE the cut so no reused arm asserts the round-95 null (`r95_classification_census.py` K1-K3 and K6, `r94_display_name.py` D10 read "no field of the TABLE row"); two existing unit tests are named in the face because they call the real block reader.

<status>pending</status>
<round>96</round>
<slot>0.9.0_WK_AMGT_RESAPP~393</slot>
<fabric>dell1</fabric>
<risk>LOCAL</risk>
<worker_class>worker</worker_class>
