# FEED 9 — the client-identity resolver: bundle auth developed, first bronze landed, every number measured

**0.5.0_AE_OpalETL · 2026-07-14 08:3x–08:4xZ · ruling chain:** Andrew option-a (@ `b9b11f7fd`) →
CTO operationalization (074036Z) → CTO sequencing approval (083018Z). Executed after build items
1–3 closed (smartx-pipeline-v1.4.0).

## 1. Bundle auth: WORKS
- `smartx/credentials/yaliu-bundle` (TF shell @ `5f503f57a`, prevent_destroy; value put out-of-band
  from the HAR login POST — never printed, never committed). ROPC mint succeeds under it (no MFA
  obstacle); `auth_bundle._read_seed` BUNDLE path implemented — bundle JWTs mint in-memory and
  NEVER park into the shared opal7 `smartx/jwt/current` slot.
- Role grant deliberately NOT added (never-widen): rides the feed-9 daily-lambda wiring, CTO gate.

## 2. Coverage — measured on the bundle's OWN roster (never inherited from the HAR)
- 906 modelAccess (**0 fullAccess, 906 view**), **452 accountAccess**.
- **7 of our 11 models visible** (all view). The 4 invisible are the Global family = the 3 unfunded
  models + `Opal Global All Equity Total Return` carrying **exactly 1 living allocation** → the
  named identity gap is **1 / 9,525**.
- Feed 8 exercised under the bundle: `accounts/{id}/activity` → 200, 97KB, 574 ledger rows.

## 3. First landing (bronze, filed under OUR rmids)
`smartx/model/{rmid}/bronze/allocation_accounts/20260714/allocation_accounts.json` × 7 (≈1.70MB,
verified landings). Registry: `ACCOUNT_TIER_MODEL_FEEDS` (@ `b9211d884`) — deliberately OUTSIDE
`MODEL_FEEDS` so the opal7 flow can never pull the endpoint that empties at its grant.

## 4. The reconciliation guard FIRED — and grounded the endpoint's semantics
Resolver rows < feed-5 rows on all 7 models (7,141 vs 9,524). Mechanism, measured per-model:
**resolver = `open` + `workingClose` allocations; feed 5 = ALL statuses (incl. `close`).**
6/7 models tie EXACTLY on that identity; Conservative Growth off by −3, consistent with
allocations closing in the 43 min between the two pulls (timing — hypothesis, labeled).
- **Contract corrected:** feed-9-vs-feed-5 reconciliation compares against feed-5's
  `status ∈ {open, workingClose}` subset, same-vintage.
- **Closed-allocation identity (2,384 today) is the completion path:** the per-account inverse
  endpoint (`3.1/allocations?accountId=&status=open,close`) DOES return closed allocations —
  452 calls sweep the historical identity. Follow-up, not a blocker: the daily map accumulates
  go-forward (model × allocation × run_date date-effectivity per CTO's framing addendum).

## 5. Dictionary open-cell 4 — account_number normalization, MEASURED (CTO 083018Z ask)
- Resolver `accountNumber`: **8-digit all-numeric** (7,130/7,141) + 11 at 9 digits.
- CRS ACC `account_id`: **10-digit numeric, universally zero-padded** (6,897/6,897 start "00").
- **Join rule: `smartx_account_number.zfill(10) == crs.account_id` → 96.4%** (5,419/5,624 distinct)
  — measured against the LATEST CRS ACC silver, which is `date=20260508` (2 months stale; the 205
  misses plausibly include accounts opened since). **Re-measure on a fresh ACC partition** — flagged
  to DS: the ACC table's staleness is itself an observation (49-schwab-conv lane).

## Open items
1. Bundle expected-coverage guard values for the daily wiring: `opal_family_view >= 7`,
   `accounts >= 452` (measured today — the guard's constants are these measurements, re-probed at
   wiring time).
2. Closed-allocation identity sweep (452-call account-side enumeration) — proposal to CTO.
3. The 1-allocation gap (`Opal Global All Equity Total Return`) — unresolvable at ANY current
   grant; noted for the vendor conversation if it ever matters at gold.
4. Feed-9 daily-lambda wiring + role grant on the bundle secret ARN — CTO gate.
