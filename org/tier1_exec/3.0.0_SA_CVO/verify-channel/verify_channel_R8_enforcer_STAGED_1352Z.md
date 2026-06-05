# /verify-channel (Mode A) — R8 universal idle-aware cap — STAGED pre-apply (structural-logic verified)

**archetype:** VALIDATE
**Agent:** 3.0.0_SA_CVO · 2026-06-05 ~1352Z · COO-staged R8 apply-verify + AE CC evidence (`20260605T134757Z`)
**Status:** PRE-APPLY. R8 (`4caa6d458`) BUILT, NOT yet applied (Andrew-gated). This banks the static-logic verification; empirical apply-verify fires on AE's apply RAVC2.

## Structural-logic verification (verifiable now, pre-apply) — POLL-GAP-SAFE
`infra/aws/lambda/ec2-auto-shutdown-enforcer/lambda_function.py` `idle_entire_window()`:
| Property | Evidence (line) | Protects against |
|---|---|---|
| Reaps only if **Maximum CPU < 3% in EVERY 5-min bucket** across 3h | L100 `all(p['Maximum'] < IDLE_CPU_THRESHOLD for p in points)` | MDPF poll-gap class: any inter-poll spike = a >3% bucket = `all()` False = SPARED |
| **Maximum** per bucket (not average) | L83-87 | a brief in-bucket spike still spares; average would dilute |
| **None on metrics-gap** -> no reap | L94-98 (`len(points) < expected-3` -> None), L127 (`if idle_all is None: skip`) | a metrics gap misread as idle |
| **`AutoShutdown=disabled` tag exempt** | L198 | legit always-on services (opt-out escape hatch) |
| Only after **>3h uptime** AND idle whole window | L124-126 | short legit runs |

**Verdict (structural): PASS — the idle-test is poll-gap-safe by design.** The blast-radius concern COO flagged (false-reap of active-but-low-CPU MDPF poll-gap class) is structurally prevented: a single >3% bucket anywhere in the 3h window spares the instance.

## AE CC empirical evidence (banked, corroborating-but-easy-case)
demo-reclone `i-03343a60`: continuous 35-50% CPU (~12x the 3% floor), no >3h sub-3% window (Pass-2 write ~18h continuous-CPU). Trivially spared — confirms R8 won't reap an obviously-active job, but NOT the sharp test (a 35-50% job is far above floor).

## REMAINING for apply-verify (fires on AE apply RAVC2) — the genuine residual
1. **Deployed == this code** — comp-pipescript / Lambda LastModified MATCH post-apply.
2. **Env vars** — `IDLE_CEILING_HOURS=3`, `IDLE_CPU_THRESHOLD=3.0`.
3. **SHARP TEST — untagged-always-on-low-CPU fleet enumeration:** the one real false-reap case is a legit always-on service that is genuinely <3% (every bucket) for >3h AND lacks `AutoShutdown=disabled`. At apply-time: enumerate the fleet, identify any long-running instance whose CPU profile could go fully-idle-but-up >3h without the exempt tag (lightly-loaded web/queue/monitoring boxes), flag before R8 reaps it.
4. **bd-gold exemption removal:** AE CPU-verified zero idle-but-up window over 10d (AE-owned); re-confirm bd-gold has activity in every 3h window during its ~6.7h run.

— 3.0.0_SA_CVO
