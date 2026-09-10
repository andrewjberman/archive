# ENDPOINT (L2, `/endpoint --forward`) — **IRPT_BACKEND** — Investor Reporting, ingestion, scoping and execution

**Seat:** `1.0.0_SA_CTO` (L2, CTO only) · **Stamp:** 2026-09-10 ~19:1xZ
**Brief consumed:** `docs/briefs/investor-reporting-ir-bk-brief-20260910.md` @`efa5a94bf1`, **50,647 bytes**,
authored `4.0.0_SA_CRO` 2026-09-10T18:58:22Z. No `generated:` line; the vintage is the commit.
**Counterpart:** `ENDPOINT_FWD_IRPT_FRONTEND_20260910.md` — cut together, cite each other.
**Commission:** Andrew-direct ~18:3xZ (*"the backend etl/multi-tenant/etc investor reporting project"*), macro
`IRPT` in D9, D9 whole to laptop. Records under this seat's deliverables, all committed.
**Project code assigned at this seat (L3 act, mine):** **`IRPT_BACKEND`** — conforms to the contract's project
grammar `^[A-Z]{4}_[A-Z0-9]{3,18}$`; 0 hits across 8,323 files over the register planes (18 binary and 206
ephemeral-floor files disclosed as NOT covered). **Placement: D9 · fabric `laptop`**, both on his word.

⛔ **THIS SUPERSEDES THE UMBRELLA ENDPOINT for this project's half.** The eight ratified ids are PERMANENT and
carried unchanged; the distribution amendment @`58266dab2d` is the source of the ACCEPT-owner column.

⛔⛔ **THIS ENDPOINT INTRODUCES TWO NEW OUTCOMES, `FWD-9` AND `FWD-10`, AND THEY ARE UNRATIFIED.** Andrew
ratified eight at ~17:3xZ. The BK brief carries seven outcomes; the subtraction (§UNCOVERED) shows two of
them are served by NO ratified id. They take the next unused numbers, never a freed one, and **they change
what "done" means for this product — so they go back to him rather than landing on this seat's word.**
Everything else in this document stands on ids he has already confirmed.

⛔ **NO FWD BELOW IS A WAIT.** The one genuine cadence — the mailbox poll under `FWD-9` — is DRIVEN on
demand for its proof and the organic case is the negative arm, per Rule 27's L2 clause.

---

## THE OUTCOMES

