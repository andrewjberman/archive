# D2 FINDINGS — OPAL_ASSETS_49METATABLES (join concept 1: SmartX ↔ 49F client identity)

**0.5.0_AE_OpalETL · 2026-07-14 ~09:3xZ · for the sec-4 convergence gate (Andrew + CTO runner
architecture session). PRD @ `bd177ba0f`. Every number in this note is a same-day measurement;
grounding artifacts cited inline.**

## THE DELIVERED STATE (all CTO-gated, all exercised)

| piece | state | evidence |
|---|---|---|
| feed 9 resolver bronze | LANDED, 7/7 bundle-visible models, daily-wired | `smartx/model/{rmid}/bronze/allocation_accounts/{d8}/` (first landing 08:39Z; wired v1.5.0 @ `72bcaa3c7`) |
| closed-identity sweep | CONVERGED 6,620/6,620 accounts, 0 failed | `smartx/account/{id}/bronze/allocations/20260714/` + manifest `smartx/platform/meta/pulls/20260714/account_allocations_sweep_manifest.json` |
| bundle credential | live, tested, structurally separated | `smartx/credentials/yaliu-bundle` (SM only); `mint_bundle_token` in-memory; separation test permanent |
| daily go-forward | feed 9 in `smartx-assets-daily-pull` 09:30 ET | coverage guards = measured constants; fail-loud reconciliation |

## THE IDENTITY TABLE, IN RUNNER-CONSUMABLE TERMS

**Grain:** `model × allocation × run_date` (date-effectivity: a row asserts "allocation A was in
model M with account X **on day D**" — accounts move between models; the runner asks WHEN, and the
daily snapshot accumulation answers it. Never collapse run_date out of the dim.)

**Columns (silver `allocation_account_map`, pinned pyarrow schema @ `fd0b2636f`):**
`model_id, rmid, allocation_id, account_id, account_number (STRING, byte-faithful), account_name,
aum_value, run_date`.

**Sources, by identity class:**
1. LIVING allocations → feed 9 (`enterprises/reports/model/{modelId}/allocations`, bundle grant).
   Measured semantics: returns `open`+`workingClose` allocations **of reporting-visible accounts**.
