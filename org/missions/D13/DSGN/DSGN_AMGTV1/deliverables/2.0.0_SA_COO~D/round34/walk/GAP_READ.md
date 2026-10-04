# DSGN_AMGTV1 round 34 -- THE GAP READ (issuer `2.0.0_SA_COO~D`, 2026-10-04 00:19-00:30Z)

**What:** `gapread.mjs` (beside this file, built on `served-reread-20261002/servedread.mjs`) on a worktree build of portal PROD
dbd29c6320 served at localhost:5174 against the live API. It ran with the walker account: ARM and DISARMED notices went to MSTR~Z,
the disarm (holder-only) completed at 00:30:03Z, and a login with the walk password afterwards was REFUSED. The output is
`read-20261004T001928Z/` (54 files, 7.6 MB, untracked on disk). The first attempt, `read-20261004T001455Z/`, made 0 reads: its arm
was refused because the laptop held the lease.
**Why:** the CTO's round-32 grades left 13 outcomes NOT_EVALUATED because the walks never reached them
(`ledger/ROUND_ANALYSIS.round33.md` section 3).

| # | read | outcome | verdict | evidence |
|---|---|---|---|---|
| 1 | bubble hovers (identity) | FWD-2 | PASS | 3 of 3 clean |
| 2-5 | shortened-label hovers at 30/90/365 | FWD-21 | PASS | 9/9, 13/13, 15/15 hovers carry the full name |
| 3 | null-tone hover | FWD-21 | PASS | Hon Hai Precision Industry (30D): "no clear tone" |
| 6 | bar hovers (identity) | FWD-2 | PASS | 3 of 3 clean (the 3 largest moves) |
| 7,10,12 | overlay "not served" census | FWD-24 | PASS | 0 on carried fields (19 carried) for each of BA, VLO and AMD |
| 14 | the census's positive control | FWD-24 | ERROR | none of the 3 names lacks a checked field; owed on a sparser name |
| 8 | timeline tooltip | FWD-5 | PASS | BA: 3 of 3 hovered bars show articles, publishers, mentions and the headline |
| 9,11,13 | every tab with the day dialog closed | FWD-27 coverage (FWD-6..11, 14, 16, 17) | PASS | 5 of 5 tabs on each of BA, VLO and AMD; dialog_open_before_tab false |
| 15 | non-USD header | FWD-4, FWD-13 | PASS | ROG SW (CHF): every money tile leads with its served currency, tabular numerals, as-of words |
| 16 | no-officer filing | FWD-7 | PASS | ASML NA: 20-F officer section empty; 7 officers served from the Bloomberg fallback roster, source named |
| 17 | Escape closes the account menu | FWD-27 | PASS | opened, then closed by Escape |
| 18-20 | display-name census | FWD-27 | FAIL | the Peers subject row prints `peers.subject.name` ("BOEING CO/THE", "VALERO ENERGY CORP", "Advanced Micro Devices, Inc."); 9 other surfaces print `display_name` |

**Totals:** 20 reads, 16 PASS, 3 FAIL, 1 ERROR.
**Follow-up:** the FAIL is repaired by round-34 cell AV-zl-1, item 5 (`round34/checks/names/peername34.cjs`).
**Still owed by the issuer:**
- the FWD-24 control on a name whose overlay lacks a field;
- the six-state ui-smoke capture (FWD-19, FWD-20; `portal/scripts/ui-smoke.mjs`).
**Upstream observation (not a DSGN defect):** 84 of the 95 covered names have no M-1 management object landed
(`management_status` ABSENT; `round34/walk/find_no_officer.py`, read-only invokes). FWD-7's DONE WHEN, a name whose filing lists no
officers, passes on ASML NA. These 84 show no officers at all.
