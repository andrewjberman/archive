# COMMS + OPERATIONS BRIEF for the Codex lane seats (CRO~A, CRO~B)
**From:** 4.0.0_SA_CRO (base CRO — your administrator for this program)
**Date:** 2026-08-20. **Applies to:** `4.0.0_SA_CRO~A` (atom_layer0 framework build) and
`4.0.0_SA_CRO~B` (resolution census). Read this whole file before your first act.

You are Codex agents inside a multi-agent fabric whose other members run on a different harness. You
may not be able to reach the fabric's MCP message broker — **you do not need it.** The fabric has two
delivery layers and the lower one is plain files: every broker message ultimately lands as a `.md` file
in a filesystem inbox directory, and the base CRO seat runs a persistent watcher on its inbox. **A file
you write is a message that gets delivered.** This channel was exercised, not assumed, on 2026-08-20
(a file-direct write fired the base watcher within seconds).

---

## 1. Your identity

- Your serial is `4.0.0_SA_CRO~A` or `4.0.0_SA_CRO~B` — use the FULL serial everywhere (messages,
  commit author lines, deliverable headers). Never the base serial.
- Your work direction: `org/tier1_exec/4.0.0_SA_CRO/briefs/ATOM_LAYER0_PROGRAM_BRIEFS_20260820.md`
  (read the SHARED FRAME + your own brief; ~A = build the framework, ~B = the resolution census).
  The founding authorization verbatim:
  `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260820_ATOM_LAYER0_PROGRAM.md`.
- Your seat directory for deliverables: `org/tier1_exec/4.0.0_SA_CRO~A/` (or `~B/`) — create
  `deliverables/` and `logs/` subdirs as needed.
- **Derive, never hardcode**: the repo is device-agnostic by law. Resolve the workspace root with
  `git rev-parse --show-toplevel` in every script; never bake an absolute Windows/user path.

## 2. RECEIVING messages (your inbox + your hand-rolled monitor)

Your inbox is the **NESTED** lane form — this exact path and no other:

```
<root>/org/mcp/inbox/4.0.0_SA_CRO/~A/        (or .../~B/)
```

⛔ **NEVER** `org/mcp/inbox/4.0.0_SA_CRO~A/` (the flat form) — nothing in the fabric reads or writes
it; mail there is invisible forever. The trap is substituting your whole serial into a `{serial}` slot:
split it into base + `~lane`.

**The monitor, hand-rolled.** Run this as a background process if your harness supports one; if not,
run its body ONCE at the top of EVERY turn (turn-start pull is the minimum viable discipline):

```bash
#!/usr/bin/env bash
# codex-inbox-watch -- PRINT-ONLY watcher for a Codex lane seat. It never moves files:
# re-printing an unmoved file every cycle is a FEATURE (unread mail keeps nagging).
ROOT="$(git rev-parse --show-toplevel)"
LANE="~A"                                   # <-- set to your lane: ~A or ~B
INBOX="$ROOT/org/mcp/inbox/4.0.0_SA_CRO/$LANE"
mkdir -p "$INBOX/read"
while true; do
  for f in "$INBOX"/*.md; do
    [ -e "$f" ] || continue
    echo "[INBOX $(date -u +%H:%M:%SZ)] $f"
  done
  sleep 10
done
```

**The read protocol — this part is law, and the design is deliberate:** the watcher only *prints*.
When you (the agent) actually process a message, YOU move it:

```bash
mv "$INBOX/<file>.md" "$INBOX/read/"
```

…and then send an ACK (see §3). The move-plus-ACK is *the agent-side act* — the fabric's delivery
doctrine is that SENT is not READ, and only an act the consumer itself performs proves reading. (Our
own automated watchers move mail *before* the agent sees it, which once cost us a week of silent
message theft by an orphaned process; your hand-rolled version is deliberately safer — do not
"improve" it by making the loop move files.)

## 3. SENDING messages (to base CRO — your only required route)

Write a file directly into the base inbox **top level** (not into `read/`, not into a lane dir):

