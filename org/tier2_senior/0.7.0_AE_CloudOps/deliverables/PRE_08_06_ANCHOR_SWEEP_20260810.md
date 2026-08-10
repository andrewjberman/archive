# Pre-2026-08-06 ANCHOR SWEEP — MDPF trigger/schedule workstream

**archetype:** VALIDATE · **Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-08-10
**GO:** `2.0.0_SA_COO` 145651Z, bounded. **Standing check adopted by CTO** (145427Z):
*"the 07-29 commit / 2026-08-06T00:04:48Z apply moved BOTH the eclipse landing pattern AND the cot
delivery clock. ANYTHING ANCHORED BEFORE 2026-08-06 IS RE-DERIVE, NOT TRUST."*

**RESULT IN ONE LINE: the sweep found NO NEW un-caught stale anchor.** Every pre-apply anchor in
scope had already been caught today. That is a real negative, and §4 states exactly what it does
and does not cover — because an absence claim without its frame is the error I made earlier today.

---

## 1. Scope + denominator

**Sources enumerated (the frame):**

| source | anchors found |
|---|---|
| `org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_TRIGGER_SEQUENCE_DIAGNOSIS_20260810.md` @087938fa61 | 10 schedule + 3 delivery + 4 vintage |
| `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_REMED_DECOMPOSITION_AND_SEQUENCE_20260810.md` @e1c891366a | carries the above + 3 delivery |
| `MDPF_REMED.W1-5` (25 timing lines) · `W1-4` (4) · `W1-2` (1) · `MDPF_CANPLAT.P0-2R` (3) · `P0-7R` (0) | 33 lines scanned |

**The apply boundary:** `ce99054e44` committed 2026-07-29, **applied 2026-08-06T00:04:48Z**
(Scheduler `CreationDate == LastModificationDate`).

## 2. The anchors split into three classes, and only one class can go stale

**CLASS 1 — SCHEDULE EXPRESSIONS (the 10 in the diagnosis + everything in W1-4/P0-2R).**
**RE-DERIVED BY CONSTRUCTION — no staleness possible.** I read all of them live today: 139
EventBridge rules (121 scheduled) + 16 Scheduler schedules, materialised and counted client-side.
A cron expression read today *is* today's value. The decomposition (line 373) already credits these
as "carried from `0.7.0_AE_CloudOps`'s live reads, credited not re-measured" — correctly.

**CLASS 2 — MEASURED DELIVERY / LANDING CLOCKS.** The only class that can be stale, because it
describes *the world*, not *the config*. Table in §3.

**CLASS 3 — EVENT OBSERVATIONS DATED 2026-08-07 OR LATER.** Post-apply, in the current regime,
nothing owed. (The 22:47:19Z inflection refusal, the 22:47:09Z 49financial write, the missing
`date=2026-08-06` partition, the served-vintage table CTO measured today ~13:0xZ.)

## 3. CLASS 2 — the sweep table

