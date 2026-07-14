# OPAL_ASSETS.C2 — The polling mirror: Orion / Eclipse / cot bronze into the monolith (three rows, never grows)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (coordination lane, Andrew-direct ~01:07Z) — authored from PRD v1.3.1 §4 row C2, RESHAPED to the C2 mechanism ruling (CTO, 2026-07-14 ~02:23Z, effective on message; PRD ruling 18 text lands with his next commit) under THE NEW-TERRITORY RULE (Andrew-direct ~02:05Z); architecture owner remains 1.0.0_SA_CTO</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<state date="2026-07-14 ~04:4xZ" by="2.0.0_SA_COO (reconciliation)">
INFRA APPLIED + LIVE (8/0/0, both schedules ENABLED, ~03:40Z). FIRST BACKFILL CORRUPTED by a dst-key
collision (the {type} segment dropped: 2,781 writes -> 2,269 type-collapsed orion keys; eclipse 624/624 +
cot 30/30 CORRECT) -- source-confirmed 55dd545d2; the write-count denominator PASSED it (doctrine: guards
assert SET-IDENTITY/DISTINCT-COUNT, never a call tally). CORRECTED FIX at CTO's gate: (i)+(ii) accepted,
(iii) reworked to per-key set-membership + classified surplus (the 2,269-orphan masking-budget catch,
ruling ~04:39Z), GO PRE-GRANTED on the reworked commit. The 2,269-orphan DELETION is AUTHORIZED --
ANDREW, VERBATIM (to COO, ~05:1xZ): "Yeah let's get that cleand up, maybe 0.6.2 can do it when theyre
done with the docs i asked them fpor." EXECUTOR: 0.6.2 per Andrew's staffing, SEQUENCED AFTER the docs
Andrew asked him for directly (that request lives in 0.6.2's own channel; his knowledge of it governs
the sequencing). PROCESS: 0.7.0 supplies the exact orphan key list from the membership guard's
classifier (flat {dst_prefix}{date}.jsonl.gz, no further '/'); each key re-verified against the class
before deletion (never a bare recursive rm); key list snapshotted as evidence; bucket versioning is ON
(ruling 17) so the deletion is REVERSIBLE (delete markers; objects survive as noncurrent versions).
POST-DELETE: 0.7.0 re-runs the guard -> surplus drops to 0 -> the C2 close tightens to clean
set-identity with an empty allowlist, no code change (per the gate ruling).
</state>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 row C2 + ruling 16 (raw-only) + the C2 mechanism ruling (msg 20260714T022304Z; PRD ruling 18 pending commit) — authored against v1.3.8 @ a0ed08933</prd>
<sequence>SECOND in your lane, after C1 is applied + verified. The mirror has no landing target until the bucket exists, and its schedule/role are "to add" resources that ride the SAME CTO apply-gate discipline.</sequence>

## THE NEW-TERRITORY RULE (Andrew-direct, ~02:05Z — this TO's shape exists because of it)

> "We're building this in parallel, there should be no reason to touch the existing buckets/structures,
> we are building a new territory."

**THE MONOLITH IS BUILT ALONGSIDE THE ESTATE. WE DO NOT MODIFY EXISTING BUCKETS, EXISTING BUCKET
POLICIES, EXISTING NOTIFICATION CONFIGS, OR EXISTING SCHEDULERS TO GET THERE. A TERRAFORM PLAN THAT
SHOWS ANYTHING OTHER THAN "TO ADD" IS OUT OF SCOPE UNTIL ANDREW SAYS OTHERWISE.**

The original C2 design (event-driven copy Lambda attached to source-bucket notifications) is DEAD under
this rule — every event-attach touches an existing bucket's config, including EventBridge-mode (it flips
a setting on the existing bucket). The S3 notification-config singleton hazard (PRD §2, §5 R4) is
thereby retired for this TO — not cleared, AVOIDED: we never go near any source bucket's config.

## Scope — the ruled mechanism (CTO, ~02:23Z, verbatim-faithful)

**A POLLING MIRROR. A NEW Lambda, on its OWN new schedule, read-only on sources. Exactly THREE rows:**

```
orion/inflection      <- opal-data-inf bronze (orion pulls)     poll ~14:15Z (pulls end ~13:47Z)
eclipse/inflection    <- opal-data-inf bronze (eclipse daily)   poll with orion's window
blackdiamond/cottonwood <- opal-data-cot bronze (nightly cube)  poll after cot's nightly window
```

- These three exist because their producers CANNOT be retargeted: orion/eclipse belong to the HELD INF
  chain; the cot estate stays untouched. **Everything else lands NATIVE** (schwab C3, ETF C4, SmartX C5).
- **The map is born with three rows and NEVER GROWS.** It dies when OPAL_RUNNERS eventually rebuilds
  those pipelines monolith-native. A fourth row is an architecture fork for CTO, not a map edit.
- Mechanics: ListObjectsV2 + GetObject on sources under the mirror's OWN role; copy to the canonical
  monolith key per the static map; never transforms — bytes in, bytes out. **Ruling 16 binds: RAW
  objects only — the map never contains a `.parquet` under any bronze path.** The 10 known parquet-only
  INF dates (and each new one until the INF hold lifts) are HONEST HOLES; coerced survivors stay in
  `opal-data-inf`, C12-inventoried, importable later only by explicit ruling into a labelled `_coerced/`
  prefix.
- Idempotent skip-if-landed; an absent source day is ABSENT in the monolith; verify per ruling 13c's
  3-tier protocol (listing-ETag single-part / source-stream-MD5 multipart / size always).
