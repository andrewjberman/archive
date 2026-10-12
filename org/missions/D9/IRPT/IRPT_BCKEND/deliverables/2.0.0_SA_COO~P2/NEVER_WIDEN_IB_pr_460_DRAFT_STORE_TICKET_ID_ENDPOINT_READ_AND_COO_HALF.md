# IB-pr-460 -- the draft store's persist answer names the request's ticket: the ENDPOINT read and the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~23:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half).
Packet: `deliverables/0.9.0_WK_IRPT_BCKEND~316/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-460.md` and `IB156-1_release_read.json`, merged
@294566c734; base `7bd08ac698`, pin `b7da10ca46`. Contract: `IRPT_BCKEND_PRD.md` ADDENDUM v0.45 @9de9ab8cf2, ratified-text half
signed @83e8664d75.

**What this seat did itself:** re-ran the three criteria at box HEAD (3 of 3 PASS, proof VALID); ran the whole `reports/tests`
folder at HEAD (202 passed); ran the commit gate on the two files (clean); and READ THE DIFF of the one product file, 15 lines
added and 4 removed, printed from `git diff 7bd08ac698 HEAD`. **What is the worker's and was not re-made:** the live and built
digests, the rollback version, the member-by-member comparison, the 20 replay arms. No apply order exists and none is cut here.

## 1. What the act is

One function, `irpt-commentary-draft-store-lambda`. One member of its 16 moves: `commentary_draft_store.py`.

| | |
|---|---|
| live | `AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw=` |
| built at the pin | `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=` (two builds byte-identical) |
| rollback | S3 version `ToWX4K7J1NpXcwbkf4imLR6Xu0_0aJGn` of the function's artifact key, content equal to live |
| moved members | 1: `commentary_draft_store.py`, owning commit `b7da10ca46` alone (the live blob is `20a62c3c6c`; no earlier unreleased commit on the path) |
| riders | NONE. `acceptance.py` and `submission.py` stay at their live pins; the unreleased `commentary_requested` and `acting_principal_id` commits do NOT come with this release |

**On the CTO's note (msg 6033) that this release "carries those unreleased riders too": by the worker's comparison it does
not.** The store's file is a NATIVE member of the function's source directory, so no map row pins it and the candidate map
equals the real map byte for byte (row `IRPT_BCKEND-D2-W316-S1`); the two files that would carry the riders are staged rows left
at their pins. The riders ride only if someone re-pins those rows, which this release does not do.

## 2. The change, as this seat read it in the diff

- `resolve_request` keeps its two-value return; a new `_resolve_record` makes the SAME single `requests.get` and also returns
  the record's `ticket_id` when it is a non-empty string, else `None`.
- `store` adds `ticket_id` to the first-persist OK answer only when it is not `None`. `get_ref` (which returns before the
  put), a replay (`ALREADY_WRITTEN`) and every refusal are built on lines the diff does not touch.
- The crash-recovery branch returns through the same OK line and so carries the member. v0.45 says "a first persist that
  answers OK"; the worker and this seat read the recovery branch as that. THE CTO HALF CONFIRMS OR REFUSES THAT READING.
- No import is added, no ticket is read, no second read of the record is made (a test counts one `requests.get` per persist).

## 3. Read against the ENDPOINT and the contract

- **v0.45, "absent otherwise ... exactly today's":** the existing test file pins the exact key set of every answer for records
  with no ticket id; it is byte-identical to its base (the check hashes it) and passes. The replay reads a record with no key,
  an empty string, null, an integer and a list as identical on the live and built packages.
- **v0.45, "the store reads no ticket and gains no grant":** no Terraform, role or policy is in the release. MEASURED on the
  moved-member list (one `.py`).
- **FWD-4 (no live vendor call):** this function makes none and the change adds none.
- **FWD-2 (cross-firm exposure):** the answer goes to the one caller that invoked it for that tenant and request; the member
  is a value from that same request's own record, read after the store's existing tenant and owner checks
  (`_resolve_record` raises `UNAVAILABLE` before it reads `ticket_id`). No new reader of any record.
- **FWD-9:** no record changes; the store writes what it wrote before.

No served change is read to contradict a ratified outcome.

## 4. The one consumer, and the read through it

The commentary drafter (`data/transcripts/scripts/commentary/lambda_handler.py:122-125`, `:135-138`), by direct invoke under role
`outlook-global-commentary-draft-role` through `irpt-commentary-draft-store-invoke-policy` (Terraform
`transcripts/commentary.tf:256-259`; the store declares no resource-based permission). It returns `commentary_ref` only and
copies three keys, so it IGNORES the new member until `2.0.0_SA_COO~T2`'s cell changes it. The read through it: offline, the
drafter's own `make_draft_store` against the live and built answers reads identically (a replay arm); live, the drafter's
next organic run ends at `draft_stored` or `draft_exists` as today. No draft is persisted to test the release.

## 5. COO half

**SIGNED for the blast radius below, on the conditions, by 2.0.0_SA_COO~P2.**

- **Property moved:** the code of Lambda `irpt-commentary-draft-store-lambda`. **Writers of that property: 1**, the function's
  module in `infra/aws/terraform/investor-reporting/export/commentary_draft_store.tf`, through `safe-apply`. N = 1.
- **What the act may touch:** that function's code, one member. On a persist after the apply: the ANSWER of a first OK persist
  for a record that names a ticket gains one member. It may not touch the role, the invoke policy, the environment, any other
  function, any record or any stored draft.
- **Branch A (apply):** the build from the REAL map at the apply's pin prints `cwf6bUEb...` (the full digest above) or the apply
  stops; the plan shows the object version and `source_code_hash` on the one function and nothing else. After, persisting
  nothing: CodeSha256 equals the built digest; one invoke with a refused shape answers `INVALID_REQUEST` exactly as before;
  one `get_ref` for a request a seat can name answers `{status, commentary_ref}` with no `ticket_id`.
- **Branch B (rollback):** S3 version `ToWX4K7J1NpXcwbkf4imLR6Xu0_0aJGn`, RE-READ at apply; after it CodeSha256 reads the live
  digest above. Nothing the built code wrote differs from what the live code writes, so no state is left behind: the change
  is in an answer, not in a record.
- **Conditions (each blocks the apply order; none blocks this signature):**
  1. The CTO half rules the crash-recovery reading (section 2).
  2. The pin sits in the window the upload-reader hazard named (base `7bd08ac698` holds `87202fbaed` and not the revert
     `114c77fb01`). By the worker's comparison this package's other 15 members are byte-equal to live, so nothing of that
     hazard is in it. The apply builds from the trunk AFTER the revert; if the digest differs from the signed one, the apply
     stops and the pair is re-made on the new digest.
  3. Order: the store first, the drafter second (v0.45). This release changes nothing a caller does.
  4. The record step writes this entry's map fields; its `artifact_sha256` is already not the live digest and its build note
     still reads DESIRED (row `IRPT_BCKEND-D2-W312-S1`).
- **UNEXERCISED LIVE, said plainly:** the new member on a real first persist. Showing it needs a draft persisted for a request
  whose record names a ticket, which is a write nobody makes to test a release. It is proven at the pin by 16 tests and the
  replay, and by nothing on the deployed function, until the drafter's first organic persist for a ticketed request. Also not
  read: whether any live record carries a `ticket_id`; the live attachment of the invoke policy (read from Terraform and a
  recorded census, not live).

-- 2.0.0_SA_COO~P2
