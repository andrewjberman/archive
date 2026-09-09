# STATE MODEL — NFRA_REPORT's rendering law (cell RP-s-1, outcomes FWD-2/FWD-4)

Authority: ruling 12, `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260909_1458Z_INFRA_REPORT_FIVE_RULINGS.md`
batch 5 ("THE NAMING LAW"), plus its forward-pointer recording `1.0.0_SA_CTO~Z`'s L4 ruling on this
cell's two expressibility gaps, and `NFRA_REPORT_PRD.md` §5/§6 (`C-FWD2-FIRST`, `C-WEBSITE-BLIND`,
`C-SENTINEL-STATE`). This document is the report's naming law: every row the report renders states
its position on Axis 1, then (only where Axis 1 says a look happened) its position on Axis 2, then
(only where the row is not fully `applied`) its position on the third axis below.

## 1. AXIS 1 — THE INSTRUMENT: did the check happen, and could it?

Six values, ratified in full by ruling 12, promoted from Contract Integrity (five) and the Terraform
drift sub-section's `deny-blocked-by-design [recorded]` tag (one). **All six bind. None is edited,
removed or redefined here or anywhere by this cell.**

| Value | Meaning |
|---|---|
| `CHECKED` | looked, and the result is trustworthy |
| `BLIND` | could not look — nothing governs or detects this surface |
| `INERT` | a control exists but CANNOT FIRE (names no live role; pages no subscriber) |
| `COARSE` | looked at the wrong grain — the answer is advisory only |
| `UNCHECKED` | deliberately not asserted |
| `DENY-BY-DESIGN` | cannot look, and that is intentional and recorded |

Worked examples ruling 12 itself gives, carried here unchanged: `opal-login-abuse-alerts` is
`INERT`, never `RED`. `comp` is `CHECKED`/`OK` carrying a stale-instrument qualifier, never `RED`.
Website security renders in the not-`CHECKED` family (see §4) — never `OK`.

## 2. AXIS 2 — THE WORLD: what was found

Meaningful **ONLY** where Axis 1 = `CHECKED`. Printing an Axis-2 value against any other Axis-1 value
is the forbidden pair ruling 12 exists to prevent.

| Value | Meaning |
|---|---|
| `OK` | within standard |
| `DEGRADED` | outside standard, contained |
| `BREACH` | outside standard, NOT contained |

**Forbidden, structurally:** `BREACH` or `OK` on a surface nobody looked at. A row whose Axis 1 is
`BLIND`, `INERT`, `COARSE`, `UNCHECKED` or `DENY-BY-DESIGN` carries NO Axis-2 value — the cell renders
`—` there, never a colour.

## 3. GREEN, defined for free

**GREEN = every property `CHECKED` on Axis 1 AND `OK` on Axis 2.** Nothing is green by virtue of not
having been looked at.

## 4. GAP 1 — PERMANENT vs TEMPORARY blind. RESOLVED, NO NEW FIELD (YAGNI).

The ratified six-value enum already carries this distinction: `DENY-BY-DESIGN` means "cannot look,
and that is intentional and recorded" — which is permanence plus a reason, in one value. `BLIND`
without qualification is the temporary/unresolved member of the same not-`CHECKED` family; `DENY-BY-
DESIGN` is its permanent, recorded sibling. No `resolvable` field is built. An earlier draft of this
cell proposed one; it was withdrawn as a second vocabulary for something the first already said, and
it stays withdrawn here.

**Worked specimen — the Website security row, settled PERMANENTLY, not pending (`C-WEBSITE-BLIND`):**

