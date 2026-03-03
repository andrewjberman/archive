# Thread System — Knowledge Items & Best Practices

This document captures lessons learned from running agent threads. It is a
living record — append new items as patterns emerge or failures are diagnosed.

**Who must read this:** Any agent or human creating or configuring a thread.
Read this before writing a CONTEXT.json or opening message.

---

## MANDATES (non-negotiable)

### M1 — Inject actual source files for knowledge-bearing agents

**Rule:** When an AE or DT is a thread participant and will be asked about
pipeline behavior, their actual source files MUST be in the CONTEXT.json.
READMEs alone are not sufficient.

**Why:** In the first DS/AE pilot thread (2026-03-02), AE PartnerETL produced
plausible-sounding but fabricated answers — invented EventBridge schedules,
made-up S3 key patterns, fictional field names — because only the portal
endpoint file was injected. AE was answering from inference, not from code.

**Minimum context for AE/DT threads:**
- The Terraform file that owns the relevant EventBridge rules (`eventbridge.tf`)
- At least one Lambda `lambda_function.py` for each producer being discussed
- The source map entry if deployment state matters (`lambda-source-map.json`)

**Example (bespoke CONTEXT.json):**
```json
{
  "code": [
    { "label": "EventBridge rules", "path": "infra/aws/terraform/bd-pipeline/eventbridge.tf" },
    { "label": "Advisor publisher Lambda", "path": "infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py" },
    { "label": "Portal endpoint contract", "path": "portal/src/api/endpoints/advisor-intelligence.ts" }
  ]
}
```

---

### M2 — DS agents must be instructed to push back on vague answers

**Rule:** The opening message for any DS ↔ AE thread must explicitly instruct
the DS to request a file path or code reference if an answer is not grounded
in a specific file, resource name, or line of code.

**Why:** In the pilot thread, DS accepted all of AE's fabricated answers at
face value and moved immediately to "I'll write the XML now." There was zero
skepticism. The DS needs permission and direction to push back.

**Add to DS opening message:**
```
If any answer references a Lambda function, S3 path, EventBridge rule, or
field name without citing a specific file or resource, ask AE to confirm
the exact location. Do not treat an answer as ground truth until it is
anchored to a real file path or AWS resource name.
```

---

### M3 — Model selection: use gpt-5.2 until chat-compatible variants confirmed

**Current safe default:** `--model gpt-5.2` for ALL thread types.

**Intended split (pending confirmation of chat-compatible model IDs):**
- Code-grounded threads (Pattern 0, Pattern 2): codex-class model
- Planning/coordination threads (Pattern 1, Pattern 3): pro-class model

**WARN — gpt-5.3-codex and gpt-5.2-pro are NOT usable until verified:**
The orchestrator calls `client.chat.completions.create()`. gpt-5.3-codex is a
completions-only model, incompatible with this endpoint. First live run (2026-03-03)
confirmed the failure and reverted to gpt-5.2. Do not configure these model strings
again until a chat-endpoint-compatible ID is confirmed by Andrew.

**Why the split matters:** Code-grounded threads read Lambda source, TypeScript,
and gold scripts where codex-class reasoning is significantly better. Planning
threads reason over prose logs and specs where pro-class is sufficient.

---

### M4 — Bespoke thread CONTEXT.json must include an inline briefing

**Rule:** Every bespoke thread must have an `inline` field in CONTEXT.json
that states: (1) the goal of the conversation, (2) what deliverable the
receiving agent will produce, and (3) which agent is the knowledge source vs.
the knowledge receiver.

**Why:** Without framing, agents default to generic professional behavior
rather than playing their specific roles in the knowledge transfer. The inline
briefing anchors both agents to the purpose.

---

### M5 — max-turns 3 for bespoke, 2 for exploratory

**Rule:**
- Bespoke threads: `--max-turns 3` (6 messages total including opening)
- Exploratory sync threads: `--max-turns 2` (4 messages total including opening)

