# AMGT_HARVST ROUND 9 -- DRAIN-END PACKET, `2.0.0_SA_COO~Y`, 2026-09-28 ~06:2xZ

**For `3.0.0_SA_CVO~O`** under `1.0.0_SA_CTO~Z`'s STANDING ROUTE (20260928T054653Z): every AMGT_HARVST round's
drain-end packet and L9 material goes to `~O` without asking per round, until `3.0.0_SA_CVO~Z` is re-seated.

## 1. WHAT WAS ISSUED AND WHAT LANDED

Both issued cells are **`complete`**, both instances **VALID (rc=0)**, drained `4d2b5d7615` and `8ac166b569`.

| cell | class | result |
|---|---|---|
| `HVST-x-1` -- the `.json()` guard, the completable test, one quarantine | LOCAL | `complete`, 3 of 3 PASS |
| `HVST-x-2` -- exercise the timeline on real landed gold | LOCAL | `complete`, 2 mechanical PASS + 1 JUDGMENT presented |
| `w-2`, `w-4`, `w-5` | WORLD | **still CARDED at Andrew**; each fires only on his live per-use word |
| item 6 (the carried rows) | -- | ISSUER act, discharged as evidence in the issuance commit @`402a3414c7` |

⭐ **NEITHER INSTANCE NEEDED AN ISSUER REPAIR.** Round 8 spent three attempts on an instance filename, a
`to_id` and an artifact pin. Those became standing clauses at decomp `s.14x`, both workers were told them in
the worker face, and **both validated first time.** The clause paid for itself in the round after it was
written.

## 2. WHAT THE CELLS MEASURED -- their own outputs

**`HVST-x-1`:**
- **AC1** -- the guard shown DIRECTLY, never through the suite: `AttributeError` pre-fix, `AuthExpired`
  post-fix on the SAME input, **and both positive controls hold** (a valid logged-in body still passes; a
  logged-out body still raises `AuthExpired`). 4 of 4 sub-outcomes.
- **AC2** -- `3 failed, 306 passed` -> **`306 passed, 1 skipped`.** The passed count **HELD at 306**, which
  was the discriminator written into the criterion against tests being deleted rather than fixed.
- **AC3** -- the quarantine is visible and its reason prints verbatim in `-rA`; `1 failed, 3 passed` ->
  `3 passed, 1 skipped`.

⭐ **MY OWN CLOSE-VERIFICATION ADDED WHAT THE COUNT PAIR COULD NOT** (rule 22): `pytest -k dow_jones` reports
that test **PRESENT AND PASSING**, 1 passed / 17 deselected. **A test that had been silenced would also have
left `306 passed` standing** -- only the targeted run separates "fixed" from "skipped."

**`HVST-x-2`:**
- **AC1** -- the census, with the security keys round 7 never named: **191** securities carry `chatter_daily`,
  **55 of 191** have a day with `articles_total > 0`, **12 `chatter_event` rows across 7 securities**,
  `publishers_distinct` max **3**.
- **AC2** -- **FWD-5 EXERCISED on Lenovo** (`992_HK_Equity`, the spec's own acceptance security): **267 of 267
  dense days with NO gap**, day `2026-05-22` opening strongest-first (tier A, A, B), **0 pairwise sort
  violations**, every field present including `mention_in_title`/`mention_in_lead` when false.
- **AC4** -- JUDGMENT, **PRESENTED with NO verdict**, `UNVERIFIABLE-BY-INSTRUMENT`, `status_reason` naming
  `3.0.0_SA_CVO` at L9. All 12 events with spans, `lead_headline`, counts and member headlines.

## 3. THE ONE THING I ASK YOU TO LOOK AT FIRST

⚠ Lenovo's 4 events include a clean earnings cluster (`2026-02-12`, *"Lenovo Posts Earnings Beat on AI-Driven
Demand"*, 2 tier-A articles / 2 publishers) **and one whose `lead_headline` is carried VERBATIM across
`992_HK_Equity`, `DELL`, `MSFT` and `NVDA` on the same day** -- *"Nvidia Introduces First PCs Designed for AI
Agents"*. **Whether a headline naming a different company is the right lead for Lenovo's own event is exactly
what `C-HV-EVENT-SPINE` cannot settle mechanically.** The mechanical column is green either way. **That is
AC4's question and it is yours.**

## 4. ROWS -- two new, both ARMED; evidence mine, clock yours

- **`Z-W26-S1`** -- `patch("lib.opal_data_harvest.publishers.DowJones", ...)` **NEVER TOOK EFFECT.** pytest's
  rootdir import (no `lib/__init__.py`) loads the test as `opal_data_harvest.test_worker`, so the code under
  test resolves `DowJones` off a **different module object** than the string-targeted patch mutates -- it
  silently no-ops. **`test_worker.py:51` only "works" by a stdlib-singleton coincidence**;
  `test_verification.py:11` carries the identical shape. **NOT REMEDIED** -- `x-1` routed around it with
  `patch.object` on the class its own file imports. **The disarm scope is a repo-wide audit of every
  `patch("lib....")` string target, which is larger than this project.**
- **`Z-W27-S1`** -- the stale-premise finding. **REMEDIED as to the records** (@`635f79990f`, @`fce7683458`).

**Carried and still ARMED from earlier rounds:** `Z-W22-S2` (one Timeout cools a whole publisher) and `Z-S32`
(bbg `search/query` in hard refusal). **Remedied earlier and already evidenced to you:** `Z-W9-S1` listings
half, `Z-S27`, `Z-W11-S1`, `Z-W23-S1`.

## 5. WHAT I GOT WRONG THIS ROUND -- twice, in opposite directions

1. ⛔ **"FWD-6 is unsatisfiable by construction" was FALSE.** `x-2`'s AC1 disproved it; I re-verified rather
   than accept the worker's word on what refutes me. **`EVENT_MIN_PUBLISHERS = 2` I read at the bytes; *"only
   `sa` has landed"* I INHERITED from round 7's measurement of a different population at an older vintage; and
   I never read `chatter_event` at all.** Labelling that pair with the measured constant's authority is how an
   inherited number acquires standing it never earned. **A conclusion is only as measured as its weakest
   premise.** Marked FALSE in place on all four bytes that carried it.
2. ⛔ **Then I OVERSTATED its spread.** My correction said the round-8 analysis "quoted" the claim. **It did
   not** -- verified, zero hits; its s.4 graded FWD-5/6 NOT REALIZED for a different and correct reason.
   **Inflating the blast radius is the same carelessness as understating it, and it put a false statement about
   a peer's document into my record** -- worse than the original, which was only about data. Corrected
   @`fce7683458`.

## 6. WHAT THIS PACKET DOES NOT DO

It does not grade AC4 -- that is yours at L9, and a judgment criterion is never self-graded. It does not claim
FWD-5 REALIZED: the cell exercised it, and **whether that realizes the outcome is `1.0.0_SA_CTO`'s grade at
L10.** It does not compile the channel, disarm a row, cut round 10, or grant a vendor word.
