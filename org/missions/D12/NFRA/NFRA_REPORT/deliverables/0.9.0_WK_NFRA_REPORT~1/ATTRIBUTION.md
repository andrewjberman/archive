# ATTRIBUTION -- the PROPERTY+OWNER axis and its mandatory rendered `UNGROUPED` value (cell RP-s-13, outcome FWD-4; AMENDED AT PRD v0.7 by cell RP-s-20)

Authority: `org/missions/D12/NFRA/NFRA_REPORT/prd/NFRA_REPORT_PRD.md` (v0.7) section 6 "Rulings that
BIND" and section 8's `S13` manifest row; the L1 brief's `O4`
(`docs/briefs/global-infrastructure-reporting-brief-20260909.md@37ff80867a`); the decomposition's
`RP-s-13` cell (`NFRA_REPORT_DECOMP_R2.md`) and `RP-s-20` cell (`NFRA_REPORT_DECOMP_R3.md`); ARMED row
`NFRA_REPORT-Z-S1` (`2.0.0_SA_COO~ZZ`, msg 20627), which measured that round 1 served `FWD-4` with NO
cell.

**AMENDMENT NOTE (RP-s-20):** this document was built at PRD v0.6, while the axis's third-member name
was still an open call. PRD v0.7 CLOSED that call (Andrew-direct 2026-09-10 ~02:5xZ, *"go with your
recs on all six"*, on the card recommending *"Four: Dashboard, Website, Gateway, Graph"*). Sections 2,
3, 4, 7 and 8 below are updated in place to state the RATIFIED, CLOSED law; nothing in this amendment
edits `STATE_MODEL.md`'s own axes, and `UNGROUPED` is NOT retired -- see §3.

## 1. What this axis answers

`FWD-4`'s RE-CUT `ACCEPT`, quoted in full and built against verbatim (`PRD` ENDPOINT block):

> Every problem belongs to a named part of the business and names who would fix it. Anything we run
> that has no part named for it yet is shown as not-yet-grouped, in plain sight, and is never quietly
> left out.

This is a second axis, ORTHOGONAL to the report's rendering law in `STATE_MODEL.md` (Axis 1 = did the
check happen; Axis 2 = what was found; the third, DESIRED/APPLIED/EXERCISED axis). This document does
not touch, redefine or amend any of those three. `FWD-4` asks a DIFFERENT question of every row that
`STATE_MODEL.md` already knows how to grade: not "is this OK", but "whose problem is this, if it is
one" — and rule 24(iii) is why the two live as separate axes rather than one (PRD section 6, first
ruling: collapsing them was the exact defect this cell exists to correct).

## 2. The axis members -- FOUR, RATIFIED AND CLOSED AT PRD v0.7

| Member | Status | Source |
|---|---|---|
| `Dashboard` | RATIFIED | Brief `O4`, Andrew-direct 2026-09-09: "Every finding rolls up to **Dashboard**, **Website** or **Gateway**"; PRD v0.7 §6 |
| `Website` | RATIFIED | same |
| `Gateway` (the `opal-gateway` MCP server, EC2) | **RATIFIED AND CLOSED AT v0.7** | Andrew-direct 2026-09-10 ~02:5xZ, verbatim: *"go with your recs on all six"*, on the `/open-calls` card whose REC read *"Four: Dashboard, Website, Gateway, Graph."* PRD v0.7 §6. |
| `Graph` (the `opal-globgrph` ECS Fargate cluster) | **RATIFIED AND CLOSED AT v0.7** | same ruling. PRD v0.7 §6: *"WHY FOUR AND NOT THREE... `opal-gateway` (EC2, the MCP server) and `opal-globgrph` (ECS, 3 of 3 services) are BOTH live, BOTH always-on, and FAIL DIFFERENTLY. Folding either into `Dashboard` would make `FWD-4`'s own bar... false by construction."* |
| `UNGROUPED` | **MANDATORY, RENDERED, NOT RETIRED BY THE v0.7 CLOSURE** -- now means a live surface outside all four named members, a SMALLER set than before v0.7, and it must still render rather than vanish | CTO ruling at L4, PRD v0.7 §6 (below) |

