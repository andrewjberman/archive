# ETFS_RIVALS round 2 -- the COO's drain-end read (`/dispatch` step 6)

**Seat:** `2.0.0_SA_COO~RV`, 2026-10-01 ~05:2xZ. **To:** `3.0.0_SA_CVO~RV`, the L8 compile and L9. Andrew paired this CVO with this
seat. **Risk:** WORLD (d-3). **CLOUD:** the drain is at caafc907e7.

## Round state: 9 of 9 task orders terminal

| order | worker @ | merged @ | issuer re-run |
|---|---|---|---|
| RIV-m-1 | ~4 @52c8423ec2 | 5b837f5024 | AC1, AC2 PASS. Verdict JOIN_BLOOMBERG, then superseded by Andrew "1b": both homes are `home_producer` |
| RIV-u-1 | ~1 @7fe00140a6 | 22d912baaa | AC1-AC3 PASS |
| RIV-b-1 | ~2 @f80f2ddeb0 | 3ac5a8666e | AC1-AC3 PASS. b-1.AC3 re-run PASS after d-3's enabling line |
| RIV-e-1 | ~3 @c70a943c70 | 6140b8a4d7 | AC1, AC2 PASS |
| RIV-g-3 | ~1 @b8722119d1 | ae1c849af1 | AC1, AC2 PASS |
| RIV-h-1 | ~1 @dd61bc2fb5 | 312fed0369 | AC1, AC2 PASS |
| RIV-g-4 | ~3 @af72811643 | 5897445325 | AC1-AC3 PASS |
| RIV-p-2 | ~1 @3f843b8c9e | db8fba2b8d | AC1, AC2 PASS |
| RIV-d-3 (WORLD) | ~5 @914c31bf3a (resume, amendment 4 @2b1b2b74fe) | caafc907e7 (close @8ad2033519) | AC1-AC3 PASS, re-run live by the issuer at ~05:0xZ |

- **Ledger.** `etfs-rivalfunds-round2` is CLOSED. Legs L1-L6 are proven, with L5 pinned to 878746ee3e. The completion record is
  `org/critical_paths/change_management/20261001T0043Z_etfs-rivalfunds-round2_deploy_completion.md`.
- **Package.** `python -m pytest data/etfs/scripts/rivalfunds/tests -q` reads 189 passed, 2 skipped, 0 failed (issuer run).

## The one real run at close (read by the issuer, 05:1xZ)

`s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-09-30/index.html` is revision 20261001T043113Z.
- It is grouped by Opal fund:
  - **Group IDVZ:** 5 of 6 funds updated. TXUE, BIDD, CGIC, INEQ and SCHY are updated through 2026-09-29. IDVZ itself is the home fund and is not read this round (row W1-S8).
  - **Group PFOE:** 1 of 7 funds updated (BASG).
- The manifest reads `status: not-updated` with `funds_total 13`, `funds_updated 6` and 10 funds in the input.
- `report_date_freshness` FAILs for WCMG, TSEL, ETFT and PCLG. Their latest Bloomberg report date is 2026-09-28 against an expected 2026-09-29: a lag of 1 trading day against a PROVISIONAL threshold of 0 (row W5-S28).
- The other checks PASS: content_repeat, completeness, identity_coverage and render_readback.
- GQGU is not in the page's input.
- **Measured served counts (d-3.AC2, issuer re-run):** G2 holds 501 objects. New-day counts equal the census: SCHY 501, INEQ 498, CGIC 496, BIDD 464, TXUE 417.
- **Bloomberg bronze** holds 937 raw captures and 937 sidecars (AC1).
- **G5** holds 19916 rows. It is income-clean, with no Curncy trade, and SCHY's cash movement is in G6 (AC3).
- **Not exercised: the live 08:03 ET Bloomberg leg.** It is enabled (`RIVALFUNDS_BBG_LEG=1`, b-1.AC3 PASS). Its first fetch needs the
  Terminal sign-in. The last health read was ok=false at 2026-09-30 20:08 ET. The next trading day's 08:03 leg plus the 09:00 sweep is
  the acceptance, and is read at the close (outcome class ABSENT until then, never EXERCISED).

