# SESSION LOG -- AMGT_RESAPP.TO-AMGT-rk-37 (0.9.0_WK_AMGT_RESAPP~39)

1. Confirmed the continuation: `git rev-parse --short=10 HEAD` -> `301cd99428`; AMGT-rk-36's
   `<status>` read `complete` and its change-management entry read CLOSED
   (`20260919T1245Z_amgt-rk36-forecasts-adapter-20260918_deploy_completion.md`).

2. Read both never-widen halves (`NEVER_WIDEN_ROUND14_CHAIN_M_{COO,CTO}_HALVES.md`) -- both carry
   a signed `AMGT-rk-37` section (COO half sha256 `594ba746e3...`, CTO half sha256
   `db0e1bbaffe...`; the CTO half's earlier WITHHOLDING on the rollback shape was already LIFTED --
   SIGNED at the `541d395e0d` re-cut, same as rk-36).

3. Confirmed `bloomberg_health` -> `ok: True`. Ran the CAT candidate-probe (ONE `reference_data`
   call carrying 11 candidates: SALES_REV_PER_SH/REVENUE_PER_SH, FREE_CASH_FLOW_YIELD,
   FCF_MARGIN/FREE_CASH_FLOW_MARGIN, RETURN_ON_TOT_ASSETS/RETURN_ON_TOTAL_ASSETS,
   NET_INCOME_MARGIN/PROF_MARGIN, CIE_DES, CIE_DES_BULK). Adopted: REVENUE_PER_SH,
   FREE_CASH_FLOW_YIELD, FREE_CASH_FLOW_MARGIN, PROF_MARGIN. RoTA's both candidates refused
   BAD_FLD/INVALID_FIELD -- reported honestly ABSENT, per the RULED instruction, rather than
   spending a second probe call (BOUNDS caps this order at exactly 16 Bloomberg requests: 1 probe
   + 5x3 pull). CIE_DES came back a plain string; CIE_DES_BULK a LIST of one-column row dicts
   (`[{"Company Description": "..."}]`) -- the shape measured BEFORE the reader was built, per
   item 2's instruction.

4. **SURPRISE, caught and corrected same-turn:** the first Edit-tool call for HEADER_FIELDS was
   given the main workspace's absolute path instead of this worktree's, and landed in the SHARED
   main tree. Caught on the very next command (git status differed between the two trees);
   confirmed the main-tree diff was clean before revert; reverted with `git checkout --` in the
   MAIN tree only; re-applied the same edit correctly inside `/c/tmp/wk-amgt-14-39`. Filed row
   `AMGT_RESAPP-Z-W39-S4` (INERT).

5. Wrote `row_mnemonics.json` (the candidate-probe record) into this worker's deliverables folder.

6. Built the producer/adapter code: `model_block_pull.py` (CIE_DES/CIE_DES_BULK join
   HEADER_FIELDS with a bulk-text join helper shared between the derive's figures loop and the
   unit-map builder's input; the four adopted rows join HIST_FIELDS; `_compute_cases()` computes
   the Base case once at derive from the block's own BEST_EPS FY1 and PE_RATIO history, and writes
   the ruled ABSENT dict for upside/downside), `build_unit_map.py` (TEXT_FIELDS/PERCENT_FIELDS/
   PER_SHARE_FIELDS gain the six new mnemonics, classified by their CAT-measured magnitudes),
   `scoped_amgt.py` (`_describes_business_test`, the gated `read_description`, `_model_cases`
   taking the block and forcing upside/downside ABSENT regardless of block content),
   `test_description_line.py` and `test_model_cases.py` (new, 14 offline planted cases).

