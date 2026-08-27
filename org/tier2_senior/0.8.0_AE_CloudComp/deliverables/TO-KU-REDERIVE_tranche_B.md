# TO-KU-REDERIVE — tranche B re-derivation: `denominator.known_unsearched` entries [8] and [9]

**Executor** `0.8.0_AE_CloudComp~X` · **Issuer** `2.0.0_SA_COO~X` · **TO** `@6361bde30c`
**Subject** `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/graph_object_manifest.json`
**Key** `denominator.known_unsearched` · **Assigned** entries `[8]` + `[9]`
**Measured** 2026-08-27, worktree at the vintages cited per claim
**Emits** nothing into L0, no held path, no generator, no registry entry.

---

## ACCESSOR CONTROL — run before any count, per the TO's header

| probe | result | |
|---|---|---|
| top-level `known_unsearched` | **0** | the wrong key — byte-identical to an empty list |
| `denominator.known_unsearched` | **12** | POSITIVE CONTROL: path resolves, non-empty |
| `denominator.nosuchkey` | **0** | NEGATIVE CONTROL: a wrong key is distinguishable |

**Denominator: 12 entries, 12,477 chars measured by `len(json.dumps(entry))`.** The TO states 12,363;
the 114-char gap is a measurement-convention difference (JSON-encoding overhead vs raw string
length), not a disagreement about content. **My tranche `[8]`+`[9]` = 3,272 by my convention, 3,243
by the TO's.** Stated rather than silently reconciled.

---

## ENTRY [8] — `cse_store.py#PATH_B_drop` — **VERDICT: STILL TRUE**

### The claim, in its own words

> *"cse_store.py:348 def drop_cse_table; :351 `if table == CSE_TABLE:`; :352 raises ValueError
> ('REFUSED: cse is the real append-only C0 log -- never dropped here'); :86 binds CSE_TABLE =
> cse_schema.CSE_TABLE = 'cse'; the docstring at :349-350 scopes the function to SCRATCH tables.
> Worktree byte-identical to the pin (git hash-object 47098758c8e4 both sides). THEREFORE PATH B's
> REACHABLE WRITE DOMAIN IS ANY TABLE IN THE NAMESPACE **EXCEPT** cse."*

### Instrument, and what a false answer looks like

Direct source read at the cited line numbers, plus `git hash-object` / `git rev-parse <pin>:<path>`.
**A false answer here looks like line drift** — the file changing so the numbers point elsewhere
while each quoted string still exists somewhere in the file. The hash comparison is what closes that.

### Measured

| claim | result |
|---|---|
| `:348` `def drop_cse_table(catalog, table: str) -> None:` | **VERIFIED** |
| `:349-350` docstring scopes to SCRATCH, names fail-closed | **VERIFIED** |
| `:351` `if table == CSE_TABLE:` | **VERIFIED** |
| `:352` raises `ValueError(f"REFUSED: {CSE_TABLE} is the real append-only C0 log -- never dropped here")` | **VERIFIED** |
| `:86` `CSE_TABLE = cse_schema.CSE_TABLE` | **VERIFIED** |
| worktree blob == pin `e48a7466ba` blob | **VERIFIED** — `47098758c8e4698316569646a0785d405bea5cc8` both sides |
| domain: `--table` defaults to `CSE_TABLE` (`:581`), `--drop` dispatches `drop_cse_table(catalog, args.table)` (`:594-595`) | **VERIFIED** — bare `--drop` targets the real log and raises |

**Controls, both fired:**
- NEGATIVE (hash): the same path at an older commit `d1d18acde3` is blob `d9fd72c59b5e` — **differs**,
  so the comparison discriminates rather than always matching.
- NEGATIVE (line read): `:451` returns `with open(uri, encoding="utf-8") as f:` — **different text**,
  so a line read is not returning a constant.

**Denominator:** 7 of 7 sub-claims verified; 2 of 2 controls fired.

### ⚠ One imprecision, not a refutation

The entry says the raise happens *"before the catalog is touched."* Measured, `:592
catalog = get_catalog()` runs **before** `drop_cse_table` is called at `:595`. **The catalog IS
obtained; what is never reached is the destructive `catalog.drop_table()` at `:353`.** The entry's
conclusion is correct and its phrasing overstates by one step. Recorded because this unit exists to
check exactly this kind of load-bearing wording.

---

## ENTRY [9] — `cse_emit_frontend_coevolution.py :: PATH A` — **VERDICT: STILL TRUE**

### The claim, in its own words

