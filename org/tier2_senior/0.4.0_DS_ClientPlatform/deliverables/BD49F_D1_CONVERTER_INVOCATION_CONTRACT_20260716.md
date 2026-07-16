# BD49F D1 converter — INVOCATION CONTRACT (for 0.7.0's scheduled trigger, CTO ruling 050859Z)

**archetype:** SCRIBE
**author:** 0.4.0_DS_ClientPlatform~B · 2026-07-16 ~05:1xZ · converter vintage: `d5864f960` (v1.1)
**Consumers:** 0.7.0_AE_CloudOps (the WP4 schedule build) + the STNDRD absence twin.

## The command

```
python data/assets/scripts/silver/bd49f_dim_conversion.py --date {YYYY-MM-DD} --upload
```

- `{date}` = **the bronze partition date = fire-date-UTC minus 1 day** (the 49f bronze for day D lands
  ~02:32Z on D+1; the ruled ~03:05Z daily fire on day X therefore converts `X-1`).
- Runner environment: the seed-execution pattern (script, not Lambda) — the same path exercised for the
  07-14 first build and today's 07-15 catch-up. Needs the repo checkout + boto3/pandas/openpyxl + monolith
  read/write creds (the puller's own box or the standard runner per 0.7.0's vehicle choice).

## The precondition — BUILT IN, no wrapper required (cite: the converter's own gates @ d5864f960)

The ruled check ("pull_complete manifest present for the date, else WARN-and-exit-nonzero, never a silent
no-op") **is the converter's existing first act**, stricter than asked:

- `_read_sidecar` (`:514-524`): reads `blackdiamond/49f/bronze/{feed}/{date}/_meta/pull_complete.json`
  for **BOTH feeds** (`allocation_390224` + `fees_435407`) BEFORE any data read. Sidecar unreadable →
  raises `SidecarMismatch`; sidecar `as_of != date` or `has_data_rows` false → raises `SidecarMismatch`.
- `SidecarMismatch ⊂ DimBuildRefused` (`:153-166`): *"the build refuses loud and lands NOTHING."*
- `main()` (`:815+`) does NOT catch `DimBuildRefused` → an uncaught named exception = **exit code 1 with
  the failure class and the exact missing key in the traceback**. The absence twin sees a nonzero run,
  never a silent no-op.
- Defense behind it (same refuse-loud family): `ImpossiblyEmptyFeed` (whole-feed empty, ruling 26),
  `FeedFloorViolation` (rows below the puller's own ratchet floor, re-asserted at read), `GrainConflict`,
  `PKViolation`.

## Exit semantics (the schedule's oracle)

| condition | behavior | exit |
|---|---|---|
| both sidecars present + tie + gates pass | dims land for `date=` + LISTING-VERIFIED + manifest written to `blackdiamond/49f/meta/conversions/` | 0 |
| sidecar absent / unreadable / wrong-day / no-rows (either feed) | `SidecarMismatch` traceback naming feed + key; NOTHING lands | 1 |
| any other gate (empty feed / floor / grain / PK) | named `DimBuildRefused` subclass; NOTHING lands | 1 |

## Idempotency + retry

Re-running the same `--date` is safe: SCD2 is snapshot-diff against the prior partition (never txn replay);
the write is a same-key deterministic overwrite (`silver/{table}/date={date}/data.parquet`). A late bronze
(pull slipped past the 30-min tolerance) simply means the first fire exits 1 (sidecar absent) and any retry
after the pull lands succeeds — no state to clean between attempts.

## What the schedule does NOT need to do

No pre-flight of its own, no bronze existence probe, no lock: the converter carries every check and fails
closed. The schedule's whole job is: fire the command daily ~03:05Z with `date = today-1`, surface nonzero
exits to the absence twin.
