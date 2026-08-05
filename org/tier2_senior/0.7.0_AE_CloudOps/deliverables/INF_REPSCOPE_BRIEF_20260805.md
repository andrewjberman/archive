# BRIEF FOR DS: INF gold chain frozen 5 days by a stale hand-drawn rep allowlist

**Author:** `0.7.0_AE_CloudOps~A` · **Date:** 2026-08-05 · **Repo HEAD at analysis:** `d98149ea6d`
**Requested by:** Andrew-direct (verify the durable fix before proposing it)
**Owner of the fix:** DS (`data/inf/scripts/silver/*.py` is DS-owned, Rule 13). AE filed this; AE does not land it.

---

## 1. What is broken

`inf-gold-chain-failed` has been in ALARM since 2026-08-02. The chain aborts at **`INF_C_01`
(canonical_nna.py), step 34/66**, exit=1, identically on 08-02, 08-03, 08-04, 08-05. Last clean
completion: **2026-07-31T14:56:48Z** (`s3://opal-data-inf/gold/meta/pipeline-complete.json`).

**Bronze and auth are healthy.** Every Orion pull step reports `ok`; the JWT is valid; silver
api_dims land fresh daily. This is not a cookie/auth problem.

The abort is a **fail-closed data-integrity guard doing its job**:

```
nna_coverage_guard.NNACoverageRegression: NNA PARTITION COVERAGE REGRESSION --
5 account(s) carrying $514,487.47 of SERVED NNA are about to be DROPPED from
partitions that are being REWRITTEN.
```
`lib/nna_coverage_guard.py:320`, raised from `INF_C_01.canonical_nna.py:918`.

## 2. Root cause (source-confirmed)

On **2026-07-31** five accounts were reassigned at Orion from Peter Lee (rep 12) to
**Noel Soderblom (rep 10)**. Rep 10 is absent from the hand-maintained scope allowlist, so from the
08-01 snapshot those accounts were filtered out of `silver/api_dims/accounts_v2`. On 08-02 a
transaction rewrote a partition holding their NNA history, and the guard correctly refused to delete it.

**The filter that drops them:**

`data/inf/scripts/silver/convert_orion_api_to_silver.py:540` @ `e3ec94f5b7`
```python
out = out[out['rep_id'].isin(INFLECTION_REP_IDS)].copy()   # INFNNA.001
```
with `INFLECTION_REP_IDS = {3, 6, 11, 12}` — `convert_orion_api_to_silver.py:631` @ `e3ec94f5b7`
and `_orion_api_silver_lib.py:113` @ `d28f2d5b93`.

`rep_id` here is the **servicing rep from `household_rep_mapping`** (joined on `household_id`,
`:513`), not the account's own `representativeId`.

> **NOTE — the custodian filter at `:431` is NOT the culprit.** `build_accounts_v2` first filters
> `custodian IN ('Fidelity_Inflection','Fidelity_LH')`, which these five **pass**. The rep filter at
> `:540` is what removes them. I initially mis-attributed this to the custodian path; corrected by
> reading the function.

**The accounts never left the vendor.** In today's raw bronze payload
(`s3://opal-data-inf/bronze/orion-api/2026-08-05/accounts_roster.json`, marker
`roster_asof=2026-08-05 status=fresh`), all five are `isActive=True`, `cancelDate=None`,
`lastPositionDate=2026-08-04`, and **gaining value**:

| Account | Name | 07-31 | 08-05 | rep change |
|---|---|---|---|---|
| 4139 | Wurzner IRA Rollover | $423,332.12 | $429,607.49 | Lee → Soderblom |
| 4136 | Wurzner Beneficiary IRA | $150,943.18 | $153,053.57 | Lee → Soderblom |
| 4358 | Wurzner Roth | $45,839.00 | $46,631.42 | Lee → Soderblom |
| 4352 | Erickson Roth | $5,025.22 | $5,116.50 | IWM → Soderblom |
| 4356 | Erickson TOD | $2,499.83 | $2,497.62 | Lee → Soderblom |

