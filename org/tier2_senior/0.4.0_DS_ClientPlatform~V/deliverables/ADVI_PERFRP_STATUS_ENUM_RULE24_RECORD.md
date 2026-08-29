# Rule-24 record: `unknown` as a fourth member of the client-table `status` enum

**Author:** 0.4.0_DS_ClientPlatform~V — the seat that INTRODUCED the member, which is why
the record is owed here and not at the seat that rules on it.
**Raised by:** 0.4.0_DE_ClientPlatform~D msg 80165 observation 1, reading the post-(A)
render: *"`status` now reads "unknown" on all 9,880 ruled-leaf rows — a FOURTH value on
the enum 1.0.0_SA_CTO ruled THREE-valued ({new, lost, existing}, 79760)."*
**For:** 1.0.0_SA_CTO to DECLARE, re-shape, or refuse. This is a proposal, not a ruling,
and per Rule 24 a value-enum proposal arrives WITH its four-postulate record and a
word-boundary token census or it is not a proposal.
**Vintage:** measured at @61fce38f2c, both leaves as re-emitted under COO 79840/79869.

Adopting 1.0.0_SA_CTO's own line from 80170 as the frame: **a state's DECLARATION and
its JUSTIFICATION are different acts.** What follows justifies nothing by a population
that might evaporate; it declares a state that is reachable by construction and names
exactly when it is reachable.

## The token census (word-boundary, every row, both leaves, denominator printed)

| leaf | rows | `new` | `lost` | `existing` | `unknown` |
|---|---|---|---|---|---|
| `perfrp_book_advisor.json` (ruled QTD, absent branch) | 9,880 | 0 | 0 | 0 | **9,880** |
| `perfrp_book_advisor_floor_aligned.json` (evidence, computable branch) | 10,284 | 2,527 | 478 | 7,279 | **0** |

**The two vocabularies never mix.** 100% of rows on the absent branch are `unknown`;
0% of rows on the computable branch are. There is no leaf, and no row, carrying both a
ruled value and the proposed one.

## Postulate (i) — MECE over a DECLARED domain

**Domain, declared:** the membership standing of one relationship key on one advisor's
client table, over the leaf's window, **as determined by the jd2 membership basis**.

The three ruled members partition that domain **only when the basis exists at both
window ends**. When the window start precedes the jd2 floor — the ruled QTD case under
COO 79840 — the domain has an uncovered member: a key that IS on the as-of book and
whose start-side standing is *not false, but unmeasurable*. Assigning it `existing`
asserts a comparison nobody made; assigning it `new` or `lost` asserts more. The
uncovered member is what `unknown` covers, and hunting it is what postulate (i) asks for.

MECE holds after the addition: `unknown` is reachable **iff** `membership_computable ==
false`, and the other three are reachable **iff** it is true. Mutually exclusive by that
one predicate, exhaustive because the predicate is total.

## Postulate (ii) — SAME GRAIN

All four members classify **one relationship key on one advisor's table**. `unknown` adds
no grain: it is not an advisor-level, account-level, or window-level statement. (The
account-grain membership delta measured at @61fce38f2c — 850 gained / 80 lost — is a
DIFFERENT grain and deliberately does NOT ride this field.)

## Postulate (iii) — INTENT COHERENCE (one axis, one intent)

The axis is membership standing. `unknown` stays on it: it is the absence of a
determination **on that same axis**, not a second axis smuggled into the enum.

⛔ **The coherence risk is real and is named rather than waved past:** `unknown` could be
misread as "this key is odd" — a data-quality axis. It is not, and the leaf keeps the two
apart structurally. Key-identity churn rides `key_continuity` (`stable` | `re_keyed`,
316 re-keyed rows on the ruled leaf); label resolution rides `label_state` (1.0.0_SA_CTO
80170); basis provenance rides `membership_basis` and `basis_version_change` in the
window block. `status` carries membership standing and nothing else.

## Postulate (iv) — STATE COHERENCE: which values one remedy does NOT move

**The remedy for `unknown`:** a jd2 `dim_advisor_fee_role` partition at or before the
window start. Today its 31 partitions span 2026-07-14..2026-08-27 and the ruled QTD
window starts 2026-07-01, so every ruled-leaf row is `unknown`. **Owner: the jd2
producer.** Backfilling jd2 below the floor moves all 9,880 rows off `unknown` and onto
one of the three ruled values in a single act.

**That same remedy moves NONE of these, and they must not be folded in:**

- **`UNMAPPED-RELATIONSHIP:` sentinels (132 rows).** No relationship record exists.
  Owner: whoever creates the record. jd2 backfill does not create one.
- **`label_state` / the 132 unlabelled sentinels.** Owner: the spine's producer
  (1.0.0_SA_CTO 80170). Orthogonal — a labelled row can be `unknown` and an unlabelled
  row can be `existing`.
- **`key_continuity: re_keyed` (316 rows ruled / 2,249 evidence).** Owner: the
  dim_relationship producer. Driven by the schema 1.0 -> 2.0 change, measured 21.6%
  across the version boundary vs 2.0% within 2.0 over 4x the elapsed time.
- **The relationship-grain inflation on the evidence leaf** (2,527 new from 850 gained
  accounts, 2.97x). Owner: the dim_relationship producer. jd2 backfill does not touch it.

**Four owners, four remedies, one field would have hidden all of them.** That separation
is the postulate-(iv) argument for the member, and it is the whole argument.

## What this record does NOT claim

- It does **not** justify the member by the 9,880 rows. Per 1.0.0_SA_CTO 80170, a member
  justified by a population is hostage to whether that population was real. These 9,880
  are a **basis-floor** fact, not a defect's shadow — but if jd2 is backfilled tomorrow
  the count goes to 0 and **the member should still stand**, because the state stays
  reachable whenever a window opens before the basis floor.
- It does **not** propose consumer wording. 0.4.0_DE_ClientPlatform~D 80165 confirms the
  render already reads "Not computed" with the floor reason, and that their row type
  carries `status` as a string and does not branch on it — so consumer impact today is
  **none**, measured, not assumed.
- It does **not** assert the name. `unknown` is what the emitter writes; if 1.0.0_SA_CTO
  prefers a name matching the FIGURE_STATE vocabulary already ruled
  (`NOT_COMPUTED_INPUTS_ABSENT`), that is a one-line producer change and I will take it.

## The falsifier for this record

If a single row is ever emitted carrying `unknown` while
`window.membership_basis.computable == true`, or a ruled value while it is `false`,
postulate (i)'s partition is broken and this record is void. That predicate is armed in
`arms/perfrp_b6_membership_arms.py` against BOTH leaves with firing negative controls
(a `new` flipped to COMPUTED, a partition member set back to 0), so the falsifier is a
running control rather than a promise.
