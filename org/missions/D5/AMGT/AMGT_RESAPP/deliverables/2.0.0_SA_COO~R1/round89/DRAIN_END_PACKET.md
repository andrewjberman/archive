# AMGT_RESAPP round 89 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~05:1xZ. Every order of the round is terminal: nn-2, nn-3, nn-4, nn-5, nn-7 complete; nn-1 and nn-8 (issuer acts)
EXERCISED and read; `AMGT-nn-6` (mm-2 to PROD) is PARKED at Andrew.** Round 89 implements the CTO~DELL1 round-88 analysis
`ledger/ROUND_ANALYSIS.round88.md` @6ad172c28d (items 1-9); decomposition s.97; issuance @16d359ecc3, amendments @68f2bbfc8b (nn-4, nn-5),
@2381761acb (nn-7 re-pin), `<to_id>` declarations @03693a4bc4 (nn-2, nn-3, nn-4). `round-close-check.py --round 89`: orders 5, complete 5,
proof_ok 5, proof_bad 0, judgment 0, verdict MAY-CLOSE (read after @03693a4bc4; before it the three short worker `to_id`s read PROOF-BAD).

## 1. Orders and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-nn-1` issuer act | 1: condition 4 against a populated watchlist | EXERCISED | `round89_prep/NN1_POPULATED_RUN_20261011.txt` @fc54cef755 |
| `AMGT-nn-2` | 3: peer identity (D1-S16) | complete, merged @a943b1b412 | worker ~351 @237699a1be, instance VALID |
| `AMGT-nn-3` | 4: subject cap vintage (D1-S15) | complete, merged @a943b1b412 | worker ~351 @ef149ef3b5, instance VALID |
| `AMGT-nn-4` | 5: audit root (S4) | complete, merged @e4b46bd517 | worker ~352 @63d9dc87b6 (fix a51ccfeed8), instance VALID |
| `AMGT-nn-5` | 6: write_pool guard (S5) | complete, merged @04ecb2d528 | worker ~353 @a173a5bc72 (guard 0e14335de2), instance VALID |
| `AMGT-nn-6` issuer act | 7: mm-2 e225e9e1 to PROD | PARKED at Andrew | call `dell1-20261011T033643Z-e7f2`; /prod-deploy is DT-only and ships 46 DEV commits (CTO msg 3446) |
| `AMGT-nn-7` | 8: ONE redeploy, peer identity + subject cap + dossier /11 | complete, APPLIED 2026-10-11T04:56:11Z | RA1 record @7cf2c2fbd4 (commit fb1d570c2d), proof instance VALID rc=0, ledger CLOSED 11/11 |
| `AMGT-nn-8` issuer read | 9: Z-W266-S3 | read, filed | `round89_prep/ISSUER_READS.md` @193ef3825c |
| item 2 (D1-S14) | peer price currency | CLOSED for round 89 on the plain reasons (CTO msg 3434 (a)) | DEMQUE request `AMGT_RESAPP-S14-CRNCY-SCANNER-US` @b6e42f51a8; round 90 replaces the reasons |

