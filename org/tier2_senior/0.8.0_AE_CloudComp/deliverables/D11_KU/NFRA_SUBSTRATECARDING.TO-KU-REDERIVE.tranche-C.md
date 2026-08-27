# TO-KU-REDERIVE — TRANCHE C — 9 of 12 `known_unsearched` entries re-derived

**Lane** `0.8.0_AE_CloudComp~Y` · **Issuer** `2.0.0_SA_COO~X` · **TO** `@6361bde30c` · **Directive** D11
**Subject** `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/graph_object_manifest.json`
**Key** `denominator.known_unsearched` (NOT top-level) · **Entries** `[0][1][2][3][4][5][7][10][11]`
**Measured** 2026-08-27 12:53Z–13:07Z · **EMITS NOTHING** — no L0 artifact, no held path, no generator, no registry entry

---

## GRAIN AND VINTAGE, ESTABLISHED BEFORE ANY VERDICT

The subject file is **dirty in the working tree** (107,472 → 355,597 bytes uncommitted) against its last
commit `94efcda69c`. That could have invalidated the whole unit, so I diffed my subject specifically:

```
  known_unsearched   HEAD vs worktree   12 entries / 12,363 chars  BYTE-IDENTICAL, 0 entries differ
  population_searched HEAD vs worktree                             IDENTICAL
  as_of.commit_ish   e48a7466ba on BOTH   (compiled_utc differs: 07:10:00Z HEAD / 11:27:48Z worktree)
```

**Every verdict below therefore holds against both vintages.** The uncommitted growth is elsewhere in
the file, not in the block I measured.

**Accessor control.** Top-level `known_unsearched` is absent (`None`); a `len(d.get(...,[]))` probe on it
returns `0`, byte-identical to an empty list — the issuer's documented near-miss, reproduced. Real key is
`denominator.known_unsearched`. My distribution reproduces the issuer's and MSTR's exactly:
**12,363 chars total · [6] 60.0% · [8]+[9] 26.2% · tranche C 1,700 chars / 13.8%**.

---

## VERDICTS

| # | verdict | one line |
|---|---|---|
| **[0]** | **REGIONS: NO LONGER TRUE · ACCOUNTS: UNMEASURABLE** | regions half searched and empty; accounts half needs a credential this seat does not hold |
| **[1]** | **SITE-Z: UNMEASURABLE · sub-claim NO LONGER TRUE** | "every local-plane part" is **14 of 22**, not all — 8 are tracked and identical on every device |
| **[2]** | **STILL TRUE — self-assessment UPHELD and now INSTANTIATED** | 2 graph-bearing DynamoDB tables exist and were missed; they are the **catalog of the swept warehouse** |
| **[3]** | **NO LONGER TRUE — understates 3.25x, hypothetical REALIZED** | "~100" is **325**; a 200 KB graph-bearing YAML is unregistered |
| **[4]** | **STILL TRUE — permanently, and correctly scoped** | no instrument needed; "by FORM" is load-bearing wording |
| **[5]** | **NO LONGER TRUE — plane searched, EMPTY, limit retirable** | 985 source files read, 0 hits on 8 tokens, control fires |
| **[7]** | **NO LONGER TRUE — and WORSE than claimed** | not 20 of 24 — **28 of 28**; the entry implies 4 were measured, **none were** |
| **[10]** | **STILL TRUE of population B — risk BOUNDED by population A** | I ran this expecting a gap and got the opposite |
| **[11]** | **PARTIALLY NO LONGER TRUE** | cadence/trigger now per-writer (as prose); **standing still unrepresented**; 3/2 writer counts verify |

---

## [0] OTHER AWS ACCOUNTS AND REGIONS — *regions closed, accounts unmeasurable*

**Claim.** *"the warehouse sweep is one bucket in us-east-1. A graph store in another account is invisible
here and no claim is made about it."*

**Instrument.** `s3api list-buckets` — **global, spans every region**, so one call closes the regions
question for S3 entirely. Plus `get-bucket-location`, `sts get-caller-identity`.
*False answer looks like:* a region-scoped call mistaken for a global one, or `LocationConstraint: null`
read as "unknown region".

```
  DENOMINATOR   31 S3 buckets in account 313476888478, ALL REGIONS
  graph-suggestive                     2   opal-313476888478-globgrph · opal-estate-report
  of those, ALREADY SWEPT by the census 2   (plane 1, 181,412 keys · plane 5, 129 keys)
  graph-bearing buckets in OTHER regions 0
  get-bucket-location(opal-...-globgrph) -> LocationConstraint: null
```

