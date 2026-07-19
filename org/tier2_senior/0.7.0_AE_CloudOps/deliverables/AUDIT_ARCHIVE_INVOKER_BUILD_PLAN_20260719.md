# Audit-Archive Invoker — BUILD PLAN (gate-request to CTO)

**Owner:** `0.7.0_AE_CloudOps~B` · **Gate:** `1.0.0_SA_CTO` · **Drive/coord:** `2.0.0_SA_COO` · **Verify:** `3.0.0_SA_CVO`
**Date:** 2026-07-19 · **Deadline:** 2026-07-23 (interim manual practice expires; after that, absence of an invoker is itself a finding)
**Spec:** `docs/briefs/audit-archive-invoker-spec-20260716.md` (4 binding clauses) · **Behind:** RV-0052 F-008 / F-A / RV-0050 tail
**Status:** DESIGN COMPLETE, ground-truth exercised · **NOT BUILT** — build gated on CTO's vehicle pick (§5) + scope confirm (§7)

This doc exists so the design does not live only in an MCP thread — the exact rot class the spec catalogues.

---

## 0. Ground truth (LIVE-EXERCISED 2026-07-19, not asserted)

| Claim | Test | Result |
|---|---|---|
| Positive control fires | `head -n <S1_lines> live \| cmp -s - <S1_copy>` (07-13 redaction sits after S1) | **FIRED** — diverges char 33/line 1 (redaction + S1 F-D encoding). Detector works. |
| S2 baseline byte-faithful | `head -n <S2_lines> live \| cmp -s - <S2_copy>` | **PASS** — S2 is a byte-exact prefix of live; append-only since 07-16. |
| Unverifiable tail is real | `wc -l` S2 (14638) vs live (15209) on git-author-override | **+571 lines** unverifiable (the RV-0052 F-008 tail). |
| Archive is tracked | `git ls-files org/audit/archive/` | 26 files (13 logs × 2 snapshots) — invoker creates + **commits** a new snapshot dir. |
| Live logs untracked+gitignored | `git check-ignore` on each | **All untracked/ignored** — a cloud Lambda CANNOT see them; **the vehicle MUST be local.** |

**Coverage = 13 audit logs**, all exist live: 6 under `org/`, 6 under `org/mcp/`, 1 under `org/tier0/audit/`.
**Live churn since S2 (6 of 13 grew):** comp-which-rail +349KB, git-author-override +48KB, ledger-hook +47KB, agent-spawn +33KB, orphan +4KB, surface-check-ack +320B. The other 7 are static.
**Snapshot dir grammar:** `YYYY-MM-DDTHHMMSSZ` (UTC, no colons in time, `Z` suffix) — parse `%Y-%m-%dT%H%M%SZ`.

---

## 1. What the invoker does (two responsibilities)

**A. ARCHIVE (durability action, currently manual):** snapshot the 13 untracked live logs into `org/audit/archive/<UTC>/` and commit them — but ONLY when the snapshot-cadence threshold is met (§6), so the archive does not bloat.

**B. VERIFY (the 4 clauses), on every run, cheap, always:**
1. **Liveness — age of newest, never existence/count** (spec §1). `now() - max(dirname-timestamp of snapshots) > AGE_THRESHOLD` → finding. Uses the ISO dirname, not mtime (mtime is gameable). Existence/count are BANNED — they pass forever on a corpse.
2. **Integrity — the prefix test, S2-forward** (spec §2). Per covered log: `head -n <baseline_lines> live | cmp -s - <baseline_copy>`. Baseline = that log's copy in the most-recent CLEAN snapshot; the chain starts at **S2** and NEVER looks at S1. PASS = append-only (permitted). FIRE = a non-append edit → finding; **withhold the snapshot, do NOT advance the baseline** (a divergence must be adjudicated before it is re-baselined).
3. **Division of labour — detect the EDIT, a human rules on the AUTHORITY** (spec §3). Finding text is `"a non-append edit occurred at line N, removing these records: <enumerated>"` — never "this was bad." No authority allowlist, ever (that is the request that turns it into something arguable-into-a-PASS).
4. **Alarm-on-its-own-death** (spec §4). The invoker writes a self last-run marker every run; an **independent reader** (§4-mech) fires if the invoker itself has gone silent. A cadence's corpse is solved by alarming on the cadence's death, not by adding a cadence.

---

## 2. The built-in controls (CVO/COO closure bar — "a check that cannot fail is not a check")

Every run, BEFORE recording any PASS, re-exercises two controls; if either does not behave, the invoker **fails-closed** (its own detector is presumed broken):

- **Positive control (real, known case):** S1 → live prefix test on git-author-override MUST FIRE (the 07-13 redaction). *A sweep that cannot find a known-present non-append edit is a broken instrument reporting silence.*
- **Negative/instrument control (generated, measures the instrument not the author):** take the current baseline, flip one byte in a temp copy, confirm the prefix test FIRES against the mutant; and confirm a pure append (baseline + appended line) does NOT fire. Per NEVER#22b: *a generated control measures the INSTRUMENT.*

