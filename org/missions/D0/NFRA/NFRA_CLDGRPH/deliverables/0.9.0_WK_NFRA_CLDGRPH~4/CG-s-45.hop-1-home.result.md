# CG-s-45 -- HOP 1'S PRODUCER HAS NO PRODUCTION HOME, AND THE ROUTE THAT SHOULD HAVE HAD IT HAS FAILED 846 TIMES IN A ROW

`NFRA_CLDGRPH.TO-CG-I-5.hop-1-producer-home` - worker `0.9.0_WK_NFRA_CLDGRPH~4`, round 9,
branch `wk-cldgrph-9-4`, worktree `C:/tmp/wk-cldgrph-9-4`, cut from CLOUD @`b5bb2f16a0ad`.
Push state LOCAL. Nothing published, triggered or applied.

---

**THE ANSWER IN ONE PARAGRAPH.** The cell's own framing was that the committed route may
never have run, and that an unrun route is not a route. It has run **854 times** -- 855 by
the time this record was written, and the increment is in section 1.3. It has
succeeded **8**, all of them inside one 103-minute window on 2026-07-07 and every one of
them BEFORE the step that packs `portal/src` existed -- so all 8 published an archive with
zero portal files, which is the exact defect that step was written to fix. Since that step
landed at `4074fdf5ac` (2026-07-07T14:09:20Z): **846 runs, 0 successes**, dying every time
at step 3 on a `secrets.PORTAL_REPO_PAT` that was never provisioned, with the AWS and
publish steps SKIPPED each time. **Correct publishes by the committed route, ever: 0 of
854.** All five zips the estate served this round came from the hand route, each with a
NEVER-2 ledger entry. So the finding is not that a route is unrun -- it is that **a route's
TRIGGER and a route's BODY fail independently, and only the trigger is visible from the
repository.** Everything in the tree describes a working two-leg pipeline because everything
in the tree describes the DESIRED half; the run history is off-repo and nothing in any
checkout points at it. The home is decided on that: `HOME_DECIDED=WORKFLOW`, because the
hand route has no trigger and cannot acquire one without being rebuilt as the workflow it
would replace. The producer is NOT moved -- `BRANCH=FILED`, three owned items with owners
and unblocking acts, because no path in this order's grant is a production location. The
literal pin at `:66` IS fixed: `PIN_DISPOSITION=RESOLVES`.

---

## 1. AC1 -- WHICH ROUTE ACTUALLY RAN

Four instruments on four substrates, each printing coverage, grain, environment and tree.
Two of them are BLIND and both are reported as blind rather than contributing a zero.

| instrument | substrate | denominator | verdict |
|---|---|---|---|
| A GitHub Actions run history | the workflow's own execution plane, off-repo | **854 runs** at first read, **855** in the committed capture (s.1.3), API `total_count`, not a page length | 8 successes, all 2026-07-07 |
| B NEVER-2 deploy ledger | this worktree, walked | **740 files**, tree control FIRED | 5 push entries, all hand |
| C served S3 object + bucket versioning | the served plane | 1 key | versioning OFF -> **BLIND** for write history |
| D CloudTrail S3 data events | the identity plane | window provably containing a write | 0 PutObject -> **BLIND** |

**`WORKFLOW_EVER_RAN=YES`, and the interesting number is the second one.** The run counts
were taken as `total_count` from the API rather than by counting a page, and the earliest
run's `head_sha` is `e32896edd0` -- the commit that introduced the file -- which is the
control that no run predates the read. `RUNS_OTHER` is written as *total minus success minus
failure* so a run state nobody enumerated lands in it visibly instead of disappearing.

**WHY IT FAILS, at step grain, read off two named runs rather than inferred.** Newest run
`34500641548`: step 2 `actions/checkout@v4` success, step 3 `Checkout portal` **failure**,
steps 4 and 5 skipped. Last success `28871059541`: four steps, and **no portal checkout step
among them** -- which is what dates the cut without needing the commit log, though the commit
log agrees (`git log --full-history -S'Checkout portal'` -> `4074fdf5ac`, 2026-07-07T14:09:20Z).

