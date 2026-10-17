# NEVER-WIDEN, COO HALF -- the Inflection transaction table: a NEW narrow role carrying the scoped policy (four statements) that the runner role assumes, the release of the launcher, its bundle and receipt and the dispatch script, and a bounded first run on the Orion gold runner (IRPT_DASHBD rounds 137 to 139)

**Signer:** 2.0.0_SA_COO~F2. **Status:** SIGNED (REVISION 2). **Date:** 2026-10-17 ~14:1xZ. This half replaces the REVISION 1 half whole; the CTO's REVISION 1 half (@028ec74371) does not carry to these bytes.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md`, committed at `b9b961b3da`), sha256 `5bfd8e040939298b3c2d35fca6c3c3bce12c2931e6b444608c8e5b1a514f1126`
(computed by this seat on the file and on the committed blob, equal; 20,918 bytes; git blob `b3ed1e6da142`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is planned, applied, uploaded, started or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Eight acts, in order, each with its stop. (1) The audit, read only: the runner role's 13 inline policies and trust, the new role ABSENT, the bucket fence's `*-inf-*` pattern present; anything else STOPS the pair. (2) ONE `safe-apply` of `infra/aws/terraform/inf-pipeline/`, plan exactly 3 add / 0 change / 0 destroy: the role `orion-inf-account-transaction-role` (trust the runner role only, fixed session name `g01-account-transaction`), its inline policy with FOUR statements (S1 GetObject on the Orion Inflection `fact_transactions` silver prefix's children, S2 ListBucket on the silver bucket under `s3:prefix` of that prefix, S3 PutObject on the one Inflection gold prefix, S4 ListBucket on the gold bucket under `s3:prefix` of that prefix; no GetObject on gold), and the runner role's one-statement policy (`sts:AssumeRole` on the new role only). (3) The simulation of the NEW role, the gold-bucket lines WITH the live bucket policy as the resource policy, plus the runner's AssumeRole line. (4) Four uploads to `opal-data-inf/code/gold/`: the launcher, the bundle zip built twice, the bundle receipt, and the dispatch script, which replaces the live copy (rollback target the live version `0JwOjjCwp0uaux9Ded7FlOAMNWtTfZdU`). (5) The runner started and the flat sync's listing printed. (6) A DRY RUN on the runner printing the assumed role and session and S6 N of N, stopping above 40 minutes. (7) ONE bounded first write by `--since`, at most 25 trading days. (8) The runner stopped and the receipt.

## 2. What this seat measured and re-ran, and what it did not

- **Re-run by this seat on the landed tree (box/dell2, LOCAL @5ac8427e04), all PASS:** the role cell `DBF139-4-AC1` to `AC3` (the 46 other files identical, the role, trust and policy, the runner's assume policy); the launcher cell `DBF139-5-AC1` to `AC3` (the assume, the main wiring, a flat-directory dry run); the earlier cells `DBF137-5-AC1` and `AC2` as they stood at their merges, `DBF138-2-AC1` to `AC3`, `DBF139-1-AC1` to `AC3`; the launcher test file 83 passed, 0 failed, 0 errors. `DBF138-3-AC1` and `AC2` and the round-137 policy criteria graded the policy on the runner role and no longer describe the tree (the policy moved by DB-f-2704): they are superseded by `DBF139-4-AC2`, not re-run.
- **Live state, read by this seat (read-only):** the runner role's thirteen inline policies, none for the transaction table; the bucket fence of `opal-data-inflection` and what-if results with and without the bucket policy as the resource policy (the finding @e2c69d8f08); the runner stopped; no `INF_G_01*` object in `code/gold/`; the live dispatch script's version matched to the repo's commit `e7d5361cf9`; the target gold prefix at 0 objects in an existing bucket; the source's snapshot counts.
- **Graded by the CVO:** the Inflection producer, DBF136-1-J1, PASS 20 of 20 on contract 0.5.1 (v146).
- **NOT done by anyone:** a `terraform plan` of the inf-pipeline root with the new resources (the 3 / 0 / 0 gate is read from the text and the live absence; Act 2 stops on any other reading); a simulation of the NEW role (it does not exist: Act 3 runs it, with the resource policy); an assume of the new role by the launcher on the runner; the launcher's first run on the runner (the flat-directory path was exercised offline, including a dry run from a flat directory with fakes); the in-instance read time of the snapshot, which sets the one-hour credential margin.

## 3. Writers of the changed properties, counted

One rule writes the Inflection `account_transaction` prefix (the launcher through `emit_transaction_day`), N = 1. The new IAM objects: one role, one policy on it of four statements, one policy of one statement on the runner role. The new role has one assumer by trust (the runner role) and one caller in the repo (the launcher). The dispatch script gains one block (the TXN-BLOCK) and loses no existing behaviour.

## 4. Blast radius, and the limits this half signs under

- Act 2 creates a role that can read the Orion Inflection transaction silver and list and write one Inflection gold prefix, and lets the runner role assume it. **The runner role's own permissions do not widen, but its HOST does:** any process on the runner host holding the instance profile can assume the role under the fixed session name (packet section 4, put to the CTO as question 3). A new read on client data, inside the never-widen scope the CTO's XA-a222 ruled yes. Act 4 adds three new code objects and a new version of the dispatch script; the next nightly chain then runs the best-effort block, bounded by the default window and unable to change the chain's exit. Act 7 writes up to 25 NEW partitions at an empty prefix and overwrites no existing key. **No existing gold table, the filled report, the published series, the bucket policy, the fence, the registry or any other firm's data is read or written.**
- **Honest limits, signed on:** no plan has run; the new role has never been simulated or assumed; the runner has never run the launcher; the assumed credentials last one hour by default and are not refreshed (the dry run is the evidence; above 40 minutes the release stops); the shared registry members of the bundle carry no cut pin (the release's receipt records them); the new table has no reader.
- **Not covered:** any day earlier than Act 7's window; the Cottonwood and 49 Financial sides; a schedule or alarm; any reader; any delete of any object or version; any change to the bucket policy, the fence or an exemption row.

## 5. Both branches

The packet's acts state their expected outcomes and their stops; the branches are: A as stated; B (a denied action: Act 3's simulation, the assume in Act 6, or Act 7's write) stops with the policy and trust read-back first and nothing tried around it; C (the producer refuses a day) stops and reports the text; D (a missing receipt or zip beside the launcher, or a zip that differs from its receipt) stops, the launcher REFUSES by design; E (S6 with a missing equal line) stops the release; F (a repeated Act 7) writes the same keys and bytes except a manifest's build time, acceptable; G (the new role already exists at Act 1) stops.

## 6. Rollback, per key

As the packet's section 7: the three IAM objects by a `safe-apply` of the same root (0 add / 0 change / 3 destroy), with the CTO's word; the dispatch script by copying the prior version back over the key (a copy, no delete); the three new code objects and the new partitions are NEW keys with no prior version, and their removal is Andrew's act, never done here.

## 7. Conditions this half signs under

The packet's section 8 as written, in particular: the order of firms (Monday's 49 Financial first-fire read first, one firm changes per fire day, never with another IB2 apply); Act 1 first and Act 3 after Act 2; the ledger entry first, bound to the packet sha256, with every live worktree's `.open_deploys/` read and the denominator printed; Acts 4 to 8 outside the nightly chain's window; no delete, no bare `terraform apply`, no `update-function-code`, no schedule or alarm, no change to the bucket policy or the fence; stop at once on the listed conditions.

## 8. Signature

I, `2.0.0_SA_COO~F2`, sign this half on the packet sha256 above. This signature authorizes nothing until `1.0.0_SA_CTO~DELL2`'s half is SIGNED on the same bytes, and it covers only what section 1 lists under the limits of section 4.

-- 2.0.0_SA_COO~F2
