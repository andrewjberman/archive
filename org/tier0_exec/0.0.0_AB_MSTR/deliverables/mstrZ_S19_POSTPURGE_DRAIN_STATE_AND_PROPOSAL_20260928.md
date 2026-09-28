# SITE Z POST-PURGE DRAIN -- STATE AND PROPOSAL

**Author:** `0.0.0_AB_MSTR~Z`. **Written:** 2026-09-28 ~17:2xZ. **Status:** PROPOSAL -- nothing in section 4 or 5
has been executed.

**Why this exists (Andrew-direct, 2026-09-28 at the site Z MSTR terminal, verbatim):** *"Yeah we need to figure
out how to parse through all of this and get it properly drained and merged. I am holding all future work on this
fabric until this is managed. I will keep the cuirrent agents online to facilitate this work: CTO~Z, CTO~O, and
CVO~O. Until all worktrees are drained/analyzed/merged (or superseded if anything is really duplicated/obsolete
work), only then can we restart work. The machine in the current state is running very slowly so if that is going
to be a substantial amount of work then we need to figure out how to establish this as a proposal/state document
and we pick it back up post reboot on sitez."* (Typos his.)

**IT IS A SUBSTANTIAL AMOUNT OF WORK.** Section 2 is the measurement that says so. This document is written to
survive the reboot and to be the first thing read after it.

---

## 1. WHERE THE REPOSITORY ACTUALLY IS

| fact | value |
|---|---|
| `origin/CLOUD` | **REWRITTEN** by the S19 purge (laptop force-push, ~16:0xZ) |
| site Z local `CLOUD` | still on the **PRE-rewrite** history |
| has site Z fetched since the rewrite | **NO**, deliberately |
| my frozen tip and its new hash | `8cf46e0802` -> `009b8f8cf6` (from the laptop's commit map) |
| local `CLOUD` commits made after the frozen tip | **15** -- these need replay onto the rewritten base |
| push freeze | **ON** (pushes only; commits were and remain legal) |

⛔ **THE PRE-REWRITE HISTORY IS NOT AT RISK.** This repo's own 69 local branches still point into it, so the
objects are reachable and nothing is pending garbage collection. A mirror also exists at
`<session scratchpad>/s19-mirror.git` (1.2 GB), but **that path is SESSION TEMP and must not be relied on after a
reboot.** The main repo is the durable copy.

⚠ **THE HASHES IN THIS TABLE ARE AS OF WRITING.** The laptop was still pushing when this was written
(`origin/CLOUD` was observed moving: `3dcd7d4049` at 16:02Z, `628e0552` at 16:31Z). **Re-measure before acting.**

## 2. THE DRAIN SURFACE, MEASURED

| measure | value |
|---|---|
| local branches | **69** |
| branches holding commits NOT in `CLOUD` | **24** |
| total undrained commits | **183** |
| worktrees | **63** |
| worktrees holding uncommitted work | **52**, totalling **121 files** |
| how far behind those branches are | **3,118 to 7,507 commits** |

That last row is the real difficulty. These branches were cut long ago and never rebased, so "drain" is not a
fast-forward -- each one is an old base meeting a trunk that has moved thousands of commits since.

## 3. THE CONSTRAINT THAT ORDERS ALL OF IT

⛔ **MERGING ANY PRE-REWRITE BRANCH INTO THE REWRITTEN TRUNK RECONNECTS THE OLD ANCESTRY AND UNDOES THE PURGE.**
The merge base would be a pre-rewrite commit, which makes every purged object reachable from `CLOUD` again. The
purge would read as done and would not be.

**Measured, and it narrows the risk usefully:** the sampled undrained branches touch **0 files** under the purged
`org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/2.0.0_SA_COO~D/*.shots/` paths. So the hazard is **ancestry
reconnection**, not direct re-introduction of the screenshots. That distinction is what makes strategy B viable.

## 4. TWO STRATEGIES

**A -- rewrite every local ref with `git-filter-repo`, then merge normally.**
Preserves branch ancestry. **BLOCKED ON THIS DEVICE:** `git_filter_repo` is not installed, not vendored in the
repo (measured: 0 hits over 80,889 files scanned), and not available as a git subcommand. Installing it is egress
off Opal infrastructure and needs Andrew's word. It also **hard-resets a non-bare checkout** (the laptop's own
warning, which is why it ran on a mirror) -- with 52 dirty worktrees here that is a live hazard.

