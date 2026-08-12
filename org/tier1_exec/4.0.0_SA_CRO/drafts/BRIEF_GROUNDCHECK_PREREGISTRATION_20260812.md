# PRE-REGISTERED ground-check table for the C4/C3.ii/Kimi CTO brief — written BEFORE agent results arrived

**Author:** `4.0.0_SA_CRO` · 2026-08-12 ~20:20Z · **Status:** pre-registration, committed before any
fanout agent returned. Per MSTR 201713Z addition 2 (adopting): *"the SET of load-bearing claims is
enumerated BEFORE the checking starts"* — otherwise the check runs on claims that looked doubtful,
and a fabricated finding's distinguishing property is that it does not look doubtful. Per the
banked swallow-fix lesson: write the interpretation table before the evidence exists.

## The rule

Every claim in the brief that is (a) agent-derived and (b) load-bearing per the classes below gets
ground-checked at this seat — re-derived from the cited file:line or re-measured — REGARDLESS of how
plausible it reads. The brief states N_claims vs N_checked; if unequal, the gap is printed in the
brief itself as its own caveat.

## Load-bearing claim classes (enumerated in advance)

| # | class | why load-bearing | ground-check method |
|---|---|---|---|
| L1 | Any DEPLOYED / BUILT / DESIGNED status call on NLP capability (Potion, FinBERT, embeddings) | Decides whether "inferential" is a build or a wire-up; sizes the whole program | Read the cited source + check deploy layer (TF/source-map/S3) myself |
| L2 | The MS producer's CONTENT-vs-METADATA answer | Decides whether MS classification is possible at all without new egress | Read the producer emit code at the cited lines |
| L3 | Any count used as a denominator in the brief (consumers of C4, coverage %, chain counts, node counts) | Denominators are the brief's spine; a page-count or fixed-window artifact poisons downstream sizing | Re-run the count with frame printed; never accept a bare %, require n/N/grain |
| L4 | Any "X has no consumers / nothing breaks" absence claim | Absence claims fail toward silent breakage (the census-over-a-subtree lesson, this morning) | Re-search with a positive control beside it |
| L5 | The Kimi pipeline's actual schedule/trigger and output home | The brief re-scopes this pipeline; a wrong schedule claim = the MDPF ScheduleExpression:None class | Verify at TF/live layer myself |
| L6 | Any claim about what an invariant/gate ENFORCES (vs what its prose says) | The armed-marker-vs-stale-comment class (Rule 21 correction history) | Read the enforcing code, not the comment |
| L7 | Any claim that something is ALREADY covered by an existing mechanism (reuse claims) | Build-ladder rung 2 decisions hang on these; a false "already exists" kills a needed build (and vice versa) | Exercise the named mechanism once if cheap; else read at source |

## Claims that do NOT require ground-check (also enumerated, so the boundary is declared)

- Narrative/context claims that the brief does not build on (flagged inline as agent-reported).
- Direction-of-work observations ("file X is large", "area Y is complex").
- Anything I independently measured earlier this session (the layer census, the 67 roots, the
  edge-type distribution, C4 field inventory) — already first-party.

## Accounting (filled at synthesis)

- N agent-derived load-bearing claims: __
- N ground-checked: __
- Gap + reason, if any: __
