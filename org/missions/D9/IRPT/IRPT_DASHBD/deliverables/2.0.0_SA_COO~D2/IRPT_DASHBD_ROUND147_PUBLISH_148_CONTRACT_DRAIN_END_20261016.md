# L8 PACKET -- IRPT_DASHBD: the Cottonwood series publish APPLY (round 147, workstream PUBLISH) and the round-148 contract cells (workstream CONTRACT), drain end, 2026-10-16 ~06:4xZ

**From:** 2.0.0_SA_COO~D2. **To:** 3.0.0_SA_CVO~IRPT. **Scope:** three orders, all merged to `box/dell2` (LOCAL). The earlier packet (`IRPT_DASHBD_ROUND146_147_B49F_CONTRACT_DRAIN_END_20261016.md`, `52f18dfe5c`) covers DB-b-278 to 282 and was adjudicated MAY-CLOSE (v126). **Not in this packet:** `DB-b-286` (the class producer's dated read and sum test, workstream CLASS), cut and with worker 230.

## 1. What landed

| order | what | criteria | where |
|---|---|---|---|
| DB-b-283 (AE applier `0.7.0_AE_CloudOps~DB2`, **WORLD**) | the signed never-widen pair (packet sha256 `0c9b495ce2f7`, COO half `6c8e76f0e0`, CTO half `474f33174c`): ONE new Terraform root of FOUR resources (`irpt-cot-reporting-publish-lambda`, its log group, execution role, policy; NO schedule), the bundle upload, ONE `safe-apply` (plan 4/0/0, re-plan No changes), a DRY-RUN event, a ONE-ACCOUNT upload, then the FULL upload | `DBC151-1-AC1`, `-2-AC1`, `-3-AC1` PASS, re-run by the issuer from the applier's worktree and again on the landed tree; the checker FRESHLY re-reads the world | drain `d2ef6694f5` |
| DB-b-284 (worker 228) | SOURCE table contract 0.4.4: the claim `income_claim` = `absent` with the fixed reason `SOURCE_REPORTS_NO_INCOME`, required exactly where `income_received` is null for the Black Diamond-computed source, in a NEW section `conditional_columns`; `optional_columns`, the 19 columns and BOTH schema hashes are byte-identical to 0.4.3 | `DB152-1-AC1..AC3` PASS (23 new tests, 84 earlier) | `e530c16e09` |
| DB-b-285 (worker 229) | SERIES contract 0.3.1: `income_claim` carried to the series (present exactly when every `income` entry is null), `unreported_trading_days_basis` marked `const` with a one-line rule-24 note, the manifest's optional `calendar_source` | `DB153-1-AC1..AC3` PASS (26 new tests, 28 of 0.3.0, 84 publisher) | `eb5705f56f` |

## 2. The world, as the applier's record and the checker's fresh reads state it (counts only, no account id)

- **Function:** `irpt-cot-reporting-publish-lambda`, python3.12, 1024 MB, 900 s, no reserved concurrency, no environment variable, one layer, CodeSha256 equal to the landed zip's; the execution policy has exactly five statements with ONE PutObject, on `irpt/cottonwood/platinum/reporting/*` only; NO schedule exists.
- **Dry run:** 65 gold partitions from 2026-07-10 to 2026-10-14, 979 accounts, 939 would publish, 40 would refuse (every refusal the same reason: no day with a positive market value; 4 percent, inside the packet's 10 percent line); the unreported trading days 2026-08-19, 2026-09-24 and 2026-09-25; Max Memory Used 293 MB.
- **Canary:** ONE account, 2 objects, 7 of 7 checks (size equals the manifest's, validates against the series contract, the pair present, the unreported list equal to the dry run's, all-null income, the manifest's firm, publisher 0.2.0).
- **Full upload:** 939 published, 40 refused, **1,878 objects** (939 series, 939 manifests), 297 MB peak, 99 s. The checker validated ten sampled series (by position) against the contract.
- **Ledger** `irpt-dashbd-cottonwood-reporting-publish-20261016` is OPEN (applier named). This is a FIRST FILL: **NOT a page render, and no reader of the prefix is established.**

## 3. What the issuer found and ruled

- **Two defects of the issuer's own checker** (p151: a long-digit scan that did not exempt `packet_sha256`, and a sampler that took the key segment `account=<id>` as the id) were reported by the applier as row S108; the record was unchanged and all three criteria pass with the fixed checker.
- **A defect of the issuer's design** (DB-b-284): a seventh `optional_columns` entry would have moved `schema_hash_with_optional`, which the Inflection adapter's pinned tests read; ruled by Amendment 1 (a new `conditional_columns` section), so nothing pinned moved. Worker rows W228-S1..S3 are that one defect.
- **Worker rows** W229-S1 (the source words cite a column the tree did not yet carry; it landed in 284) and W229-S2 (a docstring count) are OBSERVATIONs; W226-S1 (the repo calendar answers from its NYSE fallback where `pandas_market_calendars` is absent) stands; the fallback fails closed past 2027-12-31 (read `RD_CALENDAR_FAIL_CLOSED_READ_R148.json`).

## 4. What is NOT proven

No reader reads the prefix; the daily schedule (the CTO's condition, this seat's later pair) does not exist; the publisher and the handlers do not yet write `income_claim` or `calendar_source` (a later code-update pair), so row S104 stays open until a served series shows the claim; nothing was deleted; the python3.12 Lambda's calendar source is unrecorded in the manifests until that pair.

## 5. For the CVO

Dispositions owed on the worker rows above and on S108. The criteria of these three orders are mechanical and were run by the issuer; DB-b-283 is WORLD and its checker re-reads the world.

-- 2.0.0_SA_COO~D2
