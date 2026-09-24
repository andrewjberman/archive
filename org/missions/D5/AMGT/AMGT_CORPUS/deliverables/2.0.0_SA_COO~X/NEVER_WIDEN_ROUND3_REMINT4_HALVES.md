# AMGT_CORPUS round 3 -- never-widen pair, the RE-MINT (the 4 skipped registrations + the 16 dropped folder forms)

The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`, in its own lane
(`ledger/`), as for the 40-name fire. Nothing runs until both are signed at these bytes AND the production sequence now
running (started 21:35Z, log `evidence/production_sequence_after_fire40_20260924T212840Z.log`) has ended, so the crosswalk
never moves under a running sequence.

## COO HALF -- `2.0.0_SA_COO~X`

**Why a second put.** The fire @`505fc14404` landed clean inside its pair but left two gaps, both now fixed on
`2.0.0_SA_COO~Z`'s identity surface:
- **Z-S23:** 4 folders (Alphabet GOOGL US, Eli Lilly LLY US, Quanta Services PWR, UnitedHealth Group UNH US) were skipped
  as already-registered on their earlier KEYLESS rows, made no call, and stay UNRESOLVED. Fixed @`e772a89bad`.
- **Z-S24:** the 16 ENRICH folders lost their own `security-<hash>` association form when the attach retired their
  UNRESOLVED record, so the corpus ingest cannot find them (resolved_folders 73 of 89). Fixed @`74e6a76e5c`: the retired
  record's forms move onto the enriched record.

### THE ACT

The same producer, the same table, ONE run, after READ_HERE s.2 and `bloomberg_health`:

    OPAL_INDUCTION_FIRE=1 python -m lib.research.corpus.induction_run --fire --as-of 2026-09-24 \
        --evidence org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/UNRESOLVED40_CALLS_20260924.json

The 36 already keyed skip with no call (`_find_existing` now matches only keyed rows). The 4 are called: at most **4**
Bloomberg reference calls, the first for each. Vendor authority: Andrew-direct R-21 @`b390c36444`, released for this
producer by `1.0.0_SA_CTO~Z` (msg 25761; msg 25773: "R-21 already covers the calls" for these four). One batch call, at most
one conditional put. The put REBUILDS the whole document, so the 16 forms return in the same put.

### BLAST RADIUS -- unchanged from the fire's pair, re-counted

1. ONE conditional put on `s3://opal-data-harvest/crosswalk/v1/2026-09-24.json` (IfMatch, digest-differs only, read-back
   raises on mismatch). **Rollback:** copy VersionId `ISiEZGfV4H82rpz2yaM9WelZd4C9ldBI` forward (versioned bucket, no
   delete); the one before it, `BN_TiAyAX_EwRm_nP.PMymkiUnFBMA1N`, stays the round-2 anchor.
2. Up to 4 write-once raw identity landings, NEW keys only (`IfNoneMatch="*"`).
3. `lib/research/identity/registrations.json`, +4 rows at most; committed by this seat after the run or reverted with item 1.
4. This seat's read-back and log.
NOT in the write set: any other key, `universe/v1/`, any dossier/backlog/filings key, any delete.

### WRITER CENSUS -- N = 2, unchanged

`crosswalk.py:1269` (`crosswalk.main --write-pool`) and `add_security.py:380` (`_mint_pool`, this act); the CTO's put-verb
census found a third `write_pool` caller composing `universe/v1/`, a different key (CTO half @`af08f78a9b`, s.3). Both
writers call `crosswalk.build_crosswalk`, so @`74e6a76e5c`'s form carry binds either.

### BEFORE-STATE -- measured 21:54:07Z (re-measured immediately before the run)

`versions 25, latest VersionId ISiEZGfV4H82rpz2yaM9WelZd4C9ldBI, ETag "adbe628b6ba32f5658850ca6ee807a39", size 590370,
sha256 6de718bcbad4bf2d..., denominators records 238 MEASURED 234 UNRESOLVED 4 registered 47 universe_registered 158`;
raw identity objects 60. Instrument `refire_versions_probe.py`, `evidence/remint4_probe_before_20260924T215406Z.json`.

### EXPECTED OUTCOME -- read from the producer's AND the builder's rules, both branches

`preflight_40_fire.py` now models the request-side skip with the producer's own `_find_existing` and censuses each
folder's own form from `crosswalk.harvester_key` (the ingest's function), on committed bytes (identity tree 0 modified,
CLOUD @`f3c4532dd3`, `evidence/preflight_remint4_20260924T215332Z.log`): already-registered 36, called 4 (ENRICH 3, APPEND 1);
AFTER `records 235 MEASURED 235 UNRESOLVED 0 registered 47 enriched 20`, multi-claimed 0, twins 0, 234 of 234 prior keys, 1
new key = 1 appended, **folder-form coverage 40 of 40**, VERDICT PASS.
- A request that does not MEASURE: that folder stays UNRESOLVED; the put still carries the 16 forms; `UNRESOLVED 4 -> k`
  printed and named.
- Nothing lands: `pool_puts` may still be 1, because the rebuilt document now differs (the 16 forms), and that put is
  wanted; versions 25 -> 26.

**Discriminator after the run:** the probe (versions 25 -> 26), the served-object census (twins 0, multi-claimed 0, every
table folder's own form on the record carrying it), then the re-ingest reading **resolved_folders 93** (89 + the 4), then the
production sequence for the 20.

**The instrument lesson this pair carries.** This seat's first two runs of the widened pre-flight read 36 and 37 of 40
because they ran in the SHARED tree while `2.0.0_SA_COO~Z`'s fix sat there uncommitted; only the run on a clean identity tree
at a committed HEAD is cited above.

Signed: `2.0.0_SA_COO~X`, 2026-09-24 21:5xZ.

## CTO HALF -- `1.0.0_SA_CTO~Z`

Owed, in the CTO's own lane (`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`).
