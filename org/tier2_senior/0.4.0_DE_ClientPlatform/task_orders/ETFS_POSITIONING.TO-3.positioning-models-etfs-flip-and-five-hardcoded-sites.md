# TO ETFS_POSITIONING.TO-3 — the Positioning MODELS↔ETFS FLIP + the five hardcoded `'UST'` sites

<task_order id="ETFS_POSITIONING.TO-3" project="ETFS_POSITIONING">
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — cells ETFS-f-1, ETFS-f-2, ETFS-f-3, ETFS-f-4 (boundary ETFS-f-5)</decomp_ref>
<certification>⛔ **UNCERTIFIED DECOMP.** Cut before `3.0.0_SA_CVO` certified the stage-3 decomp, under Andrew's 19:3xZ priority word and CTO's explicit instruction to cut UNCERTIFIED-on-face rather than idle a seat. Permitted, disclosed by the issuer, never silent.</certification>
<issued_to>DE-class (portal plane). Seated: `0.4.0_DE_ClientPlatform` — plane (f) read complete at 65572 / 65652.</issued_to>
<executor_class>DE-class</executor_class>
<seating_trigger>SEATED NOW. Class dark mid-execution → spawn call routes to MSTR SAME-TURN.</seating_trigger>
<placement>LAPTOP (Rule 26). Portal is a WORK-SITE, never a base — address it as `git -C portal ...` or a scoped `cd portal && <work> && cd -`, and return to the workspace root. **A lingering portal CWD silently substitutes the wrong repo's git history into evidence pulls, with no error.**</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-21T19:55Z</issued>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_ETFS_POSITIONING_TO1_TO2_TO3_TO5_CERTIFICATION_20260828.md` @`e3d86ad9d1`, verdict **CERTIFIED -- 6 of 6 PASS**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**

⚠ **THE ORIGINAL `<status>` CONTENT FOLLOWS, RESTORED VERBATIM.** `2.0.0_SA_COO~Z` replaced it wholesale at @4253643625 instead of appending, destroying evidence on seven faces (142 lines on one of them). Recovered from `4253643625^` and re-attached. **NOTHING BELOW THIS LINE IS NEW; NOTHING ABOVE IT WAS IN THE ORIGINAL.**

queued -- for `3.0.0_SA_CVO~Z` CERTIFICATION. **NO EXECUTOR ACT IS PENDING AND NO SEAT IS NEEDED.**

⛔ **`queued` IS NOT A DISCHARGE CLAIM.** The acceptance criteria on this TO were **NEVER CERTIFIED**,
and this office will not buy a terminating register by asserting one. **The lead word says only what is
true: the build is done in the world and the next act is a CERTIFICATION, which belongs to
`3.0.0_SA_CVO~Z` and to no executor.**

**RE-FACED 2026-08-28 ~04:0xZ by `2.0.0_SA_COO~Z` (issuer). WHY THE LEAD WORD CHANGED, AND IT IS A
DEFECT THIS OFFICE ALREADY FIXED ONCE TONIGHT AND DID NOT CARRY ACROSS:** this face led with an emoji
(or a bare word), so `to-check.py` -- which classifies on the FIRST TOKEN ONLY -- read it **`ACTIVE`**.
⛔ **An `ACTIVE` face is an instruction to spend a seat**, and the seat it named is DEAD: `<issued_to>`
carries a BASE serial (`0.4.0_DS_ClientPlatform` / `0.7.0_AE_CloudOps` / `0.4.0_DE_ClientPlatform`) and
**no base serial is registered** -- only lettered lanes are live. **The same lead-word defect was fixed
on `ETFS_POSITIONING.TO-4` earlier tonight and NOT applied to its four siblings.**

⚠ **`<issued_to>` IS DELIBERATELY LEFT UNCHANGED.** It is the historical record of who executed this,
and rewriting it would erase that. **It is NOT a live assignment and must not be read as one.**

---

**ORIGINAL STATUS, PRESERVED VERBATIM BELOW:**

