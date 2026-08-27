# ADVI_INSURE — THE PATTERN RECORD (`INS-f-1`, criterion `INSR1DS-AC5`)

**author:** `0.4.0_DS_ClientPlatform~J` · **2026-08-25** · **TO:** `ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes`
**decomp:** `workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md`
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`, AT EVERY RELAY** (PRD s.3, Andrew ~16:1xZ).

---

## ⛔ THE ONE SENTENCE THIS RECORD EXISTS TO CARRY

**A porting firm RE-INSTANTIATES this structure on its own vendor tree. It does not import it.
NO CODE IS SHARED, NO KEYS ARE SHARED, NO PREFIX IS SHARED, NO IAM IS SHARED.**

This is not caution, it is standing law: firm separation is gate-enforced at commit and
IAM-Deny-enforced at runtime, and a pipeline tree referencing another firm's bucket is
blocked at both layers. **A pattern is a SHAPE TO COPY, never a MODULE TO CALL.** The reason
this record exists at all is that the shape is worth reusing and the *implementation* is not
reusable — and those two facts are easy to conflate into a shared library, which is the one
outcome this document is written to prevent.

---

## THE STRUCTURE, IN FIVE PARTS

A firm parameterises `{firm}` and re-instantiates. Every path below is written with `{firm}`
deliberately, so no reader can lift a literal foreign prefix out of this file.

### 1. LANDING GRAMMAR — `opal-data-assets`

```
opal-data-assets/blackdiamond/{firm}/bronze/insurance_*     RAW vendor bytes, per run
opal-data-assets/blackdiamond/{firm}/silver/insurance_*     parquet, dedup + dtype ONLY
```

The grammar is `{vendor}/{firm}/{medallion}` — **one grain per axis** (Rule 24). The vendor is
`blackdiamond`; the firm is a firm; the medallion is a medallion. Insurance is a **table-level**
concern (`insurance_*`), **never a directory level between vendor and firm** — putting it there
would place a subject-matter grain on the firm axis and break the grammar for every consumer that
enumerates firms.

- **BRONZE IS RAW** (Rule 17a). Whatever the API delivers, byte-for-byte, per run. **No parquet
  under `bronze/`** — this is bucket-policy enforced on `opal-data-assets`, not merely a
  convention. Parquet at ingest coerces schema and dtypes, and whatever the raw feed carried
  is then unrecoverable. That destroys bronze's single job: everything downstream re-derivable.
- **SILVER IS DEDUP + DTYPE ONLY** (Rule 17). No field slimming, no `fillna`, no `dropna`, no
  business-row filter. Anything requiring a judgment about field relevance or null meaning is
  gold-tier business logic and does not belong here.

⚠ **A LIVE SPELLING HAZARD THE PORT MUST NOT INHERIT.** In the 49F instance the ruled landing
prefix (`49financial`) and the pre-existing live prefix (`49f`) are **two spellings of one firm**,
recorded as an alias, with nothing live moved. **A porting firm should mint ONE spelling and
record no alias** — the alias exists here only because a live tree predated the ruling. Measured
2026-08-25: under `blackdiamond/` exactly two firm prefixes are live and the ruled 49F spelling
is not yet one of them; it is a MINT, and unbuilt is not defective.

### 2. GOLD TABLE SHAPE — the firm's own gold bucket

```
{firm-gold-bucket}/gold/advi/insurance/insurance_nav_current/date={D}/
```

**ONE additive current-state table. Not a series.**

- **Grain:** exactly one row per (`bd_account_id`, `as_of_date`).
- **Additive:** a new row appears ONLY when `as_of_date` advances. Re-running on an unchanged
  `as_of_date` produces **zero** new rows.
- **A re-emission that would CHANGE a value on a closed `as_of_date` is a CONFLICT — refuse
  loudly, never rewrite.** The refusal is the feature: silently rewriting a closed statement
  period destroys the only evidence that the source disagreed with itself.
- ⛔ **NO analytics, NO returns, NO series.** *A snapshot plane that grows a series has become
  an asset-management calculation* — which the never-blend invariant forbids. This is enforced
  by a runnable predicate (`insurance_forbidden_field_census.py`), not by a promise, because a
  promise not to add a column is unfalsifiable.
- ⛔ **PLACE IT IN ITS OWN SUBTREE, NOT BESIDE THE ASSET-MANAGEMENT CONTRACT TABLES.** The
  `canonical/` subtree is the AM contract and the agentic-query root; an enumerator over
  `canonical/*` would blend **by adjacency** the very thing never-blend forbids. Never-blend
  holds *by construction* only when the tables do not share a prefix.

### 3. THE SPINE KEYS — carried, so aggregation is a JOIN

The gold row carries the identity keys so every rollup is a join on an id, and **no figure is
ever computed in the frontend**.

| leg | basis | status |
|---|---|---|
| vendor-native account | the source's own account id | **CARRIED** |
| vendor id → firm account id | the firm's advisor/fee-role join dim | **CARRIED (id join)** |
| account → relationship | the firm's relationship dim | **CARRIED (id join)** |
| firm | constant on the tree | **CARRIED** |
| **advisor** | — | ⛔ **`NOT-CAPTURED-PENDING-SURFACE`** |

⛔ **THE ADVISOR LEG IS DECLARED ABSENT — BUT ITS STAMP WAS CORRECTED 2026-08-27 AND THE
CORRECTION IS THE POINT OF THIS ROW.** This table read **`NOT-DERIVABLE-UPSTREAM`** until
`0.4.0_DS_ClientPlatform~R`'s INS-a-2 census (@f05d754d43) falsified that value's premise, and
`2.0.0_SA_COO` 76245 restamped it. **The prior text is preserved here rather than overwritten,
because a porting firm needs the mistake more than the conclusion.**

**What stays TRUE** (the original measurement, undisturbed): zero columns matching an
advisor-identifier shape across all three spine tables (0 of 95 columns, re-run by the issuer
over a wider net and it survived); every advisor handle is a **name string**; the two name
formats are not mutually parseable. **A name-string join across a six-figure dim is a
silent-collision generator — it returns a plausible number rather than an error.** Identity is
by id, never by label, and **an honestly missing level beats a level that is right most of the
time.**

**What was FALSE:** that no upstream change could ever populate it, i.e. that the remedy lay
with the vendor. Measured: the advisor carrier is the `relationshipdetail` surface's
`financialTeam[]` — **already sanctioned in the vehicle's own egress allowlist, already routed,
and simply never called** (zero landed objects; the landed relationship rows carry a `teams[]`
key that is empty on 77 of 77, which is why the *absence* was real even though the *diagnosis*
was wrong).

>> ⛔ **THE PORTABLE LESSON, AND IT IS THE ONE THIS ROW EXISTS TO CARRY: `NOT-DERIVABLE` AND
>> `NOT-CAPTURED` ARE DIFFERENT CLAIMS WITH DIFFERENT OWNERS.** "Not derivable" says the vendor
>> cannot supply it and points at a vendor ask. "Not captured" says we never asked and points at
>> ourselves. **A porting firm that inherits the wrong one hands its own gap to its vendor and
>> waits.** Before stamping any leg absent, run the discriminating question — *what remedy moves
>> this value: our own capture, a vendor config change, or nothing ever?* — and stamp the
>> remedy, not the symptom. A confidently wrong absence-claim closes a question that an
>> honestly empty field would have kept open. <<

**A porting firm should therefore check whether its own vendor supplies the identifier on a
surface it has not yet called**, before concluding the leg is unbuildable there.

Unresolvable rows take a declared `spine_class` of `unassigned`. **They are NEVER dropped** —
a dropped row silently shrinks the denominator of every figure above it.

### 4. PLATINUM KEY FORM — one json, one producer

```
opal-data-portal-v2/platinum/advi/{firm}/insurance_nav.json
```

Emitted as an entry in the firm publisher's own `EMITTERS` registry, so it joins that firm's
twin set and rides the publisher's existing activation. **ONE PRODUCER PER SERVED KEY** — this
holds *by construction* when the leaf is an `EMITTERS` entry and the writer only touches keys
under its own serve root, not by anybody promising to be careful.

*The counter-example this estate already carries: two emitters writing one served key with
disagreeing cache headers, resolved only by write order. That is what a second producer buys.*

- **Rollups are carried AS JOIN KEYS, not as pre-summed levels**, so the served shape cannot
  disagree with a recomputation from its own rows.
- `as_of_date` is served **per row** — the consumer must be able to show the statement date,
  because a snapshot's value without its vintage is not interpretable.
- **This MINTS a served key; it does not move one.** Minting needs no never-widen sign-off.
  **Moving or repointing an existing served key does** — stated positively here so nobody
  re-derives the distinction under pressure and reaches for the wrong one.

### 5. THE CLASS-AXIS VALUE — a new value, not a fold-in

Insurance is its **own** value wherever asset totals are broken out. ⛔ **It is NOT folded into
an existing alternatives-style bucket** — the formats are too different, and the fold-in is a
category error rather than a display preference.

⛔ **MINTING THAT VALUE IS A RULE 24 AUTHORING ACT AND OWES A FOUR-POSTULATE RECORD** (MECE ·
same grain · intent coherence · state coherence) plus a token-hygiene census — **and ADOPTING
this schema elsewhere is itself an authoring act, so a porting firm owes its own record and may
not inherit this one.** The vendor's native class vocabulary is *evidence*, never the answer.

*Scope note: the class-axis work is a frontend-lane cell and is not this seat's to execute. It
is recorded here because the pattern is incomplete without it, and a porting firm reading only
the backend half would ship a plane with nowhere to render.*

---

## WHAT A PORTING FIRM MUST NOT COPY

1. **Any literal prefix from the originating tree.** Parameterise `{firm}`; mint your own.
2. **Any code module.** Re-instantiate. A shared module across firm trees is gate-blocked and
   IAM-denied, and it is blocked because it is wrong, not merely because it is watched.
3. **The alias.** Two live spellings for one firm is residue here, not design.
4. **The advisor leg's absence, unexamined.** It is a measured property of *this* vendor
   surface. Measure your own before concluding it is missing — or before concluding it is there.
5. **The `carrier` / `product` field names.** In this instance they are the PRD's *assumed*
   names; the populated characteristics schema was never observed (one specimen, empty).
   **Resolve them against a real populated response, or declare them absent.**

## THE TRIGGER

The port is a **scheduled act**, not a parallel build: it begins when the originating firm's
plane is complete and certified. ⛔ **No shadow path, no parallel emitter, no standing
comparator** — build it correctly once and port it. An extra path is never decommissioned and
becomes permanent debt; a standing comparator adds a second instrument to adjudicate instead of
clarifying the first.

---

## PROVENANCE OF EVERY MEASURED CLAIM ABOVE

| claim | grounding |
|---|---|
| two firm prefixes live; ruled 49F spelling absent | `list_objects_v2` full walk, 3,655 keys under `blackdiamond/`, 4 pages |
| zero insurance keys anywhere | 480,954 keys fully walked across 4 named trees; positive control `allocation` = 416 |
| advisor: no id column | 0 of 95 columns across the three spine tables; issuer re-ran wider and it held |
| account → relationship resolves | 7,356 of 7,382 = 99.65%; 26 unassigned |
| vendor id → firm account id exists | firm join dim carries both, 5,337 distinct each |
| publisher is a single-registry writer | source read of the firm publisher's `EMITTERS` + serve-root write path |

⚠ **Every figure here is DESIGN-layer or measured-on-neighbouring-tables. None of it is an
APPLIED claim about an insurance artifact, because no insurance artifact exists.** The day one
does, these same instruments re-run against it — and *that* run, not this record, is the applied
evidence.
