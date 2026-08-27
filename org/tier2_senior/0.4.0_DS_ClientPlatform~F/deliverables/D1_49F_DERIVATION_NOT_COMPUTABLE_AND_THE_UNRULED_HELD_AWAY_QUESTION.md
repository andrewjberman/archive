# D1_CATVIEWS — 49F: the derivation-vs-assertion question, MEASURED. And one UNRULED $138.8M question it surfaced.

**Terminal:** `0.4.0_DS_ClientPlatform~F`. **Cells:** D1-h-c1, D1-h-c2 (per-firm client feed predicate).
**Status:** measurement complete. **No code changed. No emission changed. Nothing here alters a landed figure.**

## WHY THIS EXISTS

I filed this question against myself on 2026-08-25 in
`ANDREW_DIRECT_20260825_TWO_SENSES_OF_SUPERVISED_OPAL_DEFINITION_BINDS.md:74-78`, flagged
`ONE QUESTION RAISED, NOT ANSWERED`, and then filed a proof-of-spec whose AC4 passes without it:

> for cottonwood he gave a **DERIVATION** (residual of Opal-holding accounts); for 49financial he
> gave a **FLAT ASSERTION** (ALL Client is Supervised). If 49F holds accounts with **no** Opal
> exposure, the two forms disagree for that firm.

A question recorded as open is not the same as a question answered, and this one was one command
away from being answerable. It is now answered.

## THE ANSWER: THE DERIVATION IS **NOT COMPUTABLE** FOR 49F — AND THAT IS NOT A DEFECT

49F **does** carry account grain, so my earlier working assumption that it might not was wrong:
`mdpf/feeds/model_aua_positions/49financial/2026-08-25.parquet` is 7,317 rows at
**one row per account**, with `cohort_class` ∈ {model, sma} and a resolved `model_key`.

**But the two planes the derivation needs do not share a key.** The join control, run BEFORE any
conclusion was drawn:

```
feeder (MDPF / Schwab RPS)  distinct account_id : 7,317   e.g. 33470635-db62-439e-b1da-0790e8a4a98e
universe (BD 49F silver)    distinct account_id : 7,070   e.g. z0823009851

OVERLAP  feeder.account_id <-> bd.account_id               : 0
OVERLAP  feeder.account_id <-> bd.original_account_number  : 0
OVERLAP  feeder.account_id <-> bd.account_number           : 0

key shape  feeder = UUID-form  200/200 sampled
           bd     = z0-form    200/200 sampled
```

**A ZERO HERE IS THE EXPECTED RESULT, NOT A FINDING.** 49F's Opal model exposure is sourced from
the **Schwab/RPS** plane and its account universe + supervision flag live on the **Black Diamond**
plane, and no account-grain bridge between them exists in these artifacts.

⛔ **THIS IS THE 0-OF-944 SHAPE, AND I WALKED INTO IT ONCE ALREADY IN THIS TO.** Had I joined and
reported without the control, every 49F account would have read *not-Opal-exposed*, the derivation
would have returned **Client - Opal Supervised = $0.00 / Unsupervised = $258,497,151.78** — a clean,
decisive, fully-partitioned answer that **flatly contradicts Andrew's explicit ruling** — and the
only thing that would have made it look wrong is that it contradicted him. **A control is what
stands between a plausible number and a wrong one; on this exact join, twice now, it is the only
thing that has.**

### SO THE TWO RULE FORMS DO NOT DISAGREE — THE DIFFERENCE TRACKS THE DATA

| firm | model exposure plane | universe plane | shared account key | rule form Andrew gave |
|---|---|---|---|---|
| **cottonwood** | BD rebalancer | BD | **yes** (`external_id`, 934/944) | **DERIVATION** |
| **49financial** | Schwab RPS (UUID) | BD (`z0…`) | **no** (0/3 columns) | **FLAT ASSERTION** |

**His flat assertion for 49F is the only form 49F's data can currently express.** The question I
raised resolves as *no inconsistency*: he gave each firm the rule its feeds can carry. **The
49financial emission stands exactly as landed** — `Client - Opal Supervised $258,497,151.78 /
Opal Unsupervised $0.00`, reconciling to Client to the cent.

## ⛔ THE THING THE MEASUREMENT SURFACED THAT NOBODY HAS RULED ON — $138,839,619.90

The BD plane carries `account_supervised` **for 49F**, populated, with the same value set
Cottonwood's has (BD 49F silver allocations @2026-08-21, 7,070 accounts):

```
Supervised     6,532 accounts   1,836,883,807.98
Unsupervised     538 accounts     138,839,619.90
TOTAL          7,070 accounts   1,975,723,427.88
```

For **Cottonwood**, Andrew ruled the BD-unsupervised bucket **out of everything** (verbatim,
2026-08-25): *"Cottonwood does not want Client Held Away (unsupervised by opal AND Cottonwood)
included in any figures for them"* — measured at **$30,322,927.42** @08-19 and excluded.

**For 49financial, the equivalent bucket is $138,839,619.90 and NOBODY HAS RULED ON IT.**

**MY READ, offered as a read and not as a finding:** his words are Cottonwood-scoped on their face
— *"for them"* — which points at a client preference rather than a house rule, so the default for
49F is probably **include**. I am not acting on that. **$138.8M is four and a half times the
Cottonwood bucket he cared enough to rule on, and a default that large should be stated, not
inherited from the shape of a sentence about a different firm.**

## ⛔ WHAT I COULD NOT DETERMINE, STATED SO IT IS NOT MISTAKEN FOR COVERAGE

**Whether those 538 accounts are currently IN or OUT of the served 49F figure — I cannot tell from
my plane, and I am not guessing.** The three-way comparison does not resolve it:

```
MDPF served 49financial partner_custody_total @2026-08-21   1,749,020,940.64
BD all-custodian                              @2026-08-21   1,975,723,427.88
BD supervised-only                            @2026-08-21   1,836,883,807.98
```

**The served figure matches NEITHER**, because the 49F feed is **Schwab-custody-scoped** by Andrew
Mandate (PRD v0.9; `build_mdpf_wse_49f_non_model_aua.py:16`) while the BD table is all-custodian.
The custody scoping dominates the supervision question and I cannot separate them without the
`account_id -> billing_account_custodian` crosswalk. **That is WS-E ground, not mine.** Anyone
reading the $226.7M gap as a supervision effect would be reading a custody effect.

*(Cross-check that the landed emission is unaffected: served `non_model_aua` is $281,433,164.26 and
my Client node is $258,497,151.78; the $22,936,012.48 difference is the SMA + alternatives fold,
which is what the view tree does by construction. No contradiction.)*

## OPEN CALL FOR ANDREW — one question, one line to answer

> **Does 49 Financial's "Client Held Away" (538 BD-unsupervised accounts, $138,839,619.90) get
> excluded from MDPF figures the way Cottonwood's does — or was that a Cottonwood-specific
> preference?**
>
> **REC — (b) Cottonwood-specific; 49F includes.** Your words were scoped *"for them."* But the
> bucket is $138.8M and the current behaviour is unverified either way, so this should be your
> word rather than my inference.

**A second question is downstream of the first and belongs to WS-E, not to this TO:** if the answer
is *exclude*, someone has to establish whether the Schwab-scoped feed already drops them, which
needs the custodian crosswalk.

**Author:** `0.4.0_DS_ClientPlatform~F`. **Measured 2026-08-25.** BD vintage 2026-08-21, MDPF served
vintage 2026-08-21, feeder 2026-08-25.
