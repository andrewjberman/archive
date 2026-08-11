# ending_mv LONGITUDINAL FINDINGS — the basis question, measured

**Commissioned:** Andrew-direct ~0840Z (brief: `org/tier1_exec/2.0.0_SA_COO/deliverables/BRIEF_ENDING_MV_LONGITUDINAL_INVESTIGATION_20260811.md`);
run-down assigned to MSTR Andrew-direct ~0846Z ("please run this down").
**Author:** 0.0.0_AB_MSTR · read-only over at-rest S3 copies · zero egress used.
**Companion:** `ENDING_MV_LONGITUDINAL_PROOF_OF_SPEC_20260811.json` (schema-valid instance, the
canonized deliverable form). Analysis scripts: scratchpad `mv_invest/` (session-local, not committed).

---

## 1 · THE HEADLINE, PLAIN ENGLISH

**The five hypotheses collapse into one measured fact nobody had:**

> **Wherever Orion delivers a value, `ending_mv` equals current AUA TO THE CENT — 485 of 485
> populated accounts, max difference $0.00, firm-wide, on the same day.** `"Activity: Ending
> Market Value"` in this feed is NOT a stale period-end figure. It is a same-day running market
> value. **There is no second valuation basis in this data.**
>
> **The entire $68.3M "unreconciled" gap — and all of Patrick's $568K — is accounts where Orion
> returns an EMPTY field that our parse coerces to $0.00.** The display question was never
> "current AUA vs period-end AUA." Measured, it is **"current AUA" vs "current AUA with 39% of
> asset-holding accounts silently dropped."**

## 2 · ANSWERS TO THE BRIEF'S §8, IN ORDER

### 2a. The measured cadence (with its denominator)
- Inflection's billing feed **begins 2026-04-01**. The 2025 month-end partitions and the
  2026-01..03 partitions exist but hold **0 Inflection rows** (pre-onboarding; the builder's
  INFGRD filter yields empty). The brief's "102 partitions dated 2026" counts directories;
  **nonempty = 97**, covering 2026-04-01..08-11 (132 elapsed days, 73.5% day-coverage; gaps:
  90×1d, 3×2d, 1×4d, 1×5d).
- **Consequence: the requested ≥6-month window with two closed quarterly boundaries DOES NOT
  EXIST for this firm.** 4.4 months is the whole history. Positions (the AUA side) is
  complete-daily: 223/223 days of 2026.
- Bronze (`Billing Cycle`) says the billing cadence itself is **Quarterly** (791/907 rows;
  current period end 9/30/2026); the cycle metadata never reaches silver (see §4).

### 2b. Per-account classification (counts, not a verdict)
On 2026-08-11, 907 silver billing rows; universe joined to active positions:

| class | n | dollars (current AUA) | longitudinal signature |
|---|---|---|---|
| **POPULATED — no defect** | 485 | — | `ending_mv` == current AUA **to the cent, 485/485**; values move near-daily (70-84 accounts step per snapshot) |
| **ABSENT, in-cycle, FEE-EARNING** | 259 | **$59,563,723.65** | vendor emv EMPTY every snapshot since 04-01 (never nonzero in-window); Quarterly cycle + period-end 9/30/2026 present; account IS billed (`fee_amount>0`) |
| **ABSENT, empty billing block** | 52 | **$8,757,677.86** | vendor ships NO cycle, NO period, NO fee fields; includes new accounts (e.g. Patrick's 4340/4341/4342 arrive 07-03, 4364 arrives 08-05) and never-configured small accounts |
| **ABSENT, past period-end** | 1 | $0.01 | billing lapsed |
| **No active positions** (honest zeros) | 73 billing rows | $0 | e.g. Patrick's 248/337/929/980: emv populated until ~06-02, positions end ~June — **closed accounts; emv zeroes AFTER closure** (H3, correct) |

Hypothesis disposition: **H2 (stale carry) REFUTED** (cent-exact daily, zero divergence).
**H5 (mixed-basis growth gap) REFUTED** (firm-wide divergence on populated accounts = $0.00).
**H1 (unclosed period) REFUTED as the general mechanism** — populated and absent accounts sit in
the SAME open quarter; populated ones update daily anyway. **H4-parse EXCLUDED by control**
(bronze vs silver: 0 of 907 INF accounts lose a delivered value). **H3 holds** only for the
no-position accounts. **The real class the brief had no row for: H4-SEMANTIC — vendor ABSENCE
coerced to zero at parse** (`bronze empty → silver 0.00`, 312/312), which then subtracts real
accounts out of every SUM.

Also measured (brief §4.4): **`is_fee_earning` flips on 102/907 accounts** across the window —
the fee-flag workaround is NOT stable per account (its `fee_amount>0` limb flickers with billing
events).

### 2c. The lag distribution
For populated accounts: **lag = 0 days** (same-day cent-exact match, 100% of the joined panel;
controls 159/947 match on 90.5% of days — the residue is next-morning pull timing, 186 on
98.9%). For the absent class there is NO lag to measure: **absence is persistent per account**
(0 accounts in the 2026 window went value→dark while holding assets; the only transitions are
new-account-arrivals and account closures). The brief's "median N days old" framing dissolves:
the feed is either **current-to-the-day or missing entirely.**

### 2d. The $68.3M restated (the INFERRED decomposition is now MEASURED)
`total_current_AUA − SUM(emv fee) − SUM(emv nonfee) = 209,129,912.97 − 137,185,162.73 −
3,623,738.50 = **68,321,011.74**`, which decomposes **exactly**:

| component | amount |
|---|---|
| absent-coerced-to-zero, fee-earning (259 accts) | +$59,563,710.03 |
| absent-coerced-to-zero, non-fee (53 accts) | +$8,757,691.49 |
| negative/zero-value residue on zero-emv accounts | −$389.78 |
| accounts in positions with NO billing row (36) | $0.00 |
| divergence on populated accounts | **$0.00** |

**The $68.3M is 100.0% absence artifact. It is not a reconciliation gap.** Restated on the
current-AUA basis: **fee-earning AUA ≈ $196.75M (reported $137.19M — understated 30%)**;
non-fee ≈ $12.38M (reported $3.62M). Note the business weight: **the larger absence sits on the
FEE side** — $59.6M of billed clients' assets vanish from the firm's fee-earning AUA headline.

### 2e. Which number answers "non-fee-earning assets"? *(input to Andrew's ruling, not the ruling)*
For Patrick: current-AUA basis **$695,956.41**; emv basis **$127,852.75**. The emv basis is not
a different valuation of the same accounts — **it is the same valuation with 9 of his 12
accounts dropped** ($568,103.66 absent: 4 new accounts = $538K, 5 never-configured small =
$29K). His 3 populated non-fee accounts match current AUA to the cent, today and across the
window. **On the measurement, `ending_mv` is not a "basis" at all — it is current AUA with
availability holes.** A reader asking "what non-fee assets does this advisor hold" is asking
about the accounts' assets, which exist regardless of Orion's billing-block availability; the
number that answers is the classified sum over current AUA. What `ending_mv`-basis answers is
"assets Orion's billing engine currently reports on" — a vendor-coverage statement, not an
asset statement.

## 3 · WHAT REMAINS GENUINELY UNKNOWN (and its instrument)
**Why Orion returns an empty `Activity: Ending Market Value` for 259 in-cycle, billed,
asset-holding accounts** is a vendor-side question the at-rest data cannot answer (the broken
`Included In Billing and Fees` flag reads "Error:Not supported" on ~85% of rows in BOTH the
populated and absent classes — it discriminates nothing, consistent with PATH_DISCOVERY §1.6).
Answering it needs an Orion-side read (per-use egress ask per the brief's own §6 — NOT assumed
covered by tonight's session lift).

## 4 · DEFECTS FOUND ON THE WAY (routed, not fixed here)
1. **The builder's rename map misses the period columns.** `build_billing_dim.py`
   `BILLING_COLUMN_MAP` expects `"Billing Period Start"/"Billing Period End"`; bronze headers
   are `"Billing Period Start Date"/"Billing Period End Date"` (+ `Billing Cycle`,
   `Billing As Of Date`, `Billing Days In Cycle` — never mapped). Silver therefore silently
   lacks every period column the builder's own docstring and the brief's method both assume.
   The brief's step-4 method ("with period_start/period_end marked") was structurally
   impossible against silver — run against bronze here.
2. **Absent-vs-zero conflation at parse:** `parse_dollar(empty) → 0.00` renders "vendor did not
   report" as "vendor reported zero" — the single mechanism behind the whole $68.3M. Any fix
   (e.g. nullable emv + explicit `emv_reported` flag) is a P1-scripts decision for the build
   wave, on the ratified forms — **nothing here authorizes touching serving.**
3. Fee-flag instability (102/907 flips) — relevant to any future per-account fee logic.

## 5 · CONTROLS RUN
- **Positive control:** the 3 cent-matching accounts (159/186/947) — tracked across 95
  snapshots; they show what "working" looks like (daily movement, cent-exact).
- **Contaminated-denominator mutant (self-caught):** first bronze-vs-silver comparison used the
  full 3,052-row multi-firm CSV against 907-row INF silver → 1,264 false "parse losses";
  restricting to the INF universe collapsed it to **0**. The mutant fired; the corrected
  comparison discriminates.
- **Determinism:** the headline figures ($127,852.75 / $695,956.41 / $568,103.66 /
  $68,321,011.74) replicated across three independent computation passes and tie DS's
  independent measurement (@c55e0d6fcc) to the cent.
- **Denominators printed throughout** (97/132 days; 485+312+73+36 vs 907+36; 312/312; 0/907).

## 6 · SIDE OBSERVATIONS (surprise channel, no action taken)
- `s3://opal-data-inf/bronze/orion-api-v2/2026-04-01/positions.parquet` — a `.parquet` under a
  `bronze/` segment (Rule 17a class; the live bucket-policy gate covers `opal-data-assets`
  only). Surfaced for the owning census.
- The PROOF_OF_SPEC schema's `phase` enum carries no investigation/recon value (build-scoped
  vocabulary; a Rule-24 grain note for its owner) — the instance files under `P1-SCRIPTS` as
  the least-wrong bucket since every remediation this feeds is a P1 script act.
- The brief's partition count ("102 dated 2026") counted directories; 5 are empty-for-INF. The
  1,597-partition series is majority empty-for-INF (pre-onboarding).