```
  FWD-1  An advisor finds the right client and keeps that context across the
         three tabs
         (ACCEPT owned by IRPT_FRONTEND -- see the counterpart)
         THIS       serve a compact directory keyed to the signed-in firm and
         PROJECT    advisor, resolve a selection into the exact permitted account
                    set BEFORE any report is fetched, reuse the daily sources
                    already in hand, and make no provider call per keystroke
         PROOF      duplicate names, cross-firm identifiers, overlapping advisor
                    groups, a narrow account selection, a partly permitted
                    relationship, an entitled terminated client -- each response
                    carries the same authorized-scope fingerprint as every call
                    downstream of it
         SOURCE     BK brief O1; umbrella FWD-1

  FWD-2  A restricted advisor can use every tab and export ONLY within their
         permitted client population
         DONE WHEN  EXERCISED -- an unauthorized request has been replayed and
                    refused
         ACCEPT     an advisor can only ever see, analyze and export the clients
                    they are allowed to; swapping in someone else's client,
                    account, report or download link is refused every time, even
                    for something they looked at earlier; taking a permission
                    away takes effect at once; a relationship with some accounts
                    the advisor may not see is served as exactly the allowed ones
                    or refused outright, never as the whole with rows hidden after
         PROOF      replay authorized and unauthorized requests with swapped
                    firm, advisor, account, relationship, report and PDF
                    identifiers, including a revoked grant against a previously
                    cached report and a previously issued download
         ACCEPT     ** IRPT_BACKEND ** -- server-side enforcement on every route
         OWNER      is this project's
         CROSSES    IRPT_FRONTEND handles the refusal: no protected stale display,
                    honest permission states, and the negative fixtures
         SOURCE     BK brief O1; umbrella FWD-2

  FWD-3  An advisor reads the provider's performance result in an Opal report
         and exports the same result
         DONE WHEN  EXERCISED -- a captured provider response has been carried
                    to a report and an export with its meaning intact
         ACCEPT     the figure the advisor reads is the provider's own figure --
                    same return method, same fee treatment, same dates, same
                    currency -- for exactly the accounts selected and no others;
                    where the provider has no figure, the report says so and
                    why, and never fills the gap by arithmetic of its own
         PROOF      paired native and normalized fixtures for each of the three
                    partners, the exact selected account set, daily-to-period
                    parity where meaningful, missing and annualized history cases
         ACCEPT     ** IRPT_BACKEND ** -- canonical meaning, units and dates are
         OWNER      this project's
         CROSSES    IRPT_FRONTEND renders it; the export is that project's
                    package run by this project's worker
         SOURCE     BK brief O2; umbrella FWD-3

  FWD-4  An advisor obtains a YCharts sensitivity analysis in the same client
         context and exports it
         DONE WHEN  EXERCISED -- an approved report variant has been replayed
                    from a validated input revision through its captured
                    request, job and result chain to the tab and the PDF
         ACCEPT     the advisor gets back the analysis type they asked for, with
                    the settings the vendor actually applied shown as such; an
                    interrupted generation can be picked up rather than started
                    over; a request that may or may not have gone through is
                    never blindly sent again; what the advisor sees in Opal has
                    been checked against what the vendor produced
         PROOF      all three variants, ordered comparisons, effective settings
                    read back, an expired session, a shared-user eviction, a slow
                    or uncertain submission, and a restarted worker; report
                    bytes, hashes, validated sections and source coordinates all
                    available for the same request revision
         ACCEPT     ** IRPT_BACKEND ** -- the chain from validated input to
         OWNER      certified section is this project's
         CROSSES    IRPT_FRONTEND presents the variants and renders the sections
         SOURCE     BK brief O4; umbrella FWD-4

  FWD-5  An advisor sees current holdings organized by models, with the
         underlying securities and unassigned assets preserved
         DONE WHEN  EXERCISED -- dated holdings and model snapshots have been
                    replayed for all three partner firms
         ACCEPT     today's holdings are joined to each firm's model assignments
                    and the result says, for every slice, what kind of number it
                    is -- what the account actually holds, what it has been
                    assigned, or what its model is supposed to hold -- and never
                    passes one off as another; cash, leftovers, unassigned money
                    and things that could not be classified all stay visible
         PROOF      the partner-specific joins, reconciled unique account totals
                    and drill denominators, unresolved models, missing allocation
                    positions, stale assignments, recursive blends and signed
                    values; no model's total is ever shown as a client's holding
         ACCEPT     ** IRPT_BACKEND ** -- join correctness is this project's
         OWNER
         CROSSES    IRPT_FRONTEND draws the drilldown
         SOURCE     BK brief O5; umbrella FWD-5; WS4 child brief @4a1d1ed9aa

  FWD-7  The client directory cannot go quietly stale, and its ceiling belongs
         to the system rather than to the advisor's diligence
         DONE WHEN  EXERCISED -- a DRIVEN exercise on a CONTROLLED CLOCK has
                    shown a refresh landing and a missed refresh being caught
         ACCEPT     a client added or changed at the source shows up here within
                    a bounded time the system enforces; if a refresh is missed,
                    the directory is marked stale rather than quietly served as
                    current; a client who has left stays visible, marked as
                    such, to an advisor entitled to see them
         PROOF      an added client, a changed eligibility and a MISSED trigger,
                    each driven on a controlled clock with the organic case as
                    the negative arm (the umbrella's re-cut form, unchanged)
         ACCEPT     ** IRPT_BACKEND ** -- ingestion, projection and refresh are
         OWNER      this project's
         CROSSES    IRPT_FRONTEND shows the as-of and the capability gap
         SOURCE     BK brief O1 + O7; umbrella FWD-7; Andrew "Stay visible"

  FWD-8  An advisor exports a BRANDED Opal report whose narrative page states
         what was happening in the market at the account's dramatic moves -- as
         CONTEMPORANEOUS CONTEXT, never as a cause of the return
         DONE WHEN  EXERCISED -- a branded export has been produced from a
                    frozen bundle and its narrative page read
         ACCEPT     every fact on the narrative page comes from dated evidence
                    that can be pointed to; the page says what the markets were
                    doing at the account's big moves and never that those events
                    caused the returns; retrying the export reuses exactly what
                    was frozen; changing the branding does not recompute the
                    performance; a download is re-checked for permission even
                    when the file already exists
         PROOF      the same bundle across preview, render and retry; an advisor
                    logo present, absent, inaccessible and invalid; historical
                    gaps; event-date and source-cutoff checks; factual and
                    citation validation; reauthorized download
         ACCEPT     ** IRPT_BACKEND ** -- evidence, prose validity and export
         OWNER      execution are this project's
         CROSSES    IRPT_FRONTEND supplies the rendering package this project
                    executes, and the chart composition on which markers land
         SOURCE     BK brief O6; umbrella FWD-8

  FWD-9  A forwarded holdings email becomes a durable, correctly scoped
         analysis request without anyone re-keying it
         ** NEW -- UNRATIFIED -- AT ANDREW **
         DONE WHEN  EXERCISED -- a real forwarded message with its attachment
                    has become a request an advisor can see and correct
         ACCEPT     an advisor forwards a client's holdings by email during the
                    working day and, within a short time, sees it in Opal as a
                    request with the holdings read out of the attachment,
                    attributed to the right advisor and client, and with anything
                    the system could not read flagged for correction rather than
                    guessed; forwarding the same email twice does not create two
                    requests, and a genuinely new request that happens to carry
                    the same holdings is not thrown away as a duplicate
         PROOF      representative forwarded messages with real attachments,
                    retries, a restart while an attachment is being saved,
                    checkpoint recovery, a repeated forward, a new request with
                    identical holdings, an unresolved owner, ambiguous positions
         ACCEPT     ** IRPT_BACKEND **
         OWNER
         CROSSES    IRPT_FRONTEND consumes the correction state
         SOURCE     BK brief O3
         WHY NEW    the ratified FWD-4 begins "from a validated input revision"
                    and takes that revision AS GIVEN -- nothing ratified grades
                    HOW a forwarded email becomes one. The subtraction below is
                    the record.
         ⚠ CADENCE  the brief names a 15-minute poll from 08:00 to 23:45 New
                    York, every day. That is the BRIEF's number, not ratified
                    here; no accept grades on it at L2. Its proof is DRIVEN.

  FWD-10 An operator can diagnose and recover one tenant's flow without
         corrupting another's result
         ** NEW -- UNRATIFIED -- AT ANDREW **
         DONE WHEN  EXERCISED -- one firm's flow has been deliberately broken
                    and recovered while another firm's stayed correct
         ACCEPT     when something goes wrong for one firm, the person running
                    the system can see exactly what failed and where, fix that
                    one thing, and be certain the fix touched no other firm's
                    results; a failed run never publishes a report that looks
                    complete but is not, never overwrites a newer result with an
                    older one, and never brings back a permission that was taken
                    away
         PROOF      a failed source partition, a stale model map, a duplicated
                    event, an expired lease, a queue replay, a worker restart and
                    a revocation during a job; a manifest names every upstream
                    dependency and its owner
         ACCEPT     ** IRPT_BACKEND **
         OWNER
         CROSSES    IRPT_FRONTEND surfaces the partial, stale and unavailable
                    states through the shared status contract
         SOURCE     BK brief O7
         WHY NEW    the ratified FWD-6 grades the ADVISOR continuing to work; it
                    never grades an OPERATOR recovering a tenant, and no ratified
                    outcome names cross-tenant isolation at all. For a
                    multi-tenant product that is a safety property, not a nicety.
```

