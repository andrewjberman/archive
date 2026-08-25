# ADVI_INSURE — THE GOLD BUILDER, DESIGN SPEC v1

**seat:** `0.4.0_DS_ClientPlatform~J` · **issuer:** `2.0.0_SA_COO` (71625, 2026-08-25 ~22:50Z)
**cells:** `INS-c-1`, `INS-c-2` (DESIGN layer) · **criterion:** `INSR1DS-AC2` DESIGN limb
**input:** `0.6.0_AE_PartnerETL`'s field→call map @`b2514ec61a`
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`, AT EVERY RELAY** (PRD s.3).

⛔ **DESIGN AND RECORD ONLY.** No code is authored here, no bytes are written, and **no
`UNCOMPUTABLE` row is upgraded.** A field→call map is a **SOURCE-layer** input; `AC1`/`AC2`/`AC3`/`AC4`
are gated at the **APPLIED** layer and the map does not touch them. This document extends the AC2
design already accepted at 70569; it does not re-mint it.

---

## 0. THE ANSWER THE ISSUER ASKED FOR

The issuer asked whether the design can be honestly specified against 6-of-10 fields, and said a "no"
would be a complete answer.

**It is a YES — but "6 of 10 fields" is the wrong axis, and on the right axis the answer is 4 of 6
with two named holes.** ⛔ **Counting FIELDS hides the finding: the three ABSENT items are not the
same KIND of thing.**

| ABSENT item | what it actually is | consequence if you count it as "a field" |
|---|---|---|
| `carrier` | a **COLUMN** | correctly deferrable — the table is well-defined without it |
| `product` | a **COLUMN** | same |
| **cohort membership** | ⛔ **THE ROW SET** | **NOT a column. It is the predicate that decides which rows EXIST.** |

**A table missing two columns is a table. A table with no row-selection predicate is not yet a
table.** Field-counting puts all three in one bucket at "3 ABSENT of 10" and makes the gap look
uniform. It is not.

**THE DESIGN BY DIMENSION — the axis that actually governs whether a builder can be specified:**

| # | design dimension | specifiable now? | basis |
|---|---|---|---|
| 1 | **column set / types** | ✅ **YES** | 6 measured + 2 explicitly-absent, declared |
| 2 | **spine joins** | ✅ **YES** | measured leg by leg; advisor leg already ruled absent |
| 3 | **partition grammar + storage** | ✅ **YES** | Ruling 1 + the accepted AC2 design |
| 4 | **normalization / collision contract** | ✅ **YES — and the map made this MORE specifiable, not less** | map §5(a)(b), measured |
| 5 | **row-selection predicate** | ⛔ **NO — authority named, mechanism unknown** | S1 is PROSE-ONLY, zero captures |
| 6 | **advance predicate** | ⚠ **BOUND BY RULING, PREMISE UNTESTED** | see s.4 |

**4 of 6 dimensions are fully specifiable. One has a named hole. One is bound by ruling with an
untested premise.** That is a real design, not a stub — and it is honest about where it stops.

---

## 1. THE COLUMN CONTRACT

**Grain (unchanged from the accepted design): one row per (`bd_account_id`, `as_of_date`).** Additive;
a new row only when `as_of_date` advances (Ruling 7); a value change on a **closed** `as_of_date` is a
**CONFLICT — refuse loudly, never rewrite.**

**Location (unchanged): `{49F-gold-bucket}/gold/advi/insurance/insurance_nav_current/date={D}/`** — its
own subtree, deliberately not under `canonical/`, so never-blend holds **by construction** rather than
by discipline.

| column | source | basis | note |
|---|---|---|---|
| `bd_account_id` | S3 `accounts[].id` | `MEASURED` | the gold key (Ruling 3) |
| `account_number` | S3 `accounts[].accountNumber` **unmasked** | `MEASURED` | the Ruling-2 join key. ⛔ **NOT sourceable from S5** — see s.3 |
| `current_emv` | S3 `accounts[].currentEmv.emv` | `MEASURED` | the NAV |
| `as_of_date` | S3 `accounts[].asOfDate` | `MEASURED` | partition + advance key; premise s.4 |
| `relationship_id` | S3 nesting (account under its relationship row) | `MEASURED` | spine leg 1 |
| `firm_id` | S4 `financialTeam[]` / S3 `teams[]` | `MEASURED` | spine leg 3; constant on this tree |
| `advisor_id` | — | ⛔ `NOT-DERIVABLE-UPSTREAM` | ruled 70462; **never name-joined** |
| `carrier` | — | ⛔ `UNOBSERVED-CONTAINER` | **column EXISTS and is NULL.** Deferred per 71625 |
| `product` | — | ⛔ `UNOBSERVED-CONTAINER` | same |
| `spine_class` | derived | — | `linked` \| `unassigned`; **an unresolved row is NEVER dropped** |
| `{attr}_basis` | derived | — | the axis in s.2 |

⛔ **`carrier` AND `product` ARE PRESENT-AND-NULL, NOT OMITTED, AND NO SHAPE IS INVENTED FOR THEM.**
Per the issuer: *named and counted, NOT dropped and NOT assumed.* **I have not guessed their type,
cardinality, or nesting** — the container they are presumed to live in has been observed exactly once,
empty, one specimen estate-wide. **The v1 field list rests on a shape nobody has seen, and this design
declines to invent it.**

---

## 2. ⛔ RULE 24 AUTHORING ACT — the `{attr}_basis` axis, four-postulate record

The accepted design already carries `advisor_basis = 'NOT-DERIVABLE-UPSTREAM'`. This spec needs the
same statement for `carrier`/`product`. **Rather than mint three parallel ad-hoc fields, ONE axis is
declared and reused per attribute** — a consolidation, which is the sanctioned shape.

**DECLARED DOMAIN:** *for each v1 attribute the gold row carries, why it is or is not populated.*
⛔ **GRAIN: ATTRIBUTE-level (a property of the COLUMN), never ROW-level.** A row-level null is a
*value condition*, not a basis — collapsing the two is exactly the 24(ii) grain slip.

| value | meaning | remedy that moves it |
|---|---|---|
| `MEASURED` | populated from a field observed in captured vendor bytes | none — terminal |
| `AWAITING-FIRST-RUN` | supplying call AND its response shape are known; no run has happened | **a scheduled run** |
| `UNOBSERVED-CONTAINER` | a call names the field, but its populated shape has never been observed | **one populated specimen** |
| `NOT-DERIVABLE-UPSTREAM` | no upstream field carries it under any name | ⛔ **vendor-side CONFIG change** |

- **(i) MECE over the declared domain.** *Exclusivity:* `NOT-DERIVABLE-UPSTREAM` (no field exists) vs
  `UNOBSERVED-CONTAINER` (field named, shape unseen) vs `AWAITING-FIRST-RUN` (shape known, no run)
  are pairwise disjoint on two independent tests — *does a field exist?* and *has its shape been
  observed?* *Coverage:* an attribute is populated (`MEASURED`) or not; if not, exactly one of the
  three failure modes holds. **Hunted for an uncovered member: "field exists, shape known, run
  happened, still null" — that is a ROW-level value condition and is OUT of this axis's domain by
  the grain clause, not an uncovered member.**
- **(ii) SAME GRAIN.** Every value is attribute-level. No row-level or cohort-level value sits beside them.
- **(iii) INTENT COHERENCE.** One intent: *derivability*. It does **not** encode handling policy
  (never-drop is `spine_class`'s job) and does **not** encode data quality.
- **(iv) STATE COHERENCE — ⛔ AND THE VALUES DO NOT MOVE TOGETHER, WHICH IS THE POINT.**
  **`NOT-DERIVABLE-UPSTREAM` IS THE VALUE THAT DOES NOT MOVE.** A populated specimen clears
  `UNOBSERVED-CONTAINER`; a scheduled run clears `AWAITING-FIRST-RUN`; **neither one ever clears
  `NOT-DERIVABLE-UPSTREAM`, because its remedy is a change in Black Diamond's own template
  configuration** (dim 436 / template 390224) — outside this estate entirely.
  ⛔ **So the obvious instrument — get the vendor-egress word and run the calls — DELIVERS TWO OF
  THE FOUR AND STRUCTURALLY CANNOT DELIVER THE THIRD.** Naming that is the postulate's requirement,
  and it matters here: **a reader who sees the egress grant land will reasonably expect `advisor_id`
  to fill, and it will not.**

**TOKEN-HYGIENE CENSUS** (word-boundary, case-insensitive, over the ADVI_INSURE canon set —
`docs/architecture` + this seat's deliverables + the decomp run):
```
NOT-DERIVABLE-UPSTREAM   6 files  <- ALREADY RATIFIED; REUSED, not re-coined (build-ladder rung 2)
UNOBSERVED-CONTAINER     0 files  <- clean mint
AWAITING-FIRST-RUN       0 files  <- clean mint
attr_basis               0 files  <- clean mint
advisor_basis            2 files  <- existing; PRESERVED, now drawing from this shared value set
spine_class              4 files  <- existing, untouched (different axis: handling, not derivability)
POSITIVE CONTROL  insurance_nav_current  7 files (fires)
NEGATIVE CONTROL  zzz_no_such_token_qqq  0 files (fires)
```

---

## 3. THE JOIN KEY — specifiable in shape, and the map's §2 hazard is carried forward

The Ruling-2 join is **on account number**. The map measured it **unmasked on S3** — so the column is
specifiable. ⛔ **But the surface currently inside the vehicle's egress envelope (S5) returns
`XXXX5115`, a masked last-4, and accepts no exact-number filter.** The full number lives on S2, a
separate gated egress surface.

**Design consequence, stated so nobody discovers it at build time:** this builder's join key is
**sourceable only from S3/S2, never from S5.** A builder pointed at S5 would receive a well-formed
masked string and **join on it silently**, producing a plausible row count against the wrong keys.
**This is a correctness dependency on the egress grant, not merely an enrichment one** — which is the
wider form the issuer has already put to Andrew (71625), and I am not re-routing it.

---

## 4. THE ADVANCE PREDICATE — bound by ruling, premise untested, and it SPLITS ACROSS TWO LANES

The map's §5(c) raises that one record carries **four** dates (`asOfDate` 2026-07-07, `dataAsOfDate`
2026-06-23, `startDate` 2026-06-23, `modifiedDate` 2026-07-08) and says which is the statement date is
undetermined. **That hazard is real, but for THIS builder it is smaller than it reads, and the reason
is a lane boundary:**

| use | governed by | lane | status |
|---|---|---|---|
| **gold row advances** | Ruling 7 — *"a new gold row only when `asOfDate` advances"* | **MINE** | ✅ **BOUND — the ruling names the FIELD** |
| **client string** *"statement as of MM/DD"* | Ruling 5 | ⛔ **surface (e), FRONTEND — NOT MINE** | ⚠ semantic question lives here |

**So my design CAN specify the advance predicate: `as_of_date` ← S3 `asOfDate`, per Ruling 7's own
words.** What is untested is the **semantic premise** that `asOfDate` *is* the statement date — and
that premise is load-bearing for the frontend's client-facing string, not for my partition key.

⭐ **ONE PIECE OF CORROBORATION, WITH ITS DENOMINATOR, offered as weak evidence and not as a finding:**
on the single observed specimen, **`currentEmv.asOf` (2026-07-07) EQUALS `asOfDate` (2026-07-07)**,
while `dataAsOfDate`/`startDate` (2026-06-23) and `modifiedDate` (2026-07-08) do not. **The VALUE's own
as-of agrees with `asOfDate`** — which is the agreement a NAV snapshot's advance key should show.
⛔ **n = 1. One specimen, estate-wide, and it is Cottonwood's.** That is a reason to prefer `asOfDate`,
**not** a reason to consider the question closed. I am not upgrading it and not routing it as resolved.

⛔ **CARRIED FORWARD, NOT ABSORBED:** the frontend lane inherits the live half of this question. Per
`INS-a-3` discipline I am naming the surface rather than generalising — **the gold advance key is
bound; the display semantics are not, and they are another lane's cell.**

---

## 5. THE NORMALIZATION CONTRACT — where the map made the design STRONGER

The map's §5 hazards are **measured**, and they let the silver→gold contract be specified precisely
instead of defensively. ⛔ **All three are silent-failure shapes: each returns a well-formed wrong
answer rather than raising.**

| hazard | measured | contract |
|---|---|---|
| **(a) case-variant keys** | `dataFormatID`/`dataFormatId`, `custodianID`/`custodianId` differ **by surface** | resolve keys **case-insensitively at the silver boundary**; a key resolving to `None` **raises**, never defaults. A parser keyed on one spelling returns `None` against the other **and does not raise** |
| **(b) type divergence** | `taxStatus` = `1` (int) on S3, `"Taxable"` (str) on S2 — same key, same account | Rule 17 silver standardises dtype and **will be handed both**. The contract declares the target dtype per column and **refuses on an unmapped variant** rather than coercing |
| **(c) four dates** | see s.4 | `as_of_date` binds to `asOfDate` only; the other three are **carried as-is** (Rule 17: no slimming), never substituted |

⛔ **AND ONE INHERITED DISCIPLINE FROM THE MAP'S §6, WHICH IS NOT A DESIGN ITEM BUT WILL BITE THE
BUILD: RESOLVE PAYLOADS BY `url`, NEVER BY FILENAME.** The estate's `account_detail_search.json`
actually contains a `RelationshipAccountDetailSearch` response. **Resolving by name returns a clean,
well-formed, 200-status response to a question you did not ask** — Rule 22a's "never by filename",
generalised past code.

---

## 6. ⛔ THE HOLE — the row-selection predicate

**The one dimension this design cannot close, stated plainly rather than papered over.**

**Ruling 2 makes S1 (`insurancerelationshiplist`) the cohort authority.** The map grounds S1 as
**PROSE-ONLY: no payload capture, no response shape, no field list anywhere in the estate.**

| specifiable | ⛔ NOT specifiable |
|---|---|
| the **AUTHORITY**: a row exists for an account iff S1's export lists it in the insurance cohort | the **MECHANISM**: which field carries the list, what the membership predicate is, what the response nests |

**The table's grain is well-defined; its row SET is not.** ⛔ **AND THE FAILURE MODE IF SOMEONE FILLS
THIS BY INFERENCE IS SILENT:** the obvious substitute — *"treat every account S3 returns as insurance"* —
would build a table whose row set is **whatever the relationship query happened to page**, producing a
plausible, non-empty, correctly-typed gold table **of the wrong population.** Every figure above it
would inherit that silently. **`INS-inv-1`'s byte-identity control would NOT catch it**, because that
control watches existing AM figures, not this table's membership.

**DEPENDENCY NAMED: one S1 export run.** Not mine, not chased.

---

## 7. WHAT THIS DOES **NOT** DO

- ⛔ **No `UNCOMPUTABLE` row is upgraded.** `AC1`/`AC2`/`AC3`/`AC4` remain exactly as ruled. A
  SOURCE-layer map cannot move an APPLIED-layer criterion, and treating it as if it could is the
  grain error this whole TO has been policing.
- ⛔ **No code authored.** Design and record only, per 71625.
- ⛔ **No shape invented for `carrier`/`product`.**
- ⛔ **No vendor call.** None was made or attempted at this seat.
- **No re-derivation of the map's method.** Its denominators and controls stand; I read its
  conclusions as a peer's published invocation, and re-derived only what my own design rests on.

## 8. WHAT WOULD CLOSE EACH REMAINING ITEM — and they take THREE DIFFERENT REMEDIES

| item | remedy | needs Andrew's egress word? |
|---|---|---|
| `carrier`, `product` | one **populated** `insuranceCharacteristics` specimen (S2) | **YES** |
| row-selection mechanism | one **S1 export run** | **YES** |
| statement-date semantics (frontend's half) | an S1/S2 response **OR a Ruling-7/5 clarification** | ⭐ **NO — the clarification path needs no vendor call** |
| `advisor_id` | ⛔ **Black Diamond template config (dim 436 / template 390224)** | **NO — and the egress grant will NOT fix it** |

⛔ **THE LAST TWO ROWS ARE THE ONES A READER WILL GET WRONG.** The egress grant is being read as the
single unblocker; it is not. **One item is closable tonight with no vendor call at all, and one item
will still be open after the grant lands.** *(Both stated as reads for the issuer, who owns the
routing. I am not routing either.)*