- **THE DENOMINATOR MANDATE (DS request 02:27Z, COO-adopted; ruling-11a precedent — the T1 hard-raise,
  one layer up):** the mirror EMITS ITS COUNTS every cycle — objects enumerated in the source window vs
  objects written/skipped in the monolith — and **RAISES on a mismatch rather than logging it.** A
  per-object event model is structurally blind to the object that never arrived; a polling mirror
  necessarily enumerates the source window, so the denominator is free AT BUILD TIME and unbuildable
  later. A mirror that copies 37 of 40 and exits 0 is indistinguishable from one that copied 40 — only
  the mirror is ever in a position to know, so it publishes. *(This is a hard-raise inside the component
  — the ruling-11a class, not a new alarm/watchdog under §0's constraint; CTO ratifies the distinction
  at the plan gate.)*
- **Monolith-side event wiring is UNCHANGED and stays event-driven** — `opal-data-assets` is new
  territory; its own notification config is ours to create freely, and DS's C6 parsers fire on the
  monolith's ObjectCreated. Only SOURCE-bucket attaches are dead.

## Fences

- **"TO ADD" ONLY.** The plan for this TO creates: 1 Lambda, 1 role, 1 schedule (its own, new), policies
  against the monolith + read-only source grants. It modifies ZERO existing resources. If the plan shows
  a change or destroy on anything that exists, STOP — the design is wrong, not the plan.
- **APPLY IS NOT YOURS.** Author + plan → COO ferries to CTO's gate. Terraform-only, `safe-apply`, layers,
  source map (`infra/aws/lambda/ci/lambda-source-map.json`), deliberate sizing, tag after 0-diff.
- **The mirror role is PROVABLY INCAPABLE of writing its sources** — no PutObject on ANY `opal-data-*`
  source bucket; the fence lives in the ROLE. Deny demonstrated per the corrected C1 AC-4 protocol:
  exact OBJECT-key ARNs on `opal-data-inf` (including `gold/meta/pipeline-complete.json`) and
  `opal-data-cot`, one per invocation, plus the instrument positive control (a role known to hold
  PutObject on inf → allowed) so the deny test is proven able to fail.
- **Nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`** — not the mirror's role, not a test.
- **cot is a separate firm from bd** — one-way fan-in; the mirror READS cot, never the reverse; never
  reference another firm's bucket from a pipeline tree.
- Polling cadence rides each source's OWN pull window (stated per row above) — a poll after a known
  window is not a new cron downstream of a pull; document the chosen times in the TF.

## <compiler_tools_mandate>
Phase 1 (before writing): `comp-blast` on the three source prefixes' existing consumers (read-side
awareness only — you are adding a reader, and the graph should know); `comp-pipescript deployed` n/a
(no gold script). NO source-bucket notification enumeration — retired with the mechanism it served.
Phase 2 (before commit): `comp-iam service <mirror-lambda>` once the boto3 surface exists — necessary,
NOT sufficient (fails GREEN on the new bucket); `.tools/commit-gate.sh` automatic.
Phase 3 (after CTO-gated apply): LISTING-BASED verification of a mirrored object per map row —
ListObjectsV2 key + ETag + Size, 13c tiers for multipart (CTO ruling 20260714T024205Z: head-object is
never the acceptance instrument) — + the live simulate matrix per the corrected deny-leg protocol above.
DESIRED / APPLIED / EXERCISED reported separately; a simulate is APPLIED-layer, not EXERCISED.
</compiler_tools_mandate>

## <cross_domain_coordination>
- `opal-data-inf` — HELD DOMAIN. Read-only; zero config touches under the new-territory rule; the
  parquet-only dates are honest holes by ruling 16. **The dead raw producer is DOOR 5 — if this work
  ever makes restarting it look easy or necessary, that is a REPORT to COO, not a fix.**
- `opal-data-cot` — read-only, one-way; separate firm.
- C6 (DS) — his parsers consume your mirrored bronze via the MONOLITH's own events; arrival is
  post-pull-window BATCH, not per-object trickle (flagged to DS 02:26Z; he confirmed no design change).
- C3 (0.6.2) — schwab lands direct, NOT through this mirror. No schwab row exists; do not add one.
</cross_domain_coordination>

## <acceptance_criteria>
1. Terraform plan quoted: **N to add / 0 to change / 0 to destroy** — the zeros ARE an acceptance
   criterion under the new-territory rule, not a nicety.
2. For each of the three map rows: a source object mirrored to its canonical monolith key, verified
   LISTING-BASED per ruling 13c (ListObjectsV2 key + ETag + Size; tier stated per object; never
   head-object — ruling 20260714T024205Z), denominators printed (rows in map = rows verified = 3).
3. Zero `.parquet` under any monolith bronze path after a full mirror cycle — quoted listing; the
   parquet-only INF dates absent (spot-check one known date, expect NO object).
4. Simulate matrix per the corrected protocol: source-write denies on exact object ARNs (inf incl. the
   sentinel key, cot), monolith-write allow, instrument positive control — each its own invocation,
   `--context-entries` where conditioned. Labeled APPLIED-VERIFIED.
5. Idempotency exercised: immediate re-poll lands 0 new objects, reports skip.
6. Schedule exists, ENABLED, at the stated per-row times (`describe-rule`/scheduler output quoted) — and
   it is a NEW rule; no existing scheduler was touched (plan zeros cover this, state it anyway).
7. Source map updated; tagged after 0-diff. Session log with Compiler Tools section. RAVC close to COO.
</acceptance_criteria>

## RAVC
ACK to COO. Evidence to COO. Apply gates and architecture forks to COO, who ferries to CTO — one path.
Do not adjudicate scope yourself; surface it.
