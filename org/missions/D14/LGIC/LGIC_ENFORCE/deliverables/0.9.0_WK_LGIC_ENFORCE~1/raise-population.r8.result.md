# raise-population.r8.result -- LGIC_ENFORCE.TO-EN-p-36-r8

Worker `0.9.0_WK_LGIC_ENFORCE~1`, worktree `wk-lgic-enforce-8-1`, branch `wk-lgic-enforce-8-1`.

## What ran

1. `selftest-arms` (31 arms, 13 positive-satisfiability) -- `PASS-SELFTEST-31-ARMS-13-POSITIVE`, run
   BEFORE any write. No arm unsatisfiable, no BLOCKING row owed.
2. `raise_population_r8_build.py enumerate` -- re-measured BOTH planes at this cell's own write time,
   using the SAME item-building code `census()` uses (`census_live`, `census_repo`, `_vocab`,
   `_aws_fixed`), then called `grade()` on EVERY item without stopping at the first RAISE (unlike
   `census_judge()`, which stops by design -- the whole point of this step is to learn the population
   census_judge cannot show on its own). Measured: **live to_judge 1838, raises 131**; **repo names
   1878, raises 331**. Both denominators match `R8_BASE.json`'s pinned `census_*_at_the_cut` figures
   exactly (1838/1878); the RAISE counts (131/331) do NOT match `R8_BASE`'s carried `raise_population`
   (504 live / 623 repo, `claim: reported`, W7-S1's from 2026-09-15) -- expected and stated by the order:
   the registry has grown since (gateway, globgrph, harvest, bloomberg, msci additions), shrinking the
   live population; THIS round's numbers govern per the order's own instruction.
3. `raise_population_r8_build.py classify` -- every one of the 462 raises (131+331) matched against the
   ALREADY-MEASURED per-token owner research this same worker slot filed in **round 4**
   (`OWNER_CARDS_R4.md`, Cards 1-19, registry@`af8d694cced2b38e52f5735a35bd4ea0f7655eda`). That file's
   own governing finding: *"Zero mints follow from that, not from a shortfall of effort: every token
   below was researched against infra/aws/terraform/, org/missions/DIRECTIVES.yaml, org/projects/*.json
   and the live-AWS census instruments before being carded."* The classifier raises `SystemExit` on any
   RAISE that is not a member of that already-researched set -- it did not fire; every raise this round
   measures is a member of round 4's set or the SAME structural class (K1/K3/K4a path-grammar words,
   Card 1). Disposition: **0 RESOLVED, 462 CARDED** (131 live, 331 repo).
4. One additional check beyond round 4's own research: the `dowjones` token (Card 11, "no declared
   source" at round 4's narrower `infra/`+`tools/` search) was re-searched this round with the full-corpus
   `comp-find`. It surfaces a real home -- `org/tier1_exec/4.0.0_SA_CRO/scripts/dowjones_harvest_session.py`,
   an Andrew-direct CRO harvest session (`ANDREW_DIRECT_20260914_DOWJONES_HARVEST_W.md`) -- but that is a
   SEAT's ad hoc tooling, not a mission-tree `D<n>` pipeline `systems.json`'s `owner_directive` field
   requires. No registry row was minted for it; it stays CARDED, with the wider search recorded in its
   card.
5. `python lib/opal_naming.py census --live --repo --budget 120 --not-judged <the 462 cards>
   --report NAMING_CENSUS_REPORT.r8.md` -- **rc=0**, `CENSUS: COMPLETE 3254 judged + 462 carded (live
   1707+131 of 1838 nameable, repo 1547+331 of 1878)`. Both planes run to the end: `stopped` is `null`
   on both.
6. `raise_population_r8_build.py build --judged-live 1707 --judged-repo 1547` -- wrote
   `RAISE_POPULATION_R8.json` from the real run's own printed judged counts.
7. Determinism: the whole `enumerate` -> `classify` -> `build` chain was re-run TWICE MORE against the
   same inputs after the first build; `sha256` over the worktree bytes of `RAISE_POPULATION_R8.json`
   matched all three times (`890e51edc4...` each run).
8. Live mutant controls on the COMMITTED record (not the fixture self-test), each fired alone and
   restored byte-identical after: (M1) `planes.live.raise_population` set to 999 ->
   `FAIL-P36-POPULATION` (remainder 868). (M2) one repo card's `card` field blanked to whitespace ->
   `FAIL-P36-CARDS-CARRY-REASONS` (`rows with no card reason`: 1, naming `F49ServedAndSourceRead`).
   (M3) `planes.live.stopped` set to a non-null object -> `FAIL-P36-RUNS-TO-END`. Restored bytes
   verified equal to the pre-mutation copy after each; all four arms PASS on the restored bytes.

## Final arms

```
PASS-P36-POPULATION        live: resolved 0 + carded 131 = 131 ; raise_population 131 ; remainder 0
                            repo: resolved 0 + carded 331 = 331 ; raise_population 331 ; remainder 0
PASS-P36-RUNS-TO-END        live: stopped=None judged=1707 (floor 3)
                            repo: stopped=None judged=1547 (floor 2)
PASS-P36-OWN-DENOMINATOR    live: own denominator 1838 via census --live (this cell's own run)
                            repo: own denominator 1878 via census --repo (this cell's own run)
PASS-P36-CARDS-CARRY-REASONS  carded rows inspected: 462; rows with no reason: 0
```

`resolved + carded == raise_population`, PER PLANE: live `0 + 131 == 131`; repo `0 + 331 == 331`.
Registry rows added this round: **0** (corroborated zero-mint finding, not a re-derivation).

## P36R8-AC5 (judgment, no verdict from this worker)

Material for `3.0.0_SA_CVO` at L9: does each CARD reflect a real search rather than a shrug? Every card
cites a specific Card N in `OWNER_CARDS_R4.md` (round 4, same worker slot) with that card's own "what was
measured" evidence, restated per item, plus one item (`dowjones`) where this round's own WIDER search is
recorded distinctly from round 4's. Whether 0 RESOLVED is correct (rather than a shortfall of effort) is
exactly `OWNER_CARDS_R4.md`'s own governing finding, re-confirmed here against the CURRENT, grown
registry -- not re-typed from that file without a check that this round's smaller population is still
entirely covered by it (the classifier's `SystemExit` on any uncovered raise is that check, and it never
fired).
