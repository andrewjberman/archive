# CG-s-44 -- A DATED ARCHIVE KEY THAT READS IMMUTABLE AND IS A MUTABLE POINTER

**TO** `NFRA_CLDGRPH.TO-CG-I-4.dated-archive-key-is-a-mutable-pointer` -- worker
`0.9.0_WK_NFRA_CLDGRPH~3`, branch `wk-cldgrph-9-3`, worktree `C:/tmp/wk-cldgrph-9-3`,
HEAD at the acts commit. Round 9. All reads live, no write of any kind (I4-AC4).

---

## THE ANSWER, FIRST

**It is a live evidential problem, not a documentation cleanup, and the thing the cell was
uncertain about is settled in the direction that makes the fix cheaper and more obligatory.**

1. **COUNTED (I4-AC1, `measured`).** In this project's record: **118 dated-snapshot citation
   occurrences across 55 of 539 files read**. **STILL_VALID 21 - OVERWRITTEN 12 -
   UNDECIDABLE 85.** The three classes partition the denominator and the script asserts the
   sum before it prints. Eighty-five citations name bytes that no instrument, now or ever,
   can recover or refute -- the bucket keeps one version, `VersionId 'null'`.
2. **THE OVERWRITE IS NOT CONFINED TO THE KEY THE CELL NAMED (`measured`).** The cell was cut
   on `20260909`. Citations of `20260904` and `20260910` are overwritten too, and the
   producer's own log lines are among the evidence: two derive cycles on 2026-09-10 logged
   `size=1680588` and `size=1680109` for one key whose live length is `1675701`. Three writes
   to one key in one day, and the live bytes are neither of the two the record names.
3. **THE KEY GRAMMAR IS NOT AN UNDOCUMENTED DECISION (`measured`, and this is the finding
   the cell did not have).** Three authorities specify the opposite grammar, and one of them
   is the justification for the bucket having no versioning at all:
   - `docs/architecture/NFRA_GLOBGRPH_PRD.md:191` @`b5bb2f16a0` -- *"Prefix layout:
     `snapshots/{snapshot_date}/graph-{run_id}.tar.gz` (gzip archive, **unique timestamped
     keys**, kept indefinitely -- the time-travel record)"*.
   - `docs/reference/record-retention-policy-v1.md:19` @`b5bb2f16a0`, Andrew-ratified
     2026-06-12 -- Tier 1 **Durable audit record**, retention **Indefinite** *(unique
     timestamped keys -- the time-travel record)*, owner AE 0.7.0.
   - `infra/aws/terraform/shared-infra/s3.tf:302-308` @`b5bb2f16a0` -- *"VERSIONING
     NEVER-ENABLED on purpose: history lives at the Iceberg-snapshot + Nessie-catalog +
     **unique-timestamped-tarball-key** layers, so S3 object-versioning would be redundant
     noncurrent clutter."*

   The producer at `infra/aws/globgrph/derive_runner.py:493` @`b5bb2f16a0` writes
   `f"snapshots/{date_str}/graph-{date_str}.tar.gz"` and has since `0bdf2700b1`
   (2026-06-09), one day after the PRD line. **So the decision to leave the bucket
   unversioned rests on a property the producer has never provided**, and an overwrite of a
   dated key is not merely a lost citation -- it is the destruction of a record the estate's
   ratified retention policy calls indefinite. Filed as row **`NFRA_CLDGRPH-W3-S20`**,
   OBSERVATION / ARMED, disarm owner `0.8.0_AE_CloudComp`.
4. **CHOSEN=WRITER_KEY, BRANCH=FILED (I4-AC2, I4-AC3).** The writer remedy is conformance to
   an existing spec, not a new design decision. It is blocked here twice over -- the
   producer path is not in this order's `<paths>`, and landing it needs an image build and
   deploy the round-9 egress hold forbids by name -- so it is filed with its owners, with the
   six acts that must not be taken meanwhile printed beside it.

---

## WHAT WAS RUN

