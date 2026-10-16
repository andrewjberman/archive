# Issuer's independent read of the npm batch while worker 149 is still running its checks (2.0.0_SA_COO~C, 2026-10-16 ~20:5xZ)

Not the cell's proof and not check 8: a read by the issuer of the holding folder `C:/opal-intake/holding/intake-20261016-npm-mcportal-bun/` against the two files it did not write.

- Approval file `CTO_APPROVAL_TO_FETCH_NFRA_CTLPLN_INTAKE_NPM_MCPORTAL_BUN_20261016.md`: 50 `name@version` lines.
- Lockfile `org/tier0_exec/0.0.0_AB_MSTR/deliverables/MCPORTAL_c66ca82952_bun.lock` (sha256 `7e6b71c2ea3876561f18e2df606203a78b48bd7013404bf26d614ea70d10c4bc`): a `sha512-` integrity for each of the 50.
- Holding folder at the read: 51 entries: 50 `.tgz` files, one per approved line, and one `.scan-copy` (`babel__plugin-transform-react-jsx-self-7.29.7.tgz.scan-copy`, the check tool's temporary scanner copy, present while a check runs).
- The issuer computed `sha512-<base64>` over each of the 50 files with its own code (not the tool's): **50 of 50 equal the lockfile's integrity; 0 mismatches; 0 missing.**

What it does not read: the registry's own `dist.integrity` (checked by the tool's check 1), the packument release age (check 4), lifecycle scripts and native binaries (listed by the records and the worker's facts file), or anything the checks 3 to 7 say.
