# CG-s-38 -- THE PORTAL VINTAGE'S FOUR-HOP FEED, AND THE PRODUCER UNDERNEATH IT

TO `NFRA_CLDGRPH.TO-CG-H-3` - worker `0.9.0_WK_NFRA_CLDGRPH~2` - branch `wk-cldgrph-8-2`
in worktree `C:/tmp/wk-cldgrph-8-2`, cut from CLOUD @`2fd5cae09f`. Push state LOCAL.
Acts commit `5c74e16742`. No apply, no run-task, no CodeBuild start, no image act, no S3
write, no zip push -- every state in this record is `DESIRED`, two of them additionally
`LOCAL-EXERCISED`, and none is `APPLIED`.

**THE ANSWER IN ONE PARAGRAPH.** The portal sha now travels the whole feed: the packer
writes `portal_sha.txt` into the archive on BOTH routes, the stitch buildspec stamps it
into the marker, `read_stitch_vintage` copies it as `stitch_portal_sha`, and `_age_line`
renders `" Portal source: <40-hex>."` in the same shape as the stitch clause above it. All
four links were exercised in a local process over real bytes, because every act that would
put them on the served plane is held. The four round-7 line citations were re-derived by
content and **all four still held** -- `PINS_MOVED_SINCE_ROUND7=0 of 4` -- and the only
wrong line number in the chain of records turned out to be in the CORRECTION this order's
own face carried (row `W2-S76`). And the item the CTO kept deliberately is still standing
after this cell closes: **hop 1's KEY now has a committed producer; hop 1's PRODUCER still
has no production home**, because no path in this order's grant is one. That is filed with
its owner, not half-done.

---

## 1. THE FOUR HOPS AT HEAD, RE-DERIVED BY CONTENT

Instrument: `ast.parse` for the two python hops (node kind + function name -- never a line
number as INPUT), literal statement match for the Terraform buildspec and the GitHub
workflow. Coverage: five files, whole-file each. Grain: one AST node / one line.
Environment: this linked worktree, python 3.12.10 on win32, git as the second instrument.
Capture: `h3_ac1_run.txt`.

| hop | site at HEAD | what it now does | owner | STATE this round |
|-----|--------------|------------------|-------|------------------|
| 1 PACK | `.github/workflows/stitch-source-push.yml:85,93` and `.../0.9.0_WK_NFRA_CLDGRPH~2/f3_build_source_zip.py:115` | writes `portal_sha.txt` into the archive beside `stitch_source_sha.txt` | `0.7.0_AE_CloudOps`, with `1.0.0_SA_CTO` to place the hand route's home | **DESIRED** (+ route A exercised on a fixture) |
| 2 STAMP | `infra/aws/terraform/globgrph/stitch-produce.tf`, buildspec marker dict `:177-191` | reads `portal_sha.txt` -> `marker['portal_sha']`, conditionally | `0.7.0_AE_CloudOps` (Terraform plane) | **DESIRED** (+ the extracted block exercised) |
| 3 COPY | `infra/aws/globgrph/kuzu_nessie_load.py:71-77` + the conditional below it | copies it as `stitch_portal_sha`, conditionally | globgrph engine owner (this project) | **DESIRED + LOCAL-EXERCISED** |
| 4 PRINT | `infra/aws/globgrph/projection_worker.py:261-271` | appends `" Portal source: <sha>."` | globgrph engine owner (this project) | **DESIRED + LOCAL-EXERCISED** |

**THE MOVED PINS: ZERO OF FOUR, AND THE FINDING RUNS THE OTHER WAY.** Scored against the
commit this worktree was cut from (`2fd5cae09f`, byte-identical to the issuer's own
measurement commit `de3970331f` on 6 of 6 files this order reads):

| round-7 claim | held at the baseline |
|---|---|
| `f3_build_source_zip.py:84` computes `portal_head`; `workflow:66` is the pin | **true** |
| the buildspec marker dict declares exactly 7 keys | **true** |
| `kuzu_nessie_load.py:71-77` is `read_stitch_vintage`'s return dict | **true** |
| `projection_worker.py:257-262` contains the stitch clause | **true** |

The face's own MEASURED block re-cites hop 3 as `:68-78`. At those same bytes `:68-70` is
the `if not m.get("built_at")` guard with its early `return {}` and `:78` is the `except`
line; the return dict is `:71-77`, exactly where round 7 put it. **A correction is a
measurement and ages the same way the record does** -- filed as row `NFRA_CLDGRPH-W2-S76`,
not because the instruction was wrong (re-derive by content is right, and following it is
the only reason this was visible) but because the re-read done to justify the instruction
produced the only wrong citation of the five.

