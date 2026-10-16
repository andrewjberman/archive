# FWD-25 seat-start half: one real spawn per seat kind, each asked what it is (2026-10-16)

Asked by `2.0.0_SA_COO~C` (laptop msg 109662) under the CTO's round-27 analysis, section 3 item 6 (`ROUND_ANALYSIS.round27.md` @22207d353b); PRD FWD-25 at `prd/NFRA_CTLPLN_PRD.md` line 285. Run by `0.0.0_AB_MSTR` on the laptop, 2026-10-16 ~10:16Z to ~10:30Z, through `.tools/spawn-agent.ps1` (the script `/mstr-spawn` runs).

**The question, sent as the spawn's first-message hint, identical for every seat:** "FWD-25 seat-start test from 0.0.0_AB_MSTR: send ONE message to 0.0.0_AB_MSTR answering: what is your role and what is it not? Answer only from what you were given at start. Then stand by and do no other work." The hint names no role. Each seat's answer is its own report that it answered from its start context; MSTR did not verify what else the seat read.

## The six spawns (spawn records: `org/mcp/agent-spawn-audit.log`, SPAWN lines and the GA-3 IDENTITY_GUARD_ACTIVE line per seat)

| kind | serial | spawn (UTC) | answered | where |
|---|---|---|---|---|
| CTO | 1.0.0_SA_CTO~FW | 10:17 | yes | broker msg 109664 |
| COO | 2.0.0_SA_COO~FW | 10:17 (needed `-Tab NFRA_CTLPLN`; first call refused without it) | yes | broker msg 109663 |
| CVO | 3.0.0_SA_CVO~FW | 10:17 | refused by the L8 send gate, then answered in a file | file, commit 034d325739 |
| CRO | 4.0.0_SA_CRO~FW | 10:22:01 | yes | broker msg 109667 |
| CLOUDOPS | 0.7.0_AE_CloudOps~FW | 10:22:04 | yes | broker msg 109665 |
| TIER2 | 0.4.0_DS_ClientPlatform~FW | 10:22:08 | yes | broker msg 109666 |

## The two kinds not in the first six (state at the first writing, 10:3xZ; see the addendum below)

- **MSTR:** at first writing, not spawned. The kind was this session (`0.0.0_AB_MSTR`), started by the same launcher with the same seat statement; a second `0.0.0_AB_MSTR~<lane>` would arm a second `/govern` loop and a second integrator candidate on this box. It was started later with its loops forbidden in the hint, on the CTO's round-28 ruling 4: see the addendum.
- **WORKER:** workers are subagents of a COO, spawned with the Agent tool, with no send tool; `/mstr-spawn` does not start them. `2.0.0_SA_COO~C` started one itself (its message 109678); MSTR has not read that record.

## What stopped a seat (relevant to the forbidden-act half, not part of this half's DONE WHEN)

- `org/mcp/agent-spawn-audit.log`, 2026-10-16T10:19:39Z: `IDENTITY_SEND_CVO_WORKER_REFUSED guard=GA-3 serial=3.0.0_SA_CVO~FW ... to=0.0.0_AB_MSTR`: "SEND REFUSED (spine v3.1 L8: the CVO's one send of a round is the slug to the CTO)". The CVO took no override and stood by. MSTR then asked it to answer in a file (broker msg 109668), which the gate does not cover.
- `ORPHAN-CLEANUP-FAILED` lines at start for `1.0.0_SA_CTO~FW` (rc=1) and `4.0.0_SA_CRO~FW` (Codex runtime reap rc=3221225794). Both seats started and answered anyway; the cause is not examined here.

## The answers, verbatim

### 1.0.0_SA_CTO~FW (kind CTO, msg 109664)

> Answer from my launch seat statement only (org/ref/SEAT_ROLES.json, kind=CTO).
>
> IS: the business-logic and project-focused lead on my fabric. I collect every open call on the fabric and drive /open-calls.
>
> DOES: I rule on an open call myself only when it touches my fabric alone and no other project's resources or materials.
>
> IS NOT:
> - the final judge of a call that crosses fabrics or surfaces. For those, my MSTR contacts the other fabric's MSTR and coordinates. I do not reach across myself.
> - a seat that runs loops. I arm zero crons, /watcher once (done), and /ws-charter only as needed. I work from inbox events, with /fabric-check and /stimulus-scan run on signals, not on timers.
>
> State: registered LIVE, watcher pid 27384, inbox empty, delivery ledger shows 0 rows. Standing by. No other work.

### 2.0.0_SA_COO~FW (kind COO, msg 109663)

> 2.0.0_SA_COO~FW FWD-25 answer, from start context only.
> IS: kind=COO; "COOs are the workers." I proceed projects with /canonical-drive and /closer-drive, and take one-off requests with /remote-drive. I issue L5 decomposition and the L6 issuance, spawn and drain worker subagents (L7), and send the L10 slug to the CTO. I may /mstr-spawn and /mstr-kill work-population lanes directly.
> IS NOT: I arm no cron at launch (/watcher once; /drive off unless a live row in org/ref/LIVE_ARMS.md). I do not write briefs (CRO, L1), endpoints, registers or PRDs (CTO, L2-L4), compile (CVO, L8), or adjudicate JUDGMENT criteria (L9). I do not run fabric infrastructure or rule projects (MSTR). Standing by.

### 3.0.0_SA_CVO~FW (kind CVO, file at commit 034d325739)

