# AMGT_RESAPP round 88 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~02:4xZ. mm-1 (issuer act), mm-2, mm-3, mm-4 complete; `round-close-check` reads
`orders=4 ... ungraded=0 self_graded=0 verdict=MAY-CLOSE`.** Round 88 implements the CTO~DELL1 round-87 analysis
`ledger/ROUND_ANALYSIS.round87.md` @08279f2a4f (items 1-5); decomposition s.96; issuance @450ec61d0d.

## 1. Orders and the issuer act

- **`AMGT-mm-1`** (the FAILED withhold DRIVEN -- issuer act, no store write): `round88_prep/MM1_PLANTED_RUN_20261009.txt`. The DEPLOYED
  reader (HEAD byte-equal to the live member, sha256 5b987a17) on a copy of the five drafts with NU planted from its FAILED prior version:
  withheld (0 sentences, FAILED, `withheld_failed` 1, test kept; /overlay not served). Negative arm: the round-86 reader 4c929a2ffe serves
  the planted sentence. Control: 4 of 4 unplanted names equal to live. The CTO graded round-87 item 1 EXERCISED on this run (msg 3148).
- **`AMGT-mm-2`** (the plain empty-state card): complete -- portal DEV **e225e9e1** (fast-forward, CTO-approved msg 3162, landed by
  0.0.0_AB_MSTR~DELL1 msg 3171). An empty or withheld description renders "No company description is available for this security yet."
  in navy on the white panel; a served one is unchanged. Harness 8 of 8 (the pre-change file fails 4); tsc -b 0. AC3 graded MET by the
  CVO (row AMGT_RESAPP-D1-C-S40).
- **`AMGT-mm-3`** (three repairs): complete -- merged @85777c27a8; graded MET by the CVO (ADJUDICATION_v106). (b) a set-but-missing
  `OPAL_RESEARCH_LIBRARY_ROOT` raises naming the path; (c) a filing sentence carries `generated: false`, a model sentence still requires
  true; (a) the watchlist selector stays IGNORED -- AMENDMENT 1 under its STOP clause (row D1-W350-S1: no roster, registry or status to
  mirror in scoped_amgt), D1-S18 dismissed (the CTO concurs, msg 3185).
- **`AMGT-mm-4`** (the redeploy): complete -- `0.7.0_AE_CloudOps~RA1` msg 3316; ledger `amgt-resapp-r88-mm4-scoped-api-dell1` CLOSED
  12 of 12 @192afa6912; proof-of-spec VALID rc=0 on committed bytes. Build pin box/dell1 @4d006edc74 (carries mm-3 @85777c27a8 and dossier
  `amgt-corpus-dossier/10`; scoped_amgt.py 0 team_sheet lines). Live `opal-amgt-scoped-api`: CodeSha256
  `KlosR/ap8O3tYrjDfNkUofT/vTQ5pTt32EvYL8mCqs8=` (base `b7Lj1J..`), LastModified 2026-10-09T22:55:03Z, Active, Successful.
  Source-map record step (AMENDMENT 1, row D1-S19) landed at 4607adbfcd. No STOP arm, no row.

## 2. The issuer's ONE REAL RUN at close

Run by `2.0.0_SA_COO~R1`, 2026-10-11 ~02:3xZ, against the LIVE function (no store write, no Bloomberg; `GET` through the scoped API):

- **Live hash re-read first:** `aws lambda get-function-configuration opal-amgt-scoped-api` -> `KlosR/ap8O3..`, equal to the worker's L9 value.
- **AC2** `round87_prep/checks/r87_withheld.py --crit AC1`: five drafted names (ASML_NA, BABA_US, NU_US, PBR_US, SAP_GY) each status 200,
  verdict NO_SENTENCES, 0 served sentences; `PASS W1` (no FAILED description carries a sentence), `PASS W2` (5 of 5 answered with the
  company_description section); `R87 WITHHELD AC1: YES`; exit=0. The withheld behaviour mm-1 drove on a copy holds on the deployed function.
- **AC3** `round84_prep/checks/r84_listing.py --crit AC1 --where deployed`: typed ASML resolves to ASML_NA_Equity and names the other
  listing (`PASS R1`); "Micro" still answers the 404 candidate list AMD/MSFT/MU (`PASS R2`); Nu, zzqx resolve and thesis zzqx are byte-equal
  to base, 3 of 3 (`PASS R3`); `R84 LISTING AC1: YES`; exit=0.
- **AC1** is the worker's, run in the detached build worktree at the pin (HEAD = 4d006edc74) and recorded in the proof instance; the
  issuer did not re-run it (the shared tree's HEAD is not the pin).

## 3. JUDGMENT for L9

1. mm-2 AC3: NU's page on portal DEV (e225e9e1) -- the description card's empty state. **Already GRADED MET** (row
   AMGT_RESAPP-D1-C-S40 by 3.0.0_SA_CVO, on the CVO's ui-walk); `round-close-check` counts `judgment=1 graded=1 ungraded=0`.
2. mm-4 is `risk WORLD`: no JUDGMENT criterion; its three criteria are mechanical and passed on the worker's run and the issuer's re-run.

## 4. Rows filed this round

D1-S19 (the round-87 redeploy b7Lj1J never recorded in the source map; folded into mm-4 as AMENDMENT 1; the worker reports the
record step landed at 4607adbfcd -- the row's own disposition is not re-read here); D1-W350-S1 (ruled); D1-S18 (dismissed, CTO
msg 3185). The mm-4 worker filed no row at close (msg 3316).

## 5. For the next round -- the issuer reads (`round88_prep/ISSUER_READS.md`)

1. D1-S14: 10 of 12 ASML peers carry no price currency at the scanner source.
2. D1-S15: the peer set's subject market cap is on a 2026-09-19 vintage, older than its header and its members.
3. D1-S16: 12 of 12 ASML peers read identity UNRESOLVED (SEDOL / numeric tickers on the page).
4. Z-W266-S3: the driver chart serves 1 of 94 covered names (BA); the drafted names' drivers find no numeric source.
5. Closed on reads: D1-W332-S2 (the splice is unneeded), Z-W212-S2 (url on 100% of gold mention rows since 10-06).
6. Z-S2 / Z-C-S2: this packet prints the check line below. Z-W45-S1, Z-S369: Andrew's word.

checked 7 of 7 issuer reads (D1-S6, D1-S14, D1-S15, D1-S16, D1-W332-S2, Z-W212-S2, Z-W266-S3)