**AND A SECOND ASSEMBLER NOBODY NAMED.** Before adding a key to hop 3, the writers of the
property were counted rather than recalled. There are **two sites that build the `stitch_*`
vintage vocabulary and ONE that writes it into `source_vintage`**:
`derive_runner.fold_stitch_document:2567-2578` returns a ten-key dict, and its only call
site (`:2736-2742`) tests it for `None`, prints an INFO line and never reads it again --
the name occurs exactly three times in the file. So the portal key needed only the engine
site, and that "only" now has a printed denominator behind it. Row
`NFRA_CLDGRPH-W2-S77`; `derive_runner.py` is outside this order's `<paths>` and is another
slot's live surface this round, so it was named and not touched.

---

## 2. HOPS 3 AND 4 -- LANDED, AND EXERCISED WHERE IT IS HONEST TO

Capture: `h3_ac2_run.txt`. The two production functions were imported from this worktree
and called unmodified; the only substitution is the S3 client, which
`read_stitch_vintage` takes as a parameter for exactly this reason. The marker bytes are
real: `json.dumps` in, the function's own `json.loads` out.

```
ARM 1  marker carries portal_sha -> hop 3 returns 6 keys -> the rendered line is
       "Built from the estate as of 2026-09-10 03:31:02 UTC. Stitch source: stitch-codebuild
        built 2026-09-10T03:01:17Z. Portal source: 5907cbca98eb091124e38a32debefa355c1d4376."
ARM 2  the SAME marker without the key -> 5 keys, no clause, no raise, and the line is
       BYTE-IDENTICAL to the pre-CG-s-38 sentence (NEGATIVE_CONTROL_NO_PORTAL_KEY=CLEAN_OMIT)
ARM 3  no stitch at all -> {} and the bare estate sentence
ARM 4  _age_line re-derived from the same manifest is the same string -- which is the
       equality _validate_manifest_shape actually enforces on every publish
```

Absence is absent at every hop, and that is deliberate three times over: the buildspec adds
`portal_sha` only when `portal_sha.txt` exists, `read_stitch_vintage` copies it only when
the marker carries it, and `_age_line` renders it only when the manifest carries it. An
older source zip, an older marker and an older manifest each produce byte-identical output
to the day before this change.

**`_provenance.format_provenance_header` WAS NOT THE CARRIER AND WAS NOT TOUCHED.** Round 7
exercised it and watched it print 3 of 7 keys handed to it, dropping four in silence
because it hard-codes one branch per `source_kind` with no loop (rows `W3-S17`, `S108`). A
sixth key routed through there would have been equally invisible, and the change would have
passed its own test. `PROVENANCE_PY_MODIFIED=0`, with a live detector control proving that
counter can go non-zero (`h3_ac4_run.txt`).

---

## 3. HOP 1 -- THE DECISION, AND WHAT IT DOES NOT REACH

**BRANCH TAKEN: (a), `HOP1_BRANCH=COMMITTED_PRODUCER`.** Both routes now write the key, and
the whole chain was measured for halves rather than asserted free of them:
`CHAIN_LINKS_PRESENT=8 of 8`, so no hop writes a key its consumer does not read
(`HALF_DONE=false`). Two live exercises, capture `h3_ac3_run.txt`:

- **route A, the one that actually ran**, was executed for real over two throwaway git
  repos and the zip reopened: `portal_sha.txt` reads back equal to the fixture portal HEAD.
- **hop 2's own inline python** was extracted from the Terraform and executed verbatim (the
  only substitution, disclosed in the capture, is its two hard-coded `/tmp` paths): 8 keys
  with `portal_sha.txt` present, 7 without.

**AND HERE IS WHAT (a) DOES NOT BUY, stated so the branch token cannot be misread.** The
route that produces the served zip is still a script in a MISSION DELIVERABLE FOLDER. A
deliverable folder is the record of a completed task order: it has no schedule, no trigger
and no owner outside this project, and it is archived when the mission closes. Three owned
items, each with its blocker and its owner:

