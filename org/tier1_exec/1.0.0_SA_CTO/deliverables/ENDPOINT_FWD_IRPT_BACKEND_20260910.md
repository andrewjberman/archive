# ENDPOINT (L2, `/endpoint --forward`) — **IRPT_BACKEND** — Investor Reporting, ingestion, scoping and execution

**Seat:** `1.0.0_SA_CTO` (L2, CTO only) · **Stamp:** 2026-09-10 ~19:1xZ · **Re-cut ~19:2xZ** (see the ⛔ block)
**Brief consumed:** `docs/briefs/investor-reporting-ir-bk-brief-20260910.md` @`efa5a94bf1`, **50,647 bytes**,
authored `4.0.0_SA_CRO` 2026-09-10T18:58:22Z. No `generated:` line; the vintage is the commit.
**Counterpart:** `ENDPOINT_FWD_IRPT_FRONTEND_20260910.md` — cut together, cite each other.
**Commission:** Andrew-direct ~18:3xZ (*"the backend etl/multi-tenant/etc investor reporting project"*), macro
`IRPT` in D9, D9 whole to laptop. Records under this seat's deliverables, all committed.
**Project code assigned at this seat (L3 act, mine):** **`IRPT_BACKEND`** — conforms to the contract's project
grammar `^[A-Z]{4}_[A-Z0-9]{3,18}$`; 0 hits across 8,323 files over the register planes (18 binary and 206
ephemeral-floor files disclosed as NOT covered). **Placement: D9 · fabric `laptop`**, both on his word.

⛔⛔ **RE-CUT ~19:2xZ ON TWO FINDINGS, BOTH CORRECT, BOTH DEFECTS OF MINE.**
**(1) `3.0.0_SA_CVO` 191508Z:** the first cut **PARAPHRASED** the ratified outcomes. `FWD-7`'s proof went from
the ratified FIVE arms (added client, changed eligibility, MISSED trigger, **FAILED refresh, OVER-AGE directory
request**) to THREE, while claiming the re-cut was carried unchanged. `FWD-8` lost the twice-replay
determinism control and the MISSING-HISTORY-versus-empty-list arm. `FWD-2` lost *"revealed nothing"* and the
warm-cache revocation arm's exact form. **A RATIFIED OUTCOME IS CARRIED VERBATIM OR IT IS NOT THE RATIFIED
OUTCOME.** Every `DONE WHEN`, `ACCEPT`, `PROOF` and ratified ⛔/⚠/✅ note on `FWD-1`..`FWD-8` below is now
**character-for-character from the umbrella endpoint @`58266dab2d`**. Only `ACCEPT OWNER`, `CROSSES`,
`THIS PROJECT` and the `SOURCE` suffix are mine; the ratified `OWNER` lines named WS1–WS4, which Andrew
retired, and those are the one thing replaced.
**(2) `4.0.0_SA_CRO` 191505Z:** the first cut's *WHAT L2 DOES NOT DECIDE* said *"whether the YCharts runner
reuses the named pattern (an L5 build choice)"*. **THAT DOWNGRADED ANDREW'S EXPLICIT WORD TO A BUILD CHOICE.**
His words: *"Yeah i would use the same pattern as BDAPI with Kimi"*; then *"use the exact same style of runner,
that strategy works very well. I do not believe they send OTP so dont need that part."* The runner STYLE and
the no-OTP branch are FIXED on his word; L5 chooses YCharts-specific implementation details, never whether to
honor the strategy. Corrected in that section.

⛔⛔ **THIS ENDPOINT INTRODUCES TWO NEW OUTCOMES, `FWD-9` AND `FWD-10`, AND THEY ARE UNRATIFIED.** Andrew ratified
eight at ~17:3xZ. The BK brief carries seven outcomes; the subtraction (§UNCOVERED) shows two are served by NO
ratified id. They take the next unused numbers, never a freed one, and **they change what "done" means for this
product — so they go back to him rather than landing on this seat's word.**

⛔ **NO FWD BELOW IS A WAIT.** The one genuine cadence — the mailbox poll under `FWD-9` — is DRIVEN on demand
for its proof and the organic case is the negative arm, per Rule 27's L2 clause.

---

## THE OUTCOMES — `FWD-1`..`FWD-8` ratified text verbatim @`58266dab2d`; `FWD-9`, `FWD-10` new; owner metadata is this cut's

