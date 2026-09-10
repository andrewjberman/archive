# AMGT-s-12 -- THE IDENTITY LAYER: THE ROOT

Worker: `0.9.0_WK_AMGT_RESAPP~3` | Task order:
`org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-s-12.identity-layer-the-root.md`

## AMENDMENT 1 (reopen, row AMGT_RESAPP-Z-W7-S3) -- the shared-template-placeholder fix

`0.9.0_WK_AMGT_RESAPP~7` measured (re-measured by `2.0.0_SA_COO~ZZZ` at HEAD) that 16 of the original 48
MEASURED `bloomberg_ticker` values in `universe.json` were the single string `"AAPL US"`, each read
honestly from a "FactSet Based ONE PAGER" workbook's plain `Model` sheet at row 2 beside `"Ticker:"` --
on AstraZeneca, Canadian National Railway, Clorox, Copa, Imperial Brands, JD.com, Michelin, Mitsubishi
UFJ, Nestle, Nokia, Orange, SAP, Sanofi, Shopify, Tokyo Marine and TotalEnergies (none of which is
Apple). The per-folder scan could read the cell correctly and still be wrong, because a per-folder read
cannot tell a filled-in cell from an unfilled template default -- both are syntactically valid
Bloomberg-shaped strings. That is exactly the shape of defect F6 measures on the CSC sheet, just found on
the identity block instead, and it was invisible to AC1-AC5 because every one of them is a per-member or
per-key check; none of them reads what the MEMBERS SHARE.

**The fix, in `build_universe.py`:** a new whole-population pass,
`_detect_and_downgrade_shared_placeholders()`, runs AFTER the per-folder scan and BEFORE the partition is
computed. The rule it applies (task order AC7, C-SHARED-DEFECT): **a MEASURED ticker value held by two or
more folders is the shared template's default, not any one of those folders' subject ticker** -- every
folder holding it is downgraded to UNRESOLVED, evidence naming the shared value, the sibling-folder count
and names, and the original per-folder read (workbook/sheet/cell) that produced it; `sa_symbol` is
recomputed too, since it was `INFERRED` off a value that no longer stands. The general rule is preferred
over an enumerated `"AAPL US"` ban because an enumerated ban lapses silently the day the template ships a
different example ticker; the literal is kept ONLY as a non-enforcing sanity constant
(`_KNOWN_TEMPLATE_PLACEHOLDER_TICKERS`) that prints a `WARN:` if it ever survives as MEASURED after the
general pass runs (it does not, on this corpus, at this vintage).

**Partition, before and after** (89 of 89 folders both times, denominator unchanged):

| | MEASURED | INFERRED | UNRESOLVED |
|---|---|---|---|
| Original (instance @9377323a70, text pre-amendment) | 48 | 0 | 41 |
| After the fix (this instance) | 32 | 0 | 57 |

The 16-folder delta is exactly the `"AAPL US"` set above (`universe.json`'s
`shared_ticker_placeholders_downgraded` names all 16 by folder). `sa_symbol` moved from `INFERRED 26` to
`INFERRED 10` for the same reason (all 16 downgraded names had a `" US"` suffix and had been `INFERRED`
off the placeholder). **The original measurement is not deleted** -- it is preserved verbatim below as
the measurement of the pre-amendment text, and in the proof instance's `session_log` note.

## What is here

| File | What it is |
|---|---|
| `lib/research/identity/resolver.py` | (a) the resolver module -- `resolve()`, `render_together()`, `make_cell()`, `infer_sa_symbol()`. No network call, no vendor host named (AC4). |
| `lib/research/identity/self_test.py` | (f) the self-test. `python -m lib.research.identity.self_test` -> `IDENTITY SELF-TEST: 4 keys, 3 statuses, unresolved-refused=True, resolved-admitted=True: PASS` (AC1). |
| `lib/research/identity/build_universe.py` | the script that produced `universe.json` -- not separately named by the cell text, written for reproducibility and because it demonstrates `resolver.py`'s cell shape and `infer_sa_symbol()` rule in real use over the corpus. |
| `universe.json` | (b) the coverage universe: one entry per name folder (89 of 89), each carrying the four identity keys as cells. |
| `f6_remeasure.py` / `f6_remeasure.json` | (e) F6 re-measured on the live corpus. |

