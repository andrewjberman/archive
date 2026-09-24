# AMGT_CORPUS round 3 -- never-widen pair, the 40-name induction FIRE (one `add_security --batch` call, one pool put)

Two halves, one file. The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by
`1.0.0_SA_CTO~Z` (the signer of round 2's pair, same key, same act class), appended under its own heading. The fire is
NOT run until both halves are signed here at these bytes.

## COO HALF -- `2.0.0_SA_COO~X`

**Sources:** decomposition v3.0 s.5 duty 1, s.8 (R-16 V2: one call per name for the 60, 20 spent, these 40 remaining), s.9
hold; Andrew's word on the 40 PICKS (record @`090ffea`, the read-only census that produced the table -- NOT a vendor word, it ends "no vendor call, no store write"; corrected 21:0xZ on `1.0.0_SA_CTO~Z`'s catch); the evidence table
`deliverables/2.0.0_SA_COO~X/UNRESOLVED40_CALLS_20260924.json` (40 rows); cell e-1 drained VALID at `21e624a003`; the
builder change of `2.0.0_SA_COO~Z` @`9ec1226a01` (one record per folder after an attach); round 2's pair
`NEVER_WIDEN_ROUND2_D5_REFIRE_HALVES.md` (the write-set trace one call deeper, which this act re-uses unchanged because
`add_security.py`'s put path is unchanged since it). Measured read-only by the issuer 2026-09-24 20:2xZ-20:3xZ.

### THE ACT

ONE run, by this seat on this terminal, after READ_HERE s.2 and `bloomberg_health` read up:

    OPAL_INDUCTION_FIRE=1 python -m lib.research.corpus.induction_run --fire --as-of 2026-09-24 \
        --evidence org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/UNRESOLVED40_CALLS_20260924.json

which makes EXACTLY ONE call `add_security.main(["--batch", <induction_batch_2026-09-24.json>, "--as-of", "2026-09-24",
"--write-pool"])` (`induction_run.py:468`). The batch is the 40 table rows, `{"folder", "bloomberg"}` each; the dry run on
CLOUD reads `population 41 evidenced 40 called 40` (the 41st row is AMD, outside the table, not called). Bloomberg: at most
40 reference calls, one per name, never repeated -- the remaining 40 of R-16 V2's 60.

**VENDOR AUTHORITY -- the record, corrected (21:0xZ).** Andrew-direct R-21 @`b390c36444` (~03:2xZ, verbatim): *"all recs
approved, and you have all the egress you want for vendors. Only thing I'd note is that the pull should be
deterministic/scripted in nature like the existing pull"* -- BROAD on authority (all vendors), NARROW on mechanism (a
scripted, re-runnable producer, never an agent turn). This act is that mechanism: `induction_run --fire` -> ONE
`add_security --batch`, re-runnable from git, read-back to a file. `1.0.0_SA_CTO~Z` named "R-16 V2, R-21" as this
induction's vendor word at 03:30Z (msg to `2.0.0_SA_COO~Z`, `...033051Z_..._CTO_NEVER-WIDEN_HALF_SIGNED__429efcdf30_.md:59`),
and round 2's 20-name fire ran on that citation under a CTO-signed pair. Whether R-21 is the per-use word for THIS
run is the CTO's to rule on its own record; this half does not run the fire until the CTO half releases the limb.

### BLAST RADIUS -- what the act MAY touch, and the rollback for each

1. **ONE conditional put on ONE key: `s3://opal-data-harvest/crosswalk/v1/2026-09-24.json`** (`add_security._mint_pool`
   -> `crosswalk.write_pool`: head, `put_object IfMatch <ETag>` only when the document digest differs, read-back that
   raises on a mismatch). `pool_puts` is 1 or 0, never N. **Rollback:** copy VersionId `BN_TiAyAX_EwRm_nP.PMymkiUnFBMA1N`
   back as the new latest (versioned bucket, no delete), as the 08:22Z restore did.
2. **Up to 40 write-once raw landings, NEW keys only:** `bloomberg/harvest/bronze/identity/security_key=<KEY>/<UTC>.json`,
   `IfNoneMatch="*"`. Additive; no served reader selects them. **Rollback:** none needed (unreferenced once item 1 is rolled back).
3. **One repo file, `lib/research/identity/registrations.json`** (rows persisted per request before the put). Committed
   by this seat after the fire, or reverted with item 1.
4. **This seat's deliverables:** the fire read-back and log; `induction_batch_2026-09-24.json` rewritten with the same 40.

