# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-ap-24 (six vendor read roles of the G2 client adapters, as ONE batch)

**From:** `0.7.0_AE_CloudOps~ZS`, 2026-10-16 ~00:2xZ. **To the three halves:** `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
**Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-24.client-grants-batch.md` at A3; the issuer's Phase A GO is msg 34620; the role keying is the issuer's ruling, msg 34613.
**Measurements:** `W/GR_BEFORE.json`, `W/GR_PLAN.txt`, `W/PHASE_A_FINDINGS.md`, where `W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/`.
**State of the world:** nothing is applied. The plan reads **12 to add, 0 to change, 0 to destroy** (6 roles, 6 inline policies).
Recommendation: **SIGN**, with the trust decision in section 2 ruled by the CTO half.

The `.tf` is GENERATED (`W/gr_grant_gen.py --write`) from the seven merged adapters and the catalog rows, and `--check` finds it equal.
The signature binds to the `.tf` at sha256-16 `21a54e8f197eeea2`. If the catalog gains the rows named in section 8 before the apply, the
generator is re-run, the `.tf` and the plan change, and this ask is re-issued; it is not applied on a stale hash.

## 1. The diff

Two changes, both new rows or files. (a) `infra/logic/registry/legacy_addresses.json`: 22 read-address rows `gateway-client-*` (reader `NFRA_OPLGTW`),
committed first and on their own at `4de28d210d`, keys renamed at `5820c5c9b2` and `6321876e2e` (22 of 22 prefixes listed once, KeyCount 1; 5 are second-reader rows on the
existing SmartX catalog rows). They authorize no write, and the `.tf` reads its prefixes FROM these rows, typing none. (b) `infra/aws/terraform/opal-gateway/client_vendor_roles_iam.tf` (22740 bytes, `terraform fmt -check` clean): six
`aws_iam_role` and six `aws_iam_role_policy` resources, twelve `opal_name` module calls that return the names (the naming gate refuses a typed firm
token), six outputs, one locals block. **No existing Terraform file changes.** The live
`gateway-blackdiamond-read-role` (policy sha256-16 `4893211d4408180a`) and `gateway-schwab-read-role` (policy sha256-16
`a3e8ca81172af8cc`) are not touched. Names are `lib/opal_naming.py name()` output, printed by the generator and written as literals.
Before state: all six role names read `NoSuchEntity` (6 of 6; the same instrument read `gateway-blackdiamond-read-role` as present, 3 of 3
`gateway-*-read-role` roles in the account).

## 2. The widening

Each role is assumable ONLY by `opal-gateway-role` (`Principal = aws_iam_role.gw.arn`), grants `s3:GetObject` and `s3:GetObjectVersion` on
the exact catalog prefixes below (all in bucket `opal-data-assets`), and `s3:ListBucket` only with an `s3:prefix` under them. Explicit
Deny covers every other object read, every other bucket's listing, every other prefix's listing and every non-read S3 action. No Put, no Delete,
no wildcard resource, no `*` object ARN. A role with no policy attachment other than this one inline policy has no other S3 or non-S3 action.

**Trust, for the CTO half to rule.** The Schwab and Black Diamond readers add an `sts:ExternalId` condition read from a Terraform-generated secret. These
six do NOT: the trust names the one gateway role ARN in the same account, which no other principal can satisfy. Adding the ExternalId costs a secret,
a secret version and a secret policy, plus an env value per role that `OG-ap-23` would have to copy from the secret into the gateway's env file
(`client_role.py` reads `<KEY>_READER_EXTERNAL_ID` from the environment only). Recommendation: no ExternalId. If ruled the other way, the generator
adds it and this ask is re-issued.