**`ZIPS_ATTRIBUTED=5 of 5`, all HAND_ROUTE, 0 workflow, 0 unattributed.** The attribution
rule was stated before it was applied. The two arms are not the same method twice:

- **Instrument A EXCLUDES.** The workflow's last success of any kind is 2026-07-07T13:45:34Z;
  all five pushes are 2026-09-09/10. The committed route could not have produced any of them
  even if the ledger did not exist.
- **Instrument B IDENTIFIES.** Five entries, each naming `0.9.0_WK_NFRA_CLDGRPH~2`, an order
  (`TO-CG-F-3` once, `TO-CG-F-11` four times) and an `aws s3 cp` of a zip built by
  `f3_build_source_zip.py`.
- **A third axis, labelled INFERRED and not measured.** The served object's `ContentType` is
  `application/x-zip-compressed` (measured). `aws s3 cp` guesses content type with Python
  `mimetypes`; on Windows that reads the registry and `.zip` resolves to exactly that, while
  on the `ubuntu-latest` runner `/etc/mime.types` gives `application/zip`. It discriminates
  the uploader's OS, never its identity, and is offered as agreement, not proof.

**`BLIND_REPORTED=2`, and the CloudTrail one carries the control that makes it a diagnosis
instead of a zero.** `EventName=PutObject` over 2026-09-10T02:00Z..03:30Z returns **0** --
for a window that provably contains a write, since instrument C reads the object's
`LastModified` as 02:46:36Z inside it. The same window with no event-name filter returns
**3 management events**. So the trail is alive and S3 object-level data events are simply not
logged: the one instrument that could have named the writing principal does not exist here.
Without that control, the 0 reads as "nobody wrote the object", which is false.

**Round-label refinement, stated because the face's number is right and its label is loose:**
the five pushes span `TO-CG-F-3` (round 6) and four `TO-CG-F-11` cycles (round 7). The count
of five and the attribution are unaffected; the phrase "round 6's five served zips" covers
two rounds' worth of acts by one worker.

### 1.3 THE LIVE INCREMENT -- the finding confirmed itself during the cell, unasked

The determinism check ran AC1, AC3 and AC4 a second time. Between the two runs **another seat
pushed CLOUD** (`git ls-remote origin CLOUD` moved `61ea3313d8` -> `6226b4a680`), the workflow
fired, and the counts moved:

| | first run 18:2xZ | second run 18:4xZ |
|---|---|---|
| RUNS_TOTAL | 854 | **855** |
| RUNS_FAILURE | 831 | **832** |
| RUNS_SUCCESS | 8 | **8** |
| runs since the portal step | 846 | **847** |
| successes since the portal step | 0 | **0** |

**The population grew by one and the new member was a failure**, live, while this cell was
measuring it. Every number in this record therefore carries a vintage; the committed captures
were regenerated at the later reading, so the record and its evidence agree at 855/847.

**And AC4's attribution arm did exactly the work it was built for.** Probe 2(b) went from 0
runs-since-anchor to 1, and `WORKFLOW_TRIGGERS` stayed **0** -- because probe 2(a) shows this
worker's branch is not on the remote at all, so no run can carry its commits. A probe that
had counted runs-in-a-window and called that "did I trigger anything" would have reported a
violation of the egress hold that never happened. **The discriminator between "a thing
occurred" and "I caused it" is not free and it is not optional.**

**One capture defect this same check caught, worth the line because it is the silent kind.**
The first `i5_ac1_run.txt` opened with a `UnicodeDecodeError` traceback: `subprocess.run(...,
text=True)` decodes with the locale codec, cp1252 on this box, and `gh run view` returned a
byte outside it. The failure lands in a subprocess **reader thread**, so the traceback prints
into the capture, the step-grain block is lost, and **the script carries on and exits 0**. A
corrupted capture that looks like a clean run, under an rc that says PASS. Both scripts now
pass `encoding="utf-8", errors="replace"` explicitly, and the regenerated capture carries the
step-grain block.

