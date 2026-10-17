# NEVER-WIDEN, COO HALF -- the Inflection transaction table: the runner role's scoped policy (four statements), the release of the launcher, its bundle and receipt and the dispatch script, and a bounded first run on the Orion gold runner (IRPT_DASHBD rounds 137 to 139)

**Signer:** 2.0.0_SA_COO~F2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-17 ~08:1xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md`, committed at `3fc1d3094c`), sha256 `ad67beeb8c5ce93838ce4b763c07d359d709758a454d7ca4c9807eba653cf215`
(computed by this seat on the file; 15,420 bytes; git blob `8fd04a29dc0b`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's two questions (section 9). **Nothing is planned, applied, uploaded, started or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Eight acts, in order, each with its stop. (1) The role audit, read only; another assuming principal STOPS the pair. (2) ONE `safe-apply` of `infra/aws/terraform/inf-pipeline/`, plan exactly 1 add / 0 change / 0 destroy: the one resource `aws_iam_role_policy.inf_gold_layer_account_transaction` with FOUR statements (S1 GetObject on the Orion Inflection `fact_transactions` silver prefix's children, S2 ListBucket on the silver bucket under `s3:prefix` of that prefix, S3 PutObject on the one Inflection gold prefix, S4 ListBucket on the gold bucket under `s3:prefix` of that prefix; no GetObject on gold). (3) The policy simulation with its ALLOW and DENY lines, S4's included. (4) Four uploads to `opal-data-inf/code/gold/`: the launcher, the bundle zip built twice, the bundle receipt (`make_receipt`: the build's `bundle_sha256` and the 14 shared members' sha256), and the dispatch script, which replaces the live copy (rollback target the live version `0JwOjjCwp0uaux9Ded7FlOAMNWtTfZdU`). (5) The runner started and the flat sync's listing printed. (6) A DRY RUN on the runner printing S6 N of N. (7) ONE bounded first write by `--since`, at most 25 trading days. (8) The runner stopped and the receipt.

## 2. What this seat measured and re-ran, and what it did not

- **Re-run by this seat on the landed tree (box/dell2, LOCAL), all PASS:** the policy cells `DBF137-5-AC1` and `AC2` (the original three statements) and `DBF138-3-AC1` and `AC2` (S4, a pure insertion; the round-137 criteria still PASS after it); the launcher's bounded default `DBF138-2-AC1` to `AC3`; the manifest split `DBF139-1-AC1` to `AC3`; the launcher test file 77 passed, 0 failed, 0 errors (59, 2, 7 before the split).
- **Live state, read by this seat today (read-only):** the role's thirteen inline policies, none for the transaction table; the runner stopped; no `INF_G_01*` object in `code/gold/`; the live dispatch script's version, size and ETag, matched by MD5 to the repo's commit `e7d5361cf9`, and the repo's new version is that plus exactly the round-135 TXN block and the round-137 ASCII cleanup (two commits, 145 changed lines); the target gold prefix at 0 objects in an existing bucket; the source's snapshot counts.
- **Graded by the CVO:** the Inflection producer, DBF136-1-J1, PASS 20 of 20 on contract 0.5.1 (v146).
- **NOT done by anyone:** a `terraform plan` of the inf-pipeline root with the new resource; the runner's first run of the launcher (the flat-directory path with the zip and receipt beside it has been exercised offline by tests, never on the runner); the in-instance read time of the snapshot; the S6 print on the release day's snapshot.

## 3. Writers of the changed properties, counted

One rule writes the Inflection `account_transaction` prefix (the launcher through `emit_transaction_day`), N = 1; the new IAM statements are one policy of four statements. The dispatch script gains one block (the TXN-BLOCK) and loses no existing behaviour (the diff against the live version is only that block and the ASCII cleanup).

## 4. Blast radius, and the limits this half signs under

- Act 2 gives the runner's role a read of the Orion Inflection transaction silver and a list and write of one Inflection gold prefix: a new read on client data, inside the never-widen scope the CTO's XA-a222 ruled yes. Act 4 adds three new code objects and a new version of the dispatch script; the next nightly chain then runs the best-effort block, bounded by the default window (the trading days after the newest written day, 25 at most) and unable to change the chain's exit. Act 7 writes up to 25 NEW partitions at an empty prefix and overwrites no existing key. **No existing gold table, the filled report, the published series or any other firm's data is read or written.**
- **Honest limits, signed on:** no plan has run; the runner has never run the launcher; the shared registry members of the bundle carry no cut pin (the release's receipt records them, so a change by another lane before the release is recorded, not refused); the new table has no reader.
- **Not covered:** any day earlier than Act 7's window (earlier history waits on a CVO sample from the written prefix); the Cottonwood and 49 Financial sides; a schedule or alarm; any reader; any delete of any object or version.

## 5. Both branches

The packet's acts state their expected outcomes and their stops; the branches are: A as stated; B (a denied action: Act 2's simulation or Act 7's write) stops with the policy read-back first; C (the producer refuses a day) stops and reports the text, never worked around; D (a missing receipt or zip beside the launcher, or a zip that differs from its receipt) stops, the launcher REFUSES by design; E (S6 with a missing equal line) stops the release; F (a repeated Act 7) writes the same keys and bytes except a manifest's build time, acceptable.

## 6. Rollback, per key

As the packet's section 7: the policy by a `safe-apply` removing the one resource, with the CTO's word; the dispatch script by copying the prior version back over the key (a copy, no delete); the three new code objects and the new partitions are NEW keys with no prior version, and their removal is Andrew's act, never done here.

## 7. Conditions this half signs under

The packet's section 8 as written, in particular: the order of firms (Monday's 49 Financial first-fire read first, one firm changes per fire day, never with another IB2 apply); Act 1 first and Act 3 after Act 2; the ledger entry first, bound to the packet sha256, with every live worktree's `.open_deploys/` read and the denominator printed; Acts 4 to 8 outside the nightly chain's window; no delete, no bare `terraform apply`, no `update-function-code`, no schedule or alarm; stop at once on the listed conditions.

## 8. Signature

I, `2.0.0_SA_COO~F2`, sign this half on the packet sha256 above. This signature authorizes nothing until `1.0.0_SA_CTO~DELL2`'s half is SIGNED on the same bytes, and it covers only what section 1 lists under the limits of section 4.

-- 2.0.0_SA_COO~F2
