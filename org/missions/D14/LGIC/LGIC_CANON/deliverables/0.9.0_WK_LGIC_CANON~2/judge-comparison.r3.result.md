# LGIC_CANON.TO-CN-j-11-r3 -- result

Worker `0.9.0_WK_LGIC_CANON~2`. Cell `CN-j-11`. Writes
`org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r3/judge-compare-r3.md`.

## Recount (independent of the deliverable's own printed lines, computed directly from the three TSVs and
the tree)

Tree `CN_TREE_R3.md` `## The planes` table: 23 planes.
`judge-f.tsv` / `judge-g.tsv` / `judge-h.tsv`: 23 data rows each (24 lines including header).

- PLANE INTERSECTION F.G.H = 23 of 23 (all three answer files carry rows for every tree plane, no extra).
- POSITIVE CONTROL F.F = 23 of 23 (judge F intersected with itself is its own row count).
- ROLL-UP AGREE F.G.H = 22 of 23; F.G = 22 of 23; F.H = 22 of 23; G.H = 23 of 23.
- ROLL-UP DIVERGE = 1 of 23, on `opal-data-bd/code/`: judge F `worst_verdict=UNDETERMINED, worst_rule=R13`
  (A4 compute unmeasured is F's worst axis; F's A3 naming axis itself reads `DECLARED-EXCEPTION` under R13's
  compute-axis citation not applying -- F's own row cites A3:R1 with verdict DECLARED-EXCEPTION, but the ROW's
  worst_verdict is UNDETERMINED because UNDETERMINED > DECLARED-EXCEPTION in the severity order and F's A4
  reads UNDETERMINED); judges G and H both read `worst_verdict=VIOLATES, worst_rule=R1` (their A3 naming axis
  is the row's worst, citing the bucket's own name carrying the refused short alias `bd` rather than the
  sanctioned LONG form).
- UNION REACHED = 5 of 6: R3, R8, R14, R19, R21 present in at least one judge's `reach` column; R15 absent
  from all three.

## The trace (J11R3-AC5's substance, for 3.0.0_SA_CVO)

The three rows for `opal-data-bd/code/` (read at HEAD, this worktree):

- judge-f.tsv:19 -- `A3=DECLARED-EXCEPTION ... worst_verdict=UNDETERMINED worst_rule=R13`; why: "the legacy root
  code home R1 and R16 both name and carve out until the pipeline it serves moves, so home and naming read
  DECLARED-EXCEPTION rather than VIOLATES."
- judge-g.tsv:19 -- `A3=VIOLATES ... worst_verdict=VIOLATES worst_rule=R1`; why: "the bucket's own name carries
  the refused short alias 'bd' rather than the sovereign LONG form (R1)."
- judge-h.tsv:19 -- `A3=VIOLATES ... worst_verdict=VIOLATES worst_rule=R1`; why: "R16's own census reads this
  code-beside-gold placement CONFORMANT on the principle, but the bucket name itself still carries the refused
  token 'bd'."

The canon coordinate this traces to: `infra/logic/02_DOCTRINE.md:171` -- R1's own `non-application` line names
the carve-out F leans on: *"the LEGACY root `code/` homes (R16), which stay until their pipelines move (row
LGIC_CANON-S1); a NEW code home is inside the grammar, in its code tier (N1; LGIC_NAMING v1.3)."* That
carve-out is stated as reaching the KEY's internal structure (the code home need not sit inside the new
code-tier segment yet) -- it is not written as exempting the bucket's own firm-form name, which is a
bucket-wide property (N2, `infra/logic/02_DOCTRINE.md:247`: "a data bucket name | `opal-data-{scope}` |
LONG") shared by every tier under `opal-data-bd/`, not something `code/` alone carries. The generated N1 text
at `infra/logic/02_DOCTRINE.md:223` makes the same point from R16's side: *"A legacy root code/ key grades
OUT-OF-PATTERN, its canonical_form the code-tier key; a verdict is not a mandate to move"* -- i.e. a legacy
code home still GRADES (it is not simply excepted from judgment), it is just not FORCED to move on that
verdict. R16's own non-application (line 528-530) states the general principle explicitly for the parallel
Lambda-artifact case: "R16 does not reach them; R1 grades their key" -- a carve-out from ONE rule's reach does
not carve the KEY out of R1's naming grammar.

Read together, the canon's own text supports G and H's application of R1 to the bucket name over F's read of
the carve-out as covering the whole plane, but the carve-out's own wording is compressed enough ("the LEGACY
root `code/` homes ... stay until their pipelines move") that F's broader reading is not frivolous -- it is a
genuine ambiguity in how far a "home" carve-out reaches versus a "bucket name" requirement, not a case where
one judge plainly misread a rule that unambiguously said otherwise. Whether the trace above is decisive is
3.0.0_SA_CVO's call, not self-graded here.

## The briefed-vs-unbriefed question

H (unbriefed) agrees with G (briefed) on 23 of 23 planes and disagrees with F (briefed) on exactly the one
plane F and G already disagree on. So on this tree H does not diverge from the briefed pair more than the
briefed pair diverge from each other -- F is the outlier here, not H. The full reasoning and its limits are
in `judge-compare-r3.md`'s prose section.

## Criteria

J11R3-AC1..AC4 run via `check_canon_r3.py j11-intersection|j11-rollup|j11-traced|j11-reach`, each PASS by
output (rc=0), verbatim outputs in the proof-of-spec instance's `acceptance[].output_evidence`.
J11R3-AC5 is JUDGMENT: recorded `UNVERIFIABLE-BY-INSTRUMENT` for `3.0.0_SA_CVO`, per the order.
