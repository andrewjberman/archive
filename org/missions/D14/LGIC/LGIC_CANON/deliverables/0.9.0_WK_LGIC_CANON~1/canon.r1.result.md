# LGIC_CANON.TO-CN-k-1 -- result (cell CN-k-1, round 1)

**Worker:** 0.9.0_WK_LGIC_CANON~1 · **Issuer:** 2.0.0_SA_COO~G · **Branch:** `wk-lgic-canon-1-1`, cut from CLOUD @`f95470f384`
**Artifacts commit:** `fa9212974e9c0759dfacc1abb4111542256df945` (LOCAL). It carries `infra/logic/02_DOCTRINE.md` v1.0,
the new `infra/logic/render_naming_section.py`, and rows `LGIC_CANON-W1-S1` and `-W1-S2` in the channel.
**Nothing live moves (DEC-9).** The schema and the registry were read and not written: `git diff` on both is empty.

## Premises re-grounded at the start

- The canon was v0.3 at the base. Its last touch was @`c9048873d1`, as the order says.
- `NAMING_SCHEMA.json` was v1.8 and still carried `firm_forms`, so v1.9 had not landed. Between the cut and the first
  commit, CLOUD's five commits after `f95470f384` touched none of the canon, the schema, the registry or the ledger.
- The seven criteria had a baseline before any edit, as a negative control. All seven read FAIL: `FAIL-K1-NO-CENSUS-LINE`,
  `FAIL-K1-NO-RENDERER`, `FAIL-K1-STALE-NO-RENDERER`, `FAIL-K1-NOENUM-NO-SECTION`, `FAIL-K1-S6-OPEN-ITEM` (3 of 9),
  `FAIL-K1-D10-POINTER` (0 of 3 absorbed) and `FAIL-K1-R1-CODE-UNQUALIFIED`. So the checker can tell v0.3 from v1.0.

## The criteria, run at `fa9212974e` on a clean worktree

Every invocation is `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py <sub>`,
with `<WS>` = `/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-1`.

| id | sub | deciding output | rc | denominator | status |
|---|---|---|---|---|---|
| K1-AC1 | `k1-census` | `PRINTED: 21 of 21  RECOUNTED: 21 of 21` / `VERDICT: PASS-K1-CENSUS-OK` | 0 | 21 of 21 rules | PASS-by-output |
| K1-AC2 | `k1-render` | `STAMP LINES IN THE SECTION: 1  --check rc: 0` / `VERDICT: PASS-K1-RENDER-FRESH` | 0 | 1 of 1 stamp; 135 section lines | PASS-by-output |
| K1-AC3 | `k1-stale` | `clean copy --check rc=0  doctored copy --check rc=1` / `VERDICT: PASS-K1-STALE-REFUSED` | 0 | 2 of 2 arms (clean passes, doctored refused) | PASS-by-output |
| K1-AC4 | `k1-noenum` | `LINES OUTSIDE THE GENERATED SECTION: 441  ENUMERATIONS FOUND THERE: 0` / `VERDICT: PASS-K1-NO-ENUM-OUTSIDE` | 0 | 0 hits over 441 lines outside the section | PASS-by-output |
| K1-AC5 | `k1-s6` | `ITEMS: 9  CLOSED OR NAMING A DECIDER: 9` / `VERDICT: PASS-K1-S6-CLOSED` | 0 | 9 of 9 items | PASS-by-output |
| K1-AC6 | `k1-d10` | `AXES DEFINED: 5 of 5  REGISTER SCHEMA LINE: True  D10 s.2/s.6 CITATIONS: 3  NOT MARKED ABSORBED: 0` / `VERDICT: PASS-K1-D10-ABSORBED` | 0 | 5 of 5 axes; 3 of 3 citations absorbed | PASS-by-output |
| K1-AC7 | `k1-r1code` | `R1 NON-APPLICATION LINES NAMING code/: 1  WITHOUT 'legacy': 0` / `VERDICT: PASS-K1-R1-LEGACY-CODE` | 0 | 1 of 1 line | PASS-by-output |
| K1-J1 | (judgment) | none: graded at L9 by 3.0.0_SA_CVO | -- | -- | RECORDED (judgment), no verdict |

## What the edit did, per item of the cell

1. **Census line.** Section 0 carries `RULES CARRYING ALL THREE PARTS: 21 of 21` on its own line. No rule lacked a part at
   v0.3, so no rule text was added for item 1.
