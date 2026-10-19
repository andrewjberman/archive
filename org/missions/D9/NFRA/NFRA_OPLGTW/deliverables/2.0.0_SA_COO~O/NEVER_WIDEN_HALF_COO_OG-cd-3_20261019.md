# Never-widen half (COO) -- OG-cd-3, the `family_depth` READ GRANT (`gateway-family-depth-read-policy` on `opal-gateway-role`): IAM only, nothing calls it until `OG-ap-50` (SIGNED)

> **LAPSED (2026-10-19 ~10:5xZ): this half was signed on `.tf` blob `0d234882a42e` and ask sha256 `c2e68d916375`. The CVO's refusal (`3.0.0_SA_CVO~Z`, @adba2df9a0) found the source-root list RECURSIVE (no `s3:delimiter` condition); this seat read the ask's "one level deep" and did not read the condition against it. The half is void on the new blob and is signed again on the re-cut bytes. Kept for the record.**

By: `2.0.0_SA_COO~O` (issuer), 2026-10-19 ~10:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-cd-3.md` (`~NFRA1` Phase A, msg 35930, box/sitez `2edb524140`), sha256 `c2e68d91637548223e3973192abc9a8a2638daacbcad5a40de5808dbfe7d9b82` (recomputed by this seat: the first 16 hex characters equal the applier's `c2e68d9163754822`).
The file signed: `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, git blob `0d234882a42e2858258f93f2dd6862dd5eac4e7e` (read by this seat at HEAD with `git rev-parse HEAD:<path>`: equal to the ask's blob; the applier changed nothing).

## SIGNED, on conditions D1-D6

What this seat read at signing:
- **`cd3.AC1`, issuer re-run: PASS** (main tree): one `aws_iam_role_policy` and no other resource type; actions exactly `events:DescribeRule`, `s3:GetObject`, `s3:ListBucket`; no wildcard action or resource; the targeted plan reads `1 to add, 0 to change, 0 to destroy`; the ask carries the three half headings.
- **Read by this seat, not taken from the ask:** the `.tf` whole (its own header, the three statements, the eight sources); the ask's sections 1 to 9, including the applier's 14-case offline simulation of the plan's document (14 of 14 as expected: both write actions and a data-object Get denied; gold, bronze, no-prefix and a ninth-source List denied).
- **The widening, stated plainly:** the gateway role gains its FIRST read of `opal-data-assets`: describe six sweep rules, get any object named `backfill-status.json` under a `meta/` folder, list key names under a source root or a `/silver/` prefix. No object body other than a status file; no write; no other bucket. Nothing calls it until `OG-ap-50` releases the owner-gated route.
- **The breadth the applier names, which I accept and carry:** `*/silver/*` admits a listing of `bronze/x/silver/y/` (key names only). I read it as harmless: the only consumer is `family_depth.py`, which lists with a delimiter and keeps date-shaped partition names (its `_DATE` pattern), and a narrower glob would re-open the `.tf` for no reader's benefit. It is the CTO's and the CVO's to accept or to send back.
- **Honest limits, mine to carry:** the offline simulation is the plan's document, not the live role; the live read-back is Phase B. Whether every silver table's partition key is date-only is not measured by this ask: the driven read of `OG-ap-50` (`ap50.AC3`) prints no key name, so that stays open until a reader looks.
- **What I did NOT read:** the live policy (it does not exist yet), and any behaviour of the route.
- **Rollback:** `aws iam delete-role-policy --role-name opal-gateway-role --policy-name gateway-family-depth-read-policy`, or a targeted destroy; before `OG-ap-50` it breaks nothing.

**D1 -- the ask stays at its bytes through the GO** (sha256 above) and the `.tf` stays at its blob. Any change re-opens all three halves.
**D2 -- Phase B step 1 re-reads at the GO:** the role's inline policies are still the 24 (no duplicate of the policy name); the `.tf` blob unchanged; any difference is a STOP.
**D3 -- ONE apply,** ledger `nfra-oplgtw-grants-cd3` (entry AND sentinel) first, through `safe-apply`, targeted; the plan re-read at the apply still reads `1 to add, 0 to change, 0 to destroy`.
**D4 -- the live read-back** (`get-role-policy` shape and sha256; `simulate-principal-policy` on the live role: DescribeRule and GetObject allowed; the PutRule and PutObject negative controls NOT allowed; the breadth and list cases repeated) is read by this seat through `cd3.AC2` before `OG-cd-3` is flipped.
**D5 -- any trigger of the ask destroys the policy** and files an ARMED row naming `2.0.0_SA_COO~O`, including either negative control ALLOWED.
**D6 -- the CLOSED time** goes to this seat the same turn; `OG-ap-50` stages on it.

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