| # | anchor, as recorded | taken | vs 08-06 apply | re-derived value | verdict |
|---|---|---|---|---|---|
| 1 | **"BD xlsx lands 02:00Z nightly"** (diagnosis §4, decomp :276) | carried from the ingestion draw, undated | **PRE** | `forwardfill_v2/` xlsx: **10 consecutive days 02:0xZ (07-27→08-05), then 20:3xZ (08-06→08-09)** | **MOVED** ✅ caught today |
| 2 | cottonwood bronze delivery (implied by #1) | — | **PRE** | `blackdiamond/cottonwood/bronze/` **06:00:43–48Z daily**, a *second producer* (`cot-rebalancer-runner`) | **MOVED + MISATTRIBUTED** ✅ caught today |
| 3 | **eclipse silver lands T+1 03:30Z** (W1-5 context) | 08-07 TO; underlying data spans 08-01→08-07 | **SPANS** | **22:31:07–10Z**, 3 consecutive days | **MOVED** ✅ caught today |
| 4 | **orion silver lands T+1 03:30Z** (same table) | same | **SPANS** | **14:16:03–06Z, unbroken 07-20→08-09** | **NEVER HELD** — not stale, *misattributed from the start* ✅ caught today |
| 5 | jwt mint clock **12:15Z** (Clock-v3 record) | pre-dates the record | **PRE** | plane: `cron(5 12)` = **12:05Z**, mint *lands* 12:06:33Z | **WRONG, already corrected** by `~Z` in P0-2R |
| 6 | SmartX silver lands 13:40–13:42Z | P0-2R, 2026-08-07 | **POST** | not re-derived (fence) | **IN-REGIME** ⚠ method bound stands |
| 7 | Orion vendor early-valid 12:10Z | P0-2R, 2026-08-07 | **POST** | not re-derived (fence) | **IN-REGIME** |
| 8 | jwt mint *lands* 12:06:33Z (~93s after cron) | P0-2R, 2026-08-07 | **POST** | not re-derived (fence) | **IN-REGIME** |
| 9 | `silver/assets_v2/2026-08-07.parquet` wrote 16:00Z | W1-2, 2026-08-07 | **POST** | not re-derived (fence) | **IN-REGIME** |

**Pre-apply anchors: 5. Already caught before this sweep began: 5. NEW findings: 0.**

### What the zero means, and what it does not

It is **not** "the anchors are fine." It is: **the two independent bites we took from this apply
today (BD 02:00Z, eclipse 03:30Z) appear to have exhausted the pre-apply anchor set *within this
frame*.** Row 5 is the useful corroboration — a *third* pre-apply anchor that was independently
wrong and independently caught, by `~Z`, before either of today's. The class CTO named is real and
has now produced three instances; what the sweep says is that this workstream's own surface has no
fourth.

## 4. ⚠ WHERE THIS SWEEP STOPS — the frame, stated because the absence claim is the deliverable

COO's fence was *"do not extend past this workstream's anchors into the wider MDPF program."* CTO's
standing check was broader: *"**every timing figure in the MDPF remediation record** predating that
apply is now suspect by default, including ones nobody has questioned."*

**THOSE TWO ARE NOT THE SAME SURFACE, AND I HAVE SWEPT THE NARROWER ONE.**

**NOT COVERED — named, not swept:** the MDPF remediation register `R-1..R-32`
(`docs/architecture/MDPF_REMEDIATION_REGISTER.md`), the MDPF PRDs, the CANPLAT P1/P2/P3 TO family,
and any timing figure in the INF or cot programs. **My "0 new findings" says nothing whatever about
those.** If CTO wants their standing check discharged at its stated width, that is a second sweep
with a different denominator, and it should be scoped as one rather than inferred from this result.

*This section exists because I spent a correct denominator on a filtered domain earlier today
(§8.1 of `INFLECTION_INGEST_WINDOW_RETIME_20260810.md`) and manufactured false completeness. A
clean zero is exactly the shape that error takes.*

## 5. Free observation, per COO's note — NOT a finding

`blackdiamond/cot/session-trigger-mode.json` (referenced `cot-bd-session-trigger/lambda_function.py`
as `MODE_KEY`) is a **mode-state marker the Lambda writes to select its own invocation mode** —
the `session-refresh` / `session-check` branch named in its docstring `:6-20`. It is control state,
not a data sidecar. **I did not open the object**, so this is read from the code's use of it, not
from its content. Not claiming R-20 sidecar class either way. Cost: one grep already in path.

## 6. Compiler Tools

| Tool | Result |
|---|---|
| `comp-find "forwardfill_v2"` | 604 hits / 24,960 files · **DEF=19** — the `[DEF]` band put `cot_bronze_ingest.py:64` and the bd-exporter TS sources on definition lines directly |
| `comp-find --name "*cot-bd-session*"` | **0 / 7,732** — a measured zero; the file exists under a *directory* of that name, so the printed denominator is what stopped me reading zero as absence (same trap as `*ingest-mirror*` earlier today) |
| `comp-find "ingest-mirror-cot-daily"` | 3 / 7,730 · SURFACED=1 CONFIG=2 |
| raw `aws` (s3api/events/scheduler/lambda/logs/cloudtrail/ec2/ssm) | APPLIED reads — Rule 22a: a comp-tool reads DESIRED and cannot tell landed from planned |

**Instrument note worth carrying:** CloudTrail **cannot** answer S3-write attribution on
`opal-data-assets`. Its data-event selectors cover `opal-data-bd/` + `opal-data-inf/`, **ReadOnly**,
and the served-key trail covers `opal-data-{inf,bd,cot}/platinum/firm/` writes only. That is a
**NOT-MEASURABLE**, not an absence — stated plainly per COO's instruction, since "we cannot see it"
and "it is not there" are different findings and the second is the dangerous one. The producer was
named by **key-grammar partition** instead (687 json vs 368 xlsx), which needed no new telemetry.

## 7. State

**Nothing applied. No schedule touched. No gap plan started.** Fences held: re-derived without
diagnosing, stayed inside the workstream, one line to COO on out-of-scope, and §4 declares the
frame rather than letting a zero imply a width it does not have.
