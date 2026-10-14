# AMGT_RESAPP round 105 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL for this seat's keys, 2026-10-14 ~04:5xZ.** Round 105 is the CTO's round-104 enrichment list (`ledger/ROUND_ANALYSIS.round104.md`, msg 5350), issued at `34bc28182d` under this seat's keys (workstream-less `bl-1`, workstream `PROMOTE` `bl-2`, workstream `WALK` `bl-3`).
`~R2`'s AIFILL workstream is NOT in this packet (it is compiled in its own). `round-close-check.py --round 105` is expected to read REFUSED on one item only: `bl-3` AC5, which is JUDGMENT and yours. Read section 3 first.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bl-1` | one Opal-internal portal feature: a money symbol prints only for the figure's own currency (PBR US's BRL team figures print `BRL `, no `$`); a segment-table column with no figure is dropped with one visible sentence (BATS LN `Period 4`); a Key Figures `--` cell shows its reason | complete @25177c42e8 | worker ~419 (two passes: the first stopped on a BLOCKING row because MY order named the Model tab for item 2; amended @60c451ff6d to the Thesis tab's segment table); portal `051ad362d4` (8 files under `src/pages/SecurityAnalysis/`, harness 10 of 10, feature green regressions 0, surface YES); row `dell1-20261014T031653Z-f1a4` CLOSED APPROVED (CTO) |
| `AMGT-bl-2` | the promote of that one feature to PROD | complete @9e875c1afc | `0.4.0_DT_ClientPlatform`; PROD `7d5cb34d` -> `0910f4ad` (portal-v2.1.216), CI run 38506401223 success; the DT wrote its instance (VALID); issuer re-read: 8 of 8 blobs EQUAL on origin/PROD, 8 files changed |
| `AMGT-bl-3` | the 93-name census (issuer) and the ten-name walk on a local build of PROD | complete; **AC5 is JUDGMENT** | worker ~440 @3a2a36398a merged @e8d8b5286c; the build is PROD `7db035e4` (`0910f4ad` plus `~R2`'s AI-fill feature, portal-v2.1.217: the CTO named this head, msg 5405) |

## 2. The issuer's real runs

- **Census, re-run by the issuer on the live function (`round105/census_v4.txt`, committed @58b0ba8dce):** 95 of 95 names, 0 read failures; UNEXPLAINED 3 (`thesis.model_cases` on BABA_US, BA_US, PBR_US) and STATE_ONLY 187, both exactly as in `round104/census_v3.txt`; raw-code CANDIDATES 9,614 in 899 patterns (9,609 in 896): a candidate is not a verdict. The served block did not change in round 105.
- **Walk:** the draw is the same as round 104's (same walk date 2026-10-14, the same 93): 8316 JP, NKE US, BATS LN, GOOGL US, PBR US, QXO US, COST US, 8035 JP, ISP IM, ENEL IM, so the two confirmed values are read on the same pages. Three walks (4, 4, 2 names) on PROD `7db035e4`: each ARMED then DISARMED, the post-disarm login REFUSED, `walk void: no`, 0 guard aborts;
  112 + 120 + 58 screenshots at `C:/dev/ui-walk-evidence/bl-3/{A,B,C}` (outside the repository); the walker account reads dormant after. The worker's reads are in `deliverables/0.9.0_WK_AMGT_RESAPP~440/SESSION_LOG.txt`. The issuer read PBR US's Model shot itself (`B/20261014T041917Z/shots/015-PBR-US-Model.png`).
  Two seats were spent on the walk's process, not its content: the first walk was void because Git Bash rewrote `--route /security-analysis` (the criteria now carry `MSYS_NO_PATHCONV=1`), and one walk met a held walker lease (another seat's walk on this box).

## 3. WHAT THE READINGS SAY

1. **The two confirmed values of round 104 read fixed on PROD.** PBR US Model tab: `Figures in BRL`, `EPS (per share, BRL)`, `EBITDA (millions, BRL)`, no `$` anywhere in the table; the header's price `$25.30` is the USD quote. BATS LN Thesis tab: the segment tables show Fiscal year 2025, 2024, 2023, 2021 with no `Period 4` header, and the sentence under the operating-income table reads `Period 4 is not shown: No top-level row carries a figure in this column.`
2. **Key Figures dashes carry reasons on the names read for it.** PBR US (issuer): `No consensus estimate is served for this line`, `Bloomberg reports no history for this line`. Worker: every `--` reasoned on 8316 JP, NKE US, QXO US (2025 P/E), COST US (2026 P/E, fiscal-year-end reason), 8035 JP, ISP IM, ENEL IM. Not stated by the worker for BATS LN and GOOGL US (first-pass reads): read their Model shots. The All-figures grid's team rows still carry dashes with no reason (row `W419-S3`, outside the CTO's item 3).
3. **The AI-fill blocks render and break nothing on these ten.** A `MACHINE-WRITTEN` chip on the Exec Management block of every name; on the Thesis pillars of 8316 JP, BATS LN, GOOGL US, QXO US, COST US and ISP IM; no Thesis chip on NKE US and 8035 JP, not stated for PBR US, not legible on ENEL IM at page scale. No other section broke or went blank. (`~R2`'s FWD-41 grade is theirs.)
4. **Candidates the readings raise, for your own read of the shots (none is a confirmed broken value on my read):**
   - negative money prints the sign after the symbol: `$-63.90B` (GOOGL US net debt), `$-10.19B` (COST US), `$-234.92M` (QXO US, What Changed);
   - the 2025 P/E is the fiscal year's own price over EPS and the page does not print that price: GOOGL US 28.7x against 32.2x from the header price; ISP IM likewise; PBR US's forward 5.2x sits beside a USD price and BRL EPS with the ratio's currency basis unprinted;
   - Exec Management text: colon-coded roles (`Mgr:International...`, `Co-Head:Investor Relations`), truncated words (`Sustainabil`, `Colombia &`), run-together tokens (`led:operating`, `bydisposals`, `2016.Became`), and the sentence `no management section in the research team's pack missing or earnings update 2026-Q2` on BATS LN and QXO US (a served reason string with `missing`);
   - one API issue in walk C: the login step's GET of `/api/general/json-tiered/market-overview/summary/all-returns.json` returned HTTP 500 (outside the Security Analysis page).
5. **FWD-40 (a) and (d) are yours to grade.** The issuer grades none of them. (b) was graded MET in round 104 and nothing in round 105 touched the function.

## 4. Open and carried

`~R2`'s AIFILL workstream; the Terminal sign-in (Andrew); the weekend read of bh-2. Evidence outside the repository: `C:/dev/ui-walk-evidence/bl-3/`. Left on disk: `C:/dev/wk-resapp-418` and its leftovers (a recursive delete is Andrew-class, not done).
