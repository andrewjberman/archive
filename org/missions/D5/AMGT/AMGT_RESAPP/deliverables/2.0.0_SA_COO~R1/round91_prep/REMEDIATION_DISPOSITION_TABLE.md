# AMGT_RESAPP -- the open remediation rows, one disposition each (round 91, `AMGT-pp-5`, issuer act of `2.0.0_SA_COO~R1`)

**Input:** CTO~DELL1 round-90 analysis `ledger/ROUND_ANALYSIS.round90.md` section 2 (@b462a02d8a): per row CLOSED (with the pointer),
CARRIED (reason, owner, the round that cuts it) or RE-OWNED (site Z seats -> this fabric: product rows to `2.0.0_SA_COO~R1`, ruling
rows to `1.0.0_SA_CTO~DELL1`). One file; the CVO writes each closure in its round-91 REMEDIATION; the CTO rules the rows named to it
at the round-91 analysis.

**Denominator, measured 2026-10-11 ~06:5xZ** (`comp-surprise --project AMGT_RESAPP --json`, latest remediation entry per id,
`closed` false): 508 distinct remediation ids, **30 open** (the CTO's 29 plus `D1-S20`, graduated at ADJUDICATION_v110). Placed below:
**CLOSED 3 | CARRIED 11 | RE-OWNED 16 | 30 of 30.** A row is CLOSED only where a reading made today, or a record cited, meets its own
close condition; "closed in the CTO's analysis" is not a pointer. Two rows differ from the analysis's expectation (D1-S14, D1-S16) and
say why in their own line.

## CLOSED (3)

| row | its close condition | pointer |
|---|---|---|
| `D1-C-S29` | no served section reads FAILED while showing a sentence | the withhold is live: `r89_deployed_close.sh` `R87 WITHHELD AC1: YES` (W1 offending [], W2 5 of 5 names answered, NU among them) on CodeSha256 `l8egBo/rf..` read by this seat ~05:0xZ; CVO C-S41 (ADJUDICATION_v108) |
| `D1-S15` | the served subject cap matches the header's vintage or is absent | served `621,657.438 @ 2026-10-10T13:01:55Z`, equal to the model block (stored value dated 2026-09-19), nn-7 applied 2026-10-11T04:56:11Z; CVO C-S45 (ADJUDICATION_v109) |
| `D1-S18` | an off-list selector through the edge reads the refusal, or the ruling is recorded | ACCEPTED_BY_RULING, CTO msg 3185 (ADJUDICATION_v108: its v32 entry CLOSED_UNREMEDIATED); condition 4 EXERCISED on a populated list, CVO C-S44 (ADJUDICATION_v109) |

## CARRIED (11)

| row | reason it is not closed | owner | the round that cuts it |
|---|---|---|---|
| `D1-S14` | **not closed by oo-5, as the analysis expected:** oo-5 is the pure half and nothing it serves has landed. Live today: 2 of 12 ASML members (AMD, NFLX) serve a currency; the others carry the plain reason. The US half needs the DEMQUE answer (pp-4) and a redeploy (pp-6); the non-US half is pp-1 (23 rows, ceiling 52 of 1,816) | `2.0.0_SA_COO~R1` | 91 (pp-1), staged (pp-4, pp-6) |
| `D1-S16` | **not closed by nn-7 as worded:** the row's close names Tencent and SK hynix serving exchange tickers; `BMMV2K` is still UNRESOLVED on the live ASML peers. The US alphabetic half is met (7 of 7, CVO C-S45). The two named listings are not held companies (pool: 55 non-US records) | `2.0.0_SA_COO~R1` | 91 (pp-1 reaches only held names); the rest waits on an identifier form (the CTO's call, analysis round 89 section 2) |
| `D1-S20` | graduated INERT at ADJUDICATION_v110 | `2.0.0_SA_COO~R1` | 91 (pp-1; `HEI.A` partition question answered in its record face) |
| `D1-S6` | tooling: reconcile-deployed writes no sha for a no-record function | `1.0.0_SA_CTO~DELL1` | the CTO's, unchanged |
| `D1-W324-S3` | the key rotation is Andrew's act (analysis section 4, unblock case 86a2); `--reveal` export hardening is tooling | Andrew; relayed by `1.0.0_SA_CTO~DELL1` | on Andrew's word |
| `D1-W332-S2` | the splice's dry run moves only the provenance key; needs a read of ASML's served `drafting_provenance` before a ruling | `2.0.0_SA_COO~R1` | an issuer read in round 91 (not a cell) |
| `D1-W338-S1` | a prompt or parse change proved on fresh model draws: model calls, and the key is Andrew's to rotate | `2.0.0_SA_COO~R1` | not before the key and model-use words |
| `D1-W339-S2` | LOCAL candidate: exclude bare years from the figure rule in the sentence checker | `2.0.0_SA_COO~R1` | 92, if the CTO's list names it |
| `D1-W345-S2` | LOCAL candidate: the drafting schema's `generated` const true, a consumer-wide change | `2.0.0_SA_COO~R1` | 92, if the CTO's list names it |
| `S2` | ruling: a non-worker seat's declared order paths (route, or go through a worker) | `0.0.0_AB_MSTR~DELL1` (the validator's owner) | the CTO's ruling |
| `S3` | LOCAL candidate: a set but non-directory `OPAL_RESEARCH_LIBRARY_ROOT` refuses with its path | `2.0.0_SA_COO~R1` | 92, if the CTO's list names it |

