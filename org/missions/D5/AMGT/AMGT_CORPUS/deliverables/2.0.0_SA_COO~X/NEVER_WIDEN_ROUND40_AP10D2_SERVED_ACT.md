# AMGT_CORPUS round 40 -- never-widen pair for `CRPS-ap-10 (d2)`: write the 95 research dossiers at method version 7 (the method-6 values less five trailing fragments)

**Authority:** `1.0.0_SA_CTO~Z` ruling msg 31382 (the narrow rule; "end at the last sentence end" withdrawn; then "the write at the
amended method, the trim census on all 950 with every dropped tail printed, and the re-read by `3.0.0_SA_CVO~Z`"), on the CVO's
grade of the 25 gained passages (`AMGT_CORPUS_ROUND40_AP10D_GAINED_PASSAGES_GRADE_20261007.md` @`32c6593acf`). It follows pair
(d): `NEVER_WIDEN_ROUND40_AP10D_SERVED_ACT.md` @`14c896b419` / CTO half @`b39724f085`, whose write landed 95 objects at method 6
(ledger `amgt-corpus-r40-ap10d`, leg w closed @`263b50310e`).

**Code:** CLOUD at or after `c68a1954ff` (the AMENDMENT 5 drain), `lib/research/corpus/dossier.py` equal to `901be95e86`'s.
`METHOD_VERSION` is `amgt-corpus-dossier/7`. Stored today: 95 objects at `/6` (the newest of each name), under them the `/5`
objects the live route serves.

## WHAT METHOD 7 IS, AGAINST METHOD 6

One rule added: in a section value, when the text after the LAST sentence end is one or two words, that fragment is dropped
(`_drop_trailing_fragment`, on the whole value text, lead line included). Three or more words, or no sentence end: unchanged.
AMENDMENT 4's wider rule was built, measured and withdrawn before any write (evidence @`5c91f70680`: 32 fields, 4,114 characters,
about 14 complete bullet points dropped); it is in no stored object.

## THE TRIM CENSUS ON ALL 950 FIELDS, EVERY DROPPED TAIL PRINTED (read-only, 20:52Z-20:54Z)

`checks/round40/ap10d2_trim_tails.py`, the current code re-composed in memory against the 95 stored method-6 objects
(`evidence/r40_ap10d2_trim_tails_after_a5_20261007.txt`): **5 fields change, 55 characters dropped in all, 0 other changes.**

| name | field | kept ends | dropped |
|---|---|---|---|
| NKE US | special items | "...from the US Tax Cuts and Jobs Act." | " 4_7_2026" (the source file's date; the regression the CVO named) |
| SAP GY | positives | "...the software is too mission-critical." | " sec" |
| ST SP | management | "...is expected to come from." | " Asdsa" |
| SPOT US | management | "...total remaining authorization $1.4bn)." | " Supporting documentation:" (the next heading) |
| SPOT US | why we own | "...to capitalize on the opportunity." | " It should" (two words of an unfinished sentence) |

The first two are the CVO's two misses. The other three were not among the 25 gained values; the census found them.

**KNOWN-TRUNCATED, served as stored (ruled):** six values of the 25 stop mid-sentence and are unchanged by method 7: LLY US
negatives ("...guidance ceiling was actually lowered"), NU US positives ("...approval completed digital bank"), NU US negatives
("...Mexican deposits declined slightly"), QXO US negatives ("...Sell-side estimates kept"), UNH US negatives ("...billing
practices remains"), SHOP CN management ("...created open-source libraries like"). Each is the section's own prose up to where
the block reader stops; the cell that reads across page breaks is first in round 41. The AMENDMENT 4 read shows more values of
the same kind outside the 25 (among its 32 tails: V US, WDAY US, UNVGY US, LLY US why we own; 8766 JP management; ICICI, OMAB,
SAP thesis); they are not changed by this act. Whether the method-5 values the page serves today end
the same way was NOT measured.

## THE ACT, IN ORDER (ledger `amgt-corpus-r40-ap10d` stays the entry: leg v is open; this act is recorded on it and in a new
entry `amgt-corpus-r40-ap10d2`, opened before leg w)

0. **Gate.** The CTO half signed. `git diff 901be95e86 HEAD -- lib/research/corpus/dossier.py` is empty.
1. **(w)** `python -u -m lib.research.corpus.dossier --write --workers 16`, with NO time limit on the command (pair (d)'s first
   run was cut by this seat's own 580 s limit). Each name writes ONE new object through `gold.gold_put`, which never overwrites;
   a method bump is never a no-op, so 95 names write. Expected: `names 95 written 95 existed 0`. About one to two hours.
2. **(v)** on CLOUD code: the pick reads method 7 for 95 of 95; `--short-passage-census 40`: `total_short 0`;
   `--section-recompose-census`: `fields_changed 0`; `ap10d2_trim_tails.py`: `changed 0 fields`, and the eight named values
   printed as stored. Then `3.0.0_SA_CVO~Z` re-reads the 25 from the method-7 objects. The live-route reads follow AMGT_RESAPP
   bb-18's deploy, which pins `dossier.py` only after that re-read (msg 31382).

## EXPECTED OUTCOME (every branch)

- **Writers:** a dossier object has 1 writer (`dossier.write_one`, reached only from `--write`); the reader's pick has 1 rule
  (`read_dossier`: the newest object of the READER's own method, else the newest of all).
- **Branch A:** 95 written; the four reads of leg v as stated.
- **Branch B (some names fail):** each is listed; a failed name keeps its method-6 object as its newest. The run is repeated for
  those names only after the error is read.
- **Branch C (the run is interrupted):** written names are at 7, the rest at 6; the re-run writes the rest and reports `existed`
  for the written ones. No name can carry two method-7 objects from one day's inputs (same `inputs_sha16`, same key).
- **Between w and bb-18 (expected):** the live route serves method 5, unchanged. If bb-18 deployed BEFORE this write with
  `dossier.py` at 7, its reader would find no method-7 object and serve the newest of all, the method-6 values, Nike's stray date
  among them: bb-18 follows this write and the re-read, as ruled.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition (a third object dated 2026-10-07 beside the method-6 one, a different `inputs_sha16` because the method is hashed in) | nothing served moves before bb-18, so nothing to roll back. After bb-18: re-deploying the API package at method 5 serves the `/5` objects again; no delete |

Never touched: any Bloomberg or vendor call, the model blocks, the crosswalk pool, `field_map.json`, the scheduled task, any
portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-07 20:56Z, for legs 0, w and v, covering branches A to C and the window before
bb-18.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
