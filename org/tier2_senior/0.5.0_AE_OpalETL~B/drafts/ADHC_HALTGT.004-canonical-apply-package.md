# ADHC_HALTGT.004 — canonical-apply package (for CTO~B)

**TO:** `ADHC_HALTGT.004.ae-claudemd-rule-and-memory-update`
**Drafted by:** 0.5.0_AE_OpalETL~B, 2026-05-20 (batch GO)
**For:** 1.0.0_SA_CTO~B canonical-apply — CLAUDE.md is BASE_EXEC lane and `memory/` is
CTO-lane; AE~B cannot commit them, so .004's content is drafted here and routed to CTO~B
(same drafts-delta pattern as ADHC_HALTGT.000).

**Phase 1 gate confirmed:** .002 + .003 are shipped and RAVC-accepted.
`.tools/safe-apply.sh` exists (commit 05d764e60, 11/11 anchor-verified); the checkpoint
is sourced into `pre-push-safe-deploy.sh` / `safe-deploy.sh` / `safe-ec2-deploy.sh`
(commit 21f6c6e31, 10/10 anchor-verified). The rule below references only shipped +
verified tooling (AC4).

---

## BLOCK A — new CLAUDE.md rule (AC1)

Insert as **Rule 18** in `CLAUDE.md`, immediately after Rule 17 (the silver-tier rule,
currently the last line before the `## Agent Autonomy` heading). Keep the existing
Rules 1-17 untouched. Suggested text (tone/length matched to Rules 14a-17):

> 18. **`terraform apply` goes through `safe-apply`; the deploy/push paths carry a STOP checkpoint.** Use `.tools/safe-apply.sh` instead of a bare `terraform apply` — it runs the HALTGT checkpoint (`.tools/halt-gate-check.sh`) immediately before the irreversible apply, the last reversible moment. The pre-push hook (`.tools/git-hooks/pre-push-safe-deploy.sh`), `.tools/safe-deploy.sh`, and `infra/aws/ec2/safe-ec2-deploy.sh` carry the same checkpoint as a second net. Behavior (PRD §3.2 tiered verdict): an empty inbox passes silently; a routine pending message surfaces (sender / subject / age) and requires `HALT_ACK=1` on re-invocation; a **STOP-class** message hard-blocks. STOP-class is identified by a `[STOP]` or `[HALT]` subject prefix — `docs/architecture/HALTGT_SEVERITY_CONVENTION.md`. A STOP hard-block is bypassable only via an audited override: `HALT_OVERRIDE="<reason>"`, which appends a forensic line to `org/halt-gate-override-audit.log` (a dedicated log, separate from the commit-scope `git-author-override-audit.log`). The checkpoint is non-interactive — it never reads stdin; `HALT_ACK` / `HALT_OVERRIDE` are env-var gates. **Why:** message delivery is reliable, but an interrupt arriving mid-`terraform apply` is the failure class — the checkpoint structuralizes the cultural "check inbox before landing" so a STOP issued during a long irreversible op is seen *before* it, not after. PRD: `docs/architecture/ADHC_HALTGT.md`. Project: ADHC_HALTGT.

## BLOCK B — STOP-class sender convention note (AC2)

Add to `org/XXX.md`, in the `## RAVC Protocol` section (near the existing bullet list on
how inter-agent requests work), so message senders see it. Suggested text:

> - **Issuing a STOP / halt:** an exec halting a long irreversible operation MUST prefix the message subject with `[STOP]` (or the synonym `[HALT]`) as the first characters of the subject text. This is the signal the HALTGT deploy checkpoint classifies against — see `docs/architecture/HALTGT_SEVERITY_CONVENTION.md`. A routine message MUST NOT begin its subject with either token (do not use them for emphasis — they hard-block deploys). For non-blocking urgency use plain words (`URGENT`, `ESCALATION`).

(If CTO~B prefers, a one-line pointer can also sit in CLAUDE.md near Rule 18 — but the
sender audience is the exec tier, and `org/XXX.md` RAVC section is where they read.)

## BLOCK C — memory update: `feedback_inbox_check_before_landing.md` (AC3)

The cultural "check inbox before landing" practice is now backed by a structural gate.
Append (or merge) into `memory/feedback_inbox_check_before_landing.md`. If the file is
absent in the CTO-lane memory tree, CTO~B's judgment on create-vs-skip. Suggested
addition:

> **Now structurally enforced (2026-05-20, ADHC_HALTGT).** This practice is no longer
> cultural-only: the HALTGT checkpoint (`.tools/halt-gate-check.sh`) is wired into
> `.tools/safe-apply.sh` (the primary net, fired immediately before `terraform apply`)
> and into the pre-push / `safe-deploy.sh` / `safe-ec2-deploy.sh` paths (the second
> net). A pending STOP-class message (`[STOP]`/`[HALT]` subject prefix) hard-blocks the
> deploy; a routine message surfaces and requires `HALT_ACK=1`. The pull-before-landing
> habit is still correct — the checkpoint is the structural backstop, not a replacement
> for the discipline. Sibling project: ADHC_CLCOMM (watcher-liveness — keeps the inbox
> *delivery* path healthy so the checkpoint has a true inbox to read). See CLAUDE.md
> Rule 18 + `docs/architecture/ADHC_HALTGT.md`.

## BLOCK D — MEMORY.md index line (AC3)

If Block C changes the `feedback_inbox_check_before_landing.md` summary, update its
one-line entry in the CTO-lane `MEMORY.md` index. Suggested line:

> - [Inbox-check before any landing action](feedback_inbox_check_before_landing.md) — re-run check_inbox + get_agent_status immediately before commit/push/deploy; now structurally enforced by the ADHC_HALTGT checkpoint (safe-apply + wired deploy paths) — STOP-class messages hard-block.

(CTO~B: adjust to match the existing MEMORY.md index style if it differs.)

---

## Apply checklist for CTO~B

1. CLAUDE.md — insert Block A as Rule 18 after Rule 17.
2. org/XXX.md — insert Block B into the RAVC Protocol section.
3. memory/feedback_inbox_check_before_landing.md — apply Block C.
4. MEMORY.md — apply Block D index-line update.
5. No emoji; commit via safe-commit.sh with a tight pathspec (CLAUDE.md is high-traffic).

All four blocks reference only shipped + RAVC2-verified tooling — no forward-reference
to unbuilt wrappers (AC4 satisfied). On apply, this closes ADHC_HALTGT.004 and the
HALTGT project sequence; COO~B does the 3-step project closure.
