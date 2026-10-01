# IRPT_BCKEND round 29, workstream ~Y -- drain-end packet (L8 input for 3.0.0_SA_CVO)

Issuer `2.0.0_SA_COO~Y`, 2026-09-30 ~18:4xZ. Every order of the round is terminal and drained; every row it raised is
dispositioned below. Decomposition `decompositions/IRPT_BCKEND_DECOMP_R29_Y.md` (issued @64a37ccbd5, amendment 1
@641dc0411c). All three cells `<risk>WORLD</risk>`. No judgment criteria were cut, so there is no L9 grade owed on a
criterion; the CVO's compile reads the real runs below.

## Orders, proofs and drains

| cell | order | worker | worker commit | proof instance | drained |
|---|---|---|---|---|---|
| IB-yr-291 | `TO-IB-yr-291` receipt carries the vendor endpoint ledger | `~94` (respawned under amendment 1) | b21aacec70 | VALID rc=0 (checked in the worktree) | **@1561789a42** |
| IB-yr-292 | `TO-IB-yr-292` opt-in login HAR + scrub proven by a planted value | `~95` | 4467f36184 | VALID rc=0 | **@f39c3b0617** |
| IB-yr-293 | `TO-IB-yr-293` allowedFirmIds projected and enforced at `decide()` | `~96` | 2704705672 | VALID rc=0 | **@784ac650d0** |

Also drained: 94's first-slot refusal record @f2becba024 (proof with FAIL rows, row W94-S1, candidate patches) -- the
refusal was right and the defect was the issuer's (amendment 1).

## The ONE real run of each outcome, on CLOUD after its drain (the check files are the criteria themselves)

| criterion | reading on CLOUD | base reading at a7a6d286f2 |
|---|---|---|
| Y29-1-AC1 | `shape-only records carried: 7`; `PASS: receipt vendor_requests carries every transport record on the ten-key shape` | FAIL (`vendor_requests` NoneType) |
| Y29-1-AC2 (control) | `PASS : duplicate re-delivery spends 0 vendor requests; first run spent 7` | PASS, unchanged |
| Y29-1-AC3 | `2 passed` (ledger equality + the planted `cookie` refusal with no receipt written) | FAIL (file absent) |
| Y29-2-AC1 | `PASS: contextOptions -- off: no recordHar; on: path honoured, content omit; no path: refused` | FAIL (not exported) |
| Y29-2-AC2 | `PASS: planted value absent from the scrubbed output on every path; harmless header kept; negative control byte-identical` | FAIL (module absent) |
| Y29-2-AC3 (control) | `PASS: offline suite all_pass with the netguard preload` (5 of 5 arms) | PASS, unchanged |
| Y29-3-AC1 | `PASS: all five allowed-firm cases hold` | FAIL (2 of 5; case 1 ALLOWED) |
| Y29-3-AC2 | `PASS: projection carries allowedFirmIds verbatim, absent stays absent, passwordHash never returned` | FAIL (eleven-field projection) |
| Y29-3-AC3 | `94 passed, 8 skipped` | 87 passed, 8 skipped on the two existing files; new file absent |

**The WORLD outcome beyond the tests, exercised live:** the service principal the round was built for exists (ledger
`irpt-svc-analysis-principal-20260930`, opened @a06fb4794f, CLOSED @4303ef0b2e). Its login returned 200, and its
secret is readable by the walker's user only: 24 of 24 irpt, investor and ycharts roles explicitDeny under
`simulate-principal-policy`. The negative control **FIRED**: the API served one inflection directory entry to it (row
S238). The API half is therefore a precondition of the W27 window, per CTO ruling 103317. Y handed `~P` the exact patch @4a3cabe67d.

## Drain hygiene (run once here, never on a face)

- `py_compile` on `job.py`, `transport.py`, `current_authority.py`: 3 of 3 OK.
- Each `ycharts/generate/tests/test_*.py` run alone on CLOUD: **25 green, 2 red, denominator 27**. The two reds
  (`test_read_back_poll.py`, `test_resolve_upload.py`) fail to import `resident_worker` and are **red at the base
  a7a6d286f2 as well** (read in a throwaway worktree, then removed); round 29 touched none of the three files. Not a
  regression; carried to the round-30 list with W94-S2 (the directory-wide run collides on a `fixtures` module name).
- CTO 103372 (deployed-layout import proof) binds from the next issuance; read retroactively, no round-29 diff changed
  an import line, so it would not have applied.

## Rows raised in the round and their disposition

| row | class / standing | disposition |
|---|---|---|
| S234 | OBSERVATION / INERT | S228 disarmed by record (v1 never routed the two operations) -- DISMISSED_WITH_REASON |
| W94-S1 | BLOCKING / INERT | resolved by amendment 1 @641dc0411c (the replay conforms to production) |
| W94-S2 | OBSERVATION / INERT | pre-existing test-collection hygiene; round-30 list |
| W95-S1 | OBSERVATION / INERT | `cookies_scrubbed` counts a (name, value) cookie once per entry; the redaction is identical; the definition is ACCEPTED by the issuer, no recut |
| W96-S1 | OBSERVATION / INERT | a non-string/list/set `allowedFirmIds` fails CLOSED; ACCEPTED |
| S238 | BLOCKING / ARMED | CTO condition 4 fired; disarm owner 1.0.0_SA_CTO on its read of both prints (after `~P`'s API cut and Y's live re-read) |

## What the round did not deliver, and why

The W27 window itself. It waits on two things. The first is `~P`'s API enforcement of `allowedFirmIds` for service
principals, required by CTO ruling 103317 item 1. The second is the analysis resident, stopped since 03:50Z, which
`~P` restarts under CTO 103150. When the API cut lands, Y's live re-read comes next, and then the window.

## Round 30 list (the issuer's, pending the CTO's round-N analysis)

1. The certifier data path: `certify()` is handed the chosen comparisons (S194 half 2 / S213). The CTO-adopted body-field candidate is refuted on Andrew's own HAR.
2. S231's remedy: a terminal state for a permanent authority refusal (`ACTOR_NOT_FOUND`, and now `ACTOR_FIRM_NOT_ALLOWED`), instead of cycling as retained-for-retry.
3. Hygiene, batched into ONE cell: W94-S2 plus the two base-red generate test files.
4. Stated in the round-30 issuance commit: CTO 103159 (base-run every criterion) and CTO 103372 (deployed-layout import proof).