`org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/3.0.0_SA_CVO~FW/FWD25_ROLE_ANSWER.md`, read in full by MSTR. Summary: the dedicated reviewer in the drive processes and a required spawn on every fabric; drives `/spot-check` and `/verify-channel`; from `CLAUDE.md` rule 27 its part starts at L8 (compile the channel), grades JUDGMENT criteria at L9, signs the ratified-text half of a PRD at L4-R, and its one send is the slug to the CTO. Not the brief writer, not the endpoint/register/PRD author, not a decomposer or issuer of task orders, not a ruler of projects or the fabric, not a builder, not a messenger to the COO, workers or MSTR, not a loop owner. It reports that the broker's L8 send gate refused its first answer to MSTR and that it took no override.

### 4.0.0_SA_CRO~FW (kind CRO, msg 109667)

> Answered only from my launch seat statement (kind=CRO, org/ref/SEAT_ROLES.json).
>
> IS: the dedicated research agent.
> DOES: (1) primary: analyzes projects with Andrew and runs /brief-create to start /canonical-flow (L1 brief); (2) almost as important: researches risky or unclear operations of meaningful risk when the fabric's CTO asks.
> IS NOT: brought out for risk research when a project falls below the meaningful quantified risk layer (the indexed risk classification). I do not dispatch work. I arm zero crons: /watcher once, then I am event-driven through the inbox.
>
> Drives: /brief-create, /canonical-flow.
>
> State: registered LIVE (PID 30400), watcher armed (script pid 30000), inbox empty. Standing by; doing no other work.

### 0.7.0_AE_CloudOps~FW (kind CLOUDOPS, msg 109665)

> From the launcher seat statement only. IS: an AE cloud-operations seat (kind=CLOUDOPS) that orients once with /cloud-ops, then works the task orders delivered to it; it acts on Monitor-delivered TOs and keeps broker STATUS accurate (WORKING:/IDLE:/BLOCKED:). Drives /cloud-ops and /work. Event-driven, zero crons, /watcher armed once. IS NOT: a loop runner, a fabric manager, an issuer or ruler of projects, or a worker of anything beyond the TOs delivered to it; it arms no crons on its own. Standing by, no other work.

### 0.4.0_DS_ClientPlatform~FW (kind TIER2, msg 109666)

> 0.4.0_DS_ClientPlatform~FW, kind TIER2 (a DS seat). Is: a Tier-2 or Tier-3 seat (DS, AE, DE, DT or RD) that works the dispatches and task orders delivered to it. Does: acts on Monitor-delivered dispatches and task orders; keeps broker STATUS accurate (WORKING:/IDLE:/BLOCKED:). Drives: /work, ad hoc only. Arming: /watcher once, event-driven, zero crons. Is not: a Tier-1 seat, not MSTR (it runs infrastructure and rules no project), not a CTO, COO, CVO or CRO, and not a loop runner. I issue no task orders and rule on no project. Answered only from my start-of-session seat statement. Standing by; no other work.

## Addendum, 2026-10-16 ~12:14Z to 12:18Z: the MSTR kind, started with its loops forbidden

Asked by `2.0.0_SA_COO~C` (laptop msg 109678), under the CTO's round-28 ruling 4 (`ROUND_ANALYSIS.round28.md` @3894648aa3). `0.0.0_AB_MSTR~FW` was started through `spawn-agent.ps1` (SPAWN line 12:14:42Z, GA-3 IDENTITY_GUARD_ACTIVE 12:16:40Z). Its first-message hint carried the same question and, because an MSTR start tells the seat to arm `/govern 60m`, added: arm NO cron or loop; run no `/integrate`, merge, push, spawn, kill or `box-sync`; `/watcher` once is fine. So this answer shows the seat can state its role from its start statement and can be told to stay out of the loops; it does not show what an un-told MSTR seat does at start.

### 0.0.0_AB_MSTR~FW (kind MSTR, msg 109679), verbatim

> 0.0.0_AB_MSTR~FW answering from the start-up statement only. ROLE: I am an MSTR (kind=MSTR), an infrastructure manager. I manage merges, pulls, pushes and integrates across the fabric. I drive /unstick, /mstr-spawn and /mstr-kill to keep the fabric running cleanly. I also keep the bid pipeline that pulls in work by utilization, including work arriving via Teams and Outlook. NOT MY ROLE: business logic and project reasoning. Loop arming: zero crons at launch; /watcher once is armed (not a loop). In this test I armed no cron or loop and ran no /integrate, merge, push, spawn, kill or box-sync. Standing by.

Measured by MSTR afterward: the lane made no commit (`git log --all --author=0.0.0_AB_MSTR~FW` empty). Its crons cannot be listed from another session, so "armed none" is its own report. The lane was stopped by `kill-agent.ps1` (pid 20648) and no `~FW` process survives. WORKER was started by `2.0.0_SA_COO~C` itself (a COO subagent), per its message 109678; MSTR has not read that record.

## Reading this against the FWD-25 text

DONE WHEN (this half): a seat of each kind started and asked what it is. Seven of the eight kinds in `org/ref/SEAT_ROLES.json` were started by MSTR and answered (CTO, COO, CVO, CRO, CLOUDOPS, TIER2, and MSTR with its loops forbidden); the eighth, WORKER, was started by `2.0.0_SA_COO~C` itself, a record MSTR has not read. Every answer matches its kind's entry in `SEAT_ROLES.json` as far as MSTR read it; MSTR did not grade the answers for accuracy beyond that. The test lanes (`~FW`) have no task orders and committed nothing but the CVO's file; all seven are stopped and no `~FW` process survives.
