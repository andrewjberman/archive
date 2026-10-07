# GRADING_READ -- AMGT-ba-15, round 77, 0.9.0_WK_AMGT_RESAPP~281

Measured at base ed5cadfd4a on this device, 2026-10-06. Read-only: served crosswalk, research library list, U-1 universe. No write, no vendor call.

## 1. Keyed N of 89

`python -m lib.research.identity.covered_keyed` (output kept beside this file, `covered_keyed.out.txt`):

    keyed 89 of 89 (crosswalk 89, corpus 0)
    crosswalk loaded from s3://opal-data-harvest/crosswalk/v1/2026-09-29.json; corpus read True, 96 records
    DE_US_Equity among the research library's keys: False

- Denominator: 89 coverage folders (`len(universe.json["names"])`). keyed 89 + residual 0 = 89.
- Split: served crosswalk 89, research library 0 (the library list was read, 96 records with a key, and was needed for none of the 89).
- Residual: none. Every coverage folder is keyed by the served crosswalk. The "33 of 89" in the ruling is the 2026-09-10 snapshot.
- Control (planted, in `tests/test_covered_keyed.py`): a folder the library does not hold stays out with its reason; with the library unread nothing resolves through it.

DE (row Z-W20-S12): `DE_US_Equity` is not among the research library's 96 keys, and no served crosswalk record carries a `DE_` key or a Deere folder. It stays unkeyed, with the reason "the research library holds no key for it".

## 2. Holdings re-read (ruling item 3)

Read the way `lib/research/posture/membership.py` reads it: `universe/v1/2026-10-06.json` (latest of 3 objects under `universe/v1/`), `universe_denominators`:

    names 302; holding rows 167; resolved 107; unresolved 60

- Holding rows with no resolved key: **60 of 167** (the 167 of 170 in row Z-W19-S6 was the 2026-09-15 object; the tri-state `held None` stays).
- Of the 60: 0 carry a CUSIP, FIGI or SEDOL field; 60 name a root-equal candidate in their reason; 57 carry positioning-chain CUSIP evidence in the reason text; 11 share a ticker root with a research-library key. The 60 are the ADR and ordinary-share lines (e.g. BBSEY, BKRKY, NSRGY) plus cash and money-market lines (CASH, FXFXX, SALXX).
- These need a vendor identifier map to join, not a read. Nothing built. ONE row filed with the count (60): `AMGT_RESAPP-Z-W281-S1`.

## 3. Folders with two or more ONE PAGER workbooks (5 of 89, as the row measured)

Each line is `one_pager_precedence.line()` over the research library folder:

1. Imperial Brands IMB LN: read Imperial Brands FactSet Based ONE PAGER 2026 07 17_v1.xlsx (modified 2026-07-20); superseded Imperial International Dividend One Pagers.xlsx (modified 2026-07-17)
2. Nokia FH: read Nokia FactSet Based ONE PAGER TEMPLATE 2026 04 22_v2.xlsx (modified 2026-06-01); superseded Nokia FactSet Based ONE PAGER TEMPLATE 2026 04 22_v1.xlsx (modified 2026-06-01)
3. Petrobras PETR3 BZ: read Petrobras FactSet Based ONE PAGER TEMPLATE 2026 04 15_v1.xlsx (modified 2026-04-21); superseded Petrobras International Dividend One Pagers.xlsx (modified 2026-04-15)
4. SAP GY: read SAP FactSet Based ONE PAGER 2026 07 01_v1.xlsx (modified 2026-07-01); superseded SAP International Dividend One Pagers.xlsx (modified 2024-11-07)
5. Total Energies TTE FP: read Total Energies FactSet Based ONE PAGER 2026 04 02_v1.xlsx (modified 2026-04-02); superseded FactSet Based ONE PAGER TEMPLATE 2026 03 09_v1.xlsx (modified 2026-04-02)

Two lines (Nokia, Total Energies) tie on the printed day; the order uses the full stored time, so the precedence is decided below the day.

## 4. Hookup for the issuer (not edited here)

`lib/research/identity/build_universe.py:145` (end of `_find_one_pager_files`): `return one_pager_precedence.ordered(folder_path, matches)` in place of `return sorted(matches)`, with `from lib.research.identity import one_pager_precedence`.