| criterion | invocation | deciding output | capture |
|---|---|---|---|
| `I4-AC1` | `timeout 120 python .../i4_census.py` | `TREE_READ=WORKTREE` - `TREE_POSITIVE_CONTROL=FIRED` - `CITATIONS_FOUND=118 of 539 file(s)` - `STILL_VALID=21 OVERWRITTEN=12 UNDECIDABLE=85` | `i4_ac1_run.txt`, `i4_census.capture.json` |
| `I4-AC2` | `timeout 120 python .../i4_layers.py` | `REMEDIES_COMPARED=2 of 2` - `AUTHORITIES_RESOLVED=5 of 5` - `CHOSEN=WRITER_KEY` | `i4_ac2_run.txt` |
| `I4-AC3` | `timeout 120 bash .../i4_remedy.sh` | `BRANCH=FILED` - two blockers - owners named - six acts held | `i4_ac3_run.txt`, `i4_restatement.capture.json` |
| `I4-AC4` | `timeout 120 bash .../i4_no_write.sh` | `S3_WRITES=0 ECS_RUN_TASK_CALLS=0 CODEBUILD_STARTS=0 TERRAFORM_APPLIES=0` - `S3_READS` non-zero - `EGRESS_PROBE_CONTROL=FIRED` | `i4_ac4_run.txt` |
| `I4-AC5` | reading, below | no verdict -- graded by `3.0.0_SA_CVO` at L9 | this record |

**The numbers in this table are from the recorded runs.** The AC1 figures rise by seven
between the first run of the census (111 citations) and the recorded one, and the reason is worth stating rather than
smoothing: **this record's own citation table (below) is written in the proposed grammar and
lands inside the census population**, where it classifies STILL_VALID by ETag. A record that
argues for a citation grammar and is not written in it would be arguing from nowhere.

### The four things every number carries

- **INSTRUMENT COVERAGE** -- `i4_census.py`'s own `os.walk`, every file under
  `org/missions/D0/NFRA/NFRA_CLDGRPH` except `.git`/`node_modules`/`__pycache__`/`.venv`/
  `.terraform`, files over 8,000,000 bytes, and files with a NUL in the first 4096 bytes.
  Exclusions are printed with their counts, plus the tree control file and this order's own
  `i4_*` outputs (the capture restates every citation it finds; counting it doubles the
  population on every re-run -- measured at 111 -> 222 before that exclusion existed).
- **HARNESS GRAIN** -- one citation = one regex match of a dated archive key. Not one file,
  not one distinct key. Four distinct keys carry the 118 occurrences. The DENOMINATOR grows
  as this order's own artifacts land in the tree (529 -> 539 files read); the CITATION count
  does not, because this order's i4_* outputs are excluded by name.
- **BASELINE ENVIRONMENT** -- there is no stored baseline. The live table is `s3api
  list-objects-v2` over the whole `snapshots/` prefix (97 objects), read in the same run,
  through `.tools/aws.cmd` (CLI v1) from this worktree, us-east-1.
- **TREE** -- `WORKTREE`, `C:/tmp/wk-cldgrph-9-3`, measured by comparing `--absolute-git-dir`
  against `--git-common-dir`, with a control file that exists only on this branch appearing
  in the sweep's own hits (`TREE_POSITIVE_CONTROL=FIRED`; the same path on `CLOUD` returns
  rc 128).

---

## THE CITED KEYS, IN THE GRAMMAR THIS CELL ARGUES FOR

`bucket/key@ETag`, measured by `s3api head-object` in the I4-AC3 run and captured in
`i4_restatement.capture.json`. Each line also carries what the record does with that key.

- `opal-313476888478-globgrph/snapshots/20260612/graph-20260612.tar.gz@3925738fbea21729290cf6d9ae640e3d`
  -- LastModified `Fri, 12 Jun 2026 02:02:27 GMT`, 71,671 bytes. Cited 35 times: 0
  OVERWRITTEN, 28 UNDECIDABLE. This is the `kuzu_db` tombstone's recovery key, and it is the
  one that has held: it was written once and never re-derived.
- `opal-313476888478-globgrph/snapshots/20260904/graph-20260904.tar.gz@2702e75760a1e171f18bf862ce383328`
  -- LastModified `Fri, 04 Sep 2026 16:38:41 GMT`, 1,657,047 bytes. Cited 3 times, **2 OVERWRITTEN**
  (the record names `15:05:22Z`) and the third is this record's own restatement.
