# AR-g-121 -- the issuer's re-grade of AR121-g-AC3 and the scope arm (2.0.0_SA_COO~G2, 2026-10-16)

The worker's proof instance (deliverables/0.9.0_WK_IRPT_ANLREQ~258/, valid rc=0) records AR121-g-AC1 PASS, AR121-g-AC2 PASS and AR121-g-AC3 FAIL. The worker's folder is the worker's lane, so the instance is left as written; this file carries the issuer's re-grade.

- AC3 FAILED in the worker's worktree for two defects of the issuer's, both dispositioned in the channel (row IRPT_ANLREQ-D2-S146, for W258-S1 and W258-S2): the provisioned sparse cone omitted infra/aws/lambda/investor-reporting/ycharts and .../ops (two of the three regress files cannot run without them), and the scope arm of ar_g121_checks.py did not allow the worker's own folder.
- Re-run by the issuer in the worker's worktree after `git sparse-checkout add infra/aws/lambda/investor-reporting`, with the fixed checker, on branch wk-IRPT_ANLREQ-258 at 0cdb38f70d: `ar_g121_checks.py build` -> AR-G121-OK; `guard` -> AR-G121-OK; `regress` -> AR-G121-REGRESS-OK; `scope` -> AR-G121-SCOPE-OK.
- Merged: b535f41cb8 (fast lane). The product change is intake/yfinance_check.py (`_is_ticker_missing`, exact class name in the MRO; `default_history` returns [] for it and re-raises everything else), its tests and the real yfinance 1.2.0 exceptions module as the test fixture.
