# Session log -- 0.9.0_WK_AMGT_RESAPP~385 on AMGT_RESAPP.TO-AMGT-ss-2

Worktree C:/dev/wk-resapp-385, branch wk-AMGT_RESAPP-385. TREE-OK. HEAD at start e790da8e1f, 33 commits after the issuance cab1577aba (surprise row AMGT_RESAPP-D1-W385-S2).

Baseline (unedited analyze.py): r93_scale_set.py gave FAIL M1 (kept 2023, 2024, 2025), PASS M2-M5, R93 SCALE SET: NO, exit 1.

Edit: lib/research/filings/analyze.py -- _SCALE_WORDS, _SCALE_AFTER_RE, _scale_word_after, _scale_set_reason added before _apply_point_verification; the scale hold runs before any passage is minted; the held entry keeps period, value and units and carries the scale reason.

Tests: lib/research/filings/tests/test_scale_set.py -- 6 passed (M1-M5 and the window arm).

AC1 r93_scale_set.py: PASS M1-M5, arms 5 of 5, R93 SCALE SET: YES, exit 0 (run twice, identical).
AC2 r93_scale_table.py: 12 objects, changed 1 (SAP_GY_Equity, expected 0), equal 11, PASS T1, PASS T2, R93 SCALE TABLE: YES, exit 0.
AC3 chain: r91_locator.py gave R91 LOCATOR: NO (10 of 13), FAIL L3, FAIL L4, FAIL K1; the && chain stopped there. Run separately: r92_block_bound.py R92 BLOCK BOUND: YES (5 of 5), exit 0; pytest lib/research/filings/tests 328 passed, exit 0. Surprise row AMGT_RESAPP-D1-W385-S1 (BLOCKING, ARMED).

Surprise rows filed: AMGT_RESAPP-D1-W385-S1, AMGT_RESAPP-D1-W385-S2, AMGT_RESAPP-D1-W385-S3.
