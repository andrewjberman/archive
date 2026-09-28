# Merge strategy for many worktrees per COO per project -- analysis and proposal

**Author:** `0.0.0_AB_MSTR~Z`, 2026-09-28 ~20:4xZ, on Andrew's ask ("figure out a more effective merge strategy ...
agile and effective without layering on needless process architecture"). Pushes and merges are HELD while this is
read; nothing below has been executed.

## 1. What was measured (origin/CLOUD, last 14 days, site Z)

| Measure | Value | Instrument |
|---|---|---|
| First-parent commits into CLOUD | 4,331 | `git log --first-parent --since=14.days` |
| Merge commits into CLOUD | 501 (432 by COO lanes = drains; 42 by MSTR = device pulls) | same, `--merges`, by author |
| Merges that CONFLICTED | **173 of 500 replayed (35%)** | `git merge-tree --write-tree` on each merge's two parents (read-only replay) |
| Conflicted merges whose ONLY conflicts are surprise-channel files | **154 of 173 (89%)** | per-merge conflict file list |
| Conflicted file rows by class | surprise-channel 163 / portal gitlink 5 / other 6 / log 3 / index-yaml 3 / generated `lambda-source-map.json` 2 / code **2** | of 184 rows |
| Device pulls (`origin/CLOUD` into local) that conflicted | 2 of 23 | same replay |
| Worktrees on site Z | 68: 31 on branches ALREADY MERGED, 32 unmerged, 5 detached; 55 under `C:/tmp` | `git worktree list --porcelain` + `merge-base --is-ancestor` |
| Linked worktrees holding uncommitted files | 55 of 67 (83 files) | `git -C <wt> status --porcelain` |
| Disk held under `C:/tmp` (55 of the 68 worktrees live there) | 70 GB | `du -sh /c/tmp` |
| Surprise-channel file changes that DELETE lines (not pure append) | 129 of 1,802 (7%) | `git log --numstat` on channel paths |

**Reading:** the merge problem is not topology, cadence, or code collisions. It is ONE file class: every worker
branch appends rows to the project's shared `INVESTIGATION_v1.md` while the trunk appends to the same tail, so a drain
collides there by construction. Code conflicted twice in two weeks. The worktree backlog is the second problem: the
drain merges but never tears down, so half the worktrees on disk hold work that is already on the trunk.

## 2. Proposal -- three changes, no new branches, roles or gates

### P1. Each worker writes its surprise rows to ITS OWN file (kills ~89% of conflicted merges)

A worker appends its rows to `surprise-channel/investigations/INVESTIGATION_v<N>.W<n>.md` (its slot number `n`),
never to the shared `INVESTIGATION_v<N>.md`. Seats on the trunk (COO, CVO, CTO) keep writing the shared file.
No two branches then touch the same channel file, so the collision cannot occur -- nothing to resolve, nothing to union.

- **Zero tool change:** every channel reader already globs per-plane (`surprise-row-gate.py:168`
  `investigations/*`; `comp-surprise.py:71` and `proof-of-spec-check.py:1174` `INVESTIGATION_v*`), and a per-writer
  suffix file already exists (`NFRA_OPALAI/.../INVESTIGATION_v1.Z.md`). Row ids stay `<CODE>-W<n>-S<k>`; the
  allocator-coordinate rule is unchanged; the cross-document duplicate-id limb already covers several documents.
- **The edit:** one sentence in the worker agent definitions (`.claude/agents/worker*.md`) and in `/dispatch`'s
  worker face template naming the file. Verify once with a planted row through the row gate and `comp-surprise`.
- **Rejected alternative:** `merge=union` on channel files. 7% of channel edits change lines in place, and the
  duplicate-id limb exempts rows carried by either merge parent (`surprise-row-gate.py:_parent_row_ids`), so a stale
  row kept beside its correction would pass silently -- exactly the hazard `.gitattributes:39` warns about.

### P2. The drain tears its worktree down in the same act

When `safe-merge.sh` lands a `wk-*` branch, it removes that worktree (via `wk-provision.sh remove`, which already
handles the portal nested repo) and deletes the branch. One flag, defaulted on for `wk-*`. A worktree then lives
exactly as long as its task order.

- **Backlog, once:** the 31 merged-branch worktrees and 5 detached ones go through `/cleanup` after a per-worktree
  look at their uncommitted files (55 of 67 hold some; S19 notes most are EOL churn and build clones, but that is a
  per-tree read, not a blanket). The S19 pre-rewrite branches follow their existing verdicts (cherry-pick only).
  Deletion is destructive git: executed on Andrew's word.

### P3. Small residue: let git's own mechanisms take it

- Truly append-only logs (`org/law-edit-audit.log`, `org/mcp/agent-spawn-audit.log`): one `merge=union` line each,
  inside the existing `.gitattributes` precedent's safety bound (lines never edited in place).
- Generated `infra/aws/lambda/ci/lambda-source-map.json`: on conflict, take either side and regenerate -- never
  hand-merge a generated file.
- Portal gitlink: on conflict take the commit that DESCENDS from the other (`merge-base --is-ancestor`); if neither
  does, it is a real divergence for the MSTR.

## 3. What stays exactly as it is

One trunk (`CLOUD`, portal `DEV`); one worker branch per task order cut from `HEAD`; the COO drains its own branches
through `safe-merge.sh`; the MSTR only pulls and pushes between devices. **No per-project integration branches**
(they double every merge and move the collision up a level), no merge queue or bot, no rebase flow.

## 4. Open, for Andrew

1. Approve P1-P3 as written (P1 and P3 are one-line edits in owned files; P2 is one flag in `safe-merge.sh`).
2. Device cadence: pulls are cheap (2 of 23 conflicted); the cost is divergence size, which grows while pushes wait
   (166 behind at this session's start). A standing word for "push after a clean `/integrate` assess" would keep it
   small. Pushes stay on your word either way.
3. Unmeasured, named rather than designed for: wall-clock of a drain's merge-commit hooks in the shared tree with 7
   COOs live. If it proves to be the bottleneck, the measurement comes first (safe-merge timestamps), a structure only
   after.