**COUNT: 9 outcomes carried. 7 are ratified ids (`FWD-1`, `2`, `3`, `4`, `5`, `7`, `8`); 2 are NEW
(`FWD-9`, `FWD-10`). ACCEPT owner: IRPT_BACKEND 8, IRPT_FRONTEND 1 (`FWD-1`, contributed to here).**

---

## THE UNCOVERED PARTITION — hunted BY SUBTRACTION, and this is where the two new ids come from

**Denominator: the BK brief's 7 outcomes (O1–O7).** Subtract those a ratified id serves:
O1→FWD-1 + FWD-2 · O2→FWD-3 · O4→FWD-4 · O5→FWD-5 · O6→FWD-8 · O7's directory-refresh half→FWD-7.
**7 minus 5 (whole) minus 1 (half) leaves O3 wholly uncovered and O7's diagnosability-and-isolation
half uncovered.** Those are `FWD-9` and `FWD-10`.

⛔ **WHY MY DISTRIBUTION AMENDMENT DID NOT FIND THESE, AND WHY THAT MATTERS.** That amendment asked *where
do the eight belong*. It never asked *what do the briefs contain that the eight miss*. Distributing a fixed
set across two projects is a partition of the set; it is structurally unable to see a member outside the
set. **Only a subtraction from the BRIEF's own denominator can.** Andrew asked whether I had run this
phase; I had not, and this section is the difference.

