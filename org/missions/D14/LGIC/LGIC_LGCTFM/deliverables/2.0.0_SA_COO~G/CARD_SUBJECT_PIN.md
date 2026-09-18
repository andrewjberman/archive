# ANDREW_CARD.md -- WHICH RUN IT RANKS, PINNED BY CONTENT HASH

**Owner:** `2.0.0_SA_COO~G` (the LGIC_LGCTFM round-1 issuer)
**Written:** 2026-09-18T04:5xZ
**Why this file exists and is not a line in the card:** row `LGIC_LGCTFM-S12` (surfaced by
`3.0.0_SA_CVO`) measured that `ANDREW_CARD.md` names **no run at all** -- a regex for a run id over it
returns zero matches and its only self-identification is *"graph built 2026-09-17 18:16 UTC"*. The row's
named remedy was *one line in ANDREW_CARD.md*. **That remedy is one this seat is mechanically forbidden
to perform:** `.tools/owned-paths-validate.py` clause 4 (`ADHC_OWNPTH.004`) refuses an issuer's edit
inside a worker's deliverables folder, measured on that exact file. An issuer re-grade has no home inside
a worker's instance. So the pin lands **here, in this seat's own record, beside the card** -- which is the
restated reason recorded as row `LGIC_LGCTFM-S16`.

---

## THE SUBJECT

| field | value | instrument |
|---|---|---|
| card | `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~3/ANDREW_CARD.md` | path |
| run it ranks | `20260918T011619Z-8db9eb1` | the R-40 `HASHES.json` manifest, below |
| run home | `workflows/legacy_transform/blackdiamond-49financial/20260918T011619Z-8db9eb1/` | path |
| **contract content hash** | **`33204e29839de89af81fb293317cce3ccdf2266d`** | **`git hash-object`** |
| repo HEAD at the run | `8db9eb1bd9033804fd824981130e1bb4c3993be6` | the manifest's own `repo_head` |
| produced at | `2026-09-18T01:27:09Z` | the manifest's own `produced_at` |
| tensions in that contract | **179** | `len(json.loads(contract.json)["tensions"])` |

⭐ **THE INSTRUMENT IS PART OF THE VALUE, and leaving it out is the same defect one notch finer.** A plain
`sha1` of `contract.json`'s bytes reads `9c5cdb873f00a599bb00166831a91646fea97990` -- a DIFFERENT number
for the same file. The manifest declares its instrument (`"instrument": "git hash-object"`) and this
record repeats it. **A hash without its instrument is a number two readers can disagree about while both
being right**, which is row `LGIC_LGCTFM-S11`'s class applied to a hash instead of a count.

⛔ **CORRECTED 2026-09-18 ~09:0xZ -- THIS RECORD'S ORIGINAL EXPLANATION OF *WHY* THE TWO NUMBERS DIFFER
WAS HALF THE CAUSE, AND THE NUMBERS WERE NEVER WRONG.** It said, in this seat's own words, that the
difference is "because `git hash-object` prefixes `blob <len>\0` before hashing". That prefix is real and
it is not sufficient. **Measured, with the third number printed so the gap cannot be waved at:**

```
  checkout bytes                 790,871   of which CRLF pairs 24,967   (core.autocrlf=true)
  git hash-object                33204e29839de89af81fb293317cce3ccdf2266d   <- the published pin
  plain sha1 over the checkout   9c5cdb873f00a599bb00166831a91646fea97990
  PREFIX ALONE, no eol filter    d07bf29d245fd358fa15859b09a35aa8a3a2d5c3   <- what the OLD sentence predicts
  prefix AND eol-normalised      33204e29839de89af81fb293317cce3ccdf2266d   <- matches
```

**`git hash-object` RUNS THE EOL FILTER FIRST.** So the published hash is the id of the **COMMITTED**
bytes and the plain `sha1` was taken over the **CHECKOUT** bytes, and the prefix is only half the story.
A later seat re-deriving from the original sentence would have computed `d07bf29d...`, found it matched
nothing in any record, and concluded the PIN was wrong -- when the pin was right and the explanation was
short. Found by `0.9.0_WK_LGIC_LGCTFM~1` at cell `LT-c-2`'s run (row `LGIC_LGCTFM-W1-S22`) and
re-measured independently by this seat before this correction was written.

