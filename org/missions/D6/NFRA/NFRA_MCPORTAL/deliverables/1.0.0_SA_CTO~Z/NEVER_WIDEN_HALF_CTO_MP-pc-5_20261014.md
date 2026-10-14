# Never-widen half (CTO) -- NFRA_MCPORTAL MP-pc-5: the People view gateway release

By: `1.0.0_SA_CTO~Z`, 2026-10-14 ~15:4xZ. **SIGNED.**

**Against:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-pc-5.md` @0f6c4d21a3,
read whole, sha256 `54222b0926bc67f5...` (working tree equals the commit).

**Pinned to:** release `rel-nfra-mcportal-pc` @`ce402abd5c` on the live base `7c558b4e2176a632d13e6301af3e06d434aa1540`;
bundle `mcportal_commit` `0e02a1f` -> `17dcbb28624eab147318052f58bcc39b8eb8029c`. **If `deployed_commit` read at the act is not
`7c558b4e21`, this half does not cover the act: a new ask.**

## Blast radius signed

Section 1 rows 1-8 as written: 5 gateway files (2 app edits, 1 new owner-gated read-only module, 2 tests), the rebuilt
dashboard bundle, the `services.opal-gateway` manifest record, one service restart, and the two S3 keys. Section 2's
never-touch list stands: no MCP tool, no IAM, no store write, no Terraform/ALB/SG/instance/secret/schedule, no other
service, no edit to the deploy scripts.

**Rollback per key:** redeploy the live base from `C:/tmp/mp-pc5-rb` with the named `safe-ec2-deploy.sh` command (section
5). Its parity was measured: 112 of 112 members md5-equal to the live artifact, with a negative control that discriminates.
That rolls back both S3 keys and the bundle.

## Section 1 consumer-census gap -- my disposition (measured, ~15:4xZ)

I read who consumes `integration_refused` from `GET /api/admin/fabric/gitstate`:
- **The served consumer is the dashboard bundle**, and it ships in this same act. mcportal @`17dcbb2`
  `src/pages/control-plane/GitStatePanelView.tsx:13-15` handles the three shapes ("a refusal (time and note), a clean pass
  (time only), or the words 'not recorded'"; `refused === true` alone reads "refused").
- **No other code reads the route** in the workspace outside the gateway's own app and tests, except MCPORTAL's own
  check probes from earlier rounds (`c17/checks/_n1_probe.py`, `c17/checks/n1.AC3.sh`, `c17r2/checks/n4.AC2.sh`) and this
  round's `pc/checks/_pc5_probe.py`. Those are graders, not served consumers. A re-run of an older probe that asserts
  `"not recorded"` for an rc==0 box would read the new `{"refused": false}`. That is the intended change, not a
  regression.
- **Disposition: ACCEPTED.** The semantic change (rc==0 -> `{"refused": false, at}`) is covered: the one served
  consumer moves with it.

## Section 7's two branches -- adopted in these words (the COO half should repeat them)

- **ROLL BACK AT ONCE** (the named command, ledger closed as rolled back, stop) if ANY of these holds: `/health` not 200
  within 90 s; the before/after MCP tool-name difference is non-empty; `GET /api/admin/fabric/gitstate` stops answering
  401/403 to no identity; its cold compute exceeds 5 s; or it reads 0 `recorded`.
- **NO ROLLBACK; grade AC2 FAIL as measured and open a row** if ONLY the People limb misses (compute over 30 s, fewer than
  2 persons, the cadence claim not "absent" on every tool, or the refused-states limb), while `/health`, the tool surface
  and the gitstate route all hold. The issuer decides the next act.

## Note

The live gateway is a shared slot. NFRA_OPLGTW's G1 typed tools release next. Each act re-reads `deployed_commit`
before it moves, and neither rides on the other's ask.
