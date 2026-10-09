# AMGT_RESAPP round 79 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`

**STATE: FINAL for the eight orders, 2026-10-09T00:01:23Z. One issuer act of two was NOT run (section 3, act 2).** Nothing below is a verdict.

Round 79 implements the CTO's round-78 analysis (`ledger/ROUND_ANALYSIS.round78.md` @1a67e26433) with CTO msgs 31672 and 31623.
Decomposition s.87. **8 of 8 order files are terminal** (issuance @5d126e533e). `round-close-check.py --round 79` reads
verdict=MAY-CLOSE. Its order line reads 0 complete of 8, with all 8 status fields printed blank; the last `<status>` tag of every
order file reads complete. The tool's status read was not traced here.
cc-7 redeployed `opal-amgt-scoped-api` at the build pin `63f0605039`: grant first, then code `ltXvElw` (applied 17:35:08Z), then the
/freshness snapshot (VersionId `ar7KPWgP`, 18:08Z). Its pair: COO half `round79/NEVER_WIDEN_HALF_COO_CC7.md`, CTO half (msg 31782);
the ledger is CLOSED @42700562a4.

## 1. Orders (each line is the order's own last status, written by the issuer at its drain)

- **`AMGT-cc-1`** (`AMGT_RESAPP.TO-AMGT-cc-1.the-segment-reader-finds-a-stored-table.md`): complete -- drained @0433c23f27; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; AMD read from 2 bodies; served only after the adapter cell cc-6
- **`AMGT-cc-2`** (`AMGT_RESAPP.TO-AMGT-cc-2.one-served-segment-table-with-its-labels.md`): complete -- drained @bdd1a55638; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; 85 of 85 stored names served, 72 labelled, 4 not; row Z-W309-S1 (the stale-hash test) answered by cc-5; served only after cc-6
- **`AMGT-cc-3`** (`AMGT_RESAPP.TO-AMGT-cc-3.the-seeking-alpha-store-reader.md`): complete -- drained @beee52785a; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; 95 of 95 covered, read 12, checked 13, no record 70 at the run; served only after cc-6 and the grant
- **`AMGT-cc-4`** (`AMGT_RESAPP.TO-AMGT-cc-4.five-stored-sections-served.md`): complete -- drained @f6b844fadd; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; counts 48, 18, 13, 13, 13 equal the cut; served only after cc-6
- **`AMGT-cc-5`** (`AMGT_RESAPP.TO-AMGT-cc-5.the-build-side-repairs.md`): complete -- drained @646167b6df; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; the build's gate exits 0; 4 of 4 old prefix values equal; the list reads 34 entries; nothing applied: the grant is cc-7's leg
- **`AMGT-cc-6`** (`AMGT_RESAPP.TO-AMGT-cc-6.the-adapter-cell.md`): complete -- drained @63f0605039; proof VALID rc=0 on the worker's checker; AC1 (12 of 12 clauses), AC2 and AC3 (916 passed) re-run by the issuer on the shared tree read SERVED: YES; AMENDMENT 1 landed (top_band.py:36 reads 'the analysis built for this name'); served on the live function only after cc-7
- **`AMGT-cc-7`** (`AMGT_RESAPP.TO-AMGT-cc-7.the-code-redeploy.md`): complete -- landed @42700562a4 by 0.7.0_AE_CloudOps~A (msg 31985): four legs, grant 33->34, code ltXvElw = the kept zip, snapshot ar7KPWgP 18:08Z; proof VALID; ledger CLOSED. Re-run by the issuer on the shared tree 2026-10-08T21:2xZ: AC1 R79 DEPLOYED YES 1 of 1; AC3 R78 DEPLOYED YES 3 of 3 and R77 SERVED SHAPE YES; AC2 c62 YES, c63 YES, c59 C2 and C3 PASS, C1 301 of 302 at 3.2 h after the event: the one row NG/_LN differs only by a Seeking Alpha record written 20:41Z, newer than the snapshot's generated_at 18:08Z -- the class the order names as NOT a rollback trigger; the seat's run within minutes of the event read 302 of 302. Graded YES by the issuer
- **`AMGT-cc-8`** (`AMGT_RESAPP.TO-AMGT-cc-8.the-walk-on-dev.md`): complete -- drained @5f48eb9d55 (walk f9fb9d7faf, proof 3e63fa6c88 VALID rc=0); re-run by the issuer on the shared tree: AC1 R79 CC8 WALK RECORD YES (29 of 8 captures, 4 of 4 acts named), AC2 the walker armed=no armedBy none; AC3 is the CVO's L9 read. The walk on portal 38cc0ecf: FWD-18 ASML NA draws the refusal sentence the API serves, the thesis figure is not a control (row Z-W314-S3); BA passage rendered once; FWD-1 AMD page draws a reason where the API serves a 6-row segment_table; FWD-7 page draws 0 of 10 served sentences (date or 'Not collected' only); SECTIONS page draws 0 of 5 on ASML NA and NU while the API serves 5 and 3. Rows S1/S2 disarmed by Z-S376

