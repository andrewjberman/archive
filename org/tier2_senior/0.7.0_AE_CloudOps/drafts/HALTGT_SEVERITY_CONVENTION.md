# HALTGT Severity Convention — STOP-Class Message Identification

**Status:** ACTIVE — 2026-05-20
**Owner:** 0.7.0_AE_CloudOps (ADHC_HALTGT lane)
**TO of record:** ADHC_HALTGT.000
**Consumed by:** ADHC_HALTGT.001 (checkpoint classifier), ADHC_HALTGT.004 (folds sender guidance into CLAUDE.md / org docs)

---

## Purpose

The HALTGT checkpoint fires at deploy time during a long, irreversible operation. For
each pending inbox message it must decide, deterministically, whether the message is
**STOP-class** (hard-block the operation, require explicit operator clearance) or
**routine** (surface + ack, do not block). This document is the contract that decision
is made against. ADHC_HALTGT.001 transcribes the match rule below directly — it makes
no independent judgment.

Per CTO~B §7-Q1 ruling: STOP-class is identified by a **subject-line prefix
convention** — a reserved token at the start of the message subject. This requires zero
MCP server change and is shell-greppable. The alternative (a `severity` field on
`send_message`) is explicitly deferred; revisit only if this convention proves leaky.

## Message file format (confirmed Phase 1)

Every delivered MCP message file under `org/mcp/inbox/` is markdown and carries a
single-line subject field on line 4:

```
**Subject:** <subject text>
```

Phase 1 inspection: all 15,258 message files in `org/mcp/inbox/` carry exactly one
`**Subject:**` line. The subject is reliably present and single-line — it is a sound
signal for the convention.

## The convention

| Property | Specification |
|----------|---------------|
| **Token set** | `[STOP]` and `[HALT]` — exactly these two, including the square brackets. |
| **Position** | The token must be the **start of the subject text**, after the `**Subject:**` field marker and any optional leading whitespace. A token anywhere else in the subject does NOT classify the message as STOP-class. |
| **Case** | Case-sensitive. Uppercase only. `[stop]`, `[Stop]`, `[Halt]` do NOT match. |
| **Bracket-required** | The literal square brackets are mandatory. Bare words `STOP`, `HALT`, `URGENT`, `ESCALATION` — including the legacy freeform-emphasis prefixes already in the corpus — are NOT STOP-class. The brackets are what makes the token a deliberate, unambiguous signal rather than a stylistic choice. |

## Match rule (the classifier contract)

A shell classifier extracts the `**Subject:**` line from a message file and applies
this exact `grep -E` pattern. The pattern is **canonical** — ADHC_HALTGT.001 transcribes
it verbatim.

**Against the full subject line** (as it appears in the file):

```
^\*\*Subject:\*\* *\[(STOP|HALT)\]
```

Exit 0 (match) = STOP-class. Exit 1 (no match) = routine.

Reference invocation:

```sh
grep -m1 '^\*\*Subject:\*\*' "$msg_file" | grep -qE '^\*\*Subject:\*\* *\[(STOP|HALT)\]'
```

Equivalent rule if the classifier has already stripped the `**Subject:** ` marker and
holds only the subject text:

```
^[[:space:]]*\[(STOP|HALT)\]
```

`grep -E` is case-sensitive by default — do NOT pass `-i`. The ` *` (full-line variant)
and `[[:space:]]*` (text variant) absorb optional leading whitespace after the marker.

## Sender guidance (for execs issuing messages)

- An exec issuing a halt or STOP-class directive **MUST** prefix the message subject
  with `[STOP]` or `[HALT]` as the first characters of the subject text. Use `[STOP]`
  for "stop the operation now"; `[HALT]` is an accepted synonym for the same class.
- A routine message **MUST NOT** begin its subject with either token. Do not use the
  bracketed tokens for emphasis — they are a hard-block signal, not a priority marker.
  For urgency that is not a hard-block, use plain words (`URGENT`, `ESCALATION`) which
  the classifier correctly treats as routine.
- The token is start-of-subject only. A reply or status update *about* a STOP (e.g.
  `Re: [STOP] ...`) is not itself a hard-block and must not lead with the token.

## Worked examples

| # | `**Subject:**` line | Classification | Why |
|---|---------------------|----------------|-----|
| 1 | `**Subject:** [STOP] auth-validator-edge rollback in progress — do not deploy` | **STOP-class** | `[STOP]` at start of subject text. |
| 2 | `**Subject:** [HALT] mdpf chain mid-apply — hold all S3 uploads` | **STOP-class** | `[HALT]` at start; accepted synonym token. |
| 3 | `**Subject:** RAVC2 ACCEPT — ADHC_DSFLOW.007 executing` | routine | No bracketed token. |
| 4 | `**Subject:** URGENT -- Books tab empty: dashboard.json is split` | routine | `URGENT` is a bare emphasis word, not a bracketed token. Legacy freeform prefixes are NOT STOP-class. |
| 5 | `**Subject:** chain done; see [STOP] thread for context` | routine | `[STOP]` present but not at start of subject — position rule fails. |
| 6 | `**Subject:** [stop] hold the deploy` | routine | Lowercase — case-sensitive rule fails. Sender error: should be `[STOP]`. |

Examples 4–6 are the leak cases the bracket-required, start-position, case-sensitive
rules are specifically designed to exclude. A classifier implementer can apply the
canonical pattern to every row above and reproduce this column with no judgment call.
