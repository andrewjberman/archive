# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-s-7`

Worktree `/c/tmp/wk-irpt-1-3`, branch `wk-irpt_bckend-1-3`, re-cut from `5236a7603d`. Third
order in slot ~3, after IB-s-6 drained and IB-s-3 merged.

## Order of acts

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-irpt_bckend-1-3`, HEAD `5236a7603d`;
   `test -d org && test -d .tools` -> `TREE-OK`. Session-serial line written (this cell
   deploys nothing; the line is in place anyway).
2. **Read the face FROM DISK**, not from the cut: the ISSUER AMENDMENT block and the
   `(amend)` arm are present (16,629 bytes), which is what the hand-off said to check.
3. **Re-grounded the amendment's surface before building.**
   - `_authz/enforce.py` -- `guard()` MARKS the wrapper (`__irpt_guarded__`), which is what
     makes `unguarded_routes()` a census rather than a hope; `FirmBinding.proves()` checks the
     directory artifact's own `firm_id_opaque`; `cache_key_for()` is PUBLIC and raises
     `KeyRefused` whose message names parameter NAMES only. All four are called, none
     reimplemented.
   - `_authz/tests/fixtures.py` -- `DIRECTORY`, `OWNERSHIP`, `POLICY`, `Deps`, `headers()`
     reused, so this cell's binding arm is proven against the SAME artifact shape the
     enforcement library's own tests use.
   - `_contracts/AnalysisRequest.schema.json` and `StatusEnvelope.schema.json` -- the shapes
     this cell produces, and the source of row W3-S6.
   - **The amendment's fallback object was censused and is ABSENT**: `comp-find --name
     'routes.json'` over 32,481 files returns ONE hit, this worker's own unrelated IB-s-8
     YCharts fixture. Filed as W3-S5; the arm was then satisfied by controlling the CENSOR
     rather than by reporting an empty set.
4. **Built** `parse.py`, `corrections.py`, `settings.json`, the synthetic specimens with their
   SYNTHESIZED manifest, and 15 package tests.
5. **Found a bug in my own first draft before the battery ran.** An `.xlsx` omits empty cells,
   so positional indexing read the Total row's `100%` as the description and lost the stated
   total -- while every CSV specimen passed, because a CSV has every cell. Re-addressed
   everything by COLUMN LETTER and added the test that asserts it on the xlsx specimen.
6. **Committed the build FIRST** (`5708161e8e`), then ran the graded battery, so the graded
   output was produced from committed bytes -- the rule my own IB-s-6 turn learned the hard
   way when eleven uncommitted lines had already produced a graded output.
7. **Graded.** `S7-AC1` -> `IBS7-PARSE-DETERMINISTIC`, 6 of 6 arms, rc 0.
8. **Controls.** Two monkeypatch mutants (both fired; M2 returns a portfolio the advisor never
   sent and emits zero proposals) plus the one that ships inside arm (b). Determinism: two
   runs, 126 lines, byte-identical.

## Two premises that did not hold, both filed rather than worked around

- **`IRPT_BCKEND-W3-S5`** (ARMED) -- the `routes.json` the amendment names as the guard
  census's fallback does not exist in the corpus, and this cell ships no handler, so that
  fallback was the arm's whole content. Disarmed for this cell by printing the 0-of-0 census
  AS VACUOUS and pairing it with two controls on the censor itself; the fallback's meaning is
  the issuer's, graded by the CVO at L9.
- **`IRPT_BCKEND-W3-S6`** (INERT) -- the face and the PRD row name the `StatusEnvelope` value
  `needs-correction`; the generated contract's `state` enum is closed and carries
  `NEEDS_CORRECTION`. The contract's spelling is emitted and the difference is stated at the
  constant rather than resolved silently.

## Instruments, and which are independent

- `comp-read --for` on `enforce.py`, `fixtures.py`; `comp-read --enumerate` on `REFUSAL_CODES`.
- `comp-find --name` and a content census for the route-table question -- the read that turned
  the amendment's fallback from an assumption into a measurement.
- `comp-adversary compose` on `parse.py`: declaration written, read-vintage `5708161e8e`. It
  reports `ZERO MACHINE-EXTRACTABLE PINS` -- a real finding about this deliverable, carried
  unedited: the parser cites its sources in prose, not in `file:line @commit` form.
- **openpyxl as an independent second implementation**: it WROTE the xlsx specimen, the
  stdlib reader READS it. Two different libraries, which is corroboration rather than a round
  trip through one.
- **Every arm carries its own negative**: (a) two parses compared as bytes; (b) the broken
  build; (c) the contract validator as a second judge of the same rows; (d) the tamper attempt
  and the unapproved substitution; (amend) the unguarded/guarded control pair.

## Bounds held

No live vendor call, no mailbox read, no deploy, no schedule, no monitor, no SES. No
cross-firm reach: every firm-scoped write binds through `FirmBinding` and refuses rather than
returning empty. No secret value and NO REFUSED VALUE in any artifact -- the refused value's
count is printed, never the value. `_keys` is not edited (it is not in this order's
`<paths>`). Every file written is inside the `<paths>` grant or this worker's deliverables
folder.
