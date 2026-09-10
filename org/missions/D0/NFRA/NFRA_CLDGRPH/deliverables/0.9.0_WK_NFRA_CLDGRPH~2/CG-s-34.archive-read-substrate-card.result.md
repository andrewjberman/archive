# CG-s-34 -- THE ARCHIVE-READ SUBSTRATE CARD, A ROW PER CARRIER

**Task order:** `NFRA_CLDGRPH.TO-CG-G-3` -- cell `CG-s-34` (decomp v0.10 s.1a, added on the CTO's
round-6 analysis @`d5c24a4dce` s.6 item 4).
**Seat:** `0.9.0_WK_NFRA_CLDGRPH~2`, spine v3 L7 worker of `2.0.0_SA_COO~A`, round 7.
**Worktree:** `C:/tmp/wk-cldgrph-7-2`, branch `wk-cldgrph-7-2`, from CLOUD @`f3b5f26f77`. Push state
LOCAL -- nothing pushed, nothing merged.
**Egress hold:** OBSERVED IN FULL. No ECS run-task, no CodeBuild start, no image act, no digest
re-pin, no `safe-apply`, no S3 write, no S3 read, no `aws` call of any kind, nothing that could
cause an SNS publish. Every AWS-plane number in this deliverable is read from the RECORD of a read
another seat performed, and every one says so where it appears.

---

## 1. What was built

| # | artifact | what it is |
|---|---|---|
| 1 | `deliverables/0.9.0_WK_NFRA_CLDGRPH~2/g2_card_evidence.py` | re-grounds the three instances from the record: each row read AT the commit that minted it, each fix located by the code token it introduced, each visible-making number taken from the row's own text and corroborated on a second object |
| 2 | `cards/stitch-producer-archive-read.card.json` | the CARRIER SET card at the path the face names |
| 3 | `cards/stitch-producer-archive-read.nodes.card.json` | carrier row 1 -- seven questions, seven owners |
| 4 | `cards/stitch-producer-archive-read.props.card.json` | carrier row 2 -- seven questions, seven owners |
| 5 | `cards/stitch-producer-archive-read.edges.card.json` | carrier row 3 -- seven questions, seven owners |
| 6 | `deliverables/0.9.0_WK_NFRA_CLDGRPH~2/g2_card_rows.py` | reads the set as one row per carrier: 3 carriers, 7 questions each, an owner each, question 7 answered concretely |
| 7 | `deliverables/0.9.0_WK_NFRA_CLDGRPH~2/g2_shrink_probe.py` | the round's lesson as a check: does the archive read MASK a shrink |
| 8 | this record, then the proof instance, then the flip |

Why four card files and not one: the substrate-card contract's unit is ONE SUBJECT WITH SEVEN ROWS,
`additionalProperties:false` at the root on both schema versions, so three carriers x seven
questions x an owner each (21 owned rows) cannot live in one file and a top-level array is refused
by the validator. Filed as row `NFRA_CLDGRPH-W2-S74` with the schema lines that make it so, and the
shape follows the estate's own precedent (`kuzu_nessie_db.rebuild.tmp.SET.card.json`).

## 2. The criteria, each with its instrument's coverage, its harness's grain, and its baseline's environment

### G3-AC1 -- the three instances, re-grounded from the record

`timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/g2_card_evidence.py`
-> rc 0.

```
INSTANCES_REGROUNDED=3 of 3
NODES=NFRA_CLDGRPH-W2-S61 regrounded=True
PROPS=NFRA_CLDGRPH-W2-S69 regrounded=True
EDGES=NFRA_CLDGRPH-W2-S71 regrounded=True
EVIDENCE_FROM_RECORD=true
```

