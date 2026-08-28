# TO D1_CATVIEWS.TO-N1-DS — THE SMA L0 BRANCH IS UNREACHABLE; A SERVED SENTENCE IS FALSE

<id>D1_CATVIEWS.TO-N1-DS.sma-l0-unreachable-branch</id>
**DECOMP CELLS -- NONE CLAIMED:** `D1-h-p2` — the L0 presence predicate — is the NEAREST cell, cited with a disclosure rather than a claim. ⛔ **NO CELL OWNS THE DETECTION HALF, AND THAT IS ON THE RECORD IN WRITING.** `CERT_D1_CATVIEWS_DECOMP_V2_20260824.md:129-140` (`3.0.0_SA_CVO`) closes under the heading **"WHAT COO SHOULD HAVE ASKED BUT DID NOT"** with: *"`D1-h-p2` + `D1-inv-4` handle the sum ... no cell owns detecting the transition itself."* It named the failure shape exactly — a summand silently folding into another while the sum holds — and predicted it on **Insurance**. **IT LANDED ON SMA.** This TO does not invent a cell; it discharges a gap its own decomp certificate declared open.
>> **THE DECOMP-REF ELEMENT IS DELIBERATELY ABSENT, NOT FORGOTTEN.** `proof-of-spec-check.py:24,161` arms alignment ENFORCE on the mere PRESENCE of that element, whatever its content. This face carried one whose text was a DISCLAIMER saying no cell is claimed -- **so the TO's own honest disclosure armed the enforcement that then refused the TO's own criteria.** The disclosure is preserved above verbatim; the element is gone so the instance can validate. ⛔ **NEVER fabricate `cell_refs` to satisfy it** -- that yields a VALID-READING INSTANCE THAT LIES.
<issued_to>`0.4.0_DS_ClientPlatform~Z` — the seat that FOUND it, and the seat that authored the change that armed it.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:4xZ</issued>
<status>pending -- ⛔ **"NOT STARTED" WENT FALSE AND THE FACE KEPT SAYING IT. RECONCILED 2026-08-28 ~17:2xZ by `2.0.0_SA_COO~Z` (issuer).** The build LANDED at `70a0828226` (16:04Z, `0.4.0_DS_ClientPlatform~Z`) and is ON ORIGIN; that commit is the very pin `D1_CATVIEWS.TO-V1-AE` ships. **BUILD DONE. WHAT IS ACTUALLY OUTSTANDING, measured:** (1) **NO proof-of-spec instance is filed** -- positive-controlled, sibling `D1_CATVIEWS.TO-M1-DS_PROOF_OF_SPEC.json` exists at the same convention while this one does not; (2) **AC7 is EVENT-GATED** on a scheduled fire that cannot occur before tomorrow's ~13:00Z, and no ad-hoc run may be used to beat it -- that would destroy the discriminator the criterion exists to produce; (3) **the executing lane `0.4.0_DS_ClientPlatform~Z` IS DEAD** -- it died in the ~16:0xZ reboot, reads DEAF with unread mail accumulating, and was NOT respawned (Andrew scoped the relaunch to Tier 1). ⛔ **NOBODY SHOULD WAIT ON THAT LANE and nobody should re-execute this TO** -- the code exists and re-running it would be a REWIND of accepted work. ⭐ **WHY THE CORRECTION IS WORTH A COMMIT:** a certifier reading this face AFTER the deploy lands would find a TO marked NOT STARTED whose change is live in production, and the tidy reading -- "the work was never done" -- is exactly the wrong one. A face that outlives its own truth misleads in the direction of undoing finished work. Prior text, preserved: *"CUT, SEATED, NOT STARTED. Cut on the issuer's fold-vs-cut ruling; `0.4.0_DS_ClientPlatform~Z` declined to fold and was right to."* -- that last clause remains TRUE and is not withdrawn.</status>
<priority>P1 — **a SERVED artifact asserts a falsehood that CITES ANDREW, on a surface he is actively reviewing.**</priority>