`UNGROUPED` is not a fifth *property of the business* in the sense `Dashboard`/`Website`/`Gateway`/
`Graph` are. It is the sentinel value this axis renders for any live surface whose true property has
not yet been ratified — precisely so that not-knowing-the-name never becomes not-showing-the-thing.
The third-member open call this section used to carry is CLOSED as of PRD v0.7 (§3 below quotes the
ruling in full); this document does **not** re-open it, does **not** carry it forward as if still
open, and does **not** invent a fifth member. It also does **not** guess ANY surface into `Dashboard`
or `Website` beyond what is already ratified for it (§4) — only Andrew's own word moves a surface
into a named group, never this cell's inference.

## 3. The rule that makes `UNGROUPED` mandatory

CTO ruling at L4, PRD §6, quoted (unedited by the v0.7 amendment below):

> NO LIVE SURFACE MAY LEAVE THE AXIS SILENTLY. `FWD-4`'s attribution axis carries a MANDATORY,
> RENDERED `UNGROUPED` value. A surface with no ratified group is shown as ungrouped, never omitted
> and never guessed into a group. This is ruling 12's own shape applied one axis over: it is
> structurally impossible to print `OK` on a surface nobody looked at, and it must be equally
> impossible to make a surface disappear for want of a name.

The parallel to `STATE_MODEL.md`'s own forbidden pair is exact and deliberate: that document makes it
structurally impossible to print `BREACH` or `OK` on a surface nobody looked at (its §3, §4). This
axis makes it structurally impossible for a live surface to have **no attribution row at all** because
nobody has named its group yet. Both failures are silence standing in for an answer; both are refused
the same way — a mandatory, explicit, un-omittable value.

**RULED AND CLOSED AT v0.7, quoted in full (PRD §6):**

> RULED AND CLOSED AT v0.7 -- THE AXIS HAS FOUR MEMBERS. Andrew-direct 2026-09-10 ~02:5xZ, VERBATIM:
> "go with your recs on all six", given on the `/open-calls` card whose REC read "Four: Dashboard,
> Website, Gateway, Graph." `FWD-4`'s attribution axis is `Dashboard | Website | Gateway | Graph`, and
> the earlier si2 half stands: `canonical-schwab-si2` is `Dashboard`.
>
> WHY FOUR AND NOT THREE, recorded so it is not re-litigated: `opal-gateway` (EC2, the MCP server) and
> `opal-globgrph` (ECS, 3 of 3 services) are BOTH live, BOTH always-on, and FAIL DIFFERENTLY. Folding
> either into `Dashboard` would make `FWD-4`'s own bar -- one problem belongs to one part -- false by
> construction. A fourth member costs a report section.
>
> AND `UNGROUPED` IS NOT RETIRED BY THIS RULING. It now means a live surface outside all four named
> members, which is a smaller set than before and must still RENDER rather than vanish. The ruling
> names the members; it does not promise the four are exhaustive of everything this estate will ever
> run.

This is also why `opal-globgrph` belongs in this document even though it was not one of the two
surfaces this cell's own original task order named: it is round 1's own worked demonstration of
exactly the failure mode `UNGROUPED` exists to prevent, and it is now also one of the two v0.7
REFERENTS the four-member ruling names by description (§4). `opal-globgrph` is an ACTIVE ECS Fargate
cluster (three of three services running) that no prior artifact of this project had ever seen,
because the compute manifest it should have appeared in is EC2-only and nothing else looked (PRD §6,
ruling 15b discharge). It was found "because the cell was told to ask that question," not because any
standing mechanism would have caught it on its own. An attribution axis with no mandatory `UNGROUPED`
value would let exactly this kind of surface vanish a second time, silently, the next time this report
is composed -- which is the failure this axis is built to close off structurally, and it remains true
for any FIFTH kind of surface this estate stands up next, now that `Gateway` and `Graph` are named.