## 2. The issuer's ONE REAL RUN at close

`deliverables/2.0.0_SA_COO~Z/round79/ONE_REAL_RUN_20261008.txt` was run by this seat from 2026-10-08T22:54:16Z to 22:55:56Z.
It ran on the live function `ltXvElwZ4iyRx6bJLDQRWksbDoiTesc8xvu1h+p3QI0=` (LastModified 17:35:08Z). The hash was read before
and after the run, and both reads were equal.
- `r79_deployed.py`: **R79 DEPLOYED: YES 1 of 1**, exit 0. The one listed line is `r79_cc6.py --crit AC1 --where deployed`,
  the three hookups of the adapter cell on the live function.
- `r78_deployed.py`: **R78 DEPLOYED: YES 3 of 3**, exit 0 (no regression).
- `r77_served_shape.py --where deployed`: **R77 SERVED SHAPE: YES**, exit 0.

cc-7's AC2 was re-run by this seat at about 21:2xZ, after the seat's own run:
- c62 YES and c63 YES.
- c59 C2 PASS (2 cold of 40, inside the 2000 ms bar) and C3 PASS (222 ms after idle).
- c59 C1 read 301 of 302, about 3.2 h after the snapshot event. The one row, `NG/_LN_Equity`, differs only by a Seeking
  Alpha record written at 20:41:32Z, after the snapshot's `generated_at` of 18:08Z. The order names that class as NOT a
  rollback trigger, and the seat's own run, within minutes of the event, read 302 of 302.

The walk (cc-8) looked at the page; the issuer did not (section 4).

**Not exercised by any real run this round, stated so it is not assumed:**
- **The page side of everything served this round.** Portal DEV `38cc0ecf` does not carry DSGN_AMGTV1's SAUX-41 and SAUX-42:
  0 hits for `seeking_alpha` or `dossier_sections` in the portal's `src` at that ref.
  - The served Seeking Alpha sentences, the AMD segment table and the five sections are graded on the API side only.
  - FWD-7 is graded only after DSGN's cell draws the served sentence (CTO msg 31672, term three).
- **The gateway:** every deployed check is a direct invoke. The walk is the only read through the edge.

## 3. The issuer acts (decomposition s.87b: no order file)

| act | state | record |
|---|---|---|
| 1. Z-S369's disarm (R4) | DONE as R4 allows without Andrew's word. The read is printed (`round79/reads/Z_S369_ICT_POOL_READ.md` @e9d194ebf0). The row is marked UNRESOLVED with its reason by the citing row Z-S377. The one Bloomberg identity read that decides one key or two is Andrew's word, and that word was not given. | Z-S377 |
| 2. ABNB's model-block pull (carried from round 78) | **NOT RUN.** It is a Bloomberg call under its own pair, on Andrew's per-use word. No pair was drafted and no word is on record. Carried again. | -- |

## 4. JUDGMENT for L9 (yours)

**cc-8 AC3, the walk on DEV.** Portal `38cc0ecf`, function `ltXvElw`, role admin. Record:
`deliverables/0.9.0_WK_AMGT_RESAPP~314/WALK_ROUND79.md`, 29 captures. The recorded pass is `20261008T221220Z`, the third of three
passes. The first GO came back BLOCKED (rows S1 and S2) and was re-GO'd at 21:51:49Z.