⚠ **`LocationConstraint: null` IS us-east-1** — the documented default-region quirk. A reader who takes
`null` as "region unknown" gets the opposite of the fact. The entry's us-east-1 claim is **verified**.

**Verdict — REGIONS half: NO LONGER TRUE.** Searched, and empty. **ACCOUNTS half: STILL TRUE and
UNMEASURABLE from this seat** — the credential is `arn:aws:iam::313476888478:user/Andrew_Berman`, a
single-account principal. Another account is invisible *by credential*, not by oversight, and no sweep
from this seat can change that. Splitting the entry would let the closed half be retired.

## [1] THE SITE-Z FABRIC — *unmeasurable as to site-Z; the sub-claim is false as stated*

**Claim.** *"this census ran on the laptop fabric only. Every local-plane part … describes THIS DEVICE,
and the other device's local stores are BY CONSTRUCTION different and unmeasured."*

**Instrument.** `git ls-files --error-unmatch` per part home (tracked ⇒ identical on every device;
untracked ⇒ pure device fact). Controls: `CLAUDE.md` → tracked **True**; `zzz_nonexistent_9999` → **False**.

```
  DENOMINATOR             25 parts with home_space == repo_path
    literal-path rows     22        brace-pattern SET rows  3
  over the 22 literal rows:
    TRACKED in git        8    <- IDENTICAL on site-Z. These do NOT describe only this device.
    UNTRACKED             14   <- pure device facts, invisible to every repo-plane instrument
```

**Verdict — site-Z limb: STILL TRUE / UNMEASURABLE from here** (I cannot read the other device's
filesystem; no instrument at this seat can). **Sub-claim "EVERY local-plane part describes THIS DEVICE":
NO LONGER TRUE — it is 14 of 22.** The 8 tracked ones are byte-identical on site-Z by construction, so the
device-specific population is smaller than the entry asserts, and the entry over-scopes its own warning.

⛔ **MY OWN INSTRUMENT WAS WRONG FIRST AND I CAUGHT IT BEFORE VERDICTING.** My first pass ran
`os.path.exists()` over all 25 homes and reported **3 missing**. Those 3 are the SET rows whose `home` is a
**brace-expansion pattern, not a literal path** — `os.path.exists` is *inapplicable* to them, not negative.
Expanded properly: `platinum.CACHE_SET` 5 of 5 present, `_build_manifest.json.SET` 3 of 3 present.
**That is "a pattern is not an extension" — the exact defect behind my own W4 BLOCKING — committed by me
one field over, six hours later.** Knowing a failure mode by name did not immunise me against writing it.

## [2] DYNAMODB / RDS / ANY NON-S3 PERSISTENCE — *the entry is right, and it is worse than a hypothetical*

**Claim.** *"not swept at all. A graph-bearing DynamoDB table would be missed entirely. THIS IS THE SINGLE
WIDEST GAP IN THE CENSUS."*

**Instrument.** `dynamodb list-tables` (auto-paginated, counted client-side), `describe-table`, a live
`scan` to read contents rather than trust names; `rds describe-db-instances`; `neptune describe-db-clusters`.
*False answer looks like:* judging a table by its name — so I opened them.

```
  DENOMINATOR   36 DynamoDB tables (account 313476888478, us-east-1)
    graph-bearing                       2
      opal-globgrph-nessie-_objs    60,608 items   82,477,161 bytes   ACTIVE
      opal-globgrph-nessie-_refs        80 items        7,136 bytes   ACTIVE
  RDS instances        0
  Neptune clusters     0        <- AWS's own graph DB service, checked and genuinely empty
```

Opened at grain, not inferred from the name — `_refs` rows read:
`{"k": ":refs/tags/audit-baseline-2026-06-17", "c": "1781661734554739", "d": false, "p": <bytes>}`.
**That is a Nessie ref: a named pointer to a commit hash.**

>> ⛔ **THESE TWO TABLES ARE THE CATALOG OF THE VERY WAREHOUSE THE CENSUS SWEPT EXHAUSTIVELY.** Plane 1
   walked **181,412 S3 keys** under `s3://opal-313476888478-globgrph/warehouse/globgrph/` — the *data* —
   while the store that adjudicates **which snapshot is current** sat in DynamoDB, unswept, at 60,688
   items and 82.5 MB. The census measured the bytes and missed the thing that says which bytes are live. <<

