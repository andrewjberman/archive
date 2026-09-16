# LGIC_ENFORCE.TO-EN-r-2-r2 -- RULING ROWS over the RAISE population: result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1` (slot ~1, queue position 2) · **Branch:** `wk-lgic-enforce-2b-1`, cut from
CLOUD @`ac82ad2331` · **Artifacts commit:** `72d636db4f` · **Cell:** `EN-r-2` (RULING ROWS) · **Nothing live
moved:** no AWS write, no Terraform apply.

## WHAT LANDED

1. **Every one of the 152 population groups is in exactly one class**, by subtraction from the printed
   union (Rule 24(i)): **(a) 7, (b) 93, (c) 0, (d) 46, undecided 6.**
2. **7 class (a) rows** added to `infra/logic/registry/systems.json` `systems`: five `PLATFORM_SUBSYSTEM`
   (`agentbus`, `cmtque`, `estate`, `firmsep`, `globgrph`) and two `VENDOR` (`bloomberg`, `msci`), each with
   `long`/`long_basis` citing a repo path (`.tools/agentbus-consumer.py`, `infra/aws/terraform/shared-infra/
   cmtque-alarms.tf`, `infra/aws/ec2/estate-report-runner/`, `.tools/comp-firmsep-sweep(.py)`,
   `docs/architecture/NFRA_GLOBGRPH_PRD.md`, `integrations/bloomberg/READ_HERE.md`, an `msci-api-credentials`
   secret), `owner_directive` a D-code, `owner_claim` `inferred`, and `owner_basis`.
3. **93 class (b) tokens** placed in `refused_keys`: 8 named workstream/project codes
   (`refused_keys.workstream_code`: `canonical`, `consolidation`, `gldinc`, `opsec`, `outset`, `quartz`,
   `semantic`, `wp5`) and 85 ordinary generic nouns/purpose words (`refused_keys.generic_noun`).
4. **0 class (c).** Zero of the population's 517 examples are typed `LAMBDA_LAYER` (measured, denominator
   printed in `REGISTRY_TOKEN_CLASSES.md`); `R1.e` applies to no group here.
5. **46 class (d)** tokens stay a loud RAISE: 27 pure-`K1` path-segment tokens; 5 `R8` `X#policy`-on-a-bucket
   tokens; 3 `L2` log-group-service tokens; 1 `G2.3` code/doc-divergence token; 5 `B2`-bearing tokens not
   defensible as `PRODUCT`; 2 `K1`-mixed tokens; `otp` (pure `K1`); `f49` (a garbled alias of `49f`, not a
   word).
6. **6 undecided tokens listed under `for_1.0.0_SA_CTO`** (`astn`, `trade`, `news`, `find`, `harvest`,
   `imo`) -- untouched in `systems.json`'s `unresolved`, per existing doctrine (row `LGIC_ENFORCE-W1-S6`;
   `infra/logic/05_IDENTITY_SPINE.md` s.3 tick-list row 18).
7. **11 of the 17 V2 `unresolved` tokens are removed** from `unresolved` (the 5 class-a + 6 workstream-code
   tokens); the other 6 stay exactly as they were.
8. `python lib/opal_naming.py validate` reads `VALIDATE: OK 24 system row(s), 9 scope row(s), 16 warning(s)`
   -- 0 refused, every warning `owner_directive ... inferred, owed a confirmation`, the same shape as the 9
   pre-existing inferred rows.

**A finding that shaped roughly a third of the classification (record: `REGISTRY_TOKEN_CLASSES.md`, row
`LGIC_ENFORCE-W1-S26`):** `B2` (a data bucket's scope) and `K1` (an S3Key's segment 1) accept ONLY a `V1`
token -- `refused_keys` (`V3`) membership resolves neither. This was not assumed from the rule's prose; it
was tested directly (scratch-copy `grade()` calls on `pm`/`S3_BUCKET` and `sentiment`/`S3Key` after adding
each to `refused_keys.generic_noun` -- both still raised) and independently corroborated at HEAD, no scratch
needed: `ec2` and `infrastructure`, already `refused_keys.generic_noun` members before this cell ran, both
still carry a `K1` example in this same population. Every group carrying a `K1`/`B2`/`R8`/`L2`/`G2.3`
example is therefore class (d) unless every one of its examples independently resolves (verified per-group,
not assumed).

## CRITERIA -- 6 of 6 mechanical PASS by output, 1 judgment RECORDED