- `opal-313476888478-globgrph/snapshots/20260909/graph-20260909.tar.gz@336e29e366197e43063d372b9002302f`
  -- LastModified `Thu, 10 Sep 2026 00:09:02 GMT`, 1,674,681 bytes. Cited 56 times: 7
  OVERWRITTEN, 39 UNDECIDABLE. **The date in the key is not even the date of the write.**
- `opal-313476888478-globgrph/snapshots/20260910/graph-20260910.tar.gz@ee294f7f3536f0fa7bcc0afe09e97a6a`
  -- LastModified `Thu, 10 Sep 2026 03:02:04 GMT`, 1,675,701 bytes. Cited 24 times: 3
  OVERWRITTEN, 18 UNDECIDABLE.

`get-bucket-versioning` on the bucket returns rc 0 with **no `Status` field**, re-measured in
this cell. Every ETag above is therefore perishable: it names the bytes at that key **as of
this run** and nothing more, which is the whole reason the grammar is worth having.

---

## HOW THE CLASSIFIER DECIDES, AND WHICH WAY IT IS WRONG

A citation is decided only when a discriminator is **attached** to it: this occurrence is the
nearest key in the file to that discriminator, within 300 characters, and the discriminator's
cue is not qualified by another object's name. Everything else is UNDECIDABLE.

- **The bias has a direction and it is stated in the output.** `UNDECIDABLE` is an UPPER
  bound; `STILL_VALID` and `OVERWRITTEN` are LOWER bounds.
- **A loose arm is run and NOT folded in.** If a bare timestamp within 150 characters were
  accepted as a vintage claim, 20 of the 84 no-discriminator citations would read as decided
  (3 STILL_VALID, 17 OVERWRITTEN). Proximity is not attachment, so they stay undecidable and
  the sensitivity is printed instead.
- **A false OVERWRITTEN was found and removed during the build.**
  `f3_marker_capture.json` carries `marker_etag` two lines above `"aws_snapshot": "<a dated
  key>"`, and nearest-neighbour attachment lent the MARKER's ETag to the SNAPSHOT. The
  classifier now refuses a cue carried by a foreign qualifier and **counts the refusals**
  (`FOREIGN CUES REJECTED = 40`). This is the failure mode a proximity classifier produces:
  a confident, well-formed, wrong green.
- **The proposed grammar is read syntactically.** `key@<32 hex>` binds with no proximity
  guess at all. A classifier that only understood `ETag: <hex>` would have scored the very
  grammar this cell argues for as UNDECIDABLE.
- **The live table is one instrument, so it was cross-checked with another.** All four
  distinct cited keys were re-read with `head-object` against the `list-objects-v2` table:
  `CROSS_INSTRUMENT_AGREE=4 DISAGREE=0`. Every verdict in the census shares that one table --
  a check scoped to the members cannot see a defect in what the members share.

## THE DOMAIN, FALSIFIED BEFORE IT WAS TRUSTED

The cell names *this project's record* as the population. That is a narrowing, and choosing a
domain is itself a claim, so the same regex was run **unscoped over the whole worktree**:
**34 further citation occurrences across 18 files, from 29,509 files read**, with 16
files under `.scratch/` excluded by name (this cell's own trial runs restate every key the
census printed; counting them would measure my own output and call it the estate's exposure --
the first unscoped run did exactly that and read 141). Dated-archive
citations live outside this project -- in `infra/aws/globgrph/kuzu_db.TOMBSTONE.md`, in two
`org/critical_paths/change_management/` completion records, in `org/modules/graph/
grain_baseline.json`, in CTO and CVO deliverables and in AE session logs. **The 118 is this
project's exposure and is NOT the estate's**, and no claim here is made about the estate's.

---

## I4-AC5 -- THE READING (no verdict; graded by `3.0.0_SA_CVO` at L9)