BUILD COMPLETE — cell-level: `ETFS-f-1` DONE (flip renders, exercised) · `ETFS-f-2` DONE (12 in-plane membership sites derive, not 5 — see below) · `ETFS-f-3` PROVEN (Models byte-identical, identical sha256 across all four view modes, mutant-controlled) · `ETFS-f-4` DONE against AE CONTRACT v1 (v1.1 read: moves HOW THE MINT LANDS, not key/shape/AC3) · `ETFS-f-5` UNTOUCHED (0 lines diff, mechanically verified).
Portal DEV @ee90fa8edbf12dcdfbf64e14389f72251a23c06a — **LANDED LOCAL, rides MSTR's integration window** (`git branch -r --contains` returns EMPTY; a direct push was attempted and correctly BLOCKED by the LD-0367 integrator-only gate). Typecheck rc=0 via `bun run typecheck`, instrument proven able to fail first. proof-of-spec VALID rc=0, 6/6 rows, 0 violations.
⛔ **NOT YET LIVE END-TO-END, AND THE BLOCKER MOVED WHILE I BUILT:** the `platinum/etfs/*` bucket-policy ARN has LANDED, so the blocker is no longer the S3 grant — it is that the `public-data-router` branch + the `qualified_arn` pin drop are COMMITTED BUT NOT DEPLOYED, so `/api/general/etfs/` still falls through to `/json/`. Verified harmless: `json/etfs/positioning_data.json` is a 404, so the route ERRORS rather than silently serving the MODELS book family under the ETF flip.
READY FOR DT HANDOFF once the integration push lands (DT's fence condition — `origin/DEV` reads `3ade1aba` or later — is MET by this commit's parent).
⭐ **`ETFS-f-3` (Models BYTE-IDENTICAL) INDEPENDENTLY RE-CLOSED 2026-08-28 ~01:5xZ BY `1.0.0_SA_CTO~Z` — BY CONSTRUCTION, WHICH IS THE STRONGER CLAIM THAN THE RENDER DIFF.** All 8 mode-conditional sites enumerated (5 `isEtfs`, 3 `mode === 'satellites'`): **every one is ADDITIVE** — each gates a query or renders an EXTRA element, and **not one mutates the Models render path**. And the data selector `:240 dataByMode[mode]` is a **MODE-KEYED TOTAL LOOKUP, not a boolean**: *the Models branch is not reached by elimination, it is addressed by key.* ⭐ `Positioning.tsx:161-170` documents why in its own words — a two-valued boolean over a now-three-valued axis *"silently binds every future mode to the `else` branch, so satellites would have rendered the MODELS payload under the MODELS page description while the pill said Satellites — a wrong answer wearing the right label, with a clean build."* **That is Rule 24 totality vindicated in production code.**
⛔ **SO THE ONLY REMAINING ACT ON THIS TO IS A DEPLOY, NOT A BUILD OR A MEASUREMENT:** the `public-data-router` branch + the `qualified_arn` pin drop are **COMMITTED BUT NOT DEPLOYED**. ⚠ **AND IT IS THE SECOND COMMITTED-NOT-DEPLOYED EDGE CHANGE ON THIS ESTATE TONIGHT** — the satellites route (`shared-advisor-router`, `POSN_TENANCY.TO-4-AE`) is the other. **A DIFFERENT ROUTER, POSSIBLY THE SAME DISTRIBUTION**, and this estate's standing constraint is **ONE APPLIER PER MODULE**. **Whoever is seated for either apply MUST establish whether the two changes share a distribution before applying — they must not be applied blind by two seats.**</status>

## ⛔⛔ STALE BLOCKER RETIRED — MEASURED AT THE **APPLIED** PLANE 2026-08-28 15:0xZ

**Measured by `3.0.0_SA_CVO~Z` (msg 13264) on the DEPLOYED edge artifact, not the desired plane.
Recorded here by `2.0.0_SA_COO~Z` (the COO office issued this TO, so the face is this office's to
correct). `3.0.0_SA_CVO~Z` deliberately did NOT edit it.**

```
THIS FACE SAID           a router/deploy blocker was outstanding
MEASURED 15:0xZ          distribution EVTSA9VEHNZVH, Status Deployed, 27 behaviors
  /api/scoped/satellites/*  IS behavior #27; shared-advisor-router pinned :25, NOT :24
  public-data-router:7 DEPLOYED BYTES (pin resolved BY CONTENT -- downloaded + unzipped,
  never inferred from a version number, per Rule 22a):
      else if (b.uri.startsWith("/api/general/etfs/")) -> "/platinum/etfs/"
      else if (b.uri.startsWith("/api/general/"))      -> "/json/"
  >> THE etfs BRANCH IS ORDERED BEFORE THE CATCH-ALL, so the described fall-through CANNOT occur.
  CONTROLS: etfs 3 / json-tiered 3 / general 10 POSITIVE; satellites 0 / positioning 0 NEGATIVE
            -- the probe DISCRIMINATES; it is not matching everything.
  qualified_arn pin drop: all five routers read DYNAMIC qualified_arn [OK].
```
⭐ **THE ONE-APPLIER HAZARD THIS FACE RAISED IS MOOT:** `list-distributions` returns **EXACTLY ONE**
distribution, so the two router changes necessarily shared it. **The hazard was real when written and
is now settled by measurement.**

