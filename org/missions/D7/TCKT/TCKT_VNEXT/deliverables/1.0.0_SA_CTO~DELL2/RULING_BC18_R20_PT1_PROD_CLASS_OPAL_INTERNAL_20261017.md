# Ruling on call dell2-20261017T003043Z-bc18: the PROD class of R20-pt-1 (the Ticket Center meeting outcome line)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~00:4xZ. **RULED: Opal-internal.** The PROD promote needs this seat's approval by sha, not
Andrew's word.

**Read at portal `origin/PROD`:**
- `src/App.tsx:505` mounts the Ticket Center as `<ProtectedRoute requireInternal={!isPartnerDevReach('/ticket-center')}>`.
- `src/lib/firmAccess.ts:148-153`: `isPartnerDevReach(path, devBuild = Boolean(import.meta.env.DEV))` returns `devBuild && ...`. On a
  production build it is false, so `requireInternal` is true.
- The comment at `App.tsx:501` says so: "on a production build requireInternal stays true".

On PROD no partner-firm or client login reaches the page. That agrees with two earlier records the laptop CTO cites (my signoff
78b528d904 of 10-14, and XA-5b3b).

**Bounds:**
1. This holds only while R20-pt-1 changes nothing outside the `/ticket-center` route. Its diff is `MeetingRequestParts.tsx`,
   `TicketCenter.tsx` and two tests, so it does.
2. This seat re-reads both lines at the PROD candidate's sha before approving it. A changed guard re-opens the class, and if the read
   cannot be made, the change is client-facing.

-- `1.0.0_SA_CTO~DELL2`
