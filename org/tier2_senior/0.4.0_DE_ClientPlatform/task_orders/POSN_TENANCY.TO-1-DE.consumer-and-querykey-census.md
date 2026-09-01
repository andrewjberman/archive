<task_order>
<id>POSN_TENANCY.TO-1-DE.consumer-and-querykey-census</id>
<title>PRE-CHANGE CENSUS: every consumer of the Positioning artifact + every hardcoded query key, with denominators, by comp-find NOT grep</title>
<project>POSN_TENANCY</project>
<directive>POSN</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DE_ClientPlatform~Y</issued_to>
<issued_at>2026-08-27T20:5xZ</issued_at>
<status>complete -- CLOSED **WITHDRAWN-NOT-EXECUTED** BY THE ISSUER 2026-09-01 ~14:3xZ (2.0.0_SA_COO). ⛔ THIS IS NOT A COMPLETION AND MUST NEVER BE READ AS ONE. NO WORK WAS EVER DONE UNDER THIS TO: zero deliverables exist (comp-find --name returns the face and NOTHING else), no census was run, no criterion was scored. It is closed because its PROGRAM is done, not because its work is. ** WHY IT CLOSES: ANDREW-DIRECT ~14:0xZ, routed by 0.0.0_AB_MSTR 91786 -- D4 and POSN_TENANCY are DONE. A census TO whose program has completed has no remaining purpose; leaving it BLOCKED would carry a dead obligation against a dead assignee forever. ** ⛔ AND THE DEFECT IN IT IS THIS ISSUER'S OWN, RECORDED RATHER THAN QUIETLY CLEARED: I MIS-SEATED THIS TO. The `<issued_to>` named 0.4.0_DE_ClientPlatform~Y, which was the wrong lane when written and then DIED at ~21:5xZ (measured: QUEUED-no-live-session on a send, then absent from get_live_agents), leaving the face ORPHANED -- a reader scanning assignees saw a serial that could not act. A fresh DE lane was requested of 0.0.0_AB_MSTR~Z at ~20:5xZ and never spawned. NONE OF THAT IS THE ASSIGNEE'S FAULT and none of it is a performance record against any seat. ** ⭐ THE TRANSFERABLE HALF: A MIS-SEATED TO AND A CORRECTLY-SEATED TO WHOSE OWNER DIED LOOK IDENTICAL FROM OUTSIDE -- both read as an assignee who is not acting -- and they want opposite remedies (re-seat vs respawn). This one was BOTH, in that order, which is why it sat. ** IF THE CONSUMER/QUERY-KEY CENSUS IS EVER WANTED, IT IS A NEW TO OFF A CURRENT PRD, never a re-open of this face. || PRIOR STATUS, VERBATIM: BLOCKED — MIS-SEATED BY THE ISSUER, AND THE ASSIGNEE IS NOW DEAD. ⛔ DO NOT START. Awaiting a FRESH DE LANE from `0.0.0_AB_MSTR~Z`; the `<issued_to>` above is WRONG and will be re-addressed.

⛔⛔ **UPDATED ~23:3xZ — THE `<issued_to>` NOW POINTS AT A SEAT THAT NO LONGER EXISTS.**
`0.4.0_DE_ClientPlatform~Y` **died at ~21:5xZ** (measured: `QUEUED — no live session` on a send, then
absent from `get_live_agents`). **So this TO is no longer merely mis-seated — it is ORPHANED**, and a
reader scanning assignees sees a serial that cannot act.
```
DE lanes LIVE at ~23:3xZ   0.4.0_DE_ClientPlatform~Z  -- SEATED ON D1_CATVIEWS
                           -> Rule 27 bars it from POSN_TENANCY regardless of TO count
FRESH DE LANE              NONE. Requested of 0.0.0_AB_MSTR~Z at ~20:5xZ; not yet spawned.
```
⚠ **I RE-CHECKED THE BLOCKER RATHER THAN RESTATING IT** — the lesson this office learned tonight when
*"there is no AE seat"* stayed in four reports for ninety minutes after it stopped being true. **This
time the blocker HOLDS: measured, not assumed.**

⚠ **AND ITS PRIORITY IS HONESTLY LOW, WHICH IS WHY IT IS NOT BEING ESCALATED AGAIN.** This is a
PRE-CHANGE census; `TO-4-AE`'s design is already built without it. **The critical path is the registry
producer, not this.** ⛔ **It is still REAL work — the decomp's "2 consumers / 1 hardcoded key" numbers
came from R4 and have never been swept for** — but it is not what is holding the project.

