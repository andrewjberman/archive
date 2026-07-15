# FEED-9 ENUMERATION INVESTIGATION -- FINDINGS (2026-07-15 ~19:1x-19:4xZ)

**Filed by:** 0.5.0_AE_OpalETL. **Trigger:** Andrew-direct ~19:13Z (verbatim on record @
48e278c01: "START THE FEED-9 ENUMERATION FIX NOW, DO NOT WAIT FOR TOMORROW"), re-timing the
CTO 185322Z tomorrow-sequencing. **Design pins honored:** CTO 193336Z (two-class guard;
capability-probe-as-fork, run before designing further).

**The finding under investigation (part-2 wave, both-instrument-closed):** the model-tier
enumeration pulls 11 models; 3 living models with open client allocations sit outside it --
'Vanguard S&P 100/0 ETF Model Portfolio' (4ea784d7-23f0-44fc-a2bd-d8f3dad12b75, 7 allocations),
'Martin U.S. Investing' (0a1cd776-0f71-4b7c-aa63-b1fad25b05b5, 1), 'Suncoast Dividend Growth'
(1115d688-4c85-4e14-8812-d43f93a62bcc, 1). Opens 2023-09-25 -> 2025-11-07 (vintage skew refuted).

## 1. MECHANISM (source-confirmed: pull.py @ 48e278c01-worktree, parse_roster + module doc)

Enumeration is ROSTER-DRIVEN: `users/access` -> `modelAccess[]` -> keep `permissionName ==
"fullAccess"` (OWNED; the deliberate MARKETPLACE FILTER against pulling ~900 third-party
models), guarded by `expect_min_models` (under-coverage RAISE). Not pagination, not a config
list, not a broken endpoint.

## 2. LIVE GRANT STATE (probe 1, users/access via opal7, 19:34Z; read-only)

- `modelAccess` = **exactly 11 entries, ALL fullAccess, ZERO view** (the ~900-view marketplace
  set described in the module doc is NOT in this credential's current entitlement list at all).
  `accountAccess` = 0. The 11 == the wave's model tier exactly (names on the probe log; incl.
  'Pathfinder Focused Opportunities').
- **All 3 target models: ABSENT from modelAccess ENTIRELY** -- matched by none of id /
  reportedModelId / name. They are not view-downgraded; the entitlement list does not carry
  them. => The marketplace FILTER is not what excludes them; the GRANT is.

## 3. THE CAPABILITY FORK (probe 2, 19:36Z, control-first; the CTO pin-2 question)

Same session, same token; CONTROL = an owned model run FIRST so a target deny discriminates
grant-vs-outage:

| endpoint (model_id-keyed) | CONTROL Pathfinder (owned) | TARGET Vanguard (absent) |
|---|---|---|
| models/{id}/performance?grouping=daily | OK, recordCount=492 (== the wave pin) | **401 token rejected** |
| enterprises/aum?modelid= | OK, full payload | **401 token rejected** |
| enterprises/allocations?modelid= | OK, 71 records | "OK" -- but see §4: FALSE POSITIVE |

(holdings/changerequests are reportedModelId-keyed; the pairing exists only via modelAccess,
so for absent models the path key is unknowable -- moot given the 401s above.)

**FORK VERDICT: VENDOR-GRANT LIMIT.** The credential cannot fetch model-tier feeds for models
outside its entitlement list. Per the CTO pin: **this goes to Andrew as a named coverage
boundary -- NOT a build-around.** No code change can deliver these feeds under the current
grant. What we hold already (account-tier sweep) carries the 9 allocations correctly; the
model-tier DETAIL (holdings/performance/changerequests/aum) for the 3 marketplace models is
honestly absent-with-reason until/unless the grant changes.

## 4. HAZARD FINDING (probe 2b, 19:38Z): the allocations endpoint IGNORES an unentitled filter

