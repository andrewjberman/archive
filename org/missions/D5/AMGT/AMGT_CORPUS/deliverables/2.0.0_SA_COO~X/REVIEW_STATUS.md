# Review handoff, 2026-09-23

CTO relay 24946 reports CVO **I4 PASS at offline-exercise plus retained-data-read**.
It asks whether stale is covered by `changed_input_before_rebuild`. Inspection
of the pinned builder and fixture confirms that exact mapping: the pre-rebuild
continuation has `current=false`, the rebuilt continuation has `current=true`,
and the builder asserts both. Explicit mapping is now in `INTERFACES.md` and
was returned through CTO for CVO. This is input-change staleness, not TTL expiry.
R consumer and S01 replay remain open; final journey remains NOT_EVALUATED.

H independent review `1c877a8c87` grants **routine source/offline PASS** for
exact implementation pin `dc2c0193ef`, superseding `ce57bef1c2` at that pin.
All ten independent scanner controls, 110 supplied scanner/typed tests and
5,040 period permutations pass. H matched all 28 census files to the pin and
reproduced 27 named write-like calls with zero library flags. The bounded
named-operation/origin model does not establish arbitrary-Python mutation
absence. H checked runtime exercise AST equality but did not rerun the live
exercise. CVO's I4 grade is recorded above; live integrity/final journey and
R integration remain separate. S01 full-population replay is NOT_EVALUATED.
Pinned evidence references and byte hashes are recorded in
`evidence/H_C_ROUTINE_PASS_dc2c0193ef.json`. Earlier failures below are history,
not the current verdict for `dc2c0193ef`; their original evidence is retained.

H review `ce57bef1c2` confirms eight earlier independent controls fixed at
`5812bd0dea`, but reproduces function-default and class-read-before-assignment
false-safe rows with recording fake open (no filesystem writes). Scanner FAIL
was the independent verdict for that pin. The repair separates definition
headers from body evaluation scopes, including nested default lambdas and the
outermost comprehension iterable; class bindings conservatively retain outer
origins. Twenty-four new controls pass, focused suite 91 and full corpus 202.
`evidence/SCANNER_EVALUATION_FIX.json` records the two executed fixtures and
unchanged runtime exercise ASTs. H subsequently reviewed the repair as above.

H's 17:48:27Z re-review confirms the original three controls fixed but FAILS
`f28faad15b` for comprehension, loop and unpacking rebinding. The next candidate
collects binding contexts conservatively, isolates comprehension targets,
tracks enclosing walrus assignments and invalidates cross-scope rebindings.
Related with/except/pattern/import/definition/augmented/delete forms are tested;
ambiguous import aliases retain known write candidates. Unpacked open keywords
cannot assume read mode. Twenty-nine more controls pass; full corpus 178 PASS.
This was producer evidence awaiting independent H re-review. See
`evidence/SCANNER_BINDING_FIX.json`; earlier failures remain in the record.

H review `b04336c4d8` FAILS the original static census in `d382f2a30e` for
lambda/class-body omissions and safe-global inheritance over parameters.
That static zero-write claim is withdrawn. Corrected scanner candidate covers
those lexical scopes, closures and argument kinds, with 13 new controls and
149 corpus tests passing; later H reviews are recorded above. The copied-library
exercise is not invalidated by the static instrument defect. H independently
PASSed period order across 5,040 permutations. Observation AMGT_CORPUS-Z-S7
records the defect without inferring an actual library mutation.

CTO message 24868 (17:29Z) supersedes the original reviewer assignment:
H reviews C, R reviews H, C reviews R while S lacks activation. Sent the
concrete corpus pin to H and requested R's incident-repair candidate. Prior
H reviews below were completed under the earlier assignment; they remain
evidence and do not create a reciprocal future review arrangement. All
ungraded boundaries remain NOT_EVALUATED. S01 stays with S.

Corpus implementation and execution evidence: LOCAL `d382f2a30e`.
Canonical surprise carrier and inventory correction: LOCAL `50175288e9`.
The latter changes no corpus implementation or interface. Canonical row gate
checked both S5/S6 observations; they remain UNDER_INVESTIGATION for CVO.

CTO 24841 restores C01 PASS at ACTUAL EXERCISE ON RETAINED BYTES. The protected
copy root is printed and asserted, read succeeds, writes fail, all 123 retained
byte checks succeed, and zero actual S3 PUTs are delegated. The conditional-PUT
transport seam is disclosed; no live PUT-path acceptance is claimed.

S's exact 20260923T172333Z reply confirms routine review NOT_STARTED: its own
chat authorization still requires a task order. S also has no S01 implementation
or new identity pin. Routed reviewer/owner resolution to CTO; C cannot authorize
another session. New-identity C02 replay is therefore NOT_EVALUATED. Current
reconciliation remains 351 files / 93 folders, 123 admitted sources, 33 resolved
and 60 unresolved folders. All 123 admitted lineages match retained bytes.

R's exact 20260923T172610Z reply acknowledges I4 examples and keeps consumption
open behind its serving incident repair. CVO integrity/interface review was
requested with the concrete pin. Neither review nor full-program closure is
inferred from the producer packet. No shared-branch push or deployment occurred.

C's assigned H cross-reviews are separate:

- Reader `8534a66eca`: routine PASS; evidence in corpus candidate `d382f2a30e`.
- Producer `ac4316c447`: routine PASS at review commit `d8cf72e32a`; 102
  producer/reader tests, six independent controls, and a subsequent 26-test
  shared price-generation regression PASS. No live or browser acceptance.
- Delivery repair `4f3fdff0d5`: routine source/offline PASS; 16 uploader/guard
  tests and independent guarded replay of all 21 selected local records out
  of 118. Exactly 42 fake objects created, repeat creates zero, occupied planned
  key refuses overwrite, and SQLite hash unchanged. No live append was run.
  Initial subprocess poison caught Python's local Windows version probe; the
  final exercise preloads that dependency, then poisons external operations.

The load skill's canonical messaging helper delivered review requests and ACKs
under exact seat `2.0.0_SA_COO~X`. Launcher helpers were not duplicated.
