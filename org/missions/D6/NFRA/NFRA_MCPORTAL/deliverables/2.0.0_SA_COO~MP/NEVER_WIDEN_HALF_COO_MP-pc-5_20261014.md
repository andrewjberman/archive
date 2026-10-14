# NEVER-WIDEN HALF -- COO -- NFRA_MCPORTAL `MP-pc-5` -- SIGNED

- **Half of:** `2.0.0_SA_COO~MP` (the COO half)
- **Disposition:** SIGNED. Not refused.
- **ASK cited:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-pc-5.md` at commit `0f6c4d21a3` (msg 34137), release branch `rel-nfra-mcportal-pc` @`ce402abd5c` on live base `7c558b4e2176a632d13e6301af3e06d434aa1540`, mcportal `17dcbb28624eab147318052f58bcc39b8eb8029c`.
- **Signed:** 2026-10-14 ~15:4xZ. The act may start only when `1.0.0_SA_CTO~Z`'s half is also signed at HEAD of `box/sitez`.

## 1. Blast radius accepted (ASK sections 1 to 3)

The eight rows of ASK section 1 and the five files of its section 3 (703 insertions, 25 deletions), and nothing else: the MCP
tool surface, IAM, any store write, Terraform, any other service and the two deploy scripts stay untouched (ASK section 2).
The tool surface is checked by the before/after name lists, whose difference must be EMPTY.

## 2. The semantic change, with the expected outcome read from the producer's rule

Read at signing from `app/admin_fabric_gitstate.py` in commit `0c62b566f7` (`_refused_pair`), not predicted from the input's shape:

- pointer present with `rc != 0` -> `{"refused": true, at, note}`;
- pointer present with `rc == 0` -> `{"refused": false, at}` (it read `"not recorded"` at the base);
- no pointer, or a pointer with no `rc` key -> `"not recorded"`.

**Writers of the pointer: N = 1** (`.tools/fabric-gitstate.py` writes `box=<B>/last_integrate.json`; a repo census of
`last_integrate.json` outside the gateway directory finds that file and its test only). One rule read.

**Consumer-census gap (ASK section 1), my disposition: ACCEPTED, with this measurement.** `integration_refused` is read in the
workspace by the gateway module and its test only (2 files, outside `org/`). In the mcportal bundle at `17dcbb2` it is read by
`src/pages/control-plane/GitStatePanelView.tsx` and typed in `src/api/admin.ts` as the three-state union; the same bundle ships in
the same artifact as the gateway change, so no window serves the new shape to an old reader. Consumers outside these two repos
are NOT enumerated and I claim none. The route is owner-gated and read-only, so an unknown reader meets a changed value and
nothing else. Accepted.

Expected served answers after the restart, per ASK section 1: laptop `no` (`rc: 0`), sitez / dell1 / dell2 `not recorded`.
The `rc != 0` branch stays unexercised by this act.

## 3. The failure branches, in words both halves repeat

**ROLL BACK AT ONCE** (the named command, the ledger closed as rolled back, then stop) when ANY of:
1. `/health` is not 200 within 90 seconds of the restart;
2. the before/after tool-name difference is non-empty;
3. `GET /api/admin/fabric/gitstate` stops answering 401 or 403 to no identity, or its cold compute exceeds 5 seconds, or it reads 0 `recorded`.

**NO ROLLBACK; grade FAIL as measured and open a row** when AC2's People limb alone misses (compute over 30 seconds, fewer than
2 persons, the cadence claim not "absent" on every tool, or the refused-states limb), while `/health`, the tool surface and the
gitstate route in the rollback list above all hold. The issuer decides what follows.

**One input-state case, stated so it is not contested at the act:** AC2 needs `no` among the served states, which depends on the
laptop pointer still reading `rc: 0`. If at the act the laptop pointer reads `rc != 0` or is absent, AC2's refused-states limb
misses on the input, not on the release: that is the second branch (FAIL as measured, row, no rollback).

## 4. Tests accepted

The five release-tree failures are all `FileNotFoundError` on three repo paths outside `infra/aws/ec2/opal-gateway/`, each
`ls-tree` 0 at the live base and 1 at `box/sitez` HEAD, each test passing at HEAD (ASK section 4): within the order's rule
(row Z-S45). Any other failure stops the act.
