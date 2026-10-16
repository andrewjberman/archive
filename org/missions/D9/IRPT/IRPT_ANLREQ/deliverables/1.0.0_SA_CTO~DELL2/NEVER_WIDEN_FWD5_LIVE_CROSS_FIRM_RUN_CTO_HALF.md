# Never-widen CTO half -- IRPT_ANLREQ FWD-5: the live cross-firm exercise (mint one firm-B principal, drive, remove)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~19:0xZ. **Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R58_FWD5_LIVE_EXERCISE_PACKET_DRAFT_20261016.md`
(@860c22c8a1), blob `5fbb9aaf241944505c85a634ffbf8fa1a5ec50a0`, sha256 `c33ddc205740e15476ec28b8466e7f593707ee73ec4d39b7fecf4b9a71ce7308`,
8,696 bytes (re-measured). **COO half:** `2.0.0_SA_COO~T2`.

## Verdict

**SIGNED** on the blast radius as written: ONE users row on DEV for firm B with `allowedFirmIds` = [cottonwood], zero entitlement rows,
printed by the mint and refused otherwise; GET calls to firm A's one synthetic ticket; no write to any ticket, request or job; the principal
removed and read ABSENT on the GSI and a consistent read. **Firm B = cottonwood is CONFIRMED.** Firm A is `49financial`, with the synthetic
ticket TCK-20261015-944c84f8 and REQ-d47252fe... Applier `0.7.0_AE_CloudOps~IB2` (rule 34).

## Conditions

1. **Port 5174 is shared with Andrew's smoke.** The only dev port is 5174 (Andrew-direct 2026-09-24), and it is serving his smoke copy
   (`C:/dev/smoke-template-5174`, which contains `dc057891`). The run REUSES that server and NEVER stops or restarts it. If the driver needs a
   checkout that server does not carry, the run waits and asks this seat. The same binds AR-v-34's sitting.
2. **Any LEAK stops at once:** the principal is removed first, and only the route name is reported. UNREACHED is not a pass.
3. **S134 disarms on the readback:** every made call REFUSED, the principal ABSENT.

-- `1.0.0_SA_CTO~DELL2`

## RE-SIGN on the corrected packet (2026-10-16 ~19:1xZ); the signature above is VOID

**SIGNED** on blob `2f0952bbb324b8c205755ace2ac026a2a906ba92`, sha256 `bee21686810f4968267d4c84b0228c858258742b82f65751d1dba21e59ce6830`
(@c95103f242, re-measured). Read at signing, with a diff ignoring whitespace and line endings against `860c22c8a1`, the change is two things.
First, section 1a2: the driver's flags read `--firm-a cottonwood` (the principal's own firm) and `--firm-b 49financial` (the ticket's
owner). Second, the 5174 reuse clause. The act, the blast radius and the firms are unchanged, and the conditions above stand.

## RE-SIGN 2 on the packet with the positive control (2026-10-16 ~20:3xZ); RE-SIGN 1 above is VOID

**SIGNED** on blob `57052520eb60cf7b19bc5138843045a30200d02e`, sha256 `0a0bec98665898cbe0818e59ea867f78c9e7eca408f0a2a6a457ed3e6351bfc3`,
14,221 bytes (@9666f7bf14, re-measured). Read at signing by `git diff caca1739a7 HEAD`. The change is the laptop CTO's control
(XA-...-4c60, relayed in my msg 9804), in sections 1c, 3, 4 and 7b: a second staff-only principal `fwd5-control-r60@opal.invalid`
(`allowedFirmIds` = [49financial], entitlement rows 0, no new grant), the driver's `--control` mode pinned at `06206f2864`, and the fence
graded per route as SHOWN only where the control reads ALLOWED and the firm-B run reads REFUSED.

**Blast radius:** two DEV users rows, each with a 3-hour TTL and both removed in step 3; GET calls only. That is the whole widening, and it
is covered. **Both branches:**
- **Control exit 0, run exit 0:** the fence is graded on the ALLOWED routes, and S134 disarms.
- **Control exit 1 or 2,** including the stated unread list-shape case: nothing is graded, both principals are removed, S134 stays ARMED,
  and the issuer re-cuts.

**Conditions 1 to 3 stand.** In addition:
- **A LEAK** stops the sitting whatever the control reads; both principals are removed first.
- **The applier is `0.7.0_AE_CloudOps~IB2`.**

-- `1.0.0_SA_CTO~DELL2`
