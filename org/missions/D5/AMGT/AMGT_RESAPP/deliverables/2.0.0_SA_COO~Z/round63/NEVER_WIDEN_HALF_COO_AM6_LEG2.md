# AMGT_RESAPP round 63 -- `AMGT-am-6` LEG 2 never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~17:5xZ

**The acts, in order, under ONE NEVER-2 entry:** executor `0.7.0_AE_CloudOps~A`; order
`task-orders/AMGT_RESAPP.TO-AMGT-am-6.the-code-redeploy-and-memory.md` sections 1 and 6 (AMENDMENT 1, leg 2); decomposition s.71.
- **(A)** Redeploy `opal-amgt-scoped-api` at the build commit the GO names (`6436cc930a`, or a descendant whose CONTENT-DIFF equals the
  list below). Build and upload ONE artifact, then ONE code-only `safe-apply`.
- **(B)** Step `memory_size` DOWN from 10240. Each step is ONE `safe-apply` touching only `memory_size` in
  `infra/aws/terraform/harvest/scoped-amgt-api.tf`, followed by AC1 (c1 deployed). First 1769; if AC1 misses, then 3538; if it misses
  again, back to 10240. Report each step's three cold durations.
**Begins only after leg 1 is graded** (its V1 leg closed).

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `JVMY1ZDAZifF2LycbC0hkjwD/be+sHjWkRBeYFQ354Y=` (leg 1, LastModified 2026-10-02T17:40:56Z, CodeSize 41,132,193 B) |
| function MemorySize | 10240 |
| artifact S3 VersionId | `Eb6lQYKJX.4eL8K.Qq0LHCRJs5AzCfk2` (LastModified 2026-10-02T17:31:32Z, 41,132,193 B) |

## WRITERS OF THE PROPERTY: 1 seat, 2 paths

Code: `build-and-upload-scoped-amgt.sh` plus a code-only `safe-apply`. Memory: `memory_size` in `scoped-amgt-api.tf` via `safe-apply`.
Both by AMGT_RESAPP. Leg 1's entry is this function's only open entry at signing.

## THE FILE LIST (`--build-only` of the am-1 tree `eda65ad519`, which `6436cc930a` drains; rc=0: VERIFY missing [], cold-start FATAL [], request-time break [], isolated 3 of 3)

`CONTENT-DIFF SUMMARY: files 353, IDENTICAL 352, CHANGED 1, ADDED 0, REMOVED 0` against `JVMY1ZDA...`:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | am-1 | `/security/{key}/timeline/day/{date}` only. `headline` and `published_precision` come from the GOLD mention row's own `title` and `published_precision` (HARVST rebuild #5 @ee94bac02d), not from a request-time silver read. A null title gives `headline` null. The 18 s deadline and the `headline_reason` field are removed. No other route changes. |

Package size: 253,667,918 B unzipped with the layer, against the 262,144,000 B ceiling (96.8%, 8,476,082 B spare). Any other changed file at
build time is a STOP.

## READERS

The Security Analysis timeline's day dissection (DEV and PROD). The page already tolerates a null headline and ignores an absent
`headline_reason`.

## THE BLAST RADIUS -- what the acts MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `Eb6lQYKJX.4eL8K.Qq0LHCRJs5AzCfk2` |
| code-only `safe-apply` | the function's code (source hash) only | a code-only `safe-apply` with that VersionId, restoring `JVMY1ZDA...` |
| each memory step | `memory_size` only (every route's CPU share scales with it) | `memory_size` back to 10240 |

## EXPECTED OUTCOME -- both branches, read from the code at `6436cc930a`

- **Headlines.** Measured by the issuer at ~17:4xZ, deployed (silver) against the am-1 code (gold), same days: 13 of 13 headlines equal
  over BA 2026-09-08 (6), 2026-09-30 (6) and 2026-10-01 (1); VLO and ASML_NA 2026-09-30 serve 0 articles both ways. HARVST aj-7
  built 713 rows over 5 securities with 0 title mismatches against silver, and aj-8 re-derived 149 barrons titles that silver held as
  dicts, which now serve as strings (757b50b6ad). Both are SAMPLES: the full 23,691-row gold population was not compared to silver, so
  a headline whose gold title differs from its silver text is a reachable branch, and it serves the gold text.
- **Latency.** The route no longer reads silver. AC1 (c1 deployed) expects 3 of 3 COLD BA 2026-09-08 invokes, each under 5,000 ms, with
  every headline and no `headline_reason`. Base at signing: the leg-1 code takes the deadline path cold, 15-19 s at 10240.
- **Memory.** 1769 MB is the setting every other route served at until 10:55Z today. If c1 misses at 1769 and again at 3538, memory
  goes back to 10240 and the code stays.
- **Failure branch:** c1 misses at 10240 after the code act, or any non-200 on a covered key's timeline/overlay/thesis/peers -> code
  ROLLBACK per the table and memory back to 10240.

## WHAT THIS HALF DOES NOT COVER

No store write, no S3 delete, no vendor call, no IAM, route or gateway change, no timeout change: any of these in a plan is a STOP.