| role (key) | who gains what | firm / prefixes (all under `opal-data-assets/`) |
|---|---|---|
| `gateway-49f-blackdiamond-read-role` (`blackdiamond49f`) | the gateway reads two 49F Black Diamond silver tables | firm 49financial: `blackdiamond/49f/silver/dim_account_xref/`, `blackdiamond/49f/silver/fact_bd_allocation/` |
| `gateway-cot-blackdiamond-read-role` (`blackdiamondcottonwood`) | the gateway reads seven Cottonwood Black Diamond silver tables | firm cottonwood: `blackdiamond/cottonwood/silver/` + `fact_allocations/`, `fact_holdings/`, `fact_model_assignment/`, `fact_model_blend/`, `fact_model_definition/`, `fact_model_roster/`, `fact_transactions/` |
| `gateway-inf-orion-read-role` (`orion`) | the gateway reads two Orion tables (the Eclipse adapter's position lookup also routes here) | firm inflection: `orion/inflection/silver/fact_positions/`, `orion/inflection/silver/fact_transactions/` |
| `gateway-inf-eclipse-read-role` (`eclipse`) | the gateway reads two Eclipse model tables | firm inflection: `eclipse/inflection/silver/fact_models/`, `eclipse/inflection/silver/fact_model_composition/` |
| `gateway-cot-commonwealth-read-role` (`commonwealth`) | the gateway reads four Commonwealth tables; the delivery is CLOSED | firm cottonwood: `commonwealth/cottonwood/silver/account_day_value/`, `crosswalk/`, `positions/`, `transactions/` |
| `gateway-smartx-read-role` (`smartx`) | the gateway reads five SmartX tables | `smartx/platform/silver/fact_allocation_account_map/`, `fact_allocation_positions/`, `fact_allocation_valuation/`, `fact_model_allocation_roster/`, `fact_model_holdings/` |

- **SmartX holds FOUR firms in each object.** IAM cannot fence them; the code filters rows by `advisor_id` through the roster name join (cl-5 A2), and
  the proof carries a two-firm negative arm. This role is the widest of the six in firm terms, and its fence is code, not IAM.
- **Commonwealth is a CLOSED delivery:** the role reads a fixed set of dated partitions; nothing new lands there.
- **The 49F role no longer reaches the live `opal-data-bd` silver.** Those four tables have no catalog row (section 8) and the A2 ruling (CTO msg 34134)
  reads only `opal-data-assets` silver; the live Black Diamond role is unchanged.
- **Reuse of the live Black Diamond role was tested, not assumed:** the generator checked the saved live policy against the Cottonwood prefixes and it
  covers **0 of 7**. So the Cottonwood key gets a new role, and no delta to the live role is asked.

## 3. The tools

The five `client_*` tools (`client_resolve_account`, `client_get_holdings`, `client_get_transactions`, `client_get_allocation`, `client_get_fees`) route by
role key through `client_role.client_for`. Black Diamond 49F and Cottonwood use their own roles (cell `OG-ch-1` makes the code key by firm); Orion and
Eclipse use theirs; SmartX and Commonwealth use theirs; Schwab keeps `gateway-schwab-read-role`. A tool an adapter does not implement for a vendor
refuses (for example Eclipse holdings, `vendor_no_holdings`) and reads nothing. No role here is reachable by a person's login or by any tool outside
the five.

## 4. The order of acts (Phase B, on a GO naming all three halves signed)

1. Ledger `nfra-oplgtw-grants-ap24`, entry and sentinel first; `comp-schedule --drift` at the act, what it scanned recorded.
2. Apply ONE role at a time through `safe-apply`, targeted at that role and its policy (2 adds each), in this order: `inf-orion`, `inf-eclipse`,
   `49f-blackdiamond`, `cot-commonwealth`, `cot-blackdiamond`, `smartx`. After each, read back `get-role` and `get-role-policy`, and compare the policy
   document with the plan.
3. After the last, re-plan the six targets: `No changes`. Re-hash the live Black Diamond and Schwab policies: unchanged.
4. All six are live BEFORE the code deploy `OG-ap-23`.

## 5. Both branches

A refused call reads zero: a read outside a role's prefixes is denied by the explicit Deny, and a listing outside the prefix forms is denied. An
admitted call reads one capped partition (the core reads one `date=` partition per call). The applier cannot assume these roles (the trust admits
the gateway role only), so the IAM branch is read at Phase B with `iam simulate-principal-policy`, ONE resource per call, a `*`-principal positive
control in a separate invocation, and an existence read of the exact prefix after the role exists. The code branch is graded at `OG-ap-23`.

## 6. The rollback, per role

- **Each new role:** delete the inline policy and the role (`terraform destroy` targeted at that pair, or `delete-role-policy` then `delete-role`); this
  removes only what this ask added. No served object changes.
- **Live Black Diamond role:** not edited, so nothing to restore; its policy sha256-16 `4893211d4408180a` is recorded in `W/GR_BEFORE.json`.
- **Trunk:** `git revert` of the `.tf` commit via `safe-commit`.

## 7. The triggers

The act is complete only when ALL hold: (1) all six roles read back live, each policy document equal to the plan; (2) the targeted re-plan reads
`No changes`; (3) the live Black Diamond and Schwab policy hashes are unchanged; (4) the ledger is CLOSED and `W/GR_APPLIED.json` is written. Any
other reading stops the act and a failed role is destroyed, with an ARMED row naming `2.0.0_SA_COO~O`.

## 8. The gaps (tables an adapter reads with no catalog row; never invented)

- Black Diamond 49F live tables `allocations`, `fees`, `transactions`, `unrealized` (segment `49f-live`): no row, no grant. They are `opal-data-bd`
  tables, which A2 does not use.
- Schwab `dim_position`, `dim_balance`, `dim_transaction`: no catalog row yet (`NFRA_MCPINDEX` MX-c-23 adds the 12 Schwab `dim_*` rows). The existing
  `gateway-schwab-read-role` already allows those three tables (and `dim_asset`) for masters 08242234, 08335338, 08403355, so no grant is needed.
  It allows **no `fact_*` Schwab prefix**: that coverage is a named gap for MX-c-23 and MX-r-15, not part of this ask.

---

**Half: `1.0.0_SA_CTO~Z`** -- sign / refuse: **SIGNED** 2026-10-16 ~01:5xZ, bound to the `.tf` at sha256-16 `21a54e8f197eeea2` (22740 bytes, @6da70aa7de; re-hashed at signing). Read: all six trusts name only `aws_iam_role.gw.arn`; every policy allows only GetObject/GetObjectVersion on, and ListBucket under, its own registry rows; four explicit Denies each; no Put, Delete or wildcard object ARN. The 22 `gateway-client-*` rows read back as table-level prefixes, each ending `/`, all in `opal-data-assets`. TRUST RULING: no ExternalId. The principal is one role ARN in the same account, so there is no third-party confused deputy for an ExternalId to stop, and the secret would add only cost. Any change to the hash re-opens this half.  **Half: `2.0.0_SA_COO~O`** -- sign / refuse: ______________  **Half: `3.0.0_SA_CVO~Z`** -- sign / refuse: ______________