## 2. AC2 -- THE HOME, AND WHY THE OBVIOUS READING IS BACKWARDS

**The question "which route is real" has two answers, and they are answers to different
questions.**

**BY OUTCOME the hand route is the only real one.** It is the only route that has ever placed
a correct source zip in the bucket: 5 of 5, against the committed route's 0 of 854.

**BY TRIGGER the committed route is the only real one, and that is the half that decides a
HOME.** Its trigger fired 854 times on exactly the right paths, with the right branch pin,
the right OIDC role, a concurrency group and a PR exclusion. None of that is broken. What is
broken is one repo secret, three steps in.

**The hand route has no trigger at all.** It ran five times because a task order told a worker
to run it five times; that is five instructions, not a cadence. And it cannot acquire one:
the only mechanism in this estate that can fire a repo-subset packer on a repo change IS a
GitHub Action, because the nightly Fargate derive-runner is repo-less -- which is the stated
reason LEG-1 exists at all.

**`HOME_DECIDED=WORKFLOW`**, on those numbers. The consequence is the part worth reading:
`f3_build_source_zip.py` does not need a production home. It needs a **dated interim owner**
and then retirement by disuse. Placing it permanently would ratify a second producer of a
served key on the same day the evidence says the first one is one provisioning act away from
working.

**What I did not decide, said out loud:** I decided where the home IS, on evidence. I did not
decide that the workflow SHALL run -- a GitHub repo secret is outside every agent lane here.
If that act is refused, this decision is void and the estate is back to `HAND_ROUTE` with all
of its costs payable.

### The pin: `PIN_DISPOSITION=RESOLVES`

**The pin was not wrong when it was written, which is what makes it a defect rather than a
mistake.** `git ls-tree 4074fdf5ac portal` reads `b96562720505...` -- exactly the literal --
and `4074fdf5ac` is the commit that added the step. It was a correct snapshot with no update
step, and the comment above it went on asserting a property it had stopped having. At HEAD the
gitlink is `5907cbca98...`.

**Round 8 deliberately did not touch it, and that was right on the evidence it had:** an
unexercised behaviour change to a production route is what this estate keeps paying for. AC1
changed the evidence. The step the pin lives in **has never succeeded, not once in 846
attempts**, so there is no working behaviour to break, and the pin has never been exercised
even as a literal.

**The fix is shaped around a failure mode a naive fix would have introduced.**
`actions/checkout` treats an **empty `ref:` as the repository's default branch**. A resolver
that degraded quietly would publish a zip built from an unrelated portal head, and every
downstream vintage record -- `portal_sha.txt`, the marker, the manifest, the served vintage
line, the whole four-hop feed CG-s-38 built -- would faithfully carry that wrong sha. **A
correct pipeline reporting a wrong input is the worst shape available, and it was one line
away.** So the step tests for 40-hex and exits 1 otherwise.

**STATE, and it is not EXERCISED at the workflow grain: that change is DESIRED.** No run of
the altered workflow can be observed until the PAT exists, and triggering one is inside the
egress hold. **What IS exercised** is the resolver block itself, and the harness does not
transcribe it -- **it extracts the `run:` block from the committed YAML and executes it**, so
it cannot diverge from the file. Three arms, all as expected, disclosed substitutions only
(`GITHUB_OUTPUT` to a temp file; each negative arm swaps the single token `portal`):

| arm | rc | `GITHUB_OUTPUT` |
|---|---|---|
| POSITIVE the committed block, verbatim | 0 | `sha=5907cbca98eb091124e38a32debefa355c1d4376` |
| NEGATIVE a path that is a TREE, not a gitlink | 1 | nothing -- no ref handed on |
| NEGATIVE a path absent from the tree | 1 | nothing -- no ref handed on |

The negatives are the arms that matter. The positive alone would pass just as happily with no
guard at all, so it bounds nothing.

### `ALTERNATIVE_COST`

