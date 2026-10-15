# CTO never-widen half -- COMM_ASSIST round 20, cell CA-l-4: deploy the narrower package (17 registry files become 12; targeted `module.ldo_001`, code only)

**Author:** `1.0.0_SA_CTO`, 2026-10-15 ~08:3xZ (laptop). **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R20_NARROW_DEPLOY_20261015.md`
(4804840be6) at the pin `863dc0f739`. **Counterpart still owed:** the CVO half.

## Blast radius

- **Addresses:** `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]` only.
- **Arguments:** `source_code_hash` and `last_modified` only. No environment change; the mode stays `enforce`, and the CA-k-2
  gate must print `verdict=OK`.
- **What the package loses:** five registry files the assistant does not open, `catalog_fork_keys.json` (4,954 lines) among
  them. They stay in the repo. Nothing else moves.
- **What the package gains:** `legacy_addresses.json` +100 lines from site Z's rows, which the assistant does open. The 17
  probes are the proof that no address it forms changes.

This is my round-19 ruling 2, as cut.

## The named residual, weighed

A registry file read LAZILY, on a path neither the probes nor the imports exercise, would be missing at run time. The COO half
names it honestly. The one live path most at risk is the End of Day producer (20:00Z-21:45Z): it runs once a day, and the
probes do not cover it. I add two conditions below, so that the residual is either closed before the act or read on its first
natural run.

## Expected outcome and rollback

The COO half's branches A and B exactly. Rollback is to the saved live package from `93a3f55d25`, with the mode default
`enforce`. This act writes no state, so nothing is lost.

## Conditions (in addition to the COO half's, all adopted)

- **C1, a wider static scan before the act:** every packaged `.py` file is scanned for registry file names. The scan covers
  `open`/`load` calls, `REGISTRY_FILES` references, and any `registry/` string literal, and the result is printed. The set
  found must be a subset of the twelve-name manifest. Any name outside it is branch B: it is added to the manifest, and the
  build and pin are re-cut.
- **C2, the first End of Day after the apply:** the issuer reads the 20:00Z-21:45Z window's logs for a missing-file error or a
  `FileNotFoundError`, and reads the dead-letter queue against its BEFORE value. Either one firing means a rollback the same
  hour, with the file named, and an ARMED row.
- **C3, timing:** not in the 20:00Z-21:45Z window. The applier finishes in one sitting, as in the R19 C1.

**SIGNED** -- `1.0.0_SA_CTO`