**B -- drain by CHERRY-PICK / SQUASH onto the rewritten trunk, then DELETE the branch. RECOMMENDED.**
No tool, no egress, and no ancestry reconnection, because a cherry-pick copies the change without the parent
chain. It also matches Andrew's instruction exactly: every branch gets *analysed*, then landed or declared
superseded. When the last of the 24 is gone, nothing references pre-rewrite history and the purge holds
permanently.

## 5. THE `CLOUD` RE-SYNC ITSELF -- SMALL, AND SEPARABLE FROM THE DRAIN

1. `git fetch origin`.
2. Move `CLOUD` to the rewritten `origin/CLOUD`.
3. Replay the **15** local commits by cherry-pick; verify each one lands.
4. `git reset --mixed` in each worktree -- **NEVER `--hard`**. Exercised on a scratch repo: `--mixed` touches the
   INDEX only; modified tracked files keep their contents and untracked files stay in place. The 121 uncommitted
   files survive.
5. Push, then read `git ls-remote` as the landing oracle.

**This is a short session's work and does not require the drain to be finished first.** It is the sensible first
act after the reboot.

## 6. THE 24 BRANCHES -- VERDICTS FILLED (2026-09-28 ~17:5xZ)

⭐ **THE WORKSHEET IS COMPLETE. TOTALS: SUPERSEDE 17, LAND 3 (one records-only), HOLD 4.**
**THREE SEATS, THREE METHODS, NO DISAGREEMENT ACROSS ALL 24.** Adjudicated by `3.0.0_SA_CVO~O`
(`org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoO_S19_DRAIN_VERDICTS_24_BRANCHES_20260928.md`, ON DISK and awaiting
the index at the time of writing -- confirm it committed before relying on it), with `1.0.0_SA_CTO~Z`
INDEPENDENTLY CONCURRING on the AMGT set by `git cherry` plus per-file blob comparison against a positive
control. `1.0.0_SA_CTO~O` then filled the 13 NFRA branches independently
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoO_S19_DRAIN_VERDICTS_NFRA_20260928.md` @`64dad897ff`, LOCAL) by
ancestry + `git cherry` + a 3-way blob compare, reaching 11 SUPERSEDE / 2 HOLD -- the same answer as the CVO's.
It also records that the SUPERSEDE branches' uncommitted files are EOL churn, deploy stamps and clean build
clones, i.e. disposable.

⛔ **THREE OPERATIONAL CAUTIONS THAT TRAVEL WITH THE LANDS -- read before cherry-picking:**
1. `closer/amgt-r-20260923`: its `MANIFEST.json` **DIFFERS** from the trunk's copy. Decide deliberately which
   wins; do not let the cherry-pick choose for you.
2. `wk-amgt-14-50`: **do NOT land `.open_deploys/amgt-rk49-lusha-enrich.json` in an OPEN state** -- read the
   tip's ledger first (an AC3 live write was attempted and the ledger records it). Its CODE is superseded
   (TO-AMGT-rk-49 WITHDRAWN @85a05bd6ab); records only. **Re-append its surprise row rather than cherry-picking
   the shared channel file** -- two branches appending to one channel collide at the same offset by construction.
3. `closer/amgt-h-y-20260923` and `closer/amgt-experience-z-20260923` are **ONE DECISION, not two**: 17 of h-y's
   22 unlanded commits are experience-z's commits at the SAME HASHES, and experience-z carries Andrew's
   do-not-merge word.

**Still none of them is to be `git merge`d** -- section 3 stands, every LAND is a cherry-pick.

| branch | undrained | behind | last commit | last author | uncommitted | VERDICT |
|---|---|---|---|---|---|---|
| `closer/amgt-experience-z-20260923` | 27 | 3118 | 2026-09-23 | 2.0.0_SA_COO~Z | 0 | **HOLD** -- Andrew |
| `closer/amgt-h-y-20260923` | 23 | 3136 | 2026-09-23 | 2.0.0_SA_COO~Y | 0 | **HOLD** -- 2.0.0_SA_COO~Y or Andrew |
| `rel-nfra-oplgtw-sprint-owner` | 13 | 7103 | 2026-09-27 | 0.9.0_WK_NFRA_OPLGTW~9 | 3 | SUPERSEDE |
| `rel-nfra-oplgtw-email-deny` | 12 | 7103 | 2026-09-27 | 0.9.0_WK_NFRA_OPLGTW~8 | 2 | SUPERSEDE |
| `closer/amgt-r-20260923` | 12 | 4177 | 2026-09-23 | 4.0.0_SA_CRO~Z | 0 | **LAND** (records) |
| `rel-nfra-mcpindex-r2-gateway` | 11 | 7103 | 2026-09-26 | 0.9.0_WK_NFRA_MCPINDEX~1 | 2 | SUPERSEDE |
| `rel-nfra-opalai-portal-grant-gateway` | 10 | 7103 | 2026-09-26 | 0.9.0_WK_NFRA_OPALAI~9 | 2 | SUPERSEDE |
| `rb-nfra-mcpindex-r2-base` | 10 | 7103 | 2026-09-26 | 0.9.0_WK_NFRA_OPALAI~9 | 1 | SUPERSEDE |
| `rel-nfra-opalai-zs18-gateway` | 9 | 7103 | 2026-09-25 | 0.9.0_WK_NFRA_OPALAI~8 | 3 | SUPERSEDE |
| `rb-nfra-opalai-portal-grant-base` | 9 | 7103 | 2026-09-25 | 0.9.0_WK_NFRA_OPALAI~8 | 1 | SUPERSEDE |
| `rb-nfra-opalai-zs18-base` | 8 | 7103 | 2026-09-25 | 1.0.0_SA_CTO | 1 | SUPERSEDE |
| `wk-NFRA_OPALAI-1` | 7 | 1661 | 2026-09-25 | 0.9.0_WK_NFRA_OPALAI~1 | 2 | **HOLD** -- Andrew G-ACCT/G-AUTH/G-PUSH |
| `wk-amgt-14-50` | 6 | 6317 | 2026-09-19 | 2.0.0_SA_COO~Z | 1 | **LAND** records only |
| `wk-amgt-13-26` | 4 | 7507 | 2026-09-17 | 0.9.0_WK_AMGT_RESAPP~26 | 1 | SUPERSEDE |
| `wk-NFRA_OPALAI-3` | 4 | 1537 | 2026-09-25 | 0.9.0_WK_NFRA_OPALAI~3 | 3 | **HOLD** -- same gates |
| `wk-amgt-13-29-sp` | 3 | 7502 | 2026-09-17 | 0.9.0_WK_AMGT_RESAPP~29 | no worktree | SUPERSEDE |
| `rel-nfra-mcportal-r2-gateway-2` | 3 | 7103 | 2026-09-25 | 0.9.0_WK_NFRA_MCPORTAL~2 | 3 | SUPERSEDE |
| `cvo-z-harvst-l4r` | 3 | 4146 | 2026-09-23 | 3.0.0_SA_CVO~Z | 1 | **LAND** (records) |
| `wk-amgt-13-29` | 2 | 7507 | 2026-09-17 | 0.9.0_WK_AMGT_RESAPP~29 | 1 | SUPERSEDE |
| `wk-amgt-13-28` | 2 | 7507 | 2026-09-17 | 0.9.0_WK_AMGT_RESAPP~28 | 1 | SUPERSEDE |
| `rel-nfra-mcportal-r2-gateway` | 2 | 7103 | 2026-09-25 | 0.9.0_WK_NFRA_MCPORTAL~2 | 1 | SUPERSEDE |
| `wk-amgt-13-30` | 1 | 7507 | 2026-09-17 | 0.9.0_WK_AMGT_RESAPP~30 | 1 | SUPERSEDE |
| `wk-amgt-13-27` | 1 | 7507 | 2026-09-17 | 0.9.0_WK_AMGT_RESAPP~27 | 1 | SUPERSEDE |
| `rel-nfra-opalai-r1-gateway` | 1 | 7103 | 2026-09-24 | 0.9.0_WK_NFRA_OPALAI~2 | no worktree | SUPERSEDE |

⚠ **`closer/amgt-experience-z-20260923` carries a standing instruction: DO NOT MERGE ITS TIP WITHOUT EXPLICIT
WORD.** It is also the largest at 27 commits. It is marked HOLD until that word is given.

⭐ **A SHAPE WORTH SEEING IN THIS TABLE:** the `rel-*` and `rb-*` pairs (mcpindex-r2, opalai-zs18,
opalai-portal-grant, mcportal-r2) are gateway/base pairs from the same rounds, and the `wk-amgt-13-*` family is
six sibling worker branches from one round on 2026-09-17. **These are the most likely SUPERSEDE candidates** --
sibling worker branches whose content usually drained through a different route. Check them as families, not one
at a time; that is where the 24 shrinks fastest.

## 7. WHAT MUST NOT HAPPEN

- **No `git merge` of any pre-rewrite branch into `CLOUD` after the re-sync** (section 3 is the reason).
- **No `git reset --hard` in any worktree** -- 52 of them hold uncommitted work, 121 files.
- **No force-push from site Z.** The trunk rewrite is the laptop's act and is already done.
- **No branch deletion before its content is landed or recorded as superseded**, with the record naming which
  commits were examined.
- **No `git-filter-repo` install without Andrew's word** -- it is egress off Opal infrastructure.

⚠ **`C:/tmp/oa-1` AND `C:/tmp/oa-3` -- THE "ONLY COPY" WARNING IS WITHDRAWN. MEASURED, NOT ASSUMED.**
`1.0.0_SA_CTO~O` reported at 17:55Z that the nested `opal_ai` commits behind `wk-NFRA_OPALAI-1` and
`wk-NFRA_OPALAI-3` *"exist ONLY in C:/tmp/oa-1 and C:/tmp/oa-3; never delete those worktrees"*, and an earlier
revision of this document carried that as its most severe rule. **I checked it against the opal_ai remote and it
does not hold:**

| worktree | nested branch | HEAD | unique commits | contained in a published branch |
|---|---|---|---|---|
| `C:/tmp/oa-1` | `wk-NFRA_OPALAI-1-opal_ai` | `2e48f7b` | **0** | **yes** -- ancestor of `fd8ab8a57f` (DEV and PROD) |
| `C:/tmp/oa-3` | `wk-NFRA_OPALAI-3-opal_ai` | `803f699` | **0** | **yes** -- ancestor of `fd8ab8a57f` (DEV and PROD) |

**THE TRAP THAT PRODUCED THE FALSE ALARM, and it points the other way too:** `git rev-list --count --all --not
--remotes` reads **0** in both, which looks like confirmation that everything is pushed -- but it trusts LOCAL
remote-tracking refs, which go stale. In these repos `refs/remotes/origin/wk-NFRA_OPALAI-*-opal_ai` exists
locally while **the branch does not exist on the remote at all** (`git ls-remote` returns nothing for it; the
remote has exactly two heads, DEV and PROD). So the tracking-ref check can say "all pushed" about a branch the
remote has never heard of. **The sound check is `ls-remote` plus an ancestry test against the hashes it
returns** -- which is what the table above is.

**WHAT IS ACTUALLY LOCAL-ONLY** is the ordinary thing: the PARENT branches `wk-NFRA_OPALAI-1` (7 commits) and
`wk-NFRA_OPALAI-3` (4), exactly like the other 22. They are HOLD on Andrew's cutover gates, not because they are
irreplaceable. **Treat those two worktrees as ordinary members of the 24.**

## 8. RESUMPTION CHECKLIST, POST-REBOOT

1. **Read this file first.** Then re-measure section 1 -- `git ls-remote origin CLOUD` and `git rev-parse CLOUD`.
   The hashes above were moving at the time of writing.
2. Confirm the pre-rewrite history survived the reboot: `git rev-parse 8cf46e0802` must resolve.
3. Do **section 5** (the `CLOUD` re-sync). Report the landed hash by `ls-remote`.
4. Then work **section 6** family by family -- start with the `wk-amgt-13-*` siblings and the `rel-*`/`rb-*`
   pairs, since that is where SUPERSEDE verdicts are most likely and the list shrinks fastest.
5. **Section 6 now has no unfilled verdict**, so Andrew's stated condition turns on EXECUTING it: 17 branches to
   delete (with the record of what was examined), 3 to cherry-pick, 4 that need a word from Andrew or
   `2.0.0_SA_COO~Y` before anything happens to them. The four HOLDs are the only items that can still block a
   restart, and three of the four are gated on Andrew directly.

**Seats Andrew is keeping online for this work:** `1.0.0_SA_CTO~Z`, `1.0.0_SA_CTO~O`, `3.0.0_SA_CVO~O`.

**Open with the laptop MSTR:** it expects a per-tree count and any hash disagreeing with its commit map, from my
half of the re-sync. That report is owed at step 3, not before.
