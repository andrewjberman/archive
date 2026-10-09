# AMGT_RESAPP round 88 -- the issuer's reads on the rows carried to `2.0.0_SA_COO~R1` (ROW_DISPOSITION_R1.md, "issuer READS")

Each read answers its row's question; a read that finds a defect becomes a round-89 cell, never a mid-round one.

## D1-S6 (2026-10-09 ~20:4xZ) -- the source map after the round-87 redeploy

`infra/aws/lambda/ci/lambda-source-map.json` `functions["opal-amgt-scoped-api"]` reads `deployed_code_sha256` HZoC2x...,
`last_deployed_at` 2026-10-09T13:45:16Z, `deploy_ledger` amgt-resapp-r85-jj5-scoped-api-dell1 -- the ROUND-85 deploy. Live is b7Lj1J
(19:51:25Z). **Finding:** round 87's redeploy was never recorded. Row **D1-S19** filed @0ea385c1d7; AMGT-mm-4 AMENDMENT 1 runs the
record step and prints the entry before and after.

## D1-S14 (2026-10-09 ~20:5xZ) -- peer `price_currency` on the live route

Live `GET /security/ASML_NA_Equity/peers` (b7Lj1J), 12 members: `price_currency` USD on 2 (AMD, NFLX); on the other 10 it is null with
`price_currency_reason` "The scanner price for this peer carries ..." (no currency on the scanner's price). **Answer:** the route is NOT
stale -- AMGT-at-3 serves a currency or a reason per member; the walk's "currency not stated" is true to the data. **Defect for round 89:**
the scanner's peer price carries no currency for 10 of 12; the currency must come from the price source (producer side).

## D1-S16 (2026-10-09 ~20:5xZ) -- peer identity and tickers on the live route

Same read: 12 of 12 members' `identity` read **UNRESOLVED**; tickers include a SEDOL stem (Tencent `BMMV2K`) and a numeric code (SK
hynix `645026`). **Answer:** NOT deploy lag -- the peer members are not identity-resolved at the producer, so the page falls back to the
raw scanner code. **Defect for round 89:** resolve peer members through the identity pool (the av-5 numeric-ticker resolution exists but
does not reach these members).

## D1-W332-S2 (2026-10-09 ~20:5xZ) -- the --splice-driver question

The five stored drafts (`drafting/v1/<KEY>.json`, latest) all read `analyzer_version` opal-filings-analyze/2.1.0 and all carry
`thesis_driver` with a series, a unit, a `source_passage_id` and a `why` (ASML: EUV system revenue recognition; NU: Total revenue P0252;
SAP: current cloud backlog; BABA: Cloud Intelligence Group revenue P0446; PBR: total oil and gas production P0198). **Ruling: the
provenance splice is UNNEEDED** -- analyze 2.1.0 writes the driver with its passage; D1-W332-S2 -> CLOSED (no act).

## D1-S15 (2026-10-09 ~21:0xZ) -- the peer set's subject market cap vintage

Live `GET /security/ASML_NA_Equity/peers` (b7Lj1J): `subject.market_cap_musd` 541,931.78, `cap_vintage` 2026-09-19T07:53:19Z, `cap_currency`
EUR, `cap_source` model_block:ASML_NA_Equity:CUR_MKT_CAP (with the stated caveat that no FX is applied against the members' USD caps);
members' `cap_vintage` 2026-08-06; peers `as_of` 2026-09-24T2252Z. **Answer:** UNCHANGED at HEAD -- the subject cap is three weeks older
than today's header and on a different vintage from its members. **Defect for round 89:** refresh the subject cap to the header's
vintage, or drop it with its reason (the row's two branches).

## Z-W212-S2 (2026-10-09 ~21:2xZ) -- url on every gold article_security_mention row

Read-only over all 24 objects under `amgt/harvest/gold/article_security_mention/` (459,334 rows in all), per object: the 17 builds before
2026-10-06 carry NO `url` column (0 of their rows); the 2026-10-06T06:20 build carries it on 31,919 of 33,665; every build since
2026-10-06T08:44 -- six, the latest `date=2026-10-08/part-20261009T093755Z` (52,424 rows) -- carries a url on 100% of rows (33,665;
48,025; 48,358; 52,282; 52,709; 52,424). Each build is a full rebuild, so the served latest is complete. **Answer: YES since the 10-06
rebuild; Z-W212-S2 -> CLOSED on this read** (the producer change landed in HARVST's rebuild between 10-06T06:20 and 08:44).

## Still to read this round

Z-W266-S3 (driver-chart coverage).
