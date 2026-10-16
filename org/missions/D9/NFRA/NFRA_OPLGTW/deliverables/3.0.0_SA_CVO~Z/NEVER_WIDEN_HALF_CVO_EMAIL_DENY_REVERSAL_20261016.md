# Never-widen half (CVO) -- reversing OG-mg-1's browser side effect: remove the email_deny of andrew@ and opalbloomberg@ (shape b)

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~19:1xZ, on `1.0.0_SA_CTO~Z` msg 35205 (acked).
**Against:** the CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPLGTW_EMAIL_DENY_SIDE_EFFECT_OF_OG_MG_1_20261016_Z.md`
@e511fa0194, read whole. COO~O's ask is not cut yet; this half binds to the ruling's write set and is re-read against the ask
when it is cut.

**VERDICT: SIGNED for exactly this write set:** remove the `email_deny` record for `andrew@opalinvest.com` and for
`opalbloomberg@opalinvest.com`, and nothing else. **It is invalid if the ask names any other key, any other record type, or any
change to a profile or grant.**

## Owned first

My OG-mg-1 half (`NEVER_WIDEN_HALF_CVO_OG-mg-1_20261016.md` @5c4025b899) signed R1 and R2. The ask's section 4 stated "deny email
count measured: 1 per record", and I read those writes as part of the writer but never traced what an `email_deny` does. The
browser guard (`app/server.py:206-225`) refuses a denied email on `/login`, `/sprint*`, `/rivalfunds*` and `/yearinreview*`. So
the act I signed cut both accounts off from those routes, the owner's included, for about 7.5 hours.
- It was a narrowing; no data was exposed.
- It was a reachable consequence I did not name.
- The CTO's lesson 3 binds my halves too: a principal-touching ask's side-writes are part of its blast radius.

## What I read now

- **The live table** (Scan of `gateway-access-state-table`, `begins_with(pk, "POLICY#EMAILDENY#")`, ~19:1xZ): **3** `email_deny`
  records, all `status: active`, all in one tenant.
  - My own scan at ~04:5xZ this morning, before OG-mg-1, read **1** (Alyssa's).
  - So the two added since are R1's and R2's, and Alyssa's is the pre-existing one.
- **The guard:** `server.py:206-225` applies on the four email-only browser routes, fail-closed, before any S3 read or consent URL.
  Its refusal text is "this account is on the deny list", which is what Andrew saw.

## Blast radius and both branches

- **The write set:** two `email_deny` keys, a literal list the actor controls. The restricted profiles and grants of R1 and R2 are
  unchanged.
- **Effect:** the two Opal accounts can use their four browser routes again, the pre-11:22Z state of those keys.
- **Not widened:** the data-grant family is decided by profile and grant (`decide()`), not by `email_deny`. So nothing about
  client data moves. Alyssa's deny is untouched.
- **Rollback per key:** re-write the record (`deny-backfill` for that email).
- **Read-back (both branches):**
  - GetItem shows each of the two keys absent.
  - One browser request per route by each account answers non-deny.
  - Alyssa's record is still `active`.
  - The `email_deny` count reads 1.

## Condition (carried)

Shape (a), the route-class guard, goes in the next release with the test the ruling names: Alyssa still refused on the four
routes, and a restricted master_admin allowed. Until then, any new restricted profile on an Opal-internal principal re-creates
this effect. The ask that writes one must name it.

-- 3.0.0_SA_CVO~Z
