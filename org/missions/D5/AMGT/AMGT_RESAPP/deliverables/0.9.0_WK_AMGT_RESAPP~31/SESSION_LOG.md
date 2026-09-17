# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~31 -- AMGT_RESAPP.TO-AMGT-rk-19.page-label-and-link

1. Printed `git rev-parse --abbrev-ref HEAD` (`wk-amgt-13-31-portal`) and confirmed `org/` and `.tools/`
   exist (`TREE-OK`).
2. Checked every path named in the order's section 3 against the worktree. `org/missions/...` paths
   (deliverables parent, investigation file, task-order file) all exist. The two `portal/` paths
   (`portal/src/pages/SecurityAnalysis/`, `portal/src/api/endpoints/amgt-lead-panel.ts`) do NOT exist:
   `portal/` is a git submodule (gitlink) recorded at HEAD as commit `2453a7b4c6b7ff91ea89db499890a9486265d1a0`,
   but this linked worktree's `portal/` directory is completely empty (`ls -laR portal` = only `.`/`..`).
3. Investigated why: `.gitmodules` is 0 bytes in both this worktree and the main workspace checkout, so
   there is no URL mapping for `git submodule update --init` to resolve. The main workspace's own
   `portal/` IS populated, but as an independently-managed nested git clone (origin
   `https://github.com/Opal-Capital/portal.git`, branch `DEV`) -- its object database does contain the
   gitlink's commit, confirmed via `git cat-file -t`, but that checkout lives outside this worktree and
   is not something this order's `<paths>` grants a write/init action on.
4. Per CLAUDE.md's bar ("never rebuild, extract or reconstruct the tree to make an order executable")
   and this order's own first-act instruction ("if any [named path] is absent, STOP with a BLOCKING
   row"), did NOT clone/copy portal content into this worktree. Ran both literal AC1/AC2 invocations
   as written to record their real, verbatim output on this tree (both return rc=0 but on an empty/
   nonexistent source tree -- a false-negative-shaped pass, not a genuine one against either
   criterion's stated `<expect>`).
5. Filed one surprise row, `AMGT_RESAPP-Z-W31-S1` (class BLOCKING, hazard_standing ARMED, disarm_owner
   `2.0.0_SA_COO~Z`), in
   `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`, grounded on
   the git reads above. Verified with `python .tools/surprise-row-gate.py <file>` (staged) -> `1 new
   row(s) of 344 total checked ... OK`.
6. Wrote this proof-of-spec instance recording AC1 and AC2 as FAIL (BLOCKING premise failure, not a
   defect in either criterion's own design) and left the task order's `<status>` untouched (order stays
   OPEN per the REFUSAL CLAUSE -- not repaired, widened, or routed around).
7. Did not begin `AMGT-rk-30` (page half) -- explicitly out of scope this order ("not yet ready ...
   do not begin it").
