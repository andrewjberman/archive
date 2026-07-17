# OPAL_TAXSMA -- tax-pt2 Scoped BD Table + Alyssa MCP-IAM: Current-State Assessment

**Author:** 0.2.0_DT_PortfolioAnalytics · 2026-07-17 · **archetype:** DIAGNOSE
**Scope of ask (Andrew-direct):** (1) establish that the bronze+silver ETL for the scoped Black
Diamond table is set up with a consistent process; (2) once validated, assess that entitlements +
IAM for Alyssa are set up so she can reach it through an AWS-specific entitlement layer on the OPAL
MCP EC2. Grounded against: the 2026-07-16 Yang call transcript, Manav's manual BD run (HAR
`bd3.bdreporting.com`), Andrew's 2026-07-17 corrections + Teams-to-Yang design note, and live estate.

## 0. The requirement, restated correctly

Quarterly Tax SMA report, one denormalized row-set **per account keyed off account number** (no
joins), for the 3 live accounts (Chiles 0027265115, Bump 0035940058, Macy 0091939812; grows fast).
Four data classes (Yang): **return net of all fees**, **realized/unrealized cap gain-loss (ST/LT,
for the period)**, **top-10 holdings**, **sector allocation**; plus BMV/EMV, contributions, benchmark.

**Two Andrew corrections that reshape the design (do not lose):**
- **Schwab HAS the fee/tax data.** Yang's "Schwab can't provide performance" is false (he does not
  know how Schwab works). The real unknown is fee-TIMING (amortized vs quarter-end vs year-end). BD
  is a **DEFENSIVE** choice, not a necessity -- very likely derivable from Schwab + a fee convention
  (secondary path, real, not a dead end). See `memory/project_taxsma_schwab_has_fee_data_bd_is_defensive_not_necessary.md`.
- **Design law for the table:** "very few fields, very anonymized" -- account NUMBER only, strip
  client PII; the credential lives on a perpetually-on office computer, so IAM must be tightly scoped.

## 1. Field spec (from the HAR -- what the manual process actually pulls)

BD `portfolioreporting/api/*` for Chiles (BD acct 22596361 / ext z0822596361 / Schwab XXXX5115), Q2
04-08..06-30, dataAsOf 07-15. These reconcile to the cent with the tax-pt2 skill's banked targets:

| Class | Endpoint | Key fields (Chiles Q2) |
|---|---|---|
| Performance (net of fees) | `performance/performancePeriod` | BMV 1,061,234.71 / EMV 978,575.04 / netGains -87,061.19 / netAdditions 4,401.52 / fees 0.0 / income -6,566.11 / TWR -8.2053% / MWR -8.2017% / 4 benchmark returns |
| Cap gains (tax) | `costBasis` | realizedShortTerm -61,933.73 (gain 18,376.01 / loss -80,309.74) · realizedLongTerm 0.0 · unrealizedShortTerm 50,840.31 · unrealizedLongTerm 771,349.59 · marketValue 978,575.04 · accrual 218.85 |
| Positioning | `allocation` + holdings | top-10 by portfolio weight |
| Sectors | `allocation` | sector weights |

**Load-bearing observation:** every `costBasis` field (realized/unrealized ST/LT) is the SAME tax
data already in **Schwab silver** (`fact_ult` unrealized lots, `fact_rld` realized). The ONLY field
class that is genuinely BD-only is the **net-of-fees return** (performancePeriod).

## 2. PHASE 1 -- bronze/silver ETL state

| Layer | Producer | State | Verdict |
|---|---|---|---|
| BD bronze (fees/alloc/roster) | `opal-assets-bd49f-daily-pull` (EventBridge 02:30Z + 04:30Z reattempt) | 3 feeds current to 2026-07-16 | **CONSISTENT / mature** |
| BD silver dims | `opal-assets-bd49f-dim-convert` (Scheduler 03:05Z) -> `dim_advisor_fee_role` + `dim_account_xref` | CURED today (yang... opal-assets-v0.26.0); 07-14/15 were hand-runs, 07-16 my backfill; **first unattended fire 07-18 03:05Z** | **EXISTS, not yet PROVEN consistent** |
| Schwab tax silver | schwab-silver-sweep (daily ~12:15 UTC) -> `fact_ult`/`fact_trn`/`fact_rld`/`fact_acc` @ `schwab/08335338` | current to 2026-07-16 | **CONSISTENT / mature** |

