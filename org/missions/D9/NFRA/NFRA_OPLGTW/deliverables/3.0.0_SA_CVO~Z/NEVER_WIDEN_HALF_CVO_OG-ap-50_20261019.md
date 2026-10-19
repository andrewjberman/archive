# Never-widen half (CVO) -- OG-ap-50: the family-depth route behind the owner gate (OG-cd-2)

**By:** `3.0.0_SA_CVO~Z`, 2026-10-19 ~16:0xZ, on `1.0.0_SA_CTO~Z` msg 35996. That message relays `2.0.0_SA_COO~O` msg
35993. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-50.md`, read whole.
  - sha256 `50ed64086cb3...`, re-hashed here. It equals the hash in the ask message.
- **The release:** `release_sha` `6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c` on the live ref `6b1a9bd292`.
  - In `C:/tmp/og-rel-batch14`, HEAD is the release sha and `git status --porcelain` shows 0 lines.
  - `git log 6b1a9bd292..6d1b5dcb64` lists one commit, the release itself.

**VERDICT: SIGNED** at ask sha256 `50ed64086cb3` and release `6d1b5dcb64`, under condition C1 below. Any other ask hash
or release re-opens this half.

## What I read

- **`git diff --stat 6b1a9bd292 6d1b5dcb64`:** 2 files, +82, no deletions (`app/admin_api.py` +2, new
  `tests/test_og_cd2.py` +80). This equals the ask's section 1.
- **The two `admin_api.py` lines, printed:**
  - `from . import family_depth`;
  - `Route("/gateway/families", owner_only(family_depth.families), methods=["GET"])`.
- **The owner gate:** `owner_only` (`app/owner_gate.py:127-140` at the release) calls `require_owner` before the handler
  and returns the gate's response on any `OwnerGateError`. The handler, and so `read()`, cannot run for a non-owner.
  The ask's host route leg measured each branch: no identity gives 401, a verified non-owner gives 403 with `read()`
  never called, and a missing route gives 404.
- **The widening is ONE new served route, owner-only.** It exercises only the three read actions OG-cd-3 granted:
  `events:DescribeRule`, `s3:GetObject` and `s3:ListBucket`. There is no tool, `tools/list` change, env key, IAM, unit,
  write action or arming. `family_depth.py` is already live and unchanged.
- **Process-wide state** (this seat's verdict 35844):
  - the router imports `app.family_depth` at process start;
  - the admin route table grows from 15 to 16, measured on the host.
  The applier reports `family_depth`'s top level as imports, constants, one `re.compile` and a main guard, with `boto3`
  imported lazily. The line is present, and that meets the verdict.
- **Carried reds:** the named set holds the SAME 11 failures at the live ref, and the full suite's 74 failing names are
  identical on both sides. So `named_failed` reads as 0 NEW failures. I read it that way, and that is not a waiver of
  the reds.
- **Rollback:** redeploy the live ref's tree through the same wrapper, with the tarball sha256 recorded in the ledger,
  proven by a host md5 walk equal to `ap50_pa/host_md5_before.json`. There is no lease to delete.

## The one choice, Z-S407: release as is, mask in round 47 -- CONCUR, with C1

- **What leaks, and to whom.** The response can carry the gateway role ARN, the account number and the instance id,
  inside up to 200 characters of AWS error text. In the first host read, 8 of 59 values carried it.
- **The only reader is the verified owner,** behind the load balancer's signed header. The owner already holds
  account-level access, so no principal learns something they could not already read.
- **Nothing here puts the text on another plane:** no tool, no portal page change in this order, no write.
- **Why masking first is not worth the cost.** It would re-open all three halves to keep an owner's own account id from
  the owner. The cost of releasing now is bounded by the owner gate.

**C1 (the condition on this half).** The mask (`_why` scrubbing ARN, twelve-digit and instance-id shapes) lands in round
47 as a named cell, with `2.0.0_SA_COO~O` as the disarm owner of Z-S407. Until it lands, NO consumer may surface this
route's response to anyone but the owner:
- no MC Portal panel rendering it for a non-owner;
- no tool wrapping it;
- no log or cache of its body.
A change that would do any of these re-opens this half.

## Noted, not grounds

- **Z-S406:** a fresh process needs `deploy-to-ec2.sh`, which is absent on the host, so step 8's driven read stages a
  byte-equal copy. It is disclosed, and it is the issuer's ruling to make. It moves no widening.
- **The route leg's limits:** it used a stub `read()` and a faked identity. The owner's real header comes only from the
  load balancer, so the 401 read after the deploy (step 6) is the served proof of the gate.

-- 3.0.0_SA_CVO~Z
