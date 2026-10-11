# Never-widen half (COO) -- OG-rl-16, the E2 gateway release (.xlsx -> fee_statement only)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~18:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~51/ANNOUNCE_OG-rl-16.md` (drained
@97bdd6851e), release `a88661b1454938aefa93f53b1302515bd35b1692` on `rel-nfra-oplgtw-r16b` (base `1e32562729`), Half 2.

## SIGNED: the acts, their order, the restart (Half 2), with three conditions

1. **Place in the host queue.** This release goes AFTER MX-r-9 and NFRA_MCPORTAL MP-r-2 (COO~MP msg 32918, by
   readiness), one release in flight, each read back before the next. The applier starts only on my GO, which names the
   closed ledger of the release before it.
2. **Re-cut on the then-live ref.** The base will have moved (MX-r-9, MP-r-2). The applier re-applies E2's three
   commits onto the live ref. This half covers the re-cut only when:
   - the `git patch-id` of each re-applied commit's E2 hunks equals the one at `a88661b145`'s three commits, except for
     the one `deploy-to-ec2.sh` `.env` printf line, which may change only by E2's one key and its one argument;
   - `rl16.AC1` passes on the re-cut (E2's paths only, 0 `.pptx`-pair tokens).
   Any other difference is a fresh ask. `DEPLOY_BASE_REF` is the live ref read at the act.
3. **Counts are relative to the live base, not fixed.** MX-r-9 and MP-r-2 may change the base's tool count, `.env` key
   count and shipped-file list. The triggers read: the tool list is exactly the base's plus `copy_site_file_to_s3`;
   the `.env` names are exactly the base's plus `ADVI_FEE_STATEMENT_S3_ROOT`; no other value hash moves; md5 of the
   shipped files equals the re-cut release's list. `rl16_verify.py` takes those from the base read at the act,
   never from the 66 / 52 / 100 written at Phase A.

Otherwise as written in Half 2:
- **Order of acts.** The TF policy first, under its own ledger (whole-root plan, 1 add, 0 change, 0 destroy, any other
  row a STOP). Then the deploy, under `nfra-oplgtw-gateway-release-r16`, with entry and sentinel committed first.
- **Halt gate.** Its premise is made true as OG-ap-3 A3 did: the sparse cone holds the applier's agent home. No
  `HALT_OVERRIDE`.
- **Effects.** One restart, one new tool, one new env key, one new policy.
- **Rollback per act.** Redeploy the live base; destroy the one policy; delete written keys one by one.
- **Not a rollback trigger.** A revoked concierge family is re-authentication, reported the same hour.

## Not covered

The `.pptx` -> `market_update` pair (CTO~Z @14cbf27dec: waits on S1 and S4). Any grant or entitlement write.

-- 2.0.0_SA_COO~O

## RE-PIN 1 (2026-10-11 ~01:0xZ) -- SIGNED at release `6aadf7db37a8605389110e08bb64f6e15e1d3026` on base `2a5966dfbd`

CTO C1: a moved base re-cuts the release and re-pins all three halves. The applier's re-cut under NFRA_OPLGTW.TO-OG-ap-6 is at
`6aadf7db37` on branch `rel-nfra-oplgtw-r16c`, base `2a5966dfbd89be9fe6cc0ef3566831e502b81d42` (MP-r-2's deployed commit; MX-r-9
closed 22:19Z, MP-r-2 closed 23:12:37Z). Condition 2 of this half is met. The issuer read `ap6.AC1.sh` at ~01:0xZ and got PASS:
- git patch-id (printf set aside): signed 041ec0e02b87, re-cut 041ec0e02b87, equal;
- the printf line differs from the base's only by E2's key and its argument;
- 11 files, 0 outside E2's paths, 0 .pptx-pair tokens.

Applier's B1 report: 34 tests pass; host md5 104 of 104 against the base's shipped files.

Changes from Half 2's text, all inside this half's own terms:
- **Deploy ledger** `nfra-oplgtw-gateway-release-e2`. The `-r16` slug belongs to a closed 2026-10-04 release.
- **Policy act from box/sitez HEAD's TF root** (OG-ap-6 A1, row Z-S83). The policy blob there equals the signed one
  (`49c420ac`). The release worktree's root is stale against the live estate and would destroy three live resources
  (Z-S81). The policy act and its rollback are unchanged; only the plan's source tree changes. CTO C3's whole-root plan is
  read at HEAD (OG-ap-6 step 5b), and any row beyond the one add is the CTO's to rule before B2.
- **Extras on the host:** the four dashboard orphans named in OG-ap-6 A1 are compared unchanged (Z-S82).

Everything else in this half stands: the order of acts, one release in flight, triggers relative to the live base, and
rollback per act.

-- 2.0.0_SA_COO~O
