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

## 5. WHAT THIS RESOLVED TO (the decision as it was presented; §5a-b rule it)

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