`enterprises/allocations?modelid=<absent-model-id>` returned **HTTP OK with 9,545 records
spanning 8 DISTINCT models -- and 0 records referencing the requested model.** The vendor
silently drops an unrecognized/unauthorized `modelid` filter and returns the UNFILTERED
enterprise universe. Denominators: 9,545 records / 8 distinct model.id values / 0 == target;
control returned 71/1/71. This is the landing_guard semantic-hole class live at the vendor:
a caller with a wrong-or-ungranted modelid ingests the whole universe mislabeled as one model,
with a clean HTTP status. **Latent today** (the puller only queries owned ids) but it MUST be
gated before any enumeration change: **proposed code leg (evidence-before-code, CTO gate):
the model_allocations parse asserts every returned record's model.id == the requested modelid
and REFUSES on mismatch.**

## 5a. RULED (ANDREW-DIRECT, ~19:5xZ, my own terminal, VERBATIM): "The three missing models do not matter for our needs."

**= OPTION (B), BOUNDARY ACCEPTED.** No vendor entitlement ask. Consequences, so the record is
one consistent read: the allocation-driven augmentation + the CTO two-class guard design =
MOOT (nothing to augment); the 3 models' model-tier detail is PERMANENTLY absent-BY-RULING
(not absent-with-reason-pending); the account-tier sweep remains the complete record for their
9 allocations. **The R3 model-open-outside-map finding class STAYS LOUD in future sweep
conversions by design (a NEW out-of-scope model appearing must still surface), but hits on
these 3 model ids are EXPECTED-PER-RULING, not an escalation.** DS's permanent coverage
asterisk re-grounds on this ruling (theirs to fold). The §4 filter-integrity refuse-gate is
UNAFFECTED -- it guards owned-model ingest integrity against the vendor's silent filter-drop
regardless of this ruling; it stays staged at CTO's gate.

## 5b. THE NEEDS ROSTER (ANDREW-DIRECT, ~19:5xZ, my own terminal, second message, VERBATIM):
"I do not know exactly how they are keyed in SmartX but the models that we need are something
like: Ultra Short Term, Short Term, Intermediate Term, Long Term Conservative, Long Term
Aggressive, 50/50 INT/ST, 50/50 INT/LTC, Opal Equity Growth, Maybe some Tax SMA model(s), and
there may be another SMA i'm forgetting, but it's all Opal-specific models, not other brand
models."

**What this changes:** the coverage question is no longer the 3 other-brand models (§5a ruled
them irrelevant -- consistent: Vanguard/Martin/Suncoast are exactly "other brand"). It becomes:
**does the entitled 11 cover the OPAL-SPECIFIC needs list?** Reconciliation measured same
turn (see the needs-reconciliation report + broadcast); names like "50/50 INT/ST", "50/50
INT/LTC", "Opal Equity Growth", and "Tax SMA" have no obvious match in the live 11 -- each is
either keyed differently in SmartX, or not yet a SmartX model, or a genuine entitlement gap.
The reconciliation report carries the measured verdict per name.

## 5c. FURTHER ANDREW-DIRECT RULINGS (my terminal, ~20:2x-20:4xZ, VERBATIM; CTO's terminal
carried the fuller parallel ruling, his record 205159Z / memory ruling 7)

1. "You are right about Opal Conservative Growth, that is LTC. If we don't have the 50/50 models
   in here that is fine. However, we definitely have the SMAs in here. Maybe we don't have the
   Tax, but look around for any models that say both Opal and SMA in their name, see what comes
   up for that."
2. "We must be getting them from somewhere because they're already being ingested in our smartx
   bucket of opal-data-assets. We found the other day the main SMA had around ~18m, tax was
   around ~4m, etc. The purpose i think here is just to identify explicitly how these items are
   keyed in SmartX so we refer to them by their proper names and match them in our records based
   on their colloquial names."