The worker's observations, no verdict:
- **FWD-18, ASML NA:** the chart's place draws the sentence the API serves ("The filing text kept here counts the company's own
  shares or describes its share capital, so no driver chart is shown."). `thesis_driver_chart` is ABSENT and refused, 0 points.
  - No figure in the thesis text is a control. A press on "51,095.11 shares" changed nothing (row Z-W314-S3).
  - The card press opens the passage P0064 (20-F filed 2026-02-25, Item 3.D Risk Factors, paragraph 65), with P0065 beside it.
- **FWD-18, BA:** the chart is drawn, y ticks 0 to 600. One press rendered the passage ONCE (a table, Item 7 / Table 2025).
- **FWD-1, AMD:** the page draws a reason ("No filing analysis is stored for this name yet, so no segment breakdown is shown...").
  The API serves `segment_table`: status served, 6 rows, the first "Data Center" with value 16635, period "Fiscal year 2025",
  USD millions.
- **FWD-7:** 95 rows. First paint 2,093 ms, then 1,618 ms. 1 row is stale (Lenovo 992 HK, last read 2026-09-22), and the API
  agrees.
  - Of the ten rows read, the page draws 0 of 10 served sentences: only a date or "Not collected". It shows "Not collected" for
    both `no_record` and `checked`.
  - API states over all 95 rows: read 13, checked 15, no_record 67.
- **SECTIONS:** the page draws none of the five on ASML NA or NU. The API serves 5 on ASML NA. On NU it serves 3, with
  `company_description` and `special_items` absent, each with a reason.

## 5. Rows filed this round (round 79)

| row | by | standing | one line |
|---|---|---|---|
| `AMGT_RESAPP-Z-S373` | `3.0.0_SA_CVO~Z` | INERT | AMD US says both "research pack ... Worked" and "no research pack for this security" on one screen |
| `AMGT_RESAPP-Z-W309-S1` | worker ~309 | INERT | the stale registry-hash test; answered by cc-5 |
| `AMGT_RESAPP-Z-S374` | `0.7.0_AE_CloudOps~A` | INERT | comp-lambdamap parity is blind to this function: the source-map entry has no commit or artifact hash |
| `AMGT_RESAPP-Z-S375` | `0.7.0_AE_CloudOps~A` | INERT | the GO carried call 11 as a file list; one merge window falsified the list while the term stayed true |
| `AMGT_RESAPP-Z-W314-S1`, `-S2` | worker ~314 | ARMED at filing; disarmed by Z-S376 | the walker account and port 5174 were held by another seat's walk at the first GO |
| `AMGT_RESAPP-Z-W314-S3` | worker ~314 | INERT | ASML NA: no thesis figure is a control; the passage opens on the card press |
| `AMGT_RESAPP-Z-S376` | this seat | INERT | S1 and S2's disarm. The class stands: one walker account and one port 5174 for every seat on site Z, with no lease |
| `AMGT_RESAPP-Z-S377` | this seat | INERT | Z-S369 stays unresolved: one key or two needs the identity read, which is Andrew's word |

## 6. For the next round (carried; cited, not cut here)

Andrew-direct ~22:5xZ (CTO msg 32099, record @b7361ceb2a): AMGT_RESAPP moves to DELL1 after this round. No new round is
started here. The carried items:
1. **The page side of round 79** is DSGN_AMGTV1's: SAUX-41 (the three Seeking Alpha states with their sentences) and
   SAUX-42 (the five sections). The segment table on AMD. FWD-7 is graded after that cell lands.
2. **ABNB's model-block pull** (issuer act 2, now carried twice).
3. **Z-S369's identity read** (Andrew's word).
4. **The walker and port contention** (Z-S376): three seats held them within an hour on site Z.
5. **The build's duty:** the kept zip `C:/tmp/cc7-r79-63f0605039.zip` is the next build's `AMGT_DEPLOYED_ZIP`. It is a site-Z
   path, so the move to DELL1 must carry it or rebuild it.
