# ENDPOINT (L2, `/endpoint --forward`) — **IRPT_FRONTEND** — Investor Reporting, the advisor-facing product

**Seat:** `1.0.0_SA_CTO` (L2, CTO only) · **Stamp:** 2026-09-10 ~19:1xZ
**Brief consumed:** `docs/briefs/investor-reporting-ir-fe-brief-20260910.md` @`efa5a94bf1`, **30,287 bytes**,
authored `4.0.0_SA_CRO` 2026-09-10T18:58:22Z. No `generated:` line; the vintage is the commit.
**Counterpart:** `ENDPOINT_FWD_IRPT_BACKEND_20260910.md` — the two are cut together and cite each other, because
both briefs say the ACCEPT owner is named here and *"not requiring each proof to fit wholly within one project."*
**Commission:** Andrew-direct ~18:3xZ (*"the frontend and client facing investor reporting project"*), macro `IRPT`
in D9 (~18:3xZ), D9 whole to laptop (~18:5xZ). Records under this seat's deliverables, all committed.
**Project code assigned at this seat (L3 act, mine):** **`IRPT_FRONTEND`** — conforms to the contract's project
grammar `^[A-Z]{4}_[A-Z0-9]{3,18}$`; 0 hits across 8,323 files over the register planes (18 binary and 206
ephemeral-floor files disclosed as NOT covered). **Placement: D9 · fabric `laptop`**, both on his word.

⛔ **THIS SUPERSEDES THE UMBRELLA ENDPOINT** `ENDPOINT_FWD_INVESTOR_REPORTING_LIGHTWEIGHT_20260910.md` **for this
project's half.** That document described ONE project Andrew has since split. Its eight ratified ids are
PERMANENT and are carried here unchanged; its distribution amendment (@`58266dab2d`) is the source of the
ACCEPT-owner column below and is not re-derived.

⛔ **FWD-n IDS ARE PERMANENT AND NEVER REUSED.** Every id below is one of the eight Andrew ratified at ~17:3xZ.
**This endpoint introduces NO new outcome.** The FE brief's six outcomes map one-to-one onto six ratified ids
(the subtraction is in §UNCOVERED). Two NEW outcomes surfaced on the BACKEND side and live in the counterpart.

⛔ **NO FWD BELOW IS A WAIT.** Every one is provable by an act a seat can take ON DEMAND.

---

## THE OUTCOMES

