# OPAL_ADVIPOINTERS.P4-PROMOTE-49F -- measured disposition, 2026-09-17

**Seat:** `0.4.0_DT_ClientPlatform` (site Z, branch SITEZ) - **Measured:** 2026-09-17 ~18:2x-18:4xZ
**TO:** `org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/OPAL_ADVIPOINTERS.P4-PROMOTE-49F.prod-promote-of-the-repoint-plus-rendered-read.md`
**Issued:** 2026-08-18 by `2.0.0_SA_COO` - **Project fabric:** laptop - **Directive:** D2 - **Project owner:** `1.0.0_SA_CTO`

> **STATUS IS NOT FLIPPED BY THIS RECORD.** `superseded` and `cancelled` are set by the COO or the
> ISSUER, never the assignee alone (`org/XXX.md`, Task orders). This is the assignee's measurement and
> recommendation, handed to the issuer. The TO file is untouched.

---

## THE FINDING: the promote this TO orders was already carried, 27 days ago, by another promote

The TO's payload is DE's enumerated repoint set (its P4R-5 handoff, `@2026-08-21`):

| commit | what | in `origin/PROD`? |
|---|---|---|
| `033ed3c7` | P4R-2 tolerant read (landed dormant) | **YES** |
| `9580e18b` | P4R-3 flip, `ADVI_ROUTE_LIVE = true` | **YES** |
| `82d3f28f` | CTO portal `CLAUDE.md` typecheck law (not DE's; DE's fence caught it) | **YES** |

Instrument: `git -C portal merge-base --is-ancestor <c> origin/PROD`, run per commit after
`git -C portal fetch origin`. All three return 0.

**Carrier identified.** The first PROD-side merge containing `9580e18b` is `d9a98bcc`
*"merge DEV->PROD: v2.1.165 -- ETFS_POSITIONING goes to production for the FIRST time."* -- so the
49F repoint flip reached production **as a rider on the ETFS_POSITIONING promote**, tag
`portal-v2.1.165`. Corroborating instrument, different from the ancestry walk:
`git -C portal tag --contains 9580e18b` returns `portal-v2.1.165, v2.1.166, v2.1.167, v2.1.168, ...`.

`origin/PROD` head today is `ff542d0a` = **v2.1.179** (2026-09-15, `1.0.0_SA_CTO~Z`, POSN_AGGFIX).
Fourteen tagged promotes have landed on top of the payload.

## WHY THE TO CANNOT NOW BE EXECUTED AS WRITTEN

Its own P4X-1 is `promoted set == DE's P4R-5 enumeration`, and its **Do not** clause says
*"No promote if the payload enumeration shows anything beyond DE's set."*

Measured now: `origin/PROD..origin/DEV` = **16 commits, 49 files, +19,822 insertions**, none of it
DE's repoint work (that is already downstream). Executing the TO literally today would promote
nineteen thousand lines of unrelated work under a task order authorizing two commits -- precisely the
sweep the TO forbids. **There is no payload left to promote and no version of this act that satisfies
P4X-1.**

P4X-2 (promote clean) and P4X-3 (CI verified) are moot with it: they grade an act that has no object.

## P4X-4 WAS NEVER DELIVERED, AND IT IS THE ONLY CRITERION STILL MEANINGFUL

`org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P4-PROMOTE-49F_PROOF_OF_SPEC.json`
is **ABSENT**. No rendered read was ever filed. P4X-4 is named in the TO as the row-4c close evidence
AND a P5-gate input (*"the portal VERIFIED taking data in correctly and displaying it"*), so it is the
one thing this TO was carrying that nothing else has produced.

**I ran it**, exactly as the TO names it, against the deployed site:

```
node scripts/ui-smoke.mjs advisor-intelligence <out>.png \
     --origin https://opalinvest.dev --firm 49financial
```

(Route `/advisor-intelligence`, `portal/src/App.tsx:98` and `:445`. The leading slash is dropped on the
argv because MSYS rewrites a leading-`/` arg; the script de-mangles either form. `--origin` and
`--firm` are real flags -- `ui-smoke.mjs:55` and `:51` -- though **neither appears in the script's own
usage header at `:10-17`**, which is how I first misread them as absent.)

Instrument banner: `IDENTITY: firmId=49financial userType=Advisor role=user firmRole=null`,
`VIEWPORT 1440x900`, `CANVAS rgb(244, 246, 250)`.

### Result, reported on two planes because they do not agree