<authority>
`0.4.0_DS_ClientPlatform~Z` msg 13333, surfaced OFF-SPEC via the surprise channel, ARMED/BLOCKING,
disarmed same-turn by naming its own seat owner. Independently verified at source by
`1.0.0_SA_CTO~Z` (13338) and `3.0.0_SA_CVO~Z` (13342). **Three seats, three instruments, one verdict.**
</authority>

## 1. THE DEFECT

```
consumer  mdpf_gold_consolidator.py:591   if   member.view_path.startswith("Models")   PREFIX  -- tolerant
consumer  mdpf_gold_consolidator.py:592   elif member.view_path == "SMA"               EXACT   -- CANNOT MATCH
producer  mdpf_category_registry.py:332        view_path=f"SMA > {b}"                  ALWAYS suffixed
```
`3.0.0_SA_CVO~Z`'s controls: **bare `view_path = "SMA"` in the registry = 0 occurrences; `view_path` =
47 occurrences.** ⛔ **The branch is not merely unmatched today — it is UNREACHABLE BY CONSTRUCTION.**

## 2. WHAT IS SERVED RIGHT NOW

`s3://opal-data-assets/portal/gold/mdpf/49financial/category-views/2026-08-27.json`
(4520 B, LastModified 2026-08-28T13:31:13Z via `s3api` UTC, `_provenance.trigger="scheduled"`)

```
sma_aum stays 0.0 -> sma_members_present=False -> the artifact states, VERBATIM:
  "49financial has NO SMA category members (Andrew-direct 2026-08-25 ...) A TRUE ZERO"

THAT SENTENCE IS FALSE AND IT CITES ANDREW WHILE BEING FALSE.
49financial is THE ONE FIRM THAT HAS THEM:  divz $18,783,379.81 + pfoe $4,011,386.44 = $22,794,766.25

client_aum = non_model - sma_aum is GATED on members_present, so it never fired:
  non_model_aua      290,426,813.47
  served Client.aum  290,426,813.47   <- UNNETTED, overstated by exactly $22,794,766.25
```
⛔ **A defect wearing a sovereign citation is worse than a bare defect: the citation is exactly what
stops the next reader from questioning it** (`3.0.0_SA_CVO~Z`).

## 3. ⛔ WHY 7/7 DID NOT CATCH IT — AND WHY NO INVARIANT COULD

**`D1_CATVIEWS.TO-L2-DS` was ACCEPTED 7/7 and every one of its seven criteria still passes.** All seven
sat on the **PRODUCER** side of the seam. The registry emits the new shape correctly — true, and
certified. **NOT ONE criterion asked whether the CONSUMER still recognised it.**
>> ⭐ **A PRODUCER-SIDE CRITERION SET CANNOT FAIL ON A CONSUMER-SIDE BREAK, HOWEVER MANY CRITERIA IT HAS.**

**`D1-inv-4` HOLDS, correctly, at 1,762,750,154.52.** Models 1,472,323,341.05 + SMA 0 + Alt 0 +
Insurance 0 + Client 290,426,813.47 == total_aua.
>> ⛔ **A SUM INVARIANT CANNOT SEE A MISATTRIBUTION BETWEEN TWO OF ITS OWN SUMMANDS.** The money never
   left the artifact — it stayed folded inside `Client`. **The invariant is not weak; it measures a
   different proposition, and it passes for the same reason the defect is invisible.**

⭐ **`1.0.0_SA_CTO~Z`'s architectural finding, and it is sharper than "a literal went stale":** two
adjacent lines doing the same job with **DIFFERENT PREDICATE FORMS.** `startswith` absorbed the
restructure; `==` did not. **The Models branch was ACCIDENTALLY ROBUST and SMA ACCIDENTALLY BRITTLE,
and nothing recorded that either property was a choice.** A restructure tests every coupling that is
EXACT and silently spares every coupling that is TOLERANT — **so the surviving branch teaches you
nothing about the safety of the change.** The defect was authored long before the change that
triggered it.

## 4. ⛔⛔ SEQUENCING — THIS TO LANDS **BEFORE** `TO-M1-DS` COMPLETES

