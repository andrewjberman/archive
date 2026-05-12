# DS Briefing — Cash Drag Artifact (Account-Level)

**Pipeline:** Inflection partner / Advisor Intelligence
**Artifact:** `platinum/firm/cash_drag.json` (under `opal-data-inf`)
**Consumer:** `InflectionInsightsPanel` → Cash Drag lens (`portal/src/pages/AdvisorIntelligence/_partners/inflection/InflectionInsightsPanel.tsx`)
**Status:** FE shipped (commits `073d9608` portal · `db4acad9` CLOUD). Panel empty-states with the message *"Account-level artifact pending DS rollout"* until this lands.

---

## 1. Summary

Restructure `cash_drag.json` from one-row-per-household with a 5% threshold filter to **one-row-per-account with no threshold filter** (every account, all the time). Add two new fields driving the FE's redesigned scatter view, and produce the artifact for each of four windows: `qtd`, `ytd`, `1y`, `max`.

---

## 2. Motivation

The FE redesign turns Cash Drag into a 2D account-level scatter:
- **Y = average cash balance** in the selected window (log scale, dollars)
- **X = days since the last meaningful trade** on the account
- Bubble size = avg cash. Color = percentile of regression residual.
- Every account is plotted — no upstream threshold filter.

Andrew's framing: cash drag is fundamentally a *neglect* signal. "Nobody touched this in N days" maps almost 1:1 to neglect. A self-relative persistence metric (over-engineered) was rejected in favor of the cleaner days-since-last-activity signal. See the design discussion (Option A vs B, picked A with the $1K refinement).

The old HH-level, threshold-gated rows can't serve this — we'd be filtering before the visualization that's supposed to *reveal* the distribution.

---

## 3. Current vs target state

**Current row** (HH-level, threshold-filtered upstream):
```json
{ "household_id": 449, "aua": 4720000, "cash_pct": 0.067, "cash_aua": 318000, "days_above_threshold": 75 }
```

**Target row** (account-level, every account):
```ts
interface InflectionCashDragRow {
  account_id:             string    // Orion account number (or Schwab CUSIP, whichever is canonical at IWM)
  household_id:           number    // parent HH key — must match the same household_id used in books/clients drill
  account_label?:         string    // human-readable: "Joint Roth IRA", "Charles Brokerage", etc. Optional.
  aua:                    number    // account-level AUA = positions + cash, latest snapshot
  avg_cash_balance:       number    // time-weighted avg cash over the WINDOW (definition §4.1)
  current_cash:           number    // latest snapshot cash balance — tooltip context, not used for scoring
  days_since_last_trade:  number    // days since most recent qualifying trade (definition §4.2)
}
```

The artifact is a flat array: `InflectionCashDragRow[]`. No threshold filter — every account with a non-null cash record appears regardless of cash level.

---

## 4. Definitions (the precise rules — read carefully)

### 4.1 `avg_cash_balance`

Time-weighted average of the account's cash balance over the window.

- If you have daily cash snapshots: `mean(daily_cash[start..end])`
- If you have only end-of-period snapshots: linearly interpolate between observations, then time-weight
- Cash includes money-market sweep balances and pending settlement cash
- Cash excludes positions in cash-equivalent funds that are explicitly held as investment (e.g., a deliberate SHY position is not "cash")

If the account didn't exist for the full window, time-weight only the live portion. Do **not** zero-pad pre-existence days.

### 4.2 `days_since_last_trade` — the $1,000 rule

Days between **the most recent qualifying trade** and the **window end date** (not "today"), capped at window length.

**A qualifying trade is:**
- A buy or sell of a security (equity, ETF, mutual fund, bond, option)
- Of absolute notional value **≥ $1,000**
- Recorded on this `account_id`

**Excluded** (these do **not** reset the clock):
- Automatic dividend reinvestment (DRIP)
- Cash sweep / money-market sweep activity
- Cash contributions (ACH deposits, journal entries) regardless of size
- Cash withdrawals
- Fee debits / management fee posts
- Corporate actions (splits, mergers, spin-offs) — not advisor-initiated
- Sub-$1,000 trades (small rebalance lots, fractional share auto-allocations)

If there has been **no qualifying trade** within the window, report `days_since_last_trade = <window length in days>`. Don't cap at 0, don't null. Treat "no qualifying trade ever" as "stale for the entire window."