2. **Generated section.** It sits in section 3 under `### A3 NAMING -- THE NAMING SCHEMA, GENERATED`, after R3. It holds:
   - N1, the key grammar;
   - N2, the firm forms and the per-slot table;
   - N3, the resource grammar, its last slot, the kinds by type, the cadences and the other grammars;
   - N4, the refused tokens;
   - N5, the grade.

   About the renderer:
   - It stamps each file it read, and the hash is the CRLF-normalised SHA-256.
   - `--check` fails when a stamp's hash differs from the live file, and fails when the section's bytes, CRLF-normalised,
     differ from a fresh render.
   - `--write` keeps the canon's line endings. It refuses to write to a path that is one of its inputs.
   - It adds one override the order did not name, `--registry PATH`, to exercise the registry branch.
   - It reads `firm_forms` while the field exists, and otherwise the registry's FIRM rows.

   The registry branch was exercised on scratch copies under `<WS>/.scratch/`, with a schema whose `firm_forms` was
   removed. The section then read *"Firm forms read from the FIRM rows of the scope registry"*, with two stamp lines (the
   schema and `infra/logic/registry/scopes.json -`). `--check` returned 0 against that scratch schema, and 1 against the
   live schema. That is the G-V19R re-render the issuer's drain runs, shown to work before GROUP V19 lands.
3. **No enumeration outside.**
   - R1's grammar strings and its firm-form list are gone. R1 cites N1 to N5.
   - The struck collapse clause is kept as prose, without its grammar strings.
   - The section 1 rows for tier, firm, code home and state now point at the section. This is row W1-S1.
4. **Section 6.**
   - Per-scope shape and the EC2 threshold name `decider: Andrew`. The per-scope item also carries RULED for today's
     table: v0.2 TICKED, *"Nothing on this table is open"*, as quoted in PRD DEC-3.
   - The pause lift is struck as RULED, citing PRD DEC-4.
   - The ADVI routing clause names `decider: 1.0.0_SA_CTO`, because PRD DEC-10 carries it unresolved.
   - GAP-1 and GAP-2 carry RULED, pointing at R21 and at R16's non-application.
   - The three items already struck are unchanged.
5. **D10 absorbed.**
   - The section 2 heading and R20's authority now read *absorbed at v1.0 ... provenance, not a pointer*. So does the
     section 4 schema line.
   - Section 2 gains "Five axes are canonized, not one", and D10 s.2's canonical pattern as a tier-by-tier table. Each
     row names the rules that now carry it. On platinum's home, the table states R6's refinement (`e29a895ce3` card 1).
   - Section 4 gains D10 s.6's failure mode, "an exception list that only grows is how the pattern dies", and its
     Rule-24 clause.
6. **R1's non-application** names *the LEGACY root `code/` homes (R16), which stay until their pipelines move (row
   LGIC_CANON-S1)*. A new code home is the code tier (N1).
7. **Section 4** keeps the `PERMANENT | CONDITIONAL` schema line and holds no entries. It points at
   `06_CONFORMANCE_LEDGER.md` section 6. Three census tags that pointed at the old section 4 copy now point at the
   ledger: R6's X7, R7's X2 (it read "register entry owed", while X2 is GRANTED), and R20's "zero entries exist today".
   R20's census now says the canon keeps no count, so no second number can drift.
8. **Header and change log** read v1.0. The header's "the ~16:1xZ pause stands" now reads "lifted by name (section 6)",
   to match item 4.

## For L9 (K1-J1, not self-graded)

- Two choices here are the worker's, not the order's: the ADVI clause's decider (1.0.0_SA_CTO), and the RULED marks,
  which cite the PRD's DEC-3 and DEC-4 rather than the tick-list or the card record.
- The section 1 rewording (row W1-S1) changes words, not any rule.
- The ledger's X6 has axis `tenancy`, outside A1-A5 (row W1-S2). A judge who applies section 4's schema to the ledger will
  meet it.

## Rows filed

- `LGIC_CANON-W1-S1`, OBSERVATION, INERT: the section 1 vocabulary contradicted the generated tier list and the code
  tier, and was aligned.
- `LGIC_CANON-W1-S2`, OBSERVATION, INERT: the register's two carriers had diverged by X6, and X6's axis `tenancy` is
  outside the A1-A5 schema.