7. Ran the wider `lib/research/api/tests/` suite and found the shared `_document()` fixture
   sentence ("The company builds aircraft.") now fails the new test (no descriptor phrase),
   silently dropping `test_16`'s SERVED-machine coverage under a green. Census-confirmed
   (`comp-find`) it was the ONLY other reference to that literal string; changed it to "The
   company manufactures aircraft." (passes) in `test_drafted_sections.py`, and updated
   `test_16`'s assertion in `test_generation_and_pool_routes.py` to match plus assert
   `describes_business_test.passed is True`. Re-ran: 177 passed (was 176 + the newly-fixed
   test_16), same 2 pre-existing off-task failures (`ceo_profile_reading`, unrelated to this
   cell) present both before and after -- confirmed by restoring `.scratch/scoped_amgt.py.orig`
   and re-running the same command. Filed row `AMGT_RESAPP-Z-W39-S5` (ARMED, disarm_owner
   `2.0.0_SA_COO~Z`; out of this cell's surface, not fixed here).

8. Committed the code + tests + row_mnemonics.json (`fe0435ce53`).

9. Ran the live pull + derive on the three validation names (`CAT US Equity`, `CSL AU Equity`,
   `6861 JP Equity`) -- 15 requests total (5 per name: header ref, hist, 3 forecast overrides),
   completing the 16-request budget with the CAT probe. AC1/AC3 measured PASS: all three names'
   description scalars non-empty, all four adopted rows carry 10-11 fiscal values, RoTA null with
   2 refused candidates on all three; base SERVED with an independent recomputation agreeing
   exactly on all three names; upside/downside ABSENT with the exact ruled string.

10. AC2: `pytest lib/research/api/tests/test_description_line.py lib/research/api/tests/test_model_cases.py`
    -> 14 passed, 0 failed, 0 errors (run before the deploy, per the order's own sequencing note).

11. Re-ran the stale-bytes check (EMPTY) and built/uploaded the artifact (VersionId
    `uSSIk4ptuShTa6Ac3G5ZmubCaOYbDmx1`, sha256 `EjyVSMCGIi2iqw2EN/yhG8M8gVjR0/yqvFBla885ctI=`).
    Opened the change-management entry BEFORE this build (`c9cc29e964`), with the never-widen
    pair sha256, pre-act CodeSha256/VersionId, re-measured bucket versioning `Enabled`, the
    pre-deploy 13-route census (13/13 200) and the 12 drafted names' pre-deploy description
    status (12 of 12 SERVED via the segment sentence) all recorded fresh in a "Pre-act record"
    section.

12. `HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/harvest apply
    -target=module.scoped_amgt_api.aws_lambda_function.this -auto-approve -no-color` ->
    `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` Post-act CodeSha256 matched the
    uploaded sha; targeted replan `No changes`.

13. **AC4's first live run** exposed that `read_description`'s final ABSENT branch hard-coded
    `describes_business_test: None` instead of surfacing the failed test's own `{passed: False,
    ...}` -- the criterion's own text names `test passed False` on the served plane. Fixed in the
    same worktree (tracked the last-tried test result and returned it on the ABSENT branch),
    re-ran the offline suite (14 passed, no regression), rebuilt (VersionId
    `YjjMpD9ULicxQPnExgUVIbVQkUOQ_l8k`, sha256 `QwET8XtX3Z53ylyStMoiX/yaC0Slfrc959+rUGlHGME=`) and
    re-applied the SAME targeted resource a second time (0 add/1 change/0 destroy again; post-act
    CodeSha256 matched; final targeted replan `No changes`).

14. Post-deploy 13-route census (final artifact): 13 of 13 200, `LOST=[]` `GAINED=[]`. Ran AC4's
    literal invocation (corrected the header route's rawPath to `/overlay`, per the census, as
    the criterion itself instructs): BA_US_Equity and HD_US_Equity both 200/200, description
    ABSENT/test False/probes 3/no segment text served, base ABSENT with the no-cases reason,
    upside/downside ABSENT with the exact ruled string, `check_face_len` 179/199 unmoved from the
    independently-recorded pre-deploy values. HOLLOW_NONEXISTENT_KEY_Equity: description ABSENT,
    every case ABSENT. Measured the 12 drafted names' description status post-deploy: 0 of 12
    SERVED, 12 of 12 ABSENT naming all 3 probes -- the named blast radius, exactly as measured.

15. Closed all 3 change-management legs and the entry (`a88b7fde9d`).

16. Filed surprise rows S4 and S5 into `INVESTIGATION_v1.md` (`1645f31d62`).

17. Wrote and validated the proof-of-spec instance; flipped `<status>` to `complete`.
