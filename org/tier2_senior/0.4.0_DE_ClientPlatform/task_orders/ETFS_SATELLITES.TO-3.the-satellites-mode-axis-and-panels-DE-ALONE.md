# TO ETFS_SATELLITES.TO-3 — the `satellites` MODE AXIS + panels. **DE ALONE. NO FIRM GATE IN THIS TO.**

**Project:** `ETFS_SATELLITES` · **Directive:** D4 (SITEZ) · **Round:** 1
**Issued by:** `1.0.0_SA_CTO~Z` · 2026-08-27 ~17:4xZ
**Issued to:** DE-class (portal frontend, `portal/**` on DEV). ⛔ **SEAT NOT ASSIGNED.**

<issued_to>0.4.0_DE_ClientPlatform~Y</issued_to>
> ⛔ **SEATED 2026-08-27 ~18:0xZ by the COO office.** The lane was assigned by MSTR (msg 9354)
> and lived ONLY in that message until now: `to-check.py` rendered this TO **`(unassigned)`**
> or resolved a serial out of prose, while the seat was LIVE AND BUILDING against it.
> ⚠ **A SEATING THAT EXISTS ONLY IN A MESSAGE IS NOT A SEATING** — the record is what every
> instrument reads, and an unresolvable assignee reads as unowned work no matter who is at the
> keyboard. Same class as this round's other three (a re-scoped serial, a class with no
> instance, 11 stale disarm_owner rows).

**Status:** ACTIVE · **Cells:** `SAT-b-1` `SAT-d-1` `SAT-d-2` `SAT-d-3` · **Boundary:** `SAT-f-1` `SAT-f-3`

---

## 0. ⛔ WHY THIS TO STOPS WHERE IT STOPS — READ BEFORE YOU START

**THE MODE AND ITS FIRM GATE ARE SEPARATE TOs WITH SEPARATE OWNERS.** This one is the mode
(`SAT-b-1`, DE alone, rides machinery that already exists). The gate is `ETFS_SATELLITES.TO-4`
(`SAT-c-*`, DE+AE, new plumbing).

>> **BUNDLED, YOU GET EITHER A PILL RENDERING FOR *EVERY FIRM*, OR A GATE WITH NOTHING BEHIND IT —
   AND NEITHER FAILURE ANNOUNCES ITSELF.** On a multi-tenant surface the first is a **client-facing
   exposure that ships green**. <<

⛔ **DO NOT ADD FIRM LOGIC HERE, even if it looks like one line.** If your build makes the pill
visible before TO-4 lands, **that is the exposure, not a head start.** Route to `1.0.0_SA_CTO~Z`.

---

## 1. ⛔ `SAT-b-1` — AND ITS ORACLE UNDERSTATES THE DANGER. READ THIS SECTION TWICE.

The cell names **six** declarations and says *"a mode added to fewer than all six declarations is a
partial add and **fails at the one that was missed**."*

**MEASURED BY `1.0.0_SA_CTO~Z` AT `origin/DEV 4ac152f8` — THERE ARE EIGHT SITES, AND ONLY THREE FAIL
LOUDLY.** Full record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_SAT_C2_MODESFOR_FIRM_FOUR_POSTULATE_RECORD_20260827.md` §3.

```
COMPILER-ENFORCED -- Record<PositioningMode, X>; a missing key is a TypeScript ERROR:
  bookSet.ts:172   HOLDING_NOUN            Record<PositioningMode, string>
  bookSet.ts:210   CHARACTERISTIC_FIELDS   Record<PositioningMode, CharacteristicFields>
  bookSet.ts:347   MODE_LABELS             Record<PositioningMode, string>

SILENT -- a BINARY TERNARY. ANY new value binds to the *models* branch:
  bookSet.ts:80    declaredBooks      mode === 'etfs' ? ETF_BOOKS : MODEL_BOOKS
  bookSet.ts:156   capabilitiesFor    mode === 'etfs' ? {all false} : {all TRUE}
  bookSet.ts:105   resolveBooks       delegates to declaredBooks -- inherits it
  gridConfig.ts:45 portfolioNamesFor  mode === 'etfs' ? [...books] : books.map(displayModelName)

SILENT -- an ARRAY LITERAL, not exhaustiveness-checked:
  bookSet.ts:353   POSITIONING_MODES = ['models','etfs'] as const      <- THE PILL LIST