> *"this path writes a LOCAL path only (:262 is a plain open(), no boto3). The S3 object above is
> that local file AFTER A HUMAN UPLOADED IT... SO PATH A's ARTIFACT IS A DEV-BOX LOCAL FILE THAT NO
> LONGER EXISTS AND WAS NEVER MEASURABLE. The 259,918-byte object at
> warehouse/cse_ingest_staging/cse_frontend_coevolution.jsonl is a DIFFERENT ARTIFACT WITH A
> DIFFERENT WRITER -- a human upload."*

### Instrument, and what a false answer looks like

Source read at `:262`; a token sweep for `boto3` across the whole module; a read of the cited card
(`W3-dljc`) at its committed bytes; and `s3api list-objects-v2` for the object. **A false answer on
the S3 half looks like `head-object` 404-ing on a shape mismatch** — this fabric measured that trap
today, so `list-objects-v2` was used instead.

### Measured

| claim | result |
|---|---|
| `:262` is a plain `open()` | **VERIFIED** — `with open(out, "w", encoding="utf-8") as fh:` |
| the cited card passage exists in `W3-dljc` `artifact.persistence.evidence` | **VERIFIED** — present, card `carded_by 0.8.0_AE_CloudComp~Y` |
| S3 object size 259,918 bytes at that exact key | **VERIFIED EXACTLY** — `Size: 259918`, `LastModified 2026-07-08T15:49:06Z` |

**Controls, both fired** (after a first attempt that did NOT — see below):
- POSITIVE: prefix `warehouse/cse_ingest_staging/` returns **2** objects.
- NEGATIVE: prefix `warehouse/NOSUCHKEY_zzz_9999` returns **no `Contents` key at all**.

**Denominator:** 3 of 3 sub-claims verified; 2 of 2 controls fired on the second attempt.

### ⛔ Two findings

**(a) "no boto3" is TRUE OF THE WRITE PATH AND FALSE OF THE FILE.** The module imports and uses
`boto3` at `:136-137` (`get_object`) and `:144-149` (`put_object`) for a marker object
(`MARKER_BUCKET`/`MARKER_KEY`). **So this module DOES write to S3 — just not this artifact.** The
entry's parenthetical reads naturally as file-scoped and is only correct read as line-scoped. The
conclusion (PATH A's artifact is a local file) is unaffected.

**(b) THE QUOTATION FROM THE CARD IS NOT VERBATIM, AND BOTH DIVERGENCES ESCALATE EMPHASIS.**
The entry presents the passage as read from the card itself. Compared byte-for-byte:

```
CARD  : ' ⚠ THE LOCAL FILE ... The S3 object above is that local file after a human uploaded it.'
ENTRY : '⛔ THE LOCAL FILE ... The S3 object above is that local file AFTER A HUMAN UPLOADED IT.'
         ^^                                                          ^^^^^^^^^^^^^^^^^^^^^^^^
         warning glyph -> interdiction glyph          lowercase -> uppercase
```

First divergence at offset +191. **Neither changes the meaning; both make the source seem more
emphatic than it was.** Recorded because the entry's own authority rests on having read the card in
full, and a re-emphasised quotation is the class this fabric names as *cite the act you witnessed*.

---

## ⛔ AN INSTRUMENT FAILURE OF MY OWN, DISCLOSED

My **first** pair of S3 controls returned `None` for both the positive and the negative arm. I had
used `--max-items 1 --query 'KeyCount'`; client-side pagination changes the response shape and
`KeyCount` is absent, so **both arms returned the same uninformative value.** A control set where
both arms return `None` cannot distinguish anything — the exact "a claim that cannot fail was not
tested" case this TO warns about, and I nearly recorded it as controls-run.

Re-run with the **same query shape as the measurement itself** (`Contents[]`), both arms then
discriminated. **The rule: a control must use the instrument's real query shape, or it is testing a
different call than the one that produced the finding.**

## Summary

| entry | verdict | sub-claims | controls | findings |
|---|---|---|---|---|
| `[8]` | **STILL TRUE** | 7 of 7 | 2 of 2 fired | 1 phrasing imprecision (`get_catalog()` precedes the raise) |
| `[9]` | **STILL TRUE** | 3 of 3 | 2 of 2 fired (2nd attempt) | boto3 present in-file though not in-path; quotation re-emphasised vs the card |

**Neither entry is `NO LONGER TRUE`, `UNMEASURABLE`, or `WAS NEVER MEASURED`.** Both were held at a
named vintage, both re-derive cleanly at that vintage, and the two entries in this tranche are among
the best-evidenced in the block — each already carries its own source citations and its own
withdrawal of a superseded reason.

**Nothing was refused.** Neither entry required a held artifact.
