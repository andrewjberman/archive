# Rule-24 record: `LABEL_VINTAGE_NOT_CAPABLE`, the fourth member of `label_state`

**Ruled by:** 1.0.0_SA_CTO 80311 — which WITHDREW that seat's own promotion of
`SPINE_LABEL_ABSENT` from DECLARED to JUSTIFIED and split this member out instead.
**Held by:** 0.4.0_DS_ClientPlatform~V (the emitter), per 80311 and 2.0.0_SA_COO 80318.
**Sequenced by:** 2.0.0_SA_COO into the re-open bundle's ONE key-shape change, alongside
the label-field removal and the sentinel → opaque id. **Nothing lands mid-round; (A)
stays certified.**
**Measured at:** the emitted leaves and the pinned S3 partitions, arm
`arms/perfrp_b6_unlabelled_lost_cause.py`.

The enum becomes: `LABELLED` / `UNMAPPED` / `SPINE_LABEL_ABSENT` /
**`LABEL_VINTAGE_NOT_CAPABLE`**.

## The census — and read the disclaimer before the numbers

⛔ **`label_state` IS EMITTED ON NO ROW TODAY.** Row keys are `client`, `relationship`,
`relationship_id`, `status`, `key_continuity` and the five figures. So the table below is
**DERIVED** — the classes these members *would* assign — and is **not** a read of an
emitted field. That gap is the re-open emit line this record exists to specify, and
stating it here is the difference between a census and a claim about the artifact.
DESIRED is not APPLIED.

| leaf | rows | `LABELLED` | `UNMAPPED` | `LABEL_VINTAGE_NOT_CAPABLE` | `SPINE_LABEL_ABSENT` | sum |
|---|---|---|---|---|---|---|
| `perfrp_book_advisor.json` (ruled; start vintage 2026-03-24, schema **2.0**) | 9,880 | 9,748 | 132 | **0** | 0 | 9,880 ✓ |
| `..._floor_aligned.json` (evidence; start vintage 2026-07-14, schema **1.0**) | 10,284 | 9,904 | 132 | **248** | 0 | 10,284 ✓ |

`SPINE_LABEL_ABSENT` is **0 on both leaves**. That measurement is what withdrew the
promotion: the member has no population anywhere, and the 248 sit entirely in the new one.

**Grain, stated because two seats printed different correct numbers.** 3.0.0_SA_CVO's
`248` and `19` are ROW counts; at KEY grain the same populations are `86` and `9`. One
relationship key sits on several advisors' tables. Comparing a key count to a row count
is the slip that produced the 316-vs-242 defect earlier in this round, so the arm prints
both grains side by side.

## Postulate (i) — MECE over a DECLARED domain

**Domain:** the label resolution outcome for one client-table row, **against the
vintages that row's own leaf pins**.

The uncovered member the split hunts: a row whose key has no label **because no pinned
vintage carries the label COLUMNS AT ALL**. `SPINE_LABEL_ABSENT` names a row whose key
has no label **value** in a vintage that *could* have held one. Before the split, both
collapsed into the latter — so a capability failure was scored as a data failure.

MECE holds: `UNMAPPED` iff no relationship record exists (sentinel key);
`LABEL_VINTAGE_NOT_CAPABLE` iff no pinned vintage carries the label columns;
`SPINE_LABEL_ABSENT` iff a pinned vintage carries the columns but no value for that key;
`LABELLED` otherwise. The census sums exactly to the row count on both leaves.

## Postulate (ii) — SAME GRAIN

All four classify **one client-table row against its own leaf's pins**. Not a key
property, not a leaf property. This is load-bearing for the 9 keys (19 rows) that are
labelled on the *ruled* leaf: they are label-capable **elsewhere** and still
`LABEL_VINTAGE_NOT_CAPABLE` **for this leaf's window**, because the member is a property
of the pinned vintages, not of the key. The arm prints them on their own line so they
never read as ordinary members of the class.

## Postulate (iii) — INTENT COHERENCE

One axis: how label resolution ended for this row. The member does not encode *why the
vintage is what it is* (a campaign-state question), nor whether the relationship exists
(`UNMAPPED`), nor whether it moved (`key_continuity`), nor membership (`status`).

## Postulate (iv) — STATE COHERENCE: the split's whole justification

