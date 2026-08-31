# BRIEF — the self-healing retry auth pattern, as a standalone project under D8

**Author:** `0.6.2_AE_PartnerETL` · **Date:** 2026-08-31 · **Requested by:** Andrew-direct, this session
**Status:** BRIEF. Proposes; mints nothing, builds nothing, deploys nothing.
**Minting is `0.0.0_AB_MSTR`'s act; the design gate is `1.0.0_SA_CTO`'s; the atom-decomp is `2.0.0_SA_COO`'s stage 3.**

## ANDREW-DIRECT, VERBATIM

> write a brief on what happened here. In essence, I want this self-healing auth function to be
> managed by D8. I want self-healing retry auth pattern to be a standalong project under D8.

---

## 1. WHAT HAPPENED — measured, one paragraph

On 2026-08-31 `cot-rebalancer-runner` fired at 06:00Z and raised on all three invocations
(06:00:41 / 06:01:35 / 06:03:26Z) with `RuntimeError: rebalancer /auth/token 200 but no access_token`.
Zero of three Cottonwood bronze feeds landed that day, against a 3-of-3 control on 08-30. **The auth
chain then repaired itself, unattended, at 11:33:37Z** — and nothing re-ran. The date is still a hole.

```
06:00:41 / 06:01:35 / 06:03:26Z   3 invocations, all raised at mint_rebalancer_bearer
landed 2026-08-31   models 0 · accounts 0 · model_detail 0     -> 0 of 3
control 2026-08-30   models 1 · accounts 5 · model_detail 83   -> 3 of 3
secret blackdiamond/cot/session LastChanged 11:33:37Z          -> healed on its own
```

**Severity bound:** 1,659 keys / 41 distinct dates / 2026-07-21..08-30 = 41 calendar days, **0
fully-missing, 0 partial**. 08-31 is the first hole in that feed's life.

⭐ **THE SHAPE THAT MATTERS, and it is why this is worth a project: THE SELF-REPAIR IS WHAT HIDES THE
DAMAGE.** After 11:33Z every downstream instrument reads a chain that is genuinely healthy. The only
wrong thing in the estate is a date that does not exist. **A transient auth gap converts into a
permanent data hole, and the successful self-heal removes the evidence that anything went wrong.**

## 2. ROOT CAUSE — an ORDERING defect, standing and daily

Established by `2.0.0_SA_COO` at source and re-derived by `3.0.0_SA_CVO`:

```
cot-rebalancer-runner fires   cron(0 6 * * ? *)              = 06:00Z
its session mints             cron(30 7 * * ? *) America/NY  = 11:30Z EDT
```

**The runner therefore executes 5h30m BEFORE its own session's daily mint — at MAXIMUM session age
(~18.5h) — every single day, not only on 08-31.** 41 of 41 prior days survived because absolute
session lifetime usually outlasts 18.5h. `cot_rebalancer_runner.tf:171` still reads
`PLACEHOLDER 06:00Z -- exact time = CTO/WS-4 chain-timing confirm`, and that confirm never happened.
**06:00Z is not merely unvalidated; it is the worst hour available relative to the mint.**

**A competing hypothesis was tested and FALSIFIED, so the project does not need to re-derive it:**
`bd-cot-keepalive` ran 4/hour with 0 errors in 19 of 19 hourly buckets straight through the outage.
Gap-sensitivity bounded by a negative control (a known 18h gap renders as ABSENT buckets; the
keepalive had none). ⭐ **The keepalive was working perfectly and the session still died — because the
keepalive holds READ-only on the secret and structurally CANNOT re-mint. It extends; it cannot renew.**

## 3. WHY THIS IS A PATTERN AND NOT A COTTONWOOD BUG — the blast radius, measured

The cookie-riding BD-REST auth design is **shared architecture across firms**, not a cot quirk:

| | Cottonwood | 49 Financial |
|---|---|---|
| session secret | `blackdiamond/cot/session` | `blackdiamond/49f/session` |
| keepalive | `bd-cot-keepalive`, `rate(15 minutes)` | `bd-49f-keepalive`, 15 min |
| refresh chain | `cot-bd-session-trigger` + ET scheduler | `bd-49f-session-chain.tf` auto-login |
| consumers | `cot-rebalancer-runner`, `cot_bronze_ingest.py`, `cot_backfill_date_probe.py` | `bd49f_pull.tf`, `bd49f_reporting_pull.tf`, `bd-49f-interim.tf` |

`cot-rebalancer-runner`'s own docstring names itself *"sibling of `cot_bronze_ingest.py` +
`bd-pipeline/bd-49f-runner`"* — **the estate already knows these are one pattern.** Every consumer
inherits the same three properties: (a) READ-only on the secret, (b) a keepalive that extends but
cannot re-mint, (c) an absolute session lifetime nobody's schedule is validated against.

⚠ **HONEST LIMIT ON THE CROSS-FIRM EVIDENCE.** `0.0.0_AB_MSTR` reported an `HTTP 401 at AUTH, ZERO
data calls` on the 49f side today (the ADVI_BDPARITY W2 re-fire) and a 49f cookie rotation at
`2026-08-31T00:03:47Z`. **I re-derived the rotation myself — `blackdiamond/49f/session` LastChanged
= 00:03:47Z exactly, confirmed.** ⛔ **But I could NOT corroborate a 49f *runner* auth failure:
`bd-49f-runner` Errors = 0.0 across both 08-30 and 08-31.** So the reported 401 came from a different
component, and **I am not claiming two runner failures in one day.** What IS established: the same
architecture, on both firms, with a session that rotated on both firms today.