- **COVERAGE:** every fenced json block of the channel, parsed and summed -- **245 rows in 186
  blocks, 0 unparsed** at the vintage the script ran (248 in 187 after this order's own append).
  Provenance: `git log --full-history -S<token>` over one path, never a path-simplified log.
- **GRAIN:** one row object per surprise (counted by object, never by an id grep -- the header line
  itself matches an id grep); one commit per provenance question, the FIRST that added the token.
- **ENVIRONMENT of the compared values:** NOT this process. Every visible-making number was produced
  by a CLOUD run or a served read at the time the row was filed. This worktree re-read the RECORD.
- 7 of 7 checks per carrier, including an APPEND-ONLY CONTROL: each row is byte-identical between
  the commit that minted it and HEAD, so the re-grounding reads the vintage that made the claim.

| carrier | row | row minted at | fix located by token | fix commit |
|---|---|---|---|---|
| NODES | `W2-S61` | `80daa1fff6` | `_retype_prior_cycle` | `80daa1fff6` |
| PROPS | `W2-S69` | `2f87f07926` | `RETIRED_STITCH_PROPS` | `22bc65fab0` (third cycle) |
| EDGES | `W2-S71` | `2178066b7d` | `stored_in_prior_cycle_dropped` | `f9000bd0dd` (fourth cycle) |

The numbers, from the rows themselves: NODES `retyped=1770` over a carried population the row
censuses at 1,771; PROPS `STITCH_V1_STAMPED_SERVED=1` while the fold printed `stamped=0`; EDGES
`955` emitted in the prior cycle against `137` in the next -- the second number corroborated on a
different object, `ROUND_ANALYSIS.round6.md` s.2.

### G3-AC2 -- the card is a contract

**The invocation the face names could not be run, and the substitution is recorded, not hidden.**
`.tools/validate-json-schema.py` does not exist at `f3b5f26f77` and appears nowhere in the corpus.
Per G3-AC2's own escape clause the estate's validator was used:

`timeout 120 python .tools/substrate-card-check.py org/missions/D0/NFRA/NFRA_CLDGRPH/cards/stitch-producer-archive-read.card.json`
-> rc 0:

```
substrate-card-check | .../stitch-producer-archive-read.card.json | structural=jsonschema | violations=0
  VALID
```

All four cards, one invocation, rc 0: `violations=0` and `VALID` x4.

- **COVERAGE:** the whole card, every field, under `jsonschema` Draft7 (the tool degrades loudly if
  the package is absent; here it reported `structural=jsonschema`, so the structural arm is FULL),
  plus the three cross-field rules the schema can only describe.
- **GRAIN:** one card file per validation; 4 of 4 files validated.
- **ENVIRONMENT / WHICH CONTRACT:** `.tools/substrate-card-check.py:28` hardcodes
  `org/standards/SUBSTRATE_CARD.v3.1.schema.json` and takes no schema argument, so the contract
  actually enforced is **v3.1**, NOT the `SUBSTRATE_CARD.schema.json` (v1) the face names. The two
  are mutually exclusive: `schema_version` is `const 1` in one and `const 3.1` in the other. Row
  `NFRA_CLDGRPH-W2-S73`.

### G3-AC3 -- a row per carrier, each complete

`timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/g2_card_rows.py`
-> rc 0.

```
CARD_ROWS=3 of 3 carrier(s) -- NODES, PROPS, EDGES
QUESTIONS_PER_ROW=7 of 7 (the MINIMUM across carriers, so one incomplete carrier cannot be averaged away; 3 of 3 carrier(s) at 7)
OWNER_PER_ROW=3 of 3 (carriers whose seven rows each carry an owner)
FAILURE_MODE_DISTINGUISHABLE=3 of 3 (carriers answering question 7 concretely)
SET_COMPLETE=True
```

- **COVERAGE:** 3 carriers x 7 questions = **21 of 21 rows**, each checked for a non-blank answer, a
  basis in the four-value vocabulary, an evidence string carrying a vintage, and an owner.
- **GRAIN:** one carrier per card, one question per row, one owner per row.
- **DERIVATION, disclosed:** the carrier set is read out of the SET CARD's
  `artifact.location.projection_of`, and each carrier's name out of its own `subject.id`, never from
  a filename. An unscoped control prints the 4 `*.card.json` files on disk beside the 3 enumerated,
  so a card the set card forgets is visible as a gap rather than invisible.
- Question 7 is answered `no` on nodes, `no` on props and `yes` on edges -- three carriers, three
  answers, which is the whole reason this cell exists.

### G3-AC4 -- the lesson, made falsifiable

`timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/g2_shrink_probe.py`
-> rc 0.

```
SHRINK_MASKED=true on (955 -> 137) -- 818 stale edge(s) of 955 in the artifact, 137 of 955 emitted this cycle
SHRINK_MASKED=false on the fixed-emission pair (955 -> 955) -- 955 of 955 carried in and 955 of 955 re-emitted, 0 stale
PROBE_CONTROL=FIRED (6 of 6 controls hold)
WIRED_TO=nothing
```

- **COVERAGE:** the whole reconstructed `STORED_IN` population -- denominator 191 firm-relative keys
  x 5 candidate buckets = 955 possible triples, of which 137 keys answer from their own props and 54
  answer with nothing.
- **GRAIN:** one edge triple, deduped exactly as the producer dedups (source, edge_type, target).
- **ENVIRONMENT:** in-process reconstruction from the record's measured numbers. No artifact read,
  no AWS call, no run. The baseline numbers came from the cloud artifact published
  2026-09-10T02:15:44Z and the round-6 analysis; this process rebuilds sets of that size and shape.
- **THE CONTROL THAT MATTERS:** arm 2 returns `false` WHILE 955 edges really did arrive from the
  archive -- so the negative is a measured negative and not a dead arm. Plus the remedy arm: the
  same 955 -> 137 numbers with drop-on-read enabled flip the answer to `false` and the artifact to
  137, which shows the probe responds to the MECHANISM and not to the numbers.

### G3-AC5 -- the reading (judgment; no verdict here, graded by `3.0.0_SA_CVO` at L9)

See section 3.

## 3. THE READING (G3-AC5)

### 3a. Do the three carriers really need three owners, or does one remedy move all of them?

**Measured first, argued second.** Over the 21 owned rows: `0.8.0_AE_CloudComp` **14**,
`0.7.0_AE_CloudOps` **6**, `3.0.0_SA_CVO` **1** -- 3 distinct owners, and the split is NOT by
carrier. **Owner is a function of the QUESTION, not of the carrier:** every cadence row is
CloudOps' because all three carriers ride one clock pair; every location row is CloudOps' because
all three live in one bucket; every methodology, persistence, key and failure-mode row is
CloudComp's because all three remedies are producer code. Only one row breaks the pattern -- the
edges coverage row, whose population is the CVO's S96/S97 measurement and whose re-measurement is
the CVO's instrument.

**So the card's premise as literally stated -- three carriers, three owners -- is REFUTED, and the
rule it rests on is confirmed by a stronger case.** Rule 24(iv) says remedies do not move together;
it does not say owners must differ. Here ONE seat holds three DIFFERENT remedies with three
different clocks, and the round proved they do not move together the hard way: cycle 3's props fix
did not touch the edges, cycle 4's edges fix did not touch the nodes, and the nodes remedy STILL
DOES NOT EXIST. A single-owner card with one `owner` field would have read "CloudComp owns the
carry-forward" and been true, useless, and closed -- exactly the shape that let three cells find one
disease three times. The per-row owner is doing its work here not by naming three seats but by
making one seat's three separate obligations countable.

**What would have been lost by carding this as one subject:** the three answers to question 7 (`no`,
`no`, `yes`) would have collapsed into one, and the one that is `yes` -- edges, because the producer
now COUNTS what it drops -- is the remedy pattern the other two need. A single card would have hidden
the answer inside the question.

### 3b. What a fourth carrier would look like, if one exists

The three carded carriers are the three the record found. Two candidates are named on the set card
as explicitly out of coverage, and they are not equal in standing:

1. **EDGE ATTRIBUTES -- the real fourth carrier, and it is uncarded because no instance has been
   observed.** The props remedy lives on NODES only (`_collapse_stitch_copies` visits nodes with
   `source == portal-stitch`); the edges remedy removes whole edges by TYPE. Nothing inspects the
   attributes of a carried edge. So an attribute the producer retires on an edge is in the exact
   state `vocabulary` was in on a node before cycle 3 -- with one difference that makes it worse: the
   node case was found because a served COUNT of the stamp existed to read, and no equivalent count
   exists for an edge attribute.
2. **NODE AND EDGE DELETION as a class** -- named on the set card, but it is the SAME carrier's
   failure mode rather than a new carrier, and saying so is a claim a reader can reject. It is
   recorded as the nodes card's one blocking defect.

**And the honest answer to the question is a warning about the method:** the set's denominator is
its own enumeration. Three carriers were found by three cells hitting three instances; nothing
enumerated carriers, and nothing does now. A fourth carrier will be found the same way the first
three were -- by an instance -- unless someone derives the carrier list from the producer's own
emission surface rather than from the incident history. That derivation is the one piece of work
this card could not do from inside the egress hold, because it needs the producer's emitted
attribute vocabulary and not just its source.

### 3c. What this card obliges of anyone who next builds on this producer

1. **Never read an ABSENCE from this producer's artifact as a RETIREMENT without checking the
   drop-on-read for that carrier.** Edges of type `STORED_IN`: safe, the drop is unconditional and
   counted. Node props in `RETIRED_STITCH_PROPS`: safe for the one key enumerated. Everything else:
   the artifact may be asserting last cycle's answer, and it will do so with a clean exit and a
   plausible count.
2. **Name the carrier when quoting a count from this producer.** "The stitch layer has N members" is
   a sentence with three different truth values in this card set.
3. **Any new emission this producer gains arrives with a drop-on-read AND a count, or with a
   declared reason why its emission can never shrink.** The counted drop is what made the edges
   carrier the only one where a genuine zero is distinguishable from a broken read.
4. **Do not certify a shrink by counting the artifact.** `g2_shrink_probe.py` is the standing
   demonstration: under the archive read the artifact count equals the PRIOR cycle's, so counting is
   precisely the instrument that cannot see the defect.
5. **Cite the vintage.** Every claim in these four cards carries `file:line @ f3b5f26f77` or a row
   id at the commit that minted it, and slot ~1 is editing the two producer files in this same round
   under `CG-s-33`. A card read against a later producer is a card about a different producer.

## 4. Surprises filed

| id | class / hazard | one line |
|---|---|---|
| `NFRA_CLDGRPH-W2-S73` | OBSERVATION / ARMED, disarm `2.0.0_SA_COO~A` | G3-AC2's validator does not exist; the estate's binds v3.1, not the v1 schema the face names, and the two cannot both be satisfied |
| `NFRA_CLDGRPH-W2-S74` | OBSERVATION / INERT | one row per carrier is not expressible in one substrate card on either schema version; delivered as a set card plus three carrier cards |
| `NFRA_CLDGRPH-W2-S75` | OBSERVATION / INERT | two records of the same 21:05Z snapshot population disagree by 20 nodes (1,771 against 1,791), unresolved and unaveraged |

Channel denominator: 245 rows in 186 blocks before this append, **248 in 187 after**, counted by
parsing every fenced json block and summing their lengths. No existing row was edited.

## 5. What this order did NOT do

- **No producer file was written.** `infra/aws/globgrph/derive_stitch.py` and `derive_runner.py` were
  read only; slot ~1 holds them under `CG-s-33` and `git status` on `infra/aws/globgrph/` is clean in
  this worktree.
- **No monitor, alert, checker or schedule was built.** The shrink probe is a one-shot instrument in
  a deliverables folder, wired to nothing, and it says so in its own output.
- **No AWS plane was touched, read or written**, and no snapshot was re-read -- which is why row
  `W2-S75` is filed unresolved rather than answered.
- **No schema was hand-checked and no schema was edited.** The estate's validator was run.
