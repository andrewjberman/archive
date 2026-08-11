# OPAL_ANALYST.TO6 — teams-watch expired-token QUIET RETRY, holding the identity pin

<task_order>
<id>OPAL_ANALYST.TO6</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-11</date>
<status>staged</status>
<priority>P2</priority>
<!-- SEQUENCING: runs NOW, in parallel with W0 and W1 prep. CTO~Z sequencing call recorded in
     PRD §9.9 -- MSTR~Z had queued this behind the program "unless CTO~Z sequences it otherwise."
     It is small, source-confirmed, and it removes an hourly watcher death on the concierge seat
     this entire program exists to serve; carrying that death through six waves costs more than
     the fix. Small enough to interleave with W1 prep; if it ever competes with a W1 run for your
     attention, W1 wins and this waits. -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §4.1 (IO contract) + §9.9 (sequencing call) — v1.3 @f57c2a1642</ref>
  <ref type="prior">OPAL_ANALYST.TO1 (complete) — the identity pin this TO must not regress; fix @0f1bbcf0e</ref>
  <ref type="source">`.claude/skills/teams-assist/teams-watch.py` :103, :119-121, :250, :273 @0f1bbcf0e (BG source-confirmed, relayed 20260811T163119Z)</ref>
</references>

<scope>
**The defect:** an expired token makes the watcher **exit 2**. On the concierge seat that means a
watcher death roughly hourly, each one requiring a relaunch to restore reachability — and per the
PRD §2 reliability posture, **nothing is monitoring for it**, so the seat simply goes quiet until
someone notices.

**The fix:** on an expired token, **QUIET-RETRY** — hold the pinned identity and keep polling
until the token refreshes — instead of exiting. Silent on the no-op; the retry is a recovery path,
not an event to announce.

**⛔ THE BINDING CONSTRAINT, AND IT IS THE WHOLE RISK OF THIS TO: THE IDENTITY PIN MUST SURVIVE THE
RETRY.** TO-1 closed a P0 in which the engine selected the freshest-expiring token across ALL
`mcpOAuth` records and, with both identities valid on this box, historically picked Andrew's. **A
retry path that re-enters token selection WITHOUT the pin filter reintroduces exactly that P0 —
and does it on a code path that only fires on expiry, which is to say rarely, unattended, and
long after anyone is watching.** A bare arm is still identity-blind at source; the pin is opt-in
by design. **The retry must re-apply the filter every cycle, never cache a resolved token past
its expiry, and never fall back to another identity.**

Out of scope: any change to bare-invocation behavior (the engine is SHARED with Andrew's operator
`/teams-assist`); any wrapper (the `teams-watch-bbg.py` pattern is dead by design).
</scope>

<requirements>
  <requirement id="1">Expired token → **quiet retry with backoff**, holding the pinned identity. No `exit 2` on expiry alone.</requirement>
  <requirement id="2">**The pin filter is re-applied on every retry cycle.** No caching a resolved token past expiry; no widening the record set on retry; no fallback to another identity, ever.</requirement>
  <requirement id="3">**A genuinely unsatisfiable pin still fails LOUD** — no token for the pinned identity that is not merely expired-and-refreshable, or an ambiguous multi-match after filtering, exits non-zero with a named reason. Quiet-retry must not become a silent hang that looks like health. *A watcher that retries forever on an impossible condition is worse than one that dies, because the death was at least legible.*</requirement>
  <requirement id="4">**Bare invocation (no pin flag) keeps byte-identical current behavior** — the operator's `/teams-assist` must not change.</requirement>
  <requirement id="5">**No wrapper, no shadow path, no parallel watcher.** Fix the engine.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` for consumer discovery — re-confirm the engine's downstream consumers before changing shared-engine behavior (`/teams-assist` operator skill + `/bbg-teams-assist` concierge).</before_write>
  <before_commit>`.tools/commit-gate.sh` on `teams-watch.py` (py_compile + ruff, universal Rule-14 gate).</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json --expected-criteria C1,C2,C3,C4,C5,C6`</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **0.0.3_BG_BBGTerminal** — the consumer seat. Their relaunch runbook (`refs/RELAUNCH.md`) and the `/bbg-teams-assist` arm line may need a line if operator-visible behavior changes; if they do, say so rather than editing another seat's core refs unilaterally.
- **Shared engine:** `.claude/skills/teams-assist/teams-watch.py` is shared with Andrew's operator skill. Requirement 4 is the compatibility contract.
- **Do not push.** Lane commit; MSTR~Z integrates.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">**Expired-token quiet retry EXERCISED, not reasoned:** an actually-expired token produces a retry and a subsequent successful poll, with the observed evidence quoted. A source read showing a retry branch does not satisfy this — behavior claims are exercised (Rule 22a).</criterion>
  <criterion id="C2">**NEGATIVE CONTROL — the pin survives the retry.** With both identities' tokens present on the box and the pinned one expired, the post-retry poll runs as the PINNED identity. Evidence must show WHICH identity polled, not merely that polling resumed. *"The process stayed up" is not this criterion; it is the failure mode this criterion exists to catch.*</criterion>
  <criterion id="C3">**Unsatisfiable pin still exits non-zero with a named reason** — exercised, distinguishable from the retry path.</criterion>
  <criterion id="C4">**Bare-invocation compatibility exercised** — no pin flag, selection behavior unchanged vs pre-change baseline, with the comparison stated.</criterion>
  <criterion id="C5">**No wrapper / shadow path / second watcher introduced** — stated, and verifiable from the diff.</criterion>
  <criterion id="C6">**Session log with a populated Compiler Tools section**, commit on your own lane under your own author line.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/OPAL_ANALYST.TO6_PROOF_OF_SPEC.json</instance_path>
  <!-- C2 is the criterion this TO exists for. Record it as a CONTROL, not just an acceptance row:
       an assertion that the pin holds, which has never been run against an actually-expired token,
       has never been tested -- and the P0 it guards fires only on a rare unattended path. -->
</proof_of_spec>

<deliverables>
  <deliverable type="commit">`teams-watch.py` expired-token quiet-retry holding the pin</deliverable>
  <deliverable type="document">`OPAL_ANALYST.TO6_PROOF_OF_SPEC.json`, validator-clean against C1-C6</deliverable>
  <deliverable type="document">Session log with Compiler Tools section</deliverable>
</deliverables>

<do_not>
  <rule>**Do NOT let the retry path bypass the pin filter** — the single failure this TO must not ship.</rule>
  <rule>**Do NOT build a monitor, alarm, or watchdog around the watcher** (moratorium). The fix is the retry; detection machinery is not the deliverable.</rule>
  <rule>**Do NOT recreate a wrapper or stand up a second watcher process** (no-shadow veto).</rule>
  <rule>**Do NOT change bare-invocation behavior** — Andrew's operator skill shares this engine.</rule>
  <rule>**Do NOT push.**</rule>
</do_not>
</task_order>
