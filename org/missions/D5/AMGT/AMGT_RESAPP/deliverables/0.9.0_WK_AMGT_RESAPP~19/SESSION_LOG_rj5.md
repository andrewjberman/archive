# AMGT-rj-5 session log -- `0.9.0_WK_AMGT_RESAPP~19`

Worktree `C:/tmp/wk-amgt-11-2`, branch `wk-amgt_resapp-11-2`, respawned on the same tree
at `10c74d0efb`. 2026-09-15 08:5xZ - 09:4xZ. Round 11, chain B, order 2 of 3.
Order 1 (`rj-4`) was complete and drained before this order began; nothing of it was re-run.

1. **08:5xZ the bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-2`;
   `org/` and `.tools/` present. TREE-OK. Working tree clean except `.scratch/`.
2. **08:5x-09:0xZ re-grounded every premise before writing a line.** Read `rj-4`'s own
   `MEASUREMENTS.md` and `SESSION_LOG.md` (the association key forms), both CRO briefs,
   `chatter_axis.py` end to end, `chatter_gate.py`, `movement_gate.py`, the harvester's
   `catalog.py` and both JSON schemas, the crosswalk's `resolve`/`aliases`, the union
   universe object, `rj-1`'s task order (for the G-1 row shape it consumes), the proof
   checker's expect/placeholder limbs, and the live pool.
3. **09:0xZ the premise that failed, measured before any code was written.** `AC1` as
   written returns three prefixes and a publications count of **7** against a named bar of
   **80**. A second instrument (client-side-paginated boto3 census) agrees: 73 objects in
   the bucket, 7 links and 7 bodies. Per name: BA 2, COST 2, HD 3. Row
   `AMGT_RESAPP-Z-W19-S8`. The CRO's pool-readers brief already characterises the store as
   a bounded commissioning sample. **Nothing was uploaded, no window was widened and no
   bar was re-read as satisfied** -- the four count bars are refused with their
   measurement and the order stays OPEN on them, while every field-level and behavioural
   clause of the same four criteria is met and recorded.
4. **09:0xZ checked a hazard before believing it.** The adapter imports the harvester's
   `catalog`, which imports `storage`, which does `from ctypes import wintypes` at module
   level -- a Windows-only-looking import on a module bound for a Linux Lambda. Read the
   stdlib's own `wintypes.py` before filing anything: 202 lines, no platform gate, no
   `WinDLL`/`HRESULT`/`oledll`, one `_SimpleCData` subclass. The import is portable, so
   **no row was filed on a hazard that does not exist.**
5. **09:0x-09:1xZ built** `pool_reader.py` (P-1), repointed `chatter_axis.py` onto it,
   replaced the upsert writer with the generation carrier, and wrote 25 + 16 unit arms.
6. **Two corrections this cell made to its own first cut**, both caught by a control
   rather than by re-reading the code:
   - The first producer run considered **201** names, because the union universe carries a
     raw `ticker` on unresolved holdings and the first `_universe_entries` accepted either
     identifier. The cell's own words are "the histogram per `security_key`", and ranking a
     row whose `security_key` is null would put an unresolvable identity in the top 10. The
     rule is now MEASURED off the document shape: a UNION universe ranks names with a
     canonical key (33 of 256, the other 223 counted and disclosed); the LEGACY fallback
     keeps its old precondition, so the deployed wrapper's snapshot still ranks.
   - `PoolReaderReadOnlyTest` failed on the first run: `reader carries 'put_object'`. The
     module DOCSTRING spelled the call names while promising not to use them -- and
     `AC7` counts that same token, so the criterion would have read NOT MET on a
     **sentence**. The sentence was rewritten; the property is now asserted, not promised.
7. **09:2xZ ran every criterion under `timeout`**, recorded each output verbatim with its
   denominator, and kept the dry run and the difference control beside the instance.
8. **09:3xZ filed rows** `W19-S8` (BLOCKING), `W19-S9`, `W19-S10`, `W19-S11` and committed
   them (`5f8acb7f47`); the code went in first at `fda8d96c0a`.

**Bounds honoured.** No live DynamoDB write (the single DynamoDB act is the difference
control's one commissioned read per ticker through the old index, paginated). No deploy,
no Terraform, no zip. `lib/research/api/scoped_amgt.py` untouched: **0 diff lines**.
`lib/opal_data_harvest/` and `lib/research/identity/` read, never written. No harvest
collection, cadence or backfill touched or requested. No push, no merge, no rebase, no
`checkout --`, no `stash`, no `clean`. Every mutation of a tracked file was snapshotted to
`.scratch/snapshot/` first.

**What is OPEN.** `AC1`, `AC2`, `AC3`, `AC5` on their count bars only, all four tracing to
the one world-fact in `W19-S8`. `AC4`, `AC6`, `AC7` are PASS-by-output. The remedy is the
issuer's to choose: a harvest backfill and a re-run of the four invocations UNCHANGED, or
a re-cut of the four bars against the store that exists.

---

## RE-RUN AGAINST AMENDMENT 2 (2026-09-15 ~09:4xZ, branch tip a33786b896)

The issuer UPHELD row `W19-S8` and re-cut the four count bars to the store that exists
(`AMENDMENT 2` @`a33786b896`): the pool's counts are now PRINTED as denominators and the
discriminating clauses stay. AC2's truncation was widened 170 -> 400 on row `W19-S11`, so
`title` is inside the recorded bytes at last.

**Nothing was rebuilt.** No source file, test, script or deliverable logic changed in this
pass; the seven invocations were extracted from the order file itself (so each ran LITERAL,
byte-for-byte as amended) and executed under `timeout 120`, all seven rc=0.

**Result: 7 of 7 PASS-by-output.**

| criterion | the measurement |
|---|---|
| AC1 | 3 of 3 prefixes (BA, COST, HD); publications/v1 objects **7**, printed, not graded |
| AC2 | store_item_count 2 / 2 / 3 = **7 of 7** associations; items in window 1 / 1 / 3; control 0; states 0,0,0,0; duplicate_links 0; title+url+publisher+published_at+article_key all inside the 400-char window |
| AC3 | names_read=256, names_with_links=3, links_listed=7 **= bodies_read=7**, articles_in_window=5, dynamodb_reads=0; 10 of 10 rows carry security_key; pointer payload_hash 64-hex, row_count=10, state COMPLETE, **rank_sort ABSENT** |
| AC4 | knob 0, GSI 0, pool_reader 8, overwrite_by_pkeys 0, _CURRENT 3, _FAILED 9, states 25; scoped_amgt.py **0 diff lines** |
| AC5 | pool-links 2 / 2 / 3 / 0 = 7; bodies-in-window 1 / 1 / 3 / 0 = 5; table-items **0 on 4 of 4**; the two stores DIFFER |
| AC6 | 25 + 16 = **41 of 41** arms OK, 0 failures 0 errors; defect-reproduced 41, three-states 17, alias-once 2 |
| AC7 | this serial's commit most recent on both paths; reader nonascii 0, put_object 0, delete 0 |

**The control on the re-cut itself.** A bar replaced by a printed denominator can lose its
teeth silently, so every re-cut `expect` was run against a MUTATED copy of its own evidence:
**13 of 13 mutations refused** (missing prefix, missing count line, a control carrying items,
a renamed url field, duplicate_links 1, bodies_read 6 against links_listed 7, a pointer with
no payload_hash, a pointer carrying rank_sort, a row missing security_key, dynamodb_reads 3,
table-items 9 on HD, a control with 5 links, BA with 0). AC3's partial-read clause now reads
as a BACKREFERENCE (`bodies_read` EQUAL to `links_listed`), which discriminates at any pool
size -- strictly better than the fixed 80 it replaced.

**Determinism, third observation.** The 09:48Z dry run reproduced both payload hashes from the
09:04Z and 09:21Z runs exactly, while run_id and generation_id moved. STABLE on 3 of 3.

**Bounds honoured again.** No live write of any kind; the one DynamoDB act was AC5's commissioned
read (one per name, 4 pages of 4 complete). No deploy, no push, no merge, no rebase. The order's
`<status>` is flipped to `complete` on this pass, with the instance VALID at rc=0.
