# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-421 + IB-pr-422: the vendor performance path without the one-use plan

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~09:0xZ** | **Against:** the COO half
`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_421_422_VENDOR_PERFORMANCE_PATH_COO_HALF.md` @468df7baa4, zip
`OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=`, and the two single-secret grants it names. A rebuild that moves the digest, or
a plan that changes either grant, re-opens this half.

## 1. The act, stated plainly

It widens served output and one role. Today every fresh vendor-path performance request is refused. After it, a signed-in
Cottonwood or Inflection user's fresh request calls Black Diamond or Orion with the firm's stored session credential. The
authority is Andrew-direct 2026-10-09 (`ANDREW_DIRECT_20261009_024xZ_LAW_EDIT_CLAUDE_MD_EGRESS_OPEN_EXCEPT_BBG.md`): a vendor
API other than Bloomberg needs no per-use word. Neither vendor here is Bloomberg. The radius, both branches and the rollback
per step are as the COO half states them.

## 2. What this seat read itself

- **Every hunk of `performance/authorization.py`** between the issuance and the drain (fb3bae3b99..416ead492f). The plan and
  both plan environment variables are no longer read. What stays, in the code: the firm must be a key of `firm_paths()`; the
  request must name exactly ONE account; the mapping must be a dict whose `firm_id` equals the request's firm and which
  carries a revision; the vendor requests are built by the firm's own builder from that mapping; the use record is written
  before a transport is built and a failed write refuses egress; the returned transport is still `_BoundTransport` over
  those requests. The use record is now a log (an unconditional put under a unique key), not a single-use claim.
- The diff's size outside tests: 6 files, 73 insertions, 79 deletions, all under `performance/`.
- `authorization.py:61-90` before the change (read at 07:4xZ for the ruling).

**Taken as filed:** the other five files' hunks (the transports no longer take a plan digest; not read line by line by this
seat); the issuer's AC runs and its nine live reads; the targeted plan's count; the naming limb's rc 0; both secret ARNs.

## 3. Conditions

1. The COO half's five conditions and its steps 0 to 3, as written. Policies before the zip; each count exact or STOP.
2. **No vendor call is made by the apply or by any agent to test it.** The live-call arm of step 3 is one GET as a non-49F
   caller that answers typed. If that one GET itself reaches a vendor, it is the release's one use and is stated as such in
   the close, with the use record's key.
3. The close reads APPLIED, UNEXERCISED. FWD-1 of DSGN_IRPTV1 is graded on the laptop's re-walk, asked through the managers
   after the ledger closes.
4. Three rows of the COO half stay open after this act and none holds it: a repeat request is refused
   (D2-W282-S2); one unrelated calendar test fails (D2-W282-S3), to be run on the pre-change tree so "pre-existing" is
   measured; the dead plan variables are removed in a later cell.
5. A stale vendor session is a typed refusal and a credential question for its owner, not a rollback.

-- 1.0.0_SA_CTO~DELL2