⚠ **DIRECTION, STATED: THIS FACE WAS *PESSIMISTIC*, WHICH IS THE SAFE DIRECTION.** It over-stated a
blocker rather than under-stating one, **and a pessimistic face announces itself the moment anyone
measures.** It was TRUE WHEN WRITTEN. ⛔ **The general fault is not this face's author: a `<status>`
block is a SNAPSHOT WITH NO FORWARD REFERENCE TO ITS OWN SUPERSESSION.** Two of them were read as live
state inside one hour today.

⛔ **THE RUNG REACHED IS *APPLIED*, NOT *EXERCISED*.** Deployed bytes and live distribution config were
read; **no authenticated request was issued through the route.** `auth-validator-edge:18` sits on both
behaviors, so an unauthenticated curl would 401 and produce a FALSE NEGATIVE. **"A real user is served"
remains unexercised by this measurement.**

⚠ **INSTRUMENT TRAP FOUND WHILE MEASURING, RECORDED BECAUSE IT WILL BITE THE NEXT PIN RESOLUTION:**
```
public-data-router     v7  2026-08-21T21:03:51   v6  2026-08-21T21:20:23
shared-advisor-router  v25 2026-08-28T02:29:53   v24 2026-08-28T02:46:27
```
**On BOTH routers the LOWER-numbered version is NEWER by wall clock.** ⛔ **"version number ascending ==
chronological" is FALSE on this estate, twice, on two different functions.** Cause NOT diagnosed and
none claimed. **Resolve a pin BY CONTENT, never by comparing version numbers.**


<priority>P1 — SESSION PRIORITY (Andrew-direct 19:3xZ). ⛔ **This is the surface Andrew SEES. PRD s.11.1's DONE is a rendered page, not an artifact.**</priority>
<authority>PRD s.11.1 (the DONE — the flip, the four funds, Models byte-identical) + s.5 + s.11.4(f). Rule 19: portal main worktree stays on `DEV`, always.</authority>
<proof_of_spec>
  <!-- ISSUANCE half (COO, at decomposition): the machine-readable criterion-id set.
       Ids are FIRM-TOKENED so they cannot collide across the three parallel ETFS lanes.
       CELL_REFS ARE THE POINT: 3.0.0_SA_CVO's bidirectional alignment check is a JOIN on
       these, not a prose read -- every criterion names the decomp cell it discharges, and
       every criterion-bearing cell is reachable from some criterion. A criterion arriving
       WITHOUT cell_refs is REFUSED, never retrofitted: a retrofitted derivation makes
       alignment LOOK satisfied while being FALSE, and CVO confirmed they would have
       computed exactly that as PASSING.
       COMPLETION half (assignee, from their OWN efforts): a schema-valid instance at the
       path below, validated BEFORE the status flip.
       INVOCATION IS POSITIONAL -- there is NO --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO3-AC1,ETFS-TO3-AC2,ETFS-TO3-AC3,ETFS-TO3-AC4,ETFS-TO3-AC5,ETFS-TO3-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING. The usage banner contains the vocabulary of
       BOTH verdicts ("Exit 0 = VALID"), so a caller grepping for success matches the banner
       of a call that validated NOTHING. rc=0 VALID / rc=1 INVALID / rc=2 usage. And the
       2-arg form (id set omitted) returns a clean rc=0 that says COVERAGE UNCHECKED -- pass
       the ids. -->
    <criterion id="ETFS-TO3-AC1" cell_refs="ETFS-f-2"/>
    <criterion id="ETFS-TO3-AC2" cell_refs="ETFS-f-1"/>
    <criterion id="ETFS-TO3-AC3" cell_refs="ETFS-f-3"/>
    <criterion id="ETFS-TO3-AC4" cell_refs="ETFS-f-4, ETFS-e-2"/>
    <criterion id="ETFS-TO3-AC5" cell_refs="ETFS-f-1"/>
    <criterion id="ETFS-TO3-AC6" cell_refs="ETFS-f-5"/>
  <expected_criteria>ETFS-TO3-AC1,ETFS-TO3-AC2,ETFS-TO3-AC3,ETFS-TO3-AC4,ETFS-TO3-AC5,ETFS-TO3-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ETFS_POSITIONING.TO-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## ⛔ YOUR TWO READS ARE ADOPTED INTO THIS TO — you are not asked to re-derive any of it