>> **THE PROJECT'S JUSTIFICATION DOES NOT REST ON THE 49F INCIDENT.** It rests on the shared design:
   every consumer of this pattern has an unvalidated schedule relative to a mint it does not control,
   and a keepalive that cannot save it. Cottonwood is simply where it fired first. <<

## 4. WHAT THE STANDALONE PROJECT SHOULD OWN

**Proposed scope — the AUTH PATTERN, estate-wide:**
1. **Ordering as a first-class constraint.** For every cookie-riding consumer, derive and validate the
   fire time against its own mint time. Retire every `PLACEHOLDER` schedule comment in the class.
2. **Re-mint capability, or an explicit decision not to have one.** Today nothing between the daily
   mint and the next daily mint can renew a dead session. Whether that should change is a design
   question this project owns.
3. **Post-heal recovery.** When a session heals mid-day, what re-runs? Today: nothing. This is the
   generalization of the specific hole.
4. **The pattern's inventory.** A census of every consumer, its secret, its mint, its schedule, and
   its exposure window — so the next instance is found by a table, not by an incident.

**Explicitly NOT in scope, and the boundary matters:**
- ⛔ **NOT alarms/monitors/notifications.** Andrew held all alarms 2026-08-31 pending `GLOBALALARM`
  (D10). **This project FIXES; it does not NOTIFY.** A retry is not an alarm; a detector is, and a
  detector is held. If any deliverable here starts detecting-and-reporting rather than
  retrying/reordering, it has changed category and is HELD.
- ⛔ Not vendor-credential handling, rotation policy, or login mechanism changes.
- ⛔ Not a shadow/parallel auth path (standing Andrew veto).

## 5. BOUNDARY AGAINST `MDPF_HEALGAP` — the thing most likely to go wrong

`MDPF_HEALGAP` already exists under D8 for this incident. **Two projects on one surface will collide
unless the split is stated now.** Proposed, for the gate to accept or redraw:

```
MDPF_HEALGAP            THE INSTANCE. The Cottonwood rebalancer's missing 2026-08-31 date,
                        that runner's schedule ordering, and its recovery gap (cell S9).
                        Terminates when that runner is correct and the date is closed.

THE NEW PROJECT         THE PATTERN. Auth self-healing + consumer retry across EVERY
                        cookie-riding consumer, both firms. Terminates when the class has
                        an inventory, a validated ordering rule, and a stated position on
                        re-mint.
```
⭐ **The tell that the split is right: MDPF_HEALGAP's fix (move one `schedule_expression`) does not
make any OTHER pipeline safer.** That is precisely why the pattern needs its own home — and it is, I
think, the substance of Andrew's *"standalone project"* instruction rather than a second cell inside
the existing one.

⚠ **A name is not proposed here.** Minting, code and register row are `0.0.0_AB_MSTR`'s act.

## 6. WHAT IS ALREADY MEASURED — so the project does not re-derive it

- The 41-of-41 severity bound, and that 08-31 is the first hole in that feed's life.
- RC-B (keepalive gap) FALSIFIED, with gap-sensitivity bounded by a negative control.
- The keepalive is READ-only on the secret and cannot re-mint — structural, not observational.
- `cot-bd-session-trigger` **IS** Terraform-managed (`cot-pipeline/lambdas.tf:20-37`). ⛔ **An earlier
  claim of mine that it was NOT was FALSE — I read a comment heading a `data` block and never opened
  `lambdas.tf`. It propagated into the MDPF_HEALGAP brief and a CTO routing decision before
  `2.0.0_SA_COO` caught it. Recorded here so it is not inherited a third time.**
- The mint cadence is declared: `schedule-et.tf:78-97`, `cron(30 7 * * ? *)` America/New_York.
- `cot_rebalancer_runner.tf:222-250` already carries an `on_success` completion-chain mechanism — any
  completion-keyed design is an EDIT to an existing mechanism, not a port.
- ⚠ **A dead idempotency guard sits on `cot-rebalancer-runner`:** `_already_landed()` calls
  `get_object` inside a bare `except` on a role with no `s3:GetObject` (`implicitDeny`, with
  `s3:PutObject` on the same key `allowed` as control). It has never skipped and cannot, and
  **`--force` is inert in the deployed bytes.** `1.0.0_SA_CTO` ruled it the first hardening item; the
  fix was written and then reverted (`725685f85a`) to return through the decomp path. **Evidence
  survives at `725685f85a`'s parent — do not re-derive it.** This is a PRECONDITION for any
  second-attempt design in either project: without it, a second daily fire re-pulls instead of
  skipping.

## 7. OPEN DECISIONS — none of them mine

1. **[Andrew]** the `--date 2026-08-31` one-shot recovery — currently **HELD** (*"I will discuss with
   CTO, hold for further advisory"*). The hole stays open until it is ruled.
2. **[Andrew]** placement — deferred behind the comb; the whole-register device-ownership decision
   settles it, then `/integrate` parity.
3. **[`0.0.0_AB_MSTR`]** minting the project + register row.
4. **[`1.0.0_SA_CTO`]** the design gate, and whether the §5 boundary is drawn correctly.
5. **[`2.0.0_SA_COO`]** stage-3 atom-decomp before any TO.

⚠ **CANONICAL HOME:** architecture briefs live in `docs/architecture/`, which is the `ANY_CTO` lane —
`0.0.0_AB_MSTR` was refused there earlier today for exactly this reason. **This brief is therefore
written into my own deliverables lane; moving it to `docs/architecture/` is `1.0.0_SA_CTO`'s one
commit, not mine.** Flagged rather than worked around.
