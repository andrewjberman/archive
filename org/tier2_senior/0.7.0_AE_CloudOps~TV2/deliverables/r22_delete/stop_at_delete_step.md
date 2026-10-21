# TO-R22-DL1 AMENDMENT 5 -- STOP at the first delete (bucket policy), 2026-10-21 01:00Z (0.7.0_AE_CloudOps~TV2)

Result: ZERO of 46 versions deleted. Roles created 00:58:35Z, used once, destroyed 01:03Z (4 roles and 4 inline policies, all read ABSENT: NoSuchEntity). Deny `DenyS3DeletesOnProductionData` (cloudops-dell-agent-deploy-policy v7) intact. All 46 entries re-read PRESENT at their versions (`r22_precond_readonly.py`, 01:05Z). No other identity used; no policy edited.

STOP: role 0 assumed (900 s); the first `s3:DeleteObject` with VersionId on `opal-data-cottonwood/.../8b46f055...tckt-r20-trade-synthetic.csv` returned AccessDenied (`delete_pass_output.txt`).

CAUSE (read-only): the `opal-data-cottonwood` BUCKET POLICY statement `DenyForeignFirmPrincipals` (Deny `s3:*`, Resource the whole bucket) applies to every principal NOT in a 10-entry `ArnNotLike` allow-list (`role/*-cot-*`, three named users, `cloudops-dell1/2-agent-user`, `irpt-holdings-role`, ...). The throwaway role `opal-ticket-residue-delete-0-role` is not on it, and an explicit bucket-policy Deny beats the role's Allow. (`DenyRestrictedWriteExceptBreakglass` covers only the `commonwealth/cottonwood/bronze/crm/*` prefix and is not the cause.) `opal-data-irpt` carries only `DenyInsecureTransport`: no bucket-policy block for the 42 irpt entries (UNTESTED: the pass stopped at the first object, entry 1 of 46, which is cottonwood).

A DEFECT IN THE PAIR, not the applier: the pair assumed the role's IAM Allow alone decides; the cottonwood bucket policy is a second gate the pair did not read. The manifest lists the 4 cottonwood entries first, so chunk 0 hit it before any irpt entry.

Owner decision (CTO / COO~V2), nothing the applier may do: (a) split the pass: irpt 42 entries by the same mechanism (re-cut chunks, re-signed pair), and the 4 cottonwood entries by an act the cottonwood owner approves (the allow-list names the identities that may touch the bucket; a role name matching `*-cot-*` is the pattern that already passes; a bucket-policy edit is Andrew's); or (b) leave the 4 cottonwood objects as residue. I did not use the breakglass role or any other identity, and edited no policy.

Also read at 01:05Z: `terraform plan` of the ticket-center root with the pair HCL = 8 to add only (nothing else drifted). A whole-root `plan -destroy` was run once by mistake while planning the role destroy: it lists the entire root and was NEVER applied; its planfile was deleted and the destroy was applied from a `-target` plan of exactly the 8 resources (0 add, 0 change, 8 destroy).
