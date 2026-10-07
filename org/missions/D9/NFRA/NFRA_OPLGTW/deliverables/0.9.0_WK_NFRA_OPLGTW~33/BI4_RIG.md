# BI4 rig note

Measured: the pre-change file run against the tree carrying the pre-check: 3 failed, 3 passed.

Failing (each asserted rc 0 or 3 and got rc 1):
- test_positive_control_declared_equals_live_reaches_the_upload_step
- test_live_ref_moves_between_the_early_read_and_the_upload_read
- test_no_metadata_falls_back_to_the_single_sha_key_that_shares_latests_object

Cause: these three get past the early base read and reach the mcportal build. The rig's mcportal had only package.json
(no bun.lock), and the rig copied only deploy-to-ec2.sh (no ops/bun_cache_precheck.py). The pre-check at
deploy-to-ec2.sh line 210 therefore ended rc 2 (cannot read lockfile), the subshell exited 1 after printing
"ERROR: bun cache miss", and the script stopped at line 213-214 ("ERROR: mcportal build produced no dist/index.html",
exit 1), before any upload. The other three tests refuse before the build, so they passed.

Rig change (test file only): copy ops/bun_cache_precheck.py into the rig; give mcportal a 2-package bun.lock; build a
temp stub cache of COMPLETE entries (<name>@<ver>@@@1/package.json) passed via BUN_INSTALL_CACHE_DIR. The bun stub is
unchanged. Two tests added: test_ogbi4_ac01 (positive), test_ogbi4_ac02 (one entry removed: ERROR: bun cache miss, 0 uploads).
No existing assertion edited. deploy-to-ec2.sh and ops/bun_cache_precheck.py untouched.