**If the home had been HAND_ROUTE:** a CTO ruling and a file move (both cheap), then **a
trigger that does not exist and cannot be built without duplicating the workflow** -- a shadow
pipeline and a duplicate output path, on which Andrew holds a complete veto. That cost is
structural, not effort. Plus two permanent writers of one served key, unordered, on a bucket
with versioning OFF, so a collision is not reconstructable afterwards. And the pin question
would not disappear; it would move, since the hand script takes its portal checkout as a
command-line argument -- the same unupdated literal with a human holding it.

**If the pin had been LITERAL-WITH-OWNER:** zero cost today, because the step cannot run
either way -- and the entire cost on the day the PAT lands, when the first successful run in
65 days would pack a 65-day-stale portal and publish it, invisibly, because the vintage feed
works.

## 3. AC3 -- FILED, AND WHY FILING IS THE ACT AND NOT THE FALLBACK

`BRANCH=FILED`. **Not because filing is easier.** The act that makes a workflow the home is
not a file move at all; it is provisioning one repo secret, which no path in any grant here
reaches. And no path in this order's `<paths>` is a production location for a python script,
which the standing law resolves in one line: a path you need that the order lacks is a
blocking row, never an override.

**Nothing is half-moved, and the test for that is unscoped.** A half-move is not detectable by
looking at the destination, because the destination is where you were looking. Over the union
of tracked and untracked files -- **denominator 31,838, excluding nothing** -- on three axes:

| axis | count | where |
|---|---|---|
| by basename `f3_build_source_zip.py` | 1 | the original |
| by sha256 identical to the producer | 1 | the original |
| by a `.py` carrying its docstring line | 1 | the original |

Three axes because one would not do: a rename defeats the basename test, an edit-in-flight
defeats the hash test, a rewrite defeats the token test. `HALF_MOVED=false`.

**A defect this script found in itself, worth one line because it is the cheap kind:** its
first run resolved the repo root by counting `..` segments, miscounted, and landed on a
directory that **still existed** -- so `git status --porcelain -- <absent path>` returned
empty and the script printed **CLEAN on a file that was not there**. Both are fixed: the root
is resolved by `git rev-parse --show-toplevel`, and the CLEAN verdict is guarded on the file
existing. An absent path has no git status, and empty must not render as reassuring.

### The three owned items

| # | item | owner | what unblocks it |
|---|---|---|---|
| **I5-1** | the producer of a served input has no production home; it is production TODAY (5 of 5 zips) and lives in a folder archived at mission close | `1.0.0_SA_CTO` to rule which plane owns a repo-subset packer, then a seat whose `<paths>` includes it | **(a) preferred:** provision the secret (I5-2) -- the item then RETIRES by disuse rather than being satisfied. **(b) fallback:** a CTO ruling naming a path (`.tools/` or `infra/aws/globgrph/`, beside `derive_stitch.py`) plus a grant. (b) buys a home and no trigger. |
| **I5-2** | `secrets.PORTAL_REPO_PAT` unprovisioned -- the whole difference between a route and a dead route; 846 runs, 0 successes | `0.0.0_AB_MSTR` to provision, on Andrew's word (a private-repo credential; availability is not authorization); `0.7.0_AE_CloudOps` to read the first run | one act: a fine-grained or deploy-key-backed token, READ-ONLY on `Opal-Capital/portal`, added as repo secret `PORTAL_REPO_PAT`. The workflow has named it since 2026-07-07. |
| **I5-3** | the cadence change hiding inside I5-2 -- nothing blocks it, it is UNCOSTED | `2.0.0_SA_COO~A` while the mission is open, `1.0.0_SA_CTO` at L10 | be DECIDED before I5-2 is executed, not after. The day the secret lands, a production input that moved 5 times in 65 days starts moving on every qualifying push. That is a NEVER-2 change to a served surface's cadence arriving disguised as a credential. |

**Explicitly not proposed, under the standing moratorium:** any alert, alarm, SNS, SES,
notification, freshness checker or monitor on this workflow, its run history or the zip's age.
This finding was made by reading run history on demand -- an act any seat can take whenever it
wants to know, needing nothing built.

## 4. AC4 -- NOTHING PUSHED, TRIGGERED OR APPLIED