**Why:** In the pilot, turns 4 and 5 were both convergence summaries that
added no new information — they just restated what had been said. The
productive content fit in turns 1-3. Exploratory syncs need even less — the
goal is surfacing cross-dependencies, not deep investigation.

---

### M7 — Pre-injected local context is the primary signal; tools are the fallback

**Rule:** Thread context should be anchored in what agents have actually done —
session logs, recent commits, deployment tags, task orders. This is pre-loaded
at thread creation time with zero API overhead and represents the highest-signal,
most specific knowledge each agent has. Tools (read_file, grep_content) exist
for specific factual gaps, not as the primary research mechanism.

**What is auto-injected per participant (create-thread.sh):**
- `README.md` — identity, scope, permissions, key paths
- Most recent session logs — what they worked on, decisions made, next steps
- Pending task orders — what they have been asked to do
- Recent commits by serial — `git log --grep="{serial}" -20` (actual shipped work)
- Deployment tags (AE/DT only) — `git tag --sort=-creatordate` (what was deployed, when)

**Commit injection note:** Commits are matched by agent serial in the commit message.
This requires agents to follow the commit tag format (`{serial}: description`).
Agents who do not tag commits will have empty commit context. Session logs are the
fallback signal in that case.

**When tools ARE appropriate:** an exact cron expression, a specific S3 key pattern,
a field name buried in Lambda source — facts that were not captured in logs because
they were not the subject of decision-making, just implementation detail.

**When tools are NOT appropriate:** anything the agent's own logs describe, any
deployment outcome captured in a git tag, any task order status. If it's in the
pre-injected context, do not call a tool to confirm it.

---

### M6 — Use tool-enabled runs for AE/DT agents; --no-tools for pure sync threads

**Rule:**
- Bespoke threads where AE or DT is answering technical questions: run with tools
  enabled (default). Agent will read the actual source files it needs.
- Exploratory sync threads (recent work summaries, cross-dependency awareness):
  run with `--no-tools`. Logs and READMEs are pre-injected; no file reads needed.

**Why:** Tool use adds API round-trips per tool call. For exploratory threads the
auto-injected context is sufficient. For bespoke technical threads, tool access
is what makes the difference between grounded and fabricated answers.

**Available tools (always on unless --no-tools):**
- `read_file(path)` — reads a file relative to repo root (50K char limit)
- `glob_files(pattern)` — finds files matching a glob pattern
- `grep_content(pattern, path)` — searches for a string/regex within a file or dir

**Limit:** 10 tool calls per turn (hard cap). If an agent hits the limit,
it is forced to produce a final answer from what it has already read. If you
see the WARN log, the CONTEXT.json was under-specified — add the key files
explicitly so the agent finds them in 1-2 reads rather than hunting.

**run-exploratory.sh** passes `--no-tools` automatically. The bespoke pattern
(orchestrator.py invoked directly) uses tools by default.

---

### M11 — Agents must self-unblock using tools before the final turn

**Rule:** An agent may not surface an unresolved caveat in the final turn (signal:
converge) if the caveat is answerable by reading a file. If DS is uncertain about
a data field, parquet date range, script behavior, or output shape — they must
READ the relevant file during the thread and resolve the question before writing
the final contract block. A hedged receipt is a failed receipt.

**Why:** ADVI-005 (2026-03-03) closed with "we are not guaranteeing 3Y/Max visual
completeness for rolling_1y until DS inspects actual parquet min/max dates."
Script 10 is a local file. The date range was readable in the thread. DS had tools
enabled. The hedge was unnecessary — the question was answerable in 1 tool call.

**Add to every DS/AE bespoke opening message:**
```
If you are uncertain about a data field, date range, output shape, or script
behavior: read the relevant file during this thread and resolve the question
before your final turn. Do not close the thread with a caveat that file
inspection would answer. You have tool access — use it.
```

**What counts as an acceptable blocker (not a tool-resolvable caveat):**
- Missing infrastructure that does not exist yet (e.g., gold layer lacks a join key)
- S3 data content that requires a live query (not readable from scripts alone)
- A design decision that requires Andrew's business input

