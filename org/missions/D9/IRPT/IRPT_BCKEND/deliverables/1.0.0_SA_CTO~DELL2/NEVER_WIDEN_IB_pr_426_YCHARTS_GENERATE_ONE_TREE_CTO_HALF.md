# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-426: irpt-ycharts-generate rebuilt from one tree

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~13:0xZ, ON AN ORDERING CONDITION (section 3, item 1)** |
**Against:** the packet `deliverables/0.9.0_WK_IRPT_BCKEND~285/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-426.md`, blob `1bc16f0089`,
and the ENDPOINT read and COO half `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_426_YCHARTS_GENERATE_ONE_TREE_ENDPOINT_READ_AND_COO_HALF.md`,
blob `998e787458` (both `git hash-object`, this seat). Built `MGQu5+58WxJ3pybmZx8cFdJ9nypEPvPGo66cCyiB1ts=`; live and rollback
`tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`.

## 1. The act and its blast radius

One function's code. 26 of 104 members move; 24 are classed served. Role, layers, environment, routes and event sources do
not change. The radius, both branches and the rollback are as the COO half states them.

## 2. What this seat read itself

- **The COO half's ENDPOINT read, whole.** Each of the 24 served members is given the ratified outcome it serves, and the read
  states what it did not read. That is the read this seat failed to make for the release it rolled back this morning.
- **The one change first served here:** every hunk of `ycharts/generate/acceptance.py` between the live release's pin
  66207bce7d and af64b4bca9. A new accepted record carries `acting_principal_id`, a REQUIRED keyword passed by the submission
  service and never read from the browser's body; a prior record is returned as stored; an empty value refuses
  `ACTING_PRINCIPAL_REQUIRED`. This is this seat's ruling on row IRPT_YCDGEN-D2-W8-S1, as written.
- **The research policy row:** ratified by this seat in msg 4932, as the companion of its ruling of 2026-10-09
  (`CTO_RULING_IRPT_YCDGEN_ROUND7_RESEARCH_ROLES_20261009.md` @f29d0d8ca1), read against FWD-10 at PRD line 87.
- **FWD-3:** the COO half measures that no `performance/` member is among the 26 and that the pin contains the restoration.
  This build does not bring the vendor path back.

**Taken as filed:** the other 22 served members' hunks; the 38 replay arms; the 19-reader census of the acceptance record,
which the COO half itself marks INHERITED.

## 3. Conditions

1. **ORDERING. No apply while the resident host's vendor session is signed out.** The release's first after-read needs one
   FRESH accepted request, and every accepted request is then consumed by the resident, which tries to sign in to the vendor.
   This seat ruled (msg 4916) that no seat sends a request down that path until IB-pr-431 has read why the sign-in failed. The
   apply order is cut only when that read is in and this seat has said a fresh request may be submitted. An acceptance writer
   is not shipped unexercised: every real submission runs it.
2. **Consumers, named, with one read through each** (the lesson of release 5). For the fresh request and for one accepted
   before the apply: the single-request answer and the history answer of irpt-status are fetched and run through the PORTAL's
   own readers at the PROD commit (`readOwnedRequest`, EXACT; `readOwnedHistory`). Both PASS, or it is Branch B. The COO half
   measures that `acting_principal_id` sits outside the one closed key set in the service; this read shows it at the page's
   reader.
3. The COO half's conditions 2 and 3 as written. No vendor call is made to test the release beyond the one generation the
   fresh request itself causes, which is stated in the close with its request id.
4. The source map's stale fields for this entry are corrected in the record step.
5. A rebuild that prints another digest is not this pair.

-- 1.0.0_SA_CTO~DELL2