## Rows: the channel against the round

- **Channel:** `surprise-channel/investigations/INVESTIGATION_v1.Z.md`, 66 rows. By class and standing:
  - OBSERVATION/INERT 52
  - BLOCKING/ARMED 9
  - BLOCKING/INERT 2
  - OBSERVATION/ARMED 3
- **Round-1 armed rows** (W5-S1, S4, S6, S8, S9, S10, S12, S16) were disarmed by act in round 1. They are recorded in
  `deliverables/2.0.0_SA_COO~RV/round1/DRAIN_END_READ_ROUND1.md`. Rows are immutable at the gate, so each still reads ARMED.

**Round-2 armed rows, each with `disarm_owner` 2.0.0_SA_COO~RV:**

| row | hazard | state |
|---|---|---|
| W5-S24 (BLOCKING) | `silver_bloomberg` deleted superseded silver without DeleteObject, so the batch wrote no marker | **DISARMED.** Amendment 4 @2b1b2b74fe: supersede-without-delete, live by apply 0/5/0 at 04:10Z. Resolution row W5-S25. Batches 07 and 08 wrote their markers on the new code |
| W5-S26 (OBSERVATION) | `test_b1` encoded the removed delete | **DISARMED.** Issuer test fix @8ad2033519, row Z-S3. The package is green |
| W3-S13 (OBSERVATION) | a G5 object built before its date's G3 stays income-unclean | **DISARMED by construction.** The `enrichment_gate` in `sweep.py` holds `build-trade-schedule` until a pull-enrichment marker exists on or after the batch's newest report date (`d3_live.json` `w3_s13_disarm`; `tests/test_d1_sweep.py`) |
| W2-S4 (OBSERVATION) | `silver_issuer._capture_id` now starts with the requested date. A new-format capture sorts BEFORE any old-format id (`-` < `0`), so it loses to the landed object | **ARMED, NOT DISARMED.** Measured 05:1xZ: issuer silver has 325 report dates, 325 old-format and 0 new-format. Every re-capture of an already-landed BASG report date (a carried issuer date) keeps the OLD rows silently. A new report date is unaffected. The remedy is a code change to a live Lambda (WORLD): the first cell of round 3 |

Other rows filed this round go to the analysis as OBSERVATION/INERT: W1-S6..S16, W2-S3, W2-S5, W3-S6..S12, W3-S14, W5-S18..S23,
W5-S25, W5-S27, W5-S28 and Z-S2. Two of them:
- W5-S27: the code apply moved five Lambda hashes, not one. It is inside key 6, because the five Lambdas share the `rivalfunds/` package.
- Z-S2: there is no cross-seat lock on gateway deploys. Owner: `1.0.0_SA_CTO~Z`.

## For the round-2 analysis (the next round's enrichment list, the CTO's to write)

1. **W2-S4** (armed, above): order the issuer silver by the capture's embedded UTC timestamp. It is the round's one live-correctness
   hazard.
2. **The home-producer reader** (W1-S8). IDVZ and PFOE read ABSENT on the page.
3. **The G9 recurrence gate** (PRD v0.6), together with G4 and G7-G13 as carried in the PRD.
4. **Freshness threshold.** It is PROVISIONAL 0. A 1-trading-day Bloomberg report lag on four PFOE rivals holds the publish marker
   (W5-S28, W1-S5).
5. **GQGU** is absent from the page input: measure why.
6. **Rows W5-S21** (`land_capture` is quadratic on S3) and **W5-S22** (the leg's exit codes are 90-97).
7. **Close-read owed:** the first live 08:03 leg after Andrew's Terminal sign-in.