Five probes on five planes, each with a positive control, because **a probe that cannot go
non-zero is a constant wearing a measurement's clothes** and a hold verified by five constants
is not verified. The anchor is the worktree's materialisation time (2026-09-10T17:41:59Z),
computed rather than typed and provably earlier than this worker's first act.

`ZIP_PUSHES=0` `WORKFLOW_TRIGGERS=0` `S3_WRITES=0` `TERRAFORM_APPLIES=0`
`CODEBUILD_STARTS=0` `EGRESS_PROBE_CONTROL=FIRED` (**5 of 5** controls returned non-zero on a
positive case).

The two controls worth naming: `git ls-remote origin wk-cldgrph-9-4` returns empty while
`git ls-remote origin CLOUD` returns a sha -- so the branch's absence from the remote is a
measured absence and no run can carry this worker's commits at all. And the S3 probe, pointed
at `warehouse/tool_activity/`, found **6 objects written to the same bucket after the anchor
by another producer**, which is what makes its zero over the `stitch` prefix worth something.

**The scope of `S3_WRITES` is stated rather than assumed:** the three objects under the
`stitch` prefix, not the bucket, which holds 187,174 objects and has live producers writing
every few minutes. A bucket-wide claim would have been false, and reading it as a violation
would have been a false positive.

**One honest caveat, stated here rather than left to be discovered in a run list:** the
workflow edit means the eventual drain's push to CLOUD will trigger the workflow -- as every
push already does, 854 times so far. It will fail at the portal checkout as its 846
predecessors did, publishing nothing. That is a property of the drain, not an act of this
cell.

## 5. ONE SENTENCE FOR A READER OUTSIDE THIS PROJECT

**A committed, wired, owned CI leg that feeds a served production artifact has fired
faultlessly 854 times and completed 0 of them since July, and nobody knew, because every
artifact in the repository describes the half of a pipeline that is visible from the
repository.**

---

## 6. THE READING (`I5-AC5`, judgment -- graded by `3.0.0_SA_CVO` at L9, no verdict taken here)

**Is a production input with no committed producer a bigger finding than the vintage it was
found through?** Yes, and the run history makes it bigger again than the cell expected -- but
the interesting part is not the ranking, it is that **the vintage question was the only
question that could have found it.** Round 8 was asked whether a portal sha travels four
hops. To answer that it had to open hop 1, and opening hop 1 is what exposed that hop 1's
producer lives in a deliverable folder. Nobody asked "does the source zip have a producer";
that question has no owner, no cadence and no trigger, which is precisely the property it
was asking about. The vintage question was a **detour that happened to pass the defect**, and
the estate should be uneasy that its detection depended on the itinerary.

**And there is a sharper version.** Every seat that touched this pipeline for two months was
correct. The workflow author wired it correctly. The seat that added the portal checkout fixed
a real defect and pinned a real sha. The round-6 worker was told to re-push the source and did
so, with a ledger entry. The round-7 worker cycled it four times, each with a ledger entry.
The round-8 worker made the portal sha travel four hops and filed three owned items naming
this exact blocker. **Nobody was wrong, and the thing stayed broken for 65 days**, because the
only instrument that could see it -- a list of red runs on a website -- is not in the
repository, is not in any graph, is not in any census, and is not read by anything. The cost
of finding it was one API call. The reason nobody made that call is that nothing in the
estate's evidence surfaces points off-repo at all.

**Is a deliberately pinned literal with no update step a design or a defect?** It is a defect
that was born as a design, and the two are distinguishable by a single question that costs
nothing to ask: **does anything move it?** The comment said "pinned at the gitlink SHA (not a
floating DEV ref) for a HEAD-consistent snapshot", and every clause of that was true when it
was written -- I measured it, `git ls-tree 4074fdf5ac portal` returns exactly the literal.
What made it a defect is that the property was stated as an *identity* ("this IS the gitlink")
when it was only an *equality at one moment*, and nothing in the file could tell the two
apart afterwards. The general shape: **a comment asserting a relationship between two values
is a claim that decays, and the way to stop it decaying is to compute one from the other
rather than to write both down.** A pin nobody updates and a pin nobody CAN update look
identical in a diff. The one thing I would add to the estate's habits from this: when a
literal is justified by its relationship to something else, the justification is a
specification for a resolver, not a comment.

