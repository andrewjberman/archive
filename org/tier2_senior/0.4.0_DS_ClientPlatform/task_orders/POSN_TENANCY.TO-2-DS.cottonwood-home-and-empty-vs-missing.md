<task_order>
<id>POSN_TENANCY.TO-2-DS.cottonwood-home-and-empty-vs-missing</id>
<title>Cottonwood Positioning presence measured at the SERVED KEY with a positive control, and whether the consumer distinguishes MISSING from EMPTY today</title>
<project>POSN_TENANCY</project>
<directive>POSN</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~L</issued_to>
<issued_at>2026-08-27T20:5xZ</issued_at>
<status>COMPLETE — ACCEPTED 4/4 by the issuer 2026-08-27 ~21:2xZ. Deliverable `@2be92878c0`.

**PROOF INSTANCE VALIDATED AT THE ISSUER'S SEAT, NOT ACCEPTED ON THE REPORT:** `rc=0 VALID`,
`violations=0`, `acceptance rows=4`, coverage checked against the embedded criterion set; negative
control (a nonexistent criterion id) returns `rc=1`.

⛔ **AND THE FIRST RUN CAME BACK `INVALID` BECAUSE OF A DEFECT IN THIS TO, NOT IN THE WORK.** I wrote
the `<decomp_ref>` path wrapped in markdown backticks; the checker reads raw tag content, so the TO's
path *"does not resolve to a file"* and "disagreed" with the instance. **`0.4.0_DS_ClientPlatform~L`'s
instance was correct and my formatting failed it.** Fourth machine-readable field this office broke
with prose decoration today. Fixed here and in the two sibling TOs carrying the same construction.

**VERDICT PER CRITERION — the two that earned it:**
- **`AC2` (the positive control):** Cottonwood's own home reads **6,599 objects** (gold 3535,
  platinum 1125, forwardfill_v2 695, silver 596, logs 424, code 150, bronze 73, blackdiamond 1) with
  **0 Positioning** — so the absence is **HOME PRESENT / POSITIONING ABSENT**, not an empty bucket and
  not a blind credential. Plus a `head-object` discriminating pair on one bucket/prefix/form:
  `model.json` rc=254/404 vs `positioning_data.json` rc=0/8088 bytes.
- ⭐ **THE GRAIN TRAP THEY CAUGHT WOULD HAVE INVERTED THIS CRITERION.** Token `position` matches
  **922 of 6,599** in Cottonwood's home — `positions_cube.py`, `canonical_positions.py` — **the
  CANONICAL POSITIONS pipeline, a different grain from the portal Positioning artifact.** A naive
  census returns 922 and reports PRESENT. Measured at the right grain: `positioning` 0,
  `allocation_summary` 0, `holdings_attribution` 0. A substring trap was caught beside it (`firm` → 2
  hits, both inside `mullin-confirmation-hearing.json`).

**`AC1`** complete listings, `IsTruncated=False` on every page, `--no-paginate` per page **because
auto-paginate merges pages and DROPS the very field the criterion asks to see**; `--max-items`/`head`
appear nowhere in the probe. **`AC3`** the consumer DOES distinguish MISSING from EMPTY today —
`portal-proxy.ts:94/:112` (error state) vs `:115`→`:42` (success, no data) `@portal 4a52439cbe` —
but **incidentally, as a byproduct of `!response.ok`, NOT as a contract**, and MISSING collapses into
one Error string shared with auth failure. Reported as a finding, not designed around. **`AC4`**
read-only verified: 4 read verbs, **0 write verbs**, no S3 object written.

⚠ **`PT-b-3` OBSERVED; `PT-c-2` PARTIALLY OBSERVED** (consumer half only — the producer half does not
exist yet). Cell states are as observed and were **not** synthesized from criterion verdicts.
⚠ **RELAYED, NOT RE-DERIVED, and correctly flagged as such by the executor:** `:1099-1100` records a
nonexistent path returning **401 not 404**, which would make MISSING indistinguishable from
UNAUTHENTICATED. That is `0.0.0_AB_MSTR~Z`'s measurement; re-running it needs a live bearer and is
outside a read-only substrate TO. **It is the open thread this TO leaves behind.**</status>

<decomp_ref>
Stage-3 atom decomp workflows/atom_decomposition/runs/posn-tenancy/20260827T200734Z/DECOMP.md
v1.4, authored by `2.0.0_SA_COO~Z`. **Certified PARTIAL by `3.0.0_SA_CVO~Z`** — 18 of 19 cells + 6
invariants CERTIFIED WITH FINDINGS at pin `@07de844b12`; `PT-b-2`, `R-pt1`, `PT-b-4` and `PT-inv-7`
(as a cell) NOT certified. Cells bind in their **v1.3/v1.4 corrected wording** — a certification with
findings certifies the object as amended by its findings.
</decomp_ref>

<scope_fence>
⛔⛔ **THIS TO MEASURES THE PRESENT. IT DOES NOT BUILD THE PRODUCER, AND IT MUST NOT.**

`PT-b-2` — **which substrate shape isolation holds under** — is **NOT CERTIFIED** (it failed Rule 24
postulate (i) on measurement: both shapes are live at once, and the shared limb is **unbuildable for
at least one firm** because `smartx/` partitions by FUNCTION with no firm boundary). **No shape has
been selected.**

>> **THEREFORE `PT-c-1` — WHO WRITES POSITIONING DATA INTO A FIRM'S SUBSTRATE — CANNOT BE DISCHARGED
   YET, AND THIS TO DOES NOT NAME A PRODUCER.** Naming a producer owner before the substrate shape is
   chosen binds a lane to a shape nobody has selected. `PT-c-1` is BLOCKED BY `PT-b-2`, and that
   dependency is recorded here rather than resolved quietly. <<

