# AMGT_RESAPP round 104 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL for this seat's keys, 2026-10-14 ~01:4xZ.** Round 104 runs under several keys of one project: the workstream-less issuance (bk-1 to bk-4), workstream `LAND` (bk-6), `PROMOTE` (bk-7) and `WALK` (bk-5) are issued by this seat;
workstream `AIFILL` (fa-1 to fa-9 and its redeploy) is `2.0.0_SA_COO~R2`'s and is NOT in this packet. `round-close-check.py --round 104` reads `verdict=REFUSED` for ONE reason: `bk-5`'s AC5 is JUDGMENT and is yours.
Order of reading: section 3 first, then the walk's shot reads (section 2).

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bk-1` | the overlay prints 13 sub-phase lines; its top band reuses the feed rows | complete, merged | merged in round 104; byte-equal arms (`r104_candidate_check.py`) |
| `AMGT-bk-4` | the served fiscal P/E is price over reported EPS of the same year (same currency, or a minor unit scaled by 100) | complete, merged | worker ~415; `r104_pe_check.py` 6 of 6 arms: 464 derived (437 same-currency + 27 minor-unit), 154 withheld with a reason (126 cross-currency, 28 EPS not positive) |
| `AMGT-bk-3` | USD prints `$`; every dash tile in the header shows its reason | complete | portal candidate `3dcbb6ef` (approved by the CTO, msg 5281) |
| `AMGT-bk-6` | the bk-3 feature cut from PROD `10e7664d`, registered, merged forward | complete @2953d068a7 | worker ~417; row `dell1-20261014T001511Z-633a` CLOSED APPROVED (msg 5289); DEV `5e40e54119` |
| `AMGT-bk-7` | the promote of that one feature to PROD | complete @32790ac71f | PROD `7d5cb34d` (portal-v2.1.215), CI run 38491072873 success; the DT was stood down before writing the instance: the issuer wrote it (session_log says so; audited lane override @12a6d44915) |
| `AMGT-bk-2` | the redeploy from pin `d7a79c766a` and the first cold request | complete (RA1, @a73d234bcb) | applied 00:07:07Z, `Wkt48Y6v...`; 2 members of 15 changed; naming replay 35 requests/68 calls/16 distinct/0 differ |
| `AMGT-bk-5` | the ten-name walk on a local build of PROD `7d5cb34d` | complete; **AC5 is JUDGMENT** | worker ~418 @b0f9a8da91 merged @ce02c56d12 |

## 2. The issuer's real runs

- **bk-2 (WORLD), re-read by the issuer after RA1's reads.** RA1's first cold request `26780d80-43c1-4c36-8827-693d9e4ae6b7` (ASML_NA_Equity, alone): handler **2,910.88 ms**, Init 675.26 ms, status 200; `r104_split_table.py`
  re-run by me from the request's own log stream: `R104 SPLIT TABLE: YES`, `R103 COLD TARGET: MET (2911 ms)`. Phases (ms): feed 1,376 (feed.imports 782, feed.snapshot 593), peers 735 (peers.numeric_tickers 502,
  peers.subject_cap 102), identity 157, axis_reads 263, model_block 135; sub-phases sum to their phases (T7). ONE request: not a steady-state read. The round-103 request was 3,769.92 ms (NOT MET).
- **bk-2 served bytes, issuer's normalized /thesis compare after the apply** (`r104_thesis_normalized_compare.py`, live function against the pin at `C:/tmp/bk2-build`): 95 names, 0 failed, P/E rows 928 live and 928 post, check-face rows 464 and 464,
  21 changed paths = 18 float representation + 3 request clocks, 0 other: `R104 THESIS NORMALIZED: YES`. Before the apply the live function served 1,236 P/E rows (Bloomberg's own); now the derived 928 with 154 withheld entries carrying a reason.
  The AC2 first written for bk-2 (`r104_pe_delta.py` on capture files without the fiscal figures) was my instrument's defect; amended @36c964dab9.
- **bk-5, census (issuer, 2026-10-14):** `round104/census_v3.txt`, 95 of 95 names, 0 read failures; UNEXPLAINED 3 (`thesis.model_cases` on BABA_US, BA_US, PBR_US), the same three as round 103; STATE_ONLY 187 (`coverage.items` and `coverage.key_forms`,
  a route the page does not call); raw-code CANDIDATES 9,609 in 896 patterns (a candidate is not a verdict; the largest classes are reason strings that name a mnemonic, e.g. `the row carries no value for dy_ntm`, `.model.fiscal_unresolved[].reason` on 25 names).
- **bk-5, walk:** the draw (sha256 of 2026-10-14 over the 93): 8316 JP, NKE US, BATS LN, GOOGL US, PBR US, QXO US, COST US, 8035 JP, ISP IM, ENEL IM. Three walks (4, 4, 2 names): each ARMED then DISARMED, the post-disarm login REFUSED, `walk void: no`,
  0 guard aborts, 112 + 120 + 58 screenshots at `C:/dev/ui-walk-evidence/bk-5/{A,B,C}` (outside the repository). The worker read 30 of 30 Model, Exec Management and header shots (`deliverables/0.9.0_WK_AMGT_RESAPP~418/shot_reads.txt`);
  the issuer read two itself (GOOGL US overlay and Model, `A/20261014T005546Z/shots/085` and `093`).

## 3. WHAT THE READINGS SAY

1. **The header prints `$` and no header money prints `USD `.** On all ten names no amount carried `USD ` where a `$` belongs. Dash tiles in the header carry a reason (JP, GB, IM names; PBR US market cap, EV, net debt).
   Candidate on the same tiles: negative money prints `$-63.90B` and `$-201.80B` (the sign after the symbol).
2. **The Model tab's Key Figures table still shows dash cells with no reason on every name** (GOOGL US EBITDA margin, earnings margin, EV/EBITDA, ROE for 2026E/2027E; the same shape on the other nine). bk-3 changed the header tiles and the What-Changed panel;
   it did not touch this table. The reason exists in the served payload for P/E (`fiscal_unresolved`); the table does not render it.
3. **The 2025 P/E now follows from the table's own year, and the page does not print the year's price.** GOOGL US 2025 P/E 28.7x is FY-end price over the printed EPS 10.91; the header's $351.66 over 10.91 is 32.2x, so a reader recomputes a different figure
   (ISP IM 11.2x against 11.7x the same way). The worker filed this as a disagreement (W418-S3); the issuer reads it as a missing basis line, not a wrong figure. PBR US shows 2026E/27E P/E beside a USD price and BRL EPS with no currency note (W418-S2).
4. **Other candidates the worker read, for your own read of the shots:** Exec Management role values with colon codes (`CDIO:G`, `Pres:Jordan Brand`) and truncated words (`Intermin`, `Communicati`, `Colombia &`) on JP, IM and US names; `Executive Officer/Ciso`.
   No name read clean. None is a raw code in a Model row label (the round-103 hypothesis again not borne out).
5. **FWD-40 (a), (b), (d) are yours to grade.** (b): one cold request at 2,911 ms is under the 3,000 ms line; a steady-state window read is not in this round. (d): `bk-5` AC5. (a): the census above (UNEXPLAINED 3, unchanged) and readings 1 to 4.
   The issuer grades none of them.

## 4. Open and carried

The AIFILL workstream (~R2) is not terminal. The Terminal sign-in (Andrew), the weekend read of bh-2, and the carried items stay as in the round-103 packet. Evidence outside the repository: `C:/dev/ui-walk-evidence/bk-5/`.
