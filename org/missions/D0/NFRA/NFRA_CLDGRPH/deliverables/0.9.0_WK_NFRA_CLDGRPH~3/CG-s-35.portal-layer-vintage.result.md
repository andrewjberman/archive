# CG-s-35 -- THE PORTAL LAYER'S VINTAGE, DECLARED OR EXPLAINED

TO `NFRA_CLDGRPH.TO-CG-G-4` - worker `0.9.0_WK_NFRA_CLDGRPH~3` - branch `wk-cldgrph-7-3`
in worktree `C:/tmp/wk-cldgrph-7-3`, cut from CLOUD @`f3b5f26f77`. Push state LOCAL.

**THE ANSWER IN ONE PARAGRAPH.** The portal layer's vintage moved twice in round 6 and BOTH
moves are dated from artifacts and BOTH movers are named: `ABSENT -> 18c0c5cb` at
`2026-09-09T18:47:04Z`, moved by a hand act (`0.9.0_WK_NFRA_CLDGRPH~2`'s TO-CG-F-3 zip build
plus one PutObject, under a NEVER-2 ledger); and `18c0c5cb -> 5907cbca`, first served at
`2026-09-10T02:46:36Z`, whose VALUE was moved by `0.4.0_DT_ClientPlatform` in the portal repo at
`2026-09-09T19:24:56Z` (corroborated by the superproject gitlink bump @`99277222d9`,
`19:41:59Z`) and CARRIED by the same worker's TO-CG-F-11 fourth-cycle push. Nothing declared
either move because **the carrier a reader consults EXISTS AND IS UNFED, not missing** -- the
served VINTAGE line already renders a SECOND source's vintage (the stitch clause) and would
render a portal one, but no upstream hop produces a portal sha to give it. That is the cheap
finding. The expensive part is WHERE the feed breaks: not at the display, but at hop 1, where
the zip that carried every round-6 push was built by a **worker deliverable with no committed
producer**, and the committed route (`.github/workflows/stitch-source-push.yml`) pins a stale
third sha and has produced nothing since 2026-07-07.

---

## 1. THE CENSUS -- both moves, dated from artifacts

Run: `timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/g3_vintage_census.py`
Headline: `PORTAL_VINTAGE_READINGS=3 of 3 dated from an artifact` / `MOVES_OBSERVED=2` /
`RECOLLECTION_USED=0`.

| # | when | value | served instant | instrument (coverage / grain / environment) |
|---|------|-------|----------------|---------------------------------------------|
| 1 | BEFORE | **ABSENT** -- the served zip packs no portal layer | `2026-07-07T13:46:19Z` | zip central-directory listing of the pulled object, `f3_asis_zip_manifest.json`: `portal/` prefix **0 of 7,905 entries**; grain = one zip object, counted PRESENT/ABSENT because there is no sha in the archive to count; env = `0.9.0_WK_NFRA_CLDGRPH~2` at TO-CG-F-3 from a live S3 GET ~18:2xZ. Cross-check `f3_asis_headobject.json`: LastModified AGREES, ContentLength 156,995,002 AGREES with the listing's bytes. |
| 2 | BETWEEN | `18c0c5cb6a26c2c8e9fbfa168dadf04de4344705` | `2026-09-09T18:47:04Z` | the packer's own `git -C <portal> rev-parse HEAD`, `f3_zip_report.json` (`f3_build_source_zip.py:84,128`): **435 of 8,224 entries** under `portal/src`; grain = one 40-hex portal commit per zip object; env = built in `C:/tmp/wk-cldgrph-6-2/.scratch/f3_push` from the MAIN workspace portal checkout, route 2. BOUND to the served object by size: report 181,338,655 == head-object ContentLength. |
| 3 | AFTER | `5907cbca98eb091124e38a32debefa355c1d4376` | `2026-09-10T02:46:36Z` | the same packer's `f11_zip_report.json`, BOUND to a served instant by zip **sha256 `486216313f...`** matched in `CG-s-31.stitch-vocabulary-unified.result.md` (`"served_after": "Thu, 10 Sep 2026 02:46:36 GMT"`): **435 of 8,226 entries**; env = `.scratch/f11/source_cycle4.zip`, route 2 again. |

**MOVE 1** `ABSENT -> 18c0c5cb`, served window `2026-07-07T13:46:19Z -> 2026-09-09T18:47:04Z`.
**MOVE 2** `18c0c5cb -> 5907cbca`, served window `2026-09-09T18:47:04Z -> 2026-09-10T02:46:36Z`.

**THE DENOMINATOR THAT IS THE CELL'S WHOLE POINT.** Round 6 served **5** stitch-source pushes
(`18:47:04Z`, `23:49:34Z`, `01:04:38Z`, `02:13:37Z`, `02:46:36Z`, each dated from a head-object
or `served_after` capture). **2 of those 5** have any committed artifact naming their portal
head. **0 of 5** were declared by a carrier a reader consults. The two moves are datable at all
only because the packer happened to write a scratch report twice.