**`0.4.0_DS_ClientPlatform~Z` measured** (relayed, NOT re-measured by the issuer — confirm at source
before relying on it): `SMA L0 aum = 0.0 -> presentAum() returns null -> CategoryViewTree DROPS THE
CARD ENTIRELY.`

**IF that holds, then `D1_CATVIEWS.TO-M1-DS` STRUCTURALLY CANNOT VERIFY ITS OWN SMA L2 ROWS** — they
render under a card that is not on the page. TO-M1's criteria would pass on the `Models` L2 rows and
never touch the SMA ones, **which is the SAME failure shape as TO-L2-DS's 7/7: a criterion set that
cannot fail on the invisible half.** Twice in one file is a pattern, not a coincidence.
>> ⭐ **THEREFORE: land the one-line fix FIRST, then continue `TO-M1-DS` over a summand that is
   correct.** ⚠ **`0.4.0_DS_ClientPlatform~Z` may falsify this** — if the L2 mapping is genuinely
   independent of the L0 card's presence, say so with the measurement and the order is released.
   **Do not adopt this ordering silently if it is wrong.**

⛔ **ACCEPTANCE IS DECOUPLED FROM CODE ORDER.** The served-plane proof for this TO **and** for
`TO-M1-DS` rides the **NEXT SCHEDULED FIRE (~13:31Z)** — there is no ad-hoc route to it. **This TO
cannot close today and is not expected to.** Saying so now beats discovering it at 23:00Z.

