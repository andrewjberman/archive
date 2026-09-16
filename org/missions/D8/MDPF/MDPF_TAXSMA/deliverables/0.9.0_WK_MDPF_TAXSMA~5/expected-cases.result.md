# MDPF_TAXSMA.TO-TX-v-1 -- result (cell TX-v-1, round 1)

Worker `0.9.0_WK_MDPF_TAXSMA~5`, branch `wk-mdpf_taxsma-1-5`, worktree `C:/tmp/wk-taxsma-5`, cut at
`91b11ff0c9`. Artifacts committed at `86abd7d487` (LOCAL: `git ls-remote origin refs/heads/wk-mdpf_taxsma-1-5`
returned no ref, rc 0). Specification: PRD `671925aecc` s.4; data contract 0.5.0 read at `91b11ff0c9`;
decomposition `7f65001ab3` cell `TX-v-1`.

## What was built

| Artifact | Path | Role |
|---|---|---|
| Expected-case manifest | `data/mdpf/tests/taxsma/expected_cases.json` | 102 arms over PRD s.4 A01-A08; fixture world; 99-entry Decimal ledger; 18 readings |
| Authoring script | `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~5/author_expected_cases.py` | standard library only; reads PRD and contract through `git show` at the pins; regenerates the manifest byte-identically |
| Probe | `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~5/probes/tx_v_1.py` | one run per criterion; `--manifest` / `--script` take doctored copies for the mutant controls |
| Surprise row | `MDPF_TAXSMA-W5-S1` in `org/missions/D8/MDPF/MDPF_TAXSMA/surprise-channel/investigations/INVESTIGATION_v1.md` | PRD s.3.4 label UNCONFIRMED has no contract enumeration member |

Manifest shape: every arm carries `id`, `property`, `outcome`, `prd_clauses` (clause ids whose text is pinned in
`prd_clause_text`), `covers_members`, `surfaces`, `environment`, `executes_in`, `fixture_input` plus its
canonical-JSON `fixture_input_sha256`, `control` (`kind` DIFFERENCE or INVARIANCE; `engaged` and `disengaged`,
each an `input` delta list and an `expected_observable`; `differs_on` / `invariant_within` paths, or
`invariant_on` + `contrast_arm`), `expected_observable` (the engaged side) and `readings`. Every expected number
is `{"num": <ledger id>}`; the ledger records each Decimal operation as `worked` text.

