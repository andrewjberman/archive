# AMGT_CORPUS round 2 -- never-widen pair, the CRPS-d-5 induction RE-FIRE (one `add_security --batch` call, one pool put)

Two halves, one file. The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by
`1.0.0_SA_CTO~Z` (R-49 s.3, R-51), appended under its own heading. The re-fire is NOT run until both halves are
signed here at these bytes and the d-5 amendment-3 cell has drained VALID into CLOUD.

## COO HALF -- `2.0.0_SA_COO~X`

**Sources:** decomposition v2.0 s.5 duty 1 / s.9 hold; row `AMGT_CORPUS-Z-S13` (this seat's 08:02Z incident, ARMED);
CTO R-37 (the pair's shape, now inverted by R-51), R-38/R-40 (the four preconditions), R-49 (3 and 4 PASS; count-first),
R-51 (all four hold; the halves name ONE conditional put and the `--batch` call shape); the drained builder
`lib/research/identity/add_security.py` @`a125f8be8b` (on CLOUD via `8c75f4f90d`, byte-identical per R-51); the d-5
order with ISSUER AMENDMENT 3 @`e1014a7eb6`. Measured read-only by the issuer, 2026-09-24 10:3xZ-10:4xZ.

### THE ACT

ONE run, by this seat on this terminal (READ_HERE s.2 sign-in state checked first, `bloomberg_health` up):

    OPAL_INDUCTION_FIRE=1 python -m lib.research.corpus.induction_run --fire --as-of 2026-09-24

which makes EXACTLY ONE call `add_security.main(["--batch", <induction_batch_2026-09-24.json>, "--as-of",
"2026-09-24", "--write-pool"])` (amendment 3; the CALL SHAPE is named because the one-put property is call-shape-bound:
twenty per-name `--write-pool` calls would still put twenty times -- R-51). The batch file is the list of every
effectively-EVIDENCED backlog row, `{"folder", "bloomberg"}` each, in sorted order; the dry run on CLOUD reads 20 of 60.

### BLAST RADIUS -- the act's OWN write set, counted one call deeper than the caller (Z-S192's lesson)

1. **ONE conditional put on ONE key: `s3://opal-data-harvest/crosswalk/v1/2026-09-24.json`** -- `add_security._mint_pool`
   (`:373-397`) -> `crosswalk.write_pool` (`:1087-1150`): `head_object`, then `put_object` with `IfMatch <current ETag>`
   ONLY when the stored `document-sha256` differs from the payload's, then a `head_object` read-back that RAISES on a
   digest or length mismatch. Called once per run, after every request (`main` `:605-608`: `if args.write_pool and
   landed:`), so `pool_puts` is 1 or 0, never N.
2. **Up to 20 write-once raw landings, NEW keys only:** `add_security._land_raw` (`:150-167`) -> `hbloom.bronze_write`
   -> `store.bronze_put` (`:216-255`): `put_object ... IfNoneMatch="*"` at
   `s3://opal-data-harvest/bloomberg/harvest/bronze/identity/security_key=<KEY>/<UTC stamp>.json`, one per MEASURED
   response, a fresh stamp each, so an existing object is never rewritten (same sha on PreconditionFailed is a no-op;
   a different sha raises). Additive only; no served reader selects these.
3. **One repo file, `lib/research/identity/registrations.json`** (rows persisted per request BEFORE the put, `main`
   `:599-603`), committed by this seat after the fire or reverted (the 08:02Z misfire's diff is kept as the precedent).
4. **This seat's deliverables:** the read-back `induction_run_2026-09-24_fire.json` and the fire log.

NOT in the write set: any other dated key under `crosswalk/v1/` (the key is `<as_of>.json` and `--write-pool` refuses a
non-today as-of); `universe/v1/`; any filings/management/peers/posture/social key; any delete.

### WRITER CENSUS -- N = 2 writers of the named key, PRINTED

The property signed is the served crosswalk pool key. `comp-find 'CROSSWALK_PREFIX' lib` (denominator: 12 hits across
312 files scanned under `lib/`, corpus `all`): the two DEF lines are the constant itself (`crosswalk.py:69`,
`scores/run_scores.py:69`, a reader); of the 10 SURFACED hits exactly TWO compose a key that is then PUT:
- `lib/research/identity/crosswalk.py:1184-1185` -- `crosswalk.main --write-pool` (the Peers producer's route; the
  03:32Z signed 194-key object was written here by `2.0.0_SA_COO~Z`);
- `lib/research/identity/add_security.py:380` -- `_mint_pool`, THIS ACT.
The other eight are readers (`_read_pool_latest` `:952-969`, `management/batch.py:94`, `induction_request.py:347`,
`run_scores.py:84-88`, an exception message). `build_universe.py:918` writes `UNIVERSE_PREFIX`, a different key family.
`comp-find 'write_pool' lib` (120 hits, 312 files): every other `crosswalk.write_pool` caller composes a filings,
management, peers, posture, social or universe key, never `CROSSWALK_PREFIX`. **Unscoped repo-wide sweep of `crosswalk/v1`** (`comp-find`, corpus `all`: 1,009 hits across 72,661 files scanned;
591,165 ephemeral-floor, 2 unreadable and 3,318 binary NOT searched; bands HEAD 100 / DEF 8 / SURFACED 70 / CONFIG 433 /
TEST 17 / DOC 381), the DEF and SURFACED bands read in full (78 lines): outside `lib/` every hit is a READER or a record --
`integrations/bloomberg/research/management_posture_batch.py:86` (`_latest_key`, reads; its `write_pool` at `:256` is
`management_enrich.write_pool_object`, a management key), `build_unit_map.py:464` (lists), `model_block_pull.py:731`
(lists), `.runtime/` bundle copies of `crosswalk.py`/`scoped_amgt.py` (the deployed READ adapter), two Terraform grants
naming the prefix whose action limbs are `s3:GetObject` + `s3:ListBucket` only (`chatter-axis-schedule.tf:130,136`,
`scoped-amgt-api.tf:219,229`), portal harness fixtures, this seat's probe, logs and messages. HEAD/CONFIG/TEST/DOC bands
not read line by line: HEAD is file-NAME matches (bundle copies of the same modules), CONFIG/TEST/DOC are audit logs,
tests and prose by the tool's own banding. **N = 2 holds unscoped.** By branch (a producer on a branch is a writer the
trunk cannot see): `add_security.py` is byte-identical between `a125f8be8b` and HEAD (R-51), and no open worker branch
of this project touches `lib/research/identity/` (d-5's `<paths>` exclude it).
**Both writers read ONE builder (`crosswalk.build_crosswalk`) with the universe input passed** (R-49 precondition 4), so
the two writers agree on the document's population; only the registrations input differs, and this act's registrations
are a superset of the Peers producer's.

### BEFORE-STATE -- the EXACT key, measured (probe-1, 10:44:27Z; re-measured immediately before the fire)

`versions 22, delete markers 0, latest VersionId aTOpDZTTPlIzLLoeTFumB8KHmv6A0txG (08:22:33Z, the verified restore),
size 523207, ETag "2c0ff894a1b0a3ac4dd20ca45811b76c", sha256 9bd953b9c06f7382..., document-sha256 metadata equal,
denominators records 254 MEASURED 194 UNRESOLVED 60 registered 7 universe_registered 158`. Raw identity partitions: 4.
Instrument: `deliverables/2.0.0_SA_COO~X/refire_versions_probe.py`, output under `evidence/refire_probe1_*.json`.
The reader's rule (`crosswalk._read_pool_latest` `:969`, `sorted(keys)[-1]`) selects THIS key today, so a new version of
it IS a served move and DELTA is not 0: hence this pair.

### EXPECTED OUTCOME -- read from the producer's own rule, EVERY branch

- **landed >= 1 (the expected branch):** exactly ONE new version of the key (23 versions, the new one latest, IfMatch on
  the ETag above); the document is the SAME builder over coverage + universe + (8 + landed) registration rows, so
  `MEASURED = 194 + R` where R is the count of `MEASURED:` rows landed (a `bloomberg security error` lands an UNRESOLVED
  row: records grow, MEASURED does not), `registered = 7 + landed`, `universe_registered` unchanged at 158, and every
  one of the 194 keys present before is present after (a superset; the 0-of-20 count-first read shows none of the 20
  collides, so no request is refused for a universe key). Served readers see 194 + R MEASURED after ONE atomic swap,
  never a partial object.
- **landed = 0 (every request already-registered / refused / unresolved-without-row):** `pool_puts 0`, NO put, version
  count stays 22, the key byte-identical; only registrations.json may change.
- **the vendor is down or the session is not signed in:** `bloomberg_health` is read first; a failure mid-batch raises
  out of `main` BEFORE `_mint_pool` (the put is after the loop), so the key is untouched and registrations.json holds the
  rows persisted so far -- this seat reverts or commits that file and records which.
- **write_pool's read-back mismatch:** it RAISES after the put; the new version exists and is the served one; rollback
  below applies.

### PER-KEY ROLLBACK

`copy_object` from VersionId `aTOpDZTTPlIzLLoeTFumB8KHmv6A0txG` onto the same key (the exact route `2.0.0_SA_COO~Z` used
at 08:22Z, verified 3 of 3 legs), then read back size 523207 / sha256 9bd953b9. No version is deleted. Raw bronze
landings are write-once and additive; their rollback is an S3 delete, which needs Andrew's word and is NOT pre-authorised
here (they harm nothing: no reader selects them). Rollback trigger: more than one new version of the key after the
run; any write outside the set above; `MEASURED` after < 194; any of the 194 prior keys absent after. On a trigger this
seat rolls back in-session, files a row citing Z-S13, and reports.

### THE DISCRIMINATOR (this seat's, R-49/R-51)

`refire_versions_probe.py` before and after: `versions` moves 22 -> 23 exactly (or stays 22 with `pool_puts 0`),
`latest_version_id` changes exactly once, `MEASURED` = 194 + R with R read from the fire read-back's `registered`, and
the `BATCH:` line's `pool_puts` is 1. Positive control for the probe: it reports the 08:02Z misfire's 20 versions in
its list (22 total), so it can see a multi-put run.

### NOT COVERED

- any second `--fire`, any per-name `--write-pool` call, any `crosswalk.main --write-pool` run by this seat;
- a Model-block pull or any other vendor surface (C-NO-VENDOR-CALL v0.5's one exception is this call);
- the re-ingest and the production sequence (the drain duties that follow; no pool write in them);
- any hand-typed identifier: every request's `bloomberg` comes from the request row's report evidence;
- deleting any object; any write under `universe/v1/`.

**Signature (COO):** signed `2.0.0_SA_COO~X`, 2026-09-24, at the commit of this file (its hash is the vintage). Bound to
the before-state above; a different `latest_version_id` at fire time re-opens this half.

## CTO HALF -- `1.0.0_SA_CTO~Z`

SIGNED in that seat's own folder (owned-paths refused this path to it, correctly):
`org/tier1_exec/1.0.0_SA_CTO/deliverables/AMGT_COMPLETION_20260923/NEVERWIDEN_D5_REFIRE_CTO_HALF.md` @`9a6472e58f`,
bound to this half at `4bbd43777c` and to `add_security.py` @`a125f8be8b` == HEAD (CTO msg 25431). It adds the one
measurement this half asserted without one: zero production readers of `bronze/identity` (5 hits of 8,142 code files,
all the writer's own constant, tests, or the probe). The pair is COMPLETE at that commit.