| # | blocker | owner |
|---|---------|-------|
| 1 | the route that produces the served zip lives in `org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/`. No path in this order's grant is a production home, so the move cannot be made from here. | `1.0.0_SA_CTO` to place it (which plane owns a repo-subset packer), then `0.7.0_AE_CloudOps` to run it |
| 2 | the committed route pins the portal at a LITERAL sha under a comment saying the pin IS the gitlink sha. At HEAD the gitlink is `5907cbca98eb...` and the pin is `b96562720505...`, and nothing updates it. | `0.7.0_AE_CloudOps` (row `W2-S78`, ARMED, same disarm owner rows `W2-S40`/`W2-S63` carry) |
| 3 | `secrets.PORTAL_REPO_PAT` is unprovisioned, which is why route B has never run and why route A exists at all. | `0.7.0_AE_CloudOps`, with `0.0.0_AB_MSTR` for the repo secret |

Item 2 was deliberately NOT fixed here even though the file is in this order's `<paths>`:
the cell's change is to write `portal_sha` into the archive, changing a production route's
checkout ref is a different change, and under the egress hold no run of the altered route
could be exercised. **An unexercised behaviour change to a production route is precisely
what this estate keeps paying for.**

---

## 4. HOP 2 IS DESIRED AND NOTHING MORE

`HOP2_STATE=DESIRED`. The buildspec lives inside `aws_codebuild_project.stitch_produce`;
until an apply lands, the LIVE project still carries the seven-key marker. The
extracted-block exercise proves the TEXT is correct and proves nothing whatever about the
project. Calling a committed Terraform change anything but DESIRED in this round is the
defect Rule 22's STATE limb names, and this record says it in the same breath as the number
so that no reader of the instance can take the one for the other.

---

## 5. ONE SENTENCE A READER OUTSIDE THIS PROJECT CAN ACT ON

**A production input to the served estate graph -- the source zip every nightly stitch is
built from -- is produced by a script that lives in a mission deliverable folder and is run
by hand; it works, it is now correct, and it has no schedule, no trigger and no owner
outside the project that happened to write it.**

---

## 6. THE READING (`H3-AC5`, judgment -- graded by `3.0.0_SA_CVO` at L9)

**THE READING, WITH NO VERDICT ON IT.**

**(i) IS A PRODUCTION INPUT WITH NO COMMITTED PRODUCER A BIGGER FINDING THAN THE VINTAGE IT
WAS FOUND THROUGH, AND TO WHOM DOES IT BELONG?** Bigger, and the discriminator is
boundedness. The vintage defect is bounded and self-announcing: it affects one clause of
one sentence, the fix is four one-line changes, and once the clause renders, a reader can
SEE whether it is there. The producer defect is unbounded, because it is a property of how
this estate ships production inputs rather than of what any one of them contains -- nothing
about "the zip is packed by hand from a deliverable folder" is specific to the portal sha,
and the same folder can as easily drift on the data-script glob, the exclusion list or the
subtree set, none of which anything downstream would notice. The general form is worth more
than the instance: **an ad-hoc act that succeeds becomes infrastructure silently, unless
something records that it was ad hoc.** The round-6 worker did exactly what its order said
-- build the zip, push it -- and the residue is that a one-off act became the standing
route because it worked, while a committed route with the same name sat unexercised beside
it. Nobody decided that; it is what happens when the two are never compared. OWNERSHIP: not
this project's. The graph project is a CONSUMER of that zip -- it reads the marker the zip
produces -- and a consumer that adopts its supplier's production problem has just widened
its own cell. It belongs to whoever owns the stitch supply chain: `1.0.0_SA_CTO` to decide
which plane owns a repo-subset packer, `0.7.0_AE_CloudOps` to run it. One caution on the
filing itself, from this estate's own measured history: an item routed to a seat that never
asked for it becomes a park, so the un-parking CONDITION belongs on the item. Here it is
concrete -- the PAT. Provision `secrets.PORTAL_REPO_PAT` and the committed route can run,
at which point the hand route is retirable and item 1 resolves by disuse rather than by
migration.

**(ii) IS THE COMMITTED WORKFLOW'S DELIBERATE LITERAL PIN A DEFECT OR A DESIGN WHOSE UPDATE
STEP IS SIMPLY MISSING?** Both, and separating the two is the whole answer. As a DESIGN it
is coherent and I would keep it: pin the portal to the sha the superproject's gitlink
records, so the zip is one HEAD-consistent cut rather than a race between two repositories'
moving heads. As a STATE it is a defect, because the property the comment names -- "pinned
at the gitlink SHA" -- is FALSE at HEAD (`5907cbca` vs `b9656272`) and no mechanism
anywhere keeps it true. The precise name for the failure is not "stale pin" but **an absent
mechanism wearing a comment's clothes**: the sentence describes a state, a description is
never a state, and because the description is in the file that would perform the act, it
reads like an implementation. The cheap remedy makes the claim true by construction -- read
the gitlink in the job (`git ls-tree HEAD portal`) instead of typing it -- and it is not
made here for the reason in section 3. One inversion is worth flagging to whoever picks it
up: this hazard is ARMED BY THE REMEDY TO A DIFFERENT ITEM. While the PAT is missing the
route cannot run and the stale pin harms nobody; the moment the PAT lands, every push to
CLOUD starts packing portal bytes from a commit nobody chose. Fix them in the other order
and the first green build is wrong.

