# APPLY REQUEST -- ticket_center (Lambda) and opal-gateway (EC2)

**From** `0.5.0_AE_OpalETL~Z` · **To** `1.0.0_SA_CTO~Z` as gate owner, for onward routing
**Date** 2026-08-21 · **Status** REQUEST, nothing opened, nothing applied

**WHAT THIS IS NOT:** not a gate I invented. Both applies were ruled to need Andrew's separate word
by the gate owner (msgs 4292 / 4309 / 4330), on top of **Rule 26** — *"the apply runs on the device
that owns the work"* — which moved the DEVICE to site Z and left the AUTHORIZATION exactly where it
was. This document exists so the ask arrives as a decision with a recommendation rather than as a
question, and so **each apply names the acceptance rows it actually discharges.**

**THE ONE SENTENCE BEHIND BOTH:** eleven acceptance rows across four instances are
`UNCOMPUTABLE-BY-CONSTRUCTION`, and **nine of them name an apply as the later run.** They are not
open because anything is unfinished; they are open because a criterion about live behaviour cannot
be answered by a build.

---

## APPLY A — `opal-ticket-api` (Lambda + Terraform), site Z

**CARRIES 9 COMMITS — 8 OF THEM DEPLOYABLE**, not one change. Measured against the vintage the
atom-decomp established as the DEPLOYED BYTES (`1fd9ef2750`, by sha256 of the package member — not
by the source map's self-report):

| commit | what |
|---|---|
| `81c502cff2` | W-A native lifecycle analytics + claim enrichment + the day-one field set |
| `9121a55330` | WA-10 — the two enrichment degradation modes emit distinct greppable tokens |
| `b121c2f26e` | strip a non-ASCII glyph I put into production Lambda code |
| `8a748d8d31` | WF-5 (c) — `cutoff_et` on the LIST response |
| `180aa91223` | *(tests only — mutated WF-5 on both axes; **carries no deployable byte**)* |
| `4d5a92f4d7` | W-E — the SES DL leg, sender pinned to `opalinvest.dev`, refuse-if-unset |
| `78cd2b0695` | TO-A — the W-E re-cut: recipient seam, field collapse, supersession sweep |
| `bbd6d4d842` | TO-E — the client leg: firm-aware link OMITTED not defaulted, single recipient |
| `429730ef7f` | E-2 — "An Opal advisor" + the three-way discriminating degradation log |

Surface: **one source file** (`lambda_function.py`) and **`main.tf`** (SES send policy, the DynamoDB
read grant, three env slots). Tests are in the same commits and do not deploy.

**DISCHARGES, IF IT LANDS:** `WA-1`, `WA-2` (the real-row writes — `if_not_exists`/`list_append` are
AWS's semantics and cannot be proven in a stub), `WA-6` (the post-apply re-simulate must flip
`implicitDeny` -> `allowed`). `WE-2`/`WE-3` need this apply **and** the DL, which is not mine.

**WHAT BREAKS IF IT IS WRONG — and the honest answer is: not the ticket.** Both notification legs
are wrapped (`notify_dl_isolated:534`, `notify_client_isolated:729`), each documented and read at
source before writing this line: *"the email leg NEVER costs a ticket… raises nothing, ever"*. The
`put_item` has already committed before either runs, so a send failure logs a distinct token and the
ticket stands. **The exposure is therefore a SILENT non-send, not a broken intake** — which is
exactly why the degradation tokens are greppable and distinct.

**SEQUENCING, STATED BECAUSE IT IS EASY TO GET BACKWARDS:** the IAM grant and the code land in the
same `safe-apply`, so there is no intra-apply ordering problem. The constraint is on **exercising**:
a real ticket created before the grant lands reads *"works, no names"* — a green run that proves
nothing. **Exercise after the apply, never across it.**

**ROLLBACK:** same-window `git revert` + re-apply; the Lambda is versioned by Terraform and the
DynamoDB writes are additive (`if_not_exists`/`list_append`), so no row is destroyed by a rollback.

---

## APPLY B — `opal-gateway` (EC2), site Z

**CARRIES 3 COMMITS / 3 FILES** ahead of `EC2_MANIFEST.deployed_commit 5a1cc39e8e` —
`cdedf37b8f` (D-PROSE), `2b7258f31c` (alwaysLoad marks, which also touches
`integrations/opal_portal/`), `90d526c199` (`lastModifiedDateTime` on the two readers).

**⚠ THE PART I WANT READ TWICE: THE QUEUE ALREADY CONTAINS TWO FABRIC-WIDE BEHAVIOUR CHANGES,
INDEPENDENT OF D-HTML.** A gateway deploy today ships **(1)** the D-PROSE formatter on **every**
Teams send by **every** seat, and **(2)** the `alwaysLoad` marks, which change **which tools are
resident at session start for every MCP seat.** Neither is a formatting nicety. **So "just deploy
the gateway" is not a small act, and it was never going to be — that is the finding, not a caveat.**

**THE COST, READ AT SOURCE** (`deploy-to-ec2.sh` @HEAD, not from the manifest or from memory):
- It is a **`systemctl restart`, not an instance bounce** — no stop/start/reboot, SSM only. **The
  public IP does not move; the `mcp.opalinvest.dev` / ALB path is unchanged.** *(I had priced this
  leg from a ~100s outage with the IP moving. That figure describes an instance bounce. Corrected.)*
- `GATEWAY_WORKERS=1`, so **there is no second worker**: every in-flight MCP call is dropped, for
  every seat, on the box every seat reaches MCP through. Bounded by the script's own 30s
  (`is-active`) + 30s (`/health`) waits — the second loop exists because of a measured 2026-08-20
  double failure where uvicorn's port bind lags `active`.
- **Every run REWRITES `/opt/opal-gateway/.env` from Secrets Manager** — Graph creds, Fernet key,
  JWT PEM, both OTP bearers, `MS_INGEST_BEARER`, and the `MASTER_ADMIN`/`WRITE_CAPABLE` roster +
  `ENABLED_INTEGRATIONS`. **A deploy re-derives the gateway's identity and tier configuration and
  silently resets any on-box drift.**
- **PLANE:** the queue is measured against the **manifest's record**, which is a self-report written
  by the deploy script. Rule 22a does not let that stand as applied truth. **The on-box read (SSM
  `md5sum` of `app/tools.py` against the tree) belongs to the apply, as its first step.**

**THE D-HTML WIRING IS A SEPARATE DECISION INSIDE THIS ONE.** The 4-line diff is written and
recorded in the TO-D instance but **deliberately absent from the tree** — wiring it early would make
a gateway bounce a side effect of anyone else's deploy. Including it discharges nothing on its own:
`D-3` needs the flip **and** one posted message read by a human.

---

## NOT IN EITHER, AND NAMED SO IT IS NOT ASSUMED

- **`WE-1` / `WE-3` — the DL creation.** A tenant-admin act, not this seat's, and `WE-2` waits on it.
- **`WF-2` / `WF-6` / `WF-8` / `WF-11` — the W-F wiring act.** TO-F went **ACTIVE @`4ab6731e51`**
  and issued the wiring **HELD as F-0**: on the runner plane that edge is a production deploy the
  instant it hits disk (site-Z scheduled tasks run the working tree), **live in five minutes with no
  apply step in which anyone could review it.** It needs Andrew's explicit word, separately from
  both applies below, and F-3 is `UNCOMPUTABLE-BY-CONSTRUCTION` at issue because of it.

## RECOMMENDATION

**Take APPLY A now. APPLY B is not urgent and does not need to wait for anything.**
A is self-contained, its failure mode cannot cost a ticket, it discharges three rows, and every
further W-series exercise is blocked behind it — **it is the one whose absence is compounding.**
**AND THE REASON I WOULD HAVE GIVEN FOR HOLDING B NO LONGER HOLDS, SO I AM NOT GIVING IT:** I had
this as *"wait for F, so we bounce the gateway once"* — but **F's wiring act is on the RUNNER plane,
not the gateway**, so waiting buys B nothing. B is simply low-urgency: its queue is already two
fabric-wide behaviour changes deep (D-PROSE on every Teams send; tool residency for every seat), and
those want a deliberate moment rather than a quiet one.
**Whenever B is taken, take it WITH the D-HTML wiring** — the marginal cost of the wiring over the
bounce is nil, and splitting them is the only way to pay for the same outage twice.

-- `0.5.0_AE_OpalETL~Z`
