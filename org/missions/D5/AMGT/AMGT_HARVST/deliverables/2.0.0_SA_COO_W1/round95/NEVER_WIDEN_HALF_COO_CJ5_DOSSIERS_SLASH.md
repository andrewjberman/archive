# NEVER-WIDEN -- COO HALF: 2 `research_dossier` objects are ADDED, for the two slash-key securities `BP/_LN_Equity` and `NG/_LN_Equity` (`HVST-cj-5`, round 95, workstream DOSSIER-WRITE-SLASH)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~09:4xZ UTC. **Authority:** the CTO's round-94 analysis (`ledger/ROUND_ANALYSIS.round94.md` @428b762698, msg 7946) section 3 (the rebuild "for every name WITHOUT a slash ... under its own never-widen pair. The slash-key names wait for W170-S3": "a slash-key dossier rebuilt today would be written under one key form while its reports sit under the other, so it would bake the W170-S3 split into a new object") and enrichment item 3 ("the slash-key dossiers: after item 1 is merged and its census reads every slash key whole, under the same pair shape"). **Pair shape:** `HVST-cj-4`'s pair (COO half `35e368f3...`, CTO half `b9e244d5a9` with his model-block guard), which this half repeats for two names; `HVST-cj-4` is complete (75 of 75, re-read by the issuer). **Measurement:** `HVST-ci-3`'s census rows for the two names (`deliverables/2.0.0_SA_COO_W1/round94/ci3_issuer_census.out`): `BP/_LN_Equity` moves `fund_form_ref` and `model_rows`, `NG/_LN_Equity` moves `model_rows`.

## START CONDITIONS

The gateway release `HVST-cj-3` is deployed, its `cj3_served.out` reads all four PASS, and the ISSUER has read `BP/_LN_Equity`, `BP-SLASH-_LN_Equity`, `NG/_LN_Equity` and `NG-SLASH-_LN_Equity` through the live gateway, each returning the whole record (dossier, continuation, ai_fill, reports, exec officers) and said so in the GO. **Why:** before that, a read of either spelling is half a record, so the pair's served-read proof could not be made; after it, the dossier the writes add is read back through either spelling.

## THE ACT, in the order's words

On dell1, by `0.7.0_AE_CloudOps~SC1`, from a worktree at `8f329a10b9` (the commit `HVST-ci-3`'s census ran on; `git diff 8f329a10b9 HEAD -- lib/research` printing empty): for each security in `deliverables/2.0.0_SA_COO_W1/round95/cj5_names.txt` (2 names, sha256 `1e8570870bcd47bc16b6958649b72797423afaaaa17c724c871317c3335bd923`: `BP/_LN_Equity` then `NG/_LN_Equity`), in this order: (1) BUILD in memory (`dossier.build(security_key)`) and compare with the dossier served (the gateway's pick over the partition `security_key=<slash_safe_key>/`): the moved `fields` must be a SUBSET of `{fund_form_ref, model_rows}`, the differing `inputs` kinds a subset of `{continuation, fund_form, model_block}`, and **the CTO's model-block guard** (his half of `cj-4`, condition 1) must hold for a name that moves `model_rows` (the record `SERVED`; its stamp later than the stored dossier's; the count of valued rows not lower) and for a name that does not (the record still `SERVED`, or already built from no block); else STOP before that name's write; (2) WRITE `dossier.write_one(security_key)` (it partitions with `store.entity_partition`, the encoded form the stored objects sit under; the seat prints the object key and checks it lies under `security_key=BP-SLASH-_LN_Equity/` and `security_key=NG-SLASH-_LN_Equity/`); (3) READ THE OBJECT BACK and check it (Branch A of `cj-4`); (4) append the manifest line; then the next name. **Canary:** `BP/_LN_Equity` first, read through the gateway in BOTH spellings before `NG/_LN_Equity` is written.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is the newest dossier object of each of the two securities. **N = 1 writer:** `lib/research/corpus/dossier.py::write_one` (line 1651; `gold.gold_put`, never overwriting); `continuation.write_one` is NOT called. Both objects land under the ENCODED partition where the stored objects already sit (the census: 15 and 14 objects there; 0 under the raw spelling), so the write does not create a second form.

## WHAT THIS CHANGES IN THE WORLD (named)

- **2 gold objects are ADDED; none is changed or deleted.** The gateway (after `cj-3`) serves each key, in either spelling, with the dossier of the greatest `as_of`: `dossier_key`, `as_of` (2026-10-18), `content_sha256`, the dossier entry of `source_keys` and the listed counts move; `fund_form_ref` (BP only) and `model_rows` (both) move as the list says; **every other served value is equal** (the other `dossier_fields`, `continuation_*`, `research_reports[]`, `ai_fill_*`, `management_roster`). Not touched: continuations, fund forms, silver, bronze, the gateway, IAM, schedules; the 75 non-slash names; KMB.

## BOTH BRANCHES, CONDITIONS, ROLLBACK

As the `cj-4` half (Branches A and B per name; C-1 to C-10 with the names and counts of this act: the dossier object count equals its start count plus 2, the continuation count (446) unchanged, the gateway pick over a fresh listing of each encoded partition names the manifest key). **C-7 (canary):** the four spellings are read through the gateway BEFORE the first write and AFTER the first name (`BP/_LN_Equity`): every returned entry other than the named moves is equal; for each spelling the `dossier_key` is the new object after. **C-10:** site Z is told first (window, prefix, the 2 names); no GO before its answer. **Rollback:** ADD-ONLY; removing the 2 keys restores the pre-act pick (an S3 delete, Andrew's act, not pre-approved here).

## WHAT THIS DOES NOT COVER

Any other name; any continuation write; any change to the dossier build rule; the path-component spelling question (rows `D1-W171-S4` and `-S6`, the CTO's).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
