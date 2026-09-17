# registry-campaign.r4.result -- LGIC_ENFORCE.TO-EN-c-23-r4 (RE-GRADE)

**Result: 4 of 4 mechanical criteria PASS-by-output, 1 judgment (recorded, no self-grade). `<status>` flips to `complete`.**

This is a re-grade of the same campaign (0 mints, 351 carded, commits `ebba3eb9de`/`4b3bdb5b22` on this
branch), against the repaired checker at `6876b0b526` (issuer `2.0.0_SA_COO~G`, row `LGIC_ENFORCE-W1-S29`).
The campaign's own artifacts (`OWNER_CARDS_R4.md`, `NOT_JUDGED_R4.json`) and the registry files
(`systems.json`, `resources.json`, both byte-unchanged from the pinned base `af8d694cce`) are UNCHANGED --
the repair was to the checker's `c23-mint-basis` arm, not to this cell's carding decisions, and re-running
the campaign's own measured judgment (0 mints was correct: no triple in the 351-population had a MEASURED,
never-guessed owner) against the repaired arm is what this re-grade tests.

- C23R4-AC1 (campaign-covered): **PASS**. 351 of 351 population triples closed -- 0 minted, 351 carded, 0
  open, 0 unresolved cards. Unchanged from the prior grade.
- C23R4-AC2 (mint-basis): **PASS** (was FAIL). The repair fixes the exact two defects this cell's row
  `LGIC_ENFORCE-W1-S29` measured: `_rows_of` now reads BOTH `systems` and `resources` keys (so a
  `systems.json` mint would now be visible, closing defect 1), the RESOURCES arm's basis is now `system`
  resolving to a real `systems.json` key plus `evidence` rather than the unsatisfiable `owner_claim`/
  `owner_basis` pair RES_FIELDS refused (closing defect 2), and 0 total rows added is now a stated legal
  vacuous PASS under R-32/R-33's own closure bar (`judged + carded == nameable`, never "zero carded") rather
  than a forced FAIL. Measured at this tree: `systems.json: 25 row(s) at the worktree, 0 added since
  af8d694cce`; `resources.json: 31 row(s) at the worktree, 0 added since af8d694cce`; `DENOMINATOR: 0 added
  registry row(s); 0 defective`; `VERDICT: PASS-C23-MINT-BASIS`. This cell minted nothing at the prior grade
  and mints nothing now -- the repair does not ask this worker to go back and guess an owner; it corrects
  the arm that could not previously certify a fully-carded, zero-mint campaign as legal.
- C23R4-AC3 (fence-untouched): **PASS**. `exemptions.json` byte-identical to the pinned base. Unchanged.
- C23R4-AC4 (validate-ok): **PASS**. Registry validates clean (systems.json/resources.json unchanged from
  base). Unchanged.
- C23R4-AC5 (judgment): recorded `UNVERIFIABLE-BY-INSTRUMENT`, no verdict from this worker. For
  `3.0.0_SA_CVO` at L9.

**Why 0 mints still stands.** Every one of the 351 triples was researched (see `OWNER_CARDS_R4.md`, 15 card
groups). None qualified under the WORKER FACE's "never guessed" mint rule: the 178 `astn`/`trade`/`news`
triples are already correctly measured unresolved by this registry's own rows; the 119 `S3Key` triples are
structurally outside `systems.json`/`resources.json`'s reach (governed by `NAMING_SCHEMA.json`'s tier list
and `scopes.json`, neither in `<paths>`); the remaining 54 either have no declared source at all, are
already correctly refused, are a retired or interim-pre-rename name, or (the `security` token, Card 6)
collide with an unrelated, already-established different owner. The checker repair does not change any of
that research or any card's conclusion -- it changes only whether a fully-carded, zero-mint outcome can be
CERTIFIED as satisfying AC2, and it now can. Two surprise rows already filed stand: `LGIC_ENFORCE-W1-S29`
(BLOCKING, disarmed by the issuer's repair at `6876b0b526` -- not this worker's row to disarm) and
`LGIC_ENFORCE-W1-S30` (OBSERVATION, the token-collision finding, unaffected).

**Status:** the task order's `<status>` flips to `complete` -- all four mechanical criteria now PASS-by-output
against the repaired checker, re-run at this branch tip, and C23R4-AC5 is recorded (not self-graded).

Instances: campaign artifacts at `ebba3eb9de` (systems.json/resources.json unchanged); the prior proof
instance and this re-grade's proof instance + result file at this commit.
