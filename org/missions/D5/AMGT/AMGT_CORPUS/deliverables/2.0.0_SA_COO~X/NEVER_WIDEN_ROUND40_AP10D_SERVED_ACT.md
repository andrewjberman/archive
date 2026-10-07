# AMGT_CORPUS round 40 -- never-widen pair for `CRPS-ap-10 (d)`: re-write the 95 research dossiers at method version 6, so a bare heading is no longer served as a passage

**Authority:** round-39 analysis @`5ccdc90368` ruling 9 (row `Z-S89`); `1.0.0_SA_CTO~Z` ruling msg 31134 ("fix the block reader
first; no dossier re-write until the census reads after it"; a heading followed by a table says a table follows; the re-write is
its own pair, written on the after-census). Decomposition v40.0 @`be3481c83e` s.1. Producer change CRPS-ap-6 with AMENDMENTS 1 to
3, last drain @`c9b59a78e4` (`lib/research/corpus/dossier.py` last changed at `04e5612a71`).

**Code:** CLOUD at or after `c9b59a78e4`, with `dossier.py` equal to `04e5612a71`'s. `METHOD_VERSION` is `amgt-corpus-dossier/6`;
the served dossiers are at `/5`.

## WHAT THE CODE CHANGES (three amendments, each from a measurement)

1. The build: a section block that is only its own heading reads absent, not the heading.
2. AMENDMENT 2 (the census found prose the reader stopped before): an unnamed heading-like item DIRECTLY after a section's lead no
   longer ends the block; a named lead still does. The absent reason says "is followed by a table and no prose" or "has no prose
   following it in the extracted text", never "no text".
3. AMENDMENT 3 (the after-census found page furniture served as prose; the issuer's own rule): a block is a passage only when its
   items after the lead carry prose -- one item over the heading word cap (8 words), or 25 or more words in all.

The recommendation, risks, pillar and case paths and `_PASSAGE_CAP` are untouched.

## THE CENSUS BEFORE AND AFTER (the proof the CTO's term 1 asks; read-only, real S3 reads, nothing written)

| read | result |
|---|---|
| served, `--short-passage-census 40`, 15:19Z (`evidence/r40_ap10_short_passage_census_20261007.txt`) | names 95, dossiers 95, unread 0, fields 950; 49 served values are a bare heading: management 4, thesis summary 1, special items 11, positives 11, negatives 10, comparison set 12 |
| re-composed in memory on the final code, `--section-recompose-census`, 16:46Z (`evidence/r40_ap10_section_recompose_census_after_a3_20261007.txt`) | names 95, fields 950, **changed 51, in 35 names**; of the 49: **gain prose 23, absent with the table reason 2, absent with the no-prose reason 24**; 2 changes are outside the 49 |

Every changed value is listed in the after file. By field:

| field | gains prose | absent, table | absent, no prose |
|---|---|---|---|
| positives | 11 | 0 | 0 |
| negatives | 10 | 0 | 0 |
| management | 2 (AZN LN, SHOP CN) | 1 (8316 JP) | 1 (8306 JP) |
| special items | 1 (NKE, outside the 49) | 0 | 11 |
| comparison set | 0 | 1 (9433 JP) | 11 |
| investment thesis summary | 0 | 0 | 1 (8316 JP) |
| company description | 1 (CLX, outside the 49) | 0 | 0 |

The two named fail cases of ruling 9, 8306 JP and 8316 JP "Management/Board 80", both read absent. The intermediate census after
AMENDMENT 2 alone (`evidence/r40_ap10_section_recompose_census_20261007.txt`) is kept: it counted 41 gains, of which 17 were a page
header, a page number or a table's date; AMENDMENT 3 turns those 17 into absent and takes one more special-items heading with them.

**Stated limits.** (a) 11 comparison-set sections read "no prose following it in the extracted text" where the report most likely
holds a table: a pdf extraction does not tell a table from nothing, so the reason says what was read. (b) The 23 gains were read by
this seat as their first 70 characters, not whole. (c) A gained value begins with the heading and, in a pdf, the bullet mark
("Positives - Revenue ..."), as every served section value already does. (d) The census compares SECTION fields only.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r40-ap10d`, opened before leg w)

0. **Gate.** The CTO half signed. `git diff 04e5612a71 HEAD -- lib/research/corpus/dossier.py` is empty.
1. **(w)** `python -m lib.research.corpus.dossier --write` (serial). Each name writes ONE new object
   `security_key=<KEY>/as_of=<UTC date>.<inputs_sha16>.json` through `gold.gold_put`, which never overwrites; a method bump is
   never a no-op, so 95 names write. Expected: 95 `put_performed 1`.
2. **(p) NOT THIS SEAT'S LEG, and the write does not serve without it.** `read_dossier` picks among the objects that carry
   the READER'S OWN `METHOD_VERSION` when any exist (`dossier.py:1439-1453`, CRPS-j-4), and the scoped API calls it
   (`lib/research/api/scoped_amgt.py:4954`). The deployed API package holds `dossier.py` at `/5`. So after leg w the live route
   KEEPS serving each name's `/5` object, until the scoped API package is deployed with `dossier.py` at `/6`. That deploy is
   AMGT_RESAPP's release act under its own ledger entry; this half asks for it and does not make it.
3. **(v)** after (p): `--short-passage-census 40` on the served dossiers: `total_short 0` for a bare heading (a served value under 40
   characters, if any remains, is listed and read). `--section-recompose-census`: `fields_changed 0` (both run on CLOUD code, which reads the `/6` objects as soon as leg w lands, so they can be read BEFORE
   (p) as the write's own check). Then, after (p), one live-route read of
   one gained name (TSM US positives) and one absent name (8306 JP management) through the scoped API: the value and the reason
   as the census printed them.

## EXPECTED OUTCOME (every branch)

- **Writers:** a dossier object has 1 writer (`dossier.write_one`, reached only from `--write`); the reader's pick has 1 rule
  (`read_dossier`: the newest object of the current method).
- **Branch A:** 95 written, the two census reads as stated, the two live reads match.
- **Branch B (some names fail to compose or write):** each is listed with its error; a failed name keeps serving its `/5`
  dossier. The census then reads those names as still changed.
- **Branch C (the after-census at leg v lists a served bare heading or a changed field):** it is read line by line and comes to
  the CTO; no second write without a ruling.
- **Between w and p (expected, not a branch):** the live route serves the `/5` values unchanged; the `/6` objects are stored and
  unread by the deployed reader. A page read in this window shows the bare headings still.
- **Branch D (after p the live route still serves a `/5` value for a written name):** the deployed package's `METHOD_VERSION`
  is read; the write stands and is not repeated.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; no existing object is overwritten or deleted | before leg p nothing served has moved, so there is nothing to roll back. After p: the prior `/5` objects stay stored, and re-deploying the API package at `/5` serves them again (the reader then prefers `/5`); no delete is needed |
| the Security Analysis page and the print pack, for 35 names, ONLY after leg p | 51 section values: 25 gain their prose, 26 read absent with a reason where a heading was shown | as above |

Never touched: any Bloomberg or vendor call, the model blocks, the crosswalk pool, `field_map.json`, the scheduled task, any
portal file, any other firm.

## NOT COVERED BY THIS HALF

- The 11 comparison-set sections whose content is a table: serving the table is not this cell.
- Any change to how a gained value is trimmed of its heading or bullet mark.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-07 ~17:0xZ, for legs 0, w and v, covering branches A to D and the window
between w and p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