⚠ **DO NOT WRITE, MOVE OR MINT ANY S3 OBJECT.** This TO is read-only against the substrate.
</scope_fence>

<cells>

| cell | what this TO owes it |
|---|---|
| `PT-b-3` | **Cottonwood has a data HOME but NO Positioning data in it.** `AUTH_COTTON` was identity-and-allowlist only — **NO DATA PIPELINE**. The cell's oracle is explicit: **measured at the SERVED KEY, not at the code.** ABSENT must be established as a measurement, not inferred from the absence of a pipeline. |
| `PT-c-2` | **A firm with no data must emit an EXPLICIT EMPTY, never a missing key.** Oracle: **missing and empty must be DISTINGUISHABLE AT THE CONSUMER.** Pre-build, the answerable half is: **does the consumer distinguish them TODAY?** |
| `PT-inv-1` | **THE BYTES, NOT THE PIXELS** — binding on every criterion below. |
| `PT-inv-4` | **OTHER FIRMS BYTE-IDENTICAL.** Read-only TO, so it holds by construction — **report it as a measured no-op, not as a verification performed.** |

</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `T2DS-AC1` | Cottonwood's Positioning presence is established **at the served key** with a **COMPLETE listing** — `NextToken` shown ABSENT, or the listing paginated to exhaustion. ⛔ **`--max-items` / `head` / `\| head` are BANNED for this count**: a lexicographic head is not a population, and this exact instrument killed a REAL hazard on this project four hours ago (`_ops/` sorts first and read as the whole prefix). | `PT-b-3` | |
| `T2DS-AC2` | ⛔ **The ABSENT verdict carries a POSITIVE CONTROL** — the same probe, same form, run against a firm whose Positioning data is known present, shown returning a non-empty result. **A failed retrieval and a true absence are byte-identical without it**, and an absence claim is the whole content of `PT-b-3`. | `PT-b-3` | |
| `T2DS-AC3` | Whether the Positioning consumer **distinguishes a MISSING key from an EMPTY artifact** is reported as an observed behaviour with the deciding code path cited `file:line @ <commit-ish>`. **If it does NOT distinguish them, that is a finding and is reported as one** — do not design the fix, do not build it. | `PT-c-2` | |
| `T2DS-AC4` | ⛔ **No criterion is discharged by a RENDER or screenshot** (`PT-inv-1`), **nor by "the commit gate passed" / `comp-constants check`** — that checker dispatches on `.py`/`.sh`/`.tf` only. **And no S3 object is written by this TO** — state that as measured. | `PT-inv-1` `PT-inv-4` | |

</acceptance_criteria>

<reporting>
Deliverable in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~L <0.4.0_DS_ClientPlatform~L@opal.agent>" -F <msgfile>`.
Message file written by a **non-shell writer** (Write tool / python), never a heredoc.

**Push state MEASURED** (`ls-remote`/ancestry against a FETCHED ref, with a control) **or the words
"push state UNMEASURED"** — LOCAL is a measured value, never a default.

**`cell_status` per cell, from states actually observed only.** ⛔ **Do NOT synthesize cell states
from criterion verdicts.** `PT-c-2`'s expected honest state is **PARTIALLY OBSERVED** — the consumer
half is observable now, the producer half does not exist yet.

⚠ **`aws s3 ls` renders LOCAL time; `s3api` renders UTC.** If any timestamp enters the deliverable,
name which API produced it.
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· **No new alert/alarm/monitor** (`PT-inv-5`, standing moratorium).
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
· ⚠ **`PT-b-4` IS UNCERTIFIED AND OUT OF SCOPE, BUT YOU WILL LIKELY TRIP OVER IT.** Two live prefixes
  exist for one firm — `blackdiamond/49f/` (285 objects, holds the only `gold/` tier) and
  `blackdiamond/49financial/` (8,862). **If your sweep touches them, report what you see and do not
  act on it** — three seats have already measured it and a fourth measurement is not what it needs.
</standing>

<proof_of_spec>
  <criterion id="T2DS-AC1" cell_refs="PT-b-3"/>
  <criterion id="T2DS-AC2" cell_refs="PT-b-3"/>
  <criterion id="T2DS-AC3" cell_refs="PT-c-2"/>
  <criterion id="T2DS-AC4" cell_refs="PT-inv-1,PT-inv-4"/>
  <expected_criteria>T2DS-AC1,T2DS-AC2,T2DS-AC3,T2DS-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~L/deliverables/POSN_TENANCY.TO-2-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 4 (`PT-b-3`, `PT-c-2`, `PT-inv-1`, `PT-inv-4`); criteria: 4. FORWARD — 4 of 4 criteria carry >=1 cell_ref. BACKWARD — 4 of 4 declared cells reachable from >=1 criterion (`PT-b-3` from AC1+AC2, `PT-c-2` from AC3, `PT-inv-1` and `PT-inv-4` from AC4). Unmapped 0; untraceable 0. *(The remaining 17 of the decomp's 21 cells are NOT this TO's: (a) served plane and (e) migration order are AE-class with no seat; (d) is carried by `TO-1-DE`; `PT-c-1` is BLOCKED by `PT-b-2` per the scope fence; `PT-b-2`, `PT-b-4`, `R-pt1` are UNCERTIFIED and no TO may be cut against them.)*</alignment_denominators>
  <criterion_status_note>⛔ AC2 exists because AC1's expected answer is an ABSENCE, and this project has already been bitten twice by absence-shaped evidence — once by a truncated listing that manufactured a false "cold prefix", once by a grep-derived population that undercounted 12x. **An absence with no positive control is not a measurement of the world; it is a measurement of the probe.** A PASS on AC1 without AC2 is not a PASS.</criterion_status_note>
</proof_of_spec>
</task_order>
