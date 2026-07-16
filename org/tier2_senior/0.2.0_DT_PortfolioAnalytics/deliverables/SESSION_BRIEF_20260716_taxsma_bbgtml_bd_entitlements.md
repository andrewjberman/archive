# SESSION BRIEF — 2026-07-16 (0.2.0_DT, Andrew-direct)
## Tax SMA pt2 · Bloomberg/BBGTML · Black Diamond table structure · MCP entitlements domain split

**For:** 1.0.0_SA_CTO — Andrew's instruction (verbatim intent): fold these into the relevant
project PRDs and TOs so the knowledge persists in the fabric rather than dying with this session.
**Relevant projects:** OPAL_TAXSMA (0.5.0~A delegate lane) · OPAL_BBGTML (0.2.0_DT) ·
OPAL_CONSOLIDATION/monolith (CTO) · SCTY_PREMCP/OPLMCP (gateway).
**Primary artifacts this session:** `.claude/skills/tax-pt2/SKILL.md` @ 77a523510 ·
`org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/opal_taxsma/ENTITLEMENTS_DOMAIN_SPLIT_SPEC.md`
@ ec13addee · this brief. Source materials: Yang call transcript 2026-07-16
("Dashboard Update and Tax SMA Reporting", Downloads) + BD HAR ("bd3.bdreporting.com (1).har").

---

## 1. OPAL_TAXSMA — step-2 is now buildable; /tax-pt2 commissioned (PRD update REQUIRED)

**The 07-14 ruling "step-2 cost basis stays manual / not derivable in-estate" rests on a premise
that is now FALSE.** S0.1's membership test covered `opal-data-schwab` (the 0824/CRS delivery)
only. The 0833 monolith feed (`s3://opal-data-assets/schwab/08335338/`, landed 07-14) carries
**all 3 live Tax SMA accounts** — verified 07-16 on number AND name axes with a positive-controlled
matcher: Chiles `0027265115`, Bump `0035940058`, Macy `0091939812` (fact_acc: status O, strategy
`Opal Tax SMA 200/145`, manager Opal Capital LLC, master 49 FINANCIAL).

- **THE FEED TRAP (persist this loudly):** Tax SMA unrealized lots ride **`fact_ult`, NOT
  `fact_uln`** (0 rows in ULN, 2,251 lots in ULT). Any consumer keyed on ULN reads zero rows and
  can pass silently — the /tax-pt2 skill carries a mandatory zero-lots FAIL-LOUD gate.
- **Fees in Schwab data (Andrew's net-of-fees requirement):** `fact_trn` (daily to 2024-07)
  carries MARGIN INTEREST (monthly, $3-7K/acct observed), SERVICE FEE (stock borrow, short side),
  and ADVISOR FEE debits as posted transactions. Fee SCHEDULES live in the BD daily pull
  (`blackdiamond/49f/bronze/fees_435407/`): Chiles = "49F - Flat 1" = 100bp flat on Total Value
  (schedules VARY — 0.9% rows exist; read per account, never assume).
- **/tax-pt2 skill v0.1 LIVE (Phase A, agent-run)** @ 77a523510: `/tax-pt2 {account}` → lot-level
  CostBasis CSV in the exact Schwab lot-level-export shape (pt3's pinned input contract, consumed
  unchanged) + fees/performance run report → `TAX/Tax Lot/{YYYYMMDD}/`. Andrew's three-step
  artifact-per-level design: pt1 intake (live) → pt2 assessment → pt3 FactSet conversion.
- **Scope addition from the Yang call:** a QUARTERLY per-client report (Q2 = Apr 8–Jun 30;
  template in SharePoint TAX reporting folder 2026 Q2): returns QTD/YTD/1Y/3Y/SI net of ALL fees
  (margin + advisory), realized ST/LT + unrealized ST/LT, top-10 holdings + sectors (Yang pre-pulls
  from FactSet), benchmark from Bloomberg (custom 49 benchmarks, BD ids 94554/90832-90834).
  Trade-start dates are in Yang's `Tax SMA Accounts.xlsx` (inception + latest-trade-date columns
  confirmed on the call) — the roster source to wire in.

## 2. Black Diamond — reporting mechanics grounded from the HAR (methodology facts to pin in the PRD)

From Manav's BD session for Chiles (`bd3.bdreporting.com`, endpoints under
`portfolioreporting/api/`): `performance/performancePeriod`, `performance/performanceSeries`,
`costBasis`, `transactions/star`, `benchmark`.

- **BD does NOT amortize advisory fees.** With `feeMethod: NetOfFees` the account-level window
  reported `fees: 0.0` (no advisory debit posted yet). BD's identity verifies to the cent:
  `netGains = EMV − BMV − netAdditions` (978,575.04 − 1,061,234.71 − 4,401.52 = −87,061.19).
  Consequence: a Schwab-computed posted-fees-only protocol can MATCH BD exactly; a schedule-based
  daily accrual is an overlay we can add that BD does not have — the two must stay separate,
  labeled columns (skill methodology pins 1/2).
- **`feesIn: NetAdditions` semantic:** when a fee posts, BD counts it in netAdditions (excluded
  from netGains). Must be mirrored or the first billed quarter will not reconcile.