The clause denominator is derived, not recalled: each PRD s.4 row is split into sentences, then at `; ` (rule in
the manifest's `segmentation_rule`), giving 54 clauses; 17 list clauses are further split into 74 declared
members, each a verbatim substring of its clause.

## Criteria (record runs at HEAD 86abd7d487, 2026-09-15)

| Criterion | Instrument | UTC | Deciding output | Denominator | Grade |
|---|---|---|---|---|---|
| TXV1-AC1 | `timeout 120 py -3.12 .../probes/tx_v_1.py AC1` | 22:31:44Z | `TOTALS: arms 102; clauses covered 54/54; list members covered 74/74` / `VERDICT: PASS-TXV1-AC1` | 54 of 54 clauses, 8 of 8 properties, 74 of 74 members | PASS-by-output |
| TXV1-AC2 | `timeout 120 py -3.12 .../probes/tx_v_1.py AC2` | 22:31:48Z | `LEDGER: 99 entries recomputed by Decimal ... 996 expected-number references (87 distinct), 0 unworked numbers`; AST `non-stdlib 0; engine-named 0; dynamic import/exec calls 0`; runtime `31 modules newly loaded; from the repository 0; non-stdlib 0`; `REGENERATION ... identical=True` / `VERDICT: PASS-TXV1-AC2` | 99 of 99 ledger entries; 8 of 8 imports stdlib; 0 of 31 runtime modules from the repository | PASS-by-output |
| TXV1-AC3 | `timeout 120 py -3.12 .../probes/tx_v_1.py AC3` | 22:31:52Z | `62 account-shaped tokens`; `30 fixture amount literals ... 27 declared synthetic values`; `334 workbook cells`; `15 forms ... hits 0` / `VERDICT: PASS-TXV1-AC3` | 62 tokens, 30 amounts, 334 cells, 15 real-identifier forms; 0 defects | PASS-by-output |
| TXV1-AC4 | `timeout 120 py -3.12 .../probes/tx_v_1.py AC4` | see block below | clause-to-arm map, member map, non-local arms, 18 readings | 54 clauses, 102 arms | RECORDED (judgment) -- no verdict; graded by 3.0.0_SA_CVO at L9 |

Per-property counts (AC1 output): A01 8/8 clauses, 13 arms; A02 5/5, 10; A03 12/12, 18; A04 3/3, 10 (9 local);
A05 6/6, 12; A06 4/4, 6; A07 11/11, 26 (25 local); A08 5/5, 7. Controls: 98 DIFFERENCE, 4 INVARIANCE (A01 10 / 3, A06 5 / 1,
every other property all DIFFERENCE).

AC3's limit, stated by the probe itself: no intersection with the protected live account population was run
(that population is outside this order's paths); the claim rests on construction (every account-shaped token in
the reserved 99 / 0099 block), a closed per-column cell vocabulary (SYNTH labels and enumerated values only, so no
name can enter), every fixture amount declared synthetic, and zero hits for the 15 real-identifier forms the PRD
and contract publish (masters, workbook site and item, account-shaped PRD tokens).

## Controls

**Mutants** (doctored copies in `<WS>/.scratch/`, fed through `--manifest` / `--script`; the committed files
were never edited):

| Mutant | Expected | Observed |
|---|---|---|
| every arm citing A04.c3 removed | AC1 FAIL | `clauses covered 53/54; list members covered 70/74` / `VERDICT: FAIL-TXV1-AC1 6 defect(s); first: clause A04.c3 has no arm` |
| ledger `L-TAX-D14` result 2680000.40 -> 2680000.41 | AC2 FAIL | `VERDICT: FAIL-TXV1-AC2 1 defect(s); first: ledger L-TAX-D14: recomputed 2680000.40 != recorded 2680000.41` |
| authoring-script copy with `import mdpf_category_registry` | AC2 FAIL | `non-stdlib 1; engine-named 1` / `VERDICT: FAIL-TXV1-AC2 3 defect(s); first: non-stdlib import mdpf_category_registry` |
| K1 raw key 12345678 and WB-BASE r2 Name 'Jane Doe' | AC3 FAIL | `VERDICT: FAIL-TXV1-AC3 2 defect(s)`: token 12345678 outside the synthetic key block; `Name='Jane Doe'` outside the closed vocabulary |

**Determinism:** all four criteria were run twice at HEAD 86abd7d487 on the same bytes; every output line other
than the VINTAGE timestamp is identical (4 of 4). AC2's regeneration arm also re-derives the manifest from the
authoring script and compares it byte for byte (LF-normalised) with the committed file: identical.

## Readings (the manifest's `readings`; the CVO's judgment covers them)

R1-R18 are listed verbatim in the AC4 block below with the arms that rest on each. The ones a second author could
fairly read otherwise: R1 (duplicate-row business_status left unasserted), R2 (expected_accounts null on an
invalid identity or unknown Traded), R3 (a date already proven by history keeps its complete value after a later
invalid Traded), R7/R11 (T-1 session rule and weekends), R9 ('deny capability access' exercised as AUTH_REQUIRED).

## Surprise filed

`MDPF_TAXSMA-W5-S1` -- OBSERVATION, INERT: PRD s.3.4 (`671925aecc` line 205) classifies additional custodian
candidates UNCONFIRMED; no contract status axis or reason code (`91b11ff0c9`) carries that value. A02-09 states the
candidate observable without a label.

## What this worker read, and what it did not do

Read: the task order; PRD `671925aecc` (whole); the data contract (whole); the decomposition's s.3 TX-v-1 cell,
s.6 and s.8; the investigation file; `org/standards/PROOF_OF_SPEC.schema.json`;
`org/surprise_channel/schemas/investigation_item.schema.json`; one sibling proof instance for shape
(`LGIC_CANON.TO-CN-j-2`). No TAXSMA engine module was opened or imported; no cloud, Graph or vendor call was made.
Not done (this order's bound): arm execution and output hashes (TX-v-2, TX-v-3), the non-local arms A04-10
(authorized dated-source reads) and A07-16 (TX-r-3), and the compiler-tool lenses beyond this order's probe.

## TXV1-AC4 output (record run, verbatim)

```
PROBE: tx_v_1.py AC4  manifest C:\tmp\wk-taxsma-5\data\mdpf\tests\taxsma\expected_cases.json
VINTAGE: HEAD 86abd7d487  manifest expected_cases.json sha256(LF) 4e4dc6889aa6f98a  at 2026-09-15T22:31:56Z
JUDGMENT INPUT: arm set against PRD s.4 @671925aecc (54 clauses, 102 arms)
  A01.c1 [A01-01] Full-sheet fixtures retain the existing 14 headers and seven projected fields: traded, funded-but-untraded, prospect, blank and conflict rows
      member 'traded': A01-01
      member 'funded-but-untraded': A01-01
      member 'prospect': A01-01
      member 'blank': A01-01
      member 'conflict rows': A01-01
  A01.c2 [A01-02] Flip only Traded No to Yes: current live count changes automatically
  A01.c3 [A01-03, A01-04] changing Ready or funding alone does not
      member 'Ready': A01-03
      member 'funding': A01-04
  A01.c4 [A01-05] Delete the matching Schwab record with Traded still Yes: live count stays, covered value fails and complete affected totals become unavailable
  A01.c5 [A01-06] Duplicate full keys count once but retain conflict
  A01.c6 [A01-07, A01-08] invalid YES identities and unknown identified Traded yield unknown complete counts, never vanished claims
      member 'invalid YES identities': A01-07
      member 'unknown identified Traded': A01-08
  A01.c7 [A01-09, A01-10, A01-11] Reordered/inserted rows and Bronze/Silver replay preserve all rows, fields and lineage
      member 'Reordered': A01-09
      member 'inserted rows': A01-10
      member 'Bronze/Silver replay': A01-11
  A01.c8 [A01-12, A01-13] failed Silver cannot create a complete empty cohort
  A02.c1 [A02-01] Full identities match in both directions
  A02.c2 [A02-02, A02-03, A02-04, A02-05, A02-06, A02-07, A02-08] suffix-only/masked/duplicate/malformed/master/strategy/transfer cases remain unresolved
      member 'suffix-only': A02-02
      member 'masked': A02-03
      member 'duplicate': A02-04
      member 'malformed': A02-05
      member 'master': A02-06
      member 'strategy': A02-07
      member 'transfer': A02-08
  A02.c3 [A02-09] Additional custodian candidates stay outside live membership
  A02.c4 [A02-02, A02-03, A02-04, A02-05, A02-06, A02-07, A02-08] Same fixture with the mismatch corrected changes the corresponding coverage result
  A02.c5 [A02-10] No private IDs appear in consumer/log outputs
  A03.c1 [A03-01] A new Traded Yes outside the original extent opens observed membership automatically with full protected source evidence and no CONFIRM_EFFECTIVE_MEMBERSHIP call
  A03.c2 [A03-02] With valid values, prove its inclusive first-observed UTC day
  A03.c3 [A03-03] its earlier date with no trustworthy state history stays TRADED_HISTORY_UNVERIFIED, never a complete zero
  A03.c4 [A03-04] Contrast a retained complete NO-to-YES history that proves earlier inactivity
  A03.c5 [A03-05, A03-06, A03-07, A03-08, A03-09, A03-10, A03-11, A03-12] Exercise explicit NO exclusive closure, reactivation, same-day ordering, idempotent replay, out-of-order refusal, invalid/blank Traded and removed/rekeyed claims
      member 'explicit NO exclusive closure': A03-05
      member 'reactivation': A03-06
      member 'same-day ordering': A03-07
      member 'idempotent replay': A03-08
      member 'out-of-order refusal': A03-09
      member 'invalid/blank Traded': A03-10
      member 'removed/rekeyed claims': A03-11, A03-12
  A03.c6 [A03-13, A03-14] Corrections retain old/new observations and cannot invent a flag or historical date
  A03.c7 [A03-15] Include a 2026-09-16T00:30Z boundary: it is Sep15 evening EDT but Sep16 UTC
  A03.c8 [A03-15] compare directly to session-date labels
  A03.c9 [A03-15] With retained prior state, a NO preserves Sep15 membership and excludes Sep16
  A03.c10 [A03-16] a YES with no prior history leaves Sep15 unverified
  A03.c11 [A03-17] Current live count changes immediately
  A03.c12 [A03-18] no local-time shift or invented weekend session
  A04.c1 [A04-01, A04-02, A04-03, A04-04, A04-10] Synthetic and authorized dated-source cases include cash, long/short exposure, margin and actual zero
      member 'cash': A04-01
      member 'long/short exposure': A04-02
      member 'margin': A04-03
      member 'actual zero': A04-04
  A04.c2 [A04-01, A04-02, A04-03, A04-05, A04-10] Result equals the existing canonical net-value basis to the cent, with source/date/boundary trace
  A04.c3 [A04-06, A04-07, A04-08, A04-09] Gross exposure, sales estimate, quarterly data and unverified accrual cannot replace it
      member 'Gross exposure': A04-06
      member 'sales estimate': A04-07
      member 'quarterly data': A04-08
      member 'unverified accrual': A04-09
  A05.c1 [A05-01, A05-02, A05-03, A05-04, A05-05, A05-06, A05-07, A05-08] Independently remove a claimed account at Schwab, invalidate an identified Traded value, request a date before trustworthy membership history, fail the existing source schema, deny capability access, stale a source, omit overlap evidence and break the calendar
      member 'remove a claimed account at Schwab': A05-01
      member 'invalidate an identified Traded value': A05-02
      member 'request a date before trustworthy membership history': A05-03
      member 'fail the existing source schema': A05-04
      member 'deny capability access': A05-05
      member 'stale a source': A05-06
      member 'omit overlap evidence': A05-07
      member 'break the calendar': A05-08
  A05.c2 [A05-09] Reasons remain distinct through the rendered consumer
  A05.c3 [A05-01] Custodian absence preserves current live count but withholds verified complete value
  A05.c4 [A05-02, A05-03, A05-04, A05-05, A05-06, A05-07, A05-08, A05-10] uncertain census/date shows null rather than zero
  A05.c5 [A05-11] The page distinguishes source-dated business count from valuation-dated expected/covered counts
  A05.c6 [A05-12] Correcting the actual missing input restores only the eligibility justified by that evidence/date
  A06.c1 [A06-01, A06-06] Fixed synthetic baseline and known Tax cents yield exactly one addition in Tax, SMA, ALT Strategies, 49financial and Global
      member 'Tax': A06-01
      member 'SMA': A06-01
      member 'ALT Strategies': A06-01
      member '49financial': A06-01
      member 'Global': A06-01
  A06.c2 [A06-02] Client and other firms stay unchanged
  A06.c3 [A06-03, A06-04] A deliberate overlapping full ID or basis disagreement blocks the total
      member 'overlapping full ID': A06-03
      member 'basis disagreement': A06-04
  A06.c4 [A06-05] Replaying and reconstructing Global retains `tax`/`source_basis` without a second addition
  A07.c1 [A07-01, A07-02, A07-03, A07-04] Trace automatic Traded events, original observed dates, identity joins and publication through protected evidence
      member 'automatic Traded events': A07-01
      member 'original observed dates': A07-02
      member 'identity joins': A07-03
      member 'publication': A07-04
  A07.c2 [A07-05] Ordinary JSON/page/logs contain no names, full IDs, row values or tokens
      member 'names': A07-05
      member 'full IDs': A07-05
      member 'row values': A07-05
      member 'tokens': A07-05
  A07.c3 [A07-06, A07-07, A07-08, A07-09, A07-10, A07-12, A07-11] Wrong identity, route/method/bearer/workbook and denied/revoked access controls fail
      member 'Wrong identity': A07-06
      member 'route': A07-07
      member 'method': A07-08
      member 'bearer': A07-09
      member 'workbook': A07-10
      member 'denied': A07-11
      member 'revoked': A07-12
  A07.c4 [A07-13] exact named identity and route succeed in the fixture
  A07.c5 [A07-14] Verify all seven permitted business fields and excluded fields
  A07.c6 [A07-15] Distinguish pre-Graph tool denial from SharePoint access failure
  A07.c7 [A07-16] Production activation separately proves exact opalbloomberg identity binding and the actual controlled capability read under its release conditions
  A07.c8 [A07-17] Prove the capability guard precedes generic `/ms/*` dispatch
  A07.c9 [A07-18, A07-19, A07-20, A07-21, A07-22] With otherwise identical valid inputs and the same email, wrong tid, wrong oid, missing/unvalidated claims and revoked principal fail before token fetch/Graph
      member 'wrong tid': A07-18
      member 'wrong oid': A07-19
      member 'missing': A07-20
      member 'unvalidated claims': A07-21
      member 'revoked principal': A07-22
  A07.c10 [A07-23] only the configured validated pair succeeds
  A07.c11 [A07-24, A07-25, A07-26] Generic MCP/ms-ingest/OTP credentials cannot open this capability
      member 'MCP': A07-24
      member 'ms-ingest': A07-25
      member 'OTP': A07-26
  A08.c1 [A08-01] Duplicate invocation cannot duplicate an observation or total
  A08.c2 [A08-02, A08-03] Corrupt/delete a local served artifact with unchanged source hash: the same publisher repairs it
      member 'Corrupt': A08-02
      member 'delete': A08-03
  A08.c3 [A08-04, A08-05] Inject a mid-run failure and pending same-day correction
  A08.c4 [A08-04, A08-05, A08-06] recovery preserves immutable history, dates and one writer
  A08.c5 [A08-07] Disable/restore the extension and verify the affected display plus unchanged non-Tax results
NON-LOCAL ARMS: A04-10 (AUTHORIZED, not the local harness: authorized dated-source reads), A07-16 (PRODUCTION_ACTIVATION, TX-r-3 (not the local harness))
READINGS (18):
  R1 [A01-01, A01-06, A02-04] Duplicate rows of one full key with the same Yes: the PRD fixes 'count once, retain conflict' and S04's DUPLICATE_ACCOUNT, not which business_status the duplicate rows carry, so that value is not asserted; the key is valid, so the dated expected count stays known (3) with K2 unresolved.
  R2 [A01-07, A01-08, A02-02, A02-03] An invalid identity or an unknown Traded on a Yes/identified claim leaves the identity/membership census unresolved, so expected_accounts is null as well as business_active_accounts; covered/unresolved enumerate the known claims.
  R3 [A05-02] An invalid Traded observed after a proven Yes never closes the interval, so a valuation date the history already proves (2026-09-14, proven by SNAP-S0) keeps its complete value while the current count is null.
  R4 [A02-09] PRD s.3.4's candidate label UNCONFIRMED has no contract enumeration member (row MDPF_TAXSMA-W5-S1); the candidate observable is stated without a status label.
  R5 [A07-11, A07-15] The contract fixes no error code for a SharePoint denial after the token fetch; the arms fix what makes it distinct from a guard denial: one token fetch, one Graph request and a distinct audit result.
  R6 [A07-07, A07-08, A07-10] The contract fixes no error code for a wrong route, wrong method or a caller selector; the arms fix the refusal, zero token fetches, zero Graph requests and no rows.
  R7 [A03-18] A Gold run at 13:30 UTC on knowledge date X values the latest exchange session strictly before X (PRD s.3.8 'expected completed session'); weekends and holidays advance knowledge, never the valuation date.
  R8 [manifest-wide] Master identities are referenced by contract path (CONTRACT:identity.*), never as digits, so no real identifier enters the manifest.
  R9 [A05-05] 'Deny capability access' is exercised as the Gateway reporting AUTH_REQUIRED for a revoked delegated principal; the pipeline carries AUTH_REQUIRED (reason_codes has no UNAUTHORIZED_CAPABILITY).
  R10 [A02-08] After CONFIRM_TRANSFER the arm asserts only that TRANSFER_UNRESOLVED clears and the current count is known; K9's dated coverage for dates before its own observation is not asserted.
  R11 [A03-18] Weekend knowledge runs value the prior Friday session and produce no valuation date for Saturday or Sunday.
  R12 [A04-10, A07-16] A04-10 (authorized dated-source cases) and A07-16 (production activation) are not local-harness arms; their observables are rules and aggregate counts, with no value or identifier in the repository.
  R13 [A01-13, A03-03] A valuation date earlier than any trustworthy history leaves expected_accounts null (unknown), never zero.
  R14 [A01-01] The fixture carries the explicit Total marker in the Index column; the contract fixes that the marker is unique and explicit, not which column carries it.
  R15 [A02-05] A FLOAT-kind Excel scalar equal to an integral eight-digit value is left unasserted (the contract both admits finite integral Excel numbers and forbids coercing a float); the INTEGER kind is asserted as accepted.
  R16 [A03-07] Same-UTC-day transitions: the day's latest accepted state governs that valuation date; every event is retained.
  R17 [A03-14] The legacy CONFIRM_EFFECTIVE_MEMBERSHIP kind appears only in an arm's input, never in an expected observable, because it is not a current contract disposition kind.
  R18 [A04-09] The accrual placeholder is carried as a limitation; an unverified accrual is never added to the value.
JUDGMENT: recorded for 3.0.0_SA_CVO at L9 -- no verdict given
```
