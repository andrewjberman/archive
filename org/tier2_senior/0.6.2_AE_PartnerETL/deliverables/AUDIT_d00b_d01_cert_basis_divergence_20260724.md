# AUDIT — D_00b / D_01 degenerate-cert coverage: they do not carry D_00's cliff, they carry something LIVE

**For:** `1.0.0_SA_CTO` (audit authorized 20260724T135247Z — read-only, report-do-not-fix).
**By:** `0.6.2_AE_PartnerETL~A`, 2026-07-24 ~1400Z. **Scope:** read-only. Nothing changed, nothing deployed.
**Verdict:** **NOT CLEAN.** Neither script carries the 08-01 cliff — because **neither carries a hold at all.**
The result is a **live** cross-artifact basis divergence of **−$187,425,395.30 / −9.97%** on a client-facing
number, present in today's served artifacts.

---

## 1. Method (stated, per the gate condition)

Two independent axes, not one:

1. **Source** — read every `cert` use site in both scripts: `D_00b:824-835` + `_load_aua_certification:1235-1244`;
   `D_01:2433-2442` + `_load_aua_certification:375-391`.
2. **Exercised on the SERVED artifacts** — pulled and parsed the three live platinum objects, not the source's
   intent and not a self-report. All three carry the **same `data_as_of` (2026-07-22)** and were generated
   within ~5 minutes of each other on the **same nightly run**, so this is one run's output disagreeing with
   itself — not a vintage artifact.

| artifact | producer | `generated_at` | value |
|---|---|---|---|
| `platinum/firm/header_metrics.json` → `total.aua` | D_00 | 2026-07-24T04:44:26Z | **1,879,986,733.13** |
| `platinum/firm/timeseries_chart.json` → `aua.{quarterly,monthly}` last bucket `NMNC+NMEC` | D_00b | 2026-07-24T04:49:48Z | **1,692,561,337.83** |
| `platinum/firm/partner_analytics_quarterly.json` → `views.{aua,adv,ofc}.current.donut.total` | D_01 | 2026-07-24T04:47:06Z | **1,692,561,337.83** |

**Δ = −187,425,395.30 (−9.97%).**

> ### AMENDMENT 2026-07-24 ~1442Z — the Δ is TWO STACKED EFFECTS, and "D_00b/D_01 are on the gold basis" (below) is IMPRECISE
>
> Chasing this audit's own §4 residual produced a correction to the audit. **The headline stands** — three
> artifacts, one run, −187,425,395.30 / −9.97%, invisible. **The decomposition changes.** There are **three**
> quantities, not two:
>
> | | value | what it is |
> |---|---|---|
> | (1) | 1,879,986,733.13 | held 07-17 `certified_aua` — D_00 headline + site-2 pct denominator |
> | (2) | 1,780,856,838.03 | `gold_aua` — **the 07-17 cert's own recorded field** |
> | (3) | 1,692,561,337.83 | **the GAINS/TAX frame** — D_00b buckets, D_01 donuts, *and* the tax rows |
>
> ```
> (1)->(2)  -99,129,895.10  = -5.27%   BASIS effect  (held cert vs gold)
> (2)->(3)  -88,295,500.20  = -4.96%   FRAME effect
> combined  1,692,561,337.83 / 1,879,986,733.13 = 90.03%
> ```
>
> Three independent code paths produce (3) to the cent, so it is a coherent quantity, not a coincidence.
> **Consequence for the remedy in §5:** a shared resolver closes the **−5.27% only** and leaves the −4.96%
> entirely untouched. Scoping it as "the fix for the −9.97%" would be half true.
>
> **The frame effect, source-confirmed — this closes §4's second residual with a mechanism:**
> `C_02.client_performance.py:135-196` (`load_tax_status_split`) does **not** partition `total_aua`. It sums
> `aua_current` over the 03c `CANONICAL_ACCOUNT_GAINS` partitions, joins `accounts_dimension` for
> `tax_status`/`relationship_id`, then **filters**: `gains = gains[gains['relationship_id'].notna()]` (`:175`),
> against an `acct_lookup` already reduced by `drop_duplicates('account_id')` (`:150`). `total_aua` comes from
> the client-performance frame. **The two were never expected to reconcile — no basis ruling can make them
> agree.** Two loss paths are visible at source (accounts absent from `accounts_dimension` dropped by the
> `notna` filter; accounts in the perf frame with no 03c gains row never entering a bucket); **mechanism
> identified, magnitude NOT attributed between them** — that needs measurement I have not done.
>
> **Still un-reground, flagged not claimed:** (2) is the cert's **frozen 07-17** `gold_aua`. DS reported
> today's live `perf_latest['total_aua'].sum()` as the same figure *to the cent*. That is either a live sum that
> genuinely has not moved (plausible — the allocations feed stalled after 07-17) or an inherited number. **Not
> established; do not cite (2) as "today's gold total" on this document's authority.**

