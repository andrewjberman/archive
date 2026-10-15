# ADVI_BILLING resume packet -- dell2 hands the project to dell1 at a closed round; nothing in flight, nothing cut

**By:** `2.0.0_SA_COO~B2`, 2026-10-14 ~18:5xZ. **For:** the dell1 seat that takes ADVI_BILLING, `1.0.0_SA_CTO~DELL2` (hand-over reader) and
`0.0.0_AB_MSTR~DELL2` (seating).
**Basis:** Andrew-direct 2026-10-14 ~18:5xZ, verbatim: "Moving all advisor intelligence ops to DELL1. Basically devote DELL1 wholly to
ADVI/MDPF work as well as any overflow AMGT work." Record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_185xZ_DELL1_WHOLLY_ADVI_MDPF_AMGT.md`
(@37e2467986): ADVI_BILLING moves to dell1 at its next round boundary, dell2 writes this packet. Placement ruling and flat index row are already
changed by the CTO (`project.json` reads `fabric dell1`, `placement DELL1`, `dep_stage EXECUTING`, round 3).
**Boundary:** round 3 closed 2026-10-09 (drain-end `r3_close/DRAIN_END_R3.md`, MAY-CLOSE 3 of 3, CTO ADDENDUM 4 @44f3540b16). No round is in flight
on dell2, so the hand-over is NOW. This packet cuts nothing, sizes nothing and edits no row.

## Measured at the time of writing

| item | reading | source |
|---|---|---|
| PRD | v0.2 ADMITTED, brief half SIGNED, ratified-text half SIGNED | `sequence-check --project ADVI_BILLING` |
| surprise channel | 28 items: 0 open, 0 armed, 7 graduated, 21 dismissed with reason; 0 defects (denominator 1451 files) | `comp-surprise --project ADVI_BILLING` |
| task orders | 0 active TOs for the project (denominator: 6637 faces scanned); rounds 1-3 each read MAY-CLOSE at their drain-end | `to-check --all --project ADVI_BILLING`; `r1_close` `r2_close` `r3_close` |
| open calls | `dell2-20261014T110546Z-cab3` (panel PROD push) CLOSED DECLINED | `open-calls.py list` |
| dell2 worktrees / branches for this project | none found by `git worktree list` and `git branch --list` | read at write time |
| sequence flag | UNMEASURED/WAITING: Andrew holds each firm's answers on billing system, fee terms and sign-off (Q-2 brief PART V) | `sequence-check` |

## What changed since round 3 closed (the ruling that shapes the resume)

CTO relay msg 7563 (laptop msg 109106), from `RULING_20261013_173xZ_CLUSTER_POSITIONING_ON_THE_PIVOT_AGGREGATE.md` line 32: **no second billing panel
on PROD.** Custodian fees feed the EXISTING Fee Summary panel ("we don't want to duplicate"). The advisor-book fee panel on portal DEV (`6d383958`)
is therefore NOT pushed to PROD, and the PROD-push route to realize FWD-1 is closed. The project stays parked; on un-park the work is to wire the
custodian fee into the existing panel. Under the 2026-10-14 portal law (`CLAUDE.md` Portal) any portal change goes through
`.tools/portal-merge-forward.sh cand/<box>/<slug>` on an approved row.

## The FWD list as I read it (the CTO's grade governs)

| FWD | state | what stands in the way |
|---|---|---|
| FWD-1 (one live journey end to end) | EXERCISED on DEV; was to realize on the PROD push | PROD push declined (above). Needs the CTO's re-statement of what realizes FWD-1 now that the panel is the existing Fee Summary. |
| FWD-3 (empty states) | REALIZED, graded by `3.0.0_SA_CVO` (@28215996eb) | none |
| E2 (SMArtX fee statement ingest) | NOT applied. Release packet `0.9.0_WK_ADVI_BILLING~7/RELEASE_PACKET_E2.md` is with site Z, cell `OG-ab-1` (built @17828a452d); site Z took it (msg 3104), `AE~Z` applies under its own never-widen pair. Per `1.0.0_SA_CTO~Z` (XB-ad8b, @6a81b7276e) the first E2 put is this project's. | site Z's deploy. Row D2-W7-S1 (BLOCKING for the release) is carried by site Z. I did not re-read site Z's queue today. |
| FWD-2, FWD-4, FWD-5, FWD-6 | not started | the CTO's round-N analysis names the cells. The round-1 enrichment list was E1 (book check), E2 (fee ingest), E3 (durable crosswalk), E4 (FWD-3 grade); read `r2_close/` for which round 2 served. I did not re-measure that today. |

Not measured today: whether E2 has since landed on site Z, and whether the Fee Summary panel already carries a custodian field. Read both first.

## What the dell1 seat must read, in order

1. `org/tier1_exec/1.0.0_SA_CTO/deliverables/RULING_20261013_173xZ_CLUSTER_POSITIONING_ON_THE_PIVOT_AGGREGATE.md` (the no-second-panel ruling).
2. `org/missions/D8/ADVI/ADVI_BILLING/deliverables/2.0.0_SA_COO~B2/r3_close/DRAIN_END_R3.md` and `r2_close/`, `r1_close/`.
3. The drive log `org/tier1_exec/2.0.0_SA_COO~B2/drive_log_20261009T10Z_desktop-n8rjv0a.md` (the substantive ticks, verbatim).
4. The PRD `org/missions/D8/ADVI/ADVI_BILLING/prd/ADVI_BILLING_PRD.md` and its ADDENDA 1-4 in the CTO's deliverables folder.

## Things that do not travel by git

- The real-data fee-panel render (client figures) is private on dell2 at `C:/dev/advi_billing_private/r3_close/r3_realrun_fee_panel.png`
  (sha256 prefix `8e941d5e`). It was the CVO's grading evidence and is not needed to resume. The invented-data fixture render sits in
  `r3_close/r3_fixture_fee_panel.png`. If dell1 needs a real render it makes its own, under the same privacy rule.
- Probe identity for the cross-firm arm was minted by `0.7.0_AE_CloudOps~AB2` (ledger closed @8cab625508). It does not move; a fresh probe needs a
  fresh CloudOps lane on dell1 (seating lint).

## Seating

One project per Tier-2 seat instance: dell1 seats a fresh `2.0.0_SA_COO~<lane>` for ADVI_BILLING (and a second lane for ADVI_COTBKF, which stays on
hold). `0.0.0_AB_MSTR~DELL1` seats it, or `0.0.0_AB_MSTR~DELL2` on its behalf. This lane (`~B2`) issues nothing further and stops at hand-over.

## What resume runs

`python .tools/drive-mode.py full ADVI_BILLING`, the CTO's round-N analysis cut from this packet and the FWD table, then one issuance by the dell1
lane. No loop is armed for this project and `org/ref/LIVE_ARMS.md` carries no row for it.
