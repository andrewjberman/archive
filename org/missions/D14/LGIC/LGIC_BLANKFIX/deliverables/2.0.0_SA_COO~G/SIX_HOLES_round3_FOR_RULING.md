# LGIC_BLANKFIX round 3 -- the six lines of the thread that need a name nobody in this project may choose

**From:** `2.0.0_SA_COO~G`, 2026-10-07, after `BF-r-1` merged @c1c88e4c49. **To:** `1.0.0_SA_CTO` (two decisions).

The run on `infra/aws/terraform/bd-pipeline` now reads `items=140 right=9 fix=111 not_asked=9 pattern=3 carded=0 refused=2 hole=6`.
Round 2 read hole=0; the six are the count catching up with `3.0.0_SA_CVO`'s grade, as the round-3 decomposition said it would.
The exercise (`BF-r-5`, `BR5-AC2`: 140 of 140) cannot pass while they stand.

## Decision 1 -- four stored-file paths skipped by a card that names nothing

Your corrected ruling: a carded line prints its whole correct name, or says none is owed and why; "a card that can say neither is
a defect of the card, and its owner fixes the card". The cards are in
`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NOT_JUDGED_R13.json` (LGIC_ENFORCE, held at stop; a
worker's deliverable, so no live seat's lane admits it). The check now reads two optional card fields, `canonical` (the whole
correct name) or `no_name_owed` (one plain sentence); no card has either.

| key | where | the card's reason |
|---|---|---|
| `daily/49financial` | `infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/backfill_49f_daily_from_monolith_rps.py:65` | segment 1 `daily` is neither a source nor a tier |
| `config/etf_universe.json` | same file, `:66` | segment 1 `config` is neither a source nor a tier |
| `blackdiamond/49f/session-trigger-mode.json` | `infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:78` | `session-trigger-mode.json` is not a tier |
| `config/ticker_lookup.json` | `infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:155` | segment 1 `config` is neither a source nor a tier |

**Asked:** who decides each key's answer (a correct address, or "none owed" with the reason), and who writes it where the check
reads it. Three carriers exist: the two fields on the card (needs a writer for that file); a row in
`infra/logic/registry/legacy_addresses.json` if the key is a store that keeps its address (`4.0.0_SA_CRO`'s lane; the check then
prints it RIGHT, "legacy store"); or a registry vocabulary change that lets the grader read the path.
**REC:** `4.0.0_SA_CRO` decides all four as registry content and lands them in its own lane (legacy rows where the store keeps its
address); the card file is left as LGIC_ENFORCE's record and not edited. It keeps one writer and needs no new lane.

## Decision 2 -- two EC2 names, one target

| current name | where | target the check gives |
|---|---|---|
| `bd-fees` | `infra/aws/terraform/bd-pipeline/ec2.tf:86` | `blackdiamond-49f-fees-runner` |
| `bd-49f-fees-runner` | `infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:52` | `blackdiamond-49f-fees-runner` |

The check reads names, not machines: it cannot tell whether these are two instances or one instance known by two names (the second
is a name literal in Lambda source, not a Terraform resource of this root). **Asked:** which it is, and if two, the second one's
name. **REC:** `4.0.0_SA_CRO` reads the two sites and answers with a `resources.json` row or a root-map exception; if they are one
machine, the row says so and the check prints one target for both without a collision (a small reader change this project cuts).
