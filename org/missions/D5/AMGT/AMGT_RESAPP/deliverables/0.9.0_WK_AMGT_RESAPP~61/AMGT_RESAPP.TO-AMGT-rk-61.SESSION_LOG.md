# Session log -- AMGT-rk-61 (`0.9.0_WK_AMGT_RESAPP~61`)

1. Bar check: branch `wk-amgt-14-61`, `org/`/`.tools/` present, cell paths present -- TREE-OK.
2. Confirmed `git log --oneline -3 -- lib/research/api/scoped_amgt.py` shows rk-53's commit
   (`498dda6b6f`) at the tip -- spawn sequence correct.
3. AC1: both never-widen halves present, each carrying a `## AMGT-rk-61` section (1 of 1),
   both naming a rollback; CTO half's `mentions_VersionId_or_CodeSha256` reads 0 (it defers
   the mechanism to the COO half by cross-reference, "COVERED") -- read and accepted, not
   treated as an ABSENT/0-of-1 STOP.
4. Edited `lib/research/api/scoped_amgt.py`'s `/security/{key}/{leaf}` arm:
   `len(rest) == 3` -> `len(rest) >= 3`; `requested = unquote(rest[1])` ->
   `requested = unquote("/".join(rest[1:-1]))`; `leaf = rest[2]` -> `leaf = rest[-1]`;
   docstring gained one paragraph. `scoped_amgt_route_table()` and every other arm untouched.
5. Wrote `lib/research/api/tests/test_slash_safe_security_route.py` (pattern of
   `test_route_boundary_identity.py`): 32-of-32 / 24-of-24 / 3-of-3 / 16-route-table arms.
6. AC2: full battery `python -m pytest lib/research/api/tests -q` -> 2 failed, 163 passed.
   Both failures are in `test_generation_and_pool_routes.py` (a `NOT_CONFIRMED_NOTHING_FOUND`
   literal that does not exist in `scoped_amgt.py`'s `CEO_READING_*` enum), disjoint from this
   cell's diff and pre-existing at HEAD (confirmed by isolated run: this cell's own 9 of 9
   tests green). Filed row `AMGT_RESAPP-Z-W61-S1`; refused, not repaired (out of `<paths>`).
7. Committed the router edit + new test: `11c01d7648`.
8. Filed surprise rows `AMGT_RESAPP-Z-W61-S1` and `AMGT_RESAPP-Z-W61-S2` (the latter after
   running the CTO-msg-23867 observation request -- one unauthenticated call against the live
   gateway on the encoded and literal slash forms, plus a genuinely-unmapped-route negative
   control; all three returned identical 401s, so the observation is inconclusive by
   construction on this instrument). Committed: `d40de6e07f`.
9. AC3: single-writer adapter queue census against `SITEZ` since the worktree's merge-base --
   0 of 0 commits, positive control fires (1 line). Queue holds.
10. AC4: pre-act baseline read (live `get_function_configuration`, artifact `head_object`,
    role inline-policy sha, 13-route census, 6 slash-key/leaf direct invokes) -- written to
    `.scratch/rk61_pre.json`.
11. Deploy procedure: opened `deploy_ledger.py` entry `amgt-rk61-router-slash-indifferent`;
    ran `build-and-upload-scoped-amgt.sh` (uploaded `research/opal-amgt-scoped-api.zip`,
    VersionId `gg65p2Qo.KibhsWzkZmsvaSdavPreFoF`); `terraform init`; confirmed `AMGT-rk-59`'s
    `fileexists()` guard already landed (no `chatter-axis-producer.zip` build needed); targeted
    plan `Plan: 0 to add, 1 to change, 0 to destroy.` naming only the target resource.
12. First apply attempt was killed by the harness at a 300s shell-level `timeout` before
    Terraform issued any API call (confirmed via an immediate post-kill `get-function-
    configuration` read: `CodeSha256` unchanged from AC4's baseline, and a re-plan with
    locking enabled showed no stale state lock) -- nothing had landed. Re-ran the SAME
    targeted `safe-apply` invocation in the foreground under an extended timeout; it
    completed: `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`
13. AC5: post-act `CodeSha256` moved to the uploaded sha, artifact `VersionId` moved to the
    uploaded one, `Timeout`/`MemorySize`/`Layers`/`EnvKeys` unchanged, 0-diff targeted replan.
14. AC6: served-plane read -- 13 of 13 GET routes unchanged (`LOST=[] GAINED=[]`); 6 of 6
    slash-key/leaf pairs now equal-status (literal form no longer router-refused); role
    policy sha unchanged; `lead-panel/rankings/breakout/chatter` now carries `empty_reason`
    (rk-53's adapter bytes reaching the served plane through this artifact). Never-widen
    rollback branch NOT triggered.
15. Closed the ledger leg and entry; committed the closed change-management entry: `56814ae02d`.
16. `deploy_ledger.py check` confirms `amgt-rk61-router-slash-indifferent` is absent from the
    OPEN list (other seats' unrelated open entries are pre-existing and out of scope).
17. Wrote and validated this proof-of-spec instance.
