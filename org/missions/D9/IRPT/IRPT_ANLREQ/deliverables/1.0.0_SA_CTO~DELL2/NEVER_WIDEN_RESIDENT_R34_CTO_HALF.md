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

## RE-SIGN on the rebuilt packet R34B (2026-10-16 ~04:2xZ)

The signature above (blob d18241a3b0) is **SUPERSEDED**. **SIGNED** now on
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34B_20261016.md` (commit `49f29af269`), blob
`f787a4eabcced9d53c96662e25605f69493c0fcf`, sha256 `2ed0b51b88586d0693f6b7ff1247cc372f048d94d22918418cb50c799a5b7742` (both re-measured
by this seat). Pin `4aad96b3c0`; tar `861e6900...abe8`, 314 members (8 changed, 4 added).

**Read: the diff against the signed packet.** It adds the door's yfinance checker (CTO msg 8968: `resident_session.py` changed,
`intake/yfinance_check.py` added) and section 2c. The checker's bound per upload: at most 10 symbols, one history call each, 1 s apart,
about 10 s added. A 401, 403 or 429 stops the batch. A symbol beyond the cap or stopped reads UNAVAILABLE, never absent. Only
provider-NOT_FOUND, registry-unresolved symbols reach Yahoo. Accepted.

**Every condition above stands,** plus:
- **V2's checker call on SPY must read KEPT.** A missing library (`CheckerUnavailable`, so every symbol reads CHECK_FAILED) is a STOP
  before the ledger closes, because it would silently turn every unknown ticker into a check failure.
- **The two owed rows stand,** and the checker adds no cache on the resident. If repeated uploads show Yahoo pushback, the per-day KEPT
  cache joins the negative cache as one row, owner `~G2`.

## RE-SIGN on R34D, r34c under its own names (2026-10-16 ~06:4xZ)

R34B's signature is **SUPERSEDED** (rolled back at V2: no yfinance on the host). R34C was **REFUSED**: its pre-read and D1 could not pass
over the kept r34 root and keys. **SIGNED** now on
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34D_20261016.md` (commit `d83bd3f12e`), blob
`6feb7b728c7bddf8ffb21db1533e0654cee5f498`, sha256 `52dfdd69eb8626652a3d415f98e604a4af6b4990c785cd61813873ef547e1afd` (re-measured).
Pin `bc9f2d0c44`; tar `272d5c54...2ff8` (`irpt-resident-0485393f3a-r34c.tar.gz`), 314 members (10 changed, 4 added).

**Read: the diff against R34C.** It changes the release names to r34c (root, tar, sums, host script), and the pre-read checks the r34c root
absent. The first attempt's r34 root and its three S3 objects are untouched and are never deleted by this release. The content is otherwise
R34C's: the swap, the pool, the door's yfinance checker, and the hop_failure writers (2d) with V3. r35L, the reader, is live (AQ2 msg 9129),
so the writers land behind a reader that exists.

**Conditions:** every condition above stands, plus:
- **Step 1 is a hard gate:** the yfinance 1.2.0 closure is installed under its own signed pair, which this seat approves by its exact
  name==version list, before D1.
- **V2 SPY must read KEPT.**
- **V3, the host role's UpdateItem on `irpt-jobs`, must be allowed.** Either failing is a STOP, and the release rolls back to r32 the
  same session, never left half-landed (NEVER-2).


## SIGN on r34d, the checker fix (2026-10-16 ~12:1xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34D_CHECKER_FIX_20261016.md`
(commit `2e31c78618`, msg 9328), blob `60cf9b70bcf5cb159881d708db2001bd44c576a3`, sha256 `1961c68f13d0f2b4df47ae2dab4052c23f7a81be519b0b78af60dfcb96b152df`, 8,431 bytes (re-measured). Pin `11e0751415`; tar
`9a088a5c...78ab`, 314 members, 3 changed (the checker, the bindings' package pin, the sums). The r34c root stays and is the rollback.

**Read at signing.** The code change (merge `b535f41cb8`) is the one I set in msg 9291: `default_history` returns no rows only when the
exception's MRO holds the exact class name `YFTickerMissingError`, and re-raises every other exception, so a rate limit, a timeout or a
connection error stays CHECK_FAILED. The V2 script's sha256 equals the packet's `90802b18...7940` (re-measured).

**Conditions** (each a STOP):
- **Every host script is sent AS ROOT;** the pre-read must find `0485393f3a-r34c` running (exit 40 otherwise).
- **V2 runs in the service's own environment and must print `V2S OK SPY KEPT and ZQXWVK NOT_KEPT`.** Anything else rolls back to r34c
  the same session (NEVER-2), and the ledger closes ROLLED-BACK.
- **Run 3's hold stays until this ledger reads CLOSED.** The re-probe then goes under AMENDMENT 3 of the run-3 pair, which I sign
  separately; its probe objects join row dc59's delete list.
- **The known limit stands as accepted:** a transient "no price data" on a real symbol now reads NOT_KEPT and offers Replace or No.