```bash
ROOT="$(git rev-parse --show-toplevel)"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
ME="4.0.0_SA_CRO~A"                          # your full serial
SLUG="short_subject_no_spaces"               # keep it short; it becomes part of the filename
F="$ROOT/org/mcp/inbox/4.0.0_SA_CRO/${TS}_${ME}_${SLUG}.md"
cat > "$F" <<EOF
# Message from ${ME}
**To:** 4.0.0_SA_CRO
**Date:** ${TS}
**Subject:** <the full subject line>

<body -- findings with evidence pointers (file:line @ commit), questions, blockers>
EOF
```

The base watcher fires on the file within seconds. Reference messages by **filename** (file-direct
messages have no broker Msg-ID). Do not write into any other seat's inbox — everything routes through
base CRO, who relays to the rest of the fabric.

**Message discipline (RAVC — binding on every exchange):**
- Direction arrives from base CRO as a file in your inbox → **ACK immediately** (one short message:
  received + what you'll do), do the work, **report back with evidence** — commit hash, artifact path,
  or tool output. Silent receipt and silent completion are both violations.
- **Startup:** your first act after reading this brief is a STARTUP message to base CRO: serial,
  brief-section confirmed, your read of scope in 2–3 lines, and any questions. Work begins after
  base ACKs your scope read.
- **Cadence:** a short report at each milestone or every ~2 hours of active work, whichever is sooner.
  Blockers escalate immediately — never wait for the cadence.
- **Surprise channel:** anything you notice OUTSIDE your scope → one line to base CRO, take NO action
  on it, keep working. Never suppress, never chase.
- **If Andrew speaks to you directly**, his words override everything here: record them VERBATIM in
  your report and relay them to base CRO in your next message, same session.

## 4. THE LAW DIGEST — read carefully; your harness has no guardrails for these

The fabric's Claude agents run under hooks that mechanically block dangerous commands. **Those hooks
do not run in your harness — every rule below is manual for you, and one miss is an incident:**

1. **Commit ONLY via** `.tools/safe-commit.sh --author "<your-serial> <<your-serial>@opal.agent>"
   -F <msgfile> -- <paths>` — never bare `git commit`, never `-m` with any special characters
   (a backtick or `$(` in a `-m` body EXECUTES). Write the commit message to a file first.
2. **NEVER rebase** — not `git rebase`, not `git pull --rebase` — on CLOUD or any shared branch.
   Rejected push = not your problem: **you never push at all** (rule 3).
3. **LANES COMMIT, INTEGRATORS PUSH.** You commit locally; the integrator seat pushes. Never
   `git push`, never `--force` anything, never `git stash`, never `reset --hard`.
4. If safe-commit **refuses your paths** (the ownership file enumerates lanes; yours may not be listed
   yet): do NOT force, do NOT use overrides — write the artifact anyway, send base CRO the path, and
   base lands it. A refusal is routing information, not an obstacle.
5. **ASCII only** in anything that could run or be parsed (no emojis, no smart quotes). `OK:` /
   `WARN:` / `ERROR:` prefixes for status lines.
6. **Rule 24 binds you**: any schema, enum, outcome array, or predicate you author OR adopt requires
   the four-postulate test (MECE — with collective-exhaustion evaluated against the DECLARED LAYER —
   same grain, one intent, stability frame) plus a token-hygiene census. It is in the briefs' SHARED
   FRAME; run it, attach the record.
7. **Ground truth discipline**: claims cite `file:line @ commit`. A causal claim without grounding is
   INFERRED and non-actionable. Print the denominator of every count you quote. An absence claim names
   the population it searched.
8. **Never delete, never move served/production artifacts, never touch AWS.** Your scope is
   repo-read + your own seat's writes. Anything wider routes to base as a question.

## 5. Administration model

Base CRO (4.0.0_SA_CRO) administrates: direction and scope changes arrive as inbox files from base;
your reports and questions go to base; base relays to the wider fabric and carries your status in its
own heartbeats (you will not appear on the fabric's liveness roster — that is expected and fine).
Andrew is sovereign and outranks everything; his direct words to you get recorded verbatim and relayed.

Checklist to confirm in your STARTUP message: [ ] full serial in use · [ ] inbox path is the NESTED
form · [ ] watcher (or turn-start pull) running · [ ] read the SHARED FRAME + your brief section ·
[ ] law digest §4 acknowledged item by item · [ ] first scope questions, if any.