| Property | Axis 1 | Axis 2 | 3rd axis (§5) | Reason (attached, not a caveat) |
|---|---|---|---|---|
| Website (opalinvest.com / www) | `DENY-BY-DESIGN` | — (not meaningful) | — (not applicable — nothing here is "applied" in the desired/applied/exercised sense; the state is a permanent design refusal, not an unapplied intent) | `opalinvest.com` and `www` resolve to the EC2 elastic IP with no CloudFront; AWS WAF cannot attach to a bare EC2; every candidate edge needs a GoDaddy record change. Recorded twice — `NFRA_OPSEC202609` C-19 and this PRD's `C-WEBSITE-BLIND` — and the choice not to remove the blindness is Andrew's own: "we do whatever we can without having to engage with GoDaddy." This row does **not** wait on `TO-OP-S-13` and is **not** a gap awaiting a fix. |

That is the row a reader needs to be able to tell apart from a temporary gap: **"we have no way of
seeing this, permanently, and here is why"** — not "we looked, and here is how bad it is," and not
"we haven't gotten to it yet."

## 5. GAP 2 — DESIRED-not-APPLIED. RESOLVED: A THIRD ORTHOGONAL AXIS.

A `BLOCKED` address row is INTENT that no IP set enforces. `INERT` is the closest ratified value and
is still wrong: `INERT` means a control that CANNOT FIRE, and the sentinel CAN fire and is
deliberately run watch-only (`TO-OP-S-14-21` is complete; the sentinel's reconciler `TO-OP-S-15-19` is
staged). Folding "is this desired, applied, or exercised" into either ratified axis is a rule-24(iii)
intent-coherence violation — Axis 1 asks *did the check happen*, Axis 2 asks *what was found*, and
desired-vs-applied is a **third question**, not a value on either.

**Resolution directed and built here: a third orthogonal axis, carrying CLAUDE.md rule 22's own
vocabulary VERBATIM — no synonym is minted.**

```
state: desired | applied | exercised
```

This axis is **rendered only when the row's state is not `applied`.** A fully applied-and-exercised
control carries no third-axis text at all — the omission itself says "this is real," which is why the
axis is silent everywhere except the DESIRED-not-APPLIED case it exists to name.

**Worked specimen — the blocked-address sentinel table (`C-SENTINEL-STATE`):**

| Property | Axis 1 | Axis 2 | 3rd axis | Reason (attached) |
|---|---|---|---|---|
| Blocked-address row (per address, sentinel table) | `CHECKED` (the sentinel does look/count hits against the address; it is not `INERT` — it CAN fire) | `OK` or `DEGRADED` per what the sentinel actually observes on that address | **`desired`** (rendered because it is NOT `applied`) | The address is watch-listed and the sentinel counts and evaluates it, but no IP set enforces the block: `sentinel_block_armed` runs watch-only and the enforcement reconciler (`TO-OP-S-15-19`) is staged, not applied. A report rendering this table without the third axis reports INTENT AS FACT — exactly what `C-SENTINEL-STATE` forbids. |

Note what this specimen is NOT: it is not `comp-iam`-sourced evidence. `comp-iam` does not model
`wafv2` — the plane this row's enforcement path lives on — so `comp-iam` silence is never cited here,
or anywhere in this document, as evidence about the sentinel's enforcement state. The third-axis value
above is read from the Terraform variable and the reconciler's own staged/complete status, not from
`comp-iam`.

