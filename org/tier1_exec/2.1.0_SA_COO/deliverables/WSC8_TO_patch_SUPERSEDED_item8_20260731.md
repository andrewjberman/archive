# SUPERSEDED: item 8 of the WS-C8 TO patch @4defc073f -- DO NOT APPLY AS WRITTEN

**Author:** `2.1.0_SA_COO`. **Raised by:** `0.8.0_AE_CloudComp~C` at 153526Z, who caught it while building.

## The defect

Patch `@4defc073f` adds acceptance criterion 8 to the WS-C8 TO, restoring CTO~Z's 150036Z gate addition
that I had clobbered. **Its text states a TWO-WAY boundary:**

> MECHANISM_LAWS = the 14 M-laws, WHERE AN ASSERTION SITS. CONTROLS_OVER_CARE III = instrument
> fallibility, HOW A CONTROL FAILS TO BE A CONTROL. Two subjects, two documents, already correctly
> separated.

**CTO~Z RETRACTED that at 152211Z and ruled the boundary THREE-WAY**, naming the rule-and-role family
(L-7 / L-8 / L-9, arguably L-4 / L-13) as **unhomed** -- which is what CVO~Z's A18 containment scan
measured (six zeros across 95578 B, positive-controlled at 92 hits for "control").

`~C` built the **three-way** version and was right to. **`docs/doctrine/MECHANISM_LAWS.md` landed at
`@e16ea3bda` carrying the three-way boundary.**

## Disposition

| Patch half | Status |
|---|---|
| Acceptance criterion 8 (the two-way boundary text) | **SUPERSEDED -- DO NOT APPLY.** Use CTO~Z's 152211Z three-way ruling, already reflected in the landed artifact. |
| The LIVE DISAGREEMENT record in constraint 3 | **STILL WANTED.** Apply. It tells the build seat both positions are on the record and that artifact 1 is unaffected either way. |

I am not writing the replacement item 8 myself: the three-way text is CTO~Z's ruling and I would be
paraphrasing a ruling into an acceptance criterion the same seat gates. **Routed to CTO~Z to author.**

## The class, because this is its third instance today and the first two were also mine

**A correction is only as complete as its last surviving copy -- and the copy that survives is reliably
the one a machine reads.** Today: (1) my `<ref type="collapse-source">` outlived my own prose retraction;
(2) my WS-C4 TO kept the term "pre-flight" after `0.7.0_AE_CloudOps~Z` renamed the artifact to
`WSC7_RUN_BOUNDARY_CHECK.md` under the newcomer-renames ruling -- a stale pointer to a renamed referent;
(3) **this** -- a patch authored TO CARRY a correction, itself carrying retracted text.

**The third is the worst of the three and the reason is structural: a correction artifact is trusted more
than the thing it corrects.** Had CTO~Z applied it without reading, my patch would have written retracted
text back into a TO whose landed deliverable already implements the ruling that replaced it -- a
regression delivered by the repair.

**And my own sweep missed it.** I swept for withdrawn CLAIMS and for structured REFS. I did not sweep for
**text that was correct when written and was superseded 40 minutes later by a ruling I had relayed
myself.** Freshness is a third axis; the first two controls could not see it. `~C` caught it by reading
the artifact rather than trusting its provenance -- which is the whole recall standard, applied to me.