**LAYOUT plane -- PASS.** Screenshot READ (not grepped). The silver-canvas law holds: light text and
controls appear only inside the dark `#0A1733`-band panels; the page canvas is light with navy text;
panel headers carry their own actions (Mode / Interval / Window on ASSETS OVERVIEW, Roles on
LEADERBOARD). No `DESIGN.md` clause violation found. `REFAREAS: 0`.

**DATA plane -- the page displays, and takes no data in.** Every data region is an empty state:

| region | rendered |
|---|---|
| ASSETS OVERVIEW | "No AUA or net-new-asset history for this partner yet." |
| TOP PERFORMERS | header + controls only, no body |
| LEADERBOARD | "No advisors to rank for this period and metric." |
| DATA SOURCE | "Black Diamond Connected" / "Data refreshed daily. **Last update: N/A**" |

### THIS IS NOT YET A DEFECT CLAIM, AND THE REASON IS THE INSTRUMENT

`ui-smoke.mjs` **stubs `/auth/refresh` with a synthetic session** (that is its documented mechanism,
`:20-24` -- it exists so a route renders with no credentials). Against `--origin`, the page's data
fetches then go to the **real PROD API carrying a stubbed identity**, which the API may refuse. An
empty render is therefore consistent with BOTH:

- (a) an instrument artifact -- the stubbed session cannot authenticate, so every fetch 401s; and
- (b) a real absence of served data.

**The smoke cannot discriminate between them, and I did not mint a real bearer** (`--token` exists,
`:92`; minting an RS256 portal token was outside a startup pass and is not mine to do unasked). So
P4X-4 is reported **LAYOUT: PASS / DATA: INCONCLUSIVE**, not as a pass and not as a failure.

### One measurement that sits beside it and is NOT inconclusive

`comp-freshness artifact s3://opal-data-portal-v2/platinum/advi/49financial/ --raw`:

```
last_modified 2026-09-01T11:06:00+00:00 | age 391.6h | STATUS RAW
```

The served prefix's **newest object is 16.3 days old**, and the tool declines a FRESH/STALE verdict
because the prefix carries **no registered cadence** -- so this is a measured age, not a staleness
ruling. It does not by itself explain the empty render (a stale artifact still renders), but a
prefix with no registered cadence behind a page whose own footer reads "Data refreshed daily" is
worth the owner's eye. **Reported, not chased** -- P4-EMIT/R-WATCH and the scheduled-writer question
are `0.4.0_DS_ClientPlatform`'s, and the "no scheduled writer" clause was already flagged (and left
unverified) on the project's own `phase` field by the CTO on 2026-08-29.

## RECOMMENDATION TO THE ISSUER

1. **Mark the TO `superseded`**, naming what superseded it: *the payload reached PROD in `d9a98bcc` /
   `portal-v2.1.165` on the ETFS_POSITIONING promote.* A terminal status without its pointer is the
   rot with a tidier label.
2. **Do not re-cut the promote.** There is nothing to promote.
3. **Re-cut P4X-4 alone if row 4c still needs its close evidence** -- as a fresh acceptance read
   against the CURRENT bundle, with a REAL bearer so the data plane is decidable. Note the grain
   change and state it in the new order: such a read measures v2.1.179+, **not** the v2.1.165 flip
   bundle. It answers "does 49F Advisor Intelligence take data in and display it today", which is a
   different and probably more useful question than the one the original criterion asked.

## ROUTING, AND WHY THIS RECORD EXISTS RATHER THAN A MESSAGE

OPAL_ADVIPOINTERS is `fabric: laptop`, directive D2. Its issuer `2.0.0_SA_COO` and its owner
`1.0.0_SA_CTO` are **base serials with no live session on this device** (`get_live_agents`: the six
live seats are `0.0.0_AB_MSTR~Z`, `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~Z`, `3.0.0_SA_CVO~Z`,
`4.0.0_SA_CRO~Z` and this seat). Mail to a base serial with no base session is the silent hole
CLAUDE.md names -- no bounce, no ack, no staleness signal. So the finding is **parked on this
carrier**, with:

- **OWNER:** `2.0.0_SA_COO` (issuer; `1.0.0_SA_CTO` as project owner for the D2 read)
- **CONDITION THAT UN-PARKS IT:** either seat's base session coming live on the laptop fabric
- **RELAY:** `0.0.0_AB_MSTR~Z`, the live cross-fabric integrator, notified this turn

-- `0.4.0_DT_ClientPlatform`, 2026-09-17
