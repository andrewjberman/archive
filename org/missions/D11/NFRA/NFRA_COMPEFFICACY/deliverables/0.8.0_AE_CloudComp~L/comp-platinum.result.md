# comp-platinum — T-24 result

Implementation `f7a677296427e472c312a4253c1f3bf74adf79d7` is **LOCAL**. It adds a single
`--budget` carrier shared by transform, routes, and the pipescript/DAG component to `page`.
The composite is defined as portal component dataflow → routing table → firm gold DAG. Its
coverage universe is **22 component files** from `portal/src/pages`; output names components by
stem, so four `index` stems are collision-prone and are disclosed as a named limitation.

## Measured evidence

- Default summary: 22 component files, with fetch/transform/S3/API-GW counts per component.
- FWD-9 at `2.0.0_SA_COO`, descendant HEAD `a0fdd044a4` with implementation ancestor rc=0:
  `comp-platinum page FactorTilts --budget 0` → rc=0, `FULL-STACK TRACE: FactorTilts`, BD
  firm/bucket, `FETCH: getFactorTiltsSnapshot()`, and `WITHIN BUDGET: scanned 3 of 3 component;
  budget: unbounded (--budget 0), used 3.203 s`.
- Planted local controls: an absent component returns rc=1 plus
  `ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS`; a tiny budget returns execution rc=0 plus
  `BUDGET REACHED`, `ANSWER-STATE: PARTIAL_OR_BLIND`, and a per-component deferred bucket;
  FactorTilts at `--budget 0` completes 3/3 with the zero-deferred bucket.

## Honest criterion state

T24-AC1, AC3, AC4 and AC6 have measured evidence. AC2 is incomplete: the engine carries the
absent and partial boundary states but does not yet provide planted PRESENT_WITH_ZERO_RESULTS and
NOT_APPLICABLE modes for this composite. AC5 is incomplete: the new file-grain battery has three
controls (direct and pytest 3/3) but no executable red mutant per arm. No content-bearing trace is
mislabelled as a zero-result answer; FWD-9 correctly printed no answer-state token for FactorTilts.

Push measurement: `origin/CLOUD=351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee`,
`git merge-base --is-ancestor f7a6772964 origin/CLOUD` rc=1. This seat did not push.
