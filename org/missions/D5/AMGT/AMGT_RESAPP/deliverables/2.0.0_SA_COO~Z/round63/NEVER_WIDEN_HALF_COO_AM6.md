# AMGT_RESAPP round 63 -- `AMGT-am-6` LEG 1 never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~16:4xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names (`4197279e67`, or a descendant whose CONTENT-DIFF
equals the list below). Build and upload ONE artifact, then ONE code-only `safe-apply`; `memory_size` stays 10240. Executor
`0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-am-6.the-code-redeploy-and-memory.md` section 6 (AMENDMENT 1, leg 1);
decomposition s.71. Leg 2 (am-1's code, cold BA under 5 s, the memory step-down) is a separate act under its own pair.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `bZBmEtRrAagqpRJCa4JLvyZmNaM0EvkOp6K6Gcm9kW4=` (LastModified 2026-10-02T11:26:56Z) |
| function MemorySize | 10240 |
| artifact S3 VersionId | `iDuPquXbC0ZpmHbnZREUzQd7CVYh15vi` (LastModified 2026-10-02T11:25:08Z, 41,118,711 B) |

## WRITERS OF THE PROPERTY: 1 seat, 1 path

`build-and-upload-scoped-amgt.sh` plus a code-only `safe-apply`, by AMGT_RESAPP. No other open deploy entry names this function at
signing (`.open_deploys/`, 33 entries, 0 AMGT). AMGT_CORPUS's open act (`amgt-corpus-r32-ah3`) writes `field_map.json`, which this
artifact does not package (0 of 353 members). AMGT_HARVST's rebuild #5 writes gold, not this function.

## THE FILE LIST (`--build-only` at `4197279e67`, rc=0: VERIFY missing [], cold-start FATAL [], request-time break [], isolated 3 of 3)

`CONTENT-DIFF SUMMARY: files 353, IDENTICAL 343, CHANGED 7, ADDED 3, REMOVED 0` against `bZBmEtRr...`:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | am-3, am-4, am-5 | (1) `/security/{key}/overlay`: the `breakout_price` row gains `places_moved` and `places_moved_reason` from the same join the rankings rows use; a name with no row serves top-level `places_moved: null` plus a plain `places_moved_reason`. (2) `/security/{key}/peers`: every absent-column entry gains `reason_class`. (3) The per-security arm (`overlay`, `thesis`, `peers`, `coverage`, `print`, `ledger`, `versions`, `compare`) answers 404 for an UNRESOLVED key outside the covered universe; a known key is unchanged; a failed covered-universe listing for an UNRESOLVED key answers 502. |
| `lib/research/api/monthly_chatter.py` | CHANGED | am-3, am-5 | `collected/chatter` rows gain `ticker`, `classification`, `places_moved`. The gold reads decode only the served columns; same served bytes (test: projected == full). |
| `lib/research/coverage/pool_reader.py` | CHANGED | am-5 | `_gold_latest_snapshot_rows` takes `columns=` (default unchanged for every other caller). |
| `lib/research/peers/csc_plain_reasons.py` | ADDED | ak-3 A1, am-4 | the plain absent-column reasons (moved out of `scoped_amgt`, ak-3 AMENDMENT 1) and am-4's one reason-class map. |
| `lib/research/posture/__init__.py`, `posture/fit.py` | ADDED | ak-5 | imported by `csc_plain_reasons` (top level); no route of its own. |
| `lib/research/harvest/publication_gold.py` | CHANGED | HARVST aj-7 | NONE through this function: aj-7 changed `GOLD_MENTION_SCHEMA` and `mention_rows` (the producer); the route calls `_latest_gold_snapshot_rows_cached` and `_latest_articles_for_keys`, unchanged. Gold itself moves only at HARVST's rebuild #5. |
| `lib/research/provenance/validate.py`, `render_print.py` | CHANGED | CORPUS ah-1 | NONE through this function: the route imports only `load_corrected_price_overlay` and `apply_corrected_price_overlay`, which call neither `derive_unit_status`/`derive_sign_status` nor `render_figure_line`. |
| `infra/logic/registry/reporting_policies.json` | CHANGED | IRPT DB-b-2 | NONE expected: a data member the naming registry packs; DB-b-2 added its own policy rows. The local suite (589 passed) runs on these bytes. |

Any other changed, added or removed file at build time is a STOP.

## READERS

Security Analysis (overlay, peers, thesis, print) and the Lead Panel (`collected/chatter`, rankings), DEV and PROD. Every served change is
an added key except the unknown-key status; pages request covered names only, so the 404 reaches no page read.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `iDuPquXbC0ZpmHbnZREUzQd7CVYh15vi` |
| code-only `safe-apply` | the function's code (source hash) only; `memory_size` stays 10240 | a code-only `safe-apply` with that VersionId, restoring `bZBmEtRr...` |

## EXPECTED OUTCOME -- both branches, read at `4197279e67` on the shared tree

- **The code serves as graded locally:** `r63_served.py --where deployed` reads c3 YES (95 of 95, 95 of 95, VLO overlay 13 == ranking
  13, ROG_SW_Equity a reason), c4 YES (BA and VLO 12 of 12 classed), c5 YES (fabricated key 404, BA 200). Base at signing: c3 0 of 95,
  c4 0 of 12, c5 200. c1 is NOT graded on this leg: BA 2026-09-08 keeps today's deadline behavior.
- **Failure branch:** any of c3, c4, c5 not YES, or a non-200 on a covered key's overlay, thesis or peers -> ROLLBACK per the table.

## WHAT THIS HALF DOES NOT COVER

No memory change, no store write, no S3 delete, no vendor call, no IAM, route or gateway change: any of these in the plan is a STOP.
