# Trade Request on the PROD recut -- trial receipt (2.0.0_SA_COO~V2, 2026-10-19 ~15:15Z)

Asked by the CTO (msg 10728, after Andrew's "all holds are lifted"): confirm the trade hunks and their tests pass on the PROD recut; state whether `POST /api/scoped/tickets/attachment-upload` is configured on PROD, by route and environment.

## 1. The trade hunks on a PROD base (a trial, not the recut)

Method: a scratch portal worktree `C:/dev/scratch-v2-trade` (branch `scratch/v2-trade-trial`) from `origin/PROD` @`d729ee6d84565bfa4ce508ddf199d40ac0851482`, then `git cherry-pick c05e3dda` (the DEV commit "Trade Request as a form upload; engine submit unwired"). `node_modules` is a junction to the main portal checkout, so dependency versions are DEV's, not PROD's.

- `c05e3dda` is exactly the five files the CTO named: `src/api/endpoints/tickets.ts`, `src/pages/TicketCenter/TicketCenter.tsx`, `src/pages/TicketCenter/TradeRequestParts.tsx`, `__tests__/trade-form-upload.test.tsx`, `__tests__/trade-request.test.tsx`.
- ONE conflict, `TicketCenter.tsx` import block (lines 90-103): PROD carries the meeting import block (`showsMeetingOutcome`, `viewerIsCoordinator`); the trade commit carries the older block. Resolution: keep PROD's meeting block and add `TradeFormOpen` to the trade import: `import { TradeRequestForm, TradeFormOpen } from './TradeRequestParts'`. The other four files applied clean.
- `bun test` of the five trade and meeting files: 45 pass, 0 fail (217 expect calls).
- `bun test src/pages/TicketCenter` (the whole folder): 221 pass, 0 fail, 35 files.
- Typecheck (`r20_checks.py portal-tsc`): `R20-TSC-OK`.
- Not run here: eslint, `vite build` (D2's recut gates carry them).

## 2. One finding the five files do not cover

`TicketCenter.tsx` line 745 (on PROD and on DEV) still filters the New Ticket type list: `Object.entries(TICKET_TYPE_LABELS).filter(([v]) => v !== 'trade_request')`. The five files do not remove it. With that filter in place the form is built but unreachable from the list; only an existing `trade_request` ticket shows `TradeFormOpen`. Removing the filter is a sixth hunk in `TicketCenter.tsx`, and two tests assert the hiding today and would fail without a change: `__tests__/trade-form-upload.test.tsx:480` and `__tests__/meeting-request.test.tsx:368` (both `expect(options).not.toContain('trade_request')`). So the five files, as committed, ship the form with the type list still hiding it; whether to reveal it now is the CTO's ruling.

## 3. The upload door on PROD (reads only; the route was not called)

- API `opal-portal-data-proxy-api` (`7k3ed8px20`, stage `$default`, auto-deploy). Route `POST /api/scoped/tickets/attachment-upload` is present, authorization `CUSTOM`, target integration `vgix3jf` = `AWS_PROXY` to `arn:aws:lambda:us-east-1:313476888478:function:opal-ticket-api`. Its sibling `GET /api/scoped/tickets/{ticketId}/attachment` is present with the same integration.
- Lambda `opal-ticket-api`, last modified 2026-10-17T08:20:32Z, state Active. Environment: `TICKET_ATTACH_BUCKET_TEMPLATE=opal-data-{firm}`, `TICKET_ATTACH_KEY_TEMPLATE=portal/{firm}/state/ticket_attachments/trade-form/` (the value ends in `/`, as `lambda_function.py:820` requires).
- Role policy `opal-ticket-attachments-trade-form-policy` is attached beside `opal-ticket-api-ses-send` and `opal-tickets-table-rw`.
- Not read: the policy's resource list against the bucket and prefix, and whether the S3 prefix holds objects. The form's own 503 refusal answers a missing environment.
- Claim: MEASURED for the route, the integration and the two environment values; NOT MEASURED for the S3 permission scope.
