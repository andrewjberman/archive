# ATTRIBUTION -- the PROPERTY+OWNER axis and its mandatory rendered `UNGROUPED` value (cell RP-s-13, outcome FWD-4)

Authority: `org/missions/D12/NFRA/NFRA_REPORT/prd/NFRA_REPORT_PRD.md` (v0.6) section 6 "Rulings that
BIND" and section 8's `S13` manifest row; the L1 brief's `O4`
(`docs/briefs/global-infrastructure-reporting-brief-20260909.md@37ff80867a`); the decomposition's
`RP-s-13` cell (`NFRA_REPORT_DECOMP_R2.md`); ARMED row `NFRA_REPORT-Z-S1`
(`2.0.0_SA_COO~ZZ`, msg 20627), which measured that round 1 served `FWD-4` with NO cell.

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

## 2. The axis members -- RATIFIED vs. OPEN, stated as what each currently is

| Member | Status | Source |
|---|---|---|
| `Dashboard` | RATIFIED | Brief `O4`, Andrew-direct 2026-09-09: "Every finding rolls up to **Dashboard**, **Website** or **Gateway**" |
| `Website` | RATIFIED | same |
| third member (`Gateway`, `Graph`, or **both** — a four-member axis) | **OPEN CALL AT ANDREW, NOT DECIDED HERE** | PRD v0.6 §6: "THE MEMBER NAMES ARE NOT SETTLED BY THIS RULING AND ARE NOT THIS SEAT'S TO SETTLE — naming law is sovereign. Carried to Andrew as an open call: whether the attribution axis's third member is `Gateway`, `Graph`, or both (a four-member axis)." |
| `UNGROUPED` | **MANDATORY, RENDERED, and it binds regardless of how the open call above resolves** | CTO ruling at L4, PRD v0.6 §6 (below) |

`UNGROUPED` is not a fourth *property of the business* in the sense `Dashboard`/`Website`/`Gateway`/
`Graph` are. It is the sentinel value this axis renders for any live surface whose true property has
not yet been ratified — precisely so that not-knowing-the-name never becomes not-showing-the-thing.
This cell does **not** decide the open call above, and does **not** guess a surface into `Dashboard`,
`Website`, or either candidate third name. That is the one thing this cell is bound not to do (BOUNDS,
this TO), and it is also the one thing the CTO ruling below makes structurally impossible to skip.

## 3. The rule that makes `UNGROUPED` mandatory

CTO ruling at L4, PRD v0.6 §6, quoted:

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

This is also why `opal-globgrph` belongs in this document even though it is not one of the two
surfaces this cell's own task order named: it is round 1's own worked demonstration of exactly the
failure mode `UNGROUPED` exists to prevent. `opal-globgrph` is an ACTIVE ECS Fargate cluster (three of
three services running) that no prior artifact of this project had ever seen, because the compute
manifest it should have appeared in is EC2-only and nothing else looked (PRD v0.6 §6, ruling 15b
discharge). It was found "because the cell was told to ask that question," not because any standing
mechanism would have caught it on its own. An attribution axis with no mandatory `UNGROUPED` value
would let exactly this kind of surface vanish a second time, silently, the next time this report is
composed — which is the failure this axis is built to close off structurally, not just for the two
surfaces named at this cell's issuance.

## 4. Worked specimens

| Surface | Property (this axis) | Status / reasoning | Evidence |
|---|---|---|---|
| `canonical-schwab-si2` | `Dashboard` | **RULED AND CLOSED.** Andrew-direct 2026-09-09 ~22:3xZ, verbatim: *"I would include si2 under the Dashboard."* No longer ungrouped; no cell may render it so. | PRD v0.6 §6 and §8's `S13` row: "`canonical-schwab-si2` is RULED into `Dashboard` (Andrew-direct 2026-09-09 ~22:3xZ) and is NO LONGER an ungrouped example." |
| `opal-gateway` (MCP server) | `UNGROUPED` | Live surface, no ratified group today. The candidate name "Gateway" is one half of the still-open third-member call — rendering it into "Gateway" now would be guessing the open call's answer, which this cell is bound not to do. | PRD v0.6 §8 `S13` row, verbatim: "Live surface still ungrouped: `opal-gateway`." |
| `opal-globgrph` (ECS Fargate cluster: `globgrph-nessie`, `globgrph-trino`, `globgrph-serving`, 3 of 3 services running) | `UNGROUPED` | Same reasoning, by the same rule, even though ruling 15b's prose calls the candidate bucket "the Graph group": **"Graph" is not yet a ratified axis member**, so treating this cluster as already inside it would be guessing it into a group one open call ahead of Andrew's word. Rendered `UNGROUPED` so it cannot disappear for want of a name a second time. | PRD v0.6 §6, ruling 15b discharge: "The `Graph` group is NOT empty... `opal-globgrph` is an ACTIVE ECS Fargate cluster, 3 of 3 services running... read live by `0.9.0_WK_NFRA_REPORT~2`." |

No other live surface is asserted `UNGROUPED` or assigned here. This document does not attempt a full
census of every engine this report touches — that census, and the per-row rendering of every finding
this axis governs, is the composer's act (`RP-s-15`, `S2`, "BUILD THE COMPOSER"), not this cell's. This
cell builds and demonstrates the LAW the composer applies, the same relationship `STATE_MODEL.md` has
to the report it governs.

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
property itself (`Dashboard`, `Website`, the open third member, or `UNGROUPED`) anywhere in this
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
`org/missions/D12/NFRA/NFRA_REPORT/prd/NFRA_REPORT_PRD.md@1aae9c43fe`. `opal-gateway` remains
`UNGROUPED` under both the stale and the live text, so nothing about that half of the BOUNDS changed.

## 8. What this document does NOT do

- Does **not** name the third axis member (`Gateway`, `Graph`, or both) — Andrew's open call, carried
  here as open, not decided.
- Does **not** guess `opal-gateway` or `opal-globgrph` into `Dashboard`, `Website`, or either candidate
  third name.
- Does **not** render `canonical-schwab-si2` as `UNGROUPED` — the live PRD forbids it, superseding this
  cell's own stale BOUNDS text (§7).
- Does **not** invent a per-property human or team owner not present in the source record (§6).
- Does **not** edit, remove, or redefine `STATE_MODEL.md`'s two ratified axes or its orthogonal third
  (DESIRED/APPLIED/EXERCISED) axis — this is a fourth, independent axis, same rule-24(iii) discipline.
- Does **not** attempt the full per-finding attribution census — that is the composer's act (`RP-s-15`).
