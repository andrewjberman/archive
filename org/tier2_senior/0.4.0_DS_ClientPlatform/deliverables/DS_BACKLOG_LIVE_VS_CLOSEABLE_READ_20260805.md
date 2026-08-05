# DS backlog: live vs stale-and-closeable — seat read

**Agent:** 0.4.0_DS_ClientPlatform · **For:** 2.0.0_SA_COO (their ask, 2026-08-05 1616Z)
**Universe:** `to-check.py --all --assignee 0.4.0_DS_ClientPlatform` = **61 active TOs / 27 projects**
(NOT the 16 `get_agent_status` reports — that is the pending-only slice; COO has corrected it upward).

## METHOD, AND ITS LIMIT — read this before using the table

I classified **from each TO's own `<status>` text plus what I know from working this seat**, and I
re-derived only where I had direct evidence today. **I did NOT open and verify all 61.** So:

- **Tier A (CLOSEABLE — high confidence)** rows are ones whose OWN status text declares completion,
  withdrawal, or supersession. The evidence is self-declared; closing still needs the 2-step atomic
  closure (JSON + REGISTRY) by an SA/COO, which is not my lane.
- **Tier B (SUSPECT — needs a look)** rows are ones where age + status *shape* suggests staleness.
  **This is a place to look, never a verdict.** Same discipline as `comp-state`: BEHIND is a
  candidate, not an auto-edit.
- **Tier C (LIVE)** is where I have direct current evidence.

**A row's absence from Tier A is not evidence it is live.** I am reporting what I can support.

---

## TIER A — CLOSEABLE, on the row's own declared evidence (6)

| # | TO | Why it reads closed |
|---|---|---|
| 1 | `ADHC_GLDINC.PARITY-FIX` | status: *"FIX-COMMIT CLOSED + CTO-CERTIFIED (c560e4ca9, CTO cert 145127Z)"* — 55d old |
| 7 | `ADVI_49NNAFIX.D1-D2` | status: *"D1 SHIPPED + FULLY CERTIFIED (ledger eb0cd93ee CLOSED + CVO gate-4 PASS)"* — **⚠ D2 half needs confirming before close; the row names D1 only** |
| 24 | `INF_PRICEFRESH.DRAFT` | status: **`withdrawn-wrong-premise`** — a withdrawn TO on a wrong premise is not backlog |
| 30 | `MDPF_CANRTE.A.canonical-route-design` | Phase A design COMPLETE + delivered `@ab2d2f167`; project JSON says so. Row still `pending` |
| 31 | `MDPF_CANRTE.W2.modelb-spine-shadow` | status: **`deprecated-as-shaped`** — its shape (shadow) was Andrew-vetoed 08-04; superseded by W2R |
| 32 | `MDPF_CANRTE.W2R.modelb-spine-port` | W2R **executed and swapped** 08-04 (~2050Z Andrew word); first full scheduled cycle verified clean 08-05 13:35Z. Row still `pending` |

**Note the pattern in 30/31/32: three MDPF_CANRTE rows describing work that is DONE, DEPRECATED, and
DONE respectively, all still reading `pending`/`active`.** Same seat, same project, same window —
this is where the registry drift concentrates, and it is the project I was working in all day.
(`GRF` was the fourth and I closed it today: `51cd12630`.)

---

## TIER B — SUSPECT, worth a look (11). NOT verdicts.

**B1 — TOs sitting at LANES THAT ARE NOT LIVE (5).** Verified against `get_live_agents` just now:
**no `0.4.0_DS_ClientPlatform~A` and no `~B` session exists.**

| # | TO | Assigned to |
|---|---|---|
| 36 | `NFRA_EDGES.P1.edge-reification-motif-ladder` | `DS_ClientPlatform~B` |
| 37 | `NFRA_EDGES.P3.c3-as-subgraph` | `DS_ClientPlatform~B` +AE |
| 42 | `NFRA_SYSTEM.P1.audit-investigation` | `DS_ClientPlatform~B` +AE×3 +SA |
| 44 | `NFRA_SYSTEM.P4.interplay-maturity` | `DS_ClientPlatform~B` +SA×2 |
| 55 | `OPAL_GLDRNS.A4.wave3-c-core-ports` | `DS_ClientPlatform~A` +SA |

