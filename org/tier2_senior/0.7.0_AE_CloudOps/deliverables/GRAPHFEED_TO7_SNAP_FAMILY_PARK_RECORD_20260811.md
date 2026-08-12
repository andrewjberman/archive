# PARK RECORD: the GRAPHFEED TO-7 snap family (decommission-class, fully reversible)

**Ruling:** CTO 20260811T181041Z PARK-WITH-RECORD (routed via COO 181242Z) | **Executor:** 0.7.0_AE_CloudOps
**Determination this record carries:** my 180527Z bounded read (COO dispatch 175528Z; finding by CRO~B + CVO)
**Program-value half:** CARRIED CARD to Andrew -- does he want a realized-diversity feed at all.

## THE FINDING: NEVER LAUNCHED (not superseded, not gone-dark)

The four "nightly" snap surfaces (`code_heat_snap`, `fedobs_coverage_snap`, `fedobs_coevolution_snap`,
`ms_heat_snap`) are NFRA_GRAPHFEED TO-7's own deliverable (P1 `snap_store.py` writer, P2a
`code_heat_emit.py` stager, P2b `emit_fedobs_snap.py` stager -- in-code TO citations). They ran
EXACTLY ONCE EACH, during their own build:

- **done/ census: 5 batches TOTAL**, every one dated 2026-07-16 or 2026-07-17 (full recursive listing).
- **Heartbeats written once each** (single `last_append/{surface}.json` objects, same two days).
- **THE LOAD-BEARING CONTROL -- the census is HISTORY, not a survivor set:** bucket lifecycle on
  `opal-313476888478-globgrph` carries exactly ONE rule (`abort-incomplete-mpu-7d`); NOTHING expires
  `done/`. Without this check, 5 sparse batches would be indistinguishable from an expiry policy
  having eaten the evidence, and every conclusion below would rest on an absence that could not be
  told from a deletion.
- **`pending/` is EMPTY**: the in-VPC ingest swept everything it was ever given -- the starvation is
  EMIT-side; the ingest half never broke.
- The CVO discriminator (ms_heat Iceberg newest snapshot `20260717T180941Z`) matches the last done
  batch exactly -- table data and staging agree.

## NO SCHEDULE EVER EXISTED (the ad-hoc-is-never-production class, frozen at birth)

- **Default event bus: 139 rules materialised, counted client-side** (the pagination law -- no
  `--query length`, no `--no-paginate`). 5 globgrph-family matches: `opal-globgrph-comp-learns-
  producer-nightly` cron(0 4) · `opal-globgrph-derive-runner-nightly` cron(0 2) ·
  `opal-globgrph-fedobs-producer-nightly` cron(30 4) · `infrastructure-snapshot-daily` cron(0 7) ·
  `opal-globgrph-cloudtrail-mgmt` (event). **NONE covers snap staging or `--ingest-pending` sweeping.**
- The rule cited in the routing as "the adjacent ENABLED schedule" -- `globgrph-cse-producer-nightly`
  -- **DOES NOT EXIST** on the default bus (live ResourceNotFoundException; stale name).
- **Device side: 0 scheduled-task matches** under heat/snap/globgrph/cse/graph/fedobs.
- Falsified en route: "the owner lane died and it stopped" -- `0.8.0_AE_CloudComp` logged through
  2026-08-07, three weeks past the freeze. The family's only trigger was ever its builder's session.

## RULING GROUNDS (CTO, verbatim substance)

Never launched => no serve, no consumer-in-fact, no never-widen exposure. The only citation is a DOC
claim, and **a doc is not a consumer**. Standing up three schedule legs mid-program for an
unproven-value feed inverts the moratorium's own ordering; this program's canonical schedule work is
P2, which this is not part of. Park-with-record is fully reversible.

## DISPOSITION OF ARTIFACTS -- ⛔ NO DELETIONS

The 5 build-day batches (`done/`), the heartbeats, the Iceberg `_snap` tables, and all three
stager/writer modules **STAY AT REST**. CTO classification: Rule 25 dormant, **exception-kind =
build-artifact**. Dormant is never a deletion warrant. Nothing scheduled, nothing built, no monitor
(standing moratorium honored throughout).

## SAME-ACT DOC FIX (the map-vs-territory closure)

`infra/system/06_current_state.md` cited the fedobs snap heartbeat as "the GRAPHFEED standing snap
(nightly)" realized-diversity source -- a living-feed claim about a single build-vintage table. The
doc is GENERATED (`org/modules/graph/comp_system.py` -> OUT_MD), so the fix landed AT THE GENERATOR
(this same commit): `_read_snap_realized()` docstring + emitted vintage string + the PRIMARY note now
carry `[PARKED 2026-08-11 ...single build-vintage... not a living feed]` on every future generation,
and the doc was regenerated in this act. A hand-edit of the .md alone would have been overwritten by
the next generation -- the generator is the single home.

## RE-ENTRY CONDITIONS (so the next reader does not re-derive the census)

If Andrew's carried card comes back wanting the feed, it re-enters as **DESIGNED P2-class schedule
work through the front door**, not a resuscitation:
1. **code_heat**: dev-box-resident BY RULING (TO-2, git-history-shaped over local repos) -- needs a
   DEVICE-side schedule (the `OpalEstateCaptureDaily` / B6 registration pattern is the proven shape)
   or a revisit of the TO-2 ruling.
2. **fedobs coverage+coevolution**: AWS-runnable in principle -- the stagers only READ the served
   `fedobs_observations.json` via S3 GetObject, and the upstream fedobs producer's in-VPC nightly
   (cron(30 4)) is alive today.
3. **ms_heat**: PLAUSIBLY AWS-runnable (an engine over the MS slice of the canonical warehouse) --
   verify its data access FIRST; deliberately not deepened under the bounded read.
4. **The ingest half** (`snap_store --ingest-pending`): in-VPC by design, AWS-native -- needs its own
   schedule (or event wiring off pending-landings PLUS a schedule floor, per the standing rule).
5. Whatever re-enters must land WITH its production schedule in the same act -- the defect this park
   records is precisely a build that shipped without one.
