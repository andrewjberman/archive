# AMGT_RESAPP round 89 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: DRAFT, 2026-10-11 ~04:1xZ. nn-1, nn-8 (issuer acts), nn-2, nn-3, nn-4, nn-5 complete and MERGED (box/dell1 @04ecb2d528, LOCAL).
`AMGT-nn-7` (the one redeploy) is STAGED; `AMGT-nn-6` (mm-2 to PROD) is PARKED at Andrew.** Nothing below is a verdict. Round 89 implements the
CTO~DELL1 round-88 analysis `ledger/ROUND_ANALYSIS.round88.md` @6ad172c28d (items 1-9); decomposition s.97; issuance @16d359ecc3, amendments
@68f2bbfc8b (nn-4, nn-5).

## 1. Orders and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-nn-1` issuer act | 1: condition 4 against a populated watchlist | EXERCISED | `round89_prep/NN1_POPULATED_RUN_20261011.txt` @fc54cef755 |
| `AMGT-nn-2` | 3: peer identity (D1-S16) | complete, merged @a943b1b412 | worker ~351 @237699a1be, instance VALID |
| `AMGT-nn-3` | 4: subject cap vintage (D1-S15) | complete, merged @a943b1b412 | worker ~351 @ef149ef3b5, instance VALID |
| `AMGT-nn-4` | 5: audit root (S4) | complete, merged @e4b46bd517 | worker ~352 @63d9dc87b6 (fix a51ccfeed8), instance VALID |
| `AMGT-nn-5` | 6: write_pool guard (S5) | complete, merged @04ecb2d528 | worker ~353 @a173a5bc72 (guard 0e14335de2), instance VALID |
| `AMGT-nn-6` issuer act | 7: mm-2 e225e9e1 to PROD | PARKED at Andrew | call `dell1-20261011T033643Z-e7f2`; /prod-deploy is DT-only and ships 46 DEV commits (CTO msg 3446) |
| `AMGT-nn-7` | 8: ONE redeploy, peer identity + subject cap + dossier /11 | STAGED | order + COO half @16d359ecc3; waits the CTO half and AMGT_CORPUS's pin ask |
| `AMGT-nn-8` issuer read | 9: Z-W266-S3 | read, filed | `round89_prep/ISSUER_READS.md` @193ef3825c |
| item 2 (D1-S14) | peer price currency | CLOSED for round 89 on the plain reasons (CTO msg 3434 (a)) | DEMQUE request `AMGT_RESAPP-S14-CRNCY-SCANNER-US` @b6e42f51a8; round 90 replaces the reasons |

## 2. The issuer's ONE REAL RUN at close

LOCAL cells: run on the MERGED tree (box/dell1 @04ecb2d528), the real route handler and the real neighbours (the live crosswalk, the live
model-block pool and the live peers object; nothing written):

- **nn-2** `r89_peer_identity.py --where local`: 12 members, 10 United States, 7 resolvable under `<T> US`; PASS I1 (7 of 7 served MEASURED
  with the crosswalk's own key), I2 (no member outside the pool's holdings), I3 (nothing removed or reordered); `R89 PEER IDENTITY: YES`.
- **nn-3** `r89_subject_cap.py --where local`: stored 541,931.78 @ 2026-09-19T07:53:19Z, served 621,657.44 @ 2026-10-10T13:01:55Z (the
  subject's current block); PASS C1-C3; `R89 SUBJECT CAP: YES`.
- **nn-4** `r89_audit_root.sh`: PASS A1-A4 (a linked worktree's row survives the worktree's removal; block mode exit 1 and a BLOCKED row;
  the main-worktree control; a submodule row never under `.git/modules`); `R89 AUDIT ROOT: YES`.
- **nn-5** `r89_write_pool_guard.py`: PASS G1-G4 (door A and door B refused with no put and the served object unchanged; the control and the
  union write land); `R89 WRITE-POOL GUARD: YES`.
- Drain checks, once per merge: `py_compile` rc 0; ruff clean on the four changed modules; 379 tests passed (peers, numeric tickers,
  currency, the two new api files, the identity folder: 273 with the new guard file).

WORLD cell (`nn-7`): PENDING. SERVED reach of nn-2 and nn-3 begins only when nn-7 lands; until then the live function still reads KlosR/ap8O.

## 3. JUDGMENT for L9

None in the code cells (every criterion is mechanical). Round 88's condition 4 moves from "met on its mechanism" to EXERCISED on `NN1_POPULATED_RUN`
(its CVO grade is owed as part of the L9 read of this packet).

## 4. Rows filed this round

`AMGT_RESAPP-D1-W351-S1` (a derivation that raises on a read block is served UNREADABLE, never a 500: ruled, stands); `D1-W352-S1` (a submodule's
common dir: closed by the AUDIT_ROOT `.git`-entry guard, AMENDMENT 1); `D1-W353-S1` (BLOCKING, three out-of-path test patches: closed by
AMENDMENT 1), `D1-W353-S2` (the check reads the real bucket by GET only: stands), `D1-W353-S3` (write_pool refuses any absent document over a
served count; main's early guard needs a LibraryAbsentError: stands, the CTO's device-independent rule).

## 5. For the next round

1. D1-S14 currency: the DEMQUE CRNCY request for the 1,038 US scanner rows; the 1,816 non-US rows (SEDOL stems, exchange numbers, Japanese codes,
   Canadian star-tickers) need an identifier-form decision before they can be addressed.
2. Z-W266-S3: BABA, PBR and SAP lose emitted driver points at the verifier ("no period label ... located", "value not found as a whole number");
   whether that is the locator or the excerpt is the owner's read (AMGT_FILINGS / the analyzer).
3. mm-2 to PROD: Andrew's word on the 46 DEV commits.
4. `mass-deletion-check.sh`: a pre-existing neighbour, `$ROOT/.git/MERGE_HEAD` tests a path that is a FILE in a linked worktree, so the
   merge-commit exemption never fires there (named in nn-4's record face; not fixed, not in scope).

checked 1 of 1 issuer reads (Z-W266-S3)