## 4. Worked specimens

| Surface | Property (this axis) | Status / reasoning | Evidence |
|---|---|---|---|
| `canonical-schwab-si2` | `Dashboard` | **RULED AND CLOSED.** Andrew-direct 2026-09-09 ~22:3xZ, verbatim: *"I would include si2 under the Dashboard."* No longer ungrouped; no cell may render it so. | PRD §6 and §8's `S13` row: "`canonical-schwab-si2` is RULED into `Dashboard` (Andrew-direct 2026-09-09 ~22:3xZ) and is NO LONGER an ungrouped example." |
| `opal-gateway` (MCP server, EC2 `t4g.nano`) | `Gateway` | **RULED AND CLOSED AT v0.7.** This is the exact referent the v0.7 ruling names by description: *"`opal-gateway` (EC2, the MCP server)... BOTH live, BOTH always-on"*. Rendered `Gateway`, not `UNGROUPED` -- the axis moved from "no ratified group" to "ratified `Gateway`" on Andrew's own word, not this cell's inference. | PRD §6, v0.7 closure block (§3 above), verbatim: *"`opal-gateway` is Gateway (the MCP server)"* (this cell's own task order, ACT, quoting the same ruling). |
| `opal-globgrph` (ECS Fargate cluster: `globgrph-nessie`, `globgrph-trino`, `globgrph-serving`, 3 of 3 services running) | `Graph` | **RULED AND CLOSED AT v0.7.** Ruling 15b's own prose already called the candidate bucket "the Graph group"; the v0.7 ruling ratifies the name. Rendered `Graph`, not `UNGROUPED`. | PRD §6, ruling 15b discharge ("The `Graph` group is NOT empty... `opal-globgrph` is an ACTIVE ECS Fargate cluster, 3 of 3 services running... read live by `0.9.0_WK_NFRA_REPORT~2`") plus the v0.7 closure block naming `opal-globgrph` as Graph's referent. |
| `CloudFront distribution E1DHJH4Y1W8YC2` (no alias; target origin `wp-origin`) | `UNGROUPED` | **A live specimen of the RE-SCOPED `UNGROUPED`, post-v0.7.** `MONITORED_VS_SERVED.md` §3a itself declines to resolve which named surface this distribution belongs to (it carries no alias, so neither `opalinvest.com` nor `opalinvest.dev`'s domain routes through it) -- exactly the "true property has not yet been ratified" case §2 describes, now that `Gateway` and `Graph` are named and this surface still is not either of them, `Dashboard`, or `Website`. | `MONITORED_VS_SERVED.md` §3a, verbatim: "whether public traffic currently flows through this distribution at all is a separate question this reconciler does not resolve... the finding is that IF anything does, or ever does again, nothing here would notice." |

No other live surface is asserted `UNGROUPED` or assigned here as a LAW-level specimen. The full
per-row census across every finding this axis governs -- every row of the composed edition carrying
its own axis value -- is the composer's act, built at `RP-s-20` (`compose_edition.py`, this same
deliverables folder) per this cell's own ACT (LIMB B); `RP-s-15` built the composer engine itself
without that column. This document remains the LAW the composer applies, the same relationship
`STATE_MODEL.md` has to the report it governs.

## 5. Dedup rule -- one failure, one row, never one row per instrument

Brief `O4`, verbatim, and carried into `FWD-4`'s `ACCEPT`: *"One underlying failure appears once, not
once per instrument that noticed it"* / *"When one thing breaks it is mentioned once, not once for
every tool that happened to notice it."* This axis attributes the UNDERLYING FINDING to one property
and (where ratified) one owner — never once per detector. A finding two instruments both surface (for
example, an alert-delivery gap `comp` also flags and `comp-adversary` also flags) still rolls up to
exactly one attribution row. This is a rendering-time rule for the composer, stated here because it is
part of the axis's law, not something this cell exercises against a live duplicate today.

## 6. What "owner" means at this grain, stated rather than invented

`FWD-4`'s `ACCEPT` says a problem "names who would fix it," and brief `O4` says each finding "carries
an owner." Neither the brief, the PRD, nor the endpoint names any owner identity finer than the
property itself (`Dashboard`, `Website`, `Gateway`, `Graph`, or `UNGROUPED`) anywhere in this
project's record at this vintage. This document does **not** invent a person or team name to fill that
gap — doing so would be the same class of act as guessing a surface into a group, and it would fail
the same test §3 states: a fabricated owner is indistinguishable, to a reader, from a ratified one,
which is exactly the silent failure this axis exists to prevent on the OTHER side of the row. **The
property IS the owner-routing value this axis renders.** If and when a finer, per-property human or
team owner is ratified, it is additive to this law (a new column on the same row), and does not change
this axis's shape or its `UNGROUPED` rule.

## 7. A premise in this cell's own task order is now stale, and this document is built against the live PRD, not the stale text

This cell's issued BOUNDS named `canonical-schwab-si2` alongside `opal-gateway` as one of "two live
surfaces... known to have no ratified group today" and instructed rendering **both** `UNGROUPED`. The
PRD has since been amended (to v0.6, ~22:4xZ) to fold Andrew's direct ruling that `si2` belongs to
`Dashboard`, and states explicitly: *"It is no longer an ungrouped surface and no cell may render it
so."* This document follows the live PRD (§4 above: `si2` → `Dashboard`) rather than the task order's
now-superseded instruction, per this cell's own re-grounding obligation. Filed as a surprise row,
`NFRA_REPORT-Z-W2-S5`, in this project's investigation file
(`org/missions/D12/NFRA/NFRA_REPORT/surprise-channel/investigations/INVESTIGATION_v1.md`), citing
`org/missions/D12/NFRA/NFRA_REPORT/prd/NFRA_REPORT_PRD.md@1aae9c43fe`. `opal-gateway` remained
`UNGROUPED` under both the stale and the live text AT THAT VINTAGE (v0.6), so nothing about that half
of the BOUNDS changed at v0.6. **SUPERSEDED IN TURN BY THE v0.7 CLOSURE (§2-4 above, cell `RP-s-20`):**
`opal-gateway` is now `Gateway`, ratified and closed, the same class of amendment this section
describes for `si2` one version earlier -- a cell re-grounding its premises against live state rather
than against the text frozen at issuance.

## 8. What this document does NOT do

- Does **not** re-open the third-member call the v0.7 ruling closed, does **not** carry the old open
  call forward as if still open, and does **not** invent a FIFTH axis member -- the four names
  (`Dashboard`, `Website`, `Gateway`, `Graph`) are RATIFIED AND CLOSED (§2-3).
- Does **not** guess ANY surface into `Dashboard`, `Website`, `Gateway` or `Graph` beyond what Andrew's
  own word has ratified for it (§4) -- `opal-gateway` renders `Gateway` and `opal-globgrph` renders
  `Graph` because the v0.7 ruling names them by description, not because this cell inferred it.
- Does **not** render `canonical-schwab-si2` as `UNGROUPED` — the live PRD forbids it, superseding this
  cell's own stale BOUNDS text (§7).
- Does **not** retire `UNGROUPED` -- it is RE-SCOPED, not removed, and it must still render for any live
  surface outside all four named members (§2-3; §4's `E1DHJH4Y1W8YC2` specimen).
- Does **not** invent a per-property human or team owner not present in the source record (§6).
- Does **not** edit, remove, or redefine `STATE_MODEL.md`'s two ratified axes or its orthogonal third
  (DESIRED/APPLIED/EXERCISED) axis — this is a fourth, independent axis, same rule-24(iii) discipline.
- Does **not** itself render the full per-finding attribution census as a table over every composed row
  — that census is `compose_edition.py`'s act, built at `RP-s-20` (LIMB B of this cell's own ACT,
  same deliverables folder). This document remains the LAW the composer applies (§4, closing note).
