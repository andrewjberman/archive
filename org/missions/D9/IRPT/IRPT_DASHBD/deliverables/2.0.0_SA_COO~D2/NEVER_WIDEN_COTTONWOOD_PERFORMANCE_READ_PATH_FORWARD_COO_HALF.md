# NEVER-WIDEN, COO HALF -- the Cottonwood Performance read path: a new Cottonwood read function and the forward from the 49 Financial read function (IRPT_DASHBD round 150)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-17 ~04:1xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD.md`), sha256 `07e9ab116825445bd7414e3963075be518036fe4eb209ceb93a7ede44d97cd87` (computed by this seat on the file; 14,334 bytes; blob `c7eaa9a62962`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2.

## 1. What this half covers

Six acts, in order: the build of BOTH function-map entries to the one hash `DhBc5TbOuUIdp70Op5MHpgCLq1TGnRC845ZwjEeQmoE=` (32 members) or STOP; ONE `safe-apply` of the new root `reporting-read-iso` with the plan exactly 5 add / 0 change / 0 destroy; three direct probes of the new function (manifest, series, and a forged-forward event that must be refused); ONE `safe-apply` of `reporting-read` with the plan exactly 1 add / 1 change / 0 destroy (the forward policy; the function's code and its one new environment variable); five probes through the live function (control, forward of manifest and series, a firm the literal map does not name, a non-internal caller); the after-read and receipt. **The API routes, the authorizer, every stored object and the Cottonwood bucket policy do not change.**

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the live 49 Financial function (code hash, environment keys, 512 MB, 29 s), its role's three policies (hashes in `p189`), the artifact's versions and the rollback version, the Cottonwood bucket policy (7 statements), the 939 platinum reporting account prefixes, the directory pointer.
- **Run by this seat:** `p185` (the forward code, AC1..3), `p186` (the Terraform, AC1..3) and `p187` (the function-map, AC1..3 including the real build-only run of both entries) on the landed trunk (PASS); the selftests of `p185`, `p186`, `p187` and `p189` on reference trees and synthetic records (red on 5, 30, 30 and 50 single-fault mutants).
- **NOT done by anyone:** `terraform validate` or `plan` of either root (the box has no terraform binary: the plan lines are INFERRED and gated exactly); any invoke of the new function; a forward across a real Lambda invoke; the page.

## 3. Writers, blast radius, limits

Writers of the changed properties: the Terraform roots through `safe-apply` (one each). Blast radius: one new function, role and two policies that nothing invokes until Act 4; the 49 Financial function's code and one environment variable; one `lambda:InvokeFunction` statement on one function. **A client-facing sentence this pair can move: the Performance tab of a Cottonwood account viewed by an Opal staff user, from "absent" to the published series (objects that exist and are not written by this pair; counts equal before and after).** Advisor and client viewers of Cottonwood read an empty map and are served nothing new. Not covered: any ownership-map write, any change to a staff profile row, any route, the schedule of the Cottonwood publish function, any delete.

## 4. Both branches, rollback

As the packet's sections 5 and 6: a plan line outside a gate, a different build hash, a probe outside its expectation, or a forged-forward event that returns data STOPS the pair; the rollback is the prior artifact version `J9krUD0Qw3fz5QdcfYM4CRg7bYlHNigW` and the reverted roots (revert Act 4 first), through `safe-apply`.

## 5. Conditions of this half

The CTO's four conditions are the packet's section 7.1 to 7.4 (full guard at the target and a forged-forward refusal; the literal one-entry map and no body logged; a simulated allow/deny pair; the 939-series effect named and counted). Ledger first, bound to the packet's sha256; live state re-read at the moment of each act; stop at once on a timeout, an AccessDenied, a Max Memory Used above 80 percent or an unexpected response; counts and words only, never an account id, a name or a body.
