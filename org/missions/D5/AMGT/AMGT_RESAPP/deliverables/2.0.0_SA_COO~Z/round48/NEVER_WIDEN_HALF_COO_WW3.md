# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 48, AMGT-ww-3's WRITE (the research library's missing rows into etf-classifications) -- 2.0.0_SA_COO~Z, 2026-09-29

The act this half covers is the ISSUER's, at ww-3's drain: ONE run, from the repository root at a commit containing ww-3's drain
(@b197eca459), of

    PYTHONPATH="$(pwd)" python infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py --universe amgt-library

It executes only after BOTH halves are committed, under ONE NEVER-2 entry opened and committed before it and closed after it.

## THE BLAST RADIUS

**The property written:** rows of DynamoDB `etf-classifications` (us-east-1, key `ticker`, the bare ticker). **Writers of that
table, counted:** (1) `seed-etf-constituents.py` -- universe `positioning` (preserve-by-default) and, with this act, `amgt-library`;
(2) `seed-etf-classifications.py` (the models universe); (3) `data/black_diamond/scripts/classification/seed_canonical_securities.py`
(manual, GetItem pre-check then write; none of its literal tickers is among the 59). N = 3 writer scripts; this act runs ONE of
them, with ONE universe.

**Both branches, read from the landed writer's own rule (not predicted from the input's shape):**
- **CREATE** -- a library bare ticker the table does NOT hold: ONE `put_item` with `ConditionExpression="attribute_not_exists(ticker)"`,
  item = `{ticker, asset_class: "equity", sub_asset_class: <the block's own GICS_SECTOR_NAME>, management_style: "unknown",
  last_updated, updated_by: "seed-etf-constituents --universe amgt-library (AMGT_RESAPP round 48, 2.0.0_SA_COO~Z)"}`; `name` is
  written only from `NAME_CORRECTIONS` (0 of 59 have one), else withheld (row Z-S300); `sector` is never written; `None` and `""`
  are dropped. **Expected: 59 creates** (the writer's dry-run @b197eca459: `PLAN: 59 create / 0 update / 36 preserve-existing`,
  95 readable, 0 SKIP, 0 named / 59 withheld). The 59 keys: 1299 2317 8035 8306 8316 8766 939 9433 992 ADBE AI AMXB BABA BATS
  BBSE3 BNP CDNS CELH CLX CNR COST ENEL GPN HAL HEI HSBA IBE ICICIBC IMB ISP KMB KOFUBL KPN ML MSCI NESN NG NKE NOKIA NOVN ORA
  PWR RKT RMS ROG RWE SAN SAP SHOP SLB SNPS SSE ST UBSG ULVR VIVT3 WALMEX* ZTS ZURN.
- **PRESERVE** -- a library bare ticker the table ALREADY holds: no write at all (the universe refuses `--force-names`, rc 2), and
  the condition makes an overwrite impossible even under a race. **Expected: 36 preserved, byte-unchanged** (fixture
  `round48/checks/fixtures/etfc_held_before.json`).
- A ticker absent at the dry-run but created by another writer before the act: the conditional put FAILS for that key
  (`ConditionalCheckFailedException`) and nothing is overwritten -- the create count drops by that many, which the lane prints.

**Rollback per key:** each created key is deleted by its literal ticker, only if its `updated_by` still reads the string above
(a key someone else wrote since is left alone). No existing row is touched, so there is nothing else to roll back.

## WHO READS THE TABLE -- measured 2026-09-29 ~13:2xZ (read-only census, 9 code readers, live IAM sweep 219 functions / 132 roles found no other)

| reader | shape | effect of the 59 rows |
|---|---|---|
| `scoped_amgt._classification_for_ticker` (ww-2; served at ww-1) | GetItem | the INTENDED change: 24 of 41 live ranking tickers flip classification ABSENT -> SERVED, `name_state` stays ABSENT |
| `lib/research/identity/positioning_chain.py:261` | full scan into a map, then key lookup | a printed row count 285 -> 344 (stderr); the universe's PWR (same company) gains unused fields; no name used |
| yang-generate-positioning / yang-generate-holdings-attribution (production) | GetItem | 0 of 62 / 0 of 56 universe tickers among the 59 -- no change |
| `data/etfs/scripts/gold/etf_positioning_publisher.py:250` (cron 13:00) | GetItem, `name` only | 1 of 167 (PWR, same company, entered the holdings 09-28); the new row has no name, so the publisher still serves the issuer's name -- no change |
| `build_satellites_registry.py` / `build_satellites_characteristics.py` (cron) | GetItem | 0 of 25 / 0 of 25 -- no change |
| `seed_canonical_securities.py` (manual) | GetItem pre-check | none of its literal tickers among the 59 -- no change |
| `seed_bd_securities.py:51` (manual, "one-time") | full scan copied into `bd-securities` with an OVERWRITING put | **not run by this act.** IF re-run later, 24 of the 59 keys already exist in `bd-securities` and would be overwritten; 6 mean a different company (AI = C3.ai, ML = MoneyLion, ORA = Ormat, RKT = Rocket Cos, SAN = Banco Santander ADR, ST = Sensata). Row Z-S302 carries it |

`find_by_asset_class` / `find_by_sub_asset_class` (the GSI enumerations) have zero non-example callers. Not measured: the
attribution Excel input (the served output, last written 09-04, was used) and whether anything schedules `build_universe`.

## THE LANE STOPS on any of four limbs

1. The run's PLAN line is not `59 create / 0 update / 36 preserve-existing` (or fewer creates only by conditional failures it
   prints), or it names an UPDATE.
2. Any `SKIP` line, or any CREATE line carrying a name or a non-`equity` asset class.
3. After the run, `round48/checks/ww-3.AC2.py` reads any of the 36 held rows changed -- the ROLLBACK trigger (delete the created
   keys by the rule above).
4. The run touches any table other than `etf-classifications`.

## THE FALSIFIERS

1. `round48/checks/ww-3.AC3.py`: 95 of 95 library tickers held with asset_class and sub_asset_class; 0 named all-caps or by ticker
   (at the cut: held 36).
2. `round48/checks/ww-3.AC2.py`: the 36 held rows byte-unchanged (PASS before and after).
3. After ww-1 serves, `round48/checks/ww-1.AC3.py` reads rankings rows carrying classification for the formerly-absent tickers.

Signed: `2.0.0_SA_COO~Z`, 2026-09-29.
