# INTAKE -- a second peer group for ETFS_RIVALS: IDVZ (Andrew-direct 2026-09-30 ~14:5xZ)

**Recorded by:** `2.0.0_SA_COO~RV`, for `4.0.0_SA_CRO~Z`'s L1 brief. This is not a cut: round 1 is mid-flight and its spec and
decomposition are frozen. The scope enters through the brief, then L2 and L4 (`1.0.0_SA_CTO~Z`).

## The ask

**Source:** an email from Adam Muller (Adam@opalinvest.com) to Andrew, "right comp funds for IDVZ", received 2026-09-29 23:19Z:

> I think the right comp funds for IDVZ are: IDVZ, TXUE, BIDD, CGIC, INEQ, SCHY

- Every rival built so far is in **PFOE**'s peer group; round 1's thread is BASG. The new set is **IDVZ**'s peer group.
  IDVZ is Opal's own fund, listed first.
- **Andrew-direct:** *"Flat is honestly fine, we'll just have a lambda control the grouping for the output sake, no need to
  [change] the bucketing structure unless its early enough that it is of no consequence to do so."*

## Storage stays flat -- measured, not assumed

**Live layout** under `s3://opal-data-etfs`, read 2026-09-30 ~14:5xZ, every key over every page:
- `issuer-site/etfs/{bronze,silver}/holdings/date=<D>/`
- `rivalfunds/etfs/{gold/canonical_shape,gold/trade_schedule,platinum/page,state/<stage>}/date=<D>/`

The fund is a column (`fund_ticker`), and the partition is the date only. PRD v0.2 names neither PFOE nor IDVZ.

**It is NOT early enough to re-bucket at no consequence:**
- The prefixes are applied.
- Five Lambda role policies and the gateway read policy are scoped to them.
- The bucket notification and three EventBridge rules key on the state prefixes.
- About 1,600 objects are already served (325 raw + 325 sidecars, 325 silver, 325 canonical_shape, 324 trade_schedule, the
  page and the markers).

So the grouping is an OUTPUT concern, per Andrew.

## What the brief should carry (the COO's recommendation)

1. **The peer-group dimension as DATA.** A universe registry maps each rival ticker to the Opal fund it rivals (`PFOE` or
   `IDVZ`), carried into gold as a field (e.g. `opal_fund`). No new prefix.
2. **The grouping in the page Lambda.** The publish-page stage renders one section, or one page, per Opal fund. Storage stays
   flat; only rendering changes.
3. **An issuer adapter per new ticker**, the way round 1 built `adapters/basg.py`. Round 1's reachability test (RIV-r-1,
   from AWS) is the first test per issuer site. Each issuer's file format and publication date differ, so the CRO's digging
   should name each issuer's holdings URL and format.
4. **IDVZ itself is in the list.** Opal's own fund probably wants its holdings from Opal's own records, not an issuer scrape.
   That is for the brief to settle.