**The reverse subtraction — ratified ids the BK brief does NOT serve: `FWD-6`.** Advisor-facing
degradation is IRPT_FRONTEND's; BK contributes the status contract inside O7. Not uncovered; owned elsewhere.

## WHAT L2 DOES NOT DECIDE

Cells, owners, sequencing, lanes (L5/L6). Every number the brief names — the 15-minute poll, session
recovery bounds, retry counts — is the brief's proposal and is MEASURED then declared downstream, never
ratified at L2. Which shared contracts change and how (BK §II.3 is the inventory). Whether the YCharts
runner reuses the named pattern (an L5 build choice). Any live vendor call. **Nothing here authorizes
egress.**

## WHERE THIS LANDS (F4) — **NOT YET LANDED**

Ready to paste under **`## ENDPOINT (step 2, /endpoint --forward)`** in
`org/missions/D9/IRPT/IRPT_BACKEND/prd/IRPT_BACKEND_PRD.md`. **That path does not exist.** Same three
prerequisites as the counterpart: `MACROS.yaml` D9 `[IRPT]` landed; the D9 `LAPTOP` flip; the register row.
**Plus one this side alone carries: `FWD-9` and `FWD-10` must be RATIFIED or REFUSED by Andrew before the
PRD header's `endpoint_outcomes` can list them.** A PRD may land with the seven ratified ids and take the
two on his word; it may not list an unratified id as if he had confirmed it.

## PROVENANCE (F5)

**GROUNDED ON:** `docs/briefs/investor-reporting-ir-bk-brief-20260910.md` @`efa5a94bf1` lines 1–64 (the seven
outcomes, read in full) and §II.1–II.3 (ownership, shared owners, contract inventory);
`docs/briefs/investor-reporting-ir-fe-brief-20260910.md` @`efa5a94bf1` lines 1–66 and §II.1–II.2 (every
CROSSES line); the umbrella endpoint's distribution amendment @`58266dab2d`; the umbrella's `FWD-7` driven
re-cut (carried, not re-derived); `org/standards/PROJECT_TREE.contract.json` (the code grammar).
**NOT READ:** the TO register; any `org/projects/*.json`; the nine source documents beneath the brief (its
Part IV maps them); the WS4 child brief's body (cited for `FWD-5`'s lineage only).