**Do NOT excuse these in `nna_coverage_excusals.json`.** Every existing excusal rests on a vendor
closure record (`cancelDate`, `isActive=false`, `currentValue=0.0`). These have the opposite
signature. An excusal would permanently delete the NNA history of five live, funded, actively
reconciling accounts — and the guard's own text notes the firm-total tie-out would still balance,
so nothing downstream would ever catch it.

## 3. Verification of the proposed durable fix (the ask)

Universe: `NewPortfolio` bronze 2026-08-05, 3,005 rows.

| Universe definition | Accounts | AUA |
|---|---|---|
| **A_current** — rep_id ∈ {3,6,11,12} *(today's behavior)* | 864 | $208,794,476.83 |
| **A_expanded** — rep_id ∈ {3,6,10,11,12} | **869** | **$209,431,383.43** |
| **B_predicate** — `custodian == 'Fidelity_Inflection'` | 868 | $209,431,395.13 |
| **B_wide** — `custodian ∈ ('Fidelity_Inflection','Fidelity_LH')` | 2,302 | $493,293,971.36 |

`A_current` reproduces live silver exactly (864 rows) — the model is validated against reality.

### Where the pattern breaks

**Custodian is the wrong axis. It fails in both directions:**

- **`Fidelity_Inflection` alone UNDER-covers by exactly 1 account.** Symmetric difference is a
  single row: **account 4239 "Alongside Llc"**, `custodian=Fidelity_LH`, serviced by Inflection rep 3,
  `current_value = -$11.70`, `isActive=True`. This is the residue of the documented 2026-04-30 AUM
  reconciliation (`:406-409`): `Fidelity_LH` is a second Orion custodian code covering Inflection-rep
  households. B_predicate ⊂ A_expanded strictly; nothing is in B and not in A.
- **Adding `Fidelity_LH` OVER-covers by 2.36×** — $493.3M vs $209.4M — because the LHP firm
  (reps 13/14/15, $283M) shares that custodian code. This is the failure already recorded at
  `:535-537` (Guard B fired at $476.9M in May 2026; on today's data it would fire at $493.3M).

**The rep axis is the right one, and it can be derived instead of hand-drawn.** Orion's own
`representativeNumber` cleanly separates the firms sharing this Orion instance:

```
rep=12  Peter Lee            "TAN Inflection Lee"             MATCH
rep=11  Patrick Scanlan      "TAN Inflection Lee/Scanlan"     MATCH
rep=10  Noel Soderblom       "TAN Inflection Lee/Soderblom"   MATCH   <-- missing from the hand list
rep=6   Joe Brandenburg      "Inflection Brandenburg"         MATCH
rep=3   IWM                  "Inflection Wealth Management"   MATCH
rep=5   Jeremy Keil          "Keil FP Keil"                     -     $116.5M  other firm
rep=9   John Kurcz           "Keil FP Kurcz"                    -     $93.0M   other firm
rep=18  Daria Zalewska       "Keil FP Zalewska"                 -     other firm
rep=13  Dan Sinnen           "LHP/Dan"                          -     $112.7M  other firm
rep=14  Tim DeMuth           "LHP/Tim"                          -     $96.7M   other firm
rep=15  Kevin Christensen    "LHP/Kevin"                        -     $74.5M   other firm
rep=1   New Accounts Rep     "Alongside, LLC"                   -     other firm
```

**Result — exact identity, zero discrepancy:**

| Formulation | Accounts | AUA |
|---|---|---|
| household-rep ∈ {3,6,10,11,12} *(baseline)* | 869 | $209,431,383.43 |
| account `representativeNumber` contains `"Inflection"` | 869 | $209,431,383.43 |
| account `representativeId` ∈ predicate-derived set | 869 | $209,431,383.43 |

Symmetric difference in both directions: **0**.

**The predicate is self-updating.** Re-derived against the 07-31 roster it yields `{3,6,11,12}`;
against 08-05 it yields `{3,6,10,11,12}` — it tracked the reassignment on its own, which is precisely
the property the hand-drawn list lacks.

**Guard B headroom:** post-fix AUA $209,431,383.43 sits inside `GUARD_B_AUA` bounds
($150M–$300M, `_orion_api_silver_lib.py:115-116`). The fix does not trip the guard.

## 4. The allowlist is duplicated in 9+ places, and they already disagree

| File:line | Value |
|---|---|
| `data/inf/manual_api/pull_inflection_representatives.py:65` | `[3, 6, 7, 8, 10, 11, 12]` ← **includes 10** |
| `data/inf/scripts/silver/_orion_api_silver_lib.py:113` | `{3, 6, 11, 12}` |
| `data/inf/scripts/silver/convert_orion_api_to_silver.py:631` | `{3, 6, 11, 12}` |
| `data/inf/scripts/silver/convert_orion_to_silver.py:105` | `{3, 6, 11, 12}` |
| `data/inf/scripts/gold/INF_B_00.canonical_holdings.py:91` | `{3, 6, 11, 12}` |
| `data/inf/scripts/gold/INF_D_08.nmec_nmnc_nna.py:18` | `{3, 6, 11, 12}` |
| `data/inf/scripts/verify/shape_check.py:46` | `{3, 6, 11, 12}` |
| `data/inf/manual_api/create_tax_dim_queries.py:45` | `{3, 6, 11, 12}` |
| `data/inf/manual_api/create_unified_account_dim_query.py:45` | `{3, 6, 11, 12}` |
| `data/inf/manual_api/probe_inflec_household_rep_mapping.py:44` | `{3, 6, 11, 12}` |

The **pull layer already pulls rep 10** — which is why rep 10's 2 households are present in
`household_rep_mapping` bronze — and the **filter layer then discards it**. The lists also drift the
other way: reps **7 and 8** are in the pull list and have **0 accounts** in the live roster (retired).

Two conclusions: (a) a fix applied to only one constant leaves the estate inconsistent; (b) this is
the *"a predicate is not a roster"* class (CTO, 2026-08-04) — a hand-drawn universe standing in for a
re-derivable one.

## 5. Recommendation

**Immediate (unblocks the chain today):** add `10` to `INFLECTION_REP_IDS` at every site in §4.
Verified safe: +5 accounts, +$636,906.60, Guard B satisfied. Re-run the INF gold chain; `INF_C_01`
will find the accounts present and the coverage guard will pass without an excusal.

**Durable:** replace the constant with one derived helper — Inflection scope = reps whose
`representativeNumber` matches `Inflection` in the vendor rep roster — computed once and imported by
all consumers, so the universe re-derives per run instead of being maintained by hand.

**Caveat, stated plainly:** the predicate keys on a vendor free-text field. A rep-code rename at
Orion would move the universe silently — the same failure mode one layer over. So the derived set
must be **asserted, not trusted**: fail loudly when the derived rep set *changes* between runs
(added or removed), and keep Guard B. The defect here was never the wrong number; it was that a
scope change was **silent**. A derived predicate that changes silently is no better.

## 6. Open item (not resolved by this brief)

The 08-01 run's NNA **AT-RISK REGISTER** listed 17 accounts but did **not** include these five,
although they had already been filtered out that morning. That register is the early-warning surface
for exactly this failure and it did not name them. Worth a separate look — flagging rather than
guessing at the mechanism.

## 7. Evidence

- Chain telemetry: `s3://opal-data-inf/telemetry/inf-gold-layer-runner/history/chain_full_2026080{1..5}_*.json`
- Chain logs: `s3://opal-data-inf/gold/logs/chain_full_20260805_134750.log` (guard block at ~line 35,996)
- Raw vendor roster: `s3://opal-data-inf/bronze/orion-api/{2026-07-31,2026-08-05}/accounts_roster.json`
- NewPortfolio bronze: `s3://opal-data-inf/bronze/orion-api/{date}/new_portfolio_accounts.json`
- Household rep mapping: `s3://opal-data-inf/bronze/orion-api-v2/2026-08-05/household_rep_mapping.json`
- Failure marker: `s3://opal-data-inf/gold/meta/pipeline-failed.json`

All figures re-derived from raw bronze (unmodified vendor payloads); no vendor egress was spent —
the direct API path is EC2-side and this analysis read the landed raw bytes the pipeline itself saw.