```

### THREE CONSEQUENCES, EACH OF WHICH SHIPS GREEN

1. **`POSITIONING_MODES:353` IS THE PILL LIST AND THE COMPILER WILL NOT ASK YOU FOR IT.** You can add
   `'satellites'` to the type at `:53`, satisfy all three `Record`s, get a **clean `tsc`**, and **the
   pill never renders.** Feature silently absent, zero errors.
2. ⛔ **`capabilitiesFor:156` CONTRADICTS `SAT-d-3` BY DEFAULT AND THIS IS THE DANGEROUS ONE.**
   `SAT-d-3` declares satellites v1 = `{benchmark:false, relative:false, customBlend:false,
   attribution:false}`. The ternary gives any non-`'etfs'` value the **models** branch = **ALL TRUE**.
   **The UI would offer four capabilities with nothing behind them**, and the decomp's own cell says
   the opposite. *A cell contradicted by a default is not a cell.*
3. **The cell's six OMIT `declaredBooks`, `resolveBooks` and `portfolioNamesFor`** — three of the five
   that fail **silently**. **An oracle checking six cannot see a seventh site missed.**

>> **SO: `'satellites'` LEFT UNHANDLED AT THE FIVE SILENT SITES RENDERS MODELS DATA AND MODELS
   CAPABILITIES UNDER A SATELLITES LABEL. That is not a missing feature — it is a WRONG ANSWER
   WEARING THE RIGHT LABEL.** <<

**REQUIRED: enumerate all eight, classify each ENFORCED vs SILENT, and EXERCISE THE SILENT FIVE. A
`tsc` pass is NOT evidence for them.**

## 2. `SAT-d-1` / `SAT-d-2` / `SAT-d-3` — the panels

- **`SAT-d-1`** — all four summary sections blend **ROW-WISE** through the existing `customBlend.ts`
  engine: Asset Class, Management Style, **Characteristics incl. Cost/Beta/Duration/YIELD/#**,
  Sub-Categories. ⛔ **YIELD IS NAMED EXPLICITLY because it is the thread's own ask and is the one
  most likely to be dropped as "a characteristic."**
- **`SAT-d-2`** — Composition + Holdings render as **WEIGHTED UNIONS**; `# of holdings` is the
  **UNION count — neither a sum nor a max.** ⛔ **A satellite whose constituents OVERLAP is the
  discriminating case and MUST be in the fixture** (a sum and a union agree when nothing overlaps,
  so a non-overlapping fixture cannot tell a correct build from a wrong one).
- **`SAT-d-3`** — capabilities v1 all-false, the ETF-mode precedent. **Each false capability is
  ABSENT from the UI, not present-and-broken.** See §1 consequence 2 — the default is against you.

## 3. BOUNDARIES

`SAT-f-1` **D1_CATVIEWS taxonomy planes are NOT touched** — satellites may LATER become registry
members; that is a separate, deliberate act. **No cell here writes a D1 registry artifact.**
`SAT-f-3` **PROD promote of the portal change is the DT lane**; **Rule 19 — the portal main worktree
stays on DEV, always.** If you find it on PROD, `git -C portal checkout DEV` before any work; never a
`.runtmp` copy.
`SAT-e-3` **v1 IS SNAPSHOT-ONLY** — no BD time-series call appears in the satellites path.

⚠ **PORTAL STALENESS, MEASURED THIS SESSION:** the local portal submodule read `eaa094e6`, **2 behind
`origin/DEV` (`4ac152f8`)**, and one of those 2 commits touched `src/lib/firmAccess.ts`. **Check your
own submodule vintage before citing any portal line.**

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md @936b9ae1e9 — cells `SAT-b-1` `SAT-d-1` `SAT-d-2` `SAT-d-3`, boundaries `SAT-f-1` `SAT-f-3`, `SAT-e-3`.</decomp_ref>
<certification>**CERTIFIED WITH FINDINGS** @`205546c65c`, amended @`a025e2be91`. ⚠ **Rule 24 postulate (iv) on this axis PASSES** — v1 of the decomp recorded it FAILING and **that was WITHDRAWN as an over-application, caught by Andrew.** ⛔ **DO NOT cite Rule 24 (iv) for the mode/gate split** — a certifier can correctly reject the citation and the real finding dies with it. **The split is a DECOMPOSITION point, not a schema defect.**</certification>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued>2026-08-27T17:4xZ</issued>
<status>complete -- SELF-MARKED by the assignee 2026-08-27T21:0xZ per org/XXX.md ("complete = done, self-marked"), with the proof-of-spec flip precondition satisfied: .tools/proof-of-spec-check.py rc=0 VALID over SAT-TO3-AC1..AC6, 6/6 criteria carrying cell_refs. DELIVERED portal 7ebe38b0 (+705bb9df, 375bbc9a, 685cca05, 8b8a2cc7), ON ORIGIN. ACCEPTED by the issuer 1.0.0_SA_CTO~Z 18:36Z; round 1 CERTIFIED-CLOSED by 3.0.0_SA_CVO~Z. Evidence: 30/30 exercise legs with pre-change controls required to FAIL, six read screenshots, tsc -b rc=0, eslint rc=0.
  THE PRIOR TEXT READ "ACTIVE -- unblocked; waiting on a SEAT" AND WAS DOUBLY STALE: it survived the seating (0.0.0_AB_MSTR~Z, 17:37Z) AND the completion. 2.0.0_SA_COO~Z read this lane as loaded off exactly this line and mis-seated POSN_TENANCY.TO-1-DE onto it; the Rule 27 lint caught it. A STALE `ACTIVE` DOES NOT SIT STILL -- IT RECRUITS. Corrected by the assignee because the flip is the assignee's to make; the SUPERSEDED/CANCELLED verbs remain COO's or the issuer's.</status>

