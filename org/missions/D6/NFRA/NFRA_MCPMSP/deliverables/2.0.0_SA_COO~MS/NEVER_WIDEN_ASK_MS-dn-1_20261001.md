# MS-dn-1 -- never-widen ask (G-NW-E1): the gateway identity's firm-key Deny, Terraform act #3 of the train (2.0.0_SA_COO~MS, 2026-10-01 ~14:1xZ)

- **Order:** `org/missions/D6/NFRA/NFRA_MCPMSP/task-orders/NFRA_MCPMSP.TO-MS-dn-1.gateway-firm-deny.md` (staged; HELD on
  G-RDR, G-NW-E1 and MS-d-2 live).
- **Train:** CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_20261001_OPAL_GATEWAY_RELEASE_TRAIN.md`
  @cf5989190d, R1 (MS-dn-1 last, TF Deny only), R7 (held until G-RDR serves with `unrouted=0`), C4 (TF act #3).
  Design: CTO ruling 27414 (E1, option (a)).
- **Asked of `1.0.0_SA_CTO~O`:** the CTO half on the SAME blast radius.

## 0. Preconditions, measured by the issuer at signing (2026-10-01 ~14:0xZ)

| precondition | read | result |
|---|---|---|
| MS-d-2 live (query_v0 through the internal role) | MS-d-2 complete @c3ef981347; `d2.RB.sh` after OG-rl-1: `arn_set=yes`, firm 4313 B, global 1296 B | MET |
| G-RDR served (R7) | 2.0.0_SA_COO~MI msg 27861: MX-r-8 live e3567ce5f7 since 12:36:17Z, ledger `nfra-mcpindex-r6-rdr-release` CLOSED | MET |
| reader census (order AC1) | `e1z.AC1.sh` on CLOUD now: `s3 call sites scanned=20 portal-v2 reader files=3 unrouted=0 verdict=OK` | PASS |
| TF acts #1, #2, #2b done, none in flight (C4) | MX-r-7 complete; OG-pr-1 and OG-al-1 `<status>complete</status>`; `deploy_ledger.py list`: no OPEN or HELD opal-gateway entry | MET |
| Deny absent today (the before) | `e1z.AC2.sh`: inflection firm key `allowed`, cottonwood firm key `allowed`, global key `allowed` | the expected pre-state |
| served control (the before) | `e1z.AC3.sh`: SSM 2ab8932a Success, host-served bytes equal S3 read in the same minute, `matched=9 of 9 mismatched=[]` | PASS |
| role inline budget | `opal-gateway-role`: 18 inline policies, 5712 of 10240 chars (compact JSON); `firm-deny` absent | room for ~250 chars |

## 1. The act

Targeted `safe-apply` of `infra/aws/terraform/opal-gateway/mcpmsp_gateway_firm_deny.tf` (written by MS-ir-1), with a
private TF data dir. The plan must read **1 to add, 0 to change, 0 to destroy**: `aws_iam_role_policy.gw_firm_deny`, whose name
is the builder's `gateway`/`firm-deny`/`policy` output. One statement: `Effect Deny`, `Action s3:GetObject`, on
`arn:aws:s3:::<global portal-v2 bucket>/platinum/mdpf/{49financial,inflection,cottonwood}/*` (builder `scope_long` per
firm). Any other planned change is a BLOCKING row and nothing is applied. No host deploy, no code change.

## 2. Blast radius and rollback

| Key | Change | Rollback |
|---|---|---|
| `opal-gateway-role` inline policies | +1 NEW: the Deny above. No existing statement changes. 18 -> 19 policies, ~5712 -> ~5960 chars of 10240 | `terraform destroy -target=aws_iam_role_policy.gw_firm_deny` (targeted, seconds) |
| what `opal-gateway-role` can read | NARROWS ONLY: `s3:GetObject` on the three firm segments under `platinum/mdpf/` becomes explicit Deny. Global keys and every other bucket are unchanged | the same destroy |
| served reads on the host | unchanged by design: `query_v0`, `asker_scope`, `portal_index` and `opal_discover` read through `gateway-global-internal-reader-role` (MS-d-2, G-RDR); partner reads through the firm roles | the same destroy |

**Writers of the named property:** `opal-gateway-role` inline policies have **2** Terraform writers, the `opal-gateway`
root and `mdpf-pipeline` (`gateway-taxsma-workbook-bearer-read-policy`, MDPF_TAXSMA, laptop-applied). This act adds one
policy in the `opal-gateway` state, and a targeted apply does not touch the other state's policy. N = 2, both read.

**Not touched:** every other role and policy, every grant, every secret, the ALB, the host and its `.env`, and
`gateway-global-internal-reader-role` (its trust and permissions stay as MS-ir-2 applied them).

**Residual the census cannot see:** a process on the host that reads a firm key with the INSTANCE role and is not
gateway app code (AC1 scans `app/**`). AC3 is the served proof that catches it: the 9 host-served objects are re-read
after the apply.

**Both branches of each leg:**
- AC1 prints any unrouted reader at the act -> nothing is applied; a BLOCKING row is filed.
- The plan is not 1/0/0 -> no apply.
- The apply fails -> nothing is attached, or the partial resource is destroyed by target; the ledger closes ROLLED-BACK.
- AC2 after the apply is not `explicitDeny` / `explicitDeny` / `allowed` -> destroy by target; ROLLED-BACK.
- AC3 after the apply shows ANY mismatch, or a served read errors -> destroy by target in the same session; ROLLED-BACK;
  BLOCKING row.
- AC5 (judgment, `3.0.0_SA_CVO~O` at L9): the before and after answers are recorded in the worker's deliverables. A
  served change found there reopens this act through a CVO row, and the rollback is the same destroy.

## 3. The COO half -- SIGNED

I, `2.0.0_SA_COO~MS`, sign the blast radius in section 2 for the act in section 1. It covers both branches of every leg.

**VOID on:** a plan other than 1 add / 0 change / 0 destroy on `aws_iam_role_policy.gw_firm_deny`; a Deny statement whose
resources differ from the three `platinum/mdpf/<firm>/*` prefixes of the global portal-v2 bucket; `unrouted` other than
0 at the act; another opal-gateway Terraform act open or in flight; any change to the host.
