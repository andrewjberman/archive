# NFRA_OUTSET.TO-OS-s-27 -- THE STRATUM'S OWN STRINGS REACH THE ARTIFACT: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-27` ·
**Written:** 2026-09-10T15:0xZ. **O27-AC2 carries NO verdict.**

---

## THE ONE-LINE ANSWER, IN THE ISSUER'S OWN WORDS

**APPLIED, NOT YET SERVED.** Both strings are serialized, deployed and exercised offline against
the same pinned inputs the 13:00Z run read. **The first artifact carrying them is the 2026-09-11
13:00Z fire**, and that is the distinction between an accept that is met and an accept that is met
**on the plane it names**.

`O27-AC1` **PASSES**: `OS27-BOTH-STRATUM-STRINGS-SERIALIZED`, rc=0 unpiped, 6 arms plus a
tree-provenance arm, 7 evaluated, 0 FAIL. Proof instance VALID rc=0.

## WHY BOTH STRINGS, AND WHY ONE WOULD HAVE BEEN A FAILED CELL

| field | carries | read by |
|---|---|---|
| `stratum_denominator` | the roster, the per-device states, the grain **NOTE** (`:1424`) | **O22-AC1 clause (v)** |
| `stratum_vintage` | the grain **TAG** `[grain=..., NOT resource-grain]` (`:1425`) | **O23-AC1** |

Two adjacent lines, opposite destinations. Row `S40` attributed both to the denominator; **row
`S41` corrected that before the remedy was cut**, and both the issuer and `1.0.0_SA_CTO` verified
all three of its mechanical claims at source. A denominator-only fix would have closed one clause
and presented as complete.

## THE ARMS, WITH THE CONTROLS THAT MAKE THEM MEASUREMENTS

- **(0) TREE PROVENANCE.** Measured in the main tree on branch `CLOUD`, with the battery's own path
  resolving there as a positive control -- a tool resolving its corpus elsewhere would have read a
  clean zero.
- **(a) THE ABSENCE REPRODUCED FIRST.** 5 literals, **0 hits each**, against the positive control
  `A_propagation@laptop` at **2**. The zeros are a property of the artifact.
- **(b) BOTH FIELDS**, printed verbatim, each mapped in the output to the clause it serves.
- **(c) BYTE EQUALITY, NOT CONTAINMENT.** `stratum_vintage` 167 B and `stratum_denominator`
  1,298 B, sha256-equal to what the runner composed in the same run. **Control: a truncated copy
  PASSES `contains` and FAILS equality** -- which is the same defect one level down from the
  validator this cell deliberately did not touch.
- **(d) THE DIFFERENCE CONTROL.** `[grain=` absent from the **real served** group-B block of the
  13:00Z run, present in the block rendered from the **same inputs** through the **deployed** bytes.
  Only the after side is rendered.
- **(e) NOTHING ELSE MOVED.** `tool_row_resolves` (823 B) and `tool_row_ref` (590 B)
  **byte-identical** old vs new, compared as function **bodies** because a count cannot see an edit
  that preserves length; 2 of 2 composed-string lines unchanged; 4 group statuses rewritten by
  nothing; **0 of 6** served report/manifest keys moved.
- **(f) THE DEPLOY.** Uploaded 14:15:40Z, instance read LIVE `stopped` at 14:15:23Z, **re-downloaded
  by its NEW VersionId** and byte-equal, one-bit mutant at fixed length reporting MISMATCH, 22
  versions with the rollback named from the live list. The **already-served check ran before the
  upload** and showed a real difference, so this was not a SUPERSEDED close.

## THE VALIDATOR -- OUT OF BOUNDS, AND NAMED RATHER THAN SILENTLY LEFT

`tool_row_resolves` admits any sentence containing two tokens as **substrings**, and that is what
let a five-of-five candidate set ship without the grain tag while nothing failed. It is **not**
touched here (issuer, 95206): once the artifact carries the runner's own strings as fields, the
validator stops being the only carrier and its looseness stops being load-bearing. **If it still
admits an unlabelled citation after this lands, that is its own finding with its own evidence and
its own cell.** Recorded, not fused.

## O27-AC2 -- JUDGMENT, EVIDENCE ONLY, NO VERDICT

**Can a reader now tell that group B pairs FILES rather than RESOURCES, without opening the
runner?** From 2026-09-11 13:00Z onward, yes, from one field. **Today, no** -- and that is the
`APPLIED, NOT YET SERVED` line above.

**What `tool_row_resolves` would still admit:** any sentence containing the stratum name and the
trace vintage as substrings -- a citation that drops the grain tag, appends a claim the stratum
never made, or reorders the row into a different assertion.

**Consumer census, run rather than asserted:** `comp-find 'stratum_status' --all` → **135 hits
across 154,114 files**, banded SURFACED 44 / CONFIG 38 / TEST 17 / DOC 36. It **corrected what I
was about to write from memory** and surfaced a **second producer of this block shape**
(`kimi_subdivision_harness/kimi_pipeline.py` at `:650`, `:681`, `:852`) -- row `S43`, filed at the
issuer's direction, INERT and with **no measured harm**, so it is evidence the shape recurs and not
that it costs.

**Could anything break?** The change is purely additive: 2 keys added, 0 renamed, 0 removed, 0
re-typed. Only a reader asserting an exact key set could break, and the one such reader is this
battery's own arm (b), which deliberately asserts **presence** rather than the whole set.

**Disclosed side effect:** the manifest's `ai_funnel.groups` copies every group key except
`candidates_rejected` (`:3084`), so both fields appear there too and the manifest grows. **No filter
was added to suppress it**, because adding one would have been something else moving under an arm
asserting nothing else moved.

**What a reader still cannot learn:** which failure arm a per-device read took (the vintage reads
`UNREAD (<source>)` whatever the cause, so the 403-vs-404 distinction lives in the denominator);
the row data behind a stratum; and whether a model-composed citation is faithful beyond the two
tokens the gate tests.
