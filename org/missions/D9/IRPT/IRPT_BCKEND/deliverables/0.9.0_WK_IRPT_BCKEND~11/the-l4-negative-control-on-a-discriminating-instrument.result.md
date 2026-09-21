# IB-rti-3 result -- 0.9.0_WK_IRPT_BCKEND~11

## Outcome per bucket
- opal-data-inflection: CANNOT DISCRIMINATE WITHOUT A NEW GRANT (non-verdict, owner 1.0.0_SA_CTO).
- opal-data-cottonwood: CANNOT DISCRIMINATE WITHOUT A NEW GRANT (non-verdict, owner 1.0.0_SA_CTO).
- Ledger leg L4 stays OPEN (log line appended to the ib-rte-3 entry; deploy_ledger.py has no note verb).

## Instrument
battery_ib_rti_3.py (this folder). Read-class only: iam list/get/simulate, s3 get-bucket-policy, s3 list (seat, exempt identity, KeyCount only, never as a negative arm). No assume-role was attempted because no candidate existed. Nothing written anywhere.

## Arm (a) census (principal.out)
- Denominator: 258 roles + 7 users. Users are ineligible as assume targets (the seat holds no credentials for any user but itself).
- FULL live ArnNotLike lists, printed before choosing: inflection = role/*-inf-*, Andrew_Berman, Andrew_Berman_Console, Opal_Terminal; cottonwood = role/*-cot-*, same three users. Each policy is a single Deny statement (no Allow).
- 12 roles carry trust that admits the seat (10 unconditioned; opal-gateway-access-admin with ArnNotEquals on a role, outset-drift-publisher-laptop with a RoleSessionName condition, both meetable by the seat). All 12 simulate to implicitDeny for s3:ListBucket on both buckets; therefore none is eligible.
- Simulator positive control: opal-news-lambda-role = allowed via AmazonS3ReadOnlyAccess (its trust is the lambda service, unassumable by the seat) -- shows the simulator can return allowed.
- Consequence for the instrument: any assumable role would be denied by its own IAM, giving an un-attributable denial. No attempt was made.

## R93-AC3 (judgment, no verdict)
Non-verdict branch taken: no principal granting statement exists to print for either bucket, no positive arm was possible, no denial exists. Routed to 1.0.0_SA_CTO for NOT_EVALUATED grading by 3.0.0_SA_CVO~B.

## Notes
- The live policy bytes hash (sha256 of the returned string, first 16): inflection dc24de63e81b3614, cottonwood 33992a39fefe172b; these differ from the IB-rth-8 hashes quoted in the order (2d90b2f1a01bada3 / b095cbbfe6572ae6). NOT reconciled: the hashed form (raw returned string vs the earlier worker's form) was not established, so no drift claim is made either way. Both policies keep the identical single-statement shape.
- Row: IRPT_BCKEND-W11-S1.
