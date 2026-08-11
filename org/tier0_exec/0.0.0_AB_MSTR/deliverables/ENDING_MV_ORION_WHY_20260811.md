# THE ORION-SIDE WHY — SOLVED: the Rolling-3-Year window is the whole mechanism

**Commissioned:** Andrew-direct at the MSTR terminal ~0905Z, VERBATIM: *"chase down the
orion-side why on those 259 accounts, egress granted, this is what COO discovered corroborating
your findings, I want to be able to have a brief and explanation for the Inflection team about
the nature of these numbers"* — egress used: 12 read-only Orion API calls (9 account-attribute
GETs + 1 firm roster GET + 2 re-pulls), zero writes, zero query creations.
**Author:** 0.0.0_AB_MSTR · extends `ENDING_MV_LONGITUDINAL_FINDINGS_20260811.md` · companion
draft: `DRAFT_INFLECTION_TEAM_BRIEF_ENDING_MV_20260811.md` (for Andrew's review/send).

## THE ANSWER

**`"Activity: Ending Market Value"` is Orion's Activity-engine `Activity.Value` path
(activityOptionId=1), and the Billing Dim extract runs it over a ROLLING 3-YEAR window
(`orion_billing_dim.py:62 DEFAULT_WINDOW="3y"` → Envision daterange `-3y+1d..0d`). Orion's
Activity engine returns EMPTY for any account whose `accountStartDate` is AFTER the window
start. Every "absent" account is simply an account opened in the last three years.**

## THE PROOF (three independent legs, all measured)

1. **Perfect firm-wide separation (roster GET, 3,169 accounts; start dates known 797/797 of
   the tested set):** ALL 312 absent-with-assets accounts started AFTER 2023-08-11 (min
   2023-09-11); ALL 485 populated accounts started ON/BEFORE 2023-08-04. **Zero exceptions in
   either direction.** (2023-08-11 = pull date − 3y, the window start.)
2. **The predictive longitudinal test:** accounts whose start+3y anniversary fell INSIDE the
   observed series (start dates 2023-04..2023-08) must flip absent→populated ON that
   anniversary. Observed: 27 such accounts transitioned; **22/27 first populated within ±1–3
   days of exactly start+3y** (mode −1 day = the `+1d` in the window expression); the other 5
   flipped during the April 27-day partition gap (first observable snapshot 04-28), consistent.
3. **Attribute probes (5 absent vs 3 populated accounts, full JSON):** absent accounts are
   reconciled, in-balance, active, managed — `lastReconciledEffectiveDate` current,
   `inBalance: true`. Nothing is wrong with them. The ONLY disjoint operational attribute was
   `accountStartDate`. Orion's Portfolio domain returns `currentValue` for every one of them
   (e.g. absent acct 1087: currentValue $2,738,157.63 — matching our positions feed).

## WHAT THIS MEANS

- **Nothing is wrong at Orion, and nothing is wrong with the accounts.** The extract asks a
  3-year-window activity question; the engine answers honestly (no data for accounts younger
  than the window); our parse then renders "no answer" as $0.00 and every sum silently drops
  those accounts.
- **The defect self-heals per-account, one account at a time, on each account's 3-year
  anniversary** — which is why the served numbers drift mysteriously upward (e.g. 27 accounts
  crossed during Apr–Aug alone) and why absence looked "persistent" in-window.
- **Why the money skews to the fee side:** the firm's growth since Aug 2023 — every account
  opened in the last 3 years is invisible to the extract, and those are overwhelmingly billed
  accounts ($59.56M of the $68.32M).
- **The correct raw figure exists vendor-side without the Activity engine at all:** the
  Portfolio-domain roster returns `currentValue` per account directly (our positions_mv feed
  already carries it, which is why populated emv matched it to the cent). Under the ratified
  raw-from-endpoint ethos, the fix candidates are: pull a window that predates the account
  base, use an inception-anchored option, or read the Portfolio-domain value raw — a P1
  design choice on the ratified forms (routed with CTO/COO; nothing changed tonight).

## SCOPE + AUDIT
Egress per Andrew's explicit grant, this work only; JWT read from the standing store (expires
17:07Z); all calls read-only GETs; no synthetic queries created; no data written to Orion.
Instrument note for the record: `orion_endpoint_probe.py get` caps its own output at 3,000
chars (`:3000` slice) — two truncated captures initially read as corrupt; the capped-stream
class, fourth sighting today. Worked around with a full-length scratchpad reader; tool fix is
its owner's (0.4.0_DS per the tool header).
