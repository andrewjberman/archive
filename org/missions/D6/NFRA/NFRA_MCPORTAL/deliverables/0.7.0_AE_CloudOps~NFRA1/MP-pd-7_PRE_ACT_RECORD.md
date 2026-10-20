# MP-pd-7 PRE-ACT RECORD (the NEVER-2 ledger's pointer target)

Order: `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.md` (AMENDMENT A2), GO `.../deliverables/2.0.0_SA_COO~MP/pd/GO_MP-pd-7.md`. Ask sha256 prefix `f0098d2b67ab`, both halves SIGNED at it (CTO @392b19649f, the COO~MP half at HEAD).
Ledger: `nfra-mcportal-pd-release` (legs: package build, apply, deployed-bytes read).

## Census
- Deployed function `mcportal-grant-writer-lambda`: CodeSha256 `894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck=`, LastModified 2026-10-11T20:32:52.000+0000, 11 zip members, runtime python3.12, layer version 1. Its bytes are held: `MP-pd-7_deployed_before_894RI63.zip` (sha256 prefix `f3de1123adff1b88`, 57638 bytes), kept 7 days after the close (the CTO half's condition).
- New package: built from the Lambda directory byte-equal to `LAMBDA_COMMIT` `f3774ac1df8` and the live release `13917ef993` (read twice, stable: True): 65 members. Against the deployed zip: 54 new, 6 differ, 5 equal.
- Live release (`EC2_MANIFEST.json` `services.opal-gateway.deployed_commit`) = `LIVE_BASE` `13917ef993`.

## Build comparison
Package built here (`mp_pd7_measure.py`, `new.zip`): members compared after the apply with the zip the function serves (`MP-pd-7_AFTER.json`, `member_md5_equal_to_built`). Import probe (stdlib, boto3, botocore, jwt, cryptography only): imports and answers a no-header event.

## Rollback (proven before the act, as far as it can be: the declared departure of the ask, section 5)
Old handler `30d9b99758d` on the same live closure: 65 members; against the deployed zip 54 new, 5 differ, 6 equal; negative control (the new package differs from the deployed one): True. Command: `python mp_pd7_act.py rollback` (lays the old `lambda_function.py` in the working tree, uncommitted, plans, applies the saved plan through safe-apply, restores the file). Its time is measured at the act: the build/plan time plus the apply time.

## The before invokes (2026-10-20T20:04:11Z)
`narrow`: REFUSED NO-OWNER-HEADER; `set_person_access`: REFUSED NO-OWNER-HEADER (each writes one append-only refusal record to the writer's own changes table; the function's existing behaviour).