**Two real gaps:**
- **G1 -- the scoped table does not exist.** `s3://opal-data-assets/blackdiamond/49f/` has only
  `bronze` + `silver`(the two dims) + `meta`/`_ops`; there is NO per-account Tax SMA table anywhere in
  opal-data-assets. The denormalized, anonymized, account-keyed table is the thing to BUILD.
- **G2 -- no BD performance feed.** The BD pull carries only `allocation_390224` + `fees_435407` +
  `template_roster`. `performancePeriod` (net-of-fees return, TWR/MWR/BMV/EMV) is **not pulled by any
  pipeline**. The BD silver dims (advisor/fee-role, xref) feed the **49F gold runner** (`a00_runner.py`),
  NOT tax-pt2; tax-pt2 today reads bronze `fees_435407` xlsx + Schwab silver directly.

**=> DECISION 1 (Andrew):** source the scoped table's RETURN from (a) a new minimal BD performance
pull, or (b) derive net-of-fees from Schwab silver + an explicit fee-timing convention (his preferred
secondary; Schwab has the data). Everything else (cap gains, positions, sectors, MV) is buildable from
Schwab silver today. **DECISION 2:** confirm anonymization = Schwab account number as the key, names
stripped.

## 3. PHASE 2 -- Alyssa entitlement + IAM via the MCP EC2 gateway

**Target architecture (Andrew-direct 2026-07-17):** per-employee scoped IAM ROLES; the gateway's
AWS-surface entitlement file = `email -> scoped-IAM-role-ARN(s)`; on a data-read from a
signature-verified email, the gateway STS-assumes that employee's role and reads S3 under it (the
role's policy is the boundary; the file just declares the mapping).

**Current state (live):**
- Gateway role `m365-mcp-gateway-role`: `AmazonSSMManagedInstanceCore` + inline
  audit-lake-write (`opal-mcp-audit/audit/*`) + go-live (own artifact prefix + m365/portal/ycharts
  secrets). **ZERO opal-data-assets reach** -- clean slate, consistent with "no other bucket access."
- Gateway entitlement framework (`app/entitlements.py`, `tier.py`, `identity.py`, `guard.py`,
  `token_broker.py`) is mature but **WRITE-scope-per-tier only** -- there is **no data-READ dimension,
  no per-employee-ARN map, and no S3/tax data tool** (integrations = `ycharts` + `opal_portal` upload).
- Alyssa = `WRITE_CAPABLE` + added to the portal data-refresh role (upload/rollback). That is the
  WRITE/refresh path, **not** the tax-pt2 READ path.

**=> Phase-2 verdict: NOT set up.** The identity/verification substrate exists and is solid, but the
entire read path is net-new: (i) a per-employee scoped IAM role for Alyssa (read-only, exactly the
scoped-table prefix); (ii) a trust policy letting the gateway role assume it + `sts:AssumeRole` on the
gateway side; (iii) the `email -> ARN` AWS-surface entitlements file wired into `entitlements.py`;
(iv) a gateway data-read tool/integration that assumes-then-reads; (v) Alyssa's skill over MCP.

## 4. Bottom line

- **Phase 1:** the INPUT pipelines are largely consistent (BD bronze + Schwab silver mature; BD silver
  dims cured today, scheduled reliability proves out 07-18). The **scoped table itself is not built**,
  and there is **no BD performance feed** -- so Phase 1 is NOT yet "done," it is "inputs ready, table +
  return-sourcing decision outstanding."
- **Phase 2:** entitlement/IAM for Alyssa is **NOT set up**; the target per-employee-scoped-IAM +
  email->ARN model is clean and the gateway is a clean slate, but every read-path component is net-new.
- **Blocked on:** Decision 1 (BD-pull vs Schwab-derive for the return) + Decision 2 (anonymization key)
  before building the scoped table; then the Phase-2 read path.
