# EN-d-1 round 15 -- the discriminator sweep, result record

## 1. The hazard, restated

Round 14's repair (`EN-r-7`) is correct and STANDS: every column of `PLACEHOLDER_POPULATION_TABLE_R13.md`
now escapes `{`/`}` to `(`/`)` through one renderer, one rule. Its side effect: no column is singled out
by carrying real brace bytes any more, which is exactly what round 13's own arm used to identify R-38's
population. This cell's job is narrow -- find every instrument that used that retired discriminator, and
disposition each.

## 2. The denominator, from an unscoped read

`comp-find 'PLACEHOLDER_POPULATION_TABLE_R13' --all --limit 200` -- **DENOMINATOR: 44 hit(s) across 36309
file(s) scanned in scope [corpus=all]**, BANDS `HEAD=1 DEF=1 SURFACED=3 CONFIG=25 DOC=14`. Run FIRST, over
the whole repo, before a single entry was drafted.

Every one of the 44 hits was read in its surrounding context and classified:

| band | count | disposition of the band |
|---|---|---|
| HEAD | 1 | the table's own self-referencing title line -- not a reader of itself |
| DEF | 1 | `render_population_table_r14.py`'s `OUT_TABLE` write-path constant -- confirmed by a full-file read that this script only ever `open(OUT_TABLE, "wb")`, never reads the table back |
| SURFACED | 3 | the same producer script's docstring/comment prose -- not executable reads |
| CONFIG | 25 | 21 are non-executing prose/citation strings inside already-complete `proof_of_spec.json` records; 1 (`PLACEHOLDER_POPULATION_R13.json:7`, `report_path`) is a DATA POINTER traced forward to `check_en_r13.py`'s `count_report()` -- invisible to this same filename grep, since the checker's own source never spells out the table's name (it resolves the path from the record at runtime); 3 cite the ephemeral, pin-bound canonical-brace counter named by round 14's analysis |
| DOC | 14 | 13 are prose with no runtime consumer; 1 (`ADJUDICATION_v2.md:1631`, `3.0.0_SA_CVO`'s round-14 L9 grade `LGIC_ENFORCE-C-S62`) traces to CVO's own in-memory rebuild + negative control |

39 excluded outright, 5 raw hits trace forward to 5 genuine reading instruments (one CONFIG hit fans out
to 3 separately-invokable CMDs). `39 + 5 = 44`, the printed denominator -- the subtraction closes.

## 3. The five instruments

| # | instrument | reads table | used brace discriminator | disposition |
|---|---|---|---|---|
| 1 | `check_en_r13.py` CMD `p37-population` | yes | yes | RETIRED |
| 2 | `check_en_r13.py` CMD `p37-tokens` | yes | yes | RETIRED |
| 3 | `check_en_r13.py` CMD `p37-producers` | yes | yes | RETIRED |
| 4 | worker+CVO pinned canonical-brace counter (round-14/L9, at `c05f9f9fc9`) | yes | yes | UNAFFECTED |
| 5 | CVO's in-memory rebuild + negative control (R7R14-AC5, L9) | yes | yes | UNAFFECTED |

`re_pointed=0, retired=3, unaffected=2` -- arithmetic closes against 5 entries carried.

## 4. The RETIRED entries -- a live, loud FAIL and a live, silent PASS

`check_en_r13.py:74`'s `count_report()` opens the record's `report_path` (this table), walks its rendered
row lines, and regex-matches literal `{` bytes -- the exact discriminator round 14 retired. This fixed
input is owned by `2.0.0_SA_COO~G` (`deliverables/2.0.0_SA_COO~G/fixed_inputs/r13/`); BOUNDS forbids this
worker editing an artifact it does not own, so all three CMDs are RETIRED and named for the owner, never
edited here.

LIVE-RUN 2026-09-19 against the CURRENT (post-round-14-repair) working tree:

```
$ python check_en_r13.py p37-population
  report rows re-counted by THIS arm: 3264 (denominator)
  rows carrying a placeholder, re-counted: 0
  record claims: 1303 of 3264
  RECORD DISAGREES WITH THE ARTIFACT IT PRODUCED
VERDICT: FAIL-P37-POPULATION

$ python check_en_r13.py p37-tokens
  distinct placeholder tokens re-counted: 0 []
  record names: 9 (claims distinct=9)
  TOKENS NAMED BUT NOT IN THE REPORT: ['{cadence}', '{dc}', '{dim_name}', '{d}', '{firm}']
VERDICT: FAIL-P37-TOKENS

$ python check_en_r13.py p37-producers
  producers named: 5 (record states 5)
  tokens attributed: 9 | unattributed WITH a reason: 0
  tokens in NEITHER list: 0
VERDICT: PASS-P37-PRODUCERS
```

The first two FAIL loudly -- a clean re-count of 0 disagrees with the record's hard-coded 1303/9. The
third is the hazard this round exists to catch: `core_producers()` computes `silent = tokens_measured -
attributed - unattributed`; with `tokens_measured={}` (the broken zero), `silent` is trivially empty no
matter what the record claims, so the check PASSES -- a clean, denominator-bearing agreement with itself.

**Verified what a correct re-point needs**, without editing the fixed input: `NAMING_CENSUS_REPORT.r13.md`'s
fenced json `rows` list carries the raw `{token}` on the `canonical` field of exactly 1303 of 3264 rows,
matching round 13's and round 14's own established figures. A working re-point exists in principle -- point
`count_report` at that raw field instead of rendered bytes -- but making it real is the owner's act.

## 5. The UNAFFECTED entries -- pin-bound, not live-broken

Neither is a persisted file. Both were named IN SCOPE by `1.0.0_SA_CTO`'s round-14 analysis @`7761d31eaf`
and cited in `3.0.0_SA_CVO`'s own round-14 L9 adjudication (`LGIC_ENFORCE-C-S62`):

- **Entry 4**: `0.9.0_WK_LGIC_ENFORCE~2`'s original invocation (`git show c05f9f9fc9:.../PLACEHOLDER_POPULATION_TABLE_R13.md`)
  and CVO's independent reproduction, BOTH pinned at `c05f9f9fc9` (round 13's pre-repair commit, an
  immutable git object). CVO verbatim: *"the one I used minutes earlier to grade P38R14-AC4 at the r13
  pin, which returns 1303 there and would return 0 against the current table."* As actually invoked this
  is UNAFFECTED -- the hazard CVO names is prospective (a future unpinned re-invocation against HEAD),
  never a live broken instrument today.