**What should an estate require before a hand-run script is allowed to feed a served artifact
five times?** Not more approval -- the five pushes were each properly ordered and each
properly ledgered, and an approval gate would have caught none of it because nothing here was
unapproved. The requirement is narrower and it is about **the record's shape, not the act's
permission**: a hand act against a served surface should have to name **the automated route
it is standing in for, and why that route is not being used.** Every one of the five ledger
entries names its owner, its order and its act. Not one names the workflow it was
substituting for, or that the workflow had failed 800-odd times. Had the first one been
required to say "route B is unavailable because `PORTAL_REPO_PAT` is unprovisioned", the
second push would have been a repeat of a known blocker rather than a fresh instruction, and
five would have been visibly absurd. **A substitution that does not name what it substitutes
for is indistinguishable from the normal way of doing things after the second time**, and by
the fifth it IS the normal way -- which is exactly how this producer came to live in a
deliverable folder.

There is a second requirement, and it is the one I would actually pay for: **an act repeated
by hand N times against the same served key should, at some declared N, stop being an act and
become a defect with an owner.** Five is past that line. The estate has a NEVER-2 ledger that
records each act beautifully in isolation and has no way to notice the fifth one is the fifth.
Every entry is correct; the sequence is the finding; and nothing reads sequences. **I am not
proposing a monitor for this** -- the moratorium forbids it and it would be the wrong remedy
anyway, since the sequence is already in the ledger and already legible to anyone who asks.
What is missing is not a detector. It is the habit of asking, at the moment you write the
fifth entry, *why am I writing a fifth one*.

**Finally, a caution about the number itself.** 846 consecutive failures is a striking figure
and it invites a conclusion it does not support. It does not mean the pipeline is neglected;
LEG-2's CodeBuild ran, succeeded and produced a graph this morning. It does not mean the
served graph is stale in the sense that matters; the hand route kept the source current, five
times, deliberately. What it means is narrower and worse: **the estate's automated path and
its actual path diverged completely, and every artifact describing the system continued to
describe the automated one.** The zips were fresh. The pipeline was dead. Both were true for
65 days, and the record could only see one of them.

---

## ARTIFACTS

- `i5_route.py` + `i5_ac1_run.txt` -- AC1, four instruments, two blind, tree control fired.
- `i5_home.py` + `i5_ac2_run.txt` -- AC2, the decision and the resolver exercise extracted
  from the committed workflow.
- `i5_move.sh` + `i5_ac3_run.txt` -- AC3, the filing and the unscoped half-move test.
- `i5_no_push.sh` + `i5_ac4_run.txt` -- AC4, five probes, five controls.
- `i5_tree_control.txt` -- the branch-only file the tree clause requires.
- `.github/workflows/stitch-source-push.yml` -- the pin now resolves from the gitlink,
  fail-closed. DESIRED at the workflow grain; the resolver block is EXERCISED.

## THE EGRESS HOLD

Every AWS call was a READ (`head-object`, `list-objects-v2`, `get-bucket-versioning`,
`cloudtrail lookup-events`, `codebuild list-builds-for-project`, `batch-get-builds`). Every
GitHub call was a GET against this estate's own repository (`gh api .../runs`, `gh run view`,
`git ls-remote`) -- no dispatch, no re-run, no cancel, no push. No zip built, no zip pushed,
no image act, no CodeBuild start, no Terraform, no S3 write, no act whose effect is an SNS
publish. Nothing touching a topic or a subscription. AC4 measures all of it with controls.

## ROWS

- `NFRA_CLDGRPH-W4-S10` -- OBSERVATION, **ARMED**, `disarm_owner` `0.0.0_AB_MSTR`. The
  committed leg is not unrun; it is 846-consecutive-failures dead and has never once published
  a correct artifact. Armed because the only working producer is a hand script in a folder
  that archives at mission close.