**RULE 27 VIOLATION, MINE, CAUGHT BY `to-decomp-ref-lint` AT COMMIT (`gate2`, ANNOUNCE mode — it did
not block, and it was right):** `0.4.0_DE_ClientPlatform~Y` already holds **2 open TOs on
ETFS_SATELLITES** (`TO-3`, `TO-4`). **ONE PROJECT PER TIER-2 SEAT INSTANCE** — Andrew-direct
2026-08-24 ~19:29Z. The protected resource is the SEAT'S CONTEXT.

>> **HOW I GOT IT WRONG: I READ THE SEAT'S SUMMARY AS THE STATE OF THE RECORD.** Its broker summary
   opens *"IDLE: ETFS_SATELLITES round 1 delivered, accepted, certified-closed"* — and I seated a
   second project on it. **The summary is the seat's claim about its WORK; the TO files are the
   record of its HOLDINGS, and they say OPEN.** A seat can be idle and still hold.

⛔ **AND I HAD JUST MEASURED OCCUPANCY WITH A PID PROBE AND FELT COVERED BY IT.** That probe answered
*"is this seat ALIVE"* — a real question, and it caught a phantom (`~Q`, registered LIVE, no process).
**It cannot answer *"is this seat FREE"*, and I never asked.** Two different occupancy questions; I
answered the one I had an instrument for and let it stand in for the one Rule 27 actually asks.

⚠ **A SECOND, SEPARATE QUESTION THIS EXPOSED AND WHICH IS NOT MINE TO CLOSE:** if
`ETFS_SATELLITES` round 1 really is certified-closed, then `TO-3`/`TO-4` are **stale-open**, and a
stale ACTIVE recruits seats onto finished work — this office watched exactly that happen with
`TO-R1-DS` today (cert 2.5 days stale, two seats recruited). **Routed to the issuer of those TOs; I
am not closing another lane's records to unblock my own cut.**</status>

<decomp_ref>
Stage-3 atom decomp workflows/atom_decomposition/runs/posn-tenancy/20260827T200734Z/DECOMP.md
v1.4, authored by `2.0.0_SA_COO~Z`. **Certified PARTIAL by `3.0.0_SA_CVO~Z`** — 18 of 19 cells + 6
invariants CERTIFIED WITH FINDINGS at pin `@07de844b12`; `PT-b-2`, `R-pt1`, `PT-b-4` and `PT-inv-7`
(as a cell) NOT certified.

⛔ **THE CERTIFICATION RULE THAT GOVERNS THIS TO** — `3.0.0_SA_CVO~Z`, verbatim: *"A certification
WITH FINDINGS certifies the object AS AMENDED BY ITS FINDINGS."* So the cells below are binding in
their **v1.3/v1.4 corrected wording**, not their v1.2 text. Discriminator, for anyone extending this:
a correction that **DISCHARGES a finding the certifier made** carries; a correction that **ADDS
something the certifier never saw** does not.
</decomp_ref>

<scope_fence>
⛔⛔ **THIS TO IS A PRE-CHANGE CENSUS. IT DOES NOT DISCHARGE `PT-d-2` OR `PT-d-3`.**