Both messages did real work and the TO is shaped around them.

**From 65572 — the five sites, exact `file:line` (`ETFS-f-2`):**
`shared/gridConfig.ts:26` (`PORTFOLIO_ORDER`) · `shared/customBlend.ts:25` (`MODEL_IDS`) · `panels/PositioningSummary.tsx:168` (`portfolios`) · `tabs/HoldingsTab.tsx:648` (`allPortfolios`) · `tabs/HoldingsTab.tsx:779` (`allPortfolios`).

**Your discriminator is ADOPTED AS BINDING, not noted:** *"which of them are ORDER-ONLY versus MEMBERSHIP-CARRYING — an order array tolerates a new member appended, a membership array does not."* **Treat them as two different problems, because they are.**

**From 65652 — the data contract (`ETFS-f-4`), and it is the finding that most changed the decomp:** `getPositioningData` returns **`portfolios: Record<string, PositioningPortfolio>`** (`portal-proxy.ts:1085`) — **arbitrary string keys, not a closed enum.** So the artifact side is already open, and **the five portal lists are the ONLY thing closing the set.** That makes the flip a **portal-side MEMBERSHIP problem end to end.**

### ⛔ COO RULING on what you surfaced — I ruled AGAINST the merged artifact, and the reason changes your Half 2

You correctly flagged that the type would permit adding ETF keys to `positioning_data.json`. **I ruled the ETF artifact SEPARATE** (full reasoning in `ETFS_POSITIONING.TO-2`):

- **"Models mode byte-identical" (PRD s.11.1) is sovereign.** A shared artifact makes byte-identity a property held **by discipline**; a separate artifact makes it true **BY CONSTRUCTION**. ⛔ **CARE IS NOT A CONTROL.**
- It would put **two producers on one served key**, on a **live client-facing page**.

**CONSEQUENCE FOR YOU: ETF mode reads a DIFFERENT artifact than Models mode. `positioning_data.json` is untouched by this project — which is what makes ETFS-TO3-AC3 provable rather than merely intended.** Your corollary survives intact and is Half 1's core: the portal derives ORDER from its own lists, so the positional coupling `value[i] ↔ MODEL_IDS[i]` is **entirely portal-internal — the artifact can neither break it nor fix it.**

## ⛔ SPEC-AT-PICKUP — first act

| # | Premise | Oracle that would FALSIFY it |
|---|---|---|
| O-1 | Five `'UST'` sites in-plane, eleven DEF-band estate-wide | `comp-find -i "'UST'" portal/src/` — **`-i` is MANDATORY: `comp-find` is case-sensitive by default and the dangerous mode is the UNDERCOUNT, which returns a confident non-zero count with NO caveat** |
| O-2 | The contract is `Record<string, ...>` | `grep -n "portfolios" portal/src/api/portal-proxy.ts` |
| O-3 | Portal main tree is on **DEV** | `git -C portal branch --show-current` → **must be `DEV`**; if PROD, `git -C portal checkout DEV` before any work |

## Half 1 — `ETFS-f-2` + `ETFS-f-1`: OPEN THE SET (executable NOW, no dependency)

**This half needs nothing from anyone.** Make the five sites **carry membership rather than assert it** — derive the model list instead of hardcoding it (device-agnostic reasoning, one layer up: **DERIVE, DO NOT HARDCODE**), with order-only and membership-carrying sites handled per your own discriminator.

Then build **the flip** (`ETFS-f-1`) — the Models↔ETFs mode switch. **BUILD-LADDER rung 2 before you write anything new: `portal/src/pages/Positioning/constants/etf-categories.ts` ALREADY EXISTS in the plane.** ETF-shaped code is already resident — read it first. It may also be an input to DS's `sub_asset_class` vocabulary act (TO-1 Half 2); **if it is, one line to CVO — do not coordinate it yourself mid-round.**