**Build-ladder discipline:** rung 2 — the estate already holds `desired | applied | exercised`
(CLAUDE.md rule 22, EVIDENCE LAW's STATE axis). Nothing new was minted. Nothing in ruling 12 is
amended: the third axis adds no value to either ratified enum, redefines neither, and cannot make the
forbidden pair (`BREACH` or `OK` on a surface nobody looked at) printable — the check that would have
falsified this resolution (does it let `INERT` become mutable, or let a `DENY-BY-DESIGN` row acquire an
Axis-2 colour) comes back clean: it does neither.

## 6. Naming tensions carried, not hidden

- **The record's own "two-axis" language is now a description of HISTORY, not of the current design.**
  Andrew's ratified phrase is *"the two-axis state model"* (batch 5, verbatim). A third orthogonal
  field neither collapses the two ratified axes nor removes either, so the ruling **stands** — but
  from this document forward, any artifact still calling the design "the two-axis model" without
  qualification diverges from what it now renders. This document is the one that adds the third axis,
  so it names the tension here rather than leaving a future reader to discover a silent contradiction
  between "two-axis" and a table with three columns of state.
- **`C-WEBSITE-BLIND`'s own wording says the Website row "renders BLIND."** This document renders it
  `DENY-BY-DESIGN` (§4), reading that constraint's word "BLIND" as naming the **family** (not-`CHECKED`
  — the row is not `OK`, ever) rather than the literal ratified value `BLIND`, because the constraint's
  substantive content — permanent, reason attached, not pending, does not wait on `TO-OP-S-13` — is
  exactly what `DENY-BY-DESIGN` means and `BLIND` (unqualified) does not carry permanence at all. This
  is the reading the cell's own text directs ("THE WEBSITE SECURITY ROW RENDERS `DENY-BY-DESIGN` WITH
  ITS REASON ATTACHED"), so it is applied here as a resolution, not left as an open choice. If a later
  reader of `C-WEBSITE-BLIND` alone concludes the PRD intends the literal value `BLIND`, that reader
  should file a surprise ROW rather than silently re-choosing — this document is not that ROW because
  the cell that owns this build already named the resolution.

## 7. Specimen rendered rows — the legibility test

A reader who knows nothing about how this report is built should be able to tell **"we have no way of
seeing this"** apart from **"we looked, and here is how bad it is"** from the row alone, no legend
required beyond this document. Four specimens, spanning the family:

| Row | Axis 1 | Axis 2 | 3rd axis (shown only if not `applied`) | Reads as |
|---|---|---|---|---|
| Website security (§4) | `DENY-BY-DESIGN` | — | — | **"We have no way of seeing this, permanently, by design — here is why."** Never confusable with a found problem; never confusable with `OK`. |
| Blocked-address sentinel row (§5) | `CHECKED` | `OK`/`DEGRADED` (whatever is actually observed) | `desired` | **"We looked, we see this address, but the block itself is only INTENDED — nothing enforces it yet."** Never confusable with an applied control. |
| `opal-login-abuse-alerts` (ruling 12's own worked example) | `INERT` | — | — | **"A control exists here but it cannot fire — it is not silently `OK`, and it is not `RED` either."** |
| `comp` (ruling 12's own worked example) | `CHECKED` | `OK` (carrying a stale-instrument qualifier) | — (fully applied) | **"We looked, the result is trustworthy but the instrument itself is stale — this is a found, contained state, not a blind spot."** |

The first row and the third row both answer "we have no way of seeing this" (permanently-by-design vs.
control-exists-but-cannot-fire — two DIFFERENT reasons, never collapsed into one value). The second and
fourth both answer "we looked" — one with an attached DESIRED-not-APPLIED caveat, one without. No row
in this table is green (`CHECKED`+`OK` with nothing else attached) except the fourth, and the fourth
says so by carrying no third-axis text at all.

## 8. What this document does NOT do

- Does not edit, remove or redefine any of the six ratified Axis-1 values (bound, §1).
- Does not build a `resolvable` field for Gap 1 (bound, §4) — YAGNI: `DENY-BY-DESIGN` already carries it.
- Does not mint a synonym for `desired | applied | exercised` (bound, §5) — adopted verbatim from
  CLAUDE.md rule 22.
- Does not cite `comp-iam` as evidence about the sentinel's `wafv2` enforcement path (battery finding,
  §5) — `comp-iam` does not model `wafv2` and its silence is never an ALLOW.
- Does not treat the Website row as pending or awaiting `TO-OP-S-13` (bound, §4/§6).
- Does not amend ruling 12: the third axis is orthogonal, adds no value to either ratified enum, and
  cannot make `BREACH` or `OK` printable on a surface nobody looked at.
