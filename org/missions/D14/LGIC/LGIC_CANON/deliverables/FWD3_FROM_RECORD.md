# FWD-3 FROM THE RECORD -- what ended the pause, per IRPT project

**Cell:** `CN-r-2` (LGIC_CANON round 1; PRD DEC-4; cell candidate C4) | **Order:** `LGIC_CANON.TO-CN-r-2`
**Written by:** `0.9.0_WK_LGIC_CANON~3` | **Read at:** worktree HEAD `83afab6973` (branch `wk-lgic-canon-1-3`, cut from `CLOUD` @`f95470f384`)
**FWD-3's ACCEPT:** the person running a paused project *"can point at what ended the pause -- either nothing in
their plan conflicts, or here is the list of things to change, or here is the other project whose answer decides
theirs"*. The three branches are written `nothing-conflicts`, `list-of-changes` and `derived`.

What ended the pause for BOTH projects is ONE row: card 1 of the nine-calls record, `:32`, which reads *"(a) BOTH
IRPT projects. THE PAUSE IS LIFTED, by his word, by name. IRPT_BCKEND's three CONTRADICTS become L4 amendments in
its normal loop (`1.0.0_SA_CTO`), not pause conditions."* Andrew's words for that card are at `:15-16` ("agree with
all ..."). The record's bytes are unchanged from `c6be748be7` to HEAD (`git diff --stat` empty).

---

## THE BRANCH EACH PROJECT TOOK

PROJECT IRPT_FNTEND: branch derived -- pause ended by card 1, `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260913_013xZ_NINE_CALLS_RULED_PAUSE_LIFTED_D10-2_DEMO_KEPT.md@c6be748be7` :32; the other project whose answer decides theirs is IRPT_BCKEND, per `infra/logic/03_CONTRADICTION_REPORTS/IRPT_FNTEND.md@a4cc0cb681` :15-16 ("their grade is DERIVED from IRPT_BCKEND's rows 1, 1b and 3") and :33-34 (DERIVED FROM IRPT_BCKEND rows 1, 1b / row 3)

PROJECT IRPT_BCKEND: branch list-of-changes -- pause ended by card 1, `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260913_013xZ_NINE_CALLS_RULED_PAUSE_LIFTED_D10-2_DEMO_KEPT.md@c6be748be7` :32, which turns the three CONTRADICTS into L4 amendments; the list of things to change is `infra/logic/03_CONTRADICTION_REPORTS/IRPT_BCKEND.md@a4cc0cb681` :18 (three CONTRADICTS), :35 (row 1b, R1), :36 (row 2, R11 + R14), :37 (row 3, R4 partial)

Reading notes (not a grade; R2-J1 is graded at L9 by `3.0.0_SA_CVO`):
- IRPT_FNTEND's four surfaces sit in wire-contract files, not in its PRD (`IRPT_FNTEND.md@a4cc0cb681` :26). Its
  PRD is at v0.6 (`org/missions/D9/IRPT/IRPT_FNTEND/prd/IRPT_FNTEND_PRD.md@d1479bc5f0` :8). That PRD names
  IRPT_BCKEND as the counterpart that owns the `/api/scoped/investor-reporting/...` routes (:210) and the export
  worker (:206). Nothing in FNTEND's derived grade can close before IRPT_BCKEND's list does.
- The IRPT_BCKEND report says its row `W2-S49` ("the scheduled-gold host cannot write any of the three
  destinations") *"most bears on whether 'resume' means anything yet"* (`IRPT_BCKEND.md@a4cc0cb681` :21-23,
  :65-67). That is a claim in the report, recorded here and not graded. The report's own channel denominators
  (188 rows, 71 dispositioned) are marked perishable by the report (:62-63), and this record does not re-take them.

---

## IRPT_BCKEND: THE PRD AT HEAD AND WHAT IT ABSORBED

IRPT_BCKEND PRD AT HEAD: v0.14 (MEASURED)

Instrument: the `"prd_version"` field at `:8` of `org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md`, read
at worktree HEAD `83afab6973`. The last commit touching the file is `b8e98d5a4d` (the L4 v0.14 commit), and
`git diff --stat b8e98d5a4d HEAD` on the file is EMPTY. The `CLOUD` tip read at the same time (`5061a43a46`) is
also v0.14, and `git diff --stat HEAD CLOUD` on the file is EMPTY. So the PRD's bytes at HEAD are the bytes the
IRPT_BCKEND report graded (`IRPT_BCKEND.md@a4cc0cb681` :4, "at L4 v0.14 `@b8e98d5a4d`"), and that is where it
found the three CONTRADICTS.

CONTRADICTS ABSORBED: 0 of 3 (MEASURED)

**All three are STILL OPEN.** Card 1 made each one an L4 amendment in IRPT_BCKEND's normal loop at `1.0.0_SA_CTO`.
None has landed, so all three are owed at that PRD's next L4 re-entry. DEC-4 says the same thing; this line re-measures it
instead of copying it. There are two instruments. The first is the empty byte diff above: nothing has changed since
the vintage the report graded. The second is a token census of the PRD at HEAD, 322 lines:

| # | CONTRADICTS | what absorption would look like | measured in the PRD at HEAD | state |
|---|---|---|---|---|
| 1 | the `platinum/` prefix (R1; report row 1b) | a `platinum/` tier segment in the destination key, or an R20 declaration | `platinum/`: 0 of 322 lines. `platinum`, case-insensitive: 3 lines. `:129` is the tier label BRONZE-SILVER-GOLD-PLAT. `:196` and `:312` still read `<FIRM bucket per FIRM_BUCKET_MAP>/investor-reporting/...` with no tier segment. `R20`: 0 lines | **OPEN** |
| 2 | the gold parquet artifact between silver and the served JSON (R11, R14; report row 2) | a named gold parquet artifact and its home, upstream of the PLATINUM JSON | `parquet`, case-insensitive: 2 of 322 lines. Both (`:125`, `:216`) are INPUT evidence ("23 Parquet objects, 15,753,977 bytes"), not a gold artifact. `:196` and `:311` still have the gold-named runners write PLATINUM JSON directly | **OPEN** |
| 3 | the vendor PDFs' home (R4, partial; report row 3) | vendor deliverables landed at `opal-data-assets/ycharts/{firm}/bronze/...`, or an R20 declaration naming the reason | `opal-data-assets`: 0 of 322 lines. `R20`: 0 lines. `:199` and `:313` still put `vendor/report.pdf` and `exports/{revision}/report.pdf` under `opal-data-ycharts` `firms/{firm_id}/...` | **OPEN** |

Denominator: 3 CONTRADICTS named by the IRPT_BCKEND report (`@a4cc0cb681` :18). Absorbed at HEAD: 0. Open: 3.
Limit of the census: a token count could miss an absorption worded without these tokens. The empty byte diff
against `b8e98d5a4d`, the vintage the report graded as CONTRADICTS, is what rules that out.