## RE-OWNED (16): site Z owners to this fabric

| row | from | to | state and the next act |
|---|---|---|---|
| `Z-C-S2` (BLOCKING, ARMED) | `1.0.0_SA_CTO~Z` | `1.0.0_SA_CTO~DELL1` (ruling) | `.tools/receiving-check.py` is present at HEAD; whether it still grades one file at a time is not re-measured at this cut. Its disarm needs the CTO's ruling: set-level grain, or state it is per-file |
| `Z-S2` (ARMED) | `1.0.0_SA_CTO~Z` | `1.0.0_SA_CTO~DELL1` | the same defect as `Z-C-S2` under another id; one ruling closes both |
| `Z-C-S3` (ARMED) and `Z-W2-S3` (ARMED) | `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~ZZZ` | `1.0.0_SA_CTO~DELL1` (routes to the rail owner) | comp-find's `all` corpus is "minus the declared ephemeral floor"; whether `.terraform` is on that floor is not re-measured at this cut. One instrument defect under two ids |
| `Z-S362` | `1.0.0_SA_CTO~Z` | `1.0.0_SA_CTO~DELL1` | repo-wide, outside this project's paths: one renormalising commit per owning lane |
| `Z-W281-S1` | `1.0.0_SA_CTO~Z` | `1.0.0_SA_CTO~DELL1` | a vendor identifier map is a vendor use: waits on Andrew's word through the CTO |
| `Z-W45-S1` | `2.0.0_SA_COO~Z` | `1.0.0_SA_CTO~DELL1` | the 4 pilot objects' `absence_class` backfill was held under Andrew's no-fleet-rerun word |
| `Z-S369` (ARMED) | `2.0.0_SA_COO~Z` | `2.0.0_SA_COO~R1` | waits on DEMQUE request `AMGT_RESAPP-493c-ICT-IDENTITY` (filed 2026-10-09; no answer read by this seat) |
| `Z-S220` | `2.0.0_SA_COO~Z` | `2.0.0_SA_COO~R1` | SERP freshness reads one partition and the writer writes another: a key design, a harvest-side change (AMGT_HARVST) |
| `Z-W212-S2` | `2.0.0_SA_COO~Z` | `2.0.0_SA_COO~R1` | the overlay feed's `url` needs a HARVST gold rebuild (gold `article_security_mention` has no url column) |
| `Z-W266-S3` | `2.0.0_SA_COO~Z` | `2.0.0_SA_COO~R1` | pp-2 serves the chart-points part (4 of 5 held points are LOCATOR); one passage per press, axis fit and driver choice are page cells |
| `Z-S372`, `Z-S373`, `Z-W303-S1`, `Z-W173-S3`, `Z-W286-S2` | `2.0.0_SA_COO~D`, `2.0.0_SA_COO~Z` | `2.0.0_SA_COO~R1` | page cells in a project that is CLOSED (DSGN_AMGTV1); they need a portal page round, and `AMGT-nn-6` (Andrew's PROD promote) comes first. `Z-W303-S1` and `Z-W286-S2` are one defect (the page states its inputs twice) |

## Rows owed a decision by the CTO at the round-91 analysis

`Z-C-S2`/`Z-S2` (receiving-check grain), `Z-C-S3`/`Z-W2-S3` (comp-find floor), `Z-S362`, `Z-W281-S1`, `Z-W45-S1`, `S2`, `D1-S6`,
`D1-W324-S3`: 10 ids in 8 decisions. Three of them are Andrew's words relayed by the CTO (`Z-W281-S1`, `Z-W45-S1`, `D1-W324-S3`).

checked 30 of 30 open rows (508 distinct ids; 478 already closed)
