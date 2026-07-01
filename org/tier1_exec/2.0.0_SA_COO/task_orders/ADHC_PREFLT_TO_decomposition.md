# ADHC_PREFLT — COO TO Decomposition

**Decomposed by:** 2.0.0_SA_COO 2026-07-01 · **PRD:** docs/architecture/ADHC_PREFLT_PRD.md v1.0 (RATIFIED, CTO 90fcd9bb5) · **Handoff:** CTO 041816Z
**Consumer:** 0.4.0_DS_ClientPlatform~A (proposal + seams author + proved the sentinel-watch shape) · **Co-consult:** AE 0.6/0.7 (SSM detached-launch + ceiling knobs)
**SEQUENCING (hard):** DS~A stays on INFREF L5 (validate_post_swap) as PRIMARY. These TOs are the FOLLOW-ON — start AFTER the ADVI_INFREF cutover settles. NOT preempting the fire. Not blocking ADVI_BREAKS (tonight's relaunch handled by the raised-ceiling fix).

---

## TO-1 (DS~A) — build `.tools/safe-ec2-run.sh`
Build the preflight GATE wrapper: 3 blocking checks + preflight-record + refuse-semantics.
- **Check 1 — timeout/runtime budget (first-class):** compute `est_runtime` (last-run elapsed OR date-range x per-task cost); BLOCK if `est_runtime x1.5 > ceiling`; long-build ceiling GENEROUS (up to SSM max 172800s), never the inherited 3600/7200. **DETACHED is the DEFAULT for `est_runtime > ~30min** (setsid/nohup + --resume + sentinel-OR-terminal watch = eliminates the timeout class by construction; budget check is the fallback for jobs that can't detach).
- **Check 2 — mechanical seam subset** (`/seams --axis mechanical`, scoped): argparse-choices vs driver call-args, reader-format vs on-disk bronze format, path/script-ref resolution, `bash -n` clean + `comp-pipescript deployed` MATCH on every synced script. + **stall-detection** (no-output-for-N-min = the HANG-variant coverage the budget check structurally misses).
- **Check 3 — watcher terminal-coverage:** see TO-1b.
- **Refuse + record:** REUSE `deploy_ledger.py` as a `preflight-record` leg-class (do NOT invent a new ledger — inherits RED-sweep + COO-alarm infra); REFUSE unbudgeted/unchecked builds (non-zero exit + preflight-record RED); `PREFLIGHT_OVERRIDE="reason"` audited exactly like safe-apply HALT_OVERRIDE.
- **HOME:** `.tools/safe-ec2-run.sh` (+ `comp-preflight` alias) — gate-family cohesion, NOT infra/aws/ec2/ (CTO call, PRD §4).
- **Compiler mandate:** P1 `deploy_ledger.py --help` + read `safe-apply.sh` for the refuse/override pattern; P2 `bash -n` + a canary test (mirror `test-safe-commit-canary.sh`); P3 self-validate against tonight's 3 failure modes (must BLOCK all 3).

## TO-1b (DS~A) — canonical `ssm-terminal-OR-sentinel` watch helper (check #3)
Reusable watch helper alongside `inbox-watch`. **Acceptance:** emits an event on each terminal state `TimedOut`/`Failed`/`Cancelled` AND on the success sentinel; unit-proven on BOTH paths. (This is the proven shape — CTO terminal-watch `bii1b3v64` caught tonight's TimedOut; DS~A's sentinel-watch proved the sentinel side.)

## P3 (follow-on, non-blocking) — CLAUDE.md rule + gate-ramp
CLAUDE.md rule + announce-then-enforce ramp (NFRA_COMPRAIL pattern) so the gate teaches at violation time. COO coordinates the fabric-wide rollout (touches every DS/AE build). AFTER TO-1/1b land.

---

## Acceptance criteria (PRD SS7 — machine-checkable, verbatim)
1. `.tools/safe-ec2-run.sh` exists, `bash -n` clean, on PATH; `comp-preflight` reflex resolves.
2. A build whose `est_runtime x1.5 > ceiling` is REFUSED (non-zero exit + preflight-record RED) unless detached OR `PREFLIGHT_OVERRIDE` (audited).
3. A build with a mechanical-seam defect (bad argparse choice / reader-format mismatch) is REFUSED at preflight.
4. The watch helper emits an event on each of TimedOut/Failed/Cancelled (not only sentinel) — unit test.
5. Re-running tonight's 3 INFREF failure inputs through the gate: all 3 BLOCK before firing.
6. Every gated build writes a `preflight-record` (via deploy_ledger.py) — a build with no record = a gate miss.

**Scope:** SSM/EC2/long-batch builds only. OUT: fast Lambda invokes, local .py runs, sub-minute jobs (override-fatigue risk). RAVC to COO at TO-1 + TO-1b landed; COO RAVCs CTO.
