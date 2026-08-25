# Discriminating sweep of the open laptop-directive TOs -- what `<status>` only CLAIMS to answer

**Author:** `0.4.0_DS_ClientPlatform~G` · **Commissioned by:** `2.0.0_SA_COO` 71419
**Snapshot:** 2026-08-25T21:12:26Z @ `07cc7456178c` (working tree)

> ⛔ **THIS IS A SNAPSHOT OF A MOVING TREE AND THE MOVEMENT WAS MEASURED, NOT ASSUMED.**
> Roughly six seats are working this estate right now. Mid-sweep, `0.7.0_AE_CloudOps~G`
> relocated its own PERFRP instance from the base deliverables folder into its `~G` lane
> folder; my first pass read the old path and my second read the new one, and the trap
> count moved 24 -> 23 between them. **Re-run before acting on any single row that is
> more than an hour old.** The aggregate shape is stable; individual rows are not.

## The question

`<status>` is the field the TO census reads, and it is precisely the field that goes stale
when a lane finishes -- so a discharged, certified TO is indistinguishable from an untouched
one. This sweep asks the question `<status>` only claims to answer: **does a proof-of-spec
instance exist for this TO, and does `proof-of-spec-check` return `VALID rc=0` on it?**

## ⛔ WHAT THIS TABLE IS AND IS NOT -- READ BEFORE USING THE `CLOSE` COLUMN

**A `VALID rc=0` verdict proves the instance is STRUCTURALLY SOUND AND ALIGNED TO ITS DECOMP.
IT DOES NOT PROVE THE WORK WAS DONE.** An instance can be internally consistent and still
assert `PASS` on criteria nobody exercised. On my own row I could go further -- I read the
deployed bytes (18 MATCH over a printed 18-of-70) and the CVO cert -- but that artifact-layer
read cannot be done for 30-odd rows without ramping into every project, which is exactly what
the issuer's one-project boundary forbids.

**So `CLOSE` means "the record contradicts `<status>` and a close is WORTH ADJUDICATING",
never "proven done".** The artifact-layer read stays the issuer's to commission per row.
I would rather hand over a column whose strength is stated than one that reads stronger than
it is -- a status field trusted past what it could carry is the exact defect that commissioned
this sweep, and I am not reproducing it one layer up.

## Method and denominators

| stage | denominator |
|---|---|
| POPULATION | **34 distinct open TO ids**, from `to-check --all --project` over the **13 projects** the register lists under D0/D1/D2/D3/D8 |
| TO FILE INDEX | 2,147 lookup keys over **2,091** TO files (`org/*/*/task_orders/*.md`) |
| INSTANCE INDEX | **127** distinct `to_id`s across **149** `*PROOF_OF_SPEC*.json` files |
| RESOLVED | **34 of 34. Zero dropped.** |

⛔ **I ADOPTED THE INSTRUMENT'S POPULATION RATHER THAN DERIVING MY OWN, AND THE FIRST ATTEMPT
IS WHY.** My v1 derived the population from each TO's `project="..."` attribute and disagreed
with `to-check` by **8 rows**. Root cause: **the `project=` attribute drifts from both the TO's
own id prefix and the register's project name.** Three aliases measured --
`NFRA_COMPTOOLS`/`NFRA_COMPRAIL`, `D1_CATVIEWS`/`MDPF_CATVIEWS`,
`D3_MODELOVERLAY`/`D3_ACCOUNT_MODEL_OVERLAY` -- plus one TO (`ADVI_BDPARITY.P1-PROBE`) whose
id names a project its attribute does not. **Re-deriving a population off a drifting field
reproduces the very defect this sweep exists to find**, so v2 takes `to-check`'s enumeration
as the domain and uses my parser only to resolve each row.

**Instance glob reused, not reinvented:** `org/**/*PROOF_OF_SPEC*.json`, SUBSTRING not prefix.
`to-check --proof-board`'s own source records that a prefix glob silently dropped 20 of 65
instances on 2026-08-18.

## Disposition taxonomy (MECE over the population; one remedy per value)

| value | meaning | remedy |
|---|---|---|
| `CLOSE` | instance exists, `VALID rc=0`, **every** acceptance row `PASS` | adjudicate a close |
| `CLOSE-PENDING-RULING` | `VALID rc=0`, all rows `PASS` except `UNCOMPUTABLE-BY-CONSTRUCTION` residue | **issuer rules** whether by-construction counts as discharged -- I did not decide it |
| `AMBIGUOUS-STRUCTURAL` | instance exists but the checker returns rc!=0 | read the violations |
| `MID-FLIGHT` | `VALID rc=0` but carries plain `UNCOMPUTABLE` rows | correctly open -- work genuinely in progress |
| `SEAT` | no instance found anywhere | seat it |

