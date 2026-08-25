# Rule-24 record — the per-family SERVING fields on the `EMITTERS` registry

**Cell:** `PRF-c-1` (publisher half) · **TO:** `ADVI_PERFRP.TO-R1-AE` · **Seat:** `0.7.0_AE_CloudOps~G`
**Ratified:** `1.0.0_SA_CTO` 67267, on the determination run at 67249 — *"TWO FIELDS, one grain, each with
its own small record; your write-up IS the four-postulate record of record."*
**Arch review of the field's shape:** CTO 67145. **Requirement ruled by:** COO 67133.
**Status:** AUTHORED, NOT YET LANDED — lands in the `PRF-c-1` commit beside the fields themselves.

---

## What is being minted, and why a record is owed

Two new per-family properties on `EMITTERS` entries in
`data/assets/scripts/gold/runners_49f/d_publisher_port.py`:

| field | round | question it answers |
|---|---|---|
| `deferred` | **1** | **WHETHER** this family publishes at all (carries its reason string) |
| `fan_out` | **2** | **HOW MANY OBJECTS** this family produces when it does publish |

Rule 24 binds at **authoring** time, and it binds every schema-enumeration act — minting an axis,
adding values to one, or adopting one authored elsewhere. This mints registry structure, so the
four-postulate test is owed before the field exists, not after.

## The question actually tested

CTO 67145 proposed these as **one** axis (`SERVING-STATE`), with `deferred` in round 1 and `fan_out`
joining it in round 2, and explicitly invited the opposite finding: *"if the record cannot hold them
on one axis honestly, they are two fields at one grain, and that is fine too — the record decides,
not convenience."*

Tested honestly, the single-axis form fails three of four postulates.

### (ii) SAME GRAIN — **PASSES either way**

Both properties are per-family, i.e. exactly one value per `EMITTERS` entry. Neither is per-object,
per-run, or per-firm.

This is the postulate that made the single-axis reading attractive, and **it is not sufficient on its
own** — same grain is a necessary condition for sharing an axis, never a sufficient one. Recorded
explicitly because "they sit at the same grain, so put them on one axis" is the reasoning the other
three postulates exist to interrupt.

### (iii) INTENT COHERENCE — **FAILS as one axis**

`deferred` is a **state**: does this family publish? `fan_out` is a **disposition**: how is it shaped
when it does? One axis would serve two intents, which is the pair Rule 24(iii) names in terms —
values mixing state with disposition foundationally break the schema.

### (i) MECE — **FAILS as one axis, in the collectively-exhaustive direction**

A single axis needs values along the lines of `{DEFERRED, SINGLE, FANOUT}`. **`DEFERRED` is not a
shape** — it is the absence of publication, so it does not belong in an enumeration of shapes.

The failure is not hypothetical: **Transactions is deferred today AND would be fan-out when
undeferred**, so it has no single value on the combined axis. The one family the field is being
minted for is the family that breaks the combined form.

### (iv) STATE COHERENCE — **FAILS as one axis, and this is the decisive one**

Name the state axis, then ask whether one remedy moves every value together:

| field | discharged by | owner | clock |
|---|---|---|---|
| `deferred` | a **RULING** — Transactions' serving shape being settled | CTO / Andrew | a decision |
| `fan_out` | a **BUILD** — the publisher fan-out extension | round 2, stage 3, arch review | an implementation |

**Neither remedy moves the other.** A schema whose members require different remedies presents as one
workstream and is several — the postulate verbatim, and the reason it exists.

Worth naming: the law calls (iv) *"deliberately the weakest of the four… it earns its place on the
blatant failures."* Here it was the **sharpest**. (iii) establishes that the intents differ; (iv)
establishes what treating them as one would **cost** — a field settled by a sovereign ruling tied
under a shared name to a field settled by a build, so that someone later moves both because they
moved together once.

## Determination

**TWO FIELDS, ONE GRAIN.** `deferred` and `fan_out` both sit on the entry, land together as CTO and
COO wanted, and are **not** one `SERVING-STATE` axis with mixed values.

Each field, evaluated on its own, passes cleanly:

- `deferred` — MECE over {set, unset}; one grain (per family); one intent (publish or not); one
  remedy (a ruling).
- `fan_out` — MECE over {single-object, fan-out}; one grain (per family); one intent (serving shape);
  one remedy (the round-2 build).

## The mechanism the `deferred` field must carry, and why it is not a flag

**Honored BY CONSTRUCTION**: an entry with `deferred` set **never publishes** — regardless of flags,
invocation, operator, or a session that does not know the history.

The existing `--hold-leaves` is a **runtime** hold parsed into a set that **defaults to empty**, so an
invocation omitting it **publishes the held key**. For an ordinary operational hold that is
recoverable. Here the object that would emit is a firm-wide map of every relationship's transactions —
what `s.11 #6` forbids by name and Andrew approved. **So forgetting a CLI flag would be a
sovereign-ruling violation on a served key.**

The publisher's authors already saw this direction and guarded the neighbouring case; the unknown-hold
refusal reads, verbatim, *"a typo'd hold would fail toward PUBLISHING a held key."* **That guard
catches a MISTYPED hold and structurally cannot catch an OMITTED one** — an omitted flag is
indistinguishable from a run that legitimately holds nothing. A control sound on its own axis and
blind on the neighbouring one.

`--hold-leaves` therefore stays exactly what it is — a **session-scoped operational hold** — and the
docstring states the distinction: a policy hold that must survive amnesia lives on the entry; a
temporary hold lives on the invocation. Two lifetimes, two mechanisms, not one mechanism serving both.

## Provenance

Determination run at 67249 in response to CTO 67145(1); ratified unchanged at CTO 67267. Requirement
(a deferral enforcing a sovereign ruling must be durable by construction and must not fail open) ruled
by COO 67133. The `fan_out` per-family form was adopted at CTO 67106(3) as the round-2 spec. The
finding that started the chain — that `d_publisher_port` structurally cannot fan out on any branch —
is at 67037, source-confirmed at `f696acb8f8`.
