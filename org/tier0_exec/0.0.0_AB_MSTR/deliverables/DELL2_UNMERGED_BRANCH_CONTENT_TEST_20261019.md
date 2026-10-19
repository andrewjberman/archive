# dell2 unmerged-branch CONTENT TEST (Andrew pause-and-merge-forward, CTO msgs 10816 and 10844)

Written by 0.0.0_AB_MSTR~DELL2 at 2026-10-19T18:06Z. Read-only analysis; nothing was tagged or deleted by this test.
Trunk compared against: local box/dell2 HEAD. Branch set: local branches not merged into box/dell2.

## Method
- LITERAL test (CTO msg 10844): for each file a branch changed since its merge-base, compare the branch blob with box/dell2 HEAD.
  Result for the 62 preserve/* branches: 62 of 62 DIFFER. That count is misleading, see below.
- WHAT a preserve/* branch is: one commit by worktree_gc named 'preserve: worktree dirt of <worker> at <time>'. It snapshots the
  UNCOMMITTED dirt of a worker worktree, not the worker's own commits. The dirt is line-ending churn across the same ~37 files
  (CRLF, 'git diff --ignore-space-at-eol' leaves 1 file) plus the 'portal' submodule pointer drift (' M portal').
- REFINED test: diff parent..branch ignoring CR/EOL whitespace; drop the 'portal' pointer. Anything left is real worker content.

## Result for the 62 preserve/* branches
- A: 55 are ONLY line-ending noise and/or the portal pointer. Candidates to retire: tag archive/<branch>, delete the branch.
- B: 7 carry real worker files. Owners drain or retire them (list below).

### B: real files (owner: ~Y2 for IRPT_ANLREQ, ~P2 for IRPT_BCKEND, ~D2 for IRPT_DASHBD)
- preserve/wk-IRPT_ANLREQ-215-20261017T023542Z
    - org/git-author-override-audit.dell2.log
- preserve/wk-IRPT_ANLREQ-284-20261019T130814Z
    - org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~284/r45/commit_msg_portal.txt
    - org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~284/r45/commit_msg_ws.txt
- preserve/wk-IRPT_ANLREQ-285-20261019T130826Z
    - org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~285/r46/GATES.json
- preserve/wk-IRPT_ANLREQ-295-20261019T130935Z
    - org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~295/IRPT_ANLREQ.TO-AR-y-402.original-holdings-blob-delete-path-code-and-policy-read.proof_of_spec.json
- preserve/wk-IRPT_BCKEND-449-20261019T132136Z
    - org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~449/IBhm2_criteria_output.txt
- preserve/wk-IRPT_BCKEND-455-20261019T132238Z
    - org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~455/IBhm10_criteria_output.txt
    - org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~455/IRPT_BCKEND.TO-IB-hm-10.host-role-may-assume-the-hmac-list-stage-role.proof_of_spec.json
- preserve/wk-IRPT_DASHBD-DB2-b260-20261016T162839Z
    - org/git-author-override-audit.dell2.log

### A: noise-only (55)
- preserve/wk-IRPT_ANLREQ-157-20261016T212648Z
- preserve/wk-IRPT_ANLREQ-158-20261017T024642Z
- preserve/wk-IRPT_ANLREQ-159-20261016T223343Z
- preserve/wk-IRPT_ANLREQ-160-20261016T223352Z
- preserve/wk-IRPT_ANLREQ-161-20261016T232706Z
- preserve/wk-IRPT_ANLREQ-162-20261016T232720Z
- preserve/wk-IRPT_ANLREQ-163-20261017T012636Z
- preserve/wk-IRPT_ANLREQ-164-20261017T023534Z
- preserve/wk-IRPT_ANLREQ-165-20261017T033448Z
- preserve/wk-IRPT_ANLREQ-166-20261017T182515Z
- preserve/wk-IRPT_ANLREQ-167-20261017T182521Z
- preserve/wk-IRPT_ANLREQ-168-20261017T192428Z
- preserve/wk-IRPT_ANLREQ-170-20261019T130425Z
- preserve/wk-IRPT_ANLREQ-173-20261019T130442Z
- preserve/wk-IRPT_ANLREQ-214-20261017T012645Z
- preserve/wk-IRPT_ANLREQ-216-20261017T023555Z
- preserve/wk-IRPT_ANLREQ-217-20261017T023607Z
- preserve/wk-IRPT_ANLREQ-218-20261017T023627Z
- preserve/wk-IRPT_ANLREQ-219-20261017T023638Z
- preserve/wk-IRPT_ANLREQ-220-20261017T023649Z
- preserve/wk-IRPT_ANLREQ-221-20261017T023700Z
- preserve/wk-IRPT_ANLREQ-222-20261017T024756Z
- preserve/wk-IRPT_ANLREQ-223-20261017T023712Z
- preserve/wk-IRPT_ANLREQ-224-20261017T023725Z
- preserve/wk-IRPT_ANLREQ-226-20261017T033500Z
- preserve/wk-IRPT_ANLREQ-227-20261017T033512Z
- preserve/wk-IRPT_ANLREQ-228-20261017T052912Z
- preserve/wk-IRPT_ANLREQ-229-20261017T052924Z
- preserve/wk-IRPT_ANLREQ-230-20261017T062530Z
- preserve/wk-IRPT_ANLREQ-231-20261017T062556Z
- preserve/wk-IRPT_ANLREQ-232-20261017T062606Z
- preserve/wk-IRPT_ANLREQ-233-20261017T072501Z
- preserve/wk-IRPT_ANLREQ-234-20261017T082424Z
- preserve/wk-IRPT_ANLREQ-264-20261017T162452Z
- preserve/wk-IRPT_ANLREQ-265-20261017T172450Z
- preserve/wk-IRPT_ANLREQ-266-20261017T172509Z
- preserve/wk-IRPT_ANLREQ-267-20261017T172525Z
- preserve/wk-IRPT_ANLREQ-268-20261017T182527Z
- preserve/wk-IRPT_ANLREQ-269-20261017T192433Z
- preserve/wk-IRPT_ANLREQ-270-20261017T192451Z
- preserve/wk-IRPT_ANLREQ-273-20261017T202531Z
- preserve/wk-IRPT_ANLREQ-274-20261019T130454Z
- preserve/wk-IRPT_ANLREQ-278-20261019T130508Z
- preserve/wk-IRPT_ANLREQ-280-20261019T130558Z
- preserve/wk-IRPT_ANLREQ-281-20261019T130706Z
- preserve/wk-IRPT_ANLREQ-283-20261019T130802Z
- preserve/wk-IRPT_ANLREQ-289-20261019T130839Z
- preserve/wk-IRPT_ANLREQ-293-20261019T130911Z
- preserve/wk-IRPT_ANLREQ-294-20261019T130921Z
- preserve/wk-IRPT_BCKEND-450-20261019T132146Z
- preserve/wk-IRPT_BCKEND-451-20261019T132157Z
- preserve/wk-IRPT_BCKEND-453-20261019T132214Z
- preserve/wk-IRPT_BCKEND-454-20261019T132225Z
- preserve/wk-IRPT_DASHBD-234-20261017T082435Z
- preserve/wk-IRPT_DASHBD-258-20261019T131635Z

## The other 30 unmerged branches (not preserve/*): REFINED test, files whose added lines are missing from trunk
- NOT-LANDED: 26. ALL-LANDED (every added line present on trunk): 4, all of which have a live worktree.
- 'wt' = checked out in a live worktree (not touched by this test).
- drain/dell2/20261009T1346Z | commits not on trunk: 4 | files missing from trunk: 11 of 66
- rel-anlreq-r4 (wt) | commits not on trunk: 1 | files missing from trunk: 1 of 2
- rel-resident-r5 (wt) | commits not on trunk: 1 | files missing from trunk: 1 of 2
- rel-ycdgen-390-g2 (wt) | commits not on trunk: 2 | files missing from trunk: 1 of 2
- rel-ycdgen-f1-svc | commits not on trunk: 2 | files missing from trunk: 2 of 2
- rel-ycdgen-st26 | commits not on trunk: 3 | files missing from trunk: 2 of 5
- rel-ycdgen-st27 | commits not on trunk: 2 | files missing from trunk: 2 of 5
- rel-ycdgen-st28 (wt) | commits not on trunk: 3 | files missing from trunk: 2 of 5
- rel-ycdgen-st29 (wt) | commits not on trunk: 4 | files missing from trunk: 2 of 6
- scratch/r34f-pin (wt) | commits not on trunk: 1 | files missing from trunk: 1 of 1
- scratch/r34g-pin | commits not on trunk: 1 | files missing from trunk: 1 of 1
- scratch/r34h-pin | commits not on trunk: 1 | files missing from trunk: 1 of 1
- scratch/r34i-pin | commits not on trunk: 1 | files missing from trunk: 1 of 1
- scratch/r34j-pin | commits not on trunk: 1 | files missing from trunk: 1 of 1
- scratch/r34k-pin | commits not on trunk: 1 | files missing from trunk: 1 of 1
- wk-IRPT_ANLREQ-102 (wt) | commits not on trunk: 8 | files missing from trunk: 7 of 7
- wk-IRPT_ANLREQ-297 (wt) | commits not on trunk: 2 | files missing from trunk: 5 of 5
- wk-IRPT_ANLREQ-299 (wt) | commits not on trunk: 4 | files missing from trunk: 10 of 10
- wk-IRPT_ANLREQ-300 (wt) | commits not on trunk: 2 | files missing from trunk: 8 of 8
- wk-IRPT_ANLREQ-301 (wt) | commits not on trunk: 6 | files missing from trunk: 6 of 7
- wk-IRPT_ANLREQ-302 (wt) | commits not on trunk: 11 | files missing from trunk: 10 of 11
- wk-IRPT_ANLREQ-62 | commits not on trunk: 1 | files missing from trunk: 8 of 8
- wk-P-ledger-s28 | commits not on trunk: 1 | files missing from trunk: 1 of 3
- wk-P-r103 | commits not on trunk: 1 | files missing from trunk: 5 of 5
- wk-P-r106 | commits not on trunk: 4 | files missing from trunk: 2 of 5
- wk-irpt-dashbd-56-87 | commits not on trunk: 5 | files missing from trunk: 1 of 9

ALL-LANDED:
- ib2/fmap-port-cot-publish (wt)
- scratch/ib605-49f (wt)
- scratch/ib605-cot (wt)
- scratch/ib605-inf (wt)
