# NEVER-WIDEN -- COO HALF: rebuild the served bbg silver `article` table on `q-2`'s parse (`HVST-aa-3`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~10:2xZ (06:2x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rulings served:** `ROUND_ANALYSIS.round27.md` ruling 4, as superseded @`803ea38a9e` (msg 27079): **KEEP the 11 hash-keyed empty
rows, no delete, no reader filter; the AC proves them inert; any empty row reachable from a served list is a STOP.**

**Round-25 ruling 1, all three named:**
1. **The command that reaches the put:**
   - `store.silver_append("bloomberg", "article", rows, ("article_key",), store.stamp(<now UTC>))`, with the rows from
     `round28/checks/aa3_common.rebuilt_rows()`.
   - That is `silver_from_bronze.article_rows("bbg", ...)` over every bbg bronze article object, with `n-2`'s lineage rules
     and CLOUD code carrying `q-2`'s parse (`silver_from_bronze.py:115`).
   - It makes one never-overwrite put per fetch-date group.
2. **Config defaults:** `RECORD_KEY = ("article_key",)`; the part name is `part-<run_stamp>.parquet`; readers use `o-3`'s
   tie-break (irrelevant here, since every NEW row has a new key).
3. **Stub put-count dry run:** `round28/checks/aa-3.signing.py --signing` mirrors `silver_append`'s own filter over the real
   rebuild. The expected write is 11 rows in ONE fetch-date group, so exactly ONE put.

## VERDICT: SIGNED

- **Blast radius:** ONE new bbg silver part, 11 NEW rows keyed `bbg:<story id>`.
- **Kept:** the 11 hash-keyed empty rows stay served, keys unchanged, and are proven inert.
- **Unmoved:** the other 19 rows.
- **Rollback:** forward only.

## 1. BEFORE -- measured at signing (`round28/aa3_signing_expected.json`)

| what | count |
|---|---|
| bbg silver `article` parts | 30 |
| bbg bronze `article` objects | 30 |
| served record keys | 30 |
| of which empty | 11 (the `o-5` as-received rows keyed `bbg:<hash>`) |

The act-start gate (`aa-3.signing.py` without `--signing`) STOPS on any difference in the parts, the bronze, the latest hashes or
the expected write.

## 2. EXPECTED OUTCOME, READ FROM THE MERGED RULE

**11 rows are written, all NEW** (`bbg:<story id>`), in one part for fetch date 2026-09-30. Served keys go from **30 to 41**.
The 30 pre-existing keys are unchanged, including the 11 empty ones: kept, and not rewritten, because their keys differ. A re-run
writes 0.

**INERT, measured at signing (AC2 reads it again after the act):**
- the served mention snapshot holds **0** pairs on an empty bbg row, so the empty rows are absent from `/timeline/day` and from
  the company query;
- all **32** served bbg mention pairs map to non-empty silver rows.

The NEW rows are not in the mention snapshot until a mention rebuild, so no page moves in this act.

**Readers:**
- `/timeline/day` reads silver only for mention-snapshot keys.
- `build_mention` (not run) reads all silver. When it runs, the NEW rows will add bbg pairs, and the empty rows yield none.

### Failure branches

- **`PreconditionFailed`:** nothing is written, and the act STOPS.
- **FAIL conditions (`aa-3.AC1.py` / `aa-3.AC2.py`):**
  - any row outside the 11, a pre-existing part moved, or bronze changed;
  - a NEW row served empty, or any served list reaching an empty row (the STOP).

## 3. ROLLBACK

Forward only. A delete is a human word; the ruling keeps the 11 rows.