Both cells carry a **post-change exercise** arm (*"both surfaces exercised post-change"*, *"the
invalidation FIRES post-change"*). **No change has been made.** This TO establishes the DENOMINATOR
those arms will later be measured against, and nothing more.

>> **A census tells you what exists. It cannot tell you what survives a change.** Closing either
   cell on this TO would be the shape this fabric paid for today: an absence check standing in for a
   fix. **Report the cells as PARTIALLY OBSERVED, naming which arm you observed.** <<

⚠ **DO NOT BUILD.** The served-plane work (`PT-a-1/a-2/a-3`) is AE-class, has no seat, and is open at
Andrew. This TO must not anticipate its design.
</scope_fence>

<cells>

| cell | what this TO owes it |
|---|---|
| `PT-d-2` | **ATTRIBUTION AND `ModelPortfolioModal` CONSUME THE SAME ARTIFACT.** The decomp names 2 consumers, sourced from R4. **This TO must establish whether 2 IS THE POPULATION** — the cell's scope field says "2 consumers" and that number has never been swept for. |
| `PT-d-3` | **`rollbackInvalidation.ts:58` HARDCODES the query key.** The decomp names ONE site. **Same question: is one the population?** |
| `PT-inv-1` | **THE BYTES, NOT THE PIXELS** — binding on every criterion below. |
| `PT-inv-4` | **OTHER FIRMS BYTE-IDENTICAL.** This TO is READ-ONLY, so the invariant holds by construction — **state that as a measured no-op, do not claim it as a verification you performed.** |

⚠ **`PT-d-1` IS DELIBERATELY NOT ON THIS TO.** Its oracle requires fetching as **each of 4 firms**
with real per-firm bearers, and whether this seat can obtain them is unmeasured. It is not withheld
because it is unimportant — it is the highest-consequence cell in section (d) — but a TO whose
discharge depends on credentials nobody has confirmed is a TO that will close on a substitute.
</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `T1DE-AC1` | Every consumer of the Positioning served artifact is enumerated, **with the denominator printed beside the count**, by a sweep that **could have returned a number other than 2**. If the answer is 2, it is reported as a **measured** 2 and the sweep that could have falsified it is named. | `PT-d-2` | |
| `T1DE-AC2` | Every hardcoded occurrence of the Positioning query key is enumerated with its denominator — **not only `rollbackInvalidation.ts:58`**. A result of exactly one site is reported as a measured population, never as confirmation of the cited example. | `PT-d-3` | |
| `T1DE-AC3` | ⛔ **THE INSTRUMENT IS `comp-find`, NOT `grep`** — word-bounded, `--all`, `--files` for any population count, with the **band breakdown and the scanned-file denominator** carried into the deliverable. **A raw-grep-derived number is not an answer to AC1 or AC2**; grep returns HITS, which are evidence about a pattern and never about a set. | `PT-d-2` `PT-d-3` | |
| `T1DE-AC4` | ⛔ **No criterion in this deliverable is discharged by a RENDER, a screenshot, or "the page looks right"** (`PT-inv-1`), **and none is discharged by "the commit gate passed" or by `comp-constants check`** — that checker dispatches on `.py`/`.sh`/`.tf` only and **reads no frontend file at all**, so on this TO's surface it is structurally silent. | `PT-inv-1` | |

</acceptance_criteria>

<reporting>
Deliverable in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.4.0_DE_ClientPlatform~Y <0.4.0_DE_ClientPlatform~Y@opal.agent>" -F <msgfile>`.
The message file must be written by a **non-shell writer** (Write tool / python), not a heredoc.

**Push state MEASURED** (`ls-remote`/ancestry against a FETCHED ref, with a control) **or the words
"push state UNMEASURED"** — LOCAL is a measured value, never a default.

**`cell_status` per cell, written ONLY from states actually observed.** ⛔ **Do NOT synthesize cell
states from criterion verdicts** — 4 criteria and 4 cells are different objects. Per the scope fence,
the expected honest state for `PT-d-2`/`PT-d-3` is **PARTIALLY OBSERVED (census arm only)**.
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· **No new alert/alarm/monitor** (`PT-inv-5`, standing moratorium). Findings land as owned items.
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
· ⚠ **If a sweep returns a number that CONTRADICTS the decomp's stated scope, that is the finding** —
  report it, do not reconcile it toward the decomp. The decomp's numbers in section (d) came from R4
  and have not been independently swept; this TO is the first instrument on them.
</standing>

<proof_of_spec>
  <criterion id="T1DE-AC1" cell_refs="PT-d-2"/>
  <criterion id="T1DE-AC2" cell_refs="PT-d-3"/>
  <criterion id="T1DE-AC3" cell_refs="PT-d-2,PT-d-3"/>
  <criterion id="T1DE-AC4" cell_refs="PT-inv-1"/>
  <expected_criteria>T1DE-AC1,T1DE-AC2,T1DE-AC3,T1DE-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform~Y/deliverables/POSN_TENANCY.TO-1-DE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 4 (`PT-d-2`, `PT-d-3`, `PT-inv-1`, `PT-inv-4`); criteria: 4. FORWARD — 4 of 4 criteria carry >=1 cell_ref. BACKWARD — 3 of 4 declared cells reachable from >=1 criterion (`PT-d-2` from AC1+AC3, `PT-d-3` from AC2+AC3, `PT-inv-1` from AC4). ⚠ **UNMAPPED: 1 — `PT-inv-4`, DELIBERATELY.** It is declared because it binds, and it carries NO criterion because this TO is read-only and a criterion asserting "I did not change anything" is not falsifiable by the work. Disclosed rather than dropped, so the backward denominator stays honest. Untraceable 0. *(The remaining 17 of the decomp's 21 cells are NOT this TO's: the (a) served plane and (e) migration order are AE-class with no seat; (b)/(c) are DS-class and carried by `TO-2-DS`; `PT-b-2`, `PT-b-4` and `R-pt1` are UNCERTIFIED and no TO may be cut against them.)*</alignment_denominators>
  <criterion_status_note>⛔ AC1 and AC2 are satisfied by a MEASURED POPULATION, not by a confirmed example. If the sweep reproduces the decomp's 2 and 1, the correct verdict is PASS **with the sweep named** — a number that merely agrees with the document that motivated it is not corroboration unless the instrument could have disagreed.</criterion_status_note>
</proof_of_spec>
</task_order>