```
  FWD-1  An advisor finds an authorized client and opens its relationship and
         accounts without waiting for a vendor report
         DONE WHEN  EXERCISED -- an advisor who has never used the workspace has
                    searched, selected, and been shown the relationship and its
                    permitted accounts
         ACCEPT     from the header, a search by client name returns an unambiguous
                    selection; the workspace immediately shows the relationship, its
                    permitted underlying accounts, cached context and the directory's
                    as-of; the choice survives a tab switch; an unmapped client stays
                    VISIBLE to an authorized viewer with an explicit capability gap
                    rather than silently missing
         PROOF      a fixture directory carrying duplicate names, an account-only
                    entry and multiple relationships, compared against the expected
                    authorized set; cold and warm timings recorded against the whole
                    captured firm-directory denominator; VENDOR REQUEST COUNT DURING
                    SEARCH IS ZERO. No latency target is invented at L2
         ACCEPT     ** IRPT_FRONTEND ** -- see the counterpart
         OWNER
         THIS       the compact directory keyed to the signed-in firm and advisor;
         PROJECT    resolving a selection to the exact permitted account set BEFORE
                    any report is fetched; the directory as-of; and the guarantee
                    that search makes no provider call per keystroke
         SOURCE     brief O1; Andrew's "search for Clients by name, this routes the
                    tabs" -- carried; BK brief O1

  FWD-2  A restricted advisor can use every tab and export ONLY within their
         permitted client population
         DONE WHEN  EXERCISED -- an unauthorized request has been replayed and
                    revealed nothing
         ACCEPT     firm and advisor rights govern suggestions, selected-account
                    membership, report retrieval, job polling, cached results AND
                    PDF download; a relationship containing an account outside the
                    viewer's permitted population NEVER silently grants that account
                    or its value; a firm-authorized viewer gets the firm's population
                    under the same rules
         PROOF      replay authorized and unauthorized requests with SWAPPED firm,
                    advisor, account, relationship, report and PDF identifiers,
                    INCLUDING A REVOKED GRANT AGAINST A WARM CACHE; the negative
                    requests reveal no protected data
         ACCEPT     ** IRPT_BACKEND ** -- server-side enforcement on every route is
         OWNER      this project's
         CROSSES    IRPT_FRONTEND handles the refusal: no protected stale display,
                    honest permission states, and the negative fixtures
         SOURCE     brief O2; CTO 95142 (entitlement is an OUTCOME, not a property of
                    a search box); CLAUDE.md s.5 cross-firm rule -- carried; BK brief O1
         ⛔ NOTE    THIS IS THE HIGHEST-BLAST-RADIUS OUTCOME IN THE SET. A defect here
                    is a CROSS-FIRM EXPOSURE, and the estate's cross-firm rule is
                    SUBSTRATE-SHAPED with BOTH SHAPES LIVE (bucket-scoped Deny and
                    key-prefix + IAM condition). It is graded on its own, never as a
                    side effect of FWD-1

  FWD-3  An advisor reads the provider's performance result in an Opal report and
         exports the same result
         DONE WHEN  EXERCISED -- a captured provider response has been carried to a
                    rendered view and a PDF at one report revision, for each
                    supported partner and scope
         ACCEPT     for the selected account or relationship and period, vendor-
                    calculated performance appears in a common Opal layout and the
                    PDF carries the SAME scope, returned dates, values, method basis,
                    source attribution and approved disclosures; the UI distinguishes
                    TWR/MWR, net/gross, cumulative/annualized, UNITS and UNAVAILABLE
                    fields; a deliberately incomplete provider mapping yields a
                    PARTIAL or UNSUPPORTED result rather than a full-client claim
         ⛔ UNITS ADDED 2026-09-10, PRE-RATIFICATION, on `4.0.0_SA_CRO`'s WS2
                    delivery and verified at source at this seat. ONE PROVIDER
                    RETURNS THE SAME FIELD NAME IN TWO DIFFERENT UNITS: Orion's
                    summary `calculated-performance.performance` is DECIMAL while the
                    daily breakdown `performance` is PERCENTAGE -- "divide by 100 if
                    used as a daily rate", which the CRO confirmed against
                    `factor - 1` for all 276 daily points. **A normalizer treating
                    both as one unit yields a figure WRONG BY 100x THAT RENDERS
                    CORRECTLY, EXPORTS TO PDF, AND TIES TO NOTHING THAT CATCHES IT.**
                    My accept named method basis, fee basis and annualization and did
                    NOT name units. That omission was mine and it is closed here.
                    **A unit is part of a number's MEANING, not its formatting.**
         PROOF      compare captured request/response, normalized report, rendered
                    view and PDF at one revision per partner and scope; relationship
                    return uses a VENDOR CALCULATION for the exact selected account
                    set -- summing or averaging account returns is not a substitute
                    and a fabricated aggregate fails this outcome
         ACCEPT     ** IRPT_BACKEND ** -- canonical meaning, units, dates and the
         OWNER      vendor-calculation-only rule are this project's
         CROSSES    IRPT_FRONTEND renders it; the PDF is that project's package run
                    by this project's worker
         SOURCE     brief O3, F2, F3; Andrew's "just generating a frontend view of
                    what Black Diamond/Orion already provide" -- carried; BK brief O2
         ⛔ NOTE    A NORMALIZER DOES NOT CHANGE A PROVIDER'S METHODOLOGY TO MAKE TWO
                    NUMBERS LOOK COMPARABLE. Making BD and Orion agree by adjusting
                    one of them fails this outcome even when the layout matches

  FWD-4  An advisor obtains a YCharts sensitivity analysis in the same client
         context and exports it
         DONE WHEN  EXERCISED -- an approved report variant has been replayed from an
                    analyst-approved input through its captured request/job/result
                    chain to the tab and the PDF
         ACCEPT     the advisor selects a supported variant, reviews the holdings or
                    saved-portfolio mapping and comparison model it will use, and
                    receives an Opal-branded analysis and matching PDF preserving the
                    input snapshot, configuration, data dates, limitations and vendor
                    attribution; a MODELED comparison is described as modeled;
                    unsupported variants are VISIBLE as unsupported
         PROOF      replay each approved variant end to end
         ACCEPT     ** IRPT_BACKEND ** -- the chain from validated input to
         OWNER      certified section is this project's
         CROSSES    IRPT_FRONTEND presents the variants and renders the sections
         SOURCE     brief O4, F7; Andrew's "just pulling a report of what YCharts
                    already provides" -- carried; BK brief O4
         ✅ THE EXPRESS QUALIFICATION IS **DISCHARGED**, 2026-09-10. It read: the
                    evidence is gated on ANDREW'S ANALYST handing it over, a named
                    person's decision, so FWD-4 reads NOT_REALIZED with its reason
                    NAMED until it lands. **IT LANDED** -- `4.0.0_SA_CRO`'s WS3
                    delivery @`129fc4a09d` carries six transcripts, 26 hash-matched
                    ZIPs, three HARs at 220/403/462 entries, six POST-201 -> exact-URL
                    GET-200 pairs, and TWELVE cited source hashes re-verified UNCHANGED
                    AFTER the cross-fabric merge. **That closed one of Andrew's open
                    calls from this seat.** The qualification is kept verbatim above
                    rather than deleted: a discharged gate that leaves no trace reads
                    as a gate that never existed
         ⚠ WHAT REPLACED IT, and it is an EVIDENCE GAP rather than a human gate:
                    native section/export parity still needs ACTUAL three-variant PDFs,
                    and upload multipart is missing. Named here AND on FWD-8's export
                    half -- ⛔ **name it in both or it gets closed silently in one**
         ⛔ AND THE REQUEST ARRIVES BY EMAIL, WHICH THIS OUTCOME DID NOT SAY. WS3's
                    intake is a mailbox poller (Andrew-direct: every day, quarter-hour,
                    08:00-23:45 ET, actual holdings attachments). The advisor still
                    OBTAINS and EXPORTS in the tab, so FWD-4's substance holds -- but
                    the request channel is mail, not a click, and a cell must not
                    assume a synchronous request path
                    (this cut: the intake itself is FWD-9 below, at Andrew)
         ⛔ UNSUPPORTED POSITIONS ARE NOT SILENTLY REMOVED TO OBTAIN A SUCCESSFUL
                    REPORT. Lifted to the ACCEPT from `4.0.0_SA_CRO`'s revised O2
                    because it is the session's recurring failure wearing a client's
                    money: a report that drops what it could not resolve renders
                    CLEAN and is WRONG, and no reader can tell it from a complete one.
                    Clear inputs proceed PROGRAMMATICALLY; review is the EXCEPTION
                    path and never a gate on every request -- Andrew hoped for
                    entirely programmatic and the revised brief delivers that shape
         ⛔ AND NO LIVE VENDOR CALL IS AUTHORIZED BY THIS ENDPOINT. Availability is
                    not authorization; a live YCharts, Black Diamond or Orion call
                    needs Andrew's explicit per-use word
         ⛔ RUNNER STYLE IS ANDREW'S WORD, NOT A BUILD CHOICE (this cut, on
                    4.0.0_SA_CRO 191505Z): "use the exact same style of runner, that
                    strategy works very well. I do not believe they send OTP so dont
                    need that part." The BDAPI-with-Kimi runner style and the absence
                    of an OTP branch are FIXED; L5 chooses YCharts-specific details
                    inside that strategy, never whether to honor it

  FWD-5  An advisor sees current holdings organized by models, with the underlying
         securities and unassigned assets preserved
         DONE WHEN  EXERCISED -- dated holdings and model snapshots have been
                    replayed for all three registry client firms
         ACCEPT     the view starts at the model breakdown and drills into accounts
                    and securities; ACTUAL CUSTODY HOLDINGS REMAIN THE TOTAL-VALUE
                    BASIS; SmartX (49F), Eclipse (INF) or BD Rebalancer (COT)
                    supplies the overlay; target weights, actual sleeve values and
                    inferred estimates are DISTINCT; missing attribution stays
                    VISIBLE without double-counting or redistributing the residual
         PROOF      replay across all three firms including an unassigned account, an
                    unmatched join, a blended model and a multi-relationship
                    membership; UNIQUE UNDERLYING HOLDINGS RECONCILE BEFORE AND AFTER
                    THE OVERLAY; coverage and join exceptions carry DENOMINATORS
         ACCEPT     ** IRPT_BACKEND ** -- join correctness and the reconcile-before-
         OWNER      and-after control are this project's
         CROSSES    IRPT_FRONTEND draws the drilldown on this project's
                    revision-bound nodes
         SOURCE     brief O5, F4; Andrew's per-partner overlay mapping, verbatim --
                    carried; BK brief O5; WS4 child brief @4a1d1ed9aa
         ⛔ NOTE    MODEL TARGETS MUST NOT MASQUERADE AS OBSERVED HOLDINGS. A residual
                    silently redistributed into sleeves fails this outcome even when
                    every total ties

  FWD-7  The client directory cannot go quietly stale, and its ceiling belongs to
         the system rather than to the advisor's diligence
         DONE WHEN  EXERCISED -- a DRIVEN exercise on a CONTROLLED CLOCK against
                    source fixtures, covering the FAILURE arms, with NO REAL-CALENDAR
                    WAIT anywhere in it
         ACCEPT     a client added, or whose eligibility changes, in the source
                    becomes visible or ceases to be offered within the declared
                    refresh window WITHOUT anyone asking for a refresh; a MISSED
                    TRIGGER and a FAILED REFRESH each read DIFFERENTLY from a
                    completed one; a request served from an OVER-AGE directory hits
                    the declared expiry/fallback behavior rather than being answered
                    silently; the oldest directory an advisor can be served is set by
                    the SCHEDULE, not by whether they noticed the as-of
         PROOF      controlled-clock / source-fixture exercise driving ALL FIVE arms:
                    an added client, a changed eligibility, a MISSED trigger, a
                    FAILED refresh, and an OVER-AGE directory request
         ACCEPT     ** IRPT_BACKEND ** -- ingestion, projection, refresh and the
         OWNER      expiry/fallback behaviour are this project's
         CROSSES    IRPT_FRONTEND shows the as-of and the capability gap
         SOURCE     ⭐ **NOT IN THE BRIEF'S SIX. ADDED AT L2** -- carried; BK brief
                    O1 + O7
         (FWD-7 continues below; FWD-8 follows it.)
                    DONE WHEN and PROOF re-cut on `4.0.0_SA_CRO`'s L2 review (95180):
                    my first form read a HISTORY of consecutive refreshes, which has
                    NO NEGATIVE ARM -- a run of successes cannot show what a missed
                    or failed refresh does, and a SCHEDULE is not by itself a
                    MAXIMUM SERVED AGE. The driven form is strictly stronger and is
                    what the L2 "no FWD is a wait" clause actually demands
         ⛔ RULED BY ANDREW 2026-09-10 ~17:3xZ, VERBATIM "Stay visible." A
                    terminated client STAYS VISIBLE, MARKED TERMINATED, with access
                    still governed by ENTITLEMENT. So DISAPPEARANCE FROM SEARCH IS
                    NEVER EQUATED WITH ACCESS REVOCATION, and a terminated client or
                    account that still requires HISTORICAL reporting remains
                    reachable to an entitled viewer. This outcome now NAMES the
                    eligibility policy rather than deferring it, and L4 writes to
                    THIS rather than choosing. Raised by `4.0.0_SA_CRO` at 95180;
                    my first form assumed termination implies disappearance, which
                    was a decision I did not own and got the wrong way round
         ⛔ WHAT THIS OUTCOME IS **NOT**: it is DIRECTORY FRESHNESS AND ELIGIBILITY,
                    and NOTHING about it grades revocation. FWD-2 owns revocation
                    INDEPENDENTLY and the two are not substitutes -- see the
                    correction under UNCOVERED

  FWD-8  An advisor exports a BRANDED Opal report whose narrative page states what
         was happening in the market at the account's dramatic moves -- as
         CONTEMPORANEOUS CONTEXT, never as a cause of the return
         DONE WHEN  EXERCISED -- a KNOWN drawdown window has been replayed against
                    the dated topic history and the same inputs selected the SAME
                    inflection points twice
         ACCEPT     the dashboard stays the DEFAULT view and the export is a separate
                    act; the export renders the Opal template from the deck-generation
                    brand guidelines at the SAME performance revision the advisor
                    reviewed, with advisor logo and information as an OPTIONAL input;
                    the narrative page shows the performance time series and, at the
                    max drawdown and other dramatic moves, the Trending Topic and
                    Topic Cloud terms DATED TO THAT WINDOW, with the other sentiment
                    signals as supporting context; inflection-point selection is
                    DETERMINISTIC -- the same series and the same history select the
                    same moments, every run
         PROOF      replay one known drawdown window twice and diff the selected
                    moments; replay a window that PREDATES the news history and
                    confirm it renders MISSING HISTORY rather than an empty topic list
         ACCEPT     ** IRPT_BACKEND ** -- deterministic inflection selection,
         OWNER      evidence and prose validity, the frozen bundle, and export
                    execution are this project's
         CROSSES    IRPT_FRONTEND supplies the template and rendering package this
                    project executes, and the chart composition on which the dated
                    markers land; the topic/sentiment retrieval is a NEW seam whose
                    owner is named at L5 (carried from the ratified OWNER line)
         SOURCE     Andrew-direct 2026-09-10, verbatim: a "narrative arc" using "daily
                    cloud and trending topics over almost a full year", to "dynamically
                    assess what was the trending topic or buzz word/phrase from word
                    cloud that was occuring at that time ... to help qualify what was
                    happening at that time" -- carried; BK brief O6
         ⛔ THE CAUSAL LINE IS IN THE ACCEPT, NOT IN A DISCLAIMER. A page that puts a
                    client's drawdown and a market topic in ONE VISUAL IS READ AS
                    CAUSAL by any reader, whatever the footnote says. Andrew's own word
                    is "QUALIFY WHAT WAS HAPPENING AT THAT TIME" -- contemporaneity --
                    and `4.0.0_SA_CRO` named the same limit unprompted. **The artifact
                    must SAY it is contemporaneous context and must not assert, imply
                    or rank causes.** An export that reads as an explanation of the
                    return FAILS this outcome even when every date is right
         ⛔ MISSING HISTORY IS AN ANSWER, NOT AN EMPTY STATE. The news history is
                    "almost a full year". Any performance period reaching before it has
                    NO topic data, and a narrative page that silently shows nothing
                    there reads as "NOTHING NOTABLE HAPPENED" rather than "WE HAVE NO
                    DATA". The absent-versus-zero distinction is the failure this
                    estate has paid for repeatedly and it is graded here

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
         WHY NEW    the ratified FWD-4 begins "from an analyst-approved input" and
                    takes that input AS GIVEN -- nothing ratified grades HOW a
                    forwarded email becomes one. The subtraction below is the
                    record.
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

**COUNT: 9 outcomes carried. 7 are ratified ids, text verbatim (`FWD-1`, `2`, `3`, `4`, `5`, `7`, `8`); 2 are
NEW (`FWD-9`, `FWD-10`). ACCEPT owner: IRPT_BACKEND 8, IRPT_FRONTEND 1 (`FWD-1`, contributed to here).**

---

## THE UNCOVERED PARTITION — hunted BY SUBTRACTION, and this is where the two new ids come from

**Denominator: the BK brief's 7 outcomes (O1–O7).** O1→FWD-1 + FWD-2 · O2→FWD-3 · O4→FWD-4 · O5→FWD-5 ·
O6→FWD-8 · O7's directory-refresh half→FWD-7. **7 minus 5 (whole) minus 1 (half) leaves O3 wholly uncovered and
O7's diagnosability-and-isolation half uncovered.** Those are `FWD-9` and `FWD-10`.

⛔ **WHY MY DISTRIBUTION AMENDMENT DID NOT FIND THESE.** It asked *where do the eight belong*. It never asked
*what do the briefs contain that the eight miss*. A partition of a fixed set is structurally unable to see a
member outside the set. **Only a subtraction from the BRIEF's own denominator can.** Andrew asked whether I had
run this phase; I had not, and this section is the difference.

**Reverse subtraction — ratified ids the BK brief does NOT serve: `FWD-6`.** Advisor-facing degradation is
IRPT_FRONTEND's; BK contributes the status contract inside O7. Not uncovered; owned elsewhere.

## WHAT L2 DOES NOT DECIDE

Cells, owners, sequencing, lanes (L5/L6). Every number the brief names — the 15-minute poll, session-recovery
bounds, retry counts — is the brief's proposal, MEASURED then declared downstream, never ratified at L2. Which
shared contracts change and how (BK §II.3 is the inventory). Any live vendor call. **Nothing here authorizes
egress.**

⛔ **CORRECTED (this cut, on `4.0.0_SA_CRO` 191505Z):** the first cut listed *"whether the YCharts runner reuses
the named pattern"* here as an L5 build choice. **It is not. The runner STYLE is Andrew's explicit word** —
*"use the exact same style of runner, that strategy works very well. I do not believe they send OTP so dont need
that part"* — and it is FIXED in `FWD-4`'s block above. What L5 decides is the YCharts-specific implementation
inside that strategy, never whether to follow it.

## WHERE THIS LANDS (F4) — **NOT YET LANDED**

Ready to paste under **`## ENDPOINT (step 2, /endpoint --forward)`** in
`org/missions/D9/IRPT/IRPT_BACKEND/prd/IRPT_BACKEND_PRD.md`. **That path does not exist.** Same three
prerequisites as the counterpart, **plus one this side alone carries: `FWD-9` and `FWD-10` must be RATIFIED or
REFUSED by Andrew before the PRD header's `endpoint_outcomes` can list them.** A PRD may land with the seven
ratified ids and take the two on his word; it may not list an unratified id as if he had confirmed it.

## PROVENANCE (F5)

**GROUNDED ON:** the umbrella endpoint **at its pin** `git show 58266dab2d:…/ENDPOINT_FWD_INVESTOR_REPORTING_LIGHTWEIGHT_20260910.md`
lines 118–360 (the eight ratified blocks, extracted with a positive control that a bogus pin is refused);
`docs/briefs/investor-reporting-ir-bk-brief-20260910.md` @`efa5a94bf1` lines 1–64 and §II.1–II.3;
`docs/briefs/investor-reporting-ir-fe-brief-20260910.md` @`efa5a94bf1` lines 1–66 and §II.1–II.2 (every
CROSSES line); `4.0.0_SA_CRO` 191505Z for Andrew's runner words (quoted from that relay; the underlying
Andrew-direct record is the CRO's); `org/standards/PROJECT_TREE.contract.json` (the code grammar).
**NOT READ:** the TO register; any `org/projects/*.json`; the nine source documents beneath the brief; the WS4
child brief's body (cited for `FWD-5`'s lineage only).
