# Audit-Archive Invoker — GATE-2 (script built + exercised; 1 blocker + 1 finding for CTO)

**Owner:** `0.7.0_AE_CloudOps~B` · **Gate:** `1.0.0_SA_CTO` · **Date:** 2026-07-19 · **Deadline:** 2026-07-23
**Script:** `.tools/audit-archive-invoker.py` @ `0aecf5c67` (441 lines, commit-gate clean) · **Plan:** @0d31ce396
**Status:** BUILT + EXERCISED · **BLOCKED** on a GOVERNANCE_AUDIT lane ruling (below) before S3 can mint.

---

## 1. Exercised controls (all live, evidence in hand)

`python .tools/audit-archive-invoker.py --self-test` → **7/7 OK, each asserting its SPECIFIC 3-way reason:**

| Control | Result | Reason (not just "fired") |
|---|---|---|
| A(S1-redaction) | NON_APPEND | real redaction detected, line 1/col 33 |
| B1(mutant) | NON_APPEND | generated mid-file 1-byte edit, line 2/col 1 |
| B2(append) | APPEND_OK | pure append does not fire |
| B3(growth-signal) | GREW | live_nl>base_nl **via the same prefix_test read = the interlock** |
| C1(absent+growth) | FIRE | no snapshot + uncaptured tail |
| C2(stale+growth) | FIRE | 432h-old + uncaptured tail |
| C3(stale-no-growth) | OK (no fire) | stale-but-complete = correct idle (false-Monday guard) |

`--dry-run` (mints nothing): rc=1, one finding `LIVENESS/STALE-BASELINE` — baseline 72.6h old AND uncaptured
tail exists. Correct: the archive genuinely IS stale right now.

**V1→V2 catch (the discipline):** my first self-test read PASS while 3 controls fired for the WRONG reason
(missing-file / code exception). Fixed by the 3-way {APPEND_OK/NON_APPEND/ERROR} return so each control
asserts its specific reason. A fire for the wrong reason is not a control; caught pre-gate.

## 2. F-008 tail: now VERIFIED (not just checked)

Clause-2 integrity sweep over all 13 covered logs vs the S2 baseline = **ALL APPEND_OK**. The ~571-line
git-author-override tail (and every other covered log) is confirmed **byte-exact append-only since 07-16** —
upgrading RV-0052 F-005/F-008 from "unverifiable tail" to "verified append-only" for the covered window.

## 3. S1 redaction characterization (CTO's separable finding — DISPOSITION: authorized test-fixture cleanup)

CTO asked: what was redacted, and is it authorized? Grounded from the diff (encoding-normalized, order-indep):

- **Exactly 17 records** removed (S1 → live): **12× serial=1.0.0_SA_CTO + 5× serial=0.0.0_AB_MSTR**, 0 others
  — byte-for-byte matching the spec's claim.
- **What:** all `NEVER-OVERRIDE` gate-exercise entries, 07-13 06:00–08:35Z. The 12 CTO are
  `test_never_rules_gate.sh` fixtures (`reason=scratch branch cleanup` / literal `<reason>` placeholders);
  the 5 MSTR are `RV-0048 gate exercise` harness runs. **Self-evidently test/fixture noise, not operational
  overrides.**
- **The raw diff's 576 lines were a trap:** 559 were the F-D encoding artifact (em-dash extended-ASCII in S1
  vs UTF-8 in S2 — every line with a `—`), only 17 were the real redaction. This is also WHY S1 fires the
  positive control for two independent reasons (encoding at line 1 + redaction at depth), as the spec notes.
- **Authority:** spec-documented as Andrew-authorized 07-13T16:16Z; content confirms benign test-cleanup.
  **Per clause 3 I detect the EDIT and state no authority opinion** — if CTO wants the 07-13T16:16Z
  authorization grounded independently of the spec's citation, route to MSTR. My read: clean, no live concern.

---

## 4. BLOCKER — the invoker cannot write its own output lane (CTO ruling needed)

The owned-paths gate (correctly, not bypassed) blocks 0.7.0_AE from `org/audit/archive/**` (lane
**GOVERNANCE_AUDIT** = MSTR + CTO + COO + CVO — deliberately *"not world-writable"* tamper-evidence) and from
the one-line `.gitignore` add (lane **BASE_EXEC**). This blocks (a) committing MANIFEST/.baseline/FINDINGS,
AND (b) **every runtime snapshot commit.** It also exposes a real design question: vehicle (3) runs at EVERY
agent's session-startup, so the snapshot commit's author is whatever serial started — and we cannot add every
agent to a tamper-evidence lane. Two ways to resolve (CTO's arch-call; CTO lands whichever):

**Option A — fixed invoker identity + lane grant.** Add one identity (`0.7.0_AE_CloudOps`) to GOVERNANCE_AUDIT
+ the one .gitignore/BASE_EXEC line; the invoker always commits as it. Full vehicle-(3) corpse-resistance (any
session archives). Tamper-model preserved: the tool only APPENDS immutable dated snapshots + advances the
baseline forward + appends findings — it cannot rewrite existing evidence, so "a log anyone may rewrite" does
not apply. Cost: a .owned-paths.yaml change; snapshot commits attributed to the tool's owner regardless of who
triggered.

**Option B (RECOMMENDED) — dynamic author + graceful lane-defer.** The invoker commits as the RUNNING session's
serial (from the LD-0290 `sessions/*.serial` file); an exec startup's commit lands, a non-exec startup's commit
DEFERS gracefully (a "snapshot-deferred (lane)" note, not a failure). NO .owned-paths change — respects the
lane exactly as written (only execs write GOVERNANCE_AUDIT). **Detection stays universal** (every startup runs
clauses 1–4, findings to stdout; the gitignored heartbeat is not lane-gated so clause-4 death detection works
for all); archiving rides the frequent exec sessions, and clause-1/4 self-escalate to an exec if it falls
behind. Requires a small script revision (dynamic author + treat lane-denial as "deferred", not "commit-fail").

**My recommendation: B** — lower blast radius (no governance-file change), respects the deliberate
tamper-evidence lane, keeps corpse-resistant detection universal, and aligns with the LD-0290 identity model I
already use. But A is cleaner if you want a single archiving identity. **I hold the script's commit-path +
the S3 mint until you pick.**

## 5. Wiring proposal — org/XXX.md Step-1b (I deliver the line; CTO lands it, per Q2 SoD)

Placement: a new **A.2**, immediately after A.1 (the serial-file write — which Option B's dynamic author reads):

```bash
**A.2 — Audit-archive durability + tamper-evidence (audit-archive-invoker, CTO-gated).**
python .tools/audit-archive-invoker.py || true   # append-only verify + archive-when-due; never blocks startup
```

Rationale: after A.1 (serial file exists for Option B's author resolution), before the inbox/watcher steps;
`|| true` so a fail-closed exit never blocks an agent's startup (findings surface on stdout + FINDINGS.md).
Identical line under both A and B — only the script's internal commit-authorization differs.

## 6. Remaining sequence (post-ruling)

1. CTO picks A/B (+ lands lane grant if A, or I revise script for B).
2. Mint S3 (first automated snapshot) — de-stales the 72.6h-old archive; confirm S2→S3 append-only (negative
   control, must not fire).
3. Commit MANIFEST/.baseline/FINDINGS (via the resolved lane path).
4. CTO lands the Step-1b wiring; CVO verifies fail-fires same-turn (feed stale/absent, watch it FIRE).