**THIS IS THE GRF FAILURE MODE, FIVE MORE TIMES.** GRF sat `pending` at an unoccupied chair through
**two** Andrew mentions — that is why I have this seat. These five are structurally identical: real
work, addressed to a serial nobody is running. **They are not visible as "unstaffed" anywhere; they
read as ordinary open TOs.** Whether they are live work needing a lane respawn or dead work needing
closure is a COO/MSTR call, but **the current state — assigned and unattended — is the one state
that is definitely wrong.**

**B2 — never-started, aged (6).**

| # | TO | Status | Age |
|---|---|---|---|
| 19 | `DATA_PLATFORM.D2b` | `proposed` | 28d |
| 20 | `DATA_PLATFORM.D2c` | **`proposed-not-built`** | 28d |
| 21 | `DATA_PLATFORM.D5` | `gated` | 42d |
| 22 | `DATA_PLATFORM.D6` | `gated` | 42d |
| 23 | `DATA_PLATFORM.DC-CHAR` | `queued` | 42d |
| 16 | `ADVI_TAGATTR.DS-2` | `deferred` | 35d |

`proposed` / `gated` / `queued` / `deferred` are **not `pending`** — they are pre-execution states.
Six rows in pre-execution for 28-42 days is either a real gate nobody has revisited or a proposal
that quietly died. **Each needs one question answered: what is it gated ON, and is that thing still
true?** I cannot answer that from the row.

---

## TIER C — LIVE, direct evidence (a partial list, not exhaustive)

- `OPAL_VENDORPROVENANCE.BR1-DS` (57) + `BR1` (58) — legs went **production today**; overlap day-1
  fires tomorrow 13:33Z.
- `MDPF_CANRTE` W-1a / W-3 — live program, ruled today, sequenced behind AE's W-1b.
- `MDPF_GLOBAL.EMIT-2` (33), `T4A` (34) — live, scheduled-evidence gated.
- `ADHOC` cot/shell rows (3-6) — issued 08-03/08-04, live.
- `OPAL_ASSETS` C6/C7/C10/C11/V2-5/V2-8/V2-9 (48-54) — CTO-owned program, 22d, active.

---

## THE STRUCTURAL FINDING, which matters more than any individual row

**61 open TOs at one seat is not 61 units of work. It is roughly: ~6 done-but-unclosed, ~5 addressed
to nobody, ~6 parked pre-execution for a month, a live core of maybe 15-20, and a long tail of joint
TOs where I am a SECONDARY assignee and another seat is primary.**

Three mechanisms produce that, and only the third is anyone's fault:

1. **Closure is a 2-step atomic op in an SA/COO lane** — a worker who finishes a TO can self-mark
   `complete`, but the JSON+REGISTRY closure is not mine. **Completed work therefore accumulates in
   MY queue by default.** Rows 30/31/32 are exactly this.
2. **The rollup groups by PRIMARY assignee**, so joint TOs where I am secondary appear under another
   seat's heading while still counting here. Reading headings instead of rows overstates my load.
3. **A lane-addressed TO has no liveness check.** Nothing anywhere compares `issued_to` against
   registered agents. GRF proved the cost; B1 says it is happening five more times right now.

**RECOMMENDATION (one item, cheap, and it is not mine to build):** a `to-check` flag that resolves
each `issued_to` against `get_live_agents` and marks **UNSTAFFED**. That single derived column would
have surfaced GRF before Andrew had to name it twice. **It must be a re-derived predicate over the
live roster, not a hand-maintained list of dead lanes** — otherwise it becomes the thing it detects.

## WHAT I DID NOT DO

- **Did not close anything.** Closure is SA/COO. Tier A is a proposal.
- **Did not open all 61.** Tiers are confidence-labelled; B is "look here", not "close these".
- **Did not verify the D2 half of row 7**, the joint-TO tail (35-46), or the `[??]`-status
  `ADVI_COTSNP` rows (12-14), whose status did not parse at all — three TOs with no readable state
  is its own small finding.
- **Did not judge the OPAL_ASSETS rows** (48-54) — CTO owns that program and its state is theirs.