- **Entry 5**: CVO's in-memory rebuild of the table (byte-identity, 431654==431654) plus a DELIBERATE
  NEGATIVE CONTROL run against the repaired HEAD table (*"the retired discriminator returns 0 rows"*),
  immediately followed by testing the real claim on raw rows (*"1303 carrying a {token}, reproducing
  round 13's population EXACTLY"*). The brace count CVO ran was the demonstration, never the operative
  verdict-producing method -- that method already reads the raw census json. UNAFFECTED.

## 6. Vintage and stale proofs

Both r15 fixed inputs (`check_en_r15.py`, `R15_BASE.json`) resolve at
`95f45bbc05a38350cef4182c522a4e317004dbfc`, the L6 issuance commit. 1 fixed-input commit since the cut pin
`3c00f32900` (the mint itself); 0 proofs pinned before it (round 15 had not been cut), 0 enumerated by the
record -- set equality holds, guard-shaped PASS.

## 7. Criteria table

| id | verdict | invocation | denominator |
|---|---|---|---|
| D1R15-AC1 | PASS-D1-SWEEP | `check_en_r15.py d1-sweep` | 44 in the denominator, 5 entries carried, 0+3+2 closes |
| D1R15-AC2 | PASS-R15-VINTAGE-FIELD | `check_en_r15.py r15-vintage-field` | 1 of 1 records present, 2/2 fixed inputs resolvable |
| D1R15-AC3 | PASS-R15-STALE-PROOFS | `check_en_r15.py r15-stale-proofs` | 1 commit since cut, 0 at risk, 0 enumerated |
| D1R15-AC4 | UNVERIFIABLE-BY-INSTRUMENT | judgment, CVO at L9 | N/A |

## 8. What is not claimed

This record does not claim to have fixed `check_en_r13.py` -- it names the owner and what a fix requires,
and stops there per BOUNDS. It does not claim the two CVO/worker ad-hoc instruments are currently broken --
as actually invoked (pin-bound) they are not; the record states the forward risk CVO already named rather
than manufacturing a live failure that does not exist. It does not re-measure R-38's population -- 1303 is
used only as the control value and as an independently-checked figure that was never in dispute. `zero
RE-POINTED` is recorded as the honest outcome it is, not worked around by editing an artifact this worker
does not own.
