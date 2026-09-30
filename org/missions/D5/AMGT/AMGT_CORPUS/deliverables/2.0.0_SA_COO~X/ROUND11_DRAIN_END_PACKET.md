# AMGT_CORPUS -- round 11 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~09:5xZ.** Two orders issued (@`e0887a72cd`, decomposition v11.0), two complete, drained as
one chain, re-graded at the worker's tip. Both orders were amended mid-round by the issuer (s.2). The round's one served act,
the dossier rewrite at `/4`, ran under a pair the CTO first REFUSED (the SHOP carve-out) and then re-signed. The act matched
the re-signed prediction exactly.

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19; endpoint denominator -- 19.

## 1. Orders -- 2 of 2 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-m-1` | currency by intersection + the SHOP carve-out | `450f922b65` | `b274848977`, `71a6afb25b` | AC1 `11 passed`; AC2 `m1 names 95 currency_set 4 CPA_US_Equity=USD ML_FP_Equity=EUR SPOT_US_Equity=USD UNVGY_US_Equity=USD`; AC3 SHOP_CN `currency None` with the carve-out basis, CPA `USD`; proof VALID |
| `TO-CRPS-m-2` | positional read of the six blank Base cells; `/4` | `1cfd1e6737` | `b274848977` | AC1 `12 passed`; AC2 `positional names 6 placed 6 ambiguous 0 no_positions 0 sum 6`; AC3 `absent_generic 0`; AC4 `pdf_libs_loaded none`; AC5 judgment for the CVO; proof VALID; corpus suite 441 passed |

## 2. What happened in the round, as executed

1. **Surfaced at the cut:** the round-10 analysis expected "CPA, SPOT, UNVGY -> USD, and no other name moves". Its own
   intersection rule also moved SHOP_CN (`$` on a CAD listing) to CAD. The decomposition (v11.0 s.1a) built the rule literally
   and left the call to the pair.
2. **`m-2`: all six placed by x-coordinate.** In every table, the Base column's blank is the **2030E** slot in EPS, Price and
   Return. HEI's Base header centres are 323 / 361 / 399 / 437 / 475, with values at the first four and nothing at 475. The
   position alone places the blank, never arithmetic. The worker's round-10 arithmetic had predicted the same slot.
3. **`m-2` AMENDMENT 1** (@`e119939999`, row `Z-W1-S14`): the ruled `/4` bump turned two method-version tests red outside the
   grant. The issuer granted and ruled them, and row `Z-S57` disarms. This is the same class as round 10's `Z-W1-S13`. **A cutting
   lesson:** a `METHOD_VERSION` bump ruled at a cut should grant the tests that pin the old version in the same order.
4. **The CTO half REFUSED the SHOP move** (msg 26515). SHOP's pack implies ~173.5 against a CAD PX_LAST of 206.0, and Shopify reports
   in USD, so the payload cannot tell CAD from USD. The CTO amended its own ruling: a bare `$` on a non-USD dollar listing stays
   null with its own reason. **`m-1` AMENDMENT 1** (@`1916dfe591`) carried it, with AC2 tightened to the exact set and AC3 as the
   SHOP arm plus a USD control. It is built at `450f922b65` and merged at `71a6afb25b`.
5. **The pair, re-measured per name from the build path** (`checks/round11/r11_expected_moves.py`): `moved 9`, `currency_moves
   4` (BZLFY, CPA, SPOT, UNVGY -> USD) and `served_moves 6`. The COO half's ADDENDUM 1 is @`57804317d4`, and the CTO re-signed at
   @`f9446f8021`. The CTO's wider read found 6 more names whose `currency_basis` TEXT alone changes (SHOP, ORA, SAP, TTE, BP/,
   ML), for 15 names' served text in all. My instrument compared currency, served and value, not basis. The CTO's read covers the
   difference, and the instrument's blind spot is recorded here.
6. **The rewrite at `/4`**: entry `amgt-corpus-r11-dossier-rewrite` (open `49a9c7b158`, CLOSED in this commit) ran
   `names 95 written 95 existed 0` and took objects from 751 to **846**. It serves the last write 95 of 95 and reads
   `current_method_available 95 stale_pick 0`. The census `body 102 ... currency_set 5 currency_null 29` equals ADDENDUM 1, and the
   move diff re-run afterwards reads **`moved 0`**.

## 3. The one real run (`evidence/r11_real_run.txt`, on the served table after the rewrite)

- SHOP_CN_Equity base: `currency None`, "a bare $ on a non-USD dollar listing: the pack may state the reporting currency".
- CPA_US_Equity base: `currency USD`, "symbol's ISO set and the listing agree on exactly one code".
- HEI_US_Equity base EPS: `6.03, 6.80, 7.73, 8.99, null` (2030E blank, placed by position).

## 4. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-W1-S14` | ARMED -> disarmed by `Z-S57` | CLOSE |
| `Z-S57` | INERT | the disarm carrier |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **`m-2` AC5** -- *is every placed value in the column the pdf page shows it in, and is every unplaced name still honestly
  ABSENT?* All six were placed, so the artifact is the six served tables (846 objects; `read_dossier` on 8035_JP, BZLFY_US,
  HEI_US, SNPS_US, TSM_US, V_US) against their bronze pdf page 0.

## 6. Enrichment candidates for the round-11 analysis

1. **The move-diff instrument omits `currency_basis`** (s.2 item 5). If kept, it should compare every served case key, not a
   chosen subset.
2. **A `null` year inside a served case is new to AMGT_RESAPP's reader.** It was named in both halves and belongs to their
   render.
3. None blocking.

## 7. Bounds and residue

- No vendor or gateway call. Served-plane writes this round: 95 dossier objects; no delete. The positional read opened six bronze
  pdfs read-only.
- Worktrees `/c/tmp/wk-crps11-1` and older hold only workers' untracked scratch; removal is a forced delete on the operator's word.

-- `2.0.0_SA_COO~X`
