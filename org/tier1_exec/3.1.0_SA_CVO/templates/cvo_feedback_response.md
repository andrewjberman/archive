# [Template] CVO → CTO/COO/SC/DS Response

Codex fills in against this shape. The CTO saves the response (pasted from Codex)
to `../responses/{YYYYMMDDTHHMMSSZ}_to_{primary_recipient_serial}_{subject_slug}.md`
and commits under CVO author line.

Delete italic template commentary before Codex fills in.

---

## Frontmatter

```yaml
---
from: 3.1.0_SA_CVO
to: 1.1.0_SA_CTO                         # primary recipient; secondary recipients in §Routing
report_ref: {inbox_filename}
report_trigger: wave_close               # mirrors report's trigger field
phase: Wave 3a                           # mirrors report's phase
response_date: 2026-04-24
verdict: NORMAL                          # NORMAL | MALFORMED_REPORT | WAIVED_AFTER_READ
---
```

---

## §0 — Convergence reading

*Codex: one-paragraph synthesis. What did the evidence converge on? What is
the single most important thing the CTO should walk away knowing?*

*This is the part the CTO reads in 30 seconds. Make it count.*

---

## §1 — Recommendations by driver

*Required structure. Every recommendation is: one paragraph, grounded in a
file:line citation, priority-marked, action-typed. Do NOT skip a driver section
— if there is no recommendation for a driver, write "No recommendations this
cycle."*

### For CTO (`1.1.0_SA_CTO`)

**[P0] R-CTO-1 — {one-line recommendation title}**

*One paragraph. Must include: (a) the specific change recommended, (b) the
evidence citation, (c) the mechanism-level rationale, (d) the action type —
"PRD amendment at §X.Y" / "nav schema extension" / "measurement-axis addition".*

**[P1] R-CTO-2 — ...**

...

### For COO (`2.1.0_SA_COO`)

**[P0] R-COO-1 — ...**

...

### For SC (`2.1.0_SC_CompLearns`)

**[P1] R-SC-1 — ...**

...

### For DS (any of `1.1.0-1.4.0_DS_CompLearns`)

**[P1] R-DS-1 — ...**

...

---

## §2 — Deferrals

*Codex: things the CTO asked about or you considered but are explicitly NOT
recommending. Each with reasoning.*

- **Deferred: {topic}** — Reason: *{why this is not a recommendation now; what
  would make it one later}*

...

---

## §3 — Malformed questions or premise errors

*Codex: if any of the CTO's questions were malformed, had incorrect citations,
or had false premises, call them out here. One paragraph per issue.*

- **Q{N} premise issue:** *{description + specific correction}*

*If no malformed questions, write "None this cycle."*

---

## §4 — Unknown-unknowns (MANDATORY)

*Codex: what you should have been asked but weren't. This is the one section
that does not respond to an enumerated question. It surfaces a gap the CTO
didn't know to name.*

*If there are genuinely no unknown-unknowns, say so explicitly — but be suspicious
of that answer. The whole point of an external reviewer is that the inside of
the project cannot see its own blind spots.*

---

## §5 — Cross-cutting observations (optional)

*Codex: if there are themes that run across multiple drivers' recommendations —
systematic measurement gaps, repeated failure-mode patterns, architectural
stress points — surface them here. Not a required section; skip if none.*

---

## §6 — Routing

*Codex: every P0 recommendation must be routed. Each line = one CC.*

- CC `1.1.0_SA_CTO` — R-CTO-1, R-CTO-2, R-COO-1 (cross-driver)
- CC `2.1.0_SA_COO` — R-COO-1, R-COO-2
- CC `2.1.0_SC_CompLearns` — R-SC-1
- CC `1.1.0_DS_CompLearns` — R-DS-1

---

*— 3.1.0_SA_CVO*
