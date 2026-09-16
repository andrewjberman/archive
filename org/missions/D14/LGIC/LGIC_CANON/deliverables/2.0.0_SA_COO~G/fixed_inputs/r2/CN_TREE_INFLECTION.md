# CN_TREE_INFLECTION -- the SECOND judged tree for LGIC_CANON round 2

**Issued by** `2.0.0_SA_COO~G` with the round-2 issuance. **Read-only** to every worker.
**Consumers:** `CN-j-4` (judge C) and `CN-j-5` (judge D), identically. `CN-j-6` (judge E) does NOT read this file --
its tree is round 1's MDPF tree, unchanged, as the negative arm.

⛔ **THIS FILE CARRIES THE TREE'S FACTS AND NOTHING ELSE. IT DELIBERATELY CONTAINS NO VERDICT, NO AXIS GRADE, NO RULE
NUMBER AND NO STATEMENT OF WHICH RULES THE TREE ENGAGES.** The judges are blind and the reach is what they PRODUCE. A
fixed input that named the rules would hand the judge its answer and the measurement would certify nothing. If you are
reading this as a judge and you expected a rule list, its absence is the design.

---

## Why this tree, and how it was chosen

Ruling A-13 requires round 2's second tree to be chosen **BY MEASUREMENT** rather than by preference. The choice was
made by reading `infra/logic/06_CONFORMANCE_LEDGER.md` sections 1 and 2 at CLOUD `14936be222` and comparing the
candidate families on the properties A-13 names, then taking the family that carries the most of them. The comparison
and its numbers are recorded in the issuance commit and in decomposition v4 section 0d; they are **not** repeated here,
because a judge reading this file must not learn what the chooser was looking for.

**The tree is the INFLECTION family.** Its planes are enumerated below, from the ledger's own rows. Object counts and
`newest` dates are the ledger's as of its last census and are **context, never acceptance values** -- if a count
matters to your judgment, re-measure it and say so.

---

## The planes

### In the monolith, `opal-data-assets`

| plane | tier | objects | newest |
|---|---|---|---|
| `orion/inflection/bronze/` | bronze | 4,880 | 09-12 |
| `orion/inflection/silver/` | silver | 4,879 | 09-12 |
| `eclipse/inflection/bronze/` | bronze | 1,434 | 09-12 |
| `eclipse/inflection/silver/` | silver | 424 | 09-12 |

The 108 date-named table-level prefixes inside `eclipse/inflection/bronze/` are recorded by the ledger as a naming
sub-finding it did not re-measure (CTO msg 96116 item 6). They are part of the tree you are judging.

### In the legacy firm bucket, `opal-data-inf`

| plane | objects | newest | what the ledger records |
|---|---|---|---|
| `opal-data-inf/platinum/` | 8,673 | 09-12 | destination `opal-data-inflection/advi/inflection/platinum/`; the destination bucket must be MINTED on the template, with its serving grants and the fence re-derived from the scope slot first |
| `opal-data-inf/gold/` | 22,836 (17,161 parquet) | 09-12 | destination `opal-data-inflection/advi/inflection/gold/`; 221 json residual |
| `opal-data-inf/silver/` | 16,757 (3,066 json) | 09-12 | destination `opal-data-assets/{orion,eclipse}/inflection/silver/`, whose canonical twins already exist; LIVE |
| `opal-data-inf/bronze/` | 28,614 (4,802 parquet) | 09-12 | destination `opal-data-assets/...`, as raw; 4,802 parquet sit under bronze |
| `opal-data-inf/backup/gold_canonical_PRE_REDERIVE_.../` | 8,805 | 07-13 | -- |
| `opal-data-inf/_pre_rebuild_backup/.../silver/` | 6,060 | 06-30 | -- |
| `opal-data-inf/_toolprobe_scratch/` | 1 | 07 | -- |
| `opal-data-inf/backup/pre_pullheal_.../code/gold/` | 1 | 07 | -- |
| `opal-data-inf/code/{bronze,silver,gold}` | 204 | 08-11..08-30 | one code home, beside its gold |

### The firm's identity

`infra/logic/registry/scopes.json` carries `inflection` as a FIRM row with its long and short forms. The destination
bucket `opal-data-inflection` **does not exist yet** (the ledger's census); `opal-data-inf` is the live bucket.

---

## What you are asked to do with it

Judge every plane above on the canon's five axes, using `infra/logic/02_DOCTRINE.md` **alone** as your source of rules.
For each plane emit one row with its five axis verdicts and, for each verdict, the canon rule your verdict rests on.
Where the canon does not decide a plane, say so on that axis rather than choosing the nearest rule.

Your order names the exact output path and columns. Anything you would ask is a surprise row.

---

## Provenance

```
READ:        infra/logic/06_CONFORMANCE_LEDGER.md sections 1 and 2 at CLOUD 14936be222
COUNTS:      the ledger's own, as of its last census; context, never acceptance values
NOT READ:    the live S3 plane (this tree is judged from the record, as round 1's was)
CHOSEN BY:   2.0.0_SA_COO~G at the round-2 cut, per ruling A-13, on the comparison recorded in
             decomposition v4 section 0d and in the issuance commit
```
