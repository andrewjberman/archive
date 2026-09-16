# SESSION LOG -- `0.9.0_WK_AMGT_RESAPP~20` on `AMGT_RESAPP.TO-AMGT-rj-6` (chain C, order 1 of 2)

Worktree `C:/tmp/wk-amgt-11-3`, branch `wk-amgt_resapp-11-3`, spawn tip `10c74d0efb` (= `SITEZ`).
2026-09-15, approximately 08:45Z to 10:1xZ. Site-Z fabric.

## 1. The bar, first act

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-3`; `org/`, `.tools/`,
`lib/research/drafting/` and `lib/research/identity/crosswalk.py` all present -> TREE-OK. No
BLOCKING row on the tree.

## 2. Premises re-grounded against live state before building

- U-1 at the local read-only copy and in the pool: **256 names, 12 carrying
  `filing_identity.source: edgar`**, and all five QA names present with the forms the issuer named
  (BA 12927 10-K, COST 909832 10-K, HD 354950 10-K, SAP 1000184 20-F, BABA 1577552 20-F). The
  issuer's predicted dry-run shape (12 would-fetch / 244 UNRESOLVED-SOURCE) is what the batch
  prints.
- Card 1 read first, as the cell directs: `measure_filings_analyzer.py` and
  `BA_10K_2026-01-30_measurement.json`. Confirmed on the artifact: `citations_total 0`,
  `blocks_with_citations 0`, and the citations present INLINE as `cite index="1-11,1-12"` tags
  inside the JSON strings -- which is exactly why the cut names TWO passes.
- The CRO's brief read in full; its three probes are reproduced as tests.
- The drafting library read in full: `_source_texts_for` at `10c74d0efb` skips an unknown id and
  reads `item['title']` -- both defects confirmed at the bytes before any change.
- `s3://opal-data-harvest` reachable as `user/Andrew_Berman`; `filings/` empty before this order
  (the `length(Contents)` query returned an error on a null Contents, which IS the empty answer).
- Consumers of the drafting package censused BEFORE changing its schema's top-level type:
  comp-find `research\.drafting` -> 14 hits across 23,133 files, 7 files, only 3 of them code and
  all 3 inside the package.

## 3. What was built, in order

1. `lib/research/filings/fetch.py` -- EDGAR fetch + the named-item cut + the persisted source
   object. First cut of the section rule used card 1's "last heading match" and took the WRONG
   region on BA and SAP; second cut added line-start + not-a-contents-entry + bounded and lost COST
   and BABA entirely; third cut moved the match onto a whitespace-COMPACTED copy with an offset map
   and qualified the CLOSING heading the same way. 5 of 5 correct. Row W20-S4.
2. `lib/research/filings/passages.py` -- the index-to-passage map, the Locator, the ASCII
   normalisation with its recorded count.
3. `lib/research/filings/analyze.py` -- the two passes, the resolution, the HOLD, the driver, F-1.
4. `lib/research/filings/drafting_build.py` -- the D-1 adapter and `FilingsProducer`.
5. `lib/research/drafting/{pipeline,schema,verbatim,run_drafting,tests}` -- the typed evidence
   record, the three validations before the gate, the gate against the PASSAGE. `verbatim.py`'s four
   curly-quote literals became `chr(0x2018)`-style code points: the file had to become pure ASCII
   for AC7, and deleting a glyph from a file that carries several is the silent-mojibake trap, so
   ALL of them went out rather than a subset.
6. `lib/research/filings/batch.py` + `run_batch.cmd` -- the local batch and the disabled weekly task.
7. Tests: 20 filings + 13 drafting, model stubbed throughout.

## 4. The two things that were wrong and were caught

**The 115 s bound.** The first cold BA run was killed at 115 s (rc 124), recorded verbatim. The two
passes measure 107.0-137.8 s together on all five filings, so no cold run fits. The order names the
remedy itself and it was taken: `--stage pass1` caches pass 1 on the excerpt's own hash, the literal
invocation then runs pass 2 live and prints `cached true`. Row W20-S1.

**The vacuous gate.** The first BA drafting object reported `quoted 0` across 40 of 40 sentences:
1 of 85 analysis items carried a quotation mark, so the gate ran 40 times and could not fail once.
The tell was not a failure -- it was a 100% pass rate on a zero denominator, and it only showed up
because the denominator was counted. Quoted spans are now found mechanically (the longest contiguous
run of the sentence's own words that appears verbatim in the EXCERPT), and the gate checks that run
against the CITED passage; 9 sentences across the five filings are now DROPPED for citing a
paragraph their own words did not come from. AC2 was re-run afterwards so the recorded output
describes the object actually served. Row W20-S5.

## 5. What is REFUSED and left open

**AC6.** Its `schtasks` invocation cannot produce the result it names on this device, for two
independent reasons, both measured: MSYS argv conversion rewrites `/Query` to
`C:/Program Files/Git/Query` so the literal command emits nothing (row W20-S2), and `/FO LIST`
without `/V` carries neither `Scheduled Task State` nor `Schedule Type` at all (row W20-S3). The
world-state the criterion asks about IS correct and IS measured with `/V`: the task exists, is
Weekly (`/D SUN /ST 06:00`) and is Disabled. Per the order's refusal clause the criterion is
REFUSED AS WRITTEN with its measurement, the two rows are filed, `<status>` is NOT flipped, and the
order stays OPEN on AC6 alone. Every other criterion is PASS-by-output.

## 6. Bounds honoured

- Egress: EDGAR and the Claude API only, both inside Andrew's session grant. No other host.
- Secrets: only through `comp-secrets`; the key reached the process as an environment variable in
  the same Bash call and is written to no file. Row W20-S7 records that `--reveal` prints a
  four-line labelled block, not a bare value.
- No Lambda, no terraform, no monitor, no alarm, nothing deployed.
- No non-ASCII in any file this order wrote (measured: 11 of 11 package `.py` files at 0) and none
  in anything that reached AWS (the model's output is ASCII-normalised before storage and the
  replacement count is recorded on the object).
- Writes stayed inside `<paths>` plus this deliverables folder. `lib/research/identity/` was CALLED
  (`crosswalk.serialise`, `crosswalk.write_pool`) and never written.
- `.scratch/` in this worktree only.

## 7. Commits (LOCAL on `wk-amgt_resapp-11-3`, never pushed)

- `8abfd829a7` -- the filings package, the typed drafting library, rows W20-S1..S8.
- `a536333c92` -- AC7 fix: the docstring that promised no raw secret read spelled the token it
  promised not to carry.
- (this commit) -- the proof-of-spec instance, this log and MEASUREMENTS.md.