**What is NOT acceptable as a receipt caveat:**
- "We need to check the date range" — read the script and check it now
- "We need to verify the field name" — read the Lambda and confirm it now
- "DS should investigate X before implementation" — DS is in the thread, investigate now

---

## OBSERVATIONS (patterns to be aware of)

### O1 — Agents strip code fences from frontmatter in GPT-4o-mini responses

**Observed:** In the pilot, gpt-4o-mini wrapped the YAML frontmatter in a
markdown code block (` ``` `). The signal parser regex handles this correctly
since it matches `signal:` anywhere in the file. However, the message file
itself will contain code fence markers at the top rather than raw frontmatter.

**Impact:** Cosmetically ugly in thread receipts. Does not break parsing.
**Mitigation:** The opening message template already demonstrates bare
frontmatter without code fences. If this persists, add an explicit constraint:
"Do not wrap the frontmatter in a code block — write it as raw YAML at the
start of your response."

---

### O2 — Convergence triggers on max-turns exhaustion, not double-converge

**Observed:** In the pilot, DS signaled `converge` on turn 4 (their last turn)
and AE signaled `converge` on turn 5 (their last turn). The loop detected
"all agents exhausted max turns" BEFORE it could detect the double-converge
pattern (because the convergence check runs at the TOP of the next iteration,
which never happens after the last turn).

**Impact:** Thread completes correctly either way. Receipts are written in
both paths. Not a bug, just a sequencing note.

---

### O3 — Exploratory threads produce lower-quality output when logs are sparse

**Risk:** The exploratory thread relies entirely on auto-injected session logs
for context. If an agent has no recent logs (e.g., a freshly activated agent),
the opening message will reference logs that don't exist and the conversation
will be vacuous.

**Mitigation:** Before running an exploratory thread with a new agent, verify
they have at least one session log. If not, run a bespoke orientation thread
first to seed their knowledge, THEN run exploratory syncs.

**IMPORTANT — O3 applies to EXPLORATORY threads only, not BESPOKE threads:**
Bespoke threads (orchestrator.py with TOOLS_ENABLED=true and M1 context injection)
do NOT require session logs to produce quality output. The agents have:
  (1) Their enriched prompt.md as system context
  (2) M1 file injection — source code injected directly into the thread context
  (3) Tools access — agents can read any file during the thread run
  (4) v1 session logs accessible via logs/sessions/ fallback (84 logs, 2025-11-18)
O3 is therefore already satisfied for any agent with an enriched prompt.
Do NOT block a bespoke thread because an agent lacks recent new-system session logs.

---

## WORKFLOW REFERENCE

### Creating a bespoke thread

Describe the thread in natural language to Claude Code. It will generate a
self-contained run script at `org/threads/staging/run-YYYY-MM-DD-{slug}.sh`
with the CONTEXT.json and opening message embedded as heredocs. You run it once:

```bash
bash org/threads/staging/run-2026-03-02-ds-ae-pipeline-intake.sh
```

The script scaffolds the thread and runs the orchestrator in one shot. After it
completes, the thread folder and receipt files are the permanent record --
the run script can be deleted or kept as documentation of how the thread was set up.

See `org/threads/staging/BESPOKE_TEMPLATE.sh` for the expected format.

**When describing the thread to Claude Code, specify:**
- Which agent is the knowledge source and which is the receiver
- What specific files or terraform resources are relevant (for M1 compliance)
- What deliverable the receiving agent will produce from the conversation

### Creating an exploratory sync

```bash
./org/threads/run-exploratory.sh <agent1-serial> <agent2-serial>
```

Verify both agents have recent session logs before running. Use default
`gpt-5.2` model.

### Adding a new knowledge item

Append to this file under the appropriate section:
- **MANDATES** — if it is a rule that must always be followed
- **OBSERVATIONS** — if it is a pattern or risk to be aware of

Format: short title, rule/observation statement, why it matters, mitigation
or example if applicable. Date-stamp entries if helpful for traceability.

---

---

### M8 -- Task orders from project threads inherit the thread serial as filename prefix

**Rule:** When the COO writes task orders as a direct result of a project thread,
the task order filename is prefixed with that thread's serial:

```
{agent_folder}/task_orders/{CODE}-{NNN}-{feature_slug}.md
```

Example: thread `ADVI-004` produces task orders:
- `0.4.0_DS_ClientPlatform/task_orders/ADVI-004-adv_drill.md`
- `0.4.0_DE_ClientPlatform/task_orders/ADVI-004-continuous_nna_rendering.md`
- `0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-004-continuous_nna_rendering.md`

The task order XML `<metadata>` also includes:
```xml
<thread_serial>ADVI-004</thread_serial>
<thread_ref>org/threads/ADVI-004-{slug}/</thread_ref>
```

**Why:** The thread serial is the only join key needed. It links the task order back
to the thread receipt (which contains the agreed data contract) and to the project file
(which tracks all threads). No separate task order numbering system needed.

**When NOT to prefix:** Ad-hoc task orders from DE to RD, or any task order not
directly spawned from a formal project thread, keep the plain feature slug filename.

---

### M9 -- Pre-implementation alignment threads run BEFORE task orders, not after

**Rule:** For any work stream where DS output feeds DE wiring feeds RD layout,
the COO must run a 3-party alignment thread (Pattern 0) BEFORE writing the
task orders for that stream. The thread receipt is the data contract. Task orders
reference the receipt as the binding interface specification.

**Why:** Without the alignment thread, DS produces a reasonable shape, DE types
against it, RD builds layout around the types, and they discover the mismatch
in code review. The Pattern 0 thread forces the DS/DE/RD contract conversation
to happen BEFORE anyone writes code. This eliminates the most common rework cycle.

**What the thread produces:**
- DS commitment: "I will produce {exact JSON shape} at {S3 key} on {schedule}"
- DE commitment: "I will type against {TypeScript interface} via {query key} at {endpoint}"
- RD commitment: "My component expects {field names} in {format} for {chart/layout}"

**Thread configuration for Pattern 0:**
- Participants: DS + DE + RD (3-party)
- turn_order: round_robin
- Model: gpt-5.2 (bespoke, tools enabled)
- Max turns: 3
- CONTEXT.json: PRD section, types.ts, current tab component, current Lambda/script
- Opening message structure: DS goes first describing available data -> DE responds
  with interface need -> RD responds with layout constraints -> converge on contract

---

### M10 — All threads belong to a project. Use --project when creating threads.

**Rule:** Every thread created for a feature or initiative must reference a project
via `--project {CODE}`. The project code is the join key between threads, task orders,
PRDs, and agent receipts.

**Project registry:** `org/projects/REGISTRY.md` lists all active projects.
Each project has a JSON file at `org/projects/{CODE}.json` containing the PRD path,
pod scope, and a log of all threads run under it.

**Serial format:** `{CODE}-{NNN}` (e.g., `ADVI-004`). Auto-assigned by `create-thread.sh`
when `--project` is passed. Thread folder: `org/threads/ADVI-004-{slug}/`.
Receipt in agent folder: `ADVI-004-{slug}_{other_serials}.md`.

**Why:** Without project linkage, thread receipts accumulate in agent folders with no
searchable structure. With project codes, any agent can filter their `threads/` folder
by code (`ls threads/ADVI-*.md`) to find all threads related to a specific feature.
The project JSON file gives the COO a single-file audit of every thread run for a project.

**To create a new project:** Add `{CODE}.json` to `org/projects/` (copy ADVI.json as template)
and add a row to `org/projects/REGISTRY.md`. Then pass `--project {CODE}` to any
`create-thread.sh` call and it auto-assigns the serial and updates the project file.

*Last updated: 2026-03-03*
*Updated by: 1.0.0_SA_CTO + Andrew (CEO) -- project serial system added*
