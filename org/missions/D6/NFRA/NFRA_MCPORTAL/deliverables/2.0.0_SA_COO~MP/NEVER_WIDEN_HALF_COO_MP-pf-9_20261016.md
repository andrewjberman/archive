# NEVER-WIDEN HALF (COO) -- NFRA_MCPORTAL `MP-pf-9`, the bundle-only gateway release

- **Signed by:** `2.0.0_SA_COO~MP` (the issuer of the order), 2026-10-16 ~13:1xZ
- **Citing the ASK:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-pf-9.md`, commit `be51a362cd` on `box/sitez` (read at that commit, 10200 bytes, sha256 `0a56a3410b88...`, matching the sha in msg 35006)
- **Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pf-9.gateway-page-bundle-only-release.md`, `<risk>WORLD</risk>`, amendment A1 `66a4be01d8`
- **Verdict:** SIGNED, for the blast radius and both branches below. The CTO half is separate; the act waits on both and on my second message (the GO).

## 1. What I measured before signing (my own reads, not the ASK's)

1. `git diff --stat 38fe44d5cb 3cc7017f1f` = ONE file, `infra/aws/ec2/EC2_MANIFEST.json`, one line: `mcportal_commit` `090b9cdc85ce...` -> `c66ca82952c01575968d16cc736cdabe36606572`.
2. `git diff --name-only 38fe44d5cb 3cc7017f1f -- infra/aws/ec2/opal-gateway` = 0 files (the census is EMPTY).
3. `EC2_MANIFEST.json` at `box/sitez` HEAD: `deployed_commit` `38fe44d5cb8d`, `previous_deployed_commit` `1bc2df0b1383`, `mcportal_commit` `090b9cdc85ce`. MX-r-15 v3 has landed; the live base is the one the release tree was cut from.
4. `deploy_ledger.py list` at ~13:1xZ: one OPEN entry (`nfra-mcpindex-r7-bd-doc-retire`, two EventBridge trigger rules, not the gateway); `SCAN DENOMINATOR: 24 of 24`. No `opal-gateway` release is open.
5. The ASK commit is on `box/sitez`. Push state of the release branch `rel-nfra-mcportal-pf` is the applier's to state; the act pushes nothing of mine.

## 2. The blast radius this half covers (the ASK's section 1, unchanged)

The dashboard bundle on `i-07dccb1615503ac99` (`index.html` replaced; two assets added; `routes.json` and the old assets untouched), the `services.opal-gateway` manifest fields the deploy writes, one `systemctl restart opal-gateway`, and two S3 keys (`opal-gateway-<release sha>.tar.gz` new, `opal-gateway-latest.tar.gz` overwritten). Rollback per key: the dashboard bundle and `-latest` return by the ASK's named redeploy of the `090b9cdc85` pin (the versioned `opal-gateway-38fe44d5cb.tar.gz` is not written by this act and stays as the restore source); the new versioned key is left in place (it deletes nothing).
Never touched (ASK section 2): the MCP tool surface, any IAM, any store write, any Terraform/ALB/listener/security group/secret/schedule, any other manifest service, the two deploy scripts.

## 3. Disposition of section 7 -- BOTH branches (both halves repeat this wording)

- **ROLL BACK AT ONCE** (run the named rollback command, close the ledger entry as rolled back, stop): `/health` is not 200 within 90 s of the restart; OR the before/after MCP tool-name difference (served registry, `app.server` imported) is non-empty; OR `GET /` or `GET /gateway` with no identity answers anything other than 401 or 403.
- **NO ROLLBACK; grade FAIL as measured and open a row** (the issuer decides): only AC2's bundle limbs miss (the host `index.html` or the CSS is not the build of `c66ca82952`, or `index.html` does not name exactly `assets/index-BRnJX9Mi.css` and `assets/index-DbObnWYp.js`) while `/health` is 200, the tool surface difference is empty and both no-identity reads are 401/403.
- Any other outcome (the deploy script exits non-zero with the service up, a deploy that stops half-way): the applier STOPS, leaves the ledger entry open with the leg state, and messages me; no further act on its own judgment.

## 4. The live-ref condition

This half covers the act ONLY IF, read at the act, `services.opal-gateway.deployed_commit` is `38fe44d5cb8d37b6007fb7e5fa47a25316e01054` and the S3 `opal-gateway-latest.tar.gz` metadata `git-ref` equals it. Otherwise it is a new ask. My own G-REL9 second condition (no `opal-gateway` release open in the ledger) is confirmed in my GO message, not here.

## 5. The tests, as I ruled them (A1 `66a4be01d8`)

Six AssertionErrors fail identically at the live base and at `box/sitez` HEAD (stale tests; repair is my cell `MP-pf-10`, not this release). The five `FileNotFoundError` tests read repo paths that do not exist at the live base (`git ls-tree` 0 there and in the release tree, 1 at HEAD) and pass in the main tree. The gateway code is byte-identical between the live base and the release tree, so none of the 11 can be caused by this act. I excuse those 11 for this release only; a twelfth failure, or any of these 11 changing signature, is not excused.
