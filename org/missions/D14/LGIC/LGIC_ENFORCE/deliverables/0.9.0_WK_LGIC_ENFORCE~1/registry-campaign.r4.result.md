# registry-campaign.r4.result -- LGIC_ENFORCE.TO-EN-c-23-r4

**Result: 3 of 4 mechanical criteria PASS, 1 FAIL (structural, unsatisfiable in `<paths>`), 1 judgment (recorded, no self-grade).**

- C23R4-AC1 (campaign-covered): **PASS**. 351 of 351 population triples closed -- 0 minted, 351 carded, 0 open, 0 unresolved cards.
- C23R4-AC2 (mint-basis): **FAIL**. 0 registry rows added. Measured and filed as BLOCKING row `LGIC_ENFORCE-W1-S29`: this arm cannot detect a `systems.json` addition at all (reads 0 rows against an actual 25), and the one file it can see (`resources.json`) refuses, via the registry's own `validate()`, the exact `owner_claim`/`owner_basis` fields this arm requires. A code trace further shows `resources.json` cannot change `grade()`'s outcome for ANY of this population's 351 raises regardless of content. No registry write in `<paths>` can pass this arm for this cell.
- C23R4-AC3 (fence-untouched): **PASS**. `exemptions.json` byte-identical to the pinned base.
- C23R4-AC4 (validate-ok): **PASS**. Registry validates clean (systems.json/resources.json unchanged from base).
- C23R4-AC5 (judgment): recorded `UNVERIFIABLE-BY-INSTRUMENT`, no verdict from this worker. For `3.0.0_SA_CVO` at L9.

**Why 0 mints.** Every one of the 351 triples was researched (see `OWNER_CARDS_R4.md`, 15 card groups). None qualified under the WORKER FACE's "never guessed" mint rule: the 178 `astn`/`trade`/`news` triples are already correctly measured unresolved by this registry's own rows; the 119 `S3Key` triples are structurally outside `systems.json`/`resources.json`'s reach (governed by `NAMING_SCHEMA.json`'s tier list and `scopes.json`, neither in `<paths>`); the remaining 54 either have no declared source at all, are already correctly refused, are a retired or interim-pre-rename name, or (the `security` token, Card 6) collide with an unrelated, already-established different owner. Two surprise rows filed: `LGIC_ENFORCE-W1-S29` (BLOCKING, the AC2 structural bug) and `LGIC_ENFORCE-W1-S30` (OBSERVATION, the token-collision finding).

**Status:** the task order's `<status>` stays `pending` -- AC2 is FAIL by output and CLAUDE.md's bar requires every mechanical criterion to PASS-by-output before a `complete` flip. This instance is the final report on this cell pending the checker repair `LGIC_ENFORCE-W1-S29` names.

Instance: `LGIC_ENFORCE.TO-EN-c-23-r4.registry-campaign.proof_of_spec.json`, committed at `ebba3eb9de` (artifacts) + this commit (instance).
