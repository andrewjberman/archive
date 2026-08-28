# `ETFS_SATELLITES.TO-6-AE` — the satellites registry SCHEDULE, measured

**Seat:** `0.7.0_AE_CloudOps~S` · **Issuer:** `2.0.0_SA_COO~Z` · **Certifier:** `3.0.0_SA_CVO~Z`
**Date:** 2026-08-28T01:5xZ
**TO:** `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ETFS_SATELLITES.TO-6-AE.registry-producer-schedule.md` @`2e020e86b1`
**Build:** @`3f5f8bace5` · **Ledger:** @`b33601b7ca` · **Tag:** `cot-pipeline-v0.7.7`
**Proof instance:** `ETFS_SATELLITES.TO-6-AE_PROOF_OF_SPEC.json` (schema-VALID, 0 errors; negative control confirms the validator can refuse)

---

## STATUS

**AC1 PASS · AC2 PASS · AC4 PASS · AC5 PASS.**
**AC3 WITHHELD — NOT FAILED.** It needs a fire on the schedule's own trigger at 07:00Z.
Certified AC1/AC2/AC4/AC5 by `3.0.0_SA_CVO~Z` @`324330f5f2`, who measured a rung below my census.

    cot-satellites-registry-producer-daily   cron(0 7 * * ? *) UTC   ENABLED
    -> cot-satellites-registry-producer      python3.11, 192 MB / 60 s, State Active
    apply 9 added / 0 changed / 0 destroyed · re-plan "No changes."

## 1. THE CRON IS DERIVED, NOT CHOSEN

    DENOMINATOR   38 roster objects, 38 distinct partition dates
    GAPS          0 -- DENSE OVER CALENDAR DAYS
    WEEKENDS      10 of 10 weekend days in range PRESENT
    LANDING       06:00:43-44Z every day (cot-rebalancer-runner-daily, cron(0 6) UTC)
    => cron(0 7) UTC: 59 min after the measured landing, ~6.5h before the 13:30Z serving floor.

⭐ **That measurement did more than pick a number — it defused a precedent I was about to obey.**
The nearest sibling handler says *"T-1 logic lives in the producer, never in the cron, never
wall-clock."* Its stated ground is **T-1 logic**, and this input has none: the partition set is dense
over calendar days and `as_of` is SAME-DAY. **A precedent quoted past its own stated ground is how a
rule becomes cargo**, and the issuer ruled option (A) on the *other* half — that two carriers of one
fact diverge — rather than on the sibling's sentence.

⚠ **The margin's one moving part:** it holds only while the upstream stays a UTC cron. If
`cot-rebalancer-runner-daily` is ever re-anchored to ET, this cron must move with it.

## 2. WHY AN EventBridge RULE AND NOT THIS STACK'S OWN ET-SCHEDULER PATTERN

`schedule-et.tf` uses `aws_scheduler_schedule` with `America/New_York` because **its anchor is MARKET
CLOSE**, where a UTC cron drifts an hour at DST. That reasoning is correct there and **inverts here**:
this anchor is a UTC-cron upstream, so a UTC cron holds a CONSTANT margin and the ET pattern would
have *introduced* the drift it exists to remove.

>> **The instrument follows what the schedule is ANCHORED TO, not what the neighbouring resources
>> happen to use.**

## 3. THE PACKAGING HAZARD — the reason this build is not a copy of its sibling

    data/assets/scripts/gold/satellites_weights.py:54   _REPO_ROOT = Path(__file__).resolve().parents[4]
    :59                                                 from lib.trading_calendar import ...

`parents[4]` is **repo-layout arithmetic**. The sibling builder flattens every member at the zip root,
which breaks it two ways by path depth:

    /var/task/satellites_weights.py         parents[4] -> IndexError (only 3 parents exist)
    <deep path>/flat/satellites_weights.py  parents[4] -> unrelated dir -> ModuleNotFoundError
    /var/task/data/assets/scripts/gold/...  parents[4] -> /var/task   <- CORRECT, this layout

⛔ **A flat package builds clean, uploads clean, applies clean and re-plans 0-diff — none of those
opens the zip. It dies at IMPORT, before one producer line runs.**

**Exercised with a negative control rather than asserted:** mirrored imports and resolves
`opal-data-cot` / `platinum/satellites/registry.json`; flat FAILS. The control fired, so "it imported"
is a result rather than a tautology. ⚠ The executed control produced the **ModuleNotFoundError**
branch; the `/var/task` IndexError is shown by arithmetic and was **not run** — stated separately
because conflating them would make a deep-path test read as a clean bill of health.

**Determinism:** two builds from pin `3f5f8bace5` are byte-identical (`bfea1618...`).

## 4. WHAT ONLY AN IN-SITU RUN COULD SHOW

A **DRY-RUN** invocation of the deployed Lambda (writes nothing, does not touch the served key, does
not muddy the AC3 discriminator) confirmed the layout imports under `/var/task` and that the producer
resolved `as_of=2026-08-28 (resolved today-UTC)` **in the deployed bytes**. 96 MB used of 192.

It also returned, for a partition genuinely absent at 01:39Z:

    BLOCKED: no roster partition at .../rebalancer_models/2026-08-28/page_000.json (S3 said AccessDenied)

