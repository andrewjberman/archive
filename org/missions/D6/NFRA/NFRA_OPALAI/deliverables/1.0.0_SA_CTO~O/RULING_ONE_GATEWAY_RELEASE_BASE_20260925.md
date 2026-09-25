# RULING -- ONE release base for every opal-gateway deploy, and one deployer at a time

**By:** `1.0.0_SA_CTO~O`, the D6 opal_ai program CTO. The gateway is this program's product surface: NFRA_OPALAI,
NFRA_MCPORTAL and NFRA_MCPINDEX all ship into it. **Written:** 2026-09-25 ~20:0xZ.

## Andrew-direct, as relayed

Andrew-direct ~19:3xZ at the laptop `1.0.0_SA_CTO` terminal, relayed on agentbus ac79b9b8 (19:46Z) and by
`0.0.0_AB_MSTR~Z` (inbox 20260925T195425Z), verbatim as relayed:

> coordinate with ~O team CTO on this matter and bring MSTR into the hustle

**The matter:**
- The MCPORTAL MP-d-1 deploy at ~17:18Z (`rel-nfra-mcportal-r2-gateway` @c97839d7c8) crash-looped the gateway until
  ~17:31Z, and every gateway call returned 502.
- The live `app/tools.py` differs from CLOUD HEAD. A HEAD deploy would therefore overwrite the live release AND ship
  NFRA_OPLGTW commits under Andrew's 2026-09-22 stop.

**The one ask:** name the ONE base the next gateway deploy builds on.

## The rule

1. **THE BASE IS THE DEPLOYED COMMIT, NEVER CLOUD HEAD.**
   - Every opal-gateway release is cut at `EC2_MANIFEST.json`'s `deployed_commit` for opal-gateway, re-read at the
     release's own cut.
   - It adds ONLY the releasing project's own gateway commits, applied by content, on a release branch.
   - **Today that base is `f1f0fc6780`** (NFRA_OPALAI OA-t-6's narrow release, live since 02:12Z and restored by the
     17:31Z rollback: `server.py` md5 equal).
2. **The next deploy** is NFRA_MCPORTAL MP-d-1's retry: `rel-nfra-mcportal-r2-gateway-2` = `f1f0fc6780` + MP-t-1
   @98ad7e253f + MP-t-4 @17b7e01c0f + MP-g-1 @d0ba96d27c + the deploy-script fix 83cbd1a605. The defective
   @c97839d7c8 is never used again. Its CTO sign-off is
   `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/1.0.0_SA_CTO~O/RULING_MP-d-1_RELEASE_SIGNOFF_20260925.md`
   @384fd85543. After it lands, THAT release commit becomes the base, and the manifest records it.
3. **No deploy from CLOUD HEAD, by any seat, on either device,** while HEAD carries another project's unreleased
   gateway commits. Today those are:
   - NFRA_OPLGTW 9e4074c33a and 6c37cc6b00, under Andrew's stop;
   - MDPF_TAXSMA 6abf60e5d5, 8dce9aeb0b and e8f800e6a9, row MDPF_TAXSMA-S6;
   - NFRA_MCPINDEX 650c9a99cb, which releases with its own re-cut.

   Each of those projects releases its own commits narrow, on the then-deployed base, under its own issuer.
   `0.0.0_AB_MSTR~Z`'s hold on HEAD deploys stands until they are released or reverted.
4. **ONE DEPLOYER AT A TIME, ANNOUNCED.** Before touching the instance, the deploying seat announces on agentbus, or
   through `0.0.0_AB_MSTR~Z` for a seat without the bus. It names the release branch and commit, its base, and its
   ledger entry, and waits for no competing announcement. For the three opal_ai projects the deployer is
   `2.0.0_SA_COO~O`, one release at a time.
5. **Every release carries the three guards learned today:**
   - the `.env` render check with distinct markers BEFORE the act;
   - an automatic rollback if `/health` is not 200 within 90 seconds;
   - a post-act read that the MCP tool list equals the pre-act list.

## Why this base, and not another

The deployed commit is the only one whose bytes are proven running and proven restorable. Both were proven today.
HEAD is a union of four projects' work, and at least one of them is under a stop. A base that is "whatever HEAD is"
is how the outage's second-order risk arises: a correct fix shipped on top of someone else's unreviewed change.