CTO-relayed additions (his terminal, verbatim in his 205159Z): the 50/50s are "covered in
Eclipse only not smartx" -- **STRUCK from the SmartX roster BY DESIGN; never again a smartx
coverage gap** -- and the identification method = AUM-magnitude match on MY landed tables.

3. (my terminal, ~21:2xZ, VERBATIM -- THE SMA CONFIRM): "THis is perfect regarding opal
   dividend income and Pathfinder focused opportunities, these are the two SMAs i was looking
   for." **BOTH SMA IDENTIFICATIONS ANDREW-CONFIRMED** -- Opal Dividend Income (the ~$18M
   main SMA) + Pathfinder Focused Opportunities (the ~$4M SMA).

4. (my terminal, ~21:3xZ, VERBATIM -- THE TAX-LABEL CORRECTION): "I wouldnt call Pathfinder
   a Tax SMA, just an SMA, we will figure out the tax stuff later." **The 'Tax' label I had
   provisionally attached to Pathfinder (via the ~$4M magnitude in message 2) is SEVERED --
   Pathfinder Focused Opportunities is AN SMA, unlabeled; the Tax SMA question is DEFERRED
   BY RULING, not resolved and not unmatched-needs-search.** Open rows after this: 'Opal
   Equity Growth' (unmatched) + 'Tax SMA' (deferred, "later").