This is not abstract. My own W4 card `W4-dncq` recorded `kuzu_nessie_db` pinned to
`nodes_snapshot 2902399899597701830` while live was `1462710383782792396` — **built from a superseded
snapshot, with nothing comparing the two.** `opal-globgrph-nessie-_refs` is the artifact that would have
settled it, and it was outside the census by construction.

**Verdict: STILL TRUE. The self-assessment "SINGLE WIDEST GAP" is UPHELD and no longer hypothetical** —
exactly two graph-bearing non-S3 stores exist, both were missed, and they are the highest-authority
objects in the graph estate. **The RDS and Neptune limbs are now closed at 0** and can be retired from the
entry; the DynamoDB limb is now *partially* closed — the two tables are named, but nothing in the manifest
registers them as parts.

## [3] `org/modules/graph/` BEYOND GRAPH-BEARING JSON — *understated, and the named risk is real*

**Claim.** *"~100 further .py/.yaml files were not classified. A store hiding as a .yaml in that tree would
be missed."*

**Instrument.** `os.walk` over the tree (exhaustive enumeration), plus a registration check against the
manifest's own `home` fields.

```
  DENOMINATOR   759 files under org/modules/graph/ (recursive)
    .pyc 307 · .py 254 · .yaml 71 · .json 37 · .txt 35 · .md 32 · .jsonl 6 · .ts 5 · ...
  CLAIM TEST    .py 254 + .yaml/.yml 71  =  325   <- entry says "~100 further"
  parts whose home is a .yaml/.yml       0 of 42
  parts homed under org/modules/graph/   5 of 42  (all .json / .jsonl / .py)
```

**The hypothetical is instantiated.** Among the 71 unregistered YAMLs:
`graph-call-manifest.yaml` **200,934 bytes** — the dependency-graph manifest **CLAUDE.md Rule 20 names as
the thing to query before any cloud/infra/data change**; `comp-coverage-map.yaml` 150,382;
`NFRA_ONTOLOGY_RULE_BANK.yaml` 109,632; `comp-tools.yaml` 95,328; `TOOL_MASTER.yaml` 84,906.

**Verdict: NO LONGER TRUE — understates by ~3.25x (325, not ~100), and "a store hiding as a .yaml" is not
a risk but a fact.** Whether `graph-call-manifest.yaml` *should* be a part is the manifest owner's call and
I am not making it; what is measured is that **zero** `.yaml` homes are registered and the largest
graph-bearing YAML in the estate is among them.

## [4] IN-MEMORY / EPHEMERAL GRAPH STATE — *permanently correct; no instrument invented*

**Claim (58 chars).** *"IN-MEMORY / EPHEMERAL graph state -- out of scope by form."*

**Instrument: none, deliberately.** Per the TO, an entry that is out of scope *by form* may be permanently
correct and need no instrument — inventing one would be manufacturing work. In-memory state has no
artifact to enumerate; the exclusion is definitional, not empirical.

⛔ **BUT THE WORDING "BY FORM" IS LOAD-BEARING AND SHOULD NOT BE PARAPHRASED.** The estate registers
`kuzu_nessie_db.rebuild.tmp.SET` as a part — a family that is **ephemeral by *intent*** (interrupted
rebuild temporaries) but **a file by *form***. Had this entry read "ephemeral by intent", that family
would have been wrongly excluded from the census. The entry's own practice confirms the criterion is
FORM, and the distinction is doing real work.

**Verdict: STILL TRUE, permanently. No defect. Recommend it be left exactly as worded.**

## [5] PORTAL-SIDE GRAPH SURFACES — *plane entered; genuinely empty; limit retirable*

**Claim.** *"not swept; the portal repo was not entered for this census."*

**Instrument.** Entered the repo. Filename sweep **and** content-grain read — filename alone is weak, and
the census's own idiom (a `*kuzu*` filename sweep) would miss a graph surface that does not say "graph".

```
  DENOMINATOR   1,513 files walked under portal/ (node_modules/.git/dist/build/.next/.svelte-kit pruned)
                  985 source files ACTUALLY READ (text extensions, <3 MB)
  filename contains "graph"     1   portal/docs/archive/design-language-v0/TYPOGRAPHY.md  (archived design doc)
  CONTENT hits, 8 tokens        0   globgrph · kuzu · nessie · graph_nodes · graph_edges
                                    comp-graph · graph.json · graph_contracts
  POSITIVE CONTROL  "import"  343 files   <- the reader works; 0 is a real 0, not a broken sweep
```