```
  FWD-1  An advisor finds the right client and keeps that context across the
         three tabs
         DONE WHEN  EXERCISED -- an advisor who has never used it has searched,
                    picked a client, and been shown the relationship and the
                    accounts they are permitted to see
         ACCEPT     typing a client's name finds the right one even when two
                    clients share a name; the advisor sees exactly the accounts
                    they are allowed to see and nothing more; switching between
                    the three tabs keeps the same client open; a client who has
                    left the firm still shows up, marked as such, if the advisor
                    is entitled to see them; a report that has not finished
                    loading does not stop the advisor from searching
         PROOF      a fixture with duplicate names, direct account entry, a partly
                    authorized relationship, a terminated-but-entitled client,
                    keyboard navigation, and a client switch during an outstanding
                    request; the screen shows exactly the returned scope, rejects
                    a stale response, and makes no vendor call per keystroke
         ACCEPT     ** IRPT_FRONTEND ** -- the accept is an exercised advisor
         OWNER      journey and "keeps the same client across tabs" is selection
                    state, which this project owns
         CROSSES    IRPT_BACKEND supplies the permitted account set, the
                    directory's as-of date, and the guarantee that search makes
                    zero vendor calls -- observed here, enforced there
         SOURCE     FE brief O1; umbrella FWD-1; Andrew "Stay visible" (~17:3xZ)

  FWD-3  An advisor reads the provider's performance result in an Opal report
         and exports the same result
         DONE WHEN  EXERCISED -- an advisor has read the provider's figure here
                    and exported it
         ACCEPT     the numbers on screen mean what the provider meant them to
                    mean -- the same return method, the same fee treatment, the
                    same dates -- and nothing has been recomputed or averaged on
                    the way; where the provider has no figure the screen says so
                    instead of showing a zero; refreshing and exporting are two
                    different buttons
         PROOF      render one normalized contract for all three partner fixtures,
                    including partial scope, differing returned dates and
                    unavailable metrics; compare labels, units, chart endpoints
                    and account rows to IRPT_BACKEND's certified fixtures; this
                    project neither recalculates a return nor parses a raw
                    provider response
         ACCEPT     ** IRPT_BACKEND ** -- a parity claim from capture through
         OWNER      export; canonical meaning is that project's
         THIS       presentation: labels, units, method and coverage notes, chart
         PROJECT    endpoints and account rows match the certified fixture
         SOURCE     FE brief O2; umbrella FWD-3

  FWD-4  An advisor obtains a YCharts sensitivity analysis in the same client
         context and exports it
         DONE WHEN  EXERCISED -- an advisor has obtained an approved analysis
                    variant for the client already open and exported it
         ACCEPT     the advisor can ask for any of the three analysis types for
                    the client they already have open, see what the system read
                    out of their request, correct anything it could not resolve,
                    and get the analysis back in Opal's own presentation rather
                    than as an embedded vendor page; a correction never overwrites
                    what was originally submitted
         PROOF      all three variants, comparison order, dollar versus weight,
                    cash, ambiguous share classes, unsupported holdings, a
                    recoverable session interruption and an uncertain submission;
                    stage evidence shown without invented progress figures; each
                    native section compared to its paired vendor-output fixture
                    before it is called supported
         ACCEPT     ** IRPT_BACKEND ** -- the accept replays a validated input
         OWNER      revision through the request, job and result chain
         THIS       the variant and input-review screens, request history and
         PROJECT    status, and the native sections as rendered
         SOURCE     FE brief O3; umbrella FWD-4

  FWD-5  An advisor sees current holdings organized by models, with the
         underlying securities and unassigned assets preserved
         DONE WHEN  EXERCISED -- an advisor has drilled from a client's models
                    down to the securities inside them
         ACCEPT     the advisor sees today's holdings grouped by model, can drill
                    into any slice, and every slice says what it is a share of;
                    money that belongs to no model is shown as such rather than
                    hidden or squeezed in; the picture is never forced to add up
                    to a hundred percent when it does not; what a model is
                    supposed to hold and what an account actually holds are shown
                    as two different things
         PROOF      drill an observed allocation, an account assignment and a
                    target-based blend, plus a cash remainder, an unknown
                    category, a duplicated relationship membership and a stale
                    overlay; summary and drill stay bound to one scope and one
                    revision and keep every qualifier
         ACCEPT     ** IRPT_BACKEND ** -- the accept turns on join correctness
         OWNER
         THIS       radial and category presentation, drill navigation, legends,
         PROJECT    table equivalents and coverage display
         SOURCE     FE brief O4; umbrella FWD-5

  FWD-6  An advisor can keep working when one report is unavailable, and can
         tell the age of each result
         DONE WHEN  EXERCISED -- a provider has been deliberately failed and an
                    advisor has kept working
         ACCEPT     when one report cannot be produced the other two tabs still
                    work; the advisor can see how old each result is; a failed
                    analysis does not wipe out holdings or lock the client
                    search; switching clients never leaves the previous client's
                    data on screen; an incomplete result is never dressed up as
                    a complete one showing zeros
         PROOF      controlled failure fixtures and out-of-order responses,
                    including expiry and revocation on a warm cache; unaffected
                    functions stay usable
         ACCEPT     ** IRPT_FRONTEND ** -- the accept is continued use under
         OWNER      degradation, which is this project's recovery views
         CROSSES    IRPT_BACKEND supplies the status states and the ages this
                    project renders
         SOURCE     FE brief O6; umbrella FWD-6

  FWD-8  An advisor exports a BRANDED Opal report whose narrative page states
         what was happening in the market at the account's dramatic moves -- as
         CONTEMPORANEOUS CONTEXT, never as a cause of the return
         DONE WHEN  EXERCISED -- an advisor has exported a branded report and its
                    narrative page has been read
         ACCEPT     the downloaded report looks like the preview, carries the
                    branding the advisor chose, and its market-context page
                    describes what was going on in the markets at the account's
                    big moves without claiming those events caused the returns;
                    a missing logo never blocks the report; changing the branding
                    does not re-fetch the performance
         PROOF      preview against downloaded PDF per report type, with and
                    without advisor assets and narrative; long names, varied logo
                    ratios, long tables, missing narrative history, partial
                    sections; embedded fonts, labels, page breaks, footnotes;
                    every quoted fact comes from the frozen bundle
         ACCEPT     ** IRPT_BACKEND ** -- evidence and prose validity, and the
         OWNER      export execution, are that project's
         THIS       the template and rendering package that IRPT_BACKEND
         PROJECT    executes, chart composition, annotation and footnote
                    placement, and preview-to-PDF parity
         SOURCE     FE brief O5; umbrella FWD-8; Andrew's export extension
```

