# P4 LEG A — EVIDENCE PACKAGE + NEVER-WIDEN DETERMINATION STATE (persisted pre-reboot)

**Author:** 0.4.0_DS_ClientPlatform~B · **2026-08-12 ~1548Z** · **archetype:** EVIDENCE (held act)
**Why this file exists:** Andrew-direct ~1520Z ordered a device reboot once all work is committed. LEG A is
HELD on a never-widen determination, so its evidence had no act to carry it and lived only in session
context. A reboot erases held work invisibly. Everything CTO + COO need to resume without re-deriving is here.

**Keys:** `platinum/firm/partner_analytics_{quarterly,monthly,annual}.json` (3 of the 17).
**Emitter:** `data/assets/scripts/gold/runners_49f/d13_firm_partner_analytics.py` @459434341d → @ca97f33247 → @33f7d47009.
**STATUS: HELD. NOTHING FIRED. No served-key move made. No deploy ledger open (a ledger opened on a gated
act cannot be closed — COO adopted this as the rule).**

---

## 1. THE FOUR §8 LEGS — measured by me, not cited from base

### LEG 1 — VALUES: DELTA=0 AT THE INPUT LAYER
Own full two-sided census, full pagination, materialised client-side, scoped to exactly d13's gold reads:

| table | OLD objs | NEW objs | common | ETag IDENTICAL | differ | only-OLD | only-NEW | bytes |
|---|---|---|---|---|---|---|---|---|
| `canonical/canonical_valuation` | 1,052 | 1,052 | 1,052 | **1,052/1,052** | 0 | 0 | 0 | 148,690,690 |
| `canonical/nna_canonical` | 1,052 | 1,052 | 1,052 | **1,052/1,052** | 0 | 0 | 0 | 13,256,247 |
| **TOTAL** | | | **2,104** | **2,104/2,104** | **0** | **0** | **0** | **161,946,937** |

### LEG 2 — WRITE-SIDE LOCATION (live head-object)
- NEW `canonical_valuation/date=2026-08-07/data.parquet` — LastModified `2026-08-12T14:05:42Z`, ETag `fc4dae8c704366f9`
- NEW `nna_canonical/date=2026-08-07/data.parquet` — LastModified `2026-08-12T14:10:15Z`, ETag `76f35a7c35e22589`

### LEG 3 — READ-SIDE LOCATION
d13's four reads against `portal/gold/advi/49financial/`:
1. `canonical/canonical_valuation` — PRESENT, 526 partitions, latest `date=2026-08-10`
2. `canonical/nna_canonical` — PRESENT, 526 partitions
3. `dim_advisor_fee_role` (jd2) — reference, NOT gold, zero P4 exposure
4. `dimensions/dim_relationship` — **was ABSENT at measurement time (positive-controlled: empty rc=0 while the
   identical call shape on `canonical/nna_canonical/` returned partitions).**
   ✅ **NOW CLOSED by base @4c1219fc34** — copy 10/10 (`dim_account`, `dim_relationship`, `nna_atomic`, ETags
   10/10 identical) + `dim_security`/`dim_boundary`/`dim_calendar` produced and verified at rest.
   **So LEG A's dim dependency is SATISFIED; it is held only on the never-widen call.**

### LEG 4 — OLD ROOT UNTOUCHED (the place the write should NOT have gone)
- OLD `canonical_valuation/date=2026-08-07` — LastModified `2026-08-11T18:43:29Z` (~20.2h, **predates the 14:16Z re-point**)
- OLD `nna_canonical/date=2026-08-07` — LastModified `2026-08-11T19:13:12Z` (~19.7h, predates it)
- **ETags IDENTICAL across roots** (`fc4dae8c…`, `76f35a7c…`) — the re-point changed WHERE and provably not WHAT.

---

## 2. DETERMINISM HASHES — pre-declared, which is what made them evidence
Published BEFORE any comparison (a hash published first is a prediction; published after, a description).

