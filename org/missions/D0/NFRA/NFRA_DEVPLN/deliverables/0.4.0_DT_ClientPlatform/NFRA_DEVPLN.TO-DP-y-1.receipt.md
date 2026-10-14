# Receipt: NFRA_DEVPLN.TO-DP-y-1 -- client-facing chosen-set promote of five dell2 features (0.4.0_DT_ClientPlatform, 2026-10-14)

**Shipped:** five client-facing features, all dell2 branches, all approved by Andrew (his word of 2026-10-14 ~11:4xZ), to portal PROD.
PROD `7db035e4` -> `501e998b1e576252ba493bd5427e14fba748dcef` (origin ls-remote read at push). Release branch `release/20261014T122041Z`, taken onto PROD by `--ff-only`; parity diff against the release branch = 0 lines. `origin/DEV` was never merged into PROD.

**Later PROD movement (not this promote):** `6a5926fc` (dell1 `cand/dell1/amgt-sa-pe-basis-and-reasons`, Approved-By 1.0.0_SA_CTO~DELL1 @dell1-20261014T111220Z-faa4, tag portal-v2.1.219) landed on PROD after 501e998b. PROD is now `6a5926fc`. See surprise row `NFRA_DEVPLN-S6`.

**CI:** run 38563449756 "Deploy to Production" on sha 501e998b, status completed, conclusion success (jobs Build Production Assets, Deploy to S3 + CloudFront, Tag Deployment all success); the only workflow on that sha (`gh run list --commit`). Tag `portal-v2.1.218` peels to `501e998b`.

**Precondition (step 1):** DEV carried both merges (`Feature:` trailer count 1 for `irpt-ytd-from-first-day-and-wider-export-modal`, 1 for `partner-firm-stack`; DEV was `22795405`). `open-calls.py approval-status` printed `state=APPROVED valid=yes` for all five at the table's heads.

**Builder lines (verbatim):**
```
RELEASE-CHECK features=5 first_parent_commits=5 unapproved=0 ref=refs/heads/release/20261014T122041Z sha=501e998b1e57
PROMOTE-LIST branch=cand/dell2/anlreq-90-held-submit class=client-facing by=andrew row=dell2-20261013T222707Z-8500 pages=src/pages/TicketCenter (AnalysisRequestParts,TicketCenter,analysisRequest)
PROMOTE-LIST branch=cand/dell2/anlreq-88-advisory-fee class=client-facing by=andrew row=dell2-20261013T222709Z-7b45 pages=src/pages/TicketCenter (AnalysisRequestParts,analysisRequest)
PROMOTE-LIST branch=cand/dell2/anlreq-87-model-order class=client-facing by=andrew row=dell2-20261013T222710Z-fde0 pages=src/pages/TicketCenter (AnalysisRequestParts)
PROMOTE-LIST branch=cand/dell2/irpt-ytd-from-first-day-and-wider-export-modal class=client-facing by=andrew row=dell2-20261013T221411Z-3635 pages=Investor Reporting performance picker and body,Investor Reporting export modal
PROMOTE-LIST branch=cand/dell2/partner-firm-stack class=client-facing by=andrew row=dell2-20261013T231910Z-7773 pages=Ticket Center,Analysis Request form,Ticket board
PROMOTE-CLIENT-FACING count=5
RELEASE result=READY reason=- branch=release/20261014T122041Z base=7db035e448d9e6bbc202ef4264989f54d3d3dded head=501e998b1e576252ba493bd5427e14fba748dcef
```
Push gates: VALGATE D-1 PASS (no-op), pre-push `tsc -b --noEmit` passed.

**Measurements after the push (step 4), read at 12:5xZ with origin/PROD = 6a5926fc and origin/DEV = 97c66c93:**
- `git -C portal rev-list --count origin/PROD..origin/DEV` = 7. All seven are DEV-side merges carrying "(approved feature)": `97c66c93` (dell1 amgt-sa-pe-basis-and-reasons, DEV's own merge of what PROD holds as 6a5926fc), `22795405` and `2deb4f1d` (the integrator's DEV merges of the two dell2 features PROD holds as 501e998b and 87e55658), `ab8ecc56`, `514df1bb`, `5e40e541` (three dell1 approved features not on this promote's list), `24877b67` (DEV's merge of contributing-boxes that PROD holds as 10e7664d).
- `git -C portal rev-list --count origin/DEV..origin/PROD` = 6 (`6a5926fc`, `501e998b`, `87e55658`, `690caad5`, `3e662b27`, `22bd0695`: the five release merges of this promote plus the dell1 release merge).
- `git -C portal log --first-parent --format='%h %s' 7db035e4..origin/PROD`:
```
6a5926fc merge feature cand/dell1/amgt-sa-pe-basis-and-reasons into release/20261014T123810Z
501e998b merge feature cand/dell2/partner-firm-stack into release/20261014T122041Z
87e55658 merge feature cand/dell2/irpt-ytd-from-first-day-and-wider-export-modal into release/20261014T122041Z
690caad5 merge feature cand/dell2/anlreq-87-model-order into release/20261014T122041Z
3e662b27 merge feature cand/dell2/anlreq-88-advisory-fee into release/20261014T122041Z
22bd0695 merge feature cand/dell2/anlreq-90-held-submit into release/20261014T122041Z
```
- `bash .tools/portal-release-build.sh --check PROD --repo portal --prod-ref 63c4f9e3...` -> `RELEASE-CHECK features=10 first_parent_commits=10 unapproved=0 ref=refs/remotes/origin/PROD sha=6a5926fc1194`.
- Same check on this promote's own head (`--check release/20261014T122041Z`) -> `RELEASE-CHECK features=9 first_parent_commits=9 unapproved=0 ref=refs/heads/release/20261014T122041Z sha=501e998b1e57`.
The trunks differ by the approved set only; the one deviation is the count in DPy1-AC1 (10 at the live tip, 9 at this promote's head), filed as `NFRA_DEVPLN-S6`.

**Acceptance:** DPy1-AC1 as first issued expected `features=9`; it read `features=10` at the live tip (see `NFRA_DEVPLN-S6`). The issuer amended it at `e4f3acfcc8` to `unapproved=0 ref=refs/remotes/origin/PROD`, and the re-run reads `RELEASE-CHECK features=10 first_parent_commits=10 unapproved=0 ref=refs/remotes/origin/PROD sha=6a5926fc1194`: PASS. DPy1-AC2 = 5, PASS. Instance VALID (rc=0).

**Ledger:** `devpln-r8-client-facing-chosen-set-promote-20261014` opened at start, legs L1 (PROD commit), L2 (CI), L3 (tag) proven, CLOSED.
**Teardown:** worktree deregistered (`worktree prune`); the directory `.runtmp/portal-promote-20261014T122112Z` persists on the Windows long-path error, gitignored and inert. Main portal tree on DEV, fast-forwarded to `97c66c93`. The local `release/20261014T122041Z` ref is kept (contained in origin/PROD).
