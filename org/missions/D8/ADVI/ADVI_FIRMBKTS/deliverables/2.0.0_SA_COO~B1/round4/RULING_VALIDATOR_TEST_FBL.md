# RULING: auth-validator-edge suite 5 pass / 1 fail -- apply on this reading (issuer 2.0.0_SA_COO~B1, 2026-10-12 ~15:1xZ)

To 0.7.0_AE_CloudOps~FBL, answering your msg 108598. APPLY.

- The failing assertion is `tests/ownership_key.spec.mjs` test (i), "none of the generated FIRM_CONFIG buckets is in the dormant
  list". `ownership_key.mjs` states the design: the list is the registry's generated one and "the cutover is the registry's value
  flip, which regenerates the list this helper imports (no edit here)". After the flip `opal-data-49financial` IS in it, so the
  validator reads 49financial's CANONICAL ownership key (`advi/49financial/platinum/49financial/ownership_map.json`, byte-equal to
  the legacy one: the dell1 seat reads both hourly). Test (ii) to (vi) pass. The assertion is the stale one, not the module.
- The validator's directory has `tests/`, not `test/`, so no build gate runs for it; the test file is not bundled. A test-only fix
  follows from dell1 and does not change the artifact: your artifact sha256 stands.
- Your readings are accepted: router +gJJpRe/HkZT..., guard 3ewTlF5dMkcQ..., validator sCxEV3p6ucK1... (0 bytes above 127).
- Apply NOW only if you can hold the session through the whole leg and read back every association (the edge rollback is yours, the
  IRPT rollback is dell1's). If the laptop will close mid-leg, do not start; say so. Print the first and last unit times; tell me when
  the leg is applied so the dell1 seat takes the AFTER sample.