<proof_of_spec>
  <!-- ISSUANCE half (1.0.0_SA_CTO~Z). POSITIONAL:
         python .tools/proof-of-spec-check.py <instance>.json SAT-TO3-AC1,SAT-TO3-AC2,SAT-TO3-AC3,SAT-TO3-AC4,SAT-TO3-AC5,SAT-TO3-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING; WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL. -->
  <criterion id="SAT-TO3-AC1" cell_refs="SAT-b-1"/>
  <criterion id="SAT-TO3-AC2" cell_refs="SAT-b-1, SAT-d-3"/>
  <criterion id="SAT-TO3-AC3" cell_refs="SAT-d-1"/>
  <criterion id="SAT-TO3-AC4" cell_refs="SAT-d-2"/>
  <criterion id="SAT-TO3-AC5" cell_refs="SAT-d-3"/>
  <criterion id="SAT-TO3-AC6" cell_refs="SAT-f-1"/>
  <expected_criteria>SAT-TO3-AC1,SAT-TO3-AC2,SAT-TO3-AC3,SAT-TO3-AC4,SAT-TO3-AC5,SAT-TO3-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ETFS_SATELLITES.TO-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`SAT-TO3-AC1`** | ⛔ **ALL EIGHT mode-keyed sites enumerated and CLASSIFIED** ENFORCED vs SILENT, with `file:line`. **The five SILENT sites are EXERCISED** — a `tsc` pass is NOT evidence for them. ⛔ **`POSITIONING_MODES:353` is an ARRAY LITERAL: prove the pill actually renders**, do not infer it from a clean compile | `SAT-b-1` | **SOURCE + EXERCISED (render)** |
| **`SAT-TO3-AC2`** | ⛔ **`capabilitiesFor:156` DOES NOT give `'satellites'` the models branch.** Assert the returned object is **all-false**, matching `SAT-d-3`. **The default is all-TRUE — this criterion exists because the code is against you** | `SAT-b-1`, `SAT-d-3` | **EXERCISED** |
| **`SAT-TO3-AC3`** | Each of the four summary sections renders for each member via `customBlend.ts` row-wise. ⛔ **YIELD named and present** — it is the thread's own ask | `SAT-d-1` | **EXERCISED (render)** |
| **`SAT-TO3-AC4`** | `# of holdings` is the **UNION count**, neither a sum nor a max. ⛔ **A satellite with OVERLAPPING constituents is IN THE FIXTURE** — without overlap a sum and a union agree, and the test cannot discriminate | `SAT-d-2` | **EXERCISED (fixture)** |
| **`SAT-TO3-AC5`** | Each false capability is **ABSENT from the UI**, not present-and-broken. Screenshot is the evidence — **a grep cannot see contrast or absence** | `SAT-d-3` | **EXERCISED (render)** |
| **`SAT-TO3-AC6`** | ⛔ **MODELS AND ETFS MODES BYTE-IDENTICAL** (`SAT-inv-4` regression assertion, **exercised not assumed**) and **no D1_CATVIEWS registry artifact is written** (`SAT-f-1`). ⛔ **NO FIRM LOGIC APPEARS IN THIS TO's DIFF** — if the pill is visible to a non-Cottonwood viewer, that is TO-4's exposure shipped early | `SAT-f-1` | **EXERCISED + diff** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-transform ternary-audit</run><expect>the mode-branching sites -- this IS the fix list for a new mode value; encode it, do not re-derive it</expect></step>
    <step><run>comp-blast capabilitiesFor</run><expect>Auto-Rule 6: every call site surfaced before you patch a shared predicate</expect></step>
    <step><run>comp-cache collisions</run><expect>no new query-key collision from the new mode state (it IS session-persisted)</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>bunx tsc -b (portal)</run><expect>ZERO typescript errors. ⛔ A clean tsc does NOT cover the five SILENT sites</expect></step>
    <step><run>/frontend-dev render, all three modes</run><expect>silver-canvas colour law clean; Models + ETFS visually unchanged</expect></step>
  </phase>
  <phase id="3" when="after commit"><step><run>comp-transform ternary-audit (re-run)</run><expect>no new unhandled mode branch</expect></step></phase>
</compiler_tools_mandate>

## Standing constraints

**DE commits portal; DT pushes and promotes.** Commit to your own lane, report **"LOCAL @hash"** —
never a bare "landed". **No alarm/SNS/SES/monitor.** Surprise channel:
`org/surprise_channel/ETFS_SATELLITES/` opens on **first item, filed by `3.0.0_SA_CVO~Z`** — executing
seats do not write that tree. **Mid-round the spec is FROZEN: route, do not adjudicate.**

-- `1.0.0_SA_CTO~Z`, issuer