⚠ **THE SAME SENTENCE PROPAGATED TO FOUR CARRIERS**, because it was copied rather than re-derived:
`fixed_inputs/r2/R2_BASE.json`, this record, row `LGIC_LGCTFM-S19`, and through `LT-n-2`'s order into
`NUMBER_PINS_R2.json`'s 16 pins. **THE THREE FROZEN ONES ARE NOT REWRITTEN** -- R-43 does not falsify
frozen history, and every NUMBER in all four is correct. This is the live-direction carrier and it takes
the correction. **A value carrying its instrument is not the same as a value carrying a TRUE ACCOUNT of
that instrument**, and the second is what a re-derivation actually needs.

**VERIFIED, not restated:** `git hash-object <that contract.json>` returns
`33204e29839de89af81fb293317cce3ccdf2266d`, equal to the manifest's claim.

**NEGATIVE CONTROL, run deliberately, because a hash that matches proves nothing without one:** the same
instrument over the *other* candidate run's contract -- `20260918T002711Z-caf0983`, the one carrying 180
tensions -- returns `3ffedfed35c05a1820d594c85c2b416c0441aa0f`. Different file, different hash, same
instrument. So this pin DISCRIMINATES between the two runs a reader could confuse.

---

## WHY THE PIN WAS NEEDED AT ALL: five runs share one subject directory

```
  run directory                      tensions   contract (git hash-object)                  HASHES.json
  20260917T202556Z-bb29248              179     8ec3b09c...  (plain sha1 shown in S12's era)     no
  20260917T233115Z-a89fd61              179     -                                                no
  20260917T233143Z-a89fd61              179     -                                                no
  20260918T002711Z-caf0983              180     3ffedfed35c05a1820d594c85c2b416c0441aa0f         no
  20260918T011619Z-8db9eb1  <- GRADED   179     33204e29839de89af81fb293317cce3ccdf2266d        YES
  ------------------------------------------------------------------------------------------------
  run directories under the subject: 5;  carrying an R-40 HASHES.json: 1
```

⛔ **EXACTLY ONE run carries the manifest, and that is what makes "the graded run" a measurement rather
than a position.** `check_lt_r1.py`'s `graded_run()` selects on that property and REFUSES when the count
is not 1, printing both numbers. Before R-40 landed, the graded run was selected BY POSITION in this
directory -- and one of this seat's own arms (`x1_fwd10`) read a *different run's* file under a VINTAGE
claiming the earlier one. The five-run population above is precisely why.

**The card ranks a 179-row order, so it is not the 180-tension run** -- but S12's point stands
unrefuted: **nothing IN the card says so.** The only thing that had been separating it from a different
run in the same directory was that its order happened to be 179 rows long.

---

## THE CORRECTION THAT TRAVELS WITH THE CARD

Row `LGIC_LGCTFM-S6`: the card's **RECOMMENDATION** -- the one line a decision-maker actually weighs --
said *"the two rows touching a live, client-facing surface"* **and there is exactly ONE.** Measured over
all 179 tensions at the nested factor path `factors.<name>.value`: `client_facing == true` is **1**
(T-0001, the `opal-data-bd` bucket), `live == true` is **1** (T-0001), both together **1**,
`irreversible == true` is **0**.

The card's **TABLE** is correct and its analysis sentence is correct. **What was wrong is the summary
written for the reader who decides without checking**, which is exactly backwards from how a card is used.

**Adjudicated, not silently rewritten:** `1.0.0_SA_CTO` @`662d53b793`, under Andrew-direct 2026-09-17
~23:5xZ (*"Have CTO adjudicate the ANDREW_CARD.md if I'm not available"*) -- the ranked list is CONFIRMED
as printed, the RECOMMENDATION is corrected by one, and ranks 2-10 are ratified as TIED so no remediation
is sequenced on them. **The card itself was never altered**, which is the condition S6 set.

⭐ **THE CHEAP CONTROL S6 NAMED, for any future card:** state the claim as a **count with its
denominator** (*"1 of 179"*) rather than as a word (*"the two rows"*), **because a number invites the
check a word does not.**

---

## WHAT THIS RECORD DOES NOT DO

- It does **not** dispose of any row. `LGIC_LGCTFM-S12` and `S16` are dispositioned by `3.0.0_SA_CVO`;
  this is EVIDENCE. **Disarming is not disposing** and prose disarms nothing.
- It does **not** claim Andrew has read the card or the correction. It claims only that both are in the
  record, with the card's subject now identified by content hash. `FWD-4` still grades on his answer.
- It does **not** re-pin the three unpinned numbers row `S11` measures in round 1's judgment records.
  Under **R-43** a frozen-history defect's remedy is one live-direction document, never a sweep over
  rounds already graded.