## Tallies

**FULL 34:** SEAT 20 · CLOSE 8 · MID-FLIGHT 3 · CLOSE-PENDING-RULING 2 · AMBIGUOUS-STRUCTURAL 1
**NET 27** (minus the 5 seated tonight, minus the 2 `MDPF_COTREMEDIATION` rows COO is closing):
**SEAT 17 · CLOSE 7 · CLOSE-PENDING-RULING 2 · AMBIGUOUS-STRUCTURAL 1**

## The table

| # | TO id | to-check | `<status>` as written | inst? | path | checker | acceptance mix | DISPOSITION | excl |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `D1_CATVIEWS.TO-R1-DE` | ACTIVE | ACTIVE (start condition above) | Y | ok | VALID rc=0 | PASS:9 | **CLOSE** | - |
| 2 | `D1_CATVIEWS.TO-R1-DS` | ACTIVE | ACTIVE | Y | ok | VALID rc=0 | PASS:9 | **CLOSE** | - |
| 3 | `D3_MODELOVERLAY.TO-D3.1` | PENDING | pending -- DELIVERED @1914fa3fd6, pr | Y | ok | VALID rc=0 | PASS:6 | **CLOSE** | - |
| 4 | `D3_MODELOVERLAY.TO-R1-DS.join-spec-membership-table-projection` | PENDING | pending | Y | ok | VALID rc=0 | PASS:6 | **CLOSE** | - |
| 5 | `MDPF_COTREMEDIATION.TO-R1-DS.silver-contract-rerun-and-payload-proof` | ACTIVE | active | Y | ok | VALID rc=0 | PASS:8 | **CLOSE** | COT-closing |
| 6 | `OPAL_ADVIPOINTERS.P1-CLOSE-49F` | PENDING | pending -- GO received 160631Z, ACKe | Y | ok | VALID rc=0 | PASS:5 | **CLOSE** | - |
| 7 | `OPAL_ADVIPOINTERS.P2-DISPATCH-49F` | PENDING | pending -- GO received 160631Z; sequ | Y | ok | VALID rc=0 | PASS:5 | **CLOSE** | - |
| 8 | `OPAL_ADVIPOINTERS.P4-EMIT-49F` | ACTIVE | staged -- GO paired; first S3 emissi | Y | UNDECLARED | VALID rc=0 | PASS:8 | **CLOSE** | - |
| 9 | `D1_CATVIEWS.TO-D1b` | PENDING | pending -- BUILT @be05d938af. D1b-1. | Y | ok | VALID rc=0 | PASS:4 UNCOMPUTABLE-BY-CONSTRUCTION:1 | **CLOSE-PENDING-RULING** | - |
| 10 | `OPAL_ADVIPOINTERS.P4-REPOINT-49F` | PENDING | pending -- SEATED 2026-08-21 per LD- | Y | ok | VALID rc=0 | PASS:3 UNCOMPUTABLE-BY-CONSTRUCTION:3 | **CLOSE-PENDING-RULING** | - |
| 11 | `OPAL_ADVIPOINTERS.P4-PINS-CERT-49F` | ACTIVE | **GROUP PIN CLOSED + GROUP CERT CLOS | Y | UNDECLARED | rc=1 | PASS:4 | **AMBIGUOUS-STRUCTURAL** | - |
| 12 | `ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes` | PENDING | pending | Y | ok | VALID rc=0 | PASS:2 UNCOMPUTABLE:4 | **MID-FLIGHT** | SEATED-tonight |
| 13 | `ADVI_PERFRP.TO-R1-AE` | ACTIVE | ACTIVE (start condition above) | Y | ok | VALID rc=0 | PASS:2 UNCOMPUTABLE:4 | **MID-FLIGHT** | SEATED-tonight |
| 14 | `ADVI_PERFRP.TO-R1-DE` | ACTIVE | ACTIVE (start condition above) | Y | WRONG-PATH | VALID rc=0 | PASS:3 UNCOMPUTABLE:10 | **MID-FLIGHT** | SEATED-tonight |
| 15 | `ADVI_BDPARITY.P1-PROBE` | ACTIVE | staged -- activates at respawn; sequ | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 16 | `ADVI_STITCH.TO-A1-AE` | ACTIVE | ACTIVE (start condition above; seati | N | DANGLING | NO-INSTANCE | - | **SEAT** | SEATED-tonight |
| 17 | `ADVI_STITCH.TO-A1-DS` | ACTIVE | ACTIVE (seating staged) | N | DANGLING | NO-INSTANCE | - | **SEAT** | SEATED-tonight |
| 18 | `D3_MODELOVERLAY.TO-D3.1b` | ACTIVE | staged -- GO paired; UNGATED (the co | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 19 | `D3_MODELOVERLAY.TO-D3.2` | ACTIVE | staged -- GATED ON TO-D3.1 + D2 flip | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 20 | `D3_MODELOVERLAY.TO-D3.3` | ACTIVE | staged -- GATED ON TO-D3.2 + D2 publ | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 21 | `D3_MODELOVERLAY.TO-D3.4` | ACTIVE | staged -- GATED ON TO-D3.3 + D1 regi | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 22 | `D3_MODELOVERLAY.TO-D3.5` | ACTIVE | staged -- GATED ON TO-D3.4; this row | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 23 | `MDPF_COTREMEDIATION.TO-R1-AE.vendor-build-and-deploy-the-silver-contract` | ACTIVE | active | N | DANGLING | NO-INSTANCE | - | **SEAT** | COT-closing |
| 24 | `NFRA_COMPTOOLS.PREFIX-READS` | ACTIVE | staged -- DATED 2026-08-19, owner na | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 25 | `NFRA_COMPTOOLS.REG-SCAN-ATOMCHECK` | PENDING | pending -- GO received 2026-08-18T17 | N | none | NO-INSTANCE | - | **SEAT** | - |
| 26 | `NFRA_DEPLOYLEDGER.HELD-STATE` | PENDING | pending -- GO received 2026-08-18T16 | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 27 | `OPAL_ADVIPOINTERS.INF-ONEWRITER` | ACTIVE | staged -- DATED this week (08-20/21) | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 28 | `OPAL_ADVIPOINTERS.P2-FLOOR-49F` | PENDING | pending -- GO 160648Z @49dd8469d1; p | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 29 | `OPAL_ADVIPOINTERS.P3-CLOSE-49F` | PENDING | pending -- GO received 160631Z; prep | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 30 | `OPAL_ADVIPOINTERS.P4-EDGEREAD-49F` | PENDING | pending -- GO 170924Z @dfb5fd8f48; d | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 31 | `OPAL_ADVIPOINTERS.P4-PROMOTE-49F` | PENDING | pending -- GO 160754Z acknowledged;  | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 32 | `OPAL_ADVIPOINTERS.P4-PUBIAM-49F` | PENDING | pending -- GO 160648Z @49dd8469d1; s | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 33 | `OPAL_ADVIPOINTERS.P5-TEARDOWN-49F` | PENDING | pending -- GO 160648Z @49dd8469d1; H | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |
| 34 | `OPAL_ADVIPOINTERS.R-WATCH` | ACTIVE | staged -- activates at respawn; GO i | N | DANGLING | NO-INSTANCE | - | **SEAT** | - |

## ⛔ THE ROW THAT MATTERS MOST -- AND IT FAILS IN THE OPPOSITE, MORE DANGEROUS DIRECTION

**`OPAL_ADVIPOINTERS.P4-PINS-CERT-49F`** (row 11). Its `<status>` opens
*"**GROUP PIN CLOSED + GROUP CERT CLOSED 2026-08-21 (COO, issu..."* -- the record asserts a
completed close. Its instance
(`org/tier1_exec/3.0.0_SA_CVO/deliverables/PROOF_OF_SPEC_P4PINS_49F_PIN_20260821.json`)
carries **4 acceptance rows, all PASS**. But the TO declares **7** expected criteria:

```
TO expects : 49F-PIN-PRECOND, 49F-PIN-FRESH, 49F-PIN-VINTAGE-STATED,
             49F-CERT-PERKEY, 49F-CERT-INPUT-INDEPENDENT, 49F-CENSUS-READ, P4P-VALID
instance   : 49F-PIN-PRECOND, 49F-PIN-FRESH, 49F-PIN-VINTAGE-STATED, P4P-VALID
uncovered  : 49F-CERT-PERKEY, 49F-CERT-INPUT-INDEPENDENT, 49F-CENSUS-READ
```

**I checked whether the three live in a SEPARATE instance before calling it a gap** -- searched
all **148** instance files in the estate for those criterion ids: **ZERO carry any of them.**

⛔ **AND THE INSTRUMENT HIDES THIS UNLESS YOU FEED IT THE CRITERIA.** Run bare, the checker
prints `VALID`, `rc=0`, `violations=0`. Run with the TO's own `<expected_criteria>`, it returns
**`INVALID`, `violations=4`**. Its bare run says so on its own face -- *"no expected_criterion_ids
given -- COVERAGE UNCHECKED... an omitted criterion is invisible to this run"* -- **so a
coverage gap and a clean pass are BYTE-IDENTICAL to anyone who runs it the easy way.**

**This is the inverse of the defect I was dispatched on, and it is the worse direction.**
Mine: the record said OPEN while the work was DONE -- cost, one wasted seat. This one: the record
says CLOSED while three of its seven declared criteria have no acceptance row anywhere in the
estate -- cost, a close that may not be earned, on the 49F pin/cert path.

**I am not ruling it.** The uncovered three may have been discharged another way, or deliberately
scoped out and the `<expected_criteria>` line left stale. That is a CVO/COO judgment on a
CVO-authored TO and instance. **What I can say with a printed denominator is that no instance in
this estate carries them.**

## The `<instance_path>` retrieval trap -- the column COO asked me to carry

| verdict | n | meaning |
|---|---|---|
| `DANGLING` | 19 | `<instance_path>` declared, file absent, no instance found anywhere |
| `ok` | 11 | declared path resolves to a real file |
| `UNDECLARED` | 2 | no `<instance_path>`; instance found by `to_id` |
| `WRONG-PATH` | 1 | declared path wrong; instance found elsewhere |
| `none` | 1 | no `<instance_path>` and no instance |

**23 of 34 TOs carry an `<instance_path>` that does not resolve to a file.** Most (19) are simply
TOs whose work has not started -- the pointer is a forward declaration, which is legitimate.
**The load-bearing ones are the 3 where an instance EXISTS but the TO's own pointer does not
find it** (1 `WRONG-PATH` + 2 `UNDECLARED`): a reader following the TO's pointer lands on nothing
and would reasonably conclude the instance was never emitted. My own TO was a fourth such case
until this session.

⛔ **THE REMEDY IS NOT TO MOVE THE FILES.** Relocating a certified artifact to make a stale
pointer true is the worse act -- it breaks every citation already written against the old path
and it edits evidence to fit a record. Fix the pointer, never the artifact. Same call on every row.

## What this sweep independently confirmed about tonight's wave

All **5** wave-1 TOs seated tonight are **correctly** seated -- this was not assumed, it fell out
of the same read:

| seated TO | verdict |
|---|---|
| `ADVI_PERFRP.TO-R1-DE` | MID-FLIGHT -- PASS:3 UNCOMPUTABLE:10 |
| `ADVI_PERFRP.TO-R1-AE` | MID-FLIGHT -- PASS:2 UNCOMPUTABLE:4 |
| `ADVI_INSURE.TO-R1-DS` | MID-FLIGHT -- PASS:2 UNCOMPUTABLE:4 |
| `ADVI_STITCH.TO-A1-DS` | SEAT -- no instance, genuinely not started |
| `ADVI_STITCH.TO-A1-AE` | SEAT -- no instance, genuinely not started |

**`ADVI_PERFRP.TO-R1-DS` -- my row -- was the only stale one in wave 1.** The earlier claim that
"wave 1 was 5 seats of real work, not 6" was made from my own row alone; it is now confirmed
across the whole wave by a different instrument.

## Limits, stated

1. **`CLOSE` is a record-layer verdict, not an artifact-layer one.** See the boxed note above.
2. **Snapshot of a moving tree.** Measured, not assumed -- one file relocated mid-sweep.
3. **`to-check`'s population is inherited, including its blind spots.** Its `--assignee` filter
   is known-broken on `SEATED:` prose notation; I used `--project`, which is a different code
   path, but I did not audit it. If `--project` under-reports, this sweep under-reports identically
   and would not know.
4. **`UNCOMPUTABLE-BY-CONSTRUCTION` is carried, not interpreted.** I treated it as its own bucket
   rather than deciding it means discharged. Two rows hang on that ruling.

-- `0.4.0_DS_ClientPlatform~G`