**Exercised-not-configured (COO's bar):** the fail-closed path is proven by FEEDING a stale/absent snapshot and watching it FIRE, not by reading config. Both controls run at ship time AND on every invocation. CVO verifies the fail-fires same-turn on land.

---

## 3. Delivery of findings (respects Andrew's 07-17 alert-suspension — see §4)

NO SES/SNS/CloudWatch. Findings go to a durable committed record: `org/audit/archive/FINDINGS.md` (append a dated entry per non-append/liveness/death fire) + a non-zero exit surfaced inline by the vehicle (like comp-surface-check prints CRITICAL). The snapshot itself is the durability artifact.

---

## 4. ALERT-SURFACE ANALYSIS (MSTR's explicit ask: surface to CTO if any clause reads as a new alert surface)

Andrew-direct 2026-07-17 SUSPENDS new SES/SNS/CloudWatch alert TF during OPAL_CONSOLIDATION (`memory/feedback_suspend_new_alert_systems_during_consolidation.md`) — and it OUTRANKS a per-task sequencing GO. Walking each clause:

| Clause | Realization | New alert surface? |
|---|---|---|
| 1 Liveness/age | local check → exit code + `FINDINGS.md` entry | **NO** |
| 2 Integrity/prefix | pure local `head\|cmp` computation | **NO** |
| 3 Division of labour | finding TEXT wording only | **NO** |
| 4 Alarm-on-death | local last-run marker + independent reader at session-startup (spec explicitly permits "absence-registry row, bucket-side, or equivalent") | **NO** |

**Verdict: no clause requires a new SES/SNS/CloudWatch surface.** The whole instrument is a LOCAL verifiability check emitting durable findings + a git-committed snapshot. It does not collide with the 07-17 suspension — consistent with MSTR's framing ("a verifiability instrument, spec-approved, NOT a new alert/SES/SNS system"). Recorded here per the surface-don't-self-authorize discipline; **CTO confirms.**

---

## 5. VEHICLE — CTO's decision (this is the open gate)

Because the live logs are LOCAL + gitignored (§0), a Lambda / EventBridge / scheduled-cloud-agent cannot see them (would require an S3 substrate change = out of scope AND a new surface). **The vehicle must be local.** This also sidesteps the entire apply/IAM/22a/store-writer gate surface COO flagged — there is no AWS write, no IAM, no `terraform apply` in the recommended path.

| Option | Cadence | Corpse-resistance | Shared-infra touch |
|---|---|---|---|
| **(3) RECOMMENDED — standalone `.tools` script run at session-startup + on-demand** | every new session (fabric spawns them constantly) runs the fast CHECK; snapshot only when threshold met | **Strongest** — no single keeper; the cadence is as alive as the fabric. Self-satisfies clause 4: the next session's startup run IS the independent death-reader. Mirrors `/watcher` arm-at-load. | one startup-hook line (like /watcher) |
| (1) git `post-commit` hook | every commit | dense, but committing-a-snapshot-within-a-commit is recursive/messy | `.tools/hooks/` + install |
| (2) Claude PostToolUse hook on safe-commit/push | every commit | dense; hook context can't easily self-commit | `settings.json` |

Recommendation **(3)**: it is the most direct answer to the corpse problem the spec exists to solve, needs no AWS, and self-provides clause 4. The snapshot commit uses `safe-commit.sh` with a tight pathspec (`org/audit/archive/<newTS>/ FINDINGS.md .invoker-heartbeat.json`) so it never sweeps a peer's working tree.

**Vehicle = `.tools/audit-archive-invoker.py`** (Python: clean timestamp math + `cmp`; passes commit-gate py_compile/ruff-py39; `from __future__ import annotations`). Not a `comp-*` tool → comp-manifest-check registration invariant does not bind it (will run it anyway as courtesy).

---

## 6. Proposed thresholds (configurable; CTO may retune)

- `AGE_THRESHOLD` (liveness finding): **24h** — on vehicle (3) the newest snapshot refreshes many times/day during active periods; 24h fires only if the fabric-wide cadence truly stalled.
- `SNAPSHOT_INTERVAL` (when to mint a new snapshot): **≥12h since newest AND some covered log grew** — keeps archive cadence sane (not one-per-session) while verification runs every session.
- `DEATH_THRESHOLD` (clause 4, invoker silent): **48h** since last-run marker.

---

## 7. Open questions for the CTO gate

1. **Vehicle** — approve (3) standalone-at-startup, or pick (1)/(2)?
2. **Scope** — the startup-hook line touches the shared session-startup path (org/XXX.md and/or `/watcher`). Is wiring that in-scope for me, or does CTO wire the shared-infra hook while I own the `.tools` script + controls?
3. **Thresholds** (§6) — accept or retune?
4. **Manifest** — explicit `org/audit/archive/MANIFEST.txt` (13 canonical paths; a live audit log NOT in the manifest → coverage-gap finding) vs. derive coverage from the latest snapshot's contents. I recommend the explicit manifest (implicit coverage silently drops a new log).

## 8. Build+verify sequence (once gated)

1. Write `.tools/audit-archive-invoker.py` + `MANIFEST.txt` + baseline pointer.
2. Exercise controls: S1 fires · synthetic mutant fires · append does NOT fire · stale/absent snapshot fires (COO bar).
3. Mint S3 (first automated snapshot); confirm S2→S3 is a clean append-only window (negative control at the whole-instrument level — must NOT fire).
4. Wire the gated vehicle.
5. `safe-commit` under my author line; run comp-manifest-check.
6. Report CTO + COO + CVO on land; CVO verifies fail-fires same-turn.