The trade definition matters. Andrew's exact words: *"a $50/mo recurring deposit doesn't reset the clock on a clearly-ignored account"* — that's the corner case the $1K + qualifying-event filter is designed to catch.

### 4.3 `current_cash`

Latest end-of-day cash balance available in the source (Orion sync or wherever the snapshot lives). Same definition as `avg_cash_balance` for what counts as cash; just the latest observation rather than the window average.

### 4.4 `aua`

Account-level AUA at the latest snapshot. Positions market value + `current_cash`. If the household-level `aua` aggregation already does this per-account and rolls up, use that same per-account number.

---

## 5. Window semantics

Produce the artifact for **four windows**:

| Window | Definition |
|--------|------------|
| `qtd`  | Current calendar quarter, first day → latest data_as_of |
| `ytd`  | Current calendar year, Jan 1 → latest data_as_of |
| `1y`   | Trailing 365 days from data_as_of |
| `max`  | Earliest available data → data_as_of (account inception or feed start, whichever is later) |

`avg_cash_balance` and `days_since_last_trade` are both window-scoped. Same account will have four different values across the four windows.

Serving mechanism is your call — either:
- **(A)** One artifact file per window: `cash_drag_qtd.json`, `cash_drag_ytd.json`, `cash_drag_1y.json`, `cash_drag_max.json`. Router picks based on `?window=` query param. **(Recommended — cleaner CloudFront caching, smaller per-request payload.)**
- **(B)** One artifact with all windows in a nested object. FE would need a schema change to consume this; if you go this route, flag it and I'll update the FE.

The FE currently calls `getInflectionCashDrag(firmOverride, window)` and appends `?window=qtd` to the URL. Option A drops in with zero FE changes.

---

## 6. Acceptance criteria

- [ ] `cash_drag_{window}.json` published to `opal-data-inf/platinum/firm/` for all four windows
- [ ] Each row matches the TypeScript interface in §3 — schema validates
- [ ] Row count ≈ total Inflection account count (sanity check: should be 4 advisors × N accounts each, not 8 households)
- [ ] `days_since_last_trade` distribution looks plausible (some accounts at 0–7d, others at 90–365d, no all-clustering-at-window-length unless data is truly stale)
- [ ] At least one account exists with `days_since_last_trade < 7` (the $1K threshold isn't excluding *every* trade)
- [ ] At least one account exists with `days_since_last_trade > 90` (we're actually surfacing dormant accounts)
- [ ] `avg_cash_balance` is non-zero for accounts with non-zero current cash
- [ ] `comp-validate cash_drag` passes (add a config entry if needed)
- [ ] Spot-check: pick the highest `days_since_last_trade` account, verify the trade log manually shows no qualifying trade in the window. Verify the next-most-recent trade was ≥ $1K and the gap is what we computed.

---

## 7. Coordination notes

**FE is already shipped.** Panel goes from empty-state to live the moment the new artifact path returns a non-empty array of the new shape. Console sentinel will log `[INFLEC sentinel] cash_drag: row missing account_id (artifact may still be HH-level — DS TO pending)` if the old HH-shaped artifact is still being served.

**Drill navigation:** household IDs in each row must match the `clientKey` used in BooksTab's `handleClientClick` — same `household_id` that flows through every other artifact in the Inflection pipeline. Don't introduce a new ID space.

**Old artifact:** `days_above_threshold` and `cash_pct` are no longer consumed by the portal. Audit whether anything else reads them before deprecating. The cleanest move is probably:
1. Ship new schema under the same path (overwrites old)
2. Delete old fields after one cycle of confirming no other consumer is broken

---

## 8. Out of scope (don't expand the work)

- This briefing does **not** touch Activity Scan or Concentration Risk artifacts. They have their own forthcoming refactors but aren't part of this.
- This briefing does **not** require period-specific Activity Scan artifacts (Activity Scan FE has the window toggle wired but currently shows 12m data regardless — that's a separate DS TO).
- No new SLA/freshness commitments. Match whatever the current cash_drag refresh cadence is.
- No back-fill of historical windows. Just produce going forward from first publish.

---

**Open question for DS:**
Confirm the `account_id` source-of-truth. Orion account number, Schwab CUSIP, or an internal Opal account key? The portal's L4 (account modal) drill assumes a specific account ID format — needs to match.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*FE refactor commits: portal `073d9608` · CLOUD `db4acad9`*
