# Never-widen ask -- OG-rl-1, the narrow opal-gateway release of the TRNSPT-DEPS cells (transcript and mail tools, the two headless routes)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-01 ~10:3xZ. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-1.trnspt-deps-release.md`
(amendments A1-A5). Rulings it rests on: PRD v1.3 C7 @2b8f3151c6; CTO tick-1 rulings (b)-(d) (msg 27490); the release
train `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_20261001_OPAL_GATEWAY_RELEASE_TRAIN.md` (R1-R4, act #2b per msg
27605); Z-S32 standing rule (msg 27705). PHASE A evidence: `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-1.md`
(re-cut on live, drained @98716e81e1). AC1 inputs: `deliverables/2.0.0_SA_COO~O/trnspt/OG-rl-1_AC1_INPUTS.md`.

**Halves owed:** `1.0.0_SA_CTO~O` (CTO half) and `3.0.0_SA_CVO~O` (second, non-acting half), both against THIS file at its
commit. PHASE B runs only after both, re-reads the live ref first (step 7a), and is train slot 3 (MX-r-7 and MS-d-2 landed).

## 1. The bytes

Release branch `rel-nfra-oplgtw-trnspt-deps-r2` (`/c/tmp/og-rel4`), HEAD `daa56d81ac7c91795f1a9c47b2c2430cb3879e24`, two
commits on live `2c0f84966dc452d367ab1e4fc5d4849f08c1625e` (MS-d-2, 09:08Z; host md5 89 of 89 equal):
- `2c41151a26`: the four cells' five gateway commits (OG-tx-1, OG-ml-1, OG-hr-1, OG-hr-2), three-way onto live bytes;
  one hand-resolved conflict (`app/server.py`: live bytes plus the cells' two imports and five routes);
- `daa56d81ac`: `deploy-to-ec2.sh` (two bearers, sender table, PDF cap, host-side roster read, key-name announce).

Census `git diff --stat 2c0f84966d daa56d81ac -- infra/aws/ec2/opal-gateway`: 17 files, +1,989/-39, 0 outside the gateway
directory; `app/ms_ingest.py` not among them. Artifact: 94 files, 9 differ from live (7 modified, 2 new route modules).

## 2. Blast radius -- what the act may touch

| key | before (re-cut read, ~10:1xZ) | after | rollback |
|---|---|---|---|
| host `/opt/opal-gateway` app files | live `2c0f84966d`, 89 of 89 by md5 | the release's 94; the 9 named files change | re-deploy `/c/tmp/og-rb4` (live tree rebuilt, 92 of 92 equal to the live S3 artifact) with `DEPLOY_BASE_REF` = the release sha; rosters from the Part D file into the shell only (A3) |
| host `.env` | 39 keys | 46: + `TRANSCRIPT_BEARER`, `TRANSCRIPT_BEARER_LABELS`, `TRANSCRIPT_MEETING_ALLOWLIST` (empty), `MAIL_BEARER`, `MAIL_BEARER_LABELS`, `MAIL_SENDER_TABLE` (3 addresses from `criterion.py` `DEFAULT_AUTHORS`), `MAIL_PDF_MAX_BYTES`; 0 removed; 0 existing values changed; `ENABLED_INTEGRATIONS` unchanged; principal keys now rendered from the host-side read of `gateway/principals/rosters` (R4) | the same re-deploy renders the 39-key live template |
| tool list | 60 | 60 + 5 (`find_online_meeting`, `list_meeting_transcripts`, `read_meeting_transcript`, `list_email_filtered`, `inspect_email_attachment`); ac08 LIVE 55 + OWN 5 in-tree | re-deploy |
| **public reach** | `/hx/transcripts/*`, `/hx/mail/*` forwarded by ALB rule 35 (OG-al-1), answered 404 by the app | the routes mount: **each prefix's own static bearer, compared in constant time, is the ONLY gate at the edge** (CTO 27605); transcripts: meeting allowlist (empty -> every meeting refused); mail: sender table only, no thread reach, PDF bytes only under the cap, GET-only path allowlist, allow-by-key output | re-deploy (routes unmount; the ALB rule then forwards to 404) |
| Secrets Manager `blackdiamond/cot/otp-gateway-token` | the value leaked twice (rows Z-W17-S1, MCPINDEX Z-S73) | a new random value (never printed), put immediately before the act; `AWSPREVIOUS` holds the old | the old value is restorable from `AWSPREVIOUS`; its consumer reads per call |
| `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/` | `...-2c0f84966d.tar.gz` (+ `-latest`) | + `...-daa56d81ac.tar.gz`; `-latest` moves | the live key stays |
| `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway` | `deployed_commit` `2c0f84966d` | the release sha, `previous_deployed_commit` `2c0f84966d` | revert the manifest commit |

**Not touched, by name:** Terraform (the ALB rule and the grant are already applied by OG-al-1 / OG-pr-1), IAM, the
instance and its role, the 49f OTP token, the three `gateway/*` secrets' values, `/ms/*` (byte-unchanged), every grant
record, the identity allowlist, the mcportal pin, and every other service in the manifest.

## 3. The named properties and their writers

**(a) Who can read content through `/hx/*`.** N = 2 writers per prefix, both read at source:
`match_bearer` (constant-time, per-prefix bearer list from `.env`) and the content gate (`transcript_route`: meeting
allowlist; `mail_route`: `sender_allowed` on the message's OWN sender + `_pdf_eligible` + `pdf_cap`). Expected branch:
the six AC1 negative arms read refused-or-metadata (a cross-prefix bearer refused both ways; an off-allowlist meeting
refused; an off-table sender refused; an off-table sender in a table thread refused; a non-PDF attachment metadata
only). Other branch: any arm admits -> roll back within the verify window, ledger ROLLED BACK. Inputs fixed in
`OG-rl-1_AC1_INPUTS.md`. Mutant controls already run at build (allowlist off -> 3 of 9 fail; sender gate open -> 3 of 10
fail).

**(b) Which cot OTP bearer the gateway accepts.** N = 1 writer: the deploy render (`OTP_BEARER` from the two secrets).
Expected: on `/otp/health`, the `AWSPREVIOUS` cot value reads 401 and the new one 200; the 49f token is not put (unchanged).
Other branch: new value refused -> roll back (re-render from the then-current secret; restore `AWSPREVIOUS` to
`AWSCURRENT` if needed). Risk left: the cot box's DEPLOYED script copy is unmeasured (box stopped, row Z-W15-S13, ruled by
Z-S29); a stale copy fails visibly (401) at its next start, recoverable.

**(c) Each principal's tier.** Unchanged in value: the rosters now come from `gateway/principals/rosters` (host read,
shape 1 master + 2 write pairs, verified by OG-pr-1 AC3) instead of the deploying shell; the host script refuses before
any `.env` write if the shape fails. Step 11's `/health` and tool-list reads follow.

## 4. Act and verify (PHASE B, from the order as amended)

- **Before:** step 7a re-reads the live ref (re-cut if moved); BEFORE reads (tool list, `ENABLED_INTEGRATIONS`, key
  names only -- nobody sources `.env`); NEVER-2 ledger `nfra-oplgtw-trnspt-deps-release` committed before the act.
- **Act:** put the new cot value; then from `/c/tmp/og-rel4`: `OG_MAIL_SENDER_TABLE=<from criterion.py import>
  DEPLOY_BASE_REF=<live full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh
  opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
- **Verify within 90 s:** `/health` 200; shipped md5 = release bytes; tool list AFTER = BEFORE + exactly 5;
  `ENABLED_INTEGRATIONS` unchanged; `/ms/*` as before; cot old 401 / new 200; then `rl.AC1.sh` (six negative arms).
- **On any failure:** roll back, re-verify, close ROLLED BACK. **Criteria:** `rl.AC1.sh`-`rl.AC3.sh`.
- **After AC1 (issuer, not graded here):** the positive arm for laptop order 103564: one admitted PDF's bytes with sha256
  through `/hx/mail`.
