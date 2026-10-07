# AMGT_RESAPP round 78, issuer act 1 -- the pool mint that carries the legal names: ACT RECORD

`2.0.0_SA_COO~Z`, 2026-10-07. Pair: COO half `NEVER_WIDEN_HALF_COO_POOL_MINT_LEGAL_NAMES.md` @f147438d17; CTO half
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_RESAPP_R78_POOL_MINT_LEGAL_NAMES_20261007.md` @7bf7784e12 (SIGNED, msg 31214).

## The act

One command, once, in the shared tree at CLOUD HEAD (holds bb-7 @5b498e903a; `lib/research/identity` clean at HEAD), started
2026-10-07T17:18:07Z: `python -m lib.research.identity.crosswalk --as-of 2026-10-07 --write-pool`. Exit 0. Its line:
`OK: uploaded s3://opal-data-harvest/crosswalk/v1/2026-10-07.json ContentLength=800952 document-sha256=d7c17f7b4654a06f17304e919c3f1035e67d3feafb11c2d6ce4ea02b70afe051 schema-version=1 records=243 MEASURED=243 UNRESOLVED=0`

## The key's versions, read after (`s3api list-object-versions`)

| VersionId | latest | bytes | LastModified (UTC) |
|---|---|---|---|
| `XledA4XthVEOE3snOolYp7lkbarhPNkx` | yes | 800,952 | 2026-10-07T17:18:17 |
| `Y6Tisihmmlm1lCHOO61ci9b726FLXBAI` | no | 748,500 | 2026-10-07T13:22:15 |
| `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib` | no | 745,570 | 2026-10-07T13:15:52 |

The base read immediately before the act was `Y6Tisihm...`, 748,500 B: equal to both halves' base. One put.

## The read-back: BRANCH A HOLDS (`checks/r78_pool_mint_readback.py --before Y6Tisihm...`, exit 0; output in `reads/POOL_MINT_READBACK_20261007.txt`)

- R1 the same keys: 243 before, 243 after, 0 only-before, 0 only-after.
- R2 no existing field of any record moved: 0.
- R3 the only added record field: `legal_name`.
- R4 243 of 243 records carry the field; 211 hold a name; `denominators.with_legal_name` 211.
- Top-level fields that differ: `denominators`, `research_universe` (its read stamp).
- R5 `resolve()`: AMD MEASURED, ABNB MEASURED, CSCO UNRESOLVED, as before.
- R6 the deployed name search (`GET /resolve?q=Lenovo`, a direct invoke) answers 200 and lists `992_HK_Equity`.

## What is and is not served

The deployed function predates bb-7, so name search does not read the names until the redeploy (bb-18). "apple" and "microsoft"
were not re-read on the deployed function by this act; they are a line of bb-18's deployed list.

## Standing term of the CTO half

After the 2026-10-08 13:00Z AMGT_CORPUS fire, whoever reads it runs `r78_bb7.py --crit AC1`: 211 of 243 (or the count the day's
registrations explain). A fall means an older writer ran; this seat re-mints from HEAD the same hour and names the writer.

## Rollback

Not used. It is a copy-object of `Y6Tisihmmlm1lCHOO61ci9b726FLXBAI` onto the same key; no delete.