`nn-7` history, so the record reads whole: the GO @1977885433 named pin 8f2f3339c2, which carries nn-5's merge and so `crosswalk.py` (blob
3603be4be89a), a file the COO half names a STOP. RA1 stopped before any upload (msg 3490, @9547a7f911); the issuer re-pinned to a943b1b412
(@2381761acb, the issuer's error) and the CTO upheld it (ADDENDUM 1 @1f8b8f530b, option B refused). Nothing was uploaded at the first pin.

## 2. The issuer's ONE REAL RUN at close

LOCAL cells, on the MERGED tree (box/dell1 @04ecb2d528), real route handler and real neighbours (nothing written):

- **nn-2** `r89_peer_identity.py --where local`: 12 members, 10 United States, 7 resolvable under `<T> US`; PASS I1 (7 of 7 MEASURED), I2, I3;
  `R89 PEER IDENTITY: YES`.
- **nn-3** `r89_subject_cap.py --where local`: stored 541,931.78 @ 2026-09-19T07:53:19Z, served 621,657.44 @ 2026-10-10T13:01:55Z; PASS C1-C3;
  `R89 SUBJECT CAP: YES`.
- **nn-4** `r89_audit_root.sh`: PASS A1-A4; `R89 AUDIT ROOT: YES`.
- **nn-5** `r89_write_pool_guard.py`: PASS G1-G4; `R89 WRITE-POOL GUARD: YES`.
- Drain checks, once per merge: `py_compile` rc 0; ruff clean on the four changed modules; 379 tests passed (273 in the identity folder).

WORLD cell (`nn-7`), re-run by the issuer, not taken from RA1's report, against the LIVE function `opal-amgt-scoped-api` read fresh at
~05:0xZ: `CodeSha256 l8egBo/rfEH4ddCEFyWnUOb9BvN3bGu/azarul5Ho0g=`, LastModified 2026-10-11T04:56:11Z, LastUpdateStatus Successful (base
KlosR/ap8O3.., kept as the rollback, not needed).

- **AC1** in the pin worktree (`C:/tmp/nn7a-build`, HEAD a943b1b412): `scoped_amgt.py`, `listed_identity.py`, `subject_cap.py` each present in the
  deployed package (407 members) and byte-equal to the pin's (K1 and K2 PASS three times, `R88 PACKAGE: YES` three times), exit 0.
- **AC2** `r89_peers_deployed.sh`: PASS I1 (7 of 7 resolvable US members serve a MEASURED identity), I2 (leaked []), I3; `R89 PEER IDENTITY: YES`;
  served cap 621,657.438 @ 2026-10-10T13:01:55Z equals the current model block's (stored 541,931.78 @ 2026-09-19), `R89 SUBJECT CAP: YES`;
  `R89 PEERS DEPLOYED: YES`, exit 0.
- **AC3** `r89_deployed_close.sh --want amgt-corpus-dossier/11`: P1 PASS (METHOD_VERSION amgt-corpus-dossier/11), P2 PASS; W1 and W2 PASS (5 of 5
  names answered, no sentence on a FAILED description); R3 PASS (3 of 3 byte-equal to the base); `R89 DEPLOYED CLOSE: YES`, exit 0.
- RA1's record: content diff CHANGED 2, ADDED 8, off-list 0, `crosswalk.py` identical; one resource moved, re-plan rc 0.
- AMGT_CORPUS leg p post-act read (`2.0.0_SA_COO~C1` msg 3505, packet `ROUND44_AT10_LEG_P_PACKET.md` @ba35dc20a2): TSM US master_absent 0 rows,
  SAN FP own_new 115, ROG SW own_model 99, each equal to its stored /11 field; team_cases, dossier_fields and dossier_sections EQUAL; Branch A.

## 3. JUDGMENT for L9

None in the code cells (every criterion is mechanical). Two items are owed a grade by the CVO as part of this read:

1. Round 88's condition 4 moves from "met on its mechanism" to EXERCISED on `NN1_POPULATED_RUN` (populated lists, negative control fails).
2. `nn-7` is a WORLD cell; SERVED reach of nn-2 and nn-3 begins at the apply. The three checks above are the issuer's; the CVO re-runs them.

## 4. Rows filed this round (all five ruled by the issuer in the order's status line; the CVO's sweep dispositions them)

| row | class / standing | ruling | where |
|---|---|---|---|
| `AMGT_RESAPP-D1-W351-S1` | OBSERVATION / INERT | a derivation that raises on a read block is served UNREADABLE, never a 500: stands | nn-3 status |
| `AMGT_RESAPP-D1-W352-S1` | OBSERVATION / ARMED | closed by the AUDIT_ROOT `.git`-entry guard, AMENDMENT 1, checker arm A4 (base PASS, first fix FAIL, final PASS) | nn-4 status |
| `AMGT_RESAPP-D1-W353-S1` | BLOCKING / ARMED | closed by AMENDMENT 1: `test_writers_carry_issuer.py` joined `<paths>`, three patches repointed (@f97a368f0a); identity folder 273 passed 0 failed | nn-5 status |
| `AMGT_RESAPP-D1-W353-S2` | OBSERVATION / INERT | the check reads the real bucket by GET only: stands | nn-5 status |
| `AMGT_RESAPP-D1-W353-S3` | OBSERVATION / INERT | write_pool refuses any absent document over a served count; main's early guard needs a LibraryAbsentError: stands, the CTO's device-independent rule | nn-5 status |

The two ARMED rows (W352-S1, W353-S1) name `2.0.0_SA_COO~R1` as disarm owner and are disarmed by the amendments cited; no adjudication file carries
any of the five ids yet (the CVO's carrier is `surprise-channel/adjudications/`, last ADJUDICATION_v108).

## 5. For the next round

1. D1-S14 currency: the DEMQUE CRNCY request for the 1,038 US scanner rows; the 1,816 non-US rows (SEDOL stems, exchange numbers, Japanese codes,
   Canadian star-tickers) need an identifier-form decision before they can be addressed.
2. Z-W266-S3: BABA, PBR and SAP lose emitted driver points at the verifier ("no period label ... located", "value not found as a whole number");
   whether that is the locator or the excerpt is the owner's read (AMGT_FILINGS / the analyzer).
3. mm-2 to PROD (`nn-6`): Andrew's word on the 46 DEV commits.
4. `mass-deletion-check.sh`: a pre-existing neighbour, `$ROOT/.git/MERGE_HEAD` tests a path that is a FILE in a linked worktree, so the
   merge-commit exemption never fires there (named in nn-4's record face; not fixed, not in scope).
5. nn-5 is a producer-CLI change and is NOT in the served package (`crosswalk.py` is unchanged live); it reaches the function only if a later
   redeploy admits it under its own pair.
6. Process: a worker that names a short `to_id` grades PROOF-BAD at round close when the order carries no `<to_id>` tag; the cut should declare
   the tag (this round it was added after the drain, @03693a4bc4).

checked 1 of 1 issuer reads (Z-W266-S3)