| granularity | PRE-FIX (@ca97f33247) | POST-FIX (@33f7d47009) |
|---|---|---|
| quarterly | `dfae7d2ea6fab1769467f35b0c5e96f7` | `ac3033e668938c35aaec7a6773e0b158` |
| monthly | `88a49e8b131a04557d5a9d9effa932db` | `69bfe587b70ac0b04283a720f18c110a` |
| annual | `680937dd48eb4106dc0ef01fadd07dd0` | `306b8fe1532c31c159b61e7f3d30da71` |

Both sets verified STABLE across two same-input runs. **The pre-fix set is the one eligible for the DELTA=0
comparison against an old-root read; the post-fix set supersedes it for any future run of the current code.**

---

## 3. ⛔ THE NEVER-WIDEN DETERMINATION — the substance CTO + COO hold

### 3a. PRE-FIX census (what disqualified the leg from the no-hold fast path)
| axis | served | mine (pre-fix) | consequence |
|---|---|---|---|
| advisors (adv view) | **15** (curated) | **46** | **35 NEWLY EXPOSED**, each with a real NAME + AUA + account/client counts |
| advisors | 4 present | absent | rows a consumer reads today DISAPPEAR (overlap **11/15**; served NOT a subset) |
| client label | `("z08327149","Chan, William & Shelley")` | `("rel_e9236546a41b7c","rel_e9236546a41b7c")` | every client name → a hash |
| client keys | `z…` grammar | `rel_…` grammar | fully disjoint |
| architects (nna.adv) | 53 | 45–47 | 3–5 newly exposed, 11 absent |

### 3b. POST-FIX census @33f7d47009 (CTO GO 152403Z — an act that strictly NARROWS exposure)
Identical across all three granularities:

| axis | pre-fix | **POST-FIX** |
|---|---|---|
| advisors emitted | 46 | **9** (served 15) |
| **NEWLY EXPOSED** | **35** | ⭐ **0** |
| dropped (served-only) | 4 | ⚠ **6** — `august_vordenbaum, mike_kipniss, patrick_mundlin, ted_grant, unresolved, zach_hawkins` |
| overlap | 11/15 | **9/15** |
| hash-labels | 135 | ⭐ **0/135** (now "WILLIAM CHAN", "JESSICA ABELN LINDSEY TTEE") |
| payload | 3.94 MB | 1.34 MB |

**So the IRREVERSIBLE half is CLOSED. The lane crossed from OVER-EXPOSING (irreversible) to UNDER-SERVING
(trivially reversible) — the safe side of CTO's asymmetry, but NOT correct.**

### 3c. ⛔ MY PREDICTION WAS FALSIFIED — recorded as a finding, not a footnote
I predicted the 4 dropped advisors would RETURN under the corrected filters (hypothesis: architect-primary
advisors my all-roles-touch population mis-RANKED). **They did not — the drop went 4 → 6.** CTO's condition
(i) — *verify, do not assume* — is the only reason this is a measurement rather than a false claim.

### 3d. THE PRODUCT RULE (Q1, CLOSED AT SOURCE — this is a BUILD DEFECT of mine, not a divergence)
`data/black_diamond/scripts/gold/D_01.partner_analytics.py:982-994 @00a6a8ae60`:
```
# Primary role = the role with highest AUA for each advisor.
# ADV donut filters to primary_role == 'architect' only (Andrew's UX intent:
# top N people whose PRIMARY role is architect, not anyone tagged as architect
# on a few accounts).
```
Plus `:955` — `str(adv).strip() not in ('', 'Unassigned')`. **Andrew's UX intent is in the comment, and it
rejects BY NAME exactly what my emitter did.** Ported into d13 @33f7d47009.
⚠ **How I got it wrong:** the served title "AUA by Advisor (All Roles)" is accurate about the **VALUE**
(AUA tagged across all 5 role columns) and **SILENT about the POPULATION** (primary-role-architect only).
I read the population semantics off the title. **A TITLE CANNOT SEE A POPULATION EITHER.**

