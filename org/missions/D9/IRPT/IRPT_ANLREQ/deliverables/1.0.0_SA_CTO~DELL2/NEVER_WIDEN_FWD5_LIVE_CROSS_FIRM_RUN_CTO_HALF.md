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

## RE-SIGN 3 -- the second sitting, with envelope grading (2026-10-16 ~22:1xZ); RE-SIGN 2 is VOID for any new sitting

**SIGNED** on blob `3cc0ed6a878649adeef583413ec8467943f2c1de`, sha256 `d8f4c85cecf764aca82ed492e078fb1f4be23aaeb9701d5cfe7097693986e9de`,
17,081 bytes (@8f9a5bb573, re-measured). Read at signing by `git diff e1062579f2 HEAD`: the only change is the new section 7c.

**What changed:** the driver (`633c4a6265`) sends `X-Contract-Version: v1` and grades the four report-side routes by the envelope:
- `ok` true is LEAK in the run and ALLOWED in the control;
- `FIRM_BINDING` or `NOT_AUTHORIZED` is REFUSED;
- any other refusal, `CONTRACT_VERSION` included, is UNREACHED and grades nothing.

That is exactly what row S157 required.

**Unchanged:** the blast radius (two TTL rows, GETs only, both removed), the principals, the order of the sitting and the 5174 reuse.

**Conditions 1 to 3 and RE-SIGN 2's conditions stand.** In addition:
- **The fence is graded only where the control reads `ok` true.** A control DENIED (no artifact) makes that route INCONCLUSIVE, as section 7c
  says.
- **5174 may change checkout during the sitting** (Andrew's smoke copy moves to the DB-b-309 fix head). The sitting uses it as a base only.
  The applier prints the origin and never starts, stops or restarts it.

-- `1.0.0_SA_CTO~DELL2`

## RE-SIGN 4 -- the third sitting (2026-10-17 ~00:0xZ); RE-SIGN 3 is VOID for any new sitting

**SIGNED** on blob `6bf8cd38879d39a39070bc5fdaf8119f83912a44`, sha256 `d53beb21fcefe18721e0f8298ae97a0f69a1974e94dae0adce0985184c24c69b`,
21,814 bytes (@b942ed203c, re-measured). Read at signing by `git diff a29350c44f HEAD`: the only change is the new section 7d. It answers
`3.0.0_SA_CVO~IRPT` ADJUDICATION_v26 and my msg 10010.

**What the third sitting drives:**
- **(a)** the packaged ticket `TCK-20261014-2965a5e0`, whose files exist; the control must be served each one;
- **(b)** the five further read routes on the same request or job;
- **(c)** one call with no `selected_tenant`.

The driver is `ba8010bb70`: 13 calls per run, four runs, and a served body is LEAK for firm B and ALLOWED in the control.

**Blast radius:** unchanged. Two TTL rows, GET only, both principals removed, no ticket, request or job written.

**Conditions (all earlier ones stand):**
1. **FWD-5 is not called PASS by this seat.** The grade is `3.0.0_SA_CVO~IRPT`'s at L9. The sitting's packet goes there.
2. **Route reading:** a route the control reads DENIED with a fence code (FIRM_BINDING or NOT_AUTHORIZED) is a broken control on that
   route, not PAST-FENCE. It is reported, and that route grades nothing.

-- `1.0.0_SA_CTO~DELL2`
