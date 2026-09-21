# DRAFT -- R4 narrowed to custodial data, a GENERAL tenancy, and the `harvest` scope row

**Author:** 4.0.0_SA_CRO (Chief Research Officer)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Status:** DRAFT. **Nothing here has been written to `infra/logic/**`.** Landing waits on Andrew's word on
this exact text (his ~16:3xZ 2026-09-21 "All recs approved", CALL 1: *"Nothing lands until you approve the
exact wording on its own card"*, record @4142a785fc).
**Drafted against:** laptop `CLOUD` HEAD `3467f1d265`; doctrine/registry/grader last touched @`dbfceee5e3`.

## 0. What this carries out

Andrew-direct 2026-09-18 at the `4.0.0_SA_CRO~Z` terminal (record
`org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/ANDREW_DIRECT_20260918_214xZ_CONFORM_AMGT_DATA_TO_THE_CANON.md`,
origin/SITEZ @`0756d2897d`), verbatim:

- ~21:5xZ: *"We can run bronze and silver inside the opal-data-harvest bucket, that is fine, it does not need to be
  in opal-data-assets, which i believe should exclusively be for client assets."*
- ~22:0xZ, choosing between (i) a new tenancy only and (ii) the doctrine itself recording his reading: *"yes 2 is
  the move"*
- ~22:0xZ: *"opal-data-assets is very specifically for client/partner custodial information"*

The work was routed to this seat because lane `PLATFORM_LOGIC_DOCS` (`infra/logic/**`) admits only
`4.0.0_SA_CRO` base/~A/~B/~C/~D (0.0.0_AB_MSTR~Z relay, msg 99081). Evidence base:
`LGIC_NAMING_STANDARD_READ_20260918.md` (origin/SITEZ @`0756d2897d`), re-measured here at laptop HEAD.

## 1. The three edits, exactly

### EDIT A -- `infra/logic/02_DOCTRINE.md`, R4 (currently `:360-370`)

**REPLACE** the heading sentence and the non-application line. The census and authority lines stay, with one
authority clause added.

```
**R4 -- BRONZE AND SILVER OF CLIENT/PARTNER CUSTODIAL INFORMATION HAVE ONE HOME: `opal-data-assets`.**
`opal-data-assets` is very specifically for client/partner custodial information. Every other scope --
general and product data, harvest included -- is homed by its scope at every tier, bronze and silver
included (the scope row's tenancy, `infra/logic/registry/tiers.json`). This is the ingest spine for
custodial data; it is what "consolidation" meant.
. plane: storage-path . authority: [unchanged 2026-07-13 / 2026-08-25 / Rule 17b / 3fd386598f clauses];
  **narrowed Andrew-direct 2026-09-18 ~21:5xZ-22:0xZ** (*"opal-data-assets is very specifically for
  client/partner custodial information"*; option (ii), *"yes 2 is the move"*), record
  `4.0.0_SA_CRO~Z/deliverables/ANDREW_DIRECT_20260918_214xZ_CONFORM_AMGT_DATA_TO_THE_CANON.md`
. census: [unchanged]
. non-application: none for custodial data. The narrowing MOVES NOTHING: a scope whose registry row
  homes its bronze or silver in `opal-data-assets` today keeps that address until its own classification
  and migration (R19). "Custodial" is his word and is not defined further here.
```

### EDIT B -- `infra/logic/02_DOCTRINE.md`, R8 (currently `:416-418`) and the pattern table (`:101-102`)

R8, **REPLACE** `**bronze still lands in `opal-data-assets`** (R4); everything ABOVE bronze may live in the product
bucket **with a declared reason** (R20).` **WITH**:

```
bronze and silver are homed by the scope (R4 as narrowed 2026-09-18); everything above them may live
in the product bucket with a declared reason (R20).
```

Pattern table, the BRONZE and SILVER `home` cells, **REPLACE** `` `opal-data-assets` `` **WITH**:

```
`opal-data-assets` for client/partner custodial information; otherwise the scope's bucket (R4)
```

R14's grid needs no edit: its client-confidential row already says `opal-data-assets`, and its general row
names no bronze/silver home.

### EDIT C -- `infra/logic/registry/tiers.json` and `scopes.json`

**ADD** a fifth tenancy to `tiers.json` `homes` (the four existing tenancies are NOT edited):

```json
"GENERAL": {
  "bronze":   {"home": "scope", "rule": "R4 (narrowed 2026-09-18): opal-data-assets is for client/partner custodial information only; a general scope homes bronze in its own bucket"},
  "silver":   {"home": "scope", "rule": "R4 (narrowed 2026-09-18); R8"},
  "gold":     {"home": "scope", "rule": "R5: product-shaped gold lives in opal-data-{product}"},
  "platinum": {"home": "shared", "bucket": "opal-data-portal-v2", "rule": "R6: general platinum lives in opal-data-portal-v2/platinum/"},
  "state":    {"home": "scope", "rule": "R21"},
  "code":     {"home": "scope", "rule": "R16"}
}
```

**ADD** a tenth row to `scopes.json` `scopes`:

```json
{"key": "harvest", "class": "PRODUCT", "long": "harvest", "short": "harvest",
 "tenancy": "GENERAL", "bucket": "opal-data-harvest", "bucket_provisioned": true, "aliases": []}
```

## 2. What it does -- measured by simulation, the repo registry untouched

Instrument: `scratchpad/sim_general.py`, which copies `infra/logic/registry/` to a scratch directory, applies
EDIT C there, repoints `lib/opal_naming.REGISTRY_DIR`, and calls `address()` and `validate()`. Run 2026-09-21
~16:4xZ at HEAD `3467f1d265`.

- **`validate()`: 0 refusals, 17 warnings** -- the same 17 `owner_directive` warnings the live registry carries.
  **Negative control:** the same row with `"tenancy": "NOSUCHTENANCY"` returns **1 refusal**, so a zero here can
  fail.
- **The `harvest` scope, after:**

  | source | bronze | silver | gold | platinum | state | code |
  |---|---|---|---|---|---|---|
  | `bloomberg` | harvest | harvest | harvest | portal-v2 | harvest | harvest |
  | `amgt` | harvest | harvest | harvest | portal-v2 | harvest | harvest |
  | `harvest` | REFUSED | REFUSED | REFUSED | REFUSED | REFUSED | REFUSED |

  e.g. `s3://opal-data-harvest/bloomberg/harvest/bronze/<table>/date=2026-09-21/<object>`. The `harvest`-as-source
  refusals are the existing scope rule (*"a product is never a scope beneath itself"*), correct and unchanged.
- **Nothing that resolves today moves.** Over the **9 existing scopes x 7 sources x 6 tiers = 378** combinations,
  **0** addresses that resolved before changed. **3** that were REFUSED now resolve: source `harvest`, scope
  `global`, tiers gold/state/code -> `opal-data-harvest` (the COMPOSITE tenancy homes those by source, and the new
  row gives `harvest` a bucket). That is a newly reachable address, not a re-homed one.

## 3. Why NO R20 exception entry

The relay (99081) listed "the R20 ledger entry" among the pieces. Under option (ii) there is no departure to
record: once R4's own text scopes `opal-data-assets` to custodial data, harvest's bronze and silver in
`opal-data-harvest` CONFORM. An R20 entry would declare an exception to a rule the edit has already changed,
creating a second carrier for one fact (doctrine s.4: *"two carriers of one list drift"*). Recommended: none.

## 4. Choices this draft makes that Andrew should see

1. **A NEW tenancy rather than editing PRODUCT's cells.** Changing PRODUCT's bronze/silver to `scope` would
   silently re-home `mdpf` and `etfs` bronze/silver -- the hazard CRO~Z named in the 9/18 record, item 3 of the
   ~22:0xZ addendum. Under this draft, whether `mdpf`/`etfs`/`global` bronze and silver are custodial is **not
   decided**; each keeps its current home until its own classification (R19).
2. **Harvest platinum stays in `opal-data-portal-v2`.** His word covered bronze and silver; R6 homes general
   platinum in portal-v2. Moving it would be a separate departure he has not made.
3. **"Custodial" is quoted, not defined.** Whether a firm-attributable derivation of custodial data is itself
   custodial is his question (9/18 record, final addendum).

## 5. What this draft does NOT settle

- **AMGT_RESAPP's own key shapes** (which `{source}` each prefix takes, and which prefix is which tier) are that
  project's L4 classification, owned by `1.0.0_SA_CTO~Z` / `2.0.0_SA_COO~Z`. This draft makes the keys BUILDABLE.
- **The `harvest` systems.json row's `owner_directive` (D5)** stays `inferred`; `validate()` keeps warning on it.
- **CLAUDE.md Rule 30's "(WARN today, LGIC_ENFORCE)"** is stale per CRO~Z's read (naming limbs enforcing since
  2026-09-17 @`d181e0ac5a`). Not touched here; that is a CLAUDE.md edit.