| member | owner | remedy | does the remedy move the others? |
|---|---|---|---|
| `LABEL_VINTAGE_NOT_CAPABLE` | the **vintage's producer** — here the 49F campaign rewriting 2026-07-14/15 to schema 2.0 | a label-capable vintage covers the window | **no** |
| `SPINE_LABEL_ABSENT` | the **spine's label producer** | populate the label value | **no** |
| `UNMAPPED` | whoever creates the relationship record | create it | **no** |

**Three owners, three remedies.** Folding the 248 into `SPINE_LABEL_ABSENT` would put two
owners on one member and point the remedy at a producer who cannot move it.

## DECLARED ON THE CAUSE, NEVER ON THE COUNT

A schema-capability boundary is a permanent property of a versioned store pinned at a
historical vintage. The member stands whether today's count is 248 or, after the
campaign's rewrite, 0.

⛔ **This is the whole reason the member exists in this form.** 1.0.0_SA_CTO 80170 held
that a member justified by a population is hostage to whether that population was real,
and struck the 270 on exactly that ground — then justified `SPINE_LABEL_ABSENT` on the
248, a population this seat predicts a scheduled job erases. The prediction is the
member's **test**, not its warrant: a drop to 0 after the rewrite CONFIRMS the member
rather than orphaning it.

## The falsifier — and the cells that kill this record

The arm asserts the **CAUSE** (does the pinned partition carry `mapped` /
`registration_name`?) read **at the partition**, never at the leaf's own
`label_basis` claim — the artifact must not be the evidence for a statement about itself.
The leaf's claim is a **cross-check that must AGREE**; a disagreement is the finding, not
a tolerance. Both leaves agree today.

`(S)` is read **PER PARTITION** and its load-bearing date is taken from the leaf's own
pin, not a literal, so a re-emission that moves the window start moves the oracle with it
(3.0.0_SA_CVO 80341: a conjunction over 07-14/15 would read false on a 07-14-only
rewrite *while the labels collapsed* — "no evidence" printed beside the evidence).

Against 2.0.0_SA_COO's re-issued table, **two cells destroy this record and both are
owned here**:

- **`(R)` without `(L)`** — the vintage becomes label-capable and the 248 do **not**
  resolve. Then the cause is a JOIN or EMITTER defect, not a vintage one, and
  `LABEL_VINTAGE_NOT_CAPABLE` is the wrong diagnosis for those rows. **Mine.**
- **Neither, with `(S)` true** — the capability reading is refuted at its root, the fourth
  member is wrong, and `SPINE_LABEL_ABSENT` reabsorbs the 248. 1.0.0_SA_CTO recorded this
  as the falsifier of the member; it is equally the falsifier of the argument this seat
  made for it.

## `(R)` would be UNTESTABLE by construction, and it is rescuable — measured

2.0.0_SA_COO's hazard: if the campaign rewrites **both** sides of the re-key comparison,
the collapse from 21.6% is guaranteed by construction and `(R)` stops discriminating —
the arm would confirm the producer reading using an artifact the rewrite manufactured.

**Measured at the bucket, not assumed:** `opal-data-49financial` has versioning
**Enabled**, so the pre-rewrite bytes of `2026-07-15` remain addressable by `VersionId`
after the campaign overwrites them. `(R)` can therefore be re-measured against the
**same old vintage** rather than against the rewritten one, which restores its power to
discriminate.

⛔ **Exactly what was proven, and what was not.** A **non-latest** version was read
successfully by `VersionId` (`date=2026-08-18/data.parquet`, two versions, both
materialised) — that is the readability limb the rescue depends on, and it holds.
**Distinctness was NOT demonstrated**: the only two versions available today are
content-identical (7,321 rows, 12 columns, `schema_version` 2.0 both), so no control here
shows a prior version differing from its successor. `date=2026-07-15/data.parquet`
currently has ONE version; the rewrite is what creates its second. So the rescue is
sound on the limb that matters and **unexercised on a genuine content change** — state it
that way rather than as a demonstrated round trip.

## What this record does not claim

- It does **not** claim the member is emitted. It is not, on any row, on either leaf.
- It does **not** claim `SPINE_LABEL_ABSENT` is unnecessary — it is DECLARED at
  population 0 and remains reachable whenever a label-capable vintage holds a null label.
- It does **not** propose consumer wording. Per 0.4.0_DE_ClientPlatform~D 80227 the row
  type carries these as strings and does not branch on them.
