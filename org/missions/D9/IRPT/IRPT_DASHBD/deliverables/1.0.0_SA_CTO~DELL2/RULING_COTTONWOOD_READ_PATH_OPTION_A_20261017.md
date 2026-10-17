# Ruling: the Cottonwood Performance read path -- option A (2026-10-17 ~01:3xZ)

**Seat:** `1.0.0_SA_CTO~DELL2`. **On:** `2.0.0_SA_COO~D2`'s plan
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/COTTONWOOD_READ_PATH_PLAN_20261017.md` (@bba0548150). It answers Andrew's smoke
(2026-10-17 ~01:0xZ): the Cottonwood Performance tab reads OBJECT_NOT_COVERED, because the reporting-read route has a 49 Financial function
only.

**RULED: A.**
- A NEW `irpt-cot-reporting-read-lambda`. Its role carries `-cot-`, so the Cottonwood bucket's `DenyForeignFirmPrincipals` admits it, and it is
  scoped to Cottonwood's platinum reporting prefix only, with addresses by `address()`. New root `reporting-read-iso`.
- A ONE-FIRM FORWARD in the 49 Financial read function. It gains `lambda:InvokeFunction` on that one function ARN and NO S3 grant.
- B is refused: it needs an exemption to a bucket-policy Deny. C is refused: it adds a component on the client path.
- **C0 is authorized:** IB2's read-only trace of the Cottonwood ownership map and the authorizer's firm list.

**Conditions (cross-firm law, CLAUDE.md section 5):**
1. **The Cottonwood function authorizes the request itself.** It runs the full served guard (firm binding, ownership) on the event it
   receives, and trusts NO header or field the forwarder adds. A test sends a forged forward for another firm's id and reads a refusal.
2. **The forwarder is a literal one-entry map** (`cottonwood` to that one ARN), never a generic dispatch. It forwards only AFTER its own
   guard has admitted the caller for `cottonwood`. It never logs or stores the response body. Tests cover the 49F path unchanged, Cottonwood
   forwarded, and any other firm refused.
3. **The 49 Financial role stays without any Cottonwood S3 grant.** A simulate-principal-policy read after the apply shows DENY for the 49F
   role on the Cottonwood prefix and ALLOW for the new role (negative and positive control).
4. **The never-widen pair (C4)** names the client effect: Cottonwood clients' Performance tabs start showing published series, 939 by
   count. It also names the rollback per key (remove the forward, then the function). C5, `~C2`'s real run, is the acceptance: Thiessen's two
   accounts read served.

-- `1.0.0_SA_CTO~DELL2`
