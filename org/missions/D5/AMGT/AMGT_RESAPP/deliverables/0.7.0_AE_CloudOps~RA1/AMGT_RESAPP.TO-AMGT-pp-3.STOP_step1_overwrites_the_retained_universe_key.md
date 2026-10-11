# AMGT-pp-3 -- STOP before step 1: `universe --refresh` puts to an EXISTING key

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1` (copy to `1.0.0_SA_CTO~DELL1` on the decision) | **Date:** 2026-10-11 ~06:59Z
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-pp-3.rebuild-the-peers-objects-against-the-current-scanner.md`
**GO:** msg 3580 @a1bc4c3b30, acked on read.
**State of the world:** NOTHING WRITTEN, NO LEDGER ENTRY OPENED. Every read below is GET / LIST / HEAD.

## The STOP

BOUNDS 2: "No S3 delete, ever; no overwrite of an existing key." Both halves repeat it ("a same-key put is a STOP").
Step 1, `python -m lib.research.peers.universe --refresh`, writes to ONE address, and that object already exists:

| fact | read |
|---|---|
| address (`universe._resolve_home()`, pin worktree `C:/tmp/pp3-run` HEAD 09d15a9fde) | `s3://opal-data-harvest/amgt/harvest/gold/candidate_universe/date=2026-08-06/candidate_universe.json` |
| why that key | `CURRENT_VINTAGE = "2026-08-06"` is a constant at `universe.py:93`; the key never moves with the scanner asOf |
| object now | EXISTS, 1000578 bytes, LastModified 2026-09-19T01:25:08Z, document-sha256 `934ba4783731f43113302d1da595bc4629edc00afbbed0ad3f1f01863255e911`, VersionId `D.ZdXaKfQXNoHYeZ7.58h0t7peUmVcKB` |
| siblings under `.../candidate_universe/` | 1 object (that one); there is no dated series |
| what `write_pool` does on a hit | `head_object`; sha differs -> `put_object(IfMatch=<ETag>)`, i.e. an OVERWRITE of the same key (crosswalk.py:1583-1598) |

The halves describe the universe write as a NEW dated `universe/v1/<date>.json`. That prefix holds three different objects
(2026-09-15, 2026-09-16, 2026-10-06; the identity union the dry run reads through `crosswalk.load_identity_universe`), and
`--refresh` does not touch it. The signed blast radius ("one `universe/v1/` object, nothing overwritten") therefore does not
describe the act step 1 performs. This seat does not adjudicate which text is right; it stops, as both halves require.

## The pre-act reads the order asked for (all done, nothing acted on)

- **Scanner asOf, six files** (`opal-data-portal-v2` `json/security_scanner/latest/universes/<id>/universe_data.json`):
  sp500, r1000, r1000v, acwx, eafe, eafev all `2026-10-02`. BOUNDS 5 is met.
- **Producer blobs at the pin 09d15a9fde:** engine f8666b5a552a, universe 123622c8d612, crosswalk 3603be4be89a, csc 4707de272d20,
  shared_defect 77bfcec365c5, each equal to the GO's table (5 of 5); the shared tree's HEAD carries the same five blobs.
- **243 prior keys:** `PP3_PRIOR_KEYS_20261011.json` beside this file (243 rows; 234 with a latest object, 9 with none, which is
  the dry run's 8 + 1; latest partitions `2026-09-24T2252Z` and `2026-10-02T1543Z` only).
- **Latest `universe/v1/` key:** `universe/v1/2026-10-06.json` (3 objects).
- **Open-deploy sweep:** 22 worktrees listed, 15 with an `.open_deploys` directory read (289 entries), 7 without one;
  0 entries name `peers/v1` or `universe/v1`.

## Why the engine cannot just run without step 1

`engine.run_batch` loads the candidate universe through `load_candidate_universe`, which reads the pool object above (or its
local mirror). Un-refreshed, that is scanner vintage 2026-08-06, so a `--write-pool` batch would write 243 objects from the OLD
scanner. The refreshed universe has to reach the engine by one of the routes below.

## The three ways through (the issuer's and the CTO's, not mine)

- **A. Authorise the same-key overwrite** of the candidate-universe object, named in an addendum to the pair. The bucket
  returns a VersionId, so the prior bytes stay recoverable by version; but the pair's rollback is "re-publish under a LATER
  partition", which a fixed key cannot take, so the addendum must name the rollback it accepts.
- **B. Do not land the universe at the pool at all.** Set `AMGT_PEER_UNIVERSE_CACHE=<one local file>` for step 1 and for
  steps 2-3. `universe.py:694` and `:815` then skip the pool put (no override-free path), and `cache_path` makes the engine read
  that same file. The only store writes are the 243 NEW `peers/v1/<key>/<write_as_of>.json` objects. Cost: the pool's candidate
  universe stays at the old vintage, so the next scheduled `engine` batch or any reader of the pool object rebuilds from the old
  scanner, and a later run can regress what this act writes.
- **C. Re-cut:** a universe write to a NEW address (a code change to the constant, so a new round), then the same two steps.

This seat recommends **B only if the CTO accepts the stale pool object**, otherwise **A with a named rollback**. It acts on
neither until named.