## (b) The coverage universe -- what it found

Corpus root: `C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared - Documents\Asset Management\Research\`
(read-only, outside the repo). Root mtime at read time: `2026-09-09T14:25Z`; read window recorded in
`universe.json`'s `read_started_at`/`read_finished_at`.

**Denominator measured, not assumed:** 89 name folders (`denominator_folders`). The brief's F6 cites 89 as
well, at its own 2026-09-10 vintage -- this build re-measured its own 89 independently, not quoted from F6.

- `workbook_partition`: 49 of 89 folders carry at least one `*ONE PAGER*.xlsx` workbook; 40 carry none (a
  `.docx`/`.pdf` earnings update instead, e.g. Adobe, China Construction Bank, British American Tobacco --
  measured directly, not assumed).
- `ticker_status_partition`: **MEASURED 32 / INFERRED 0 / UNRESOLVED 57** (post-AMENDMENT-1; originally
  MEASURED 48 / INFERRED 0 / UNRESOLVED 41 before the shared-placeholder pass -- see the AMENDMENT 1
  section above), summing to 89.
  - Of the (post-fix) 57 UNRESOLVED: 40 are folders with no one-pager workbook at all (evidence: "no
    *ONE PAGER*.xlsx workbook found in this folder"); 16 are the `"AAPL US"` shared-template-placeholder
    folders (AMENDMENT 1); **1 is a folder WITH a workbook that carries none usable** --
    `Rio Tinto RIO LN`'s `Model` sheet reads `Identifier = 'HESAY-US EQUITY'` with `Sector:` /
    `Location:` both `#N/A Invalid Security` beside it. That is not Rio Tinto's ticker (Rio Tinto is
    `RIO LN`) -- it is unrepointed, broken template residue, the same *shape* of defect F6 measures on
    the CSC sheet, just found on the identity block instead. `build_universe.py`'s ticker-shape validator
    (`_TICKER_SHAPE_RE`) rejects the hyphenated `HESAY-US` on structural grounds (Bloomberg ticker roots in
    this corpus never carry a `-`; the `#N/A` beside it corroborates that the cell is not live data) and the
    entry is correctly left UNRESOLVED rather than guessed.
  - A second incidental finding, same shape: `Walmart de Mexico WALMEX MM`'s `Overview` sheet carries, at
    row 15 col G, unrelated KPN/VodafoneZiggo fixed-line-market narrative text -- template bleed-through
    onto a retailer's one-pager. Its `Identifier` cell (`WALMEX* MM EQUITY`) IS valid and was read
    (MEASURED) once the ticker-shape validator was widened to accept the `*` character that this corpus
    uses as a footnote marker (measured directly on this workbook; not present anywhere in the sample used
    to write the first draft of the validator).
- `sa_symbol` over the 89: `INFERRED 10 / UNRESOLVED 79 / MEASURED 0` (post-AMENDMENT-1; originally
  `INFERRED 26 / UNRESOLVED 63` -- the 16-point drop is exactly the 16 `"AAPL US"` folders, whose
  `sa_symbol` had been INFERRED off the now-retracted placeholder and is recomputed to UNRESOLVED once
  `bloomberg_ticker` is UNRESOLVED) -- the rule (c) infers a slug only for US-listed names whose Bloomberg
  ticker ends ` US`/` US EQUITY`; every ex-US name (the majority of this corpus) is UNRESOLVED, honestly,
  rather than guessed.
- `ir_domain` and `social_account`: **UNRESOLVED for all 89**, every one with evidence `"no vendor word at
  this cut (G-24; ...)"` -- bound (d), exercised on the whole universe, not asserted in prose only.

## (c) The SA-symbol key -- what the rule does and does not claim

