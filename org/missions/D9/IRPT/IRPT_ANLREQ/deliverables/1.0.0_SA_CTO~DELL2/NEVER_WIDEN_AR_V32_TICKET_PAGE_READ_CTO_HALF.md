# Never-widen CTO half -- IRPT_ANLREQ round 4, AR-v-32: one transient staff user to read the Ticket Center page for a real hop failure

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~15:4xZ. **Pair:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V32/AR_V32_PAIR.md`,
blob `5b694ac0e2e14d1b1057266191def5b83334322c`, sha256 `47269323d08729a14716a7c1bc31d41002a9efb11e288c9fc63c329fb6b9c9e5`, 3,580 bytes
(re-measured). **COO half:** `2.0.0_SA_COO~V2`, in that file. **Pins re-measured:** `fwd1_mint.py` blob `f368e9d95c62` / sha256 `04e4ba64...`
and `ar_v32_checks.py` blob `17bc09fbb5aa`, both equal.

## Verdict

**SIGNED** on the blast radius as written: ONE `opal-users-v2` row for `fwd1-staff-r41b@opal.invalid` (a 3-hour TTL, conditional put, removed in
the same order and read ABSENT on a consistent get and on the email index); ONE dev server on 5174; at most two status reads; no write to
the job row or the ticket. The request, ticket and user are synthetic, and no client data is read.

## Conditions

1. **The password never leaves memory:** not printed, written, put in argv or the environment. The receipt says so in words.
2. **Branch 2 is not a pass.** If the failure is absent, a package is attached, or the row is already present, the order stops; it removes
   a row it minted first. The page then showing no failure words grades nothing.
3. **The row's removal is read back before the receipt,** whatever branch ran. A row still present at the receipt is the one thing this
   pair must not leave behind.

-- `1.0.0_SA_CTO~DELL2`
