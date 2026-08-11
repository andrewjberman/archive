# BRIEF — Inflection ADVI: the billing discrepancy, and why the pipeline freeze must not be lifted yet

**Author:** 4.0.0_SA_CRO · **2026-08-11** · **For:** Andrew; CC CTO~A (non-MDPF lane), COO (hold owner), CVO
**Trigger:** Patrick Scanlan (Inflection) → Joe Brandenburg → Yang Liu → Andrew, 2026-08-10. Andrew
assigned the dig to this seat and ordered Phase 0 of an unstick spec run.
**Status:** the BILLING question is answered. **PHASE 0 IS INCOMPLETE — one decisive check remains
UNMEASURED, and it is the check that gates any unstick.** Stopped at Andrew's instruction.

---

## 1. THE ANSWER TO THE PARTNER'S QUESTION

**Yang asked for "the tag behind the billing field." It is:**

```
is_fee_earning = (fee_schedule_name != "0 Fee Schedule Names") AND (fee_amount > 0)
```

`data/inf/scripts/silver/build_billing_dim.py:85`, built from the **Orion Billing export**
(Fee Schedule Name · Billing Amount · Billing Ending Market Value · Billing Period Start/End), with rep
attribution joined via the tax-unrealized dim. That is also Joe's answer: the unbilled number pulls from
Orion **Billing**, not from positions or performance.

**But the displayed figure is not that tag.** MEASURED at
`data/inf/scripts/gold/INF_D_04.client_portal_summary.py:763`:

```
fee_earning_aua     = SUM(billing.ending_mv WHERE is_fee_earning)   <- Orion Billing
non_fee_earning_aua = total_aua - fee_earning_aua                   <- RESIDUAL
                      ^^^^^^^^^ canonical_holdings (a DIFFERENT source, date, population)
```

**Non-Fee AUM is a subtraction, not a classification.** Anything in AUA that fails to match a fee-earning
billing row lands in it — a genuinely unbilled account and a bookkeeping artifact are indistinguishable
**by construction**. This is also the mechanical reason Patrick cannot drill in: there is no list, only a
difference.

### Patrick's real numbers (MEASURED, billing dim snapshot_date=2026-08-10)

| | |
|---|---|
| Displayed on his Profile tab (2026-07-31 build) | ~$606,000 |
| **Actually classified non-fee** | **$127,961.76 across 16 accounts** |
| **Residual — not accounts** | **~$478,000** |

Composition of his 16, independently corroborated by two separate agent runs that agree to the cent:
**three funded** (636-649046 $67,058.80 · 636-648986 $53,296.23 — both household 402 · 618-720647
$7,606.73) and **thirteen zero-balance shells**. All sixteen sit on the `"0 Fee Schedule Names"` schedule
— deliberately non-billing, not accounts that fell out of billing.

### What fills the ~$478K residual (all MEASURED unless marked)

- **3 accounts in his ADVI book have no billing row at all** (159 ADVI accounts, 156 matched).
- **Two different definitions of "Patrick's book."** ADVI aggregates by `advisor_key`, billing by
  `rep_id`, and they disagree: 6 of his 159 ADVI accounts bill under other reps (5 Peter Lee, 1 firm);
  his billing book holds 171 accounts to ADVI's 159.
- **`ending_mv` is the billing period-end value; `total_aua` is current holdings** — drift between those
  dates lands in Non-Fee permanently. *(INFERRED from the field definitions; not sized.)*
- **The 10-day freeze** compounding all of the above at a stale vintage.

### Was there a real billing gap? NO EVIDENCE FOUND — and it was tested for

Firm-wide the billing dim carries 907 accounts / 118 non-fee / $3,608,248.62. Exactly **two** accounts
firm-wide carry a live fee schedule with a non-positive fee — **both dismissed on measurement: zero
balance, negative fee amounts, i.e. closed-account fee reversals.** A null-coalescing defect
(`fee.fillna(0)`) was my first hypothesis and the data **refuted** it: zero NULL fee_amounts exist.

**Verdict for the partner: the display is misleading; the billing is not.** The one place a real gap
could still hide is the 3 ADVI accounts with no billing row at all — named for follow-up, not yet
resolved.

---

## 2. THE FREEZE IS NOT A BUG. IT IS A DELIBERATE HOLD, AND IT IS LOAD-BEARING.

Andrew's suspicion was correct that ADVI is frozen, and the measurement localizes it precisely:

```
inf_gold_accounts_dimension    2026-08-10 14:08Z    11.5h   PASS
inf_gold_positions_cube        2026-08-10 14:09Z    11.5h   PASS
inf_gold_canonical_holdings    2026-08-01 14:54Z   226.7h   FAIL   <- THE GATE (INF_B_00)
inf_gold_client_performance    2026-08-01 14:54Z   226.7h   FAIL
inf_gold_employee_leaderboard  2026-07-31 14:52Z   250.8h   FAIL
inf_platinum_dashboard         2026-07-31 14:53Z   250.7h   WARN   aua 8 trading days behind
```

The dimension/lots/positions chain runs daily. `gold/canonical/` — described in its own note as *"the
gate for the entire C+ and D+ chains"* — stopped, and everything downstream stopped with it.
**The vendor feed is healthy** (Orion bronze newest 2026-08-10 14:15:55Z; billing silver written daily
through 08-10). This is downstream of ingest, at one gate.

**Why it stopped:** all three EventBridge rules targeting `inf-gold-trigger` are DISABLED, two of them
explicitly *"DISABLED 2026-07-13 under the INF gold dispatch hold (b7bce51bd)."*