⛔ **S3 returns 403 AccessDenied rather than 404 NoSuchKey for a missing object when the caller has no
`s3:ListBucket`.** So **"upstream is late" and "my read grant is broken" are byte-identical at this
producer's error surface.** Benign today — established, not assumed: `simulate-principal-policy`
returns `allowed` on both read prefixes and the exact write key, with **three negative controls
returning `implicitDeny`**, one `--resource-arns` per call so the multi-ARN false-deny mode could not
silently disarm them.

⭐ **This is the same shape `TO-5-DS` AC3 records for the SERVING layer** — where an absent artifact and
a forbidden read are one status, the reason the edge synthesis was removed @`24a8435642`. It has
reappeared one rung up, on the producer's READ side, **and it is a cost of my own no-`ListBucket`
design, which the issuer had ratified.** Surfaced against my own interest rather than quietly fixed,
because the absence was explicitly ratified; filed by `3.0.0_SA_CVO~Z` as `ETFS_POSITIONING-Z-S12`,
class OBSERVATION, standing INERT.

⛔ **Scope note preserved:** the remedy (a prefix-conditioned `ListBucket`) **does NOT implement option
(C)**. (C) was a newest-partition RESOLUTION strategy; this only changes which error code a failure
carries. Rejecting (C) does not entail rejecting this.

## 5. ⛔ AC3 — WITHHELD, AND MY FIRST INSTRUMENT FOR IT WAS UNSOUND

**No `FAIL` row is filed.** An un-fired scheduled criterion is not a failed one, the status enum has no
value for "not yet measurable", and 18 `FAIL` rows already exist across 1,258 acceptance rows
estate-wide with at least one a self-declared false failure that nothing downstream can distinguish.
Withholding was ratified by `2.0.0_SA_COO~Z` (11579 s.5) and `3.0.0_SA_CVO~Z`.

**AND THE INSTRUMENT I FIRST ARMED WAS WRONG.** I armed a watch on the artifact's VersionId and
reported it as armed. **It fired within 90 seconds, on another seat's write:**

    2026-08-28T01:09:51Z  2182 B  D1iVAJ4LJOqx1BDPMLmcEXLOUJvcP7wb  the ad-hoc QA write
    2026-08-28T01:38:46Z  2196 B  xLcuAW7VMbGyF.0kpt2LQ9Wb24WVnQaS  NOT MINE  <- current baseline

My function's own log group carries **exactly one** invocation (01:39:10Z, the dry-run) and it wrote
nothing.

>> **A VersionId delta answers "did the key change", NOT "did MY SCHEDULE fire" — and any seat's
>> ad-hoc run satisfies it.** The TO requires evidence distinguishing a scheduled fire from a manual
>> one. **It was caught only because the timestamp was impossible (5h21m before the cron); with a
>> nearer cron, another seat's write would have been accepted as this TO's acceptance evidence.**

**THE SOUND ORACLE, armed instead:** this function's OWN CloudWatch log group, watched for its
`OK: wrote s3://...` line. Emitted by the function under test only on a completed write; no other
seat's producer run can produce it.

⚠ **And the baseline is perishable in two ways, not one.** `get-bucket-versioning` reads `Enabled`, but
`get-bucket-lifecycle-configuration` carries `expire-noncurrent-versions-14d` over `Prefix: ""` — so
the superseded version dies in 14 days. It also perished in **29 minutes** from a concurrent writer.
Both are why the baseline is banked in the ledger as a durable artifact.

⚠ The TO's named discriminator **does not exist**: the artifact carries no `provenance` field
(measured — `schema_version, as_of, source, claim, books`). AC3 therefore rests on the invocation
record plus the version delta, which is the **stronger** instrument: a provenance field is written by
the system under test.

## 6. WHAT IS NOT MINE, AND WAS NOT TOUCHED

The producer and the QA write (`0.4.0_DS_ClientPlatform~L`, `TO-5-DS`) · the `POSN_TENANCY.TO-4-AE`
apply hold (lifted @`0e8aa52d20` and re-seated to `0.7.0_AE_CloudOps~Y` — a different project) · the
`ETFS_SATELLITES` PROD promote (DT lane) · `D1_CATVIEWS` D1-i-2 · the `etfs-positioning` apply
(declined on Rule 27; the recommendation was retracted and the issuer affirmed the refusal rather than
assigning it here).

⛔ **AND THIS TO DOES NOT MAKE THE PAGE WORK.** `Z-S11` records that no fetch path exists. A correctly
scheduled producer writing a correct artifact to the correct key still does not reach the view until
the route is DEPLOYED (`POSN_TENANCY.TO-4-AE`, `~Y`) and the consumer seam lands (`TO-8-DE`).

## 7. `cell_status` — from OBSERVED states only

⚠ In the `.md`, not the proof instance: `PROOF_OF_SPEC.schema.json` is `additionalProperties:false`.

| cell | status | basis |
|---|---|---|
| `SAT-a-4` | **PARTIALLY OBSERVED** | The trigger half is APPLIED and verified on the live plane. The EXERCISED half (AC3) is unobserved until 07:00Z, and the SERVING half of the same cell belongs to `TO-7-AE`/`TO-4-AE` and is NOT deployed. |
| `SAT-b-2` | **OBSERVED** | The scheduled path preserves publish-the-empty: no branch on member count, no delete, measured in the deployed bytes. |
