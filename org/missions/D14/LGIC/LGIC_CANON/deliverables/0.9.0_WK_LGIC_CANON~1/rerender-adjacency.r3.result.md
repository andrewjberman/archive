# LGIC_CANON.TO-CN-k-4-r3 -- result (cell CN-k-4, round 3)

**Worker:** `0.9.0_WK_LGIC_CANON~1`. **Worktree:** `.worktrees/wk-lgic-canon-3-1`, branch `wk-lgic-canon-3-1`,
cut from CLOUD at `881b419753`. **Commit carrying the edit + surprise row:** `68b2ca86f7`.

## Baseline (pre-edit, this worktree at spawn)

`python infra/logic/render_naming_section.py --content-diff` read `CONTENT-DIFF: 17` -- every dropped item
under `/alias_adjacency/` (`org/standards/NAMING_SCHEMA.json` gained the field at v1.10, @5a12d0b97c) plus
`/refused_tokens/bd`'s updated note text (the same v1.10 edit). `--check` read `CHECK: STALE`, stamping the
schema at v1.9. No `EXCLUSION-PREDICATE` line existed at all -- `--content-diff` had no producer census.

## What the edit did, per WORKER FACE instruction

1. **Re-render (alias_adjacency).** `render_naming_section.py`'s `render()` gained an "Alias adjacency"
   block in N4, rendered from `schema["alias_adjacency"]`: per token, `reads_as`, `test`, `either_way`,
   `source`, and an `examples` table -- every string carried byte-for-byte from the schema, never
   paraphrased, so the content-diff arm's substring comparison passes on it. `--write` re-rendered the
   canon; the section now stamps `NAMING_SCHEMA.json v1.10` and `--check` reads `CHECK: FRESH`.

2. **The producer exclusion's predicate, made mechanical (A-20).** `producer_consumer_census()` runs over
   `git ls-files` (excluding the renderer, the schema and the canon) and content-diff now prints
   `EXCLUSION-PREDICATE producer: <n> consumer(s) of <m> file(s) scanned`, and, only while `n` is 0,
   `EXCLUDED: /key/legacy_served_paths/producer -- no consumer reads it`. Match rule, stated verbatim in
   `--content-diff`'s `--help` text (two arms, MECE over "code or documents that read the field"):
   - CODE ARM: a file with a code extension (`.py .js .jsx .ts .tsx .mjs .cjs .sh .ps1`) carrying an access
     chain from `legacy_served_paths` to `producer` -- bracket indexing or dotted attribute access.
   - DOCUMENT ARM: any tracked file reproducing the field's own value text verbatim, in any file type.

   A first draft used a looser same-line co-occurrence rule and measured 13 "consumers" -- including
   `check_canon_r3.py`'s own `PRODUCER = "/key/legacy_served_paths/producer"` line, which greps the
   RENDERER's OUTPUT and never opens the schema (a mention of the path string, not a read of the field),
   and two round-2 markdown records that only discuss the earlier drop (row LGIC_CANON-W2-S4). Since
   `check_canon_r3.py` is a fixed, un-editable input, that rule could never reach `n=0` regardless of the
   true state, so it was replaced with the two-arm rule above.

   **Measured at this commit: 4 consumers of 36,940 files scanned** -- the four LGIC_NAMING grading-exercise
   prompt files (`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/{r2,r3}/seats/{e1,e2}.prompt.txt`)
   embed the whole `NAMING_SCHEMA.json` verbatim as a fixture, reproducing the producer note's value text
   (document arm). So the exclusion does **not** currently hold, and per the task order's own instruction
   ("When `<n>` is above 0 the exclusion drops and the item is compared like any other") the item enters the
   content-diff domain. `render()` now also carries the producer note in N1
   (`- **legacy served paths producer:** ...`), rendered **unconditionally** -- while the census reads 0 this
   is extra disclosure the canon is not obligated to carry; the moment a reader exists (as measured) it is
   required -- so `CONTENT-DIFF: 0` holds whichever way a later run's census reads. Filed as surprise row
   `LGIC_CANON-W1-S5` (OBSERVATION, INERT): the task order's framing ("absent until LN-g-1 lands it")
   assumed the census would read 0; the measured, mechanical answer is 4.

3. **Commit, then grade.** Both files committed at `68b2ca86f7` before any criterion ran.

**⛔ Nothing live moved:** `org/standards/NAMING_SCHEMA.json` and `infra/logic/registry/scopes.json` are
untouched (not in `<paths>`, not edited). The canon's generated section is the ONLY thing that changed in
`02_DOCTRINE.md` -- `git show --stat 68b2ca86f7` shows the diff confined to the marked section (plus the
renderer and the investigation file).

## Deciding output, each mechanical criterion, at commit `68b2ca86f7` (clean worktree)

```
$ python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py k4-fresh
the section stamps the schema: True ; render --check FRESH: True
VERDICT: PASS-K4-RERENDERED-AT-SCHEMA
```

```
$ python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_canon_r3.py k3-contentdiff
PLANTED REMOVAL (the negative control this criterion claims):
  candidates tried before one moved the count: 2
  removed line: - **ruled:** Andrew-direct 2026-09-13 ~03:2xZ card 1, verbatim; the five segments and their order ar
  TRUE tree   -- CONTENT-DIFF: 0  (0 required for PASS)
  DOCTORED    -- CONTENT-DIFF: 1  (must EXCEED the true tree's)
  the control fires: True
  file restored byte-identically: True
a clean run alone proves nothing; the arm must be shown to FIRE (W2-S3)
VERDICT: PASS-K3-CONTENTDIFF-PLANTED
```

```
$ python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_canon_r3.py k4-producer
producer consumers 4 of 36940 file(s) scanned; EXCLUDED line printed: False
the exclusion must hold exactly while the consumer count is zero (A-20)
VERDICT: PASS-K4-PRODUCER-PREDICATE
```

```
$ python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py k3-note
FIRM rows in the registry carrying a note, denominator 1: ['demo']
of those, rendered into the canon's generated section: 1 -- ['demo']
every FIRM note reaches the section: True
VERDICT: PASS-K3-FIRM-NOTE-RENDERED
```

Full `--content-diff` on the true tree at this commit (tail):
```
EXCLUSION-PREDICATE producer: 4 consumer(s) of 36940 file(s) scanned
NOT EXCLUDED: /key/legacy_served_paths/producer -- 4 consumer(s) found, compared like any other item: [...]
...
items carried by the section: 217 of 217
CONTENT-DIFF: 0
```

Determinism: `--content-diff` run twice back-to-back on the unchanged tree prints the identical
`EXCLUSION-PREDICATE producer: 4 consumer(s) of 36940 file(s) scanned` and `CONTENT-DIFF: 0` both times.

**K4R3-AC5 (judgment, for `3.0.0_SA_CVO` at L9):** the census's match rule is stated verbatim in
`--content-diff`'s `--help` output (both arms, above); the canon's generated `bd` reading now carries the
schema's `alias_adjacency` content (the `Alias adjacency, closed list (1): \`bd\`` block in N4, with
`reads_as`, `test`, `either_way`, `source` and the four-row `examples` table, all byte-identical to the
schema). No verdict is recorded here; this row is `UNVERIFIABLE-BY-INSTRUMENT` naming `3.0.0_SA_CVO`.