`infer_sa_symbol()` in `resolver.py` applies exactly the rule the cell text states: a US-listed name's SA
slug is INFERRED to equal its Bloomberg ticker root (e.g. `BABA US` -> `BABA`); an ex-US name has no stated
slug rule at this cut and is UNRESOLVED (the cell text permits "INFERRED with lower confidence OR
UNRESOLVED" for ex-US names -- UNRESOLVED was chosen here rather than a guess with no stated basis, since a
guessed slug that never resolves would sit in the record looking more confident than it is). **No sa_symbol
cell is ever MEASURED by this order** (AC5) -- the numeric `sa_id` and the SA fetch path stay
AMGT-s-b4's, per Andrew-direct @d09e26e1b1 / `1.0.0_SA_CTO~Z` msg 21056: this order is not a procurement
order.

## (d) IR domain and social account -- KNOWN and SAID, not resolved

Both keys are UNRESOLVED for every one of the 89 folders in `universe.json`, and for `resolve()`'s output in
general. Evidence on every cell: `"no vendor word at this cut (G-24; a SERP zone request would be
required)"` / `"...a social lookup would be required"`. This is bound (d) exercised over the whole
universe, mechanically, not merely asserted -- see AC5's zero counts.

## (e) F6 re-measured

`f6_remeasure.py` re-derives F6 independently, with the method the cell text states (read each
`*ONE PAGER*.xlsx` workbook's `CSC` sheet -- not a "SAP sheet"; no sheet named `SAP` was found on any
workbook measured while building this script, and the CRO's own text gives no numeric threshold either --
so this script states its own: overlap >= 6 of the fixed 12-name KPN set counts as "stale"). Denominator:
54 workbooks across the 89 folders (not 89 folders -- measured directly: `Imperial Brands IMB LN` alone
carries two `*ONE PAGER*.xlsx` files that DISAGREE with each other, one the stale KPN copy, one its own
analyst-chosen peer set, which is only coherent if the population is workbooks, matching F6's own "all 54
... workbooks" wording).

**Result at this cut: stale-set 48 / own-set 4 / no-CSC 2 of 54 workbooks** -- an exact match to the brief's
CITED 48/4/2 of 54, independently re-derived rather than quoted. Full per-workbook classification, extracted
ticker lists and the fixed KPN-set definition are in `f6_remeasure.json`. Agreement with the CITED figure is
a FINDING (`agreement_with_cro_cited` in the JSON), not a proof of either method -- this script's overlap
threshold and sheet-scan are its own, stated in the script's docstring so a re-run is reproducible.

## AC6 (judgment) -- what this deliverable says and does not say

Per key, per record, this layer says plainly what it could not resolve and why:

- **bloomberg_ticker**: MEASURED where a workbook carried a readable, shape-valid identifier that no other
  folder also carries; UNRESOLVED where the folder has no one-pager workbook, the workbook's identity
  block is itself broken residue (Rio Tinto), or the value is a template default shared by two or more
  folders (AMENDMENT 1, the `"AAPL US"` set -- AC7). Never guessed from the folder name -- evidence always
  cites the workbook path and the sheet/row the value came from, and a downgraded cell's evidence also
  names the sibling folders that share the value and the original per-folder read it superseded.
- **sa_symbol**: INFERRED only for US names via the stated ticker-root rule, evidence naming the rule and
  the input ticker; UNRESOLVED everywhere else, including every non-US name and every folder with no
  ticker to derive from. Never MEASURED (AC5).
- **ir_domain / social_account**: UNRESOLVED everywhere, always, evidence naming the missing vendor word
  (G-24) rather than a placeholder value.

**Reproducibility:** both `build_universe.py` and `f6_remeasure.py` read only the live corpus (no repo
fixtures, no cached snapshot) and print their own vintage (`corpus_root_mtime`, `read_started_at`/
`read_finished_at`) beside every count. A reader re-running either script against the same corpus at the
same vintage (root mtime unchanged) gets the same partition -- both scripts are deterministic (no randomness,
no network call, sorted folder/file iteration) and every non-MEASURED cell's `evidence` states the specific
rule or absence that produced it, not a bare "unknown". Re-running `f6_remeasure.py` right now (after
`universe.json` was written) reproduced the identical 48/4/2 of 54 on the second pass, confirmed above.
