# BUILD SPEC — raw-grep file-corpus ban, gated to comp-find (shadow-log first)

**Authority:** Andrew-direct at the `0.0.0_AB_MSTR` terminal, 2026-08-27 ~20:22Z ("all recs
approved, just need to make sure the deny log is inobtrusive and doesnt slow down work") +
~20:2xZ ("I will personally have 0.8.0_AE_CloudComp build it and oversee them directly").
Ruling record: `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20260827_GREP_BAN_COMPFIND_GATE.md`
@3b5c7c3df9 (on origin). **The record's sequencing row routed the build to CTO — SUPERSEDED by
his later word: `0.8.0_AE_CloudComp` builds, Andrew oversees directly, Andrew ferries this spec.**

**Builder:** `0.8.0_AE_CloudComp` (seat/lane per Andrew's direction at handoff).
**Overseer:** Andrew personally. MSTR holds the record and lands the Rule 21 law edit at arming.

---

## 0. Objective, one paragraph

Convert the comp-rail's advisory nudge into a mechanical gate for exactly the class where raw
grep fails and comp-find is strictly better: **file-corpus content search over the tracked repo**.
Ship it in two phases: a **shadow (log-only) window** that is invisible to every seat and costs
zero latency, then — after the shadow log is read for would-break classes — the **armed deny**
(rc=2 refusal naming comp-find). A third, non-blocking workstream extends comp-find's corpus so
the escape hatch shrinks over time.

## 1. Measured facts the design rests on (re-verify any you rely on)

- **comp-find's corpus is TRACKED FILES ONLY** (measured 2026-08-27 at this device):
  `comp-find "comp-find" org/mcp/comp-tool-runs.jsonl` (gitignored, content known present) →
  `0 hit(s) across 0 file(s)`; `comp-find "bridge" .runtime/` → same. **The `across 0 file(s)`
  denominator is the out-of-corpus tell** — the refusal text must teach it (§4).
- **Grep is plumbing in 62 `.tools/*.sh` + 8 `org/mcp/*.sh` scripts** — the gate binds the
  AGENT-INVOCATION layer (hook on the Bash/Grep tools), never grep-as-subprocess inside scripts.
- **The existing hook already has the exemption grammar**: `.tools/hooks/comp-tool-hud.sh`
  (333 lines) — pipe-receiver exemption (:81–88), single-file heuristic (path ends in extension,
  :98), comp-reference (:99), operational-aws (:100), corridor carve-outs (:109, :114), and the
  global FAIL-SAFE ("any jq/parse issue -> silent exit 0", :23).
- **NOT verified by the spec author, builder must check at source:** where the CURRENT hard-deny
  limbs live (CLAUDE.md Rule 21 names raw-aws-inspection + `infra/*.tf`-grep denies;
  `rail-checked` appears in both `comp-tool-hud.sh` and `never-rules-gate.sh`). Read both before
  extending; put the new classifier beside the existing deny, not in a third place.

## 2. The deny class (precise, both tool surfaces)

DENY-CLASS = a search invocation over a repo file-corpus, i.e.:

**(a) Bash tool:** leading (or `&&`/`;`-chained leading) invocation of
`grep|rg|egrep|fgrep|ack|ag|findstr` whose target is a DIRECTORY, GLOB, or `-r/-R/--recursive`
sweep inside the workspace. Leading = the search IS the command, per the existing :68–74 logic.

**(b) Native `Grep` tool:** calls whose `path` is a directory or unset (= workspace root) —
i.e. corpus sweeps. (The hook already receives tool names; extend its match beyond Bash.)

**CARVE-OUTS (all measured load-bearing — a hit on any = NOT deny-class):**
1. **Pipe-receiver** — `cmd | grep ...` filtering live stdout (`ps -ef | grep`, `git log | grep`).
   No comp substitute exists. Keep the existing :81–88 detection.
2. **Single named file** — target path ends in a file extension (:98 heuristic). Reading one
   file's internals is not a sweep.
3. **`# rail-checked: <why>`** inline marker — the existing audited override, unchanged.
4. **`# rail-checked: non-indexed-corpus <why>`** — the NEW named escape for
   gitignored/untracked/runtime/temp targets, where comp-find structurally cannot answer (§1).
   Same mechanics as (3); the distinct prefix makes the escape countable in the audit.
5. **comp- reference in the command** (:99) — already on the rail.

## 3. Phase 1 — SHADOW MODE (build first; this is the deliverable Andrew oversees)

**The constraint, his words: "inobtrusive and doesnt slow down work." Operationalized:**

- The hook classifies; on DENY-CLASS it appends **one JSONL line** to a **device-local,
  gitignored** shadow log and **exits 0 with ZERO bytes of stdout/stderr** — no nudge change, no
  refusal, no visible difference to any seat.
- **Latency bound:** the classifier is pure bash string tests on a string already in hand + one
  `>>` append to a local file. No new subprocess beyond what the hook already spawns, no network,
  no locking (single-line O_APPEND writes under PIPE_BUF are atomic enough for a measurement
  window; do NOT add flock — Git Bash 3.6.7 has none, per the bash-utilities law).
- **Fail-safe posture is law:** any classifier/parse error → silent exit 0. NEVER block or slow a
  search in shadow mode. (Same posture the hook already declares at :23.)

**Shadow log:** `org/grep-ban-shadowlog.jsonl` + a `.gitignore` entry (device-local by design;
site Z accumulates its own via normal hook parity). Line fields:
`{ts, serial, tool, cmd (first 300 chars), verdict: "WOULD_DENY", carveout: "none"}` — and, cheap
and worth it, also log carve-out HITS (`verdict: "CARVEOUT", carveout: "<name>"`) so the window
read can see the ratio, not just the numerator.

**Window:** 24–48h from landing. **Window read:** classify the WOULD_DENY lines; any legitimate
class the deny would break goes to Andrew before arming. The read is the arming gate.

## 4. Phase 2 — ARM (only after the window read; flip, don't rebuild)

- One switch (env var or a constant at the top of the hook, e.g. `GREP_BAN_MODE=shadow|deny`),
  so arming is a one-line change against an already-exercised classifier.
- Armed behavior on DENY-CLASS: **rc=2 refusal**, zero side effects, message naming the remedy:
  ```
  BLOCKED: file-corpus grep is gated to comp-find (Andrew-direct 2026-08-27).
    -> comp-find '<pattern>' <path>   (denominator + bands + paging; see comp-find --help)
    -> non-indexed target (gitignored/untracked/.runtime/temp)? re-run with
       '# rail-checked: non-indexed-corpus <why>' -- comp-find cannot see those files,
       and a comp-find zero reading 'across 0 file(s)' is OUT OF CORPUS, not absence.
  ```
- Still logs to the shadow log (now as `verdict: "DENIED"`) — the audit continues past arming.
- `/freeform` stands the rail down, unchanged. Refusals must never fire in freeform sessions —
  verify the hook's existing freeform handling covers the new limb.
- **MSTR lands the Rule 21 law edit in the same window as arming** (three surfaces: commit +
  same-turn broadcast + push state). The law must not describe an unarmed gate — do not land the
  text early.

## 5. Phase 3 — comp-find corpus extension (commissioned, NON-BLOCKING)

`--corpus all` (or equivalent flag): extend the sweep to untracked + gitignored files on request.
Default stays tracked-only. The DENOMINATOR line must print the corpus mode so a reader can tell
which population a zero certifies. When this lands and is exercised, the `non-indexed-corpus`
escape narrows; retiring it is a later Andrew/law decision, not automatic.

## 6. Acceptance criteria (machine-checkable; run at the builder's seat, report numbers)

Shadow mode:
- **AC-1 (both arms, from different truths):** a 6-command battery — 3 DENY-CLASS
  (`grep -rn foo org/`, `rg foo data/`, native Grep with dir path) + 3 carve-outs
  (`ps -ef | grep foo`, `grep foo org/XXX.md`, `grep -rn foo org/ # rail-checked: x`) —
  produces EXACTLY 3 `WOULD_DENY` lines + 3 `CARVEOUT` lines, exit 0 on all six, **0 bytes
  stdout** on all six.
- **AC-2 (latency):** median hook wall-time over 20 runs of a DENY-CLASS command, shadow vs
  hook-disabled baseline: delta < 25ms. Print both medians.
- **AC-3 (fail-safe):** malformed hook input → exit 0, no log line, no output.
- **AC-4 (mutant):** with the append target unwritable, a DENY-CLASS command still exits 0
  silently (the log is best-effort; work never waits on it).
Armed mode (exercised in a scratch check, not left armed):
- **AC-5:** DENY-CLASS → rc=2 + the §4 message; all 3 carve-outs unchanged; the
  `non-indexed-corpus` marker passes on a gitignored target.

## 7. Builder hazards (banked, save yourself the rediscovery)

- Git Bash 3.6.7 default utilities only; `.tools/jq.exe` is the vendored jq — resolve it the way
  the hook already does. No non-ASCII in output.
- Never `2>/dev/null` a read whose emptiness carries a verdict (the shadow log read at window
  close especially).
- The hook runs on EVERY Bash call — every branch you add is on the hot path; string tests before
  any subprocess, and bail early on the cheap non-matches (the existing code's shape).
- MSYS argv mangling: if a probe misbehaves, echo the received argument back before diagnosing.
- Do not touch the existing nudge/deny limbs' behavior — this is an ADDITIVE limb beside them;
  re-run whatever self-exercise the hook carries for the old limbs after editing.

## 8. What this spec deliberately does NOT include

- No Rule 21/CLAUDE.md edit (MSTR's, at arming — §4).
- No retirement of comp-find's own trap catalogue (predicate audit, denominator-certifies-the-
  sweep, page-1) — those survive the ban and stay in law.
- No site-Z-specific work: the hook + gitignore travel by normal parity; shadow logs are
  per-device by design.