**COUNT: 6 outcomes carried, 6 of 6 are ratified ids. ACCEPT owner: IRPT_FRONTEND 2 (`FWD-1`, `FWD-6`),
IRPT_BACKEND 4 (`FWD-3`, `FWD-4`, `FWD-5`, `FWD-8`).**

⛔ **A PROJECT WHOSE "DONE" INCLUDES FOUR OUTCOMES ANOTHER PROJECT GRADES IS NOT A DEFECT; IT IS THE
SPLIT ANDREW ORDERED, STATED HONESTLY.** IRPT_FRONTEND is CLOSED when its two owned outcomes grade
REALIZED **and** its contribution to the four crossing outcomes is graded as met by IRPT_BACKEND's
adjudication. Pretending the four belong wholly here would let this project close on a render nobody
has certified against the data behind it.

---

## THE UNCOVERED PARTITION — hunted BY SUBTRACTION

**Denominator: the FE brief's 6 outcomes (O1–O6).** Subtract those mapped to a ratified id above:
O1→FWD-1, O2→FWD-3, O3→FWD-4, O4→FWD-5, O5→FWD-8, O6→FWD-6. **6 minus 6 = 0 uncovered on this side.**

**The reverse subtraction — ratified ids the FE brief does NOT serve: `FWD-2` and `FWD-7`.** Both are
backend-owned (authorization enforcement; directory freshness). FE's brief names their VISIBLE halves
inside O1 and O6 rather than as outcomes of their own, which is correct: FE contributes *"correct
response handling, no protected stale display, UI permission states"* to FWD-2 and *"displays the as-of"*
to FWD-7. **They are not uncovered; they are owned elsewhere and contributed to here.** The counterpart
carries them.

## WHAT L2 DOES NOT DECIDE

Cells, owners-per-cell, sequencing, lane suffixes (L5/L6). Latency and TTL numbers. The shared contract
schemas (BK's §II.3 inventory is the source; a change needs matching producer and consumer fixtures).
Which analysis sections are "supported" (paired fixtures decide, per outcome). Any live vendor call.

## WHERE THIS LANDS (F4) — **NOT YET LANDED**

Ready to paste under **`## ENDPOINT (step 2, /endpoint --forward)`** in
`org/missions/D9/IRPT/IRPT_FRONTEND/prd/IRPT_FRONTEND_PRD.md`. **That path does not exist.** It needs, in
order: `MACROS.yaml` D9 `[IRPT]` landed by `0.0.0_AB_MSTR` (record exists @`643116f787`, ratification
already given); the D9 `LAPTOP` flip; the register row for `IRPT_FRONTEND`. Until then this endpoint lives
here, at the seat that cut it, and says so.

## PROVENANCE (F5)

**GROUNDED ON:** `docs/briefs/investor-reporting-ir-fe-brief-20260910.md` @`efa5a94bf1` lines 1–66 (the
six outcomes, read in full) and §II.1–II.2 (the ownership table and the handoff contracts);
`docs/briefs/investor-reporting-ir-bk-brief-20260910.md` @`efa5a94bf1` lines 1–64 and §II.1–II.2 (for
every CROSSES line); the umbrella endpoint's distribution amendment @`58266dab2d`;
`org/standards/PROJECT_TREE.contract.json` (the code grammar, read from the contract and not from prose).
**NOT READ:** the TO register; any `org/projects/*.json`; the umbrella endpoint's original outcome text
except to carry ids; the nine source documents beneath the brief (the brief's Part IV maps them and I did
not re-derive that map).
