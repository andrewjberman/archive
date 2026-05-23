# [Template] CVO to CTO/COO/DS/AE/DT Response

CVO fills in against this shape, saves to `../responses/{YYYYMMDDTHHMMSSZ}_to_{primary_recipient_serial}_{subject_slug}.md`, and commits under its own author line via `.tools/safe-commit.sh`.

Delete italic template commentary before filling in.

---

## Frontmatter

```yaml
---
from: 3.0.0_SA_CVO
to: 1.0.0_SA_CTO                         # primary recipient; secondary recipients in §Routing
report_ref: {inbox_filename}
report_trigger: wave_gate                 # mirrors report trigger field
phase: ADHC_WAVPLN Wave 1                # mirrors report phase
response_date: {YYYY-MM-DD}
verdict: NORMAL                           # NORMAL | MALFORMED_REPORT | WAIVED_AFTER_READ
---
```

---

## §0 — Convergence reading

*CVO: one-paragraph synthesis. What did the evidence converge on? What is
the single most important thing the CTO should walk away knowing?*

*This is the part the CTO reads in 30 seconds. Make it count.*

---

## §1 — Recommendations by driver

*Required structure. Every recommendation is: one paragraph, grounded in a
file:line citation, priority-marked, action-typed. Do NOT skip a driver section —
if there is no recommendation for a driver, write "No recommendations this cycle."*

### For CTO (`1.0.0_SA_CTO`)

**[P0] R-CTO-1 — {one-line recommendation title}**

*One paragraph. Must include: (a) the specific change recommended, (b) the
evidence citation, (c) the mechanism-level rationale, (d) the action type —
"PRD amendment at §X.Y" / "pipeline architecture change" / "measurement-axis addition".*

**[P1] R-CTO-2 — ...**

...

### For COO (`2.0.0_SA_COO`)

**[P0] R-COO-1 — ...**

*One paragraph. Action type for COO is usually: "TO decomposition into X lanes",
"wave sequencing change", "gate unlock decision", "agent serialization recommendation".*

...

### For DS (`0.4.0_DS_ClientPlatform`)

**[P1] R-DS-1 — ...**

...

### For AE (`0.6.1_AE_PartnerETL` / `0.7.0_AE_CloudOps`)

**[P1] R-AE-1 — ...**

*Specify which AE serial if recommendation applies to one. Action type: "Lambda deploy
sequence change", "IAM gap fix", "CW alarm addition", "S3 sentinel pattern application".*

...

### For DT (`0.3.0_DT_TradingOperations` / `0.4.0_DT_PortalDev`)

**[P2] R-DT-1 — ...**

...

---

## §2 — Deferrals

*CVO: things the CTO asked about or you considered but are explicitly NOT
recommending. Each with reasoning.*

- **Deferred: {topic}** — Reason: *{why this is not a recommendation now; what
  would make it one later}*

...

---

## §3 — Malformed questions or premise errors

*CVO: if any of the CTO questions were malformed, had incorrect citations,
or had false premises, call them out here. One paragraph per issue.*

- **Q{N} premise issue:** *{description + specific correction}*

*If no malformed questions, write "None this cycle."*

---

## §4 — Unknown-unknowns (MANDATORY)

*CVO: what you should have been asked but were not. This is the one section
that does not respond to an enumerated question. It surfaces a gap the CTO
did not know to name.*

*If there are genuinely no unknown-unknowns, say so explicitly — but be suspicious
of that answer. The whole point of an external reviewer is that the inside of
the project cannot see its own blind spots.*

---

## §5 — Cross-cutting observations (optional)

*CVO: if there are themes that run across multiple drivers recommendations —
systematic deployment gaps, repeated silent-failure patterns, IAM scope creep,
architectural stress points — surface them here. Not a required section; skip if none.*

---

## §6 — Routing

*CVO: every P0 recommendation must be routed. Each line = one CC.*

- CC `1.0.0_SA_CTO` — R-CTO-1, R-COO-1 (cross-driver)
- CC `2.0.0_SA_COO` — R-COO-1, R-COO-2
- CC `0.4.0_DS_ClientPlatform` — R-DS-1
- CC `0.6.1_AE_PartnerETL` — R-AE-1
- CC `0.7.0_AE_CloudOps` — R-AE-2

---

*— 3.0.0_SA_CVO*
