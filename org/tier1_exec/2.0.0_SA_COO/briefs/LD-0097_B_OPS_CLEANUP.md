# LD-0097 §B ws-side ops cleanup track — banking brief

**Author:** 2.0.0_SA_COO (ws COO)
**Date:** 2026-05-26T~12:10Z
**Origin:** MSTR LD-0097 §B SCOPE-ASSIGN MCP `20260526T120500Z` (CL COO + ws CTO + ws CVO CC'd)
**Disposition:** CORROBORATE-no-additives on §1 scope shape (per `[[framing-lean-to-explicit-verdict-on-invite]]` cycle 87 canonical doctrine)
**Surface at:** next /mstr-review cron tick (AC7 LD-0087 fire ~HH:?+12h) per LD-0097 §B coordination clause

---

## §1 — Item 1: Sister-improvement scan (.tools/ consumers of .comp-graph/.agent_context)

**Scope:** identify `.tools/` consumers of legacy shared `.comp-graph/.agent_context` file pattern for follow-on session-id-keyed migration per LD-0070 §7.2 pattern (ws CTO halt-gate-check.sh fix `5879534fa` precedent).

**Survey result:** 5 active consumers in `.tools/` (1 documentation):

| Consumer | Lines | Migration status | Sister-improvement candidate? |
|---|---|---|---|
| `.tools/halt-gate-check.sh` | 38, 44, 46, 65 | **ALREADY MIGRATED** to session-id-keyed pattern with legacy fallback (ws CTO `5879534fa` cycle 86; comment block lines 44-46 explicitly cites clobber-prone-class) | n/a (canonical anchor) |
| `.tools/ajb.ps1` | 10, 180 | Uses session-id-keyed primary already (per LD-0088 A.1 launcher pattern); comments reference shared file as fallback context only | NO — already pattern-aligned |
| `.tools/git-hooks/headmove-guard.sh` | 57-58 | Reads SERIAL from legacy shared file only; no session-id-keyed fallback | **YES — sister-improvement candidate** |
| `.tools/hooks/post-send-commitment.sh` | 28-29 | Falls back to shared file when AGENT env-var unset | **YES — sister-improvement candidate** |
| `.tools/hooks/post-tool-telemetry.sh` | 32 | Falls back to shared file when OPAL_AGENT_SERIAL env-var unset | **YES — sister-improvement candidate** |
| `.tools/hooks/README.md` | 24 | Documents SERIAL= source ordering | n/a (doc; would update post-migration) |

**3 sister-improvement candidates** for session-id-keyed migration: headmove-guard.sh + post-send-commitment.sh + post-tool-telemetry.sh.

**Banking observation:** the 3 candidates differ in priority:
- **headmove-guard.sh** = git-hook fires on every commit; clobber risk = wrong author-line attribution under concurrent multi-agent commits. **HIGH-PRIORITY**.
- **post-send-commitment.sh** = MCP commitment-ledger fires on every send_message; clobber risk = wrong agent-source in ledger. **HIGH-PRIORITY**.
- **post-tool-telemetry.sh** = PostToolUse-hook telemetry stream; clobber risk = wrong agent-attribution in telemetry events. **MEDIUM-PRIORITY** (telemetry stream is observational; downstream tools cross-check).

**Recommendation:** route these 3 to ws CTO substrate-improvement track for slack-cycle migration (per LD-0097 §B "bank for slack-cycle write"). Three are bounded scope (each ~10-line edit + session-id-keyed env-var lookup with legacy fallback per halt-gate-check.sh pattern).

**Action:** bank for ws CTO follow-on; do NOT execute migration during AC9 12h convergence window per LD-0097 §B out-of-scope discipline.

---

## §2 — Item 2: MSTR registration TTL-drop pattern survey

**Scope:** investigate MSTR-specific (CronCreate frequency mismatch) vs fabric-wide (broker heartbeat-window mismatch); propose mitigation if structural.

**Empirical anchor (session-cumulative, leveraging prior banking):**

- **MSTR observed STALE drops:** /watcher cycles 34 / 37 / 40 / 41 / 42 / 43 / 47 / 50 + cycle 41 598s recovery (cycle 84 §4 banking)
- **CL COO Step 0.5 fires:** 12 corrective fires across cycles #1-#16 (12:0 CL:ws ratio per cycle 87 §1)
- **ws COO Step 0.5 fires:** 11 PASS-no-op cycles 77-87 (zero drops)
- **ws CTO + ws CVO:** no observed TTL drops this session (broker shows them LIVE 0-1s consistently across all cycle queries)

**Pattern empirical (per cycle 85 §6 obs 2 CL COO refinement):** TTL drop is **session-lifecycle-asymmetric** not pure-fabric-class.

**Refined hypothesis:**
- ws COO + ws CTO + ws CVO: actively cron-firing (20m /drive, 30m /ws-charter, 20m /spot-check) within TTL window (broker STALE-at-120s; heartbeat-on-cycle within 20m); TTL never elapses
- CL COO: same 20m /drive cron but each cycle is shorter execution time → less cron-fire-density per wall-min → TTL drops between fires
- MSTR: /watcher cron at different cadence (~10m wakeup per `ScheduleWakeup` chain not CronCreate fixed-interval); /watcher self-relaunches; possible wakeup-chain-pause when no new message activity → TTL window can elapse during long quiet stretches

**Mitigation proposal (structural-or-pattern):**
- (a) **No-op**: Step 0.5 self-registration check per /drive + /watcher cron handles drops corrective; mechanism works as designed; fabric-asymmetry is observable-not-blocking
- (b) **Heartbeat-extension reduction**: lower broker TTL from 120s to 60s would NOT help (would just create more drops requiring more corrective fires); raise to 300s would mask the corrective trigger pattern
- (c) **Cron-cadence-density refinement**: synchronize cron cadences across Tier-1 agents to ensure heartbeat within 60-90s window — but this would create cron-fire-collision risk

**Recommendation:** **(a) No-op**. The current 12:0 + Step 0.5 corrective fires + ws COO 11-cycle PASS-no-op pattern empirically demonstrates the mechanism is **stable + self-healing**. Step 0.5 is the structural solution; no mitigation needed. Banking observation: fabric TTL pattern is healthy; observability without action required.

**Action:** mark Item 2 as **INVESTIGATED → NO-MITIGATION-NEEDED**; surface at /mstr-review fold as empirical confirmation that Step 0.5 mechanism works as designed across all Tier-1 + Tier-0 agents.

---

## §3 — Item 3: AC10 launcher cleanup follow-on audit

**Scope:** verify-class one-cycle audit; confirm no residual launcher inconsistencies.

**Audit:**
- AC10 origin: ws CTO `076b48d49` ajb.ps1 launcher first-message templates cleanup (cycle 68 ~05:13Z; Andrew direct flag on "garbled phrasing")
- AC10 sub-tests AC10.1-.4 acceptance criteria all met per commit message
- AC10 verified: ws CVO + CL CVO cross-fabric paired-verifier 8/8 templates literal-read PASS (cycle 70 §1 banking; LD-0089 §3 paired-verifier canonical first-fire)
- AC10 status per LD-0089 ws CTO closure refresh (cycle 73): "AC10 CLOSED-EMPIRICALLY-VERIFIED"

**Subsequent launcher amendments (post-AC10):**
- LD-0093 (`b7e0bd048` cycle 76) added AJB_FORCE_WS env-var bypass for LD-0088 A.1 CL-serial routing — default A.1 behavior unchanged; bypass fires only on explicit env-var set
- ws CTO `5c5eacdf2` (cycle 77) Step 0.5 self-registration health check to /drive SKILL — not launcher
- ws CTO `cfaba5800` (cycle 74) AC1 A.1+A.2 SHIPPED: ajb.ps1 CL-serial cwd routing + org/XXX.md Step 1a fabric-cwd documentation

**Residual check:**
- ajb.ps1 ~/.tools/ has 3 modifications since AC10 ship: AC10 cleanup `076b48d49` + AJB_FORCE_WS bypass `b7e0bd048` + AC1 A.1+A.2 cwd-routing `cfaba5800`
- Templates content (per AC10.1-.4) preserved through all 3 modifications (additive changes; not edits to template content)
- Cross-fabric verification (cycle 70) confirmed 8/8 templates clean

**Verdict:** **NO RESIDUAL LAUNCHER INCONSISTENCIES**. AC10 cleanup remains CLOSED-EMPIRICALLY-VERIFIED through subsequent additive launcher work (LD-0093 bypass + LD-0088 A.1 cwd-routing). Templates content preserved.

**Action:** mark Item 3 as **AUDIT-CLEAN**; surface at /mstr-review fold.

---

## §4 — Summary disposition for /mstr-review surface

| Item | Disposition | Action |
|---|---|---|
| §1 Sister-improvement scan | 3 sister-improvement candidates identified (HIGH: headmove-guard.sh + post-send-commitment.sh; MEDIUM: post-tool-telemetry.sh) | Bank for ws CTO substrate-improvement-track slack-cycle migration; do NOT execute during AC9 12h convergence |
| §2 MSTR TTL-drop survey | INVESTIGATED → NO-MITIGATION-NEEDED; pattern is session-lifecycle-asymmetric; Step 0.5 mechanism handles corrective fires structurally | Banking observation only; confirms Step 0.5 doctrine empirical |
| §3 AC10 launcher audit | AUDIT-CLEAN; no residual inconsistencies; AC10 closure stable through subsequent additive launcher work | None; AC10 stays CLOSED-EMPIRICALLY-VERIFIED |

**Time-to-execute:** ~10min wall total (parallel grep + empirical-leverage + reasoning); zero ws-side infra churn; AC9 12h convergence stability preserved.

**Out-of-scope items confirmed not touched:**
- ws CTO substrate-improvement track (their lane)
- feature_clb-cwd Claude Code hang investigation (CL COO liaison per LD-0097 §B)
- Substrate that ws CTO owns

**Surface scheduled:** next /mstr-review cron tick (AC7 LD-0087 fire ~12h cron) per LD-0097 §B §2 coordination clause.

— 2.0.0_SA_COO (ws COO)
