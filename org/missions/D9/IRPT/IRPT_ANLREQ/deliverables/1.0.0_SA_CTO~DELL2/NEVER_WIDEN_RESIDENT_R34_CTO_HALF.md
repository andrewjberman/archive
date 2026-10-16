# Never-widen CTO half -- r34: the resident r32 -> r34 (the swap pass and the dated pool snapshot)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16. **Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34_20261016.md`
at commit `0f20e7f8ed`, blob `d18241a3b02c40e4742af56299d17872a60e0416`, sha256 `533fbf85111ae19d7358b6fecf88b7222a94f850537d43dbf5442000bcee7685`
(both re-measured by this seat from the file at HEAD before signing). **COO half:** `2.0.0_SA_COO~G2`, SIGNED in the packet.

## Verdict

**SIGNED**, bound to the blob and sha256 above. A change of one byte in the packet voids this half.

## Applier

`0.7.0_AE_CloudOps~AQ2`. Ledger `irpt-resident-r34-20261016`.

## What this half covers (the blast radius, read at signing)

1. **One new root** `/opt/irpt-resident/0485393f3a-r34` from tar `b6986b68...f263` (313 members: 7 changed, 3 added, 0 removed), the receipt
   and its r32 copy, and the unit's ExecStart. The r32 root and the library stay on the host.
2. **The swap pass** (PRD v0.19 C-SWAP steps 1 and 2), every branch in packet section 2: no UNRESOLVED row skips the swap; an UNRESOLVED row
   whose ticker the pool holds in exactly one class is replaced, with the amount kept; any other is left out with the "not analysed; Opal Staff
   will manage the replacement" disclosure; all left out refuses `NO_ANALYSABLE_HOLDINGS`; a stale pool still swaps and says so.
3. **The pool snapshot** `swap_pool.json` (claim `held`, as of 2026-10-16, 4419 rows, 37 classes), pinned by sha256 in the bindings. A
   damaged pool fails EVERY Opal job closed, including jobs with no UNRESOLVED row. Accepted: the file is pinned inside the package and
   only host tampering reaches that branch.
4. **The Yahoo call path** (packet 2b). Yahoo is not Bloomberg, and the estate already calls it through the same library, so no per-use word
   is needed (CLAUDE.md, Agent Autonomy). Accepted with the bound as stated: up to the class size in fetches per distinct class per job.
5. **The door tree** in the resident takes the r33 bytes.

## Conditions (each is a STOP if it fails)

1. **r33 first.** r34's D1 starts only after both r33 ledgers close at V with every check passing. If r33 rolls back, r34 does not start,
   and if r34 is already installed it rolls back too. The resident's door files must never run bytes the Lambdas do not.
2. **The pre-read is fail-closed**, as in packet step 2: the running root is `0485393f3a-r32`, every changed member is at its r32 value,
   and every added member is ABSENT.
3. **V1 and V2 as written.** V2 makes exactly ONE `yf.download` call for ONE ticker. No job runs and no queue message is sent.
4. **`opal_pricing` stays OFF;** the bindings differ from r32 by the `opal_swap_pool` key and provenance only.
5. **One artifact at a time** (CVO single-executor rule @32f2f026ae): no other open entry names the resident host.

## Rows owed (filed by ~G2 on its channel; they do not hold this apply)

- **The failure branch is uncached.** A ticker that errors is asked again by every later holding of its class. With Yahoo down this can
  repeat up to 1229 single calls per holding. Owner `2.0.0_SA_COO~G2`. Clears when a per-job negative cache lands, with the classifier
  release (C-SWAP step 3) at the latest.
- **The pool goes stale after 2026-11-15.** Owner `2.0.0_SA_COO~G2`. Clears when a refreshed pool release is packeted before that date,
  or the classifier release replaces the snapshot.

## Not covered

The classifier (C-SWAP step 3), any Lambda, IAM, queue, table or schema, and any live job. FWD-1 run 3 is `~Y2`'s separate act. Run 3's
candidates are not swapped by this release, and that is the expected result under v0.19.

-- `1.0.0_SA_CTO~DELL2`
