# NEVER-WIDEN HALF (COO) -- NFRA_MCPORTAL.TO-MP-z-5 -- SIGNED, with two dispositions

**Signer:** `2.0.0_SA_COO~MP` (the issuer), 2026-10-13 ~20:5xZ.
**ASK:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-z-5.md` @`fa8d4250bf`,
read whole, together with row `NFRA_MCPORTAL-Z-S45`. Release branch `rel-nfra-mcportal-gw` @`233440afaf` on live base
`185dc048881da2030efa11f4d0bfb8704b500c66`. mcportal bundle `0e02a1f`.

## What this half signs

The ASK's sections 1 and 2, unchanged. Five gateway files ship (three under `app/`; the two test files are source only).
One owner-gated admin route is added, `GET /api/admin/gateway/breakdown`. One catch-all route is added LAST, and it
answers only the paths in the served bundle's `routes.json`. The bundle moves from `bc37107` to `0e02a1f`. There is one
restart and two S3 keys. It may not touch the MCP tool surface, any IAM, any store write, any Terraform or other
infrastructure, any other manifest service, or the two deploy scripts.

## The blast radius, read by this seat (not taken from the ASK)

- **Census.** `git diff --stat 185dc04888 233440afaf` over the whole repo reads 6 files, 1014 insertions and 2 deletions:
  `EC2_MANIFEST.json` (1 line, `mcportal_commit` bc37107 -> 0e02a1f), `admin_api.py` +2, `admin_gateway_breakdown.py`
  +377, `server.py` +29/-1, and the two new test files. This matches ASK section 3.
- **`admin_api.py`.** One import and one `Route("/gateway/breakdown", ..., methods=["GET"])` after
  `/fabric/calls/close`. Nothing else in the file moves. This is the order's step 0, verbatim.
- **`server.py`.** Three hunks, read in full: the `dashboard_deep_link` handler; its `Route("/{path:path}", ...)` line
  as the LAST route after `Mount("/mcp")`, with a two-line comment; and `PlainTextResponse` added to the
  `starlette.responses` import.
- **Both branches of the catch-all, from the handler's own code.** A GET or HEAD whose path is listed in `routes.json`,
  other than `/`, goes to `dashboard_root`, so the owner gate applies first. Every other request falls to the
  slash-redirect replay (a 307 only where another route matches the alternate path) and then a plain 404. If
  `routes.json` is missing or malformed, the handler lists nothing and fails closed. Because the route is last, no
  existing route can be shadowed.
- **The served `routes.json` at `0e02a1f`.** It lists 12 paths: `/`, `/control-plane`, `/cost-management`, `/gateway`,
  `/health-check`, `/infosec`, `/mcp-server`, `/mcp-server/recent-changes`, `/open-calls`, `/operations-report`,
  `/user-analytics`, `/user-management`. None of them is a gateway API path. `/health` stays its own route above the
  catch-all.
- **Bundle swap `bc37107..0e02a1f`.** 19 files, +758/-43, all under `src/` (the gateway page, the Control Plane and Open
  Calls readability changes, the sidebar) plus `public/routes.json`. These are MP-z-2 and its Amendment 1, both drained.

## Disposition of ASK section 3a -- the `server.py` import hunk: ACCEPTED, within the bound

The order's bound names the deep-link handler, its route line and its comment. The import token is part of that
handler: its 404 branch calls `PlainTextResponse`, and without the import every unlisted path would raise `NameError`.
The token comes from MP-z-3's own graded and drained commit `e42d2c35c3`. It adds no route, no behaviour and no
capability beyond the handler's. This is not a widening, and the act is not stopped on it.

## Disposition of ASK section 6 -- step 1's "0 failed": a CLOSED-LIST version of option (a)

Option (b), "no test newly fails against the base's own run", does not cover this case. The two MP-z-1 tests are NEW in
this release, so under (b) they would read as newly failing. So this half rules as follows:

1. **The payload's grade is `box/sitez` HEAD.** There the named set already reads 87 passed, 0 failed (row Z-S45), and
   that grade stands.
2. **On the release tree, the step-1 run must read EXACTLY 67 passed and EXACTLY these 7 failed, by test id, and no
   other:**
   - `test_admin_fabric.py::test_roster_equals_devices_register`
   - `test_admin_fabric_calls.py::test_real_capture_calls`
   - `test_admin_fabric_calls.py::test_request_accepted_by_open_calls_scan`
   - `test_admin_fabric_gitstate.py::test_real_capture_gitstate`
   - `test_admin_fabric_overlap.py::test_real_capture_overlap`
   - `test_admin_gateway_breakdown.py::test_channel_with_no_holder_is_empty_list`
   - `test_admin_gateway_breakdown.py::test_holders_match_the_dispatch_chain`

   If any other id fails, or any of these passes or fails for a different exception, the act STOPS with a BLOCKING row.
   Re-run this immediately pre-act and record the id list in `MP-z-5_PRE_ACT_RECORD.md`.
3. **Causes accepted, as Z-S45 measured them.**
   - Five of the failures read repo data files that are absent from the base commit (`ls-tree` 0 at `185dc04888`,
     1 at HEAD). They sit in test files this release does not modify, and no gateway payload reaches them.
   - The other two encode the trunk's emptied `_SEED` in `identity_scope.py` (NFRA_OPLGTW OG-tg-1, not yet released).
     On the live base, `opalbloomberg@opalinvest.com` really is a scoped m365 holder, and the handler reports that
     truthfully, as C15 requires.
4. **Consequence, stated so that nobody reads it as a defect at the FWD-20 sitting.** Until NFRA_OPLGTW releases OG-tg-1,
   the breakdown page will list the Bloomberg account as a holder on the m365 channel. That is the live grant, and it
   agrees with DIRECTION_SITEZ Z7: the account keeps mirroring until Andrew has read FWD-20.

## Conditions

1. Follow the order's step 4 as written: open the NEVER-2 entry and commit its sentinel BEFORE the act; run `/health`
   within 90 seconds or roll back at once; read the MCP tool names before and after, with an empty difference.
2. Re-read the rollback key `opal-gateway-185dc04888.tar.gz` (ETag `b486e614fc122cf854f0d063bd198e4e`) immediately before
   the act. Also re-read `EC2_MANIFEST.json` `deployed_commit` at the act: if it is no longer `185dc04888`, STOP and
   re-cut. NFRA_OPLGTW's OG-bd-2 is queued behind this release (`2.0.0_SA_COO~O` msg 33706), and nothing else may land
   in between.
3. Post-act, the manifest record corrects `previous_deployed_commit` to `185dc04888...`. The release tree carries the
   stale `2c0f84966d`, which is the known safe-ec2-deploy defect recorded on MP-x-4, MP-r-2 and MP-n-1.

## Verdict

**SIGNED.** This half binds the blast radius above. Section 3a is accepted. Section 6 is ruled as the closed list in item
2. Row Z-S45 is dispositioned by this half for the issuer; its L8 adjudication remains the CVO's.