**WHAT THIS CENSUS DOES NOT ESTABLISH, STATED.** It cannot say at which of the five pushes the
value first became `5907cbca`: the three middle pushes recorded no portal head. The clone's HEAD
was already `5907cbca` by `19:28:09Z` (below), so the second move probably reached the served
plane at `23:49:34Z` and not at `02:46:36Z` -- but no artifact says so, and this record will not
say so either. `02:46:36Z` is the earliest instant the artifacts can BIND to the value.

---

## 2. THE MOVERS -- both named, three limbs each

Run: `timeout 120 python .../g3_mover.py`. Headline: `MOVERS_NAMED=2 of 2` /
`UNNAMED_REPORTED=0` / `NAMED_PLUS_UNNAMED=2` / `MOVER_PROBE_CONTROL=FIRED`.

A move is probed on two limbs -- what made the sha the value the packer would see
(VALUE-SOURCE), and what put that value into the served zip (CARRIER) -- across three
instruments on three different substrates.

**MOVE 1 -- NAMED.** The portal clone did not move for this one: it had been detached at
`18c0c5cb` since `2026-09-01T21:27:35Z`. The whole of move 1 is the PUSH.
- CARRIER: `20260909T184608Z_stitch-source-repush_deploy_completion.md`, opened `18:46:08Z`,
  CLOSED, owner `0.9.0_WK_NFRA_CLDGRPH~2`, order `NFRA_CLDGRPH.TO-CG-F-3`. **A HAND ACT** -- a
  local zip build plus one PutObject. Not a build, not a fold, not the GH-Action route.
- VALUE-SOURCE (background, not the mover): portal commit `18c0c5cb` authored
  `2026-09-01T18:41:15Z` by `0.0.0_AB_MSTR`; superproject gitlink set to it @`a23a6d6681` by
  `0.0.0_AB_MSTR~Z`.