**The four funds are DIVZ / IDVZ / PFDE / PFOE.** ⛔ **SHIP SHAPE IS ANDREW'S (PRD s.10.4): TWO FULL BOOKS (PFDE/PFOE) + TWO BOOK-LEVEL SHELLS (DIVZ/IDVZ).** **The page must render the two shells gracefully — a shell is the CORRECT state today, not an error state, not an empty-data bug.** They upgrade forward automatically when constituent rows land. **The page does NOT wait for them.**

## Half 2 — `ETFS-f-4`: READ THE ETF ARTIFACT (anchors on TO-2's contract)

Wire ETF mode to the ETF artifact. **ANCHOR: AE's contract from `ETFS_POSITIONING.TO-2` ETFS-TO3-AC2 — an OBSERVED-completion trigger, not a date.** AE is instructed to ship that contract FIRST, as a one-pager, precisely so you and DS build in parallel.

**Do not idle waiting for it — Half 1 is a full workload and needs nothing.** RQ keys in the plane today: `['positioning-data']` (`Positioning.tsx:40`), `['holdings-attribution']` (`PositioningSummary.tsx:499`).

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO3-AC1** | All five sites derive membership rather than hardcode it; **order-only vs membership-carrying handled distinctly** and which-is-which stated | `ETFS-f-2` | SOURCE |
| **ETFS-TO3-AC2** | The Models↔ETFs flip renders; ETF mode shows **all four funds**, PFDE/PFOE full, **DIVZ/IDVZ as shells rendering GRACEFULLY** | `ETFS-f-1` | **EXERCISED — render it** |
| **ETFS-TO3-AC3** | ⛔ **MODELS MODE BYTE-IDENTICAL.** Proven by a **byte-diff of the Models-mode payload before/after**, not by inspection | `ETFS-f-3` | **EXERCISED** |
| **ETFS-TO3-AC4** | ETF mode reads the ETF artifact per AE's contract; `positioning_data.json` **unmodified** | `ETFS-f-4`, `ETFS-e-2` | EXERCISED |
| **ETFS-TO3-AC5** | **ZERO typescript errors** (the typecheck law) before any promote hand-off | `ETFS-f-1` | MECHANICAL |
| **ETFS-TO3-AC6** | **The six out-of-plane `'UST'` sites are UNTOUCHED** — boundary, out of round 1 | `ETFS-f-5` | SOURCE |

**⛔ ETFS-TO3-AC2 and ETFS-TO3-AC3 are EXERCISED criteria and a grep cannot satisfy either.** Use `/frontend-dev` — render the route headlessly and **READ the screenshot**. **The canvas is SILVER: light text or ghost-white buttons outside a dark Panel are the #1 recurring portal defect, and a grep cannot see contrast.**

## The promote leg is NOT yours, and there is a live fence on it

DT holds the portal promote (`/prod-deploy`, DT lane). **DT has declared a fence: no promote cut until `git ls-remote origin DEV` reads `3ade1aba` or later** — that is Andrew's two-condition ADVI hold expressed at the promote boundary. MSTR pushed to disarm it. **Hand off to DT when Half 1+2 land and typecheck is zero; do not cut a promote yourself.**

## Your banked surprise line — correctly handled, and here is its disposition

The `portal-proxy.ts:1073-1078` *"DEMO MODE … no auth"* comment: **you did exactly the right thing.** You checked the route before sending, found CF behavior 20 `/api/general/*` carries `auth-validator-edge`, and reported **declarative drift** rather than an auth finding — **and you did not elide that `comp-routes` is DESIRED-plane by its own header and you have not exercised an unauthenticated fetch.** That caveat is the difference between a finding and a false alarm on Andrew's top-priority page.

**DISPOSITION: it stays BANKED at CVO. It is OUT of this TO.** *(A stale comment on the very file this project touches is worth having on the record precisely because a seat reading it during ETFS work could reasonably conclude the page is on a public endpoint and act on it — which is why it was worth reporting and is not worth chasing mid-round.)* The non-ASCII marker at `:1073`: same disposition — mentioned once, not chased.

## Surprise channel · Reporting

`3.0.0_SA_CVO` owns the channel. **OBSERVATION never interrupts** (one line, keep working); **BLOCKING** routes same-turn to me, cc CVO; **ARMED** needs a named disarm owner same-turn; DISARMED ≠ REMEDIATED. **Mid-round the spec is FROZEN.**
**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN.** Status is CELL-level.
**EVERY REPORT OF A COMMIT STATES ITS PUSH STATE** — you adopted this unilaterally at 65588 and CTO has since RULED it fabric-wide. Never bare "landed."
