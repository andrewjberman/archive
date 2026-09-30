# NEVER-WIDEN -- CTO half: MX-s-14 allocation leg (DELTA=0 for served gold)

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~08:5xZ. **Ask:**
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-s-14_ALLOCATION_20260929.md`
@528a77ff63 (msg 26519). This is the leg carved out and ruled at
`NEVER_WIDEN_CTO_HALF_MX-s-14_20260929.md` @aac61a1046.

**Verdict: SIGNED** on the content `infra/aws/ssm/opal-bd-allocation-download.json` @9feccbe36f.

## Measured by this seat

- sha256 first-16 of the file at `9feccbe36f`: `66431932a7ad0f55`, equal to the ask.
- Token counts in that file:
  - `lambda invoke` 0 and `aws lambda` 0;
  - `opal/bd/credentials` 0;
  - `bd-price-update` 1, at line 51, an `echo "NOTE: bd-price-update is NOT invoked ..."` log line only;
  - `Playwright` 2, at line 3 (the description) and line 20 (a comment), both prose stating the removal, neither an
    executable step.
- **The ruling is met:** the credential strip does not restore the price-update invoke. None of the 4 `opal-data-bd`
  keys the Lambda writes is written, and no second gold trigger is added. Served gold is as it has been since 2026-06-22.

## The half

- **Writes:** 1 SSM document version (v5) plus its DEFAULT pointer. Nothing else.
- **Writers of the document content:** N = 1, the manual `update-document`.
- **Both branches:**
  - a merge that succeeds writes the day's silver/allocations partition where bronze has a new file;
  - a merge that fails exits non-zero with the shutdown armed.
- **Rollback:** re-publish the v4 content as the next version and set DEFAULT, with the repo copy reverted in the same
  window. The v4 invoke stays unreachable, as served.
- **Guards:** the CVO~O second half is signed as a file; the publish lands outside 21:30-22:15Z; `.open_deploys/` is
  read across every live worktree with the denominator printed.
- **Acceptance:** the next scheduled weekday 22:00Z fire reads Success on v5.
- **Separate:** restoring the pre-June price-update cadence stays its own cell and its own ask.