**MOVE 2 -- NAMED, and the mover is OUTSIDE THIS PROJECT.**
- VALUE-SOURCE, instrument A (this repo's object DB): superproject commit `99277222d9`,
  `2026-09-09T19:41:59Z`, author **`0.4.0_DT_ClientPlatform`**, subject
  `bump(0.4.0_DT_ClientPlatform): portal pointer 30ca034b -> 5907cbca; live PROD=b1389c85 ...`.
- VALUE-SOURCE, instrument B (the portal clone's own object DB + reflog -- a DIFFERENT
  substrate, so this is corroboration and not repetition): commit `5907cbca` authored
  `19:24:56Z`, committed `19:28:09Z`, same author; the clone's reflog shows the sequence
  `18c0c5cb --(15:20:21-04:00 feat commit)--> 2d646532 --(15:24:56 merge origin/DEV)-->
  e2c97bca --(15:28:09 amend)--> 5907cbca`, an ANDREW-DIRECT portal feature landing
  33 minutes after TO-CG-F-3's push.
- CARRIER: `20260910T024600Z_cldgrph-cgs31-fourth-cycle-...md`, opened `02:46:00Z`, CLOSED,
  owner `0.9.0_WK_NFRA_CLDGRPH~2`, order `NFRA_CLDGRPH.TO-CG-F-11`, act
  `.scratch/f11/source_cycle4.zip` -> the served key.

**THE PROBER'S CONTROLS.** POSITIVE: probing a sha whose act IS in the record returns a name
(`18c0c5cb -> 0.0.0_AB_MSTR`). NEGATIVE: probing `d3adb33f...` (40 valid hex, in no record)
returns UNNAMED on all three instruments -- so the prober is not a constant that says NAMED to
anything, and `UNNAMED_REPORTED=0` is a finding rather than an artifact of the tool.

**GRAIN CAVEAT, STATED.** The reflog is a LOCAL, PER-CLONE, EXPIRING artifact -- not pushed, not
shared, pruned by default. It is cited only as corroboration of instrument A, which is
durable repository history.

---

## 3. THE CARRIER DECISION -- IT EXISTS AND IT IS UNFED

Run: `timeout 120 python .../g3_carrier.py`. Headline: `EXISTING_CARRIER=true` /
`CARRIER_UNFED=true` / `CANDIDATES_SWEPT=8 of 8`.

| id | candidate | exists for a reader | carries a portal vintage | could, without a new surface |
|----|-----------|--------------------|--------------------------|------------------------------|
| C1 | the served VINTAGE line, `projection_worker._age_line:241-263` | yes | **no** | **yes (EXERCISED)** |
| C2 | the manifest's `source_vintage` dict, `kuzu_nessie_load.read_stitch_vintage:51-79` | yes | no | yes |
| C3 | `_provenance.format_provenance_header:753-857` | **no** | no | **no (EXERCISED)** |
| C4 | the stitch marker `stitch/stitch_marker.json` | yes | no | yes |
| C5 | the served `PORTAL_BUNDLE` node's props, `extract_portal_stitch.py:131-142` | yes | no | yes |
| C6 | `stitch_source_sha.txt` inside the source zip | yes | no | yes |
| C7 | the superproject gitlink | yes | yes (a repo declaration) | n/a |
| C8 | the GH-Action's pinned ref | yes | yes (a STALE declaration) | n/a |

**C1 WAS CALLED, NOT READ.** The function was extracted by AST from
`infra/aws/globgrph/projection_worker.py` and invoked twice. With a stitch-bearing manifest it
returns `Built from the estate as of 2026-09-10 03:02:00 UTC. Stitch source: stitch-codebuild
built 2026-09-10T03:01:17Z.` With the SAME manifest plus `stitch_portal_sha=5907cbca...` it
returns a **byte-identical** string. The extension point is not a hope: the stitch clause is
itself an append CG-s-24 made to this very function, and a portal clause is the same shape.

**C3 MUST NOT BE CHOSEN, AND THIS ORDER'S OWN PREMISE POINTS AT IT.** Handed 7 non-empty
`source_vintage` keys, `format_provenance_header` PRINTED 3 and DROPPED 4 -- including all
three stitch keys `read_stitch_vintage` already injects. The drop is structural: the function
hard-codes one branch per `source_kind` and has no loop over the dict. Filed as
**`NFRA_CLDGRPH-W3-S17`** (ARMED, `disarm_owner 2.0.0_SA_COO~A`). This is a DIFFERENT finding
from `W3-S14` (no serve path calls the function at all): W3-S14 says a reader never reaches it,
W3-S17 says that even if a reader did, the new key would not be there. Each alone leaves the
other undiscovered.

**C7 AND C8 ARE DECLARATIONS, NOT CARRIERS, AND ONE HAS QUIETLY CONVERGED.** The superproject
gitlink at this worktree's HEAD is `5907cbca` -- it now AGREES with the portal actually packed.
It did not on 2026-09-09, when `W2-S40` measured the gitlink at `30ca034b`, an object that did
not even exist in the portal clone. The agreement is a coincidence of `0.4.0_DT_ClientPlatform`'s
bump, not a mechanism: the packer reads `git -C <portal> rev-parse HEAD` and never consults the
gitlink (measured -- the packer contains no `ls-tree` call), so the two can diverge again at any
time with nothing to notice. The GH-Action still pins `b9656272`, a third value that has
described nothing served since 2026-07-07.

---

## 4. THE DECLARATION A READER CAN CITE -- and exactly what it costs

**THE DECLARATION, AS OF THIS RECORD.** The portal half of the served graph is the portal repo
at commit `5907cbca98eb091124e38a32debefa355c1d4376`, authored `2026-09-09T19:24:56Z` by
`0.4.0_DT_ClientPlatform`, packed as 435 files under `portal/src` into the source zip served at
`2026-09-10T02:46:36Z` (sha256 `486216313f...`), from which `opal-stitch-produce` built the
artifact whose marker reads `built_at 2026-09-10T03:01:17Z`, folded into the projection whose
pointer advanced to `2026-09-10T03:02:00`.

**AND HERE IS WHY THAT SENTENCE IS NOT THE FIX.** It lives in a document, not in the answer.
Its falsifier is one line: **the next source push by either route changes the referent and
nothing updates this paragraph.** Citing it a week from now would be exactly the failure the
cell names, one level up. A declaration a reader can cite has to come out of the artifact.

**WHAT BLOCKS ONE, WHOSE IT IS, AND WHAT IT COSTS.** The feed is a four-hop chain. Hops 3 and 4
are two lines on this project's plane. Hops 1 and 2 are not, and hop 1 is the real blocker.

| hop | site | change | owner |
|-----|------|--------|-------|
| 1 PACK | the zip builder for the route that actually runs. `org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f3_build_source_zip.py:84` already computes the portal head and writes it only to a scratch report. The committed route `.github/workflows/stitch-source-push.yml:66` pins a stale sha. | write `portal_sha.txt` into the archive beside `stitch_source_sha.txt` | **`0.7.0_AE_CloudOps`** (the disarm_owner `W2-S40` and `W2-S63` already carry) |
| 2 STAMP | `infra/aws/terraform/globgrph/stitch-produce.tf`, the inline buildspec's `marker` dict (declared keys measured: `built_at, aws_snapshot, git_sha, producer, total_nodes, total_edges, artifact_sha256`; the LIVE marker carries exactly those seven) | one entry, `'portal_sha': ...` | **`0.7.0_AE_CloudOps`** (Terraform plane) |
| 3 COPY | `infra/aws/globgrph/kuzu_nessie_load.py:71-77` | one line beside the five marker fields it already copies | the globgrph engine owner (this project's plane) |
| 4 PRINT | `infra/aws/globgrph/projection_worker.py:257-262` | two lines, the same shape as the stitch clause directly above them | the globgrph engine owner (this project's plane) |

**NOT WRITTEN HERE.** This order is READ ONLY on producer code; every site is named with its
file, its line and its owner, and the next cut carries them. `PRODUCER_FILES_MODIFIED=0`.

**THE ITEM UNDERNEATH, WHICH IS NOT A VINTAGE PROBLEM.** Hop 1 has no committed producer for the
route that produced every served zip in round 6. Five pushes, all by hand, all from a worker
deliverable in a mission folder. A portal vintage is downstream of that; so is the question of
what else the zip's contents depend on that nothing records. Naming this cell "the portal
layer's vintage" and closing it with two display lines would leave that where it is.

---

## 5. THE READING (`G4-AC5`, judgment -- graded by `3.0.0_SA_CVO` at L9, no verdict here)

**(a) Does it mislead a reader TODAY, or only could it?** Today it mostly *could*. The three
names have converged by accident: built portal, gitlink and served zip all read `5907cbca`, so a
reader who resolves "which portal" through the repo gets the right answer for the wrong reason.
It DID mislead during round 6: in the window `18:47:04Z -> 19:41:59Z` the gitlink said
`30ca034b` while the served zip carried `18c0c5cb`, and `30ca034b` was not even an object in the
portal clone -- a reader resolving through the gitlink in that window would have got a sha
naming nothing. The live harm is not misdirection, though: it is **incomparability**. Two graph
reads taken four hours apart in round 6 differ in their portal half and neither answer says so.
`W2-S63` armed exactly that, and this census is its measurement: 5 served pushes, 2 with any
portal record, 0 declared.

**(b) Which of FWD-3's readers would notice?** The diff-taker would. The CTO's whole-graph node
diff already prints a `PROPS_KEY_DELTA` across 27,665 nodes; a portal-layer move would surface
there as portal-layer adds/removes with nothing to attribute them to -- visible, but as noise.
The reader who would NOT notice, and who is the actual exposure, is anyone who takes ONE read
and cites its VINTAGE line: that line names the estate vintage and the stitch build and stops.
Worth putting in front of the L9 seat specifically: round 6's own stability argument
(`ROUND_ANALYSIS.round6.md` s.3, "the five magnitudes held UNCHANGED across three successive
served vintages ... they held while things changed") spans a window in which the portal half
moved from `18c0c5cb` to `5907cbca`. It does not overturn the sign -- the file count was 435 on
both sides and the five magnitudes are measured quantities -- but "things changed" did not
know it included the portal commit, and a stability claim is stronger when it can name the
variables it held constant and the ones it did not.

**(c) Does the fix belong to this project's plane at all?** Split, and the split is the point.
The two DISPLAY hops are this project's engine and are genuinely cheap. The two FEED hops are
not: they belong to whoever owns the portal extract route, and `0.7.0_AE_CloudOps` already holds
the disarm on `W2-S40` and `W2-S63`. If the whole cell is treated as a globgrph display item,
hops 3 and 4 will land, the served line will gain a clause, and the clause will render nothing,
because `source_vintage` will still have no portal key -- a change that passes its own test and
alters nothing a reader sees. That is the same failure mode as routing the remedy to
`format_provenance_header` (`W3-S17`), arriving from the other direction. Rule 28's sentence
covers this exactly: every row carries its owner because remedies do not move together.

---

## ARTIFACTS

- `g3_vintage_census.py` - `G4-AC1`, the three readings and the two moves.
- `g3_mover.py` - `G4-AC2`, the movers with their controls.
- `g3_carrier.py` - `G4-AC3`, the eight candidates, two of them exercised.
- `g3_no_producer_change.sh` - `G4-AC4`, `PRODUCER_FILES_MODIFIED=0 ALERTS_BUILT=0
  EGRESS_ACTS=0 CONTROL=FIRED`.
- `NFRA_CLDGRPH-W3-S17` in `.../surprise-channel/investigations/INVESTIGATION_v1.md`.

## THE EGRESS HOLD

Honoured in full and measured, not asserted: no `ecs run-task`, no CodeBuild start, no image
build or push, no digest re-pin, no `safe-apply`, no zip push, no act whose effect is an SNS
publish. This order made **no AWS call of any kind** -- the client library appears zero times in
its four executables, which bounds every AWS act at once. Every reading above comes from a
committed artifact, from git, or from calling a producer function in-process on a temporary
fixture. The 02:00Z and 03:00Z scheduled fires are the estate's own and were neither stopped,
started nor imitated.