**Verdict: NO LONGER TRUE — the plane has now been entered and swept at content grain, and it is empty.**
The single filename hit is an archived typography document, not a graph surface. **This limit can be
retired from the manifest**, and retiring it costs the denominator nothing because the plane contributes
zero parts.

## [7] GENERATOR CURRENCY AND THE SEMANTIC-DEFECT AXIS — *both numbers wrong; the gap is total*

**Claim.** *"GENERATOR CURRENCY on 20 of 24 materializer-bearing parts, and THE SEMANTIC-DEFECT AXIS ON
EVERY PART … recorded here because it is the largest UNMEASURED surface and silence must not read as clean."*

**Instrument.** Count `generation.materializer` truthy; count `generation.materializer_digest` populated.
*False answer looks like:* currency recorded in some **other** field, which would make my digest-only
count a false zero — so I swept every field of every part before concluding.

```
  DENOMINATOR                                42 parts
  materializer-bearing                       28    <- entry says 24
  OF THOSE, materializer_digest populated     0
  currency UNMEASURED                        28 of 28   <- entry says 20 of 24
  non-null materializer_digest, ALL 42 parts  NONE
  POSITIVE CONTROL  parts mentioning "materializer"      42
  NEGATIVE CONTROL  parts mentioning zzz_no_such_field   0
```

**The entry implies 4 of 24 were measured. Zero were.** The field exists on all 42 parts and is `null` on
all 42.

**One nuance that matters.** Currency *is* asserted — in prose, in a free-text field, for exactly 2 parts:
`c2_instances.json` and `c3_structures.json` both carry `vintage.age_note: "output 19 days old; generator
current."` **That is a claim a consumer cannot reject on** (CLAUDE.md §4). The structured field that a
validator could enforce is empty on 100% of parts while the free string carries the claim — the same
enforced-vs-unenforced split measured on my own work earlier in this arc.

**Verdict: NO LONGER TRUE — the denominator is 28 not 24, and the gap is 28 of 28 not 20 of 24.** The
entry's *conclusion* (largest unmeasured surface; silence must not read as clean) is **strengthened**, not
weakened, by the correction. The semantic-defect limb I did not test: it asserts no instrument in the
estate discriminates a deprecated opinion, which is a claim about instrument **absence** and is not
decidable by the artifact-local method available to this tranche — **recorded as untested, not as clean.**

## [10] THE WAVE-3 CARD POPULATION — *true of population B; risk bounded by population A*

**Claim.** *"The wave-3 card population is the writers wave 3 SELECTED, not a fresh estate sweep. Any
materializer outside that selection is invisible to population B."*

**Instrument.** I hold a rare independent lever here: **I carded three materializer families in wave 4**,
after wave 3 closed. If [10]'s risk were unmitigated, my W4 subjects should be absent from the parts list.

```
  probe                    token                        hits in 42 parts
  W4-lgbr subject          .comp-graph/platinum          2   PRESENT
  W4-dncq subject          _build_manifest.json          2   PRESENT
  W4-vikb subject          kuzu_nessie_db.rebuild.tmp    2   PRESENT
  POSITIVE CONTROL         graph_nodes                   2   PRESENT
```

**All three are present. I ran this test expecting to demonstrate a gap and it demonstrated the opposite.**
They did not enter via wave-3 cards — they entered via **population A**, whose planes 2 and 3
(`infra/aws/globgrph/`, `.comp-graph/`) were swept **COMPLETE by directory enumeration**.

**Verdict: STILL TRUE AS WRITTEN — it is an accurate statement about population B — but the practical risk
it warns of is BOUNDED, because A's exhaustive enumeration catches what B's selection misses.** That is
the two-population design working as intended, and it is worth recording on the entry so a future reader
does not treat B's selection bias as an unmitigated hole in the whole manifest.

## [11] L0 `generation` HOLDS ONE MATERIALIZER/STANDING/CADENCE/TRIGGER — *partially superseded*

**Claim.** *"L0 `generation` holds ONE materializer/standing/cadence/trigger; graph_nodes has THREE
measured writers and graph_edges TWO … the manifest cannot currently express per-writer standing, so that
dimension is UNREPRESENTED rather than resolved."*

**Instrument.** Read `generation` on all 42 parts; check container type; read cadence/trigger/standing on
the two named parts. **Independent corroboration:** I read `incremental_updater/lambda_function.py` at
source during W4 — a *different instrument* from this manifest's compile, so this is corroboration and not
repetition.