Every invocation ran as `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/
2.0.0_SA_COO~G/fixed_inputs/r2/check_en_r2.py <sub>`, at commit `72d636db4f`. The checker exits 0 even on a
FAIL verdict, so the VERDICT line is the reading.

```
===== r2-every-group-classed                                                             R2-AC1  rc=0
POPULATION Built from the estate as of 2026-09-15 1: 152 groups (live 115, repo 134), minus the issuer's pre-landed [] = 152
CLASSED: {'a': 7, 'b': 93, 'c': 0, 'd': 46, 'undecided': 6}  SUM: 152  UNCLASSED: []  NOT IN THE POPULATION: []  IN TWO CLASSES: []  COUNTS WRONG FOR: []
VERDICT: PASS-EVERY-GROUP-CLASSED

===== r2-registry-valid                                                                  R2-AC2  rc=0
rc=0  REFUSED: 0 []  WARNINGS: 16
VERDICT: PASS-R2-REGISTRY-VALID

===== r2-a-rows                                                                          R2-AC3  rc=0
CLASS (a): 7  WITHOUT A systems.json ROW OF CLASS ['PLATFORM_SUBSYSTEM', 'PRODUCT', 'VENDOR'] AND A D-CODE OWNER: []
VERDICT: PASS-A-ROWS-PRESENT

===== r2-examples-resolve                                                                R2-AC4  rc=0
EXAMPLES OF CLASSES (a) (b) (c) RE-GRADED AT HEAD: 378  STILL RAISING ON THEIR OWN GROUP: 0 []
VERDICT: PASS-GROUP-EXAMPLES-RESOLVE

===== r2-d-still-loud                                                                    R2-AC5  rc=0
EXAMPLES OF CLASS (d) AND UNDECIDED RE-GRADED AT HEAD: 139  NO LONGER RAISING: []
VERDICT: PASS-D-STILL-LOUD

===== r2-no-token-twice                                                                  R2-AC6  rc=0
TOKENS BOTH A ROW AND unresolved/refused, OR BOTH REFUSED AND A ROW: []
VERDICT: PASS-NO-TOKEN-TWICE
```

`R2-J1` is a judgment criterion: **RECORDED, no verdict.** It is graded at L9 by `3.0.0_SA_CVO`, and the
proof instance carries it `UNVERIFIABLE-BY-INSTRUMENT`. What the CVO reads: `REGISTRY_TOKEN_CLASSES.md`'s
`why:` entry for each of the 7 class (a) rows (owner + basis), each of the 8 named class (b) workstream
codes, every class (d) special-case entry, and every undecided token's citation.

**Denominators.** R2-AC1: 152 groups, 0 pre-landed subtracted, 152 classed, 0 unclassed/extra/duplicate/
count-mismatched. R2-AC2: 24 system rows, 9 scope rows, 0 refused, 16 warnings. R2-AC3: 7 class (a) tokens,
0 without a valid row+owner. R2-AC4: 378 examples across 100 class (a)/(b)/(c) groups, 0 still raising.
R2-AC5: 139 examples across 52 class (d)/undecided groups, 0 no longer raising. R2-AC6: 0 collisions between
a row/refused token and `unresolved`/`refused_keys`.

## ROWS FILED (surprise channel, `INVESTIGATION_v1.md`)

| id | class / hazard | what |
|---|---|---|
| `LGIC_ENFORCE-W1-S26` | OBSERVATION / INERT | `B2`/`K1` accept only a `V1` token, never `V3`/`refused_keys` -- empirically verified (scratch-copy `pm`/`sentiment` tests; direct corroboration on already-registered `ec2`/`infrastructure`). Governs every class (d) call in this cell; filed because the cell's own plain language does not state the boundary. |

## INSTRUMENTS AND CONTROLS

- **Negative control (mutant):** the six `r2-*` subcommands were run on the pre-edit tree at `ac82ad2331`
  (before `REGISTRY_TOKEN_CLASSES.md` existed); `r2-every-group-classed` printed `FAIL-NO-CLASSES-RECORD`,
  rc=1.
- **Discrimination (a second mutant):** before trusting the plain reading of the cell's step 2, the proposed
  fix was tested against tokens outside this cell's own population (`pm`, `sentiment`) in a scratch registry
  copy -- both falsified the naive "refused_keys resolves any V3-classed token" reading.
- **Determinism:** all six subcommands ran twice -- once pre-commit and once at `72d636db4f` -- same verdict
  both times.
- **Not re-measured:** nothing live moved; no Terraform ran; `EN-s-1`'s full census is not re-run here (it
  is a separate cell, spawned after `EN-r-4` drains).