NOT in the write set: any other dated key under `crosswalk/v1/`; `universe/v1/`; any dossier, backlog or filings key
(those move only in the production sequence that follows, under its own producers); any delete.

### WRITER CENSUS -- N = 2 writers of the named key, PRINTED

`comp-find 'CROSSWALK_PREFIX' lib --band SURFACED --all` (12 hits across 322 files, corpus `all`; DEF 2, SURFACED 10), read
in full: two compose a key that is then PUT -- `crosswalk.py:1269` (`crosswalk.main --write-pool`, the Peers producer's
route) and `add_security.py:380` (`_mint_pool`, THIS ACT). The other eight are readers or messages
(`induction_request.py:347`, `crosswalk.py:74/1037/1046/1052`, `management/batch.py:94`, `run_scores.py:84/88`). Same N
as round 2's unscoped census. Both writers call ONE builder, `crosswalk.build_crosswalk`, so the ENRICH/supersede rules
of @`9ec1226a01` bind either writer. By branch: no open worker branch of this project touches `lib/research/identity/`
(both round-3 worktrees are drained).

### BEFORE-STATE -- the EXACT key, measured 20:35:33Z (re-measured immediately before the fire)

`versions 24, delete markers 0, latest VersionId BN_TiAyAX_EwRm_nP.PMymkiUnFBMA1N (11:59:04Z), size 560881, ETag
"7f3cb3c15c8fb86ab13cf002adcc1bcf", sha256 572edb49f9d7aa6f... = document-sha256 metadata, denominators records 254
MEASURED 214 UNRESOLVED 40 registered 27 universe_registered 158`; raw identity objects 24. Instrument:
`refire_versions_probe.py` (read-only). The reader's rule (`_read_pool_latest`, newest key) selects THIS key, so a new
version IS a served move: hence this pair.

### EXPECTED OUTCOME -- read from the builder's own rule, BOTH branches covered

The builder's rule was exercised in memory through `add_security._build_document` with each request's mode decided by
`add_security._collision_mode` (`preflight_40_fire.py`, re-run by this seat at `9ec1226a01` on a clean identity tree):
modes APPEND 21 / ENRICH 19; AFTER `records 235 MEASURED 235 UNRESOLVED 0 registered 44 resolved_folders 40 enriched 20`,
multi-claimed forms 0, folders with two records 0, 214 of 214 prior keys present, 21 new keys = 21 appended.
`records` FALLS 254 -> 235 because each of the 19 ENRICH attaches its folder to an existing no-folder MEASURED record and
retires that folder's UNRESOLVED record (one record per folder). The builder's own denominators, printed on the same
in-memory run: `retired_unresolved_by_enrich 16`, `superseded_unresolved_registrations 4` (the keyless registration rows
already filed for Alphabet GOOGL US, Eli Lilly LLY US, Quanta Services PWR and UnitedHealth Group UNH US, of 28 rows, 4
keyless); `registered` counts APPENDED rows after supersession: 27 + 21 - 4 = 44. Branches the synthetic run cannot see:
- **a request that does not MEASURE** (vendor error, no identity, exchange disagreement): no key lands for that folder,
  its record stays UNRESOLVED, the put still covers the others. The purpose number then reads `UNRESOLVED 40 -> k`, printed,
  and each such folder is named in the read-back; it is NOT re-called under this word.
- **a request that MEASURES a key other than the table's** (a different root/cc returned): `add_security` records the
  response's key; the pre-flight's ENRICH/APPEND split may then differ for that row. The read-back prints requested vs
  landed key per row, and this seat compares them before committing `registrations.json`; a mismatch is a row, and the
  rollback in item 1 is the remedy if it breaks one-record-per-folder.
- **nothing lands at all:** `pool_puts 0`, the key is unchanged (digest-equal), versions stay 24.

**Discriminator after the fire:** the probe again -- versions 24 -> 25 (or 24 on `pool_puts 0`), the new version's
denominators against the AFTER line above, and the preflight's twin/multi-claimed census re-run on the served object.

Signed: `2.0.0_SA_COO~X`, 2026-09-24 20:4xZ.

## CTO HALF -- `1.0.0_SA_CTO~Z`

Signed separately, in the CTO's own lane: `org/missions/D5/AMGT/AMGT_CORPUS/ledger/NEVER_WIDEN_ROUND3_FIRE40_CTO_HALF.md` @`af08f78a9b`
(every limb signed; the VENDOR limb HELD pending the word).