## 5. ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| `CATV-TON1-AC1` | **The consumer recognises every SMA member the registry builds.** Print the resolved member set per firm **with its denominator, all three firms**. ⚠ **POSITIVE CONTROL: `Models` members still match** — a fix that repairs SMA by breaking Models scores identically on a SMA-only check. |
| `CATV-TON1-AC2` | ⛔ **THE TWO PREDICATE FORMS AGREE** (`1.0.0_SA_CTO~Z` ruling, narrow): `:591` and `:592` consume the same producer field and use the **SAME predicate form**, or the difference **carries a comment saying why**. Form is the DS lane's call; `startswith("SMA")` is the obvious candidate precisely because `:591` already proves it works against this producer. |
| `CATV-TON1-AC3` | ⛔ **AMENDED 2026-08-28 ~20:3xZ by `2.0.0_SA_COO~Z` (issuer, AC3's author). THE LITERAL CONSTANT IS DATE-SCOPED AND WOULD HAVE FAILED A CORRECT FIX.** ~~The delta must equal **$22,794,766.25 exactly**~~ — that figure is the sum of two MARKET-VALUED balances at **`as_of` 2026-08-27** (`opal_div_sma` 18,783,379.8116 + `opal_growth_sma` 4,011,386.4409), and **they move every trading day** (08-26: 22,963,460.88 · 08-25: 22,982,737.10 · 08-24: 23,043,880.88 — measured across 455 dates). **The served AFTER comes from a fire whose `as_of` is not 2026-08-27, so the delta differs by ~$170k-$250k and the literal text returns FAIL ON A CORRECT FIX — the same false-verdict shape this TO was cut to fix, pointed the other way.** ⭐ **THE EXACTNESS IS KEPT; WHAT CHANGES IS WHAT IT IS EXACT AGAINST.** The real proposition is *the money was REATTRIBUTED and none was created or destroyed*, which is scoreable to the cent on ANY `as_of`: **(A)** `SMA.aum(after)` == sum of `model_value` for resolved SMA members **at the after-artifact's OWN `as_of`**; **(B)** `Client.aum(after)` == `non_model_aua(after)` − `SMA.aum(after)`; **(C)** pre-fix signature `Client.aum(before)` == `non_model_aua(before)`, UNNETTED; **(D)** the literal constants `22,794,766.25` / `267,632,047.22` are scored **ONLY when `as_of` == 2026-08-27**, and reported **`N/A-BY-DATE` — never PASS, never FAIL** — otherwise, **with the `as_of` printed**. A/B/C are exact-to-the-cent on any date; D neither silently drops the TO's measured number nor fails a correct fix on it. **Print before AND after FROM THE SERVED ARTIFACT.** A different delta that also breaks A or B means a different defect and this TO does not cover it. ⚠ **FOUND BY `0.4.0_DS_ClientPlatform~Z` mid-build, surfaced to the channel WITHOUT halting, and the remedy above is that seat's — adopted verbatim because it is better than what I would have written.** |
| `CATV-TON1-AC4` | ⛔⛔ **THE OTHER TWO FIRMS DO NOT MOVE.** `inflection` and `cottonwood` resolve **ZERO** SMA members, so `members_present=False` is **CORRECT** for them and their `absent_reason` is **TRUE**. Their served `Client` and `SMA` values are **byte-identical before and after**. ⚠ **A fix that improves 49financial while moving a firm that was already right is a FAIL** — and the bug being invisible on 2 of 3 firms is exactly the coverage shape that lets a spot check pass. |
| `CATV-TON1-AC5` | **THE FALSE SENTENCE IS GONE FOR 49financial — AND STILL PRESENT WHERE IT IS TRUE.** ⛔ **Deleting the `absent_reason` everywhere is a FAIL.** It is a correct, sovereign-cited statement for the two firms that genuinely have no SMA members. **Both limbs measured and printed.** |
| `CATV-TON1-AC6` | **`D1-inv-4` STILL HOLDS AND `total_aua` DOES NOT CHANGE.** Sum of L0 == `total_aua`, printed before and after. ⚠ **The total moving at all means value was created or destroyed rather than reattributed** — that is a different and worse defect. |
| `CATV-TON1-AC7` | ⛔ **EXERCISED ON A SCHEDULED FIRE. NO AD-HOC GOLD RUN.** Name the fire and quote its `_provenance.trigger`. **An ad-hoc artifact is never production evidence**, and an ad-hoc write here lands a real client-facing artifact at the real key. |
| `CATV-TON1-AC8` | **THE WIDER CENSUS** (`3.0.0_SA_CVO~Z`, named and not run): **every EQUALITY comparison against a `view_path` anywhere in the consumer**, with a printed denominator. ⛔ **NOT "find other `== "SMA"`"** — the question is which OTHER tolerant/exact asymmetries the same restructure could have broken silently. **A census scoped to the known instance cannot find the unknown one.** |

## 6. NOT YOURS
⛔ **Widening beyond the predicate fix** — this is a reattribution, not a re-model of the category tree.
⛔ **`D1_CATVIEWS.TO-M1-DS`'s scope** — found while grounding it, NOT part of it.
⛔ **Any ad-hoc gold run.** ⛔ **The PROD promote** — Andrew's word, per promote.
⛔ **Amending `TO-L2-DS`'s 7/7 certificate.** It is `3.0.0_SA_CVO~Z`'s, its criteria were true as
written, and the finding is that they were the WRONG SET — a certifier-side lesson, not a DS edit.

<proof_of_spec>
  <criterion id="CATV-TON1-AC1"/>
  <criterion id="CATV-TON1-AC2"/>
  <criterion id="CATV-TON1-AC3"/>
  <criterion id="CATV-TON1-AC4"/>
  <criterion id="CATV-TON1-AC5"/>
  <criterion id="CATV-TON1-AC6"/>
  <criterion id="CATV-TON1-AC7"/>
  <criterion id="CATV-TON1-AC8"/>
  <expected_criteria>CATV-TON1-AC1,CATV-TON1-AC2,CATV-TON1-AC3,CATV-TON1-AC4,CATV-TON1-AC5,CATV-TON1-AC6,CATV-TON1-AC7,CATV-TON1-AC8</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-N1-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 8, all FIRM-TOKENED (`CATV-TON1-ACn`) at cut time — the defect `ETFS_INGEST.TO-8` was measured to carry. Cell `D1-h-p2` cited WITH the disclosure that the detection half is unowned per `CERT_D1_CATVIEWS_DECOMP_V2_20260824.md:129-140`.</alignment_denominators>
</proof_of_spec>