2. CLOSED allocations → the account-side sweep (`3.1/allocations?accountId=&status=open,close`,
   one call per enumerable account) — run once as backfill 2026-07-14; the daily feed-9
   accumulation covers closures go-forward (yesterday's living row persists).

## COVERAGE — measured, per class (2026-07-14)

```
LIVING  (open+workingClose, all 11 models):  7,141 / 7,144  = 99.96%
  gap  = 3 allocations on non-reporting-visible accounts (CG-3: verified OPEN in feed 5
         right now, absent from resolver AND sweep; their accounts are not in the 6,620
         enumerable actives) + note 1 more living allocation sits in the bundle-invisible
         'Opal Global All Equity TR' (counted in the 7,144 denominator; identity unresolvable
         at any held grant)
CLOSED  (status=close, all 11 models):       1,315 / 2,381  = 55.2%
  gap  = 1,066 closed allocations whose accounts are NOT enumerable at the bundle grant
         (4.1/accounts exposes ZERO closed/inactive accounts -- measured; the direct
         allocation-detail endpoint 400s). STRUCTURALLY INVISIBLE at every credential we
         hold. If gold needs pre-2026-07-14 closed-client attribution beyond 55.2%, that
         is a VENDOR-GRANT conversation, not an engineering one.
```
Per-model living coverage: 6 of 7 bundle-visible models tie feed-5-living EXACTLY; Conservative
Growth −3 (the CG-3 above — account-visibility, NOT timing; the timing hypothesis was falsified by
re-reading feed 5 live). The 3 unfunded Global models: nothing to cover.

## THE JOIN RULE (dictionary open-cell 4) — measured, residual honestly open

```
join:  smartx.account_number.zfill(10) == crs_acc.account_id
       (SmartX emits 8-digit numeric (7,130/7,141; 11 at 9 digits);
        CRS account_id is 10-digit, universally zero-padded)
rate:  96.4% (5,419/5,624 distinct) against silver/ACC date=20260508
```
**The residual 205 stays UNPINNED** (CTO concurrence 084515Z): the CRS side is a 2-month-stale
vintage; fresh ACC bytes exist in monolith bronze through 07-13 (DS pointer: C3 lands
`08242234.CRS*.ACC.zip` daily; the staging silver/ACC table is also MEASURED LOSSY — the long-term
join substrate is 0.6.2's V2-8 converter output, not the legacy table). Re-measure there before
pinning.

### ADDENDUM 2026-07-15 ~14:5xZ — RE-MEASURED on the ruled substrate; residual PINNED to classes

Substrate: 0.6.2's V2-8 `fact_acc` (the long-term join substrate named above), fresh partitions,
both masters — `schwab/08242234/silver/fact_acc/date=2026-07-14/` (7,066 rows, 7,066 distinct
10-digit account_id; 0824 leg CTO-CERTIFIED 07-15, manifest shortfall_post=0) and
`schwab/08335338/silver/fact_acc/date=2026-07-14/` (7,139 rows). SmartX side unchanged:
fact_allocation_account_map date=2026-07-14 (7,141 rows, 5,624 distinct account_numbers — the
SAME denominator as the 20260508 measure).

```
rate:  99.43% (5,592/5,624 distinct) against fact_acc/date=2026-07-14 (master 0824)
       (was 96.4% = 5,419/5,624 on the stale lossy staging table -- the stale-vintage
        explanation HELD: 173 of the 205 residual join on fresh bytes)
residual: 32 distinct, $29.2M of $1.42B map AUM (2.06%), decomposed:
  19 = PRESENT ON MASTER 0833 (identity probe against 08335338 fact_acc same-date).
       RECORDED AS IDENTITY, NOT SUMMED (0824/0833 never-summed law). $21.0M map AUM.
  13 = ON NEITHER MASTER (9 nine-digit + 4 eight-digit; $8.2M map AUM).
       INFERRED (unpinned): the nine-digit class (346482072, 6383xxxxx, 6554xxxxx,
       645624489) does not fit Schwab's numbering -- plausibly non-Schwab custody.
       No instrument we hold can confirm custodian from these tables; stays open.
```
Gold-join consequence: the runner's 0824-scope join substrate is CLEAN at 99.43% with every miss
named; the 19 other-master accounts are a ROUTING fact (they join 0833's view), not a data hole.

## GUARDS THE RUNNER INHERITS (all live in v1.5.0)
- Coverage constants are MEASUREMENTS (`OPAL_FAMILY_VIEW_MIN=7`, `BUNDLE_ACCOUNTS_MIN=452`) — a
  grant shrink fails loud before a partial identity table can look clean.
- Feed9-vs-feed5(living) same-vintage reconciliation — a partial resolver payload fails loud.
- Fleet-zero = broken endpoint (the 267B class, both directions — the instrument itself was
  fixed once for reading POPULATED as EMPTY on nested shapes).
- Two-writers-one-scope: registered account-tier feeds are not surplus; unregistered keys still trip.

## OPEN CELLS FOR THE ARCHITECTURE SESSION
1. The 55.2% closed-history ceiling → vendor-grant question (named, quantified).
2. The join residual → re-measure on fresh CRS bronze / V2-8 converter output.
3. The 9-digit account_number minority (11 rows) → classify at CRS contact.
4. silver `allocation_account_map` build → V2-8 lane (schema pinned, writes phase-open per
   Andrew's silver-ahead-of-cert word; converter slots after 22:00Z per my sequencing).

---

## UPDATE 2026-07-14 ~11:0xZ — the CTO-GO'd four-item set EXECUTED (GO 095823Z)

**1. By-UUID number enrichment: COMPLETE, 91/91.** Unresolved set re-enumerated at run time
(reproduced exactly: 2,381 closed / 1,315 sweep-matched / 1,066 no-UUID / **91 unresolved
accounts**). `GET 3.1/accounts/{uuid}` under the bundle: 91/91 landed
(`smartx/account/{uuid}/bronze/detail/20260714/`), **brokerageAccountNumber present 91/91**,
status census `{active: 91}`, guard listing-based missing=0/surplus=0. Manifest:
`smartx/platform/meta/pulls/20260714/account_detail_enrichment_manifest.json`.
**CONSEQUENCE: every sweep-matched closed allocation (1,315, across 1,009 accounts) now has a
brokerage number pair** — 918 accounts via the living map + 91 via detail enrichment.
The by-UUID view carries **NO amount/date fields** (identity only) — Andrew's "amount+date in
the uuid view" hypothesis measured NO; the money leg rides nonzerosleeve + the atom, per the
addendum's own ranking.

**2. nonzerosleeve: LANDED.** 394,660B → `smartx/platform/bronze/nonzerosleeve/20260714/`,
511 rows / 511 distinct accounts / 511 with brokerageAcctNum / **47 outside the living map —
all 47 already inside the sweep universe** (no new enumeration unlock; their value is
corroboration). Money-leg fields confirmed on-row: `asOfTimestamp` + full opening/closing
valuation envelope (equity/cash/dividend/fee/interest + position counts). Registered as
`ACCOUNT_TIER_PLATFORM_FEEDS` @ `1061ef2ed`; agreement-rate vs fact_rps rides the V2-8/CRS
convergence (identity leg stays primary; money leg confidence-reported, never sole
determination).

**3. models/summary content check (read-only, NOT landed): 7/11.** The 5,234,127B served under
the bundle (platform `09a26328...`) carries **exactly the 7 bundle-visible Opal models**
(keyed by modelId; 897 entries total; per-model statistics: today/mtd/qtd/ytd, sharpe,
sortino, std_dev, annualizedReturn...). The 4 misses are the 4 Global models the yaliu grant
lacks — the same boundary as feed-9. **The models_summary open closes PARTIALLY via the bundle
path**; the 4 Global summaries (3 unfunded + Opal Global All Equity TR) are unreachable at
every held credential. Yaliu-platform bytes deliberately never land under our platform
models_summary key (would false-green the honest-dirty opal7 guard).

**4. Roster status-filter probe: THE WIDENING IS ZERO — hypothesis FALSIFIED.**
`4.1/accounts` DOES take a `status` param (and pages via `page`, not `pageNumber`):
`status=active` = 6,620 (= baseline), **`status=closed` = 0 rows, `status=inactive` = 0 rows**
at this grant. No enumeration-side widening exists; the 1,066 no-UUID class stands on its own
terms (vendor-grant conversation, unchanged). The "roster walk was default-status-filtered"
reading conflated the ROSTER with the LIVING MAP: measured, **91/91 enriched accounts ARE in
the active roster** — they were never roster-invisible, only living-map-absent (no living Opal
allocation ⇒ no feed-9 row). Denominator disclosure: the sweep universe is **7,066 = 6,620
roster ∪ 446 resolver-only accounts** — the two enumeration surfaces are overlapping partial
views (which is why the sweep took the union).

**Infrastructure note:** the two new bronze feeds are registered + guard-integrated
(`smartx-pipeline-v1.5.1`, artifact swap, deployed sha verified vs live, 0-diff) — the 13:30Z
daily fire reconciles clean over the coexisting bundle-lane landings (platform + account scope
two-writers exclusions, tests included).

**CTO RULINGS on this set (110557Z):** all four accepted. **models_summary open CLOSES as
RESOLVED-PARTIAL** — the summary surface is obtainable for every bundle-visible model via the
bundle lane; the opal7 guard stays honestly dirty; the refusal to land yaliu-platform bytes
under our platform key (which would false-green that guard) is the reason the close is
partial-by-design. **The yaliu-grant boundary CONSOLIDATES into ONE Andrew conversation**:
(a) the 1,066 no-UUID closed allocations (three independent measurements of the same wall:
roster status=closed → 0; feed-5 carries no accountId; direct allocation-detail 400s),
(b) the 4 Global model summaries, (c) feed-8 activity outside the 6,620. CTO carries it to
Andrew's list with these denominators.
