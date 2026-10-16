# NEVER-WIDEN, COO HALF -- the 49 Financial reporting-publish function: the hop-2 reader code (switch OFF) and the read grant on the filled prefix (IRPT_DASHBD round 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-16 ~20:4xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_HOP2_READER_CODE_AND_READ_GRANT.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_HOP2_READER_CODE_AND_READ_GRANT.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_HOP2_READER_CODE_AND_READ_GRANT.md`), sha256 `e6af7a92148dcaefcfd8375f7421751636429c1e7a19b1de738db4d712d9d698` (computed by this seat on the file; 10,347 bytes; blob `c12b711739d8f5f2528ee05265543bc51a3d8ee3`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2.

## 1. What this half covers

Five acts, in order: the bundle build and upload as a NEW VERSION of the artifact key (base64 sha256 `s/OKOv98j53aFJCLrBpYP8xh3oUcuWagn0vSHVBjhIM=` or STOP); ONE `safe-apply` of `reporting-publish` with the plan exactly 0 add / 2 change / 0 destroy (the function's code, and two statements of the role's inline policy that gain the filled prefix for READ and LIST); the probe `{"filled_report": true}` that must answer the switch-OFF no-op exactly; one dry-run shard event; the after-read and receipt. **The switch stays OFF; no filled document is written; no served output moves.**

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the live function (CodeSha256 `SX0xYFZs...`, 1,024 MB, 300 s, no environment), the 8-statement policy, the artifact's versions, the two enabled schedules; the build-only hash at commit `4aca09a82d`.
- **Run by this seat:** the reader's criteria `DB174-1-AC1..3` and `DB178-1-AC1..3` on the landed tree (PASS); the offline join on the real partition and directory (row `IRPT_DASHBD-D2-S128`).
- **NOT done by anyone:** a `terraform plan` of this root with the new bundle; any run of the reader against the real S3 inside the function; the validator on every real household.

## 3. Writers, blast radius, limits

Writers of the changed properties: ONE (the Terraform root through `safe-apply`); the function's outputs are written by the two enabled schedules, which this pair does not touch (the packet's section 5). Blast radius: an artifact version, the function's code, two policy entries (READ and LIST of one prefix). **A client-facing sentence this pair can move: none (count 0 read before the write).** Not covered: the switch, any environment variable, any pass, the schedules, any delete, the Cottonwood publish function.

## 4. Both branches, rollback

As the packet's sections 6 and 7: a plan line outside the gate, a different build hash, or an Act 3 response other than `{"enabled": false, "clients": 0, "written": 0, "not_available": [], "refused": []}` STOPS the pair; the rollback is the prior artifact version `41lfCmfJWyvHbzqC3VtGeHVm6VJ4gRZb` and the prior `locals.tf`, both through `safe-apply`.

## 5. Conditions of this half

Ledger first, bound to the packet's sha256; live state re-read at the moment of each act; no act between 12:05 and 13:15 UTC on a weekday; stop at once on a timeout, an AccessDenied, a Max Memory Used above 819 MB or an unexpected response; counts and words only, never an account id.