- **BD Since-Inception anchors at FUNDING (Chiles 2026-03-16, ~$1,047,024.72 in-kind), not
  trade-start (04-08).** Trade-start is an explicit input, never BD's inception.
- **Reconciliation targets banked** (Chiles 04-08→06-30): TWR −8.2053%, MWR −8.2017%,
  netGains −87,061.19, income −6,566.11 (margin interest nets here).
- **Tax-SMA-specific:** transferred-in appreciated lots are normal (Chiles: ~$771K unrealized LT
  on ~$156K original 2005 basis) — old acquired_dates are correct, never "fixed".

## 3. New BD/monolith table structure — `dim_taxsma_costbasis` (gold leg for OPAL_CONSOLIDATION routing)

Andrew's design: a daily table covering **all 0833 clients**, produced in the existing bronze→
silver 0833 ETL chain, that /tax-pt2 (and Alyssa's narrow access) reads. Spec leg 4 @ ec13addee:
- **GOLD, not silver** (naming law: silver `fact_*` complete mirrors / gold `dim_*` projections /
  gold is the ONE parse-down point): `schwab/08335338/gold/dim_taxsma_costbasis/{date}/`.
- Columns: lot-level cost basis (fact_ult shape), posted-fee ledger aggregates (fact_trn),
  realized/unrealized ST-LT splits, daily MV, fee-schedule join from fees_435407.
- Producer gate: zero rows for a live Tax SMA account = FAIL (the ULT trap, moved upstream).
- All-0833 coverage = new Tax SMA clients onboard with zero code change.
- DS/monolith lane build; bd49f dims runner precedent (opal-assets-bd49f-dim-convert).

## 4. OPLMCP entitlements — domain partition (ms | aws), Andrew-direct architecture ruling

**Andrew (verbatim):** "we need to develop the entitlements layer so that theyre broken up by
domain. there are entitlements for ms (graphapi) already set up, we also need an entitlements
for AWS." Scoping rulings: nobody has AWS access except Andrew; alyssa@opalinvest.com gets one
narrow gateway-brokered path; the simplest shape = the dedicated daily table + scoped access +
`/tax-pt2 {account}`.

Grounded current state: `entitlements.py` is a Graph write-class gate per TIER (no per-email
dimension, no AWS awareness, no git anything). Spec @ ec13addee, 4 legs:
1. **Domain-partitioned entitlements.txt** (backwards compatible): legacy `tier class` lines =
   implicit ms; new `user:<email>|tier:<tier> <domain>:<class>` lines; fail-closed; master
   wildcard on read classes only (Andrew's implicit coverage).
2. **`taxsma` integration** (AuthKind.NONE, read-only, `taxsma_costbasis(account, asof)`), new
   IntegrationSpec field `entitlement:` — the reusable per-email narrow-grant mechanism.
3. **IAM:** gateway EC2 role read on exactly the dim_taxsma_costbasis prefix; 22a battery
   INCLUDING a negative control (out-of-prefix key must implicitDeny). First client-data S3
   capability on that box — the dedicated table is the blast-radius bound.
4. The gold table (§3).
**Sharp acceptance test:** a third standard-tier user must be DENIED — proves the per-email gate
discriminates within a tier. End-to-end: Phase-B numbers == Phase-A direct-S3 numbers, then
Phase A retires. Default held CLOSED pending Andrew: Alyssa's tool refuses non-Tax-SMA accounts.

## 5. OPAL_BBGTML — new facts from the Yang call (TO/PRD updates)

- **Bloomberg terminal login is username+password only — NO MFA** (Alyssa confirmed live).
- **Yang explicitly authorized scheduled automation** on the terminal laptop under Alyssa's
  login: once daily ~8:00 AM ET **± a random ±5 minutes** (his words — not 8:00 sharp, never
  more than once/day), downstream kicks ~8:10. This upgrades the B5 operator-run posture to a
  sanctioned scheduled-job design leg (Bloomberg-side lockout/relogin behavior still untested —
  Andrew flagged it needs a test).
- The manual pull+upload flow was exercised END-TO-END live on the call (Alyssa ran both
  notebooks, uploaded via the dashboard data-refresh, tables displayed as-of 07-15) — the process
  the .bat + opal_data_refresh_upload wrap is confirmed operator-runnable.
- Andrew described the double-click .bat consolidation on the call (built prior session); install
  target = the terminal machine.

## Routing asks (CTO)

1. OPAL_TAXSMA PRD: kill the "step-2 manual/not-derivable" premise (cite §1), add pt2 + the
   quarterly-report scope (§1-2 methodology pins), wire the roster source.
2. OPAL_CONSOLIDATION: route the dim_taxsma_costbasis gold leg (§3) to the DS/monolith lane.
3. SCTY_PREMCP/OPLMCP PRD: the domain-split architecture (§4) + arch-gate legs 1+3 (request
   already in your inbox, 192417Z).
4. OPAL_BBGTML TO: fold §5 (no-MFA fact, Yang's scheduled-automation authorization + jitter
   spec, the untested-relogin risk).