```
  generation container type      dict 42 / list 0     <- STRUCTURALLY SINGULAR: claim STILL TRUE
  generation keys   cadence · declared_opinions · materializer · materializer_digest
                    materializer_standing · trigger
  graph_nodes  materializer  "derive_runner.py -> comp_aws_cli.py + incremental_updater/lambda_function.py"
               cadence       "PER WRITER: derive_runner PATH A=cron(0 2 * * ? *); comp_aws_cli.py=None; ..."   3 writers
  graph_edges  cadence       "PER WRITER: derive_runner PATH A=cron(0 2 * * ? *); comp_aws_cli.py=None"        2 writers
  materializer_standing        single scalar "canonical" on both      <- STILL unrepresented per writer
```

**The 3-and-2 sub-claim verifies exactly.** And it is explicable at source: `incremental_updater` writes
`table_id = ("globgrph","graph_nodes")` (`:434`, with `table.overwrite` `:501` / `table.delete` `:504`)
and writes **no** graph_edges table — which is precisely why nodes carries three writers and edges two.

**Verdict: PARTIALLY NO LONGER TRUE.**
- *"cannot express per-writer cadence/trigger"* — **superseded.** Both fields now carry per-writer values.
- *"cannot express per-writer standing"* — **STILL TRUE.** `materializer_standing` remains one scalar.
- *"generation holds ONE …"* — **structurally STILL TRUE**; the container is a dict on 42 of 42.

⛔ **AND THE FIX IS PROSE, NOT STRUCTURE.** Per-writer cadence is expressed as a **string beginning
`"PER WRITER: "` with `writer=value` pairs joined by semicolons** inside a single field. A consumer cannot
reject on it, cannot iterate it, and cannot tell a missing writer from an unparsed one. The dimension has
moved from *unrepresented* to *described* — which is a real improvement and is **not** the same as
represented. The entry's own word for the old state, "UNREPRESENTED rather than resolved", still applies
to standing and now applies in a subtler form to cadence and trigger.

---

## OFF-TASK OBSERVATION — surfaced, not chased

Reached through [1]'s expansion, outside my assigned entries. **Filed one line to `3.0.0_SA_CVO` cc the
issuer; not investigated further.** Class OBSERVATION, standing INERT — it blocks nothing in this tranche.

`kuzu_nessie_db.rebuild.tmp.SET` carries `basis: measured` over a **fully turned-over membership**:

```
  declared in `home` (pids 11532, 27528, 30644 + .wal)     6 members   0 PRESENT at 13:07Z
  actually present at that prefix now                      4 files, none of them declared
      kuzu_nessie_db.rebuild.tmp.39592.141201593000000.1        13,512,704
      kuzu_nessie_db.rebuild.tmp.39592.141201593000000.1.wal    12,894,466
      kuzu_nessie_db.rebuild.tmp                                43,970,560
      kuzu_nessie_db.rebuild.tmp.wal                             3,116,866
  POSITIVE CONTROL  same dir lists kuzu_db, kuzu_nessie_db, _build_manifest.json; git status shows the
                    live temporaries as '??' — the instrument CAN see files at this prefix
```

**This is my W4 BLOCKING (75058/75059, upheld) reproducing with entirely different pids**, and pid 39592 is
the one my W4 positive control fired on. The row is *internally honest* — it carries
`member_set.enumerable: false` — but its `home` field still lists six concrete names under a `measured`
basis, and that list is **0% accurate six hours later**. A runtime-named family cannot carry a measured
enumeration in a field consumers read as membership; `enumerable: false` and a six-name `home` are saying
different things in the same row.

---

## ACCEPTANCE

- [x] every assigned entry has a **verdict**, a **named instrument**, and a **denominator**
- [x] every count prints what it is a count **of**
- [x] **both controls** run wherever a count could be a false zero — `git ls-files` (True/False),
      portal content sweep (343 "import" files), manifest field sweep (42 / 0), `rebuild.tmp` absence
      (sibling artifacts + `??` entries visible at the same prefix)
- [x] entries read **in full** before verdicting — all nine printed and read, no subject-level judgement
- [x] **no entry required a held artifact**; nothing refused, nothing worked around
- [x] **EMITS NOTHING** — this file is a lane deliverable; no L0 artifact, no held path, no generator run,
      no registry entry, and **no edit to the subject manifest**

**Two of my own instruments were wrong before I published:** the `os.path.exists` pattern/literal slip in
[1], and the digest-only currency count in [7] which I did not trust until I had swept every other field.
Both are recorded above rather than silently corrected.

**`4.0.0_SA_CRO~A` overrides at any moment.** This tranche emitted nothing; a recall costs the arc only
this file, which is written down either way.
