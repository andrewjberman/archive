# AMGT-pp-6 -- the act is applied; ONE served property moved that the signed outcome did not predict

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1`, `1.0.0_SA_CTO~DELL1` | **Date:** 2026-10-11 ~07:50Z
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-pp-6.redeploy-the-scoped-api-carrying-the-rounds-served-cells.md`
**Ledger:** `amgt-resapp-r91-pp6-scoped-api-dell1`, OPEN, L1-L8, L10, L11 closed, **L9 open on this finding**.
**State of the world:** APPLIED 2026-10-11T07:37:03Z. Live CodeSha256 `0Oy6BG/PXP2HFmQqq0VDSFeGbItvFPf3q2pGQLJ8mxE=`. Rollback kept.

## What passed

AC1 (4 of 4 members byte-equal to the pin, exit 0), AC2 (R89 PEERS DEPLOYED YES, R89 DEPLOYED CLOSE YES, exit 0) and AC3
(24 candidates, 24 served, 0 missing, 0 leaked, R91 NAME MATCH DEPLOYED YES, exit 0). Re-plan rc=0, one resource moved.

## What moved that the halves did not name

The COO half's EXPECTED OUTCOME says: "Currency: byte-equal to today unless pp-4 is in the pin." pp-4 is not in the pin.
The member-by-member compare of the live `/peers` response of all 243 subjects (2230 members, baseline read at
`l8egBo..` before the act) reads:

| | count |
|---|---|
| subjects compared / status moved / subject-level fields changed outside `members` | 243 / 0 / 0 |
| member-count changes | 0 |
| members changed | **24** (exactly the AC3 candidates) |
| changed fields on 23 of them | `identity`, `security_key`, `price_currency` |
| changed fields on 1 of them | `identity`, `security_key`, `price_currency_reason` |
| `matched_as` / `resolution` on all 24 | `company_name` / `MEASURED` |

The 23 now serve a currency where each served none: **GBp 12, EUR 6, SGD 3, CHF 2**. The 24th (member `B0744B` of subject `BZLFY_US_Equity`) serves no currency and a NEW reason, "this price is quoted on the
company's home exchange; the company record we hold is its United States listing". Every one of the 24 keeps `price_currency_claim` null, and
23 keep the STORED `price_currency_reason` text ("... not matched to a company record that states its trading currency"),
which now contradicts the served code.

## Why (read from the code, not guessed)

`scoped_amgt._with_price_currency` (AMGT-at-3, unchanged by this act) reads the currency from the member's own record
once the member has a key. pp-1 gave these 24 members a key, so the same decorator now finds one. Nothing in pp-6 edits
the currency path. The signed text treated currency as independent of identity; it is downstream of it.

**The shape is not new.** At the base, 156 members already serve a `price_currency` together with the stored reason text
and a null claim (5 more serve a currency with no reason): the MEASURED identities nn-2 and the numeric-ticker arm produce.
Base census of 2230 members: 1589 unresolved, no currency; 480 MEASURED, no currency; 156 MEASURED, currency + stored reason;
5 MEASURED, currency, no reason. So the 24 take the path the 156 already take.

## What this seat did and did not do

- Did NOT roll back. The deviation is a prediction error in the signed text; the served values are the held record's own
  CRNCY, and the shape matches 156 existing members. Rolling back would drop 24 correct identities for a stale-text defect
  the base already has.
- Did NOT flip the order to `complete`: the pair's expected outcome says currency does not move and it did, so the grade
  is yours. The three criteria PASS as written.
- The rollback stays ready: the kept `l8egBo/rf..` package (`LIVE_ROLLBACK_opal-amgt-scoped-api_l8egBo.zip`, sha256
  base64 equal to the prior live), one `safe-apply`, inside the pair's same hour (apply 07:37:03Z).

## The call

**Keep** (the CTO accepts the derived currency, and the stale reason text on these and the 156 becomes a cell), or
**roll back** now and re-cut pp-1 with the currency path guarded. This seat recommends KEEP; the contradiction between the
served code and the stored reason is a defect of the 156 as much as the 24, and it is round 92's to fix once.

Per-member before/after: `PP6_CHANGED_MEMBERS_20261011.json` (24 rows).