---

## 2. What they actually do

Both use a **truthiness-only** check and have **no BRANCH-A floor and no last-good lookback**:

```
D_00b:824   if cert:                       # a dict with certified_aua == 0 is TRUTHY
D_00b:832       scale = cert['certified_aua'] / gold_total
D_00b:833-834   last['NMNC'] *= scale ; last['NMEC'] *= scale

D_01:2435   if cert and is_current_period:
D_01:2436       certified = cert['certified_aua']
D_01:2437-40    views['aua'|'geo'|'adv'|'ofc'][period]['donut']['total'] = round(certified, 2)
```

Neither routes through `_resolve_served_aua`. Neither has `DEGENERATE_CERT_MODE`, `_last_good_certified_aua`,
or any hold. **`_load_aua_certification` returns `None` on absence, and `None` silently means "use gold."**

### 2.1 Why the divergence is live today

`_load_aua_certification` keys on **today's** date. The newest cert is `2026-07-17.json`; there is no cert for
2026-07-24. So on today's run:

- **D_00**: cert `None` → `_resolve_served_aua` → `DEGENERATE_CERT_MODE='hold'` → `_last_good_certified_aua`
  finds 07-17 within its 14-day window → serves **the held cert**.
- **D_00b / D_01**: cert `None` → `if cert:` is **False** → no override → serve **gold**.

**The same absent cert routes to two different bases in the same nightly.** D_00's hold is doing exactly what it
was designed to do; the other two have nothing to do it with.

### 2.2 The latent second failure — currently masked by C_02

`if cert:` is truthiness, not `> 0`. A cert whose `certified_aua == 0` is a **non-empty dict and therefore
TRUTHY**, which would drive `scale = 0` in D_00b (zeroing the latest AUA buckets) and set all four D_01 donut
totals to `0`. **This is latent, not active** — `C_02:309-332`'s BRANCH-A floor SKIPs writing a degenerate cert,
so no such file exists to be read. But the protection lives in a *different script*, and D_00's own comment
(`:246-249`) names this exact outcome as the thing to never permit: *"Serving display_aua=0 would silent-wrong
the firm AUA (worse than a stale value)."* **D_00 was hardened against it; D_00b and D_01 were not — they are
protected only by an upstream producer's discipline.**

---

## 3. Verdict against the three outcomes CTO asked for

> *"Establish whether each carries the same degenerate path, a different one, or none."*

**A DIFFERENT ONE — and the difference is not in our favour.** D_00's cliff is an 8-day-away **future** basis
flip on one artifact. D_00b/D_01 have **already** flipped, quietly, and have been on the gold basis since the
first day without a cert. The cliff I was sent to design against is, in these two scripts, **already the status
quo** — and it produced a ~10% disagreement that no instrument reports, because each artifact is internally
consistent and freshness-GREEN.

**This is the scope-coverage class again, one level up:** the BRANCH-A hardening was written at the scope of
*one script's resolver*, and the estate serves the same quantity from *three* producers.

---

## 4. What I am NOT doing / NOT claiming

- **No fix.** Report-only per the authorization. Any repair is a separate design at a separate gate, and it must
  **not** be folded into DS's D_00 limb.
- **I am not asserting which basis is correct.** That is a business call. This audit establishes only that
  **three client-facing artifacts disagree by ~10% while presenting the same quantity**, and that the
  disagreement is invisible.
- **Unexplained residual, flagged not explained:** `views.geo.current.donut.total = 1,691,386,392.56` — a
  **fourth** distinct value, ~$1.17mm below its sibling views. I did not characterize it; it may well predate
  all of this. Naming it so it is not silently absorbed into the −9.97% headline.
- **Coverage bound of THIS audit:** the three producers above and the `cert` path only. I did not audit any
  other consumer of `certified_aua`, and I am not claiming these three are the whole surface — that is the exact
  claim this audit exists because someone else made.

---

## 5. Recommendation (CTO routes)

1. **Do not widen the D_00 limb.** Ship it as designed; it is correct and independently valuable.
2. **Open a separate item for cross-producer basis coherence.** The right shape is almost certainly the one
   already gated for D_00: a **single shared resolver** that returns value + `basis`, used by all three
   producers, so the basis is decided once and *carried* rather than re-derived three ways. The `aua_provenance`
   block then makes any future divergence visible in the artifact instead of requiring an audit to find.
3. **Harden the truthiness checks regardless** (`if cert:` → an explicit `certified_aua > 0` test) — cheap, and
   it removes the latent zeroing path without depending on C_02 continuing to behave.

**Runway note:** unlike the 08-01 cliff, this one has no runway — it is live now.
