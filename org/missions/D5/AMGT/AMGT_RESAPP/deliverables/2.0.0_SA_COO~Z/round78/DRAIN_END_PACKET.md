# AMGT_RESAPP round 78 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`

**STATE: FINAL for the nineteen orders, 2026-10-08T09:15:21Z. One issuer act of three was NOT run (section 3, act 2).** Nothing below is a verdict.

Round 78 implements the CTO's round-77 analysis (`ledger/ROUND_ANALYSIS.round77.md` @a1e519f9eb with ADDENDUM 1 @6d7cd1fe3c) and
the rulings at the cut (@f97be3fd6f). Decomposition s.86 with ADDENDUM 1 (86e: cell bb-23, carried as LEG 0 of the bb-18 order).
**19 of 19 order files are terminal** (issuance @3161dbc59a). The function `opal-amgt-scoped-api` was redeployed by bb-18 at the
build pin `fbb643923e` and reads `+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=` (applied 2026-10-08T07:19:32Z; this seat's
own read, equal to the kept zip's hash). Its never-widen pair: COO half `round78/NEVER_WIDEN_HALF_COO_BB18.md` with two addenda
(@e78b0d506e); CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_RESAPP_R78_BB18_REDEPLOY_20261007.md` with two
addenda (@72afea4d2e). Seven files of other projects rode that artifact; they are listed in the COO half.

## 1. Orders (each line is the order's own last status, written by the issuer at its drain)

- **`AMGT-bb-1`** (`AMGT_RESAPP.TO-AMGT-bb-1.the-segments-reader.md`): complete -- drained @52daa06f53; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES after AMENDMENT 1; built, NOT served this round
- **`AMGT-bb-2`** (`AMGT_RESAPP.TO-AMGT-bb-2.one-statement-of-inputs.md`): complete -- drained @025cab3f95; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; served only after the adapter cell bb-17
- **`AMGT-bb-3`** (`AMGT_RESAPP.TO-AMGT-bb-3.the-officer-rank.md`): complete -- drained @357436b20d; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; served only after the adapter cell bb-17
- **`AMGT-bb-4`** (`AMGT_RESAPP.TO-AMGT-bb-4.the-slash-safe-officers-reader.md`): complete -- drained @70d0d07c5f; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; served at the next redeploy
- **`AMGT-bb-7`** (`AMGT_RESAPP.TO-AMGT-bb-7.the-pool-carries-each-legal-name.md`): complete -- drained @5b498e903a; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; the legal names are served only after the issuer's pool mint
- **`AMGT-bb-8`** (`AMGT_RESAPP.TO-AMGT-bb-8.peer-price-with-its-own-listing-currency.md`): complete -- drained @ebcb0a4d26; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; served only after the adapter cell bb-17
- **`AMGT-bb-9`** (`AMGT_RESAPP.TO-AMGT-bb-9.the-country-in-plain-case.md`): complete -- drained @7c1cd7c32b; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; served only after the adapter cell bb-17
- **`AMGT-bb-10`** (`AMGT_RESAPP.TO-AMGT-bb-10.one-marker-for-a-name-outside-coverage.md`): complete -- drained @60a87724eb; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads SERVED: YES; served only after the adapter cell bb-17
- **`AMGT-bb-11`** (`AMGT_RESAPP.TO-AMGT-bb-11.a-plain-served-news-source-name.md`): complete -- drained @580080832e; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; served only after the adapter cell bb-17
- **`AMGT-bb-13`** (`AMGT_RESAPP.TO-AMGT-bb-13.peers-v-below-three-peers.md`): complete -- drained @1423b8974b; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; the new sentence is stored only at the next scores run
- **`AMGT-bb-14`** (`AMGT_RESAPP.TO-AMGT-bb-14.the-pull-driver-names-a-missing-library.md`): complete -- drained @905d541a83; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; AC3 by the amended check
- **`AMGT-bb-15`** (`AMGT_RESAPP.TO-AMGT-bb-15.the-rot-signal-gets-a-home.md`): complete -- drained @b68f3c888b; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; the data file must be in the redeploy's closure (issuer reads it at the bb-18 pair) -- CORRECTION by the issuer (2026-10-07): the note above that the data file must be in the redeploy's closure was the issuer's assumption and is wrong; measured for the bb-18 pair, rot_signal.json is not packaged and no served route opens it (/freshness computes the register in memory); nothing else of the status changes
- **`AMGT-bb-16`** (`AMGT_RESAPP.TO-AMGT-bb-16.the-seeking-alpha-collector-record-reader.md`): complete -- drained @e033632835; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; built, NOT served this round
- **`AMGT-bb-17`** (`AMGT_RESAPP.TO-AMGT-bb-17.the-adapter-cell.md`): complete -- drained @5909213803; proof VALID rc=0 on the worker's checker; AC1 H1-H6 and AC2 re-run by the issuer on the shared tree read exit 0 and SERVED: YES after AMENDMENT 1 to the check (H5 read the provenance's shape wrongly, row Z-W302-S1); ISSUER RULING on row Z-W302-S2: the overlay's input_provenance is left unchanged this round, because the statement there would need the whole thesis read on first paint or else serve a false filings row; the ONE statement is /thesis's; served at bb-18
- **`AMGT-bb-18`** (`AMGT_RESAPP.TO-AMGT-bb-18.the-code-redeploy.md`): complete -- legs 0, 1 and 2 landed by 0.7.0_AE_CloudOps~A; applied 2026-10-08T07:19:32Z at the pin fbb643923e; live CodeSha256 +s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ= (base MkM9Kf37), equal to the kept zip C:/tmp/bb18-r78-fbb643923e.zip by the issuer's own hash; CONTENT-DIFF CHANGED 22 / ADDED 8 / REMOVED 0; AC1 R78 DEPLOYED: YES 3 of 3, AC2 r76 c62 and c63 and r75 c59 YES, AC3 R77 SERVED SHAPE: YES, AC4-AC6 YES at LEG 0; proof VALID rc=0 re-run by the issuer; NEVER-2 amgt-resapp-r78-bb18 CLOSED 6 of 6; the issuer's four hand reads @92cfe7bd29 (C4 branch (a)); executor's report org/tier2_senior/0.7.0_AE_CloudOps~A/logs/2026-10-08/round78_bb18_legs1_2_code_redeploy.md; both zips kept
- **`AMGT-bb-19`** (`AMGT_RESAPP.TO-AMGT-bb-19.the-walk-on-dev.md`): complete -- drained @d508b0d687 (worker HEAD a557d5ba61); proof VALID rc=0 on the worker's checker; AC1 (23 captures of a floor of 8, six act tokens named) and AC2 (the walker reads disarmed) re-run by the issuer on the shared tree, exit 0; port 5174 reads 0 listeners; AC3 is the CVO's L9 read of deliverables/0.9.0_WK_AMGT_RESAPP~303/WALK_ROUND78.md; the walk's findings (two statements of inputs that disagree, the coverage sentence served and not drawn, BP/ LN officers drawn CFO first) are page findings for DSGN_AMGTV1, rows Z-W303-S1 and Z-S372
- **`AMGT-bb-20`** (`AMGT_RESAPP.TO-AMGT-bb-20.nine-files-recommitted-with-lf-endings.md`): complete -- drained @ba80b22747; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; AC3 by the amended check; 9 of 45 landed, row Z-S362 stays open
- **`AMGT-bb-21`** (`AMGT_RESAPP.TO-AMGT-bb-21.segment-periods-labelled-where-they-tie.md`): complete -- drained @be6b1ad6f7; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; built, NOT served this round
- **`AMGT-bb-22`** (`AMGT_RESAPP.TO-AMGT-bb-22.divergence-reads-the-served-dispersion-fields.md`): complete -- drained @7ae6a03fda; proof VALID rc=0 on the worker's checker; every criterion re-run by the issuer on the shared tree reads exit 0 and SERVED: YES; D stays ABSENT until the fields land

## 2. The issuer's ONE REAL RUN at close

`deliverables/2.0.0_SA_COO~Z/round78/ONE_REAL_RUN_20261008.txt`, on the live function `+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=`,
2026-10-08 09:02Z to 09:04Z, by this seat (the hash read before and after, equal):
- `r78_deployed.py`: **R78 DEPLOYED: YES 3 of 3**, exit 0. Line 1 (`r78_bb17.py --crit AC1 --where deployed`) grades the six
  hookups; lines 2 and 3 (`r78_bb5.py`, `r78_bb6.py`) read all 95 `/thesis` bodies.
- `r77_served_shape.py --where deployed`: **R77 SERVED SHAPE: YES**, exit 0.

And four reads by hand, `round78/reads/BB18_ISSUER_HAND_READS_20261008.txt` (@92cfe7bd29), direct GET-shaped invokes:
- a 2009 as-of date on the rankings route answers 200 with a plain reason; the 90-day branch, the one that reaches the unguarded
  staleness call site, does not read the request's as-of at all (CTO half C4: branch (a), no blocking row);
- `/thesis` for `BP/_LN_Equity` serves 10 officers and for `NG/_LN_Equity` 9, each led by its chief executive, then its chief
  financial officer (bb-4 and bb-3 on the live function);
- `/resolve?q=apple` lists `AAPL_US_Equity` ("Apple Inc") and `?q=microsoft` lists `MSFT_US_Equity` ("Microsoft Corp") (bb-7 after
  the pool mint); `?q=Lenovo` still lists `992_HK_Equity`.

The page was looked at by the walk (bb-19), not by the issuer: section 4.

**Not exercised by any real run this round, stated so it is not assumed:**
- bb-1, bb-21 and bb-16 are BUILT and NOT SERVED by ruling: no route reads them. bb-16's module is not in the package at all.
- bb-13's sentence and bb-22's fields change nothing served until a scores run; `run_scores` was not re-run (rulings file).
- bb-14 (the driver's stop word) and bb-15 (the rot signal's home) are hand-run tools; their checks ran on fakes and on the tree.
- bb-20 changed line endings of 9 files and applied nothing.
- The gateway: every deployed check is a direct invoke. The walk is the only read through the edge.

## 3. The issuer acts (decomposition s.86b: no order file)

| act | state | record |
|---|---|---|
| 1. the pool mint that carries the legal names | DONE 2026-10-07T17:18:17Z under its pair (COO @f147438d17, CTO @7bf7784e12); VersionId `XledA4XthVEOE3snOolYp7lkbarhPNkx`, 243 records, 211 named; read-back branch A | `round78/POOL_MINT_LEGAL_NAMES_ACT_RECORD_20261007.md` @e7e9b3e638 |
| 2. ABNB's model-block pull (ruling 7) | **NOT RUN.** No pair was drafted: the round's hours went to the redeploy's package route. It is a Bloomberg call under its own pair. The issuer carries it to round 79 and says so to the CTO in the slug; nothing of this round's nineteen orders depends on it | -- |
| 3. the ARMED rows read one by one; the wrong peer currencies | DONE: 13 rows read, 0 a live hazard today (`round78/ARMED_ROWS_READ_20261007.md` @d8c2508869); row Z-S368 filed and its disarm cited in Z-S371 | section 5 |

The standing term of act 1 (CTO half): after the 2026-10-08 13:00Z AMGT_CORPUS fire, `r78_bb7.py --crit AC1` reads 211 of 243 or
the count the day's registrations explain; a fall means an older writer ran and this seat re-mints from HEAD the same hour.

## 4. JUDGMENT for L9 (yours)

- **bb-19 AC3, the walk on DEV** (portal `d1b21c97`, function `+s6R0/rc`): `deliverables/0.9.0_WK_AMGT_RESAPP~303/WALK_ROUND78.md`,
  23 captures, two walker arms (row Z-W303-S2). The worker's observations, no verdict:
  - **FWD-16:** BA's band reads "In the news on October 6th, 2026" with one item from "Barron's", a plain publisher name. The ONE
    PRESS opened a new browser tab to www.barrons.com; the walker's third-party block aborted that tab, so the article was not read.
  - **FWD-12:** the page states the inputs in TWO places and they disagree (the block above the tabs: Seeking Alpha "September
    11th, 2026 -- Worked"; the Model tab ledger: Seeking Alpha "has not run yet", Filings "no source set up yet"). The server now
    sends ONE statement with a filings row on `/thesis`; the page at this ref does not draw it (row Z-W303-S1).
  - **FWD-7:** 95 rows, 3 stale; the Seeking Alpha cell read `2026-09-11` three times and `Not collected` twice on the 5 rows
    (the column's reader is unchanged this round; row Z-S367). First paint 4,580 ms then 2,019 ms.
  - **FWD-1 on AMD:** a reason where the segment breakdown would be, marked SEGMENT TABLE NOT SERVED THIS ROUND.
  - **COVERAGE:** on MSFT the page does not draw the served "We do not cover this company yet" sentence and shows ten other
    absence statements; the portal source at this ref does not reference `research_coverage`.
  - **OFFICERS:** BA and HD draw the chief executive then the chief financial officer. **BP/ LN draws the CFO first** while the
    function serves the CEO first (row Z-S372).
- **The dossier at method 7 on served routes:** the redeploy moved the reader from method 5 to method 7. Your grade @09c91edcc2
  read the stored objects; nothing in this round's checks reads the served management text against a filing. If L9 wants the
  served side, the artifact is the live `/thesis` on any of the 35 names of AMGT_CORPUS's census. The CTO has since ruled
  (msg 31623) that five stored dossier fields are served by NO route today, so of the "51 values" only those in management and the
  four other served fields can have moved on the page.

## 5. Rows filed since the last packet (disarm_owner `2.0.0_SA_COO~Z` unless said)

| row | standing | one line |
|---|---|---|
| `AMGT_RESAPP-Z-S368` | ARMED at filing; its disarm is cited in Z-S371 | the deployed page served USD beside a foreign-listed peer price, 2 of 60 sampled rows |
| `AMGT_RESAPP-Z-S371` | INERT | Z-S368's disarm: after bb-18 the same clause reads 0 wrong of 60 on the live function |
| `AMGT_RESAPP-Z-S372` | INERT, disarm_owner `2.0.0_SA_COO~D` | BP/ LN: the function serves the CEO first, the page draws the CFO first |
| `AMGT_RESAPP-Z-S370` (by `0.7.0_AE_CloudOps~A`) | INERT | the Lambda source map's note for this function still reads "NOT YET UPLOADED" after two deploys |
| `AMGT_RESAPP-Z-W289-S1` | ARMED at filing; answered by bb-1 AMENDMENT 1 | a later pull of other fields hid AMD's stored segment table; residual: the reader looks at five objects |
| `AMGT_RESAPP-Z-W299-S1` | INERT | a stale constant in the bb-14 check; the check was amended |
| `AMGT_RESAPP-Z-W302-S1`, `-S2`, `-S3` | INERT | the bb-17 check misread the provenance shape (amended); the overlay's inputs list left unchanged (issuer ruling); one stale test (repaired) |
| `AMGT_RESAPP-Z-W303-S1`, `-S2` | INERT | two statements of inputs on the page that disagree; two walker arms |
| `NFRA_CTLPLN-Z-S3` (that project's channel) | ARMED, dated, disarm_owner `2.0.0_SA_COO~C` | the trading calendar's fallback ends at 2027: staleness reads raise from 2028-01-01 |

Row `AMGT_RESAPP-Z-S369` exists in the channel and was not filed by this seat; it is not described here.
The 13 older ARMED rows the analysis named: `round78/ARMED_ROWS_READ_20261007.md`. Eleven still read OPEN and ARMED in
`remediations/`, which is your clock. Row Z-S362 stays OPEN: bb-20 landed 9 of the 45 files.

## 6. For round 79 (carried; cited, not cut here)

1. **Serve five stored dossier fields no route serves** (positives, negatives, special_items, why_we_own, company_description):
   CTO msg 31623; where each shows is DSGN_AMGTV1's.
2. **The segment table's hookup** (bb-1 with bb-21): 72 of 76 names tie to stored revenue; the CTO reads this round's result first.
3. **The Seeking Alpha last-read reader's hookup** (bb-16): only when AMGT_HARVST's collector records exist for the reached names.
4. **ABNB's model-block pull** (issuer act 2 of this round, not run).
5. **The five packaged files the trunk merge moved** (`lib/opal_naming.py`, three registry files, `NAMING_SCHEMA.json`): the live
   code is behind CLOUD HEAD on them by the CTO's C1; the next redeploy's half measures them.
6. **The page findings of the walk** are DSGN_AMGTV1's: the one statement of inputs, the coverage sentence, the officers order.
7. **The build's duty:** `C:/tmp/bb18-r78-fbb643923e.zip` is the next build's `AMGT_DEPLOYED_ZIP`; a wheel version bump goes
   through the laptop's intake.
8. **Filing coverage** (83 names with no filing read) and **the Recommendation label**: reads delivered in `round78/reads/`; no cell.
