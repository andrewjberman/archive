<!-- HANDOFF DRAFT, NOT AN ORDER: re-pointed to DSGN_AMGTV1 (2.0.0_SA_COO~D) at the round-77 cut; the page is that lane's. -->
# AMGT_RESAPP task order -- `AMGT-ba-5` -- FWD-18 AND FWD-1 ON THE PAGE: THE PASSAGE ONCE PER PRESS, THE SERVED TABLE DRAWN WITH ITS COLUMN LABELS, READABLE AXIS TICKS, ONE HEADING PER SEGMENT (CTO RULING 6)

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D5/AMGT/AMGT_RESAPP/decompositions/AMGT_RESAPP_DECOMP.md</decomp_doc>
<owned_cells>AMGT-ba-5</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_AMGT_RESAPP~271</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no cron, alarm, monitor or cadence; page code and its checks only.
comp-iam: DECLARED-NOT-APPLICABLE -- no store, role or route changes; the page reads the same /thesis body it reads today.
comp-adversary: RUN by the issuer at the cut -- all three FWD-18 defects are on the page, not in the served data. On deployed OVpDhfwD, BA's first driver point already serves `passage_table` with columns 737, 747, 767, 777, 787, Total and two labelled rows; the page reads `passage_table` in 0 places. ASML NA's three points share ONE passage id (P0086), and the page keys its open state on the passage id, so one press opens three blocks. The chart's `YAxis` has no tick formatter.
EGRESS CLASS, declared: NONE. No vendor, SEC or model call; a captured fixture only.
</preflight>

**Your worktree:** `C:/tmp/r77-271` (branch `wk-AMGT_RESAPP-271`, cut from the issuance commit with `--portal-ref PORTAL_REF_AT_CUT --node-modules link`, so `portal/` is at the portal DEV head at the cut). Work and commit only there. Start every shell call with `cd /c/tmp/r77-271`: a call that starts elsewhere resolves `git rev-parse --show-toplevel` to the base checkout.

## 1. THE ACT -- `AMGT-ba-5` (round 77, decomposition s.85)

CTO ruling 6 (round-76 analysis @c8bbeeac10) and the walk's rows Z-W266-S2 and Z-W266-S3. All five repairs are on the security
page, in `portal/src/pages/SecurityAnalysis/components/`. The served data does not change.

1. **The passage renders ONCE per press** (`ThesisDriverChart.tsx`). Today the open state is the pressed point's passage id.
   Where several points cite one passage (ASML NA: three points, one id), one press opens a block under every point. Key the
   open state on the POINT, so one press opens one block under the pressed point, a press on another point moves it, and a
   second press on the open point closes it.
2. **A served table passage is drawn as a table** (`ThesisDriverChart.tsx`, with a new `PassageTable.tsx` beside it). A point may
   carry `passage_table: {columns: [...], rows: [{label, values: [...]}], heading, note}`. Draw it as a table: one column
   header per served column label, each row's label in the row, the figures in the order served, the `heading` above it and
   the `note` (when not null) below it in words. Compute, join or re-order nothing. A row may carry more or fewer figures than
   there are columns; draw what is served. When a point carries no `passage_table`, keep today's text block. Show
   `passage_table_reason` in words when it is served. The cite line stays.
3. **The y-axis ticks are readable** (`ThesisDriverChart.tsx`). Give the chart's `YAxis` a `tickFormatter`: a large figure reads
   short (393,421,721 as about "393.4M"), a small figure is exact (528 reads "528"), and the axis is wide enough that no tick
   is clipped.
4. **One heading per segment** (`SegmentBreakdown.tsx`). The served rows each carry `segment`. Today the label is printed on
   every row and the rows interleave (BA: 11 rows under 3 labels). Group the rows by `segment`, in the order each segment is
   first served. Print the segment's name ONCE as that group's heading and its rows beneath it. The rows keep their text, their
   closed Source disclosure and their served order inside a group. A row's `segment_reason`, when served, is shown once
   under its heading.

5. **A refused chart reads its reason** (`ThesisDriverChart.tsx`). Cell `AMGT-ba-6` refuses a share-count figure as a driver
   chart; the route will then serve the chart `status: "ABSENT"` with `plain_reason`, a sentence written for a reader. When
   an ABSENT chart carries `plain_reason`, show that sentence in place of the default message. The existing `reason` field
   is system text and stays in the data attribute, never in visible text. An ABSENT chart with no `plain_reason` keeps
   today's message. A refused segment breakdown needs no page change: it serves no rows and its `reason`, which the page
   already shows.

**The contract the check reads.** Keep these attributes:
- the pressed element carries `data-driver-chart-passage-link` and its `onClick`, and `aria-expanded`;
- each OPEN passage block carries `data-driver-chart-passage-source`;
- the table is `<table data-driver-chart-passage-table>` with a `<th>` per column label;
- each segment heading carries `data-segment-heading`, and each row keeps `data-segment-row`;
- the open state stays in React state (`useState` or `useReducer`).

**The existing harnesses** under `portal/src/pages/SecurityAnalysis/__harness__/` assert on today's markup. Run the ones that
name `data-driver-chart` or `data-segment` (`node <file>`), and re-anchor only the assertions your change moves. Say which.