### 3e. THE RESIDUAL 9-vs-15 — mechanism SOURCE-CONFIRMED, not tuned
The served `primary_role` rides a **CANONICAL role_aua SNAPSHOT**, not a jd2 derivation:
- override `D_01:970-976` (RA-P4) · loader `D_01:394-413` · key `gold/canonical/role_aua/{date}.parquet`
  · producer `C_01c.role_aua_flow_join.py` · resolver `lib/s3_layout.py:173-174`
- **LIVE: `2026-08-06` PRESENT (18,379 B, LM `2026-08-12T05:05:46Z`); `2026-08-07` ABSENT** (positive-controlled;
  the probe's own control key returned present, so the ABSENT is real).
- I derive role AUA from **jd2 × canonical_valuation — A DIFFERENT BASIS** ⇒ different primary-role
  assignments ⇒ different population. **Not a tuning parameter; a basis difference.**
⛔ **OPEN DESIGN QUESTION (CTO/COO, not mine): should d13 consume the canonical role_aua artifact?** It lives
in the LEGACY bd gold path — outside P3's copy scope and outside the new product root.

---

## 4. ⛔ THE TWO-IDENTITY-SYSTEMS FINDING (the other live blocker) — PRODUCT question for ANDREW

**Measured, decisive:**
- **0/201** served client keys match ANY id in the canonical dim (`account_id`, `relationship_id`,
  `master_group_id`) — including z-prefix / leading-zero normalisation. **Not a re-keying: a different system.**
- **113/201** served labels are MULTI-PERSON household forms ("Chan, William & Shelley"). A per-account
  registration name **structurally cannot** produce them — the second is two people.
- Same advisor, same recognisable people, **ZERO exact AUA matches**, mine systematically smaller:

| served | mine |
|---|---|
| Chan, William & Shelley **$75,464,904.18** | WILLIAM CHAN **$61,723,413.86** |
| Lindsey, Jessica **$36,415,063.78** | JESSICA ABELN LINDSEY TTEE **$32,653,203.51** |
| Smith, Craig & Kimberly **$25,727,221.15** | CRAIG M SMITH **$25,186,727.37** |
| Waldrop, Mark and Dreama **$40,194,499.26** | WALDROP INVESTMENTS LLC **$23,817,167.64** |

⚠ **DO NOT QUOTE THE DOLLAR TABLE AS A MEASURED GRAIN DELTA.** It is a measured TOTAL delta with THREE live
candidates: household grain · valuation basis · role-tagging. Travis Penfield's own advisor total also differs
(**$446,677,579.87** served vs **$361,133,185.60** mine) — a grain story cannot explain a delta that also appears
one level up. **The IDENTITY gap is isolated decisively; the DOLLAR gap is not.**

**GRAIN, honestly stated:** my `rel_` is an ACCOUNT-GROUPING (7,239 account-rows → 4,291 relationship_ids,
1.69 accounts each; `a01` anchors on min account_id). The served household groups PEOPLE. **Both are
coarser-than-account; whether they are the SAME grain is NOT established** (one-noun-two-things refused, not resolved).

**WHERE THE HOUSEHOLD IDENTITY COMES FROM — traced to the artifact:**
`D_01:1023` `name_map = client_dim.set_index('relationship_id')['relationship_name']` → `:1029-1031` map with
`.fillna(<the id>)` → `:330,344` loads constant `CLIENT_DIMENSION` → `lib/s3_layout.py:38` =
**`gold/dimensions/client_dimension.parquet`**; AUA from **`gold/client_performance.parquet`** (daily × relationship).
⭐ **D_01/D_04 COMPUTE NOTHING about household identity — they map and pass through.** By COO's own rule,
*"which identity system is the product"* is therefore **a PRODUCT question for Andrew.**
⭐ **The `.fillna(id)` at `:1030` is the tell: the LEGACY degrades to key-as-label exactly as my emitter did
whenever the name is missing. My hash-labels were the same failure the legacy avoids by having the dimension.**
⛔ **UNMEASURED (the one hop left): who produces `client_dimension.parquet`, and is the household grouping
DERIVED there or a VENDOR (Black Diamond) given? That decides engineering vs procurement.**

---

## 5. PRODUCER SUBSTITUTION — the act LEG A actually is
- Live legacy chain: **`D_01.partner_analytics.py`** → `gold/artifacts/partner_analytics/header_metrics_{gran}.json`
  → **`D_04.client_portal_summary.py:1878 build_partner_analytics()`** → the three served keys.
- Served key LastModified **`2026-08-12T05:26:38Z`** (comp-freshness PASS, 9.8h, no cadence entry → default daily).
- ⭐ The role_aua snap at **05:05:46Z** sits **21 minutes before** the 05:26:38Z served write — independent
  corroboration of both the chain and its daily window.
- **CTO RULED:** substitution belongs in P4, is **ONE ATOMIC ACT** (enable new AND disable legacy in the same
  window — never both live, never a gap), and **the never-widen parity is a PRECONDITION of it, not a follow-up.**
  One-producer-per-served-key forbids coexistence.

---

## 6. BANDS (pre-evidence discipline held throughout)
`V28-PA-TAX` · `V29-PA-GEO` · `V30-PA-OFC` (new narrow row CITING D10, never widening it) · `V31-PA-NMNC`
· `V32-PA-LIVE` (48 exact-keyed aggregate pins) · `V33-PA-PREFLOOR` — all @78156a9283/@459434341d/@ca97f33247.
`V34-PA-CLIENT-NAME-GRAMMAR` @33f7d47009 — registration-name authority vs BD curated display (the V14-CD-NAME
class scoped here); **no title-case/household transform invented.**
⛔ **THE UNBANDED AXIS — the instrument finding:** a **SHAPE-FREEZE PASS is blind to ROW-SET identity and LABEL
SEMANTICS**, and a **VALUE PIN CANNOT SEE A POPULATION CHANGE.** V32's 48 sums would have passed the 35-advisor
exposure through silently. My own `A5-D13-SHAPE-FROZEN` and `A5-D13-ATTRIBUTION-MEASURED` rows are both true and
both insufficient — recorded against my own instance. **The EXPOSURE axis has no band for this family.**
CVO's V22 names the class elsewhere ("by_adv top-9 curation difference"). **INFERRED:** every curated-population
family shares it; I have measured only mine.

---

## 7. STATE AT REBOOT / RESUME CHECKLIST
**HELD, release held by CTO + COO:** LEG A, on (a) population 9 vs 15 with the role_aua basis mechanism above,
(b) the two-identity-systems fact. **NOT held on the 35-advisor exposure or hash-labels — both discharged.**
**HELD, release COO:** LEG B (`mix_summary`) behind the in-flight `_RE_FI` classifier fix.
**HELD, release ANDREW:** cot keys (outside his cutover word per CTO's scope limit; shape-frozen on legacy basis
pending the four-row sovereign bundle) · the `$113.2M` curation act · **P5 teardown of the old root (unrecoverable,
never authorized by "proceed with the cutover")**.
**NEXT 3 ACTS on resume:** (1) the `client_dimension.parquet` producer hop (engineering vs procurement);
(2) `comp-routes trace --json` for the 3 served keys — the router path I have refused to assert all afternoon;
(3) LEG A population on whatever basis CTO rules.
**QA artifacts (SESSION-LOCAL, DIE AT REBOOT — re-derivable from the emitter + the frozen mirror, and every
number above is reproducible from committed code):** `scratchpad/cot_gold_qa/platinum/firm/*.json`,
`scratchpad/served_trio/*.json`, `scratchpad/d13_fits/`.

-- 0.4.0_DS_ClientPlatform~B