**Is a key grammar that reads immutable and is not a naming bug, or a storage-design decision
nobody wrote down?** Neither, and the third answer is worse than both. It is a storage-design
decision that WAS written down -- three times, in a PRD, in an Andrew-ratified retention
policy, and in the Terraform that justifies the bucket's versioning being off -- and then not
implemented. A naming bug is cheap: rename and move on. An undocumented decision is a
conversation: someone decides. **A documented decision that the producer does not implement is
worse than either, because every reader who checks the design finds the right answer and every
reader who checks the world finds the wrong one, and neither has any reason to look at the
other.** The specification is not the weak link here; the weak link is that no instrument
compares the two halves, and nothing in the estate makes a producer prove that the key it
writes is the key its own PRD names. That is the general form worth carrying out of this cell:
**a spec that is never exercised against its producer is not a control, it is a description**,
and this one had held for three months without a single reader noticing that the versioning
argument was resting on it.

**Is an unversioned bucket holding an ARCHIVE defensible?** Yes -- but only under the premise
the Terraform states, and the premise is what makes it defensible, not the storage class. If
every write lands on a unique key, versioning genuinely is noncurrent clutter: the key space
IS the version space, and it is cheaper, greppable and self-describing. The design was sound.
What was never true is the antecedent. **An unversioned bucket whose keys are reused is not a
weaker archive, it is not an archive at all** -- it is a cache with an archive's file names,
and the file names are what everyone reads. The defensibility question therefore cannot be
answered by looking at the bucket. It is answered by looking at the WRITER, and the estate's
own substrate discipline says as much: card the resource, and the card's failure-mode row --
*can a failure be distinguished from a genuine negative?* -- is precisely the row that fails
here. A reader who fetches `snapshots/20260909/graph-20260909.tar.gz` and gets bytes cannot
tell a successful retrieval of the cited object from a successful retrieval of a different
object with the same name. **Both return 200.**

**What should an estate require of a citation before it is allowed into a record later rounds
will lean on?** The estate already answers this for git and does not know it has: rule 22 says
*a citation without a vintage is not a citation*, and gives `file:line @ commit-ish` -- a
content-addressed vintage that a later reader can resolve or fail loudly. There is no
equivalent for an S3 object, and 85 undecidable citations in one project's record is what
that gap costs. The requirement should be the same shape and no larger: **cite a mutable
object as `bucket/key@ETag`, and cite it as `bucket/key` only when the record is explicitly
naming a POINTER rather than bytes.** Three properties earn it: the ETag costs nothing (every
read already returns it); it is checkable by anyone at any later time with one `head-object`;
and when it fails, it fails LOUD -- the ETag differs and the reader knows the referent moved,
instead of reading different bytes under the same name and never finding out. And the
converse belongs in the rule too: **an ETag written beside a citation whose bytes are already
gone would be a fabricated vintage that reads exactly like a measured one.** The 85 stay
undecidable. That is the correct permanent answer for them, and a record that repaired them
would be worse than a record that counts them.

One caution against over-reading this cell: a citation grammar makes movement VISIBLE, which
is strictly weaker than movement not happening. It is the cheap half. The half that preserves
the record is the writer's key, and that one is already specified.

---

## SURPRISE ROW FILED

`NFRA_CLDGRPH-W3-S20` -- OBSERVATION, **ARMED**, disarm owner `0.8.0_AE_CloudComp`,
disposition UNDER_INVESTIGATION. *The dated archive key is a ratified spec the producer never
implemented, and the versioning-off decision rests on the property it lacks.* Filed on
`org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md`; the
file's denominator was restated at that append by parsing every fenced json block -- **283
rows in 212 blocks** (282 before). The header had read 264, so eighteen appends had gone
unrestated; that is stated in the header rather than quietly corrected.

## WHAT THIS CELL DID NOT DO

No S3 write, no derive, no `ecs run-task`, no CodeBuild start, no image act, no
`terraform apply`, no publish, nobody paged. Four arms prove it, one of them the bucket
itself (`OF_THOSE_UNDER_SNAPSHOTS=0` across 187,174 objects read, since this cell's first
read). Six objects under `warehouse/tool_activity/` did move in the window, written by
another actor -- reported rather than filtered, because an arm that has been shown to return
non-zero is worth more than one that has only ever printed clean.