### The hold's reason — and it names this same advisor's money

COO, 2026-07-13, per-row census over 1,410 partitions: **running a full gold rebuild would DELETE
$453,179.39 of attribution from the served spine.** Nine accounts have **zero rows in silver**; they
survive in gold only because nothing has re-derived their partitions. A re-derive does not misattribute
them — **it produces no row at all.** The at-risk set includes **Peter Lee's $368,965.68 and Patrick
Scanlan's other $84,213.71.**

And the reconciliation cannot see it: *"a deleted row leaves the ADVISOR side and the FIRM side AT THE
SAME INSTANT, so sum(advisors)==firm_total stays true forever."*

> **"INF being stalled is the only thing currently holding this line, and a stall is not a control."**

⛔ **CONSEQUENCE FOR THE ORIGINAL PLAN:** fixing the ADVI freeze "in the same sweep" as the billing
question — executed directly — would have destroyed $453K of attribution **including $84K belonging to
the advisor who raised the ticket.**

---

## 3. PHASE 0 — WHAT IT ESTABLISHED, AND THE ONE CHECK IT DID NOT REACH

The hold's lift conditions are explicit: **`INF_GOLD_DISPATCH_RELEASE` + CTO/COO co-sign, gated on the
coverage guard LIVE AND EXERCISED ON THE RUNNER + the `INF_B_00` selector fix** — with the doc's own
warning: ***"Deploying code is not running it… a guard in the code bucket that nothing calls is a comment
with parentheses."***

### Both of my first precondition checks were the WRONG TEST, and I caught both

| Check I ran | Why it does not establish the condition |
|---|---|
| rep_id NULLs in silver: **0 of 1,407,740** on the 08-10 partition | The hold's risk is **ABSENT ROWS**, not null values. A NULL-count structurally cannot see a row that does not exist. This result is real and **does not** show the 9 accounts are back. |
| F7 coverage detector **exists in source** (`aor_attribution_audit.py:59` — *"coverage_drop (F7, round-8.2) is the RE-ESTABLISHED per-account coverage detector"*) | The condition is **live and exercised on the runner**. Source presence is a DESIRED-state read; the hold explicitly rejects it. |

### What the deployed state does show (MEASURED, `s3://opal-data-inf/code/gold/`)

```
INF_B_00.canonical_holdings.py   2026-08-05 17:39:03   47,199 B   <- deployed AFTER the freeze began
INF_C_01.canonical_nna.py        2026-07-13 14:59:33   47,510 B   <- deployed AFTER the 11:38Z hold
lib/nna_coverage_guard.py        2026-07-13 08:48:15   26,438 B
lib/aor_resolution.py            2026-07-13 12:02:28   92,291 B
```

The repo's `INF_C_01.canonical_nna.py:105` **does** carry `from nna_coverage_guard import (...)`, and the
deployed C_01 was pushed at 14:59Z — *after* both the guard (08:48Z) and the hold (11:38Z). That ordering
is **consistent with** the guard having been wired since, which matches the hold doc's own line: *"the
code lands today; the serve waits on the guard."*

### ⛔ THE DECISIVE CHECK, STILL UNMEASURED

**Does the DEPLOYED `INF_C_01.canonical_nna.py` actually call the coverage guard, and has it ever been
exercised on the runner?** I was mid-fetch of the deployed artifact when work stopped. Everything else in
Phase 0 is inconclusive without it:

1. **Deployed-artifact call check** — fetch `code/gold/INF_C_01.canonical_nna.py` and confirm the guard
   import *and a call site*, not just the import.
2. **Presence test for the 9 at-risk accounts in current silver** — by account_id, testing presence, not
   nullity. *(Account IDs are in the hold's census; the doc names 560/703/1225 for the rep_id-NULL trio
   and shows the SURVIVOR(9) row set.)*
3. **Single-date dry-run** of the canonical rebuild into a scratch prefix, diffing account coverage
   against the live spine — which is precisely what F7 was rebuilt to detect. **Release only if the 9 are
   present and coverage does not drop.**

---

## 4. RECOMMENDATION

**Do not lift the hold on anything established so far.** Two of the three lift conditions remain
unverified at the layer the hold requires, and the one instrument that would verify them (the F7
coverage guard, exercised on a real dry-run) has not been run.

**The billing answer does not wait on any of this.** It can go to Yang and Joe now: the tag, the residual
mechanism, Patrick's true $127,961.76 across 16 accounts (3 funded / 13 shells), and the honest statement
that no billing gap was found. That answer is complete and independently corroborated.

**The two fixes are independent and should not be bundled:**
- **The display fix** (stop computing Non-Fee as a residual; reconcile the `advisor_key` vs `rep_id`
  book definitions) touches no held path and can proceed on its own.
- **The unstick** belongs to COO (hold owner) and CTO on the mechanism, gated on Phase 0 completing.

**Ownership, stated plainly:** the hold is not mine to lift, and this brief does not propose lifting it.
It reports what is measured, names what is not, and hands the release decision back to the seats that
own it.

---

## 5. INSTRUMENT NOTE — three of my own hypotheses died on measurement

Recorded because the pattern is the point: the null-coalescing defect (refuted by zero NULLs), the two
suspect unbilled accounts (refuted — closed-account fee reversals), and **both** precondition checks
(wrong tests, caught before they were reported as clean). Client account numbers are masked by Orion at
the API boundary; no client data is committed to this repo.
