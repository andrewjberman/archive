# FIDUPL msg 8990 -- the G-scoped export probe: the export is identical under every G number tested

Author 2.0.0_SA_COO~P1, 2026-10-21 ~05:55Z. Counts, ordinals and hashes only; no G number, label, account number or id appears here.

## Result (one sign-in, SSM 36fff741, 05:46:18Z to 05:47:04Z, 11 requests, no 401/403/refused switch, starting G restored)

Record: `org/missions/D8/NFRA/NFRA_FIDUPL/deliverables/0.7.0_AE_CloudOps~NFRA1/NFRA_FIDUPL.TO-FT-s-8.step2Gv2_g_export_probe_output.md`. Day 2026-10-20. For ordinals 0 (the start), 1 and 15 of the 31:

- the Export Status list: 6 elements, all 6 files COMPLETED, 1 profile, 1 request, `ids_sha8` d79c7806 (same on all three);
- `account.txt`: 3,794,367 bytes, 5009 rows, `sha8` 94a0f611, `line1_sha8` 8a4cbf3b (same on all three).

The landed 2026-10-19 `account.txt` in S3 (`fidelity/alongside/bronze/account/20261019/`) has the same byte count, row count and `sha8`: the file read under every G is the landed file, byte for byte.

## What is now measured about the G number (four instruments, all agree the switch scopes nothing we can read)

1. The change form switches the session's Current G (31 of 31, Current: re-read each time).
2. `accountList.json` answers `available=5204` after each of the 31 switches (probe 2P-v2).
3. The scheduled export is ONE profile, one request id: the same six files whatever the G (this probe).
4. No file carries the G: the landed `account.txt` (5009 x 141) has no G-shaped value and no column near 31 or 8 distinct values; the other five files hold G-shaped tokens only in security-identifier columns (position 11 distinct, prices and security 11 each), not account-grain.

So the G number does not scope the list, the export or the files in this session. What the switch changes is NOT yet known (home tiles, reports, worklists are candidates; the browser also refreshes `ATC`/`ATCTO` after each switch).

## Routes that remain (from the CRO's research, RESEARCH_20261019_NFRA_FIDUPL_G_NUMBERS.md and the UI bundle)

- (a) One scheduled export profile PER FIRM, filtered to the firm's G numbers: needs the Custom Export wizard's step 3 "Choose Filter" to offer a G number filter; never captured.
- (c) `accountSearch.json` (POST, JSON array of `{column, operator, value}`): the UI's own narrowing call; a G-number column in its filters is unmeasured. `worklist/criteria-fields.json` lists a `gnumber` access-attribute field (the 31).
- (e) `verify.json` per account carries `gnumberAssociations` (empty on the one account captured).
- Crosswalk by the firms' own sources (CRO section 2): 1,418 of 5,007 accounts claimed by exactly one firm (inflection 779, cottonwood 639), 3,589 unclaimed.

The cheapest next read is the wizard's step 3 and the criteria shown in the UI's account search, by an agent-driven walk of the box's Chrome over CDP (names only, nothing saved or created).
