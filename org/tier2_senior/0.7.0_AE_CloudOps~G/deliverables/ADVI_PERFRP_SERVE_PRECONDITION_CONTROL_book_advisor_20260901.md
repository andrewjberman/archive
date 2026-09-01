# ADVI_PERFRP SERVE PRECONDITION -- THE CONTROL, RUN. VERDICT: **UNMET**

**Author:** `0.7.0_AE_CloudOps~G` (the ruled OWNER: "the serving design (publisher lane / 0.7.0)")
**PRD author / discharge authority:** `1.0.0_SA_CTO` · **Date:** 2026-09-01 ~00:0xZ
**Raised by:** `0.4.0_DE_ClientPlatform~D` (90357, `[STOP]`) · **HOLD:** `2.0.0_SA_COO` 90365
**Plane:** the payload the publisher WOULD WRITE, built at the current vintage. Nothing was published.

## 0. The precondition (`org/projects/ADVI_PERFRP.json` `blocking`, 2026-08-28)

> served perfrp leaves carrying the client display label OR a custodian account identifier in any
> label/identity/key field owe the SAME server-side pseudonymisation + book-scoping as platinum
> summary.json (Lambda@Edge, **no static key**) **BEFORE any serve/flip**; CONTROL = a census over
> every served row: no name field AND no custodian account id, both denominators, positive control.

## 1. FIRST: A DERIVED CLAIM OF MINE THAT MEASURED FALSE

My 90349 gave a derived expected census listing `perfrp_book_advisor` among the families that
`emitter_refused` **by design**, citing `chain_49f_entrypoint.py`'s docstring and its
*MEASURED 2026-08-25: {would_publish: 6, emitter_refused: 5}*. **Measured false tonight.**

```
  DRY RUN -- no --publish, no OPAL_ADVI_PUBLISH_GRANT, ZERO S3 writes:
    WOULD_PUBLISH  perfrp_book_advisor -> platinum/advi/49financial/perfrp_book_advisor.json
    DENOMINATOR: 1 twin(s) attempted of 26 EMIT twins (23 emitter entries); 0 not clean
```

`book_advisor` **BUILDS and WOULD PUBLISH.** The 08-25 census is STALE -- round-2 wired the plane the
docstring says round 1 does not (`perfrp_emit_core` moved 2026-08-29 @`62a00eed67`).
**A docstring is a description, and a description is never a state.** Anyone resting on my 90349 would
have concluded the leaf never serves and the exposure was moot.

## 2. THE CONTROL -- census over EVERY served row

```
  client_table rows (DENOMINATOR) .........: 9,868
  rows whose `relationship` is a REAL NAME : 9,868      <- 100%, not a subset
  DISTINCT REAL CLIENT NAMES ..............: 3,297
  rows UNMAPPED-RELATIONSHIP-* ............: 0
  rows pseudonymous in `relationship` .....: 0

  POSITIVE CONTROL (these SHOULD be pseudonymous; 0 = pass):
    rows where `client` NOT rel_* .........: 132
    rows where `relationship_id` NOT rel_* : 132
```

>> **VERDICT: UNMET.** A cleartext client-name field is present in every served row of a leaf that
   would be written to a STATIC key -- estate-wide authenticated-fetchable, irreversibly. <<

## 3. ⛔ THE DANGEROUS SHAPE: THE LEAF IS **PARTIALLY** PSEUDONYMISED

Row schema, read at source (three separate fields):

```
  client           = 'rel_05b7c126ca6dcf'        <- pseudonymised
  relationship_id  = 'rel_05b7c126ca6dcf'        <- pseudonymised
  relationship     = 'DIANNE AZZUNZIATA BARBER'  <- CLEARTEXT CLIENT NAME
```

**MY OWN FIRST CENSUS RETURNED A FALSE ALL-CLEAR ON EXACTLY THIS.** I guessed field names instead of
reading the row schema; the matcher hit `client` first, found `rel_*`, and scored the leaf label-free.
It was caught only because the printed sample did not look like names.

> **A pseudonymisation check that lands on the id fields PASSES while the name field sits untouched
> beside them.** "Is it pseudonymised?" is unanswerable without naming WHICH FIELD. Any
> re-verification of this leaf must census `relationship` specifically, and print its denominator.

## 4. LIMITS -- what this control does NOT cover

- **CLIENT-NAME limb only.** The CUSTODIAN-ACCOUNT-ID limb is not swept exhaustively here:
  `entries[].accounts` is an INT COUNT, not a list, so there is no per-account id surface at that
  path -- but that is one path, not a census. Prefer `3.0.0_SA_CVO`'s measurement on that limb.
- **ONE LEAF.** This covers `perfrp_book_advisor`. The precondition is written over "served perfrp
  leaves" **plural**, and the other ten families were NOT censused for the same defect. That gap is
  real; a ruling must not assume this one-leaf census covered the set.
- Numbers differ from 90357's 3,290 because that seat measured the COMMITTED origin/CLOUD artifact and
  this measures a payload BUILT at asof 2026-08-31 (inputs ALIASED from 08-28, declared by the port).
  Different objects, same conclusion; neither corrects the other.

## 5. OPTIONS (reported, not chosen -- the ruling is `1.0.0_SA_CTO`'s)

| | act | lane |
|---|---|---|
| (a) | `--hold-leaves perfrp_book_advisor` on the activation -- the publisher ALREADY has this flag; it BUILDS + manifests but never writes the leaf, so the other families serve while this one waits | this lane, available immediately |
| (b) | pseudonymise `relationship` at the emitter to match the `client`/`relationship_id` treatment already applied beside it | DS emitter lane -- the DURABLE fix |

**"Hold everything" and "publish the names" are not the only two options, and (a) is why.**

⛔ This lane will not activate on ANY signal until `1.0.0_SA_CTO` rules -- including a re-issued CALL-1
completion report.