**A render for the review.** Write `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~271/RENDER_BA5.md`: for BA (a table passage, three ids) and ASML NA (one shared id), the page's rendered
text of the driver chart after one press and of the segment breakdown, from the fixture `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round77/checks/r77_groupB_fixture.json` (the deployed /thesis
bytes of four names). If `scripts/ui-smoke.mjs --dist` can capture `/security-analysis/BA_US_Equity` with that fixture, add the
PNGs under `captures/`; if it cannot, say why in one line and file no row.

**Commit inside the nested `portal/` repository** on branch `wk-AMGT_RESAPP-271-portal`; report the commit hash and do not push.
The candidate goes to the CTO, who reviews it from a render. The DEV push is Andrew's word.

**Stamp any surprise row's `surfaced_at` with `date -u +%FT%TZ` at filing.** Rows: id form `AMGT_RESAPP-Z-W271-S<k>`, `disarm_owner` `2.0.0_SA_COO~Z`.

## 2. BOUNDS

1. Write only the paths below. No push, no deploy, no store write. Do not edit `App.tsx`, the Thesis tab's layout or any other
   component.
2. Presentation only: no number is computed, joined, rounded in the table or rewritten. The axis formatter is the one
   place a figure is shortened, and only on the axis.
3. Colours and type come from the design system's tokens already used in these two files. No new colour.
4. Plain words on the page; no internal names (identity, security key, crosswalk, dossier, model block, input ledger, passage id).
5. Standing: no S3 delete, no push of shared branches.

## 3. SURFACES

<paths>
portal/src/pages/SecurityAnalysis/components/ThesisDriverChart.tsx
portal/src/pages/SecurityAnalysis/components/PassageTable.tsx
portal/src/pages/SecurityAnalysis/components/SegmentBreakdown.tsx
portal/src/pages/SecurityAnalysis/types.ts
portal/src/pages/SecurityAnalysis/__harness__/
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~271/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

## 4. PROOF OF SPEC (literal; timeout 600)

<proof_of_spec>
  <criterion id="AC1" cell_refs="AMGT-ba-5"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round77/checks/r77_ba5.py" --crit AC1 --where local; echo "exit=$?"</invocation><expect>one press opens ONE passage where three points share an id, a press on another point moves it, a second press closes it, and the three-id control opens one; C1-C5 PASS; R77 BA5 AC1 SERVED: YES; and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="AMGT-ba-5"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round77/checks/r77_ba5.py" --crit AC2 --where local; echo "exit=$?"</invocation><expect>BA's served table is drawn with its six column labels, both row labels and every figure; the no-table control draws none; the y axis formats a nine-digit figure in 7 characters or fewer and keeps 528 exact; an ABSENT chart shows its served plain reason; C1-C10 PASS; R77 BA5 AC2 SERVED: YES; and exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="AMGT-ba-5"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round77/checks/r77_ba5.py" --crit AC3 --where local; echo "exit=$?"</invocation><expect>BA's 11 rows sit under 3 headings in first-served order, each name alone once; the one-label and no-row controls hold; C1-C6 PASS; R77 BA5 AC3 SERVED: YES; and exit=0</expect></criterion>
  <criterion id="AC4" cell_refs="AMGT-ba-5" judgment="true"/>
</proof_of_spec>

A fourth criterion: AC4 is the CTO's judgment on the render (a portal candidate is reviewed from a render), not a fourth mechanical check.

## 5. WHEN YOU ARE DONE

Commit in your worktree via `.tools/safe-commit.sh --author "0.9.0_WK_AMGT_RESAPP~271 <0.9.0_WK_AMGT_RESAPP~271@opal.agent>" -F <msgfile> -- <paths>`
(message file written with the Write tool; confirm with `git log -1`). Instance at
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~271/AMGT_RESAPP.TO-AMGT-ba-5.passage-once-table-labels-axis-segment-headings.proof_of_spec.json`.
Run `python .tools/proof-of-spec-check.py <instance>` on the committed bytes and report its verdict line. Do not stage `portal`.
Report once:
- the commit hash;
- every criterion's output lines;
- the portal commit hash and branch;
- the existing harnesses you ran, and which assertions you re-anchored;
- any row.

The `<status>` flip is the issuer's.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES:** CTO round-76 analysis ruling 6, enrichment item 5; rows Z-W266-S2 (one heading per segment) and Z-W266-S3. Scope
set at the cut: all of ruling 6 measured as PAGE defects (the served `passage_table` is already there for BA), so this is a portal
cell on a DSGN_AMGTV1 page (`2.0.0_SA_COO~D`'s lane); the "one heading per segment" item of ruling 7 is page work too and sits
here, not in ba-6. Checks dry-run at portal origin/DEV 13509c52: AC1, AC2, AC3 base FAIL as expected (open 3; tables 0 and no
formatter; headings 0). AC4 is the CTO's render review. The DEV push is Andrew's word.

status: handoff draft (never issued in AMGT_RESAPP)
<round>77</round>
<slot>0.9.0_WK_AMGT_RESAPP~271</slot>
<fabric>site-z</fabric>
<risk>LOCAL</risk>
<worker_class>worker</worker_class>