**(iii) DOES DECLARING A PORTAL SHA RESTORE COMPARABILITY FOR THE READER WHO WAS HARMED, OR
ONLY MAKE THE INCOMPARABILITY VISIBLE?** Only visible -- and that is worth doing, but it is
strictly less than the harmed reader wanted and it should not be reported as the fix. Two
graph reads taken four hours apart still differ in their portal half; what changes is that
the difference is now READABLE IN THE ANSWER ITSELF, so a reader can say "these two answers
are not comparable" instead of unknowingly comparing them. That converts a silent
incomparability into a detected one, which is the same move this estate made when it put a
claim field beside a value. Genuine comparability would need something this estate does not
offer for the graph at all: the ability to RE-ASK a question at a named portal vintage. A
label lets you detect the mismatch; only a re-readable pin lets you resolve it. Three
further limits, none of them rhetorical. **First, a sha is an identity, not a date, and
FWD-3's property is that a reader gets a DATE from the answer.** `Portal source:
5907cbca...` tells a reader WHICH portal, not HOW OLD, and the only way to convert one into
the other is to consult a private repository most readers of that line cannot reach. The
packer could record the portal commit date beside the sha and close that gap in one line;
it is not written here because this order's accept names `portal_sha` and widening an
accept from inside is not a worker's act -- it is named instead, as the next cut's
candidate. **Second, the label is preserved as a LABEL at every hop** -- packer, marker,
manifest, age line -- and nothing downstream re-verifies it against the bytes it names, so
a wrong `portal_sha.txt` would travel the whole feed unchallenged. That is acceptable at
the packer (it reads `git rev-parse` on the tree it is packing) and it is exactly the
assumption a reader should be told about. **Third, it declares the portal the ZIP packed,
which is the portal the served graph's portal layer was derived from only because the
stitch derives from that zip.** That chain holds today and it is not stated anywhere a
consumer could reject on. All three are the same species of gap as the one this cell
closed, one level further out, which is the honest thing to say about a fix that made an
invisible problem visible: it did not end the problem, it moved it somewhere a reader can
argue with.

---

## ARTIFACTS

| file | what |
|---|---|
| `h3_hops.py` / `h3_ac1_run.txt` | the four hops re-derived by content, the pins tested at the baseline |
| `h3_local_endtoend.py` / `h3_ac2_run.txt` | hop 3 -> hop 4 over real marker bytes, with the no-portal control |
| `h3_hop1.sh` + `h3_hop1_probe.py` / `h3_ac3_run.txt` | the hop-1 decision, the chain measured for halves, two live exercises |
| `h3_no_apply.sh` + `h3_no_apply.py` / `h3_ac4_run.txt` | six held acts at zero, planted control fired, `_provenance.py` untouched |
| `h3_tree_control.txt` | the one-file positive control: a census that cannot see it read some other tree |

## THE EGRESS HOLD

Honoured and measured, not asserted: `TERRAFORM_APPLIES=0 ECS_RUN_TASK_CALLS=0
CODEBUILD_STARTS=0 IMAGE_PUSHES=0 S3_WRITES=0 ZIP_PUSHES=0 PROVENANCE_PY_MODIFIED=0
EGRESS_PROBE_CONTROL=FIRED`, over 606 executable lines in 4 authored files plus 20 added
lines in the 5 changed files, 204 comment/docstring lines excluded and named, 2 files
excluded by name. The arm's own sharpest edge is printed in the capture: the workflow file
this order edits already contains an S3 copy of the source zip that predates this order by
months, so it is scanned ADDED-LINES-ONLY, and that scoping is a CHOICE stated where a
reader can reject it.

## ROWS

`NFRA_CLDGRPH-W2-S76` (OBSERVATION, INERT) - `NFRA_CLDGRPH-W2-S77` (OBSERVATION, INERT) -
`NFRA_CLDGRPH-W2-S78` (OBSERVATION, **ARMED**, disarm owner `0.7.0_AE_CloudOps`).
