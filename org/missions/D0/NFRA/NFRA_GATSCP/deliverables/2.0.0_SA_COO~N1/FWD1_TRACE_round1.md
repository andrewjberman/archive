# NFRA_GATSCP round 1 -- FWD-1 one real run (issuer 2.0.0_SA_COO~N1, 2026-10-09 08:2xZ-08:36Z, dell1)

**Arrangement:** CTO ruling J (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_BATCH_20261009T0550Z.md` @85ff358078): PLAN B.
The two errors were placed on the never-pushed QA branch `qa/gatscp-fwd1` (worktree `/c/Dev/qa-gatscp-fwd1`, since removed; the
branch is kept on dell1 as the record), based on box/dell1 85ff358078, which carried GS-t-1 and GS-t-2 and not GS-t-3.
Bystander: IRPT_FNTEND (status closed). Tools: those at the QA branch's HEAD, run from an ordinary seat shell.

## Result

| step | act | commit | outcome |
|---|---|---|---|
| 1 | place: IRPT_FNTEND row W1-S15 `surfaced_at` non-UTC; `project.json` dep_stage EXECUTING->DECOMP, index not regenerated | staged | row gate rc 1 (in-act NEW failure + in-place mutation); tree hook rc 1 (in-act INDEX-DRIFT) |
| 2 | the placement committed on the QA branch only (plumbing, per ruling J) | 451f4a7716 | -- |
| 3 | the REAL DRAIN: worker 0.9.0_WK_NFRA_GATSCP~2's GS-t-3 commit 3d465ade72 merged by `.tools/safe-merge.sh` (in-tree path; two conflicts resolved and re-entered with `--continue`) | 96efab3b0c | LANDED; `STANDING IRPT_FNTEND surprise-corpus ... IRPT_FNTEND-W1-S15 /surfaced_at` and `STANDING IRPT_FNTEND INDEX-DRIFT org/projects/IRPT_FNTEND.json`; 0 in-act |
| 4 | the SYNC: `box-sync.sh grade` (GS-t-3's real grade), then `safe-merge.sh` fast lane landing origin/box/dell2 @976d2e685e (45 commits) | dfa7e833ed | LANDED, 60 paths, dropped 0; graded 0 of 60 -> SKIP, nothing printed (row D1-S3) |
| 5 | restore of both files to 85ff358078 | 241c069351 | `safe-commit` refused it on the row gate's append-only limb (an in-place restore mutates the act's own row); the tree hook passed the restored row (0 in-act, 0 STANDING); committed on the QA branch by plumbing |
| 6 | history read | -- | no commit touched IRPT_FNTEND between placement and restore; `qa/gatscp-fwd1` absent from origin (ls-remote empty) |

The origin/CLOUD sync attempted first had nothing to take (QA 0 behind CLOUD; `grade` SKIP, graded 0/0); box/dell2 was taken instead.

## What this shows and does not show

- Both standing errors were printed and named to their project by the DRAIN, and the drain landed beside them. Nobody repaired.
- The sync landed beside them and printed nothing: its graded path set was empty, so neither gate ran (row D1-S3, for the round-1
  analysis). FWD-1's "both errors printed" is met by the drain alone.
- The QA branch is a QA location (spine v3.18); no shared branch carried a placed error.

## Raw output (line-ending warnings removed)

### 01_place_gates.txt

```
2026-10-09T08:30:18Z
== row gate, act = the placed channel document
[surprise-corpus] REFUSED: 1 NEW failure(s), 0 RESOLVED baseline tuple(s). The set moved.
[surprise-row-gate] BLOCKED -- 2 violation(s) on NEW rows:
    org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md: EXISTING row IRPT_FNTEND-W1-S15 was MUTATED in place (content hash 771187b7b303 -> fca41b01c043). Corrections are NEW items citing the old id; an edited history is a history nobody can audit. A remediation row's own clocks may advance in place (disarm ARMED->DISARMED with `at`, remediation OPEN->REMEDIATED or OPEN->CLOSED_UNREMEDIATED adding only `remediation.closure`, closed false->true, nothing else changed).
    standing corpus pass REFUSED -- see the [surprise-corpus] lines above
    override (audited) ON A COMMIT: put '# surprise-row-override: <reason>' in the commit message body and commit via .tools/safe-commit.sh -- it audits the line, then exports SURPRISE_ROW_OVERRIDE for the hook.
    ON A MERGE (safe-merge.sh) THERE IS NO OVERRIDE PATH: the merged index is graded BEFORE a merge commit message exists, and safe-merge sets no override variable. Fix the state the violation names, or route it to the gate's owner (1.0.0_SA_CTO).
[surprise-row-gate] input: 1 path(s) from the STAGED environment variable (argv was empty; the ~32 KB argv cliff, 0.0.0_AB_MSTR 94338)
[surprise-corpus] DENOMINATORS: documents=339 rows=10077 malformed_blocks=0 failures=5 baseline=4 known=4 new=1 resolved=0
  NEW      org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md  IRPT_FNTEND-W1-S15  /surfaced_at  71eefb651595
  KNOWN    org/surprise_channel/D1_CATVIEWS/INVESTIGATION_v1.md  D1_CATVIEWS-S8  /disposition
  KNOWN    org/surprise_channel/ETFS_INGEST/INVESTIGATION_v1.Z.md  ETFS_INGEST-Z-S37  /disposition
  KNOWN    org/surprise_channel/ETFS_POSITIONING/INVESTIGATION_v1.md  ETFS_POSITIONING-S14  /hazard_standing
  KNOWN    org/surprise_channel/POSN_TENANCY/INVESTIGATION_v1.md  POSN_TENANCY-S3  /surfaced_at
[surprise-corpus] SCOPE: act_documents=1 in-act findings=1 (new=1 malformed=0) STANDING=0 (new=0 malformed_docs=0) resolved=0
[surprise-row-gate] org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md: 0 new row(s) of 278 total checked (278 pre-existing, NOT re-graded)
rc=1
== tree hook, act = the placed tree row
BLOCKED: missions-tree-check -- the project tree's validator REFUSES this commit (staged: org/missions/D9/IRPT/IRPT_FNTEND/project.json )
missions-tree-index check: tree=50 project(s) under 11 directive folder(s), 50 valid | flat index rows=398 (generated=50, hand-written=348, parse-errors=0) | DIRECTIVES.yaml: 84 entries across 15 directives | MACROS.yaml: 11 of 11 directive(s) RATIFIED
  ACT SCOPE: in-act=1 STANDING=0 (act projects: IRPT_FNTEND)
  [INDEX-DRIFT] org/projects/IRPT_FNTEND.json: dep_stage: index='EXECUTING' tree='DECOMP'
RESULT: 1 violation(s) in the act's projects, 0 STANDING  (denominators on the first line)
  remedy: fix the state the violation names (R5 = the register's members list, 0.0.0_AB_MSTR's lane); never bypass.
rc=1
placement=451f4a7716ada3c2bde8b49b3a515ecb6df617ea base=85ff35807862ec8384c1239ba2a12b11547c1961
```

### 02_drain.txt

```
2026-10-09T08:31:01Z
safe-merge: merging '3d465ade72' with --no-commit (the index will be graded before anything lands)
Auto-merging .tools/box-sync.sh
CONFLICT (content): Merge conflict in .tools/box-sync.sh
Auto-merging org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md
CONFLICT (content): Merge conflict in org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md
Auto-merging org/missions/D0/NFRA/NFRA_GATSCP/task-orders/NFRA_GATSCP.TO-GS-t-3.merge-graded-by-scoped-tree-check.md
Automatic merge failed; fix conflicts and then commit the result.
safe-merge: *** CONFLICT -- THE MERGE IS OPEN AND NOTHING HAS LANDED. ***
            2 conflicted path(s):
              .tools/box-sync.sh
              org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md
            An append-only channel conflicts on EVERY concurrent drain -- this is the
            normal path, not the exception (NFRA_CLDGRPH-S36).
            RESOLVE, then re-enter so the guards actually run:
                bash .tools/safe-merge.sh --continue
            Or give up cleanly:  bash .tools/safe-merge.sh --abort
            STOP: Do NOT finish this with a bare `git commit` -- that is precisely the
            hand-merge that runs no index guard and no row gate.
rc=4
== --continue 2026-10-09T08:32:23Z (resolved: box-sync.sh = worker's merge_tree_of + CRO~A's CLOUD_SIDE; channel = union of 7 rows)
safe-merge: --continue on '3d465ade72' -- 0 unresolved, 0 foreign staged path(s)
safe-merge: grading the MERGED index -- 3 of 5 staged path(s) (introduced by the merge or changed on both sides)
[surprise-corpus] DENOMINATORS: documents=339 rows=10080 malformed_blocks=0 failures=5 baseline=4 known=4 new=1 resolved=0
  KNOWN    org/surprise_channel/D1_CATVIEWS/INVESTIGATION_v1.md  D1_CATVIEWS-S8  /disposition
  KNOWN    org/surprise_channel/ETFS_INGEST/INVESTIGATION_v1.Z.md  ETFS_INGEST-Z-S37  /disposition
  KNOWN    org/surprise_channel/ETFS_POSITIONING/INVESTIGATION_v1.md  ETFS_POSITIONING-S14  /hazard_standing
  KNOWN    org/surprise_channel/POSN_TENANCY/INVESTIGATION_v1.md  POSN_TENANCY-S3  /surfaced_at
STANDING IRPT_FNTEND surprise-corpus org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md IRPT_FNTEND-W1-S15 /surfaced_at
[surprise-corpus] SCOPE: act_documents=1 in-act findings=0 (new=0 malformed=0) STANDING=1 (new=1 malformed_docs=0) resolved=0
[surprise-corpus] OK: the act's documents are clean against the baseline (4 known, 1 STANDING outside the act, 0 resolved).
[surprise-row-gate] org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md: MERGE COMMIT -- foreign-row sweep exempt for 3 row(s) a PARENT carried, attributed to 1 seat(s) (0.9.0_WK_NFRA_GATSCP) and graded at their own authorship. The integrator is not their author (0.0.0_AB_MSTR 94283; boundary (b) 3.0.0_SA_CVO 94299).
[surprise-row-gate] org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md: 3 new row(s) of 7 total checked (4 pre-existing, NOT re-graded)
[surprise-row-gate] OK: 1 file(s), all new rows carry their step-7/step-10 fields.
safe-merge: committing the merge as 2.0.0_SA_COO~N1 (from the index snapshot taken right after the merge; a peer's later staging cannot enter it)
[one-writer] OK: merge commit -- 1 append-only path(s) carried from the merged side, exempt
[surprise-row-gate] input: 5 path(s) from the STAGED environment variable (argv was empty; the ~32 KB argv cliff, 0.0.0_AB_MSTR 94338)
[surprise-corpus] DENOMINATORS: documents=339 rows=10080 malformed_blocks=0 failures=5 baseline=4 known=4 new=1 resolved=0
  KNOWN    org/surprise_channel/D1_CATVIEWS/INVESTIGATION_v1.md  D1_CATVIEWS-S8  /disposition
  KNOWN    org/surprise_channel/ETFS_INGEST/INVESTIGATION_v1.Z.md  ETFS_INGEST-Z-S37  /disposition
  KNOWN    org/surprise_channel/ETFS_POSITIONING/INVESTIGATION_v1.md  ETFS_POSITIONING-S14  /hazard_standing
  KNOWN    org/surprise_channel/POSN_TENANCY/INVESTIGATION_v1.md  POSN_TENANCY-S3  /surfaced_at
STANDING IRPT_FNTEND surprise-corpus org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md IRPT_FNTEND-W1-S15 /surfaced_at
[surprise-corpus] SCOPE: act_documents=1 in-act findings=0 (new=0 malformed=0) STANDING=1 (new=1 malformed_docs=0) resolved=0
[surprise-corpus] OK: the act's documents are clean against the baseline (4 known, 1 STANDING outside the act, 0 resolved).
[surprise-row-gate] org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md: MERGE COMMIT -- foreign-row sweep exempt for 3 row(s) a PARENT carried, attributed to 1 seat(s) (0.9.0_WK_NFRA_GATSCP) and graded at their own authorship. The integrator is not their author (0.0.0_AB_MSTR 94283; boundary (b) 3.0.0_SA_CVO 94299).
[surprise-row-gate] org/missions/D0/NFRA/NFRA_GATSCP/surprise-channel/investigations/INVESTIGATION_v1.md: 3 new row(s) of 7 total checked (4 pre-existing, NOT re-graded)
[surprise-row-gate] OK: 1 file(s), all new rows carry their step-7/step-10 fields.
[to-pipeline-gate] OK: MERGE COMMIT -- task-order checks exempt; merged orders were gated at their own authorship, on their own fabric's spine version (0.0.0_AB_MSTR 94264; siblings owned-paths-check.sh:85, surprise-row-gate.py).
STANDING IRPT_FNTEND INDEX-DRIFT org/projects/IRPT_FNTEND.json dep_stage: index='EXECUTING' tree='DECOMP'
OK: missions-tree-check -- 3 tree/register path(s) staged; RESULT: 0 violation(s) in the act's projects, 1 STANDING  (denominators on the first line)
[qa/gatscp-fwd1 96efab3] drain: merge 3d465ade72 (row gate clean on the merged index)
 Author: 2.0.0_SA_COO~N1 <2.0.0_SA_COO~N1@opal.agent>
safe-merge: tree check 96efab3b0c: branch needed 5 file(s), dropped 0, foreign 0
safe-merge: MERGED and committed -- 96efab3b0c
safe-merge: remember the drain's remaining steps -- remove the worktree and its branch explicitly.
safe-merge: index check 96efab3b0c: 0 of 5 merged path(s) differ between the index and HEAD
rc=0
```

### 03_sync.txt

```
2026-10-09T08:32:57Z sync: QA 96efab3b0cdd0d3797bf5921b503887a5b017383 <- origin/CLOUD 393790d6ad4d11054e8b916f3d4c69447fca2817; behind=0
== box-sync.sh grade (real tool, read-only)
box-sync: grade SKIP -- the merge introduces nothing and no path changed on both sides
box-sync: grade 96efab3b0c + 393790d6ad -> PASS (graded=0/0); nothing landed, no ref moved
rc=0

2026-10-09T08:33:36Z sync 2: QA 96efab3b0cdd0d3797bf5921b503887a5b017383 <- origin/box/dell2 976d2e685e6febbe9df2c8d4e0acb503c6558e2d (45 commits QA lacks)
== box-sync.sh grade
box-sync: grade SKIP -- the merge introduces nothing and no path changed on both sides
box-sync: grade 96efab3b0c + 976d2e685e -> PASS (graded=0/60); nothing landed, no ref moved
rc=0
== safe-merge.sh (fast lane) lands it
safe-merge: fast lane -- grading 0 of 60 merged path(s) (introduced by the merge or changed on both sides)
safe-merge: SKIP -- the merge introduces no content of its own and no file changed on both sides; each side was graded at its own commit (Andrew ~19:1xZ)
safe-merge: tree check dfa7e833ed: branch needed 60 file(s), dropped 0, foreign 0
safe-merge: MERGED and committed -- dfa7e833ed (fast lane: no merge was opened in this worktree; land 0.96s)
safe-merge: index check dfa7e833ed: 0 of 60 merged path(s) differ between the index and HEAD
rc=0
```

### 04_restore.txt

```
2026-10-09T08:34:07Z restore
  [risk-reflex] comp-pulse diff -- THE PRE-COMMIT RISK REFLEX (NFRA_NERVES L5)
  [risk-reflex]   INVOCATION (pin beside any quoted result): cmd=diff days=7 top=8 (argv: diff org/missions/D9/IRPT/IRPT_FNTEND/project.json org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md)
  [risk-reflex]   danger map: 0.1h old
  [risk-reflex]   DENOMINATOR: 2 file(s) checked against 1662 danger node(s)
  [risk-reflex]   ANSWER STATE: PRESENT_WITH_ZERO_RESULTS
  [risk-reflex]   REFLEX CLEAN -- a MEASURED result (map read, every file checked), not a default.
  [risk-reflex]   WITHIN BUDGET: scanned 2 of 2 file(s); budget: 90 s (default), used 0.01596589999826392 s
  [commit-gate] WARN: commit-gate checked 0 of 2 file(s) -- NOTHING WAS CHECKED.
  [commit-gate]       This line is NOT evidence of a clean gate. This gate reads only .py / .sh / .tf / org/projects/*.json; every other suffix falls through unexamined.
  [commit-gate]       Do NOT cite it as validation for a frontend artifact -- use the language-appropriate instrument (tsc -b, eslint, a read render).
  [naming-gate] DENOMINATOR: 1 path(s) in this diff; declaration-tree domain = 1 MINUS EXCLUDED(org/, docs/, run-artifact dirs ^workflows/[^/]+/[^/]+/[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7,40}/) 1 = 0 path(s) [of the excluded, 0 are run artifacts and 1 are org//docs/]
  [naming-gate] COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 0 seen
  [naming-gate] NAMING-GATE: PASS 0 graded
  [to-pipeline-gate] OK: no task_orders/*.md in this commit (denominator: 2 dispatched path(s), 0 staged-added).
ERROR: BLOCKED -- surprise-channel row gate (steps 7/10). Commit aborted.
       Unstaged 2 file(s) staged by THIS call; none remains staged; staging from before it is untouched.
  [surprise-row-gate] BLOCKED -- 1 violation(s) on NEW rows:
      org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md: EXISTING row IRPT_FNTEND-W1-S15 was MUTATED in place (content hash fca41b01c043 -> 771187b7b303). Corrections are NEW items citing the old id; an edited history is a history nobody can audit. A remediation row's own clocks may advance in place (disarm ARMED->DISARMED with `at`, remediation OPEN->REMEDIATED or OPEN->CLOSED_UNREMEDIATED adding only `remediation.closure`, closed false->true, nothing else changed).
      override (audited) ON A COMMIT: put '# surprise-row-override: <reason>' in the commit message body and commit via .tools/safe-commit.sh -- it audits the line, then exports SURPRISE_ROW_OVERRIDE for the hook.
      ON A MERGE (safe-merge.sh) THERE IS NO OVERRIDE PATH: the merged index is graded BEFORE a merge commit message exists, and safe-merge sets no override variable. Fix the state the violation names, or route it to the gate's owner (1.0.0_SA_CTO).
  [surprise-corpus] DENOMINATORS: documents=339 rows=10089 malformed_blocks=0 failures=4 baseline=4 known=4 new=0 resolved=0
    KNOWN    org/surprise_channel/D1_CATVIEWS/INVESTIGATION_v1.md  D1_CATVIEWS-S8  /disposition
    KNOWN    org/surprise_channel/ETFS_INGEST/INVESTIGATION_v1.Z.md  ETFS_INGEST-Z-S37  /disposition
    KNOWN    org/surprise_channel/ETFS_POSITIONING/INVESTIGATION_v1.md  ETFS_POSITIONING-S14  /hazard_standing
    KNOWN    org/surprise_channel/POSN_TENANCY/INVESTIGATION_v1.md  POSN_TENANCY-S3  /surfaced_at
  [surprise-corpus] SCOPE: act_documents=1 in-act findings=0 (new=0 malformed=0) STANDING=0 (new=0 malformed_docs=0) resolved=0
  [surprise-corpus] OK: the act's documents are clean against the baseline (4 known, 0 STANDING outside the act, 0 resolved).
  [surprise-row-gate] org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md: 0 new row(s) of 278 total checked (278 pre-existing, NOT re-graded)
rc=1
== tree hook on the staged restore of the row
fatal: cannot change to '/c/Dev/qa-gatscp-fwd1': No such file or directory
OK: missions-tree-check -- 1 tree/register path(s) staged; RESULT: 0 violation(s) in the act's projects, 0 STANDING  (denominators on the first line)
rc=0
restore=241c0693515522fa55ea7a97551c03b1796790ea
```

### 05_history.txt

```
2026-10-09T08:35:44Z history read: first-parent commits on qa/gatscp-fwd1 since 85ff358078
241c069351 2.0.0_SA_COO~N1 qa-restore(NFRA_GATSCP FWD-1 close, 2.0.0_SA_COO~N1): IRPT_FNTEND's two files restored byte-for-byte to 85ff35807
dfa7e833ed 2.0.0_SA_COO~N1 drain: merge 976d2e685e6febbe9df2c8d4e0acb503c6558e2d (fast lane: no merge opened in the shared tree; row gate on
96efab3b0c 2.0.0_SA_COO~N1 drain: merge 3d465ade72 (row gate clean on the merged index)
451f4a7716 2.0.0_SA_COO~N1 qa(NFRA_GATSCP FWD-1 close, 2.0.0_SA_COO~N1): PLACED on the never-pushed QA branch only (CTO ruling J @85ff358078
== commits touching IRPT_FNTEND between placement 451f4a7716 and restore 241c069351 (exclusive), all parents:
(end; empty = nobody repaired)
== pushed? ls-remote for qa/gatscp-fwd1:
(end; empty = never pushed)
```
