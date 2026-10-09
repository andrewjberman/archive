# NFRA_GATSCP round 4 -- base measurement before the cut (issuer 2.0.0_SA_COO~N1, 2026-10-09 ~16:0xZ)

Read-only, box/dell1 HEAD; method: every BLOCK line of `org/git-author-override-audit.log` from 2026-10-02T13:57Z to 2026-10-09T14:03Z
(119 lines; the census said 118), each traced to the author's next non-merge commit on any ref (`git log --all --no-merges --author
--since --reverse`) and to the author's commits of the same path within 12 h, plus the commit messages.

## 1. owned-paths-check already grades the commit's own write set

- The hook takes `OWNED_PATHS_STAGED_FILES`, exported by the installed pre-commit hook as `git diff --cached --name-only` (pre-commit
  :14, :90) of the index git hands the hook (owned-paths-check.sh :168-172).
- safe-commit's two-phase path stages ONLY the pathspec into a private index (safe-commit.sh :459-462, :713-718) and runs the hook
  there (:484); linked worktrees take the legacy `git commit --only -- PATHSPEC` (:406, :1559), whose hook sees a temporary index of
  HEAD + the pathspec (the repo's own record: safe-commit.sh :1260-1262); a bare `git commit` commits every staged path, so its staged
  set IS its write set. On every path the hook grades exactly what the commit writes.
- The one measured outside-the-act case: `infra/aws/lambda/ci/source-map-reconcile-audit.jsonl`, 10 BLOCK lines by 2.0.0_SA_COO~P,
  added to the deploy recorder's own pathspec while already dirty (record-terraform-deploy.sh :895-898); FIXED at 2f954669c8 ("the
  deploy recorder commits only paths it changed").

## 2. The census's 26 "false refusals" are an artifact of its pairing

The census paired each BLOCK with the first later OVERRIDE by the same author within 400 lines (reproduced exactly: 26 pairs). Traced:

| of 26 | finding |
|---|---|
| 19 | the author COMMITTED the blocked path itself, between the BLOCK and the OVERRIDE (+10 min): the gate refused the commit's OWN path -- a true refusal, then an audited override |
| 6 | never committed by that author, and the paired OVERRIDE names a DIFFERENT lane than the BLOCK (39959 TREE_DELIVERABLES vs IRPT_COMPLETION_P; 40602 TREE_COO vs TREE_DELIVERABLES; 40786, 40874 BASE_EXEC vs NFRA_CTLPLN_FAST_C; 42229 LOOP_MECHANISM vs an ANDREW_DIRECT token; 39887 matches but 264 lines later): most likely a different commit |
| 1 | 44486 (IRPT_COMPLETION_REGISTRY, lane matches): never committed by anyone after it |

All 119 BLOCK lines: (a) path in the author's next commit 24; (b) not committed by the author within 12 h 75 (b1: the message says the
author's OWN edit was refused and handed off as a patch 35; b2: someone else's / already-dirty file 10 -- all the deploy-recorder case
above, fixed; b3: no evidence 30); (c) other 20 (16 committed by the author within 12 h; 2 test exercises; 1 non-seat; 1 no commit).

Why a census cannot measure this: a BLOCK line logs only the first three violating paths (owned-paths-check.sh :259-266), and an
OVERRIDE line logs only the lane name, never a reason or the act it serves (:201-205). Nothing links an OVERRIDE to the BLOCK it answers.

## 3. to-pipeline-gate's 4

Two commits, each logged twice (once inside safe-commit, once in the hook): 1a5d8a7b84 (AMGT_HARVST.R75-ZW.POINTER.md) and
964d155998 (MDPF_DEMQUE.R4-ZQ.POINTER.md). Nothing was refused: a file carrying `# pipeline-override:` is audited and short-circuited
(to-pipeline-gate.py :2838-2863). Without the header the refusing limb would be the preflight check (:2929-2933, no `</preflight>`):
a true refusal of a non-order file in an order folder. GS-f-1 already made such files not orders in the row gate; FWD-7 removes the
need for new pointers.

## 4. D1-S10, a live cross-box order to a non-Codex seat with no manual relay

- `crossbox-call.py send-pending` (GS-e-3) is called by nothing automated: not /govern, not box-sync, not open-calls-scan, no
  scheduled task. It runs only under an MSTR serial.
- On the receiving box nothing calls `crossbox-call.py receive`: the agent-bus consumer prints the line as a chat event, and the
  /agentbus skill gives the receive step to the box manager by hand (SKILL :241-243).
- Both hookups live in 0.0.0_AB_MSTR's skills (/govern, /agentbus), outside this project's write set.
- `org/mcp/liveness.json` lists 22 seats, all on dell1; no live dell2 or laptop seat is measurable from here.

## 5. D1-W13-S1

`safe-merge.sh` `_verify_staged_carried` (:318-333): the exemption is :326 `git diff --quiet HEAD -- "$p" && continue`, which also
passes a path reset in both the index and the working copy. The expected set is captured at :863 and checked at :900.
