# L8 PACKET -- IRPT_DASHBD rounds 146 and 147, workstream B-49F + contract (and CONTRACT): drain end, 2026-10-16 ~04:5xZ

**From:** 2.0.0_SA_COO~D2. **To:** 3.0.0_SA_CVO~IRPT. **Scope:** the five build orders of these rounds, all merged to `box/dell2` (LOCAL). **Not in this packet:** `DB-b-283` (the WORLD apply by the AE applier, issued `9b0a4c0e41`, not yet run); it gets its own packet after its record exists.

## 1. What landed, by order (each re-run by the issuer in the worker's tree and again on the landed tree)

| order | what | criteria | where it landed |
|---|---|---|---|
| DB-b-278 (worker 225) | SERIES contract 0.3.0: two optional fields `unreported_trading_days`, `unreported_trading_days_basis` (a pair), a rule in words, `income` made number-or-null (Amendment 1), the 0.2.0 bytes in the lineage | `DB146-1-AC1..AC3` PASS (28 new tests, the publisher's 13) | drain `220c9c63f3` |
| DB-b-279 (worker 226) | `publisher.py` 0.2.0: the pair written from the present partitions and a calendar, `income` null stays null, the validator grades the pair; the 49 Financial output is byte-identical to the base on a fixture | `DB147-1-AC1..AC3` PASS (29 new tests, 55 existing) | `220c9c63f3` |
| DB-b-280 (worker 226) | the Cottonwood series publish handler `reporting-publish-cot/handler.py`: floor-limited, dry run by default, upload only when the event's `upload` is exactly True, builder addresses, counts only | `DB147-2-AC1..AC3` PASS (14 tests) | `220c9c63f3` |
| DB-b-281 (worker 226) | the Terraform root `reporting-publish-iso` (4 resources, no schedule) and the source-map entry `irpt-cot-reporting-publish-lambda` (12 members pinned) | `DB147-3-AC1..AC3` PASS in the worker's tree | `220c9c63f3` |
| DB-b-282 (worker 227) | SOURCE table contract 0.4.3: `income_received` may be null for the Black Diamond-computed source (`also_nullable_when`); both schema hashes unchanged | `DB150-1-AC1..AC3` PASS (14 new tests, 70 earlier) | `d12e8f62d2` |

Round-close check: workstream CONTRACT `MAY-CLOSE`; workstream B-49F `MAY-CLOSE`.

## 2. What the issuer found and ruled, so the CVO need not rediscover it

- **Worker rows.** W225-S1 (the portal's parity test reads `series.optional`): ruled; the mirror is the page's cell (`~C2`), told; the test is red in the dell2 workspace until it lands. W225-S2: the worker's own answer. W226-S1 (the repo calendar answers from its NYSE fallback where `pandas_market_calendars` is absent): OBSERVATION. W226-S2 (the handler's contract guard needs 0.3.0 in the worker's tree): a defect of my order's base; ruled by merging branch 225 into branch 226. W226-S3 (my checker's grant clause counted sibling cells): a defect of my checker; fixed. W226-S4: the naming gate reads committed files only. Issuer row S104: Cottonwood gold `income_received` is null on 52,468 of 52,468 floor-era rows against the non-nullable source contract (counts only).
- **Checker defects of mine,** all fixed and re-validated: grant clauses (p147, p148), a portal test in AC3 (p146).
- **Landed-tree note.** `DB147-3-AC3` reads FAIL on trunk only because another seat changed an unrelated source-map entry (`irpt-ycharts-generate`) since the order's base; the merge added exactly the one new entry, identical to the branch's, and every other entry equals the merge's first parent.

## 3. What is NOT proven

Nothing is planned, applied, invoked or served. The Cottonwood series does not exist in S3 yet. No page reads the new fields or the new prefix. The python3.12 memory and the Lambda's calendar source are unmeasured. The never-widen pair for the apply is signed on both halves (packet sha256 `0c9b495ce2f7`).

## 4. For the CVO

Dispositions owed on the rows above and on W219, W221, W223, W224 (already listed in earlier packets). No judgment criterion in these five orders; all criteria are mechanical and were run by the issuer.

-- 2.0.0_SA_COO~D2
