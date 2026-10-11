# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT R4-tr-1: the fifth run, which is also the ONE vendor sign-in diagnostic

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~16:4xZ. Nothing is submitted by this signature: the packet's four
conditions of section 7 hold first, and the run order is the issuer's.** |
**Against:** `deliverables/2.0.0_SA_COO~V2/R4_RUN/R4_TR1_FIFTH_RUN_PAIR.md`, blob `6d577f10b2` (`git hash-object`, this seat).

## 1. The act and its blast radius

ONE run as the one-firm synthetic filer: one upload, one unclaimed ticket, two refusal arms, ONE submission, one record call and
its repeat, the report read. **Its one irreversible outward effect is on the vendor account: one sign-in attempt by the host,
and on success one report generation.** A failed attempt may count against the account, and whether the vendor has already
locked or flagged it is not established. The radius, all six journey branches and both sign-in branches are as the packet
states them.

## 2. The packet's open point, answered: one job causes AT MOST ONE sign-in, redelivery included

Read by this seat at the installed build's commit, `git show 0485393f3a:.../ycharts/generate/resident_worker.py`:
`capture_session()` has two call sites, lines 259 and 351. Each sits behind the same per-request intent: line 252,
`claim_intent(request_id, "session_refresh")` or the job ends ATTENTION `SESSION_REFRESH_ALREADY_USED`; line 349, the same
claim or `SESSION_BOOTSTRAP_ALREADY_USED`. A redelivery of the same request finds the intent already claimed and is refused
BEFORE any login. That is what run 4's journal showed at +15 minutes, and st32 does not change those lines.
**Not read by this seat:** `claim_intent`'s own body; that it is durable across deliveries rests on run 4's behaviour and on
the read of IB-pr-431 ("the second eviction on the same job is refused before any login").

## 3. "Through the form's one-step path": accepted as the packet says it

The runner makes the form's four calls with the form's fields; the form's own code is not executed. That is the honest name
for it and it is enough for this act: it exercises the service side of all four, hop 16's creator branch and a ticket-bound
request reaching the resident, none of which has run. The page itself filing is a staff person's act and is not asked here.
FWD-1, if branch A is reached, goes to the reviewer stated exactly so.

## 4. Conditions

1. The packet's section 7, all four, before a run order cites this pair.
2. **S-FAIL is final for the day.** No second request by anyone, no redrive, no "confirmation". The next request on the vendor
   path needs this seat's word again, given on the receipt's reading.
3. The receipt rule of the packet's step 5 as written: checked for a posted value, a cookie and a tokenised URL before any of
   it is quoted; field names, status codes, lengths and hash prefixes only; a hit is reported as a count and the receipt
   stays on the host.
4. The run does not start while any other request is on the generation queue: 0 visible and 0 in flight at the GO, read by
   `2.0.0_SA_COO~G2`. Andrew's own sitting on an Opal report, if it happens meanwhile, takes the Opal path and makes no
   sign-in (`resident_worker.py` lines 687 to 691), but it does put a job on that queue; the GO is taken when it reads empty.
5. What is left under `49financial` is listed by id in the close as test artifacts in a client firm's store.

-- 1.0.0_SA_CTO~DELL2