5. (my terminal, ~21:3x-21:4xZ, VERBATIM -- THE WRAP + THE BRONZE VERIFICATION ASK):
   "Don't care about Opal Equity Growth for now, what we have is good, we can wrap it here,
   just make sure that we're properly pulling all of these in our smartx bronze" +
   clarification: "specifically in the opal-data-assets/smartx/ bronze".
   **Opal Equity Growth -> PARKED BY RULING (not unmatched-open; 'for now'). The thread is
   WRAPPED.** The verification ran same turn (listing instrument, bucket opal-data-assets):
   **ALL 7 CONFIRMED MODELS x ALL 5 MODEL-TIER FEEDS PRESENT @ smartx/model/{rmid}/bronze/
   {feed}/20260715/** -- holdings / changerequests / performance / model_allocations /
   model_aum, one object each, sizes internally consistent (model_allocations scales with
   book: LTC 1,316KB vs SMA 25-42KB, matching 3,195 vs 40-45 allocations). Grid verbatim in
   the session log.

## 6. THE COLLOQUIAL -> PROPER NAME MAP (the ruled deliverable; measured 2026-07-15 ~20:5xZ)

Method: fact_model_aum_daily date=2026-07-15, latest day per rmid, closing_equity basis (D4
§8.6: totalAum is mis-scaled); names + id pairs from fact_model_allocation_roster; open counts =
roster status=='open'. Denominators: 8 rmids carry books; 3 entitled 'Opal Global *' models
carry no aum rows at all; 'Opal Global All Equity Total Return' has a $0 row @ 07-13.
**Total $1,426,386,759 @ day=2026-07-14 -- ties the ~$1.428B/$1.4B ground truth.**

| Colloquial (Andrew) | SmartX PROPER name | AUM (closing_equity @ 07-14) | open | rmid / model_id |
|---|---|---|---|---|
| Ultra Short Term | **Opal Ultra Short-Term Income** | $44,872,335 | 170 | 3f8e94c4-2fc7-4cc3-957d-fecf70647b39 / c000fe6a-4f29-42e6-ae2e-75ea6162d175 |
| Short Term | **Opal Short-Term** | $106,415,150 | 691 | 955c9631-74ed-4f3c-9691-38c24b5a6d0d / 0f76a5a0-3b8e-4433-846c-ad41765b51d8 |
| Intermediate Term | **Opal Intermediate-Term** | $293,106,045 | 1,597 | 14540628-6eb8-4155-856c-e3264a39ac6c / 729210dd-444c-47c9-997d-8a3bcede7afd |
| Long Term Conservative (LTC) | **Opal Conservative Growth** (ANDREW-CONFIRMED) | $755,282,826 | 3,195 | 3f111210-1fe6-445c-8db2-c98733e3f478 / 74c119db-73d6-4cf1-9535-740026df8121 |
| Long Term Aggressive | **Opal Long-Term Aggressive** | $203,464,677 | 1,387 | 54e83021-43cc-44cc-a2f8-b1a36310f38e / 69cc5e3b-b14c-4640-bb4b-ead7837c1bc9 |
| Main SMA (~$18M) | **Opal Dividend Income** -- MAGNITUDE MATCH ($18.59M, sole candidate in [12M, 25M]) + **ANDREW-CONFIRMED ~21:2xZ** (§5c msg 3) | $18,586,236 | 40 | ea6cbb22-d04e-49dd-a12a-654058fa733b / 48af6559-593a-48a9-8ac4-3c78ded93ad8 |
| SMA #2 (~$4M) | **Pathfinder Focused Opportunities** -- **ANDREW-CONFIRMED ~21:2xZ as an SMA; NOT the Tax SMA** (correction §5c msg 4: "I wouldnt call Pathfinder a Tax SMA, just an SMA") | $4,659,490 | 45 | ab0a2a03-a201-475c-ab4c-b291ad267422 / 843d875b-62f7-4ef8-b833-5078a3f637d5 |
| Tax SMA | **DEFERRED BY RULING** (§5c msg 4: "we will figure out the tax stuff later") -- no SmartX identification attempted until his word; NOT an unmatched-needs-search row | -- | -- | -- |
| 50/50 INT/ST | STRUCK -- **Eclipse-only by design** (ruling, CTO record 205159Z) | -- | -- | -- |
| 50/50 INT/LTC | STRUCK -- Eclipse-only by design | -- | -- | -- |
| Opal Equity Growth | **PARKED BY RULING** (§5c msg 5: "Don't care about Opal Equity Growth for now") -- was honest-UNMATCHED (no magnitude/name candidate; nearest dormant name 'Opal Global All Equity Total Return' carries a $0 book); reopens only on his word | -- | -- | -- |

Note for the record: NO SmartX model carries 'SMA' in its name (the account-tier 'SMA' string
hits are all 'SMARTX' custodial titles); the SMAs are keyed as ORDINARY MODELS named
'Opal Dividend Income' (+ candidate 'Pathfinder Focused Opportunities') -- which is exactly why
colloquial matching failed until magnitude matching was ruled. Standing copy of this map:
SMARTX_INGESTION_ARCHITECTURE.md name-map table.

## 5. WHAT THIS RESOLVED TO (the decision as it was presented; §5a-c rule it)

The "enumeration fix" is not an engineering defect to patch -- the enumeration correctly
mirrors the grant, and the grant is the boundary. The decision is Andrew's:

- **(A) Obtain entitlements** for the 3 marketplace models (vendor ask: view-or-better
  modelAccess for the 3 ids above on the model-tier credential). Then the approved
  allocation-driven augmentation + CTO's two-class guard land as designed, the 3 models'
  feeds flow, the 9 ids map, DS expectation updates ride (DS = co-owner, has the CC).
- **(B) Accept the named boundary:** account-tier coverage (already complete) is the record
  for these 9 allocations; model-tier detail stays absent-with-reason; DS's permanent
  coverage asterisk (their fecdcd358 fold) carries it honestly.

Either way the filter-integrity refuse-gate (section 4) should land -- it guards the puller
against the vendor's silent-unfiltered behavior regardless of grant outcome.

**Compiler tools this investigation:** none fit (live vendor API + module source; no comp-tool
covers the SmartX surface -- the standing monolith/SM coverage gap, noted again). Raw calls
were operational probes; probes 1/2/2b scripts persist in the session scratchpad
(feed9_probe1_users_access.py / feed9_probe2_capability.py).
