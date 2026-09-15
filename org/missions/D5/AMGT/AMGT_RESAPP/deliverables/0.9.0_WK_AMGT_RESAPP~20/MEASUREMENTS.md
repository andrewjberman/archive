# AMGT-rj-6 -- THE FILINGS ANALYZER: every number this order produced

Worker `0.9.0_WK_AMGT_RESAPP~20`, branch `wk-amgt_resapp-11-3`, 2026-09-15.
Every model call is listed with its instrument, model and usage. Every count states its denominator.

---

## 1. THE MODEL RUN LEDGER -- every vendor call this order made

Model `claude-opus-5` throughout, via the `anthropic` python SDK 0.116.0, streaming, through
`lib.research.filings.analyze.anthropic_call` -- the ONE vendor seam in the package. Key from
`comp-secrets get anthropic-api-key --reveal`, extracted from the `value:` line (row W20-S7),
exported as `ANTHROPIC_API_KEY` in the same Bash call and never written to a file.
Cost basis: card 1's own, Opus 5 list, USD 5 / MTok in and USD 25 / MTok out.

| # | call | in | out | s | USD | note |
|---|---|---|---|---|---|---|
| 0 | parameter probe (300 max_tokens, 3-line document) | 938 | 147 | 2.2 | 0.0084 | validated `output_config.effort`, streaming and the `char_location` citation shape BEFORE any real run |
| 1 | BA pass 1 (COLD, inside the run killed at 115 s) | -- | -- | >115 | ~0.44 | rc 124; usage not returned to the process. Row W20-S1 |
| 2 | BA pass 1 (`--stage pass1`) | 56,427 | 6,397 | 65.2 | 0.4421 | cached |
| 3 | BA pass 2 | 6,068 | 6,767 | 60.4 | 0.1995 | AC2's recorded run |
| 4 | BA pass 2 (re-run after the quoted-span fix, row W20-S5) | 6,068 | 6,767 | 60.4 | 0.1995 | so the record and the served artifact agree |
| 5 | COST pass 1 | 28,396 | 5,425 | 57.0 | 0.2776 | |
| 6 | SAP pass 1 | 50,507 | 6,227 | 64.0 | 0.4082 | |
| 7 | HD pass 1 | 39,204 | 5,499 | 55.7 | 0.3335 | |
| 8 | BABA pass 1 | 59,005 | 6,848 | 72.8 | 0.4662 | |
| 9 | COST pass 2 | 5,206 | 5,859 | 53.2 | 0.1725 | AC3 |
| 10 | SAP pass 2 | 5,693 | 6,489 | 59.3 | 0.1907 | AC3 |
| 11 | HD pass 2 | 5,203 | 5,873 | 51.3 | 0.1728 | AC4 |
| 12 | BABA pass 2 | 6,414 | 7,185 | 65.0 | 0.2117 | AC4 |

**TOTAL: 13 calls, approximately USD 3.49** against the cell's bound of five pass-1 + pass-2 runs at
about USD 1.1 each (USD 5.5). FIVE FILINGS were analyzed, which is the bound's unit. The extra calls
are named, not hidden: one cold BA pass 1 lost to the 115 s timeout (row W20-S1), one BA pass 2
re-run so the recorded AC2 output describes the object actually served (row W20-S5), and one
sub-cent parameter probe. Every dollar figure is computed, not estimated: `usd = in*5e-6 + out*25e-6`.

**No pass 1 was ever billed twice for the same excerpt.** The cache is keyed on `excerpt_sha256` +
`prompt_version`; a cached pass 1 prints `cached true` on its PASS1 line and sets
`passes.pass_1.cached` on the analysis object.

---

## 2. THE FIVE FILINGS -- fetch

EDGAR, `https://data.sec.gov/submissions/CIK<cik>.json` then the primary document, with the SEC
fair-access User-Agent REUSED verbatim from card 1's measurement script.

| security_key | form | filed | accession | document chars | excerpt chars | of named items | truncated | officer section |
|---|---|---|---|---|---|---|---|---|
| BA_US_Equity | 10-K | 2026-01-30 | 000162828026004357 | 494,399 | 137,314 | 147,211 (93%) | mdna | 9,409 |
| COST_US_Equity | 10-K | 2025-10-08 | 000090983225000101 | 218,139 | 69,703 | 69,634 (100%) | -- | 3,759 |
| HD_US_Equity | 10-K | 2026-03-18 | 000162828026019436 | 363,346 | 101,436 | 106,719 (95%) | risk | 8,261 |
| SAP_GY_Equity | 20-F | 2026-02-26 | 000110465926020058 | 937,411 | 113,823 | 120,083 (95%) | mdna | 40,000 |
| BABA_US_Equity | 20-F | 2026-05-20 | 000119312526231755 | 1,308,999 | 150,078 | 481,938 (31%) | risk, mdna | 40,000 |

Coverage ranges 100% to 31% of the named items; the caps are declared, recorded per object
(`excerpt.truncated_items`, `excerpt.item_full_chars`) and required by the 115 s bound. Row W20-S8.
The officer section is PERSISTED and NOT extracted -- `officer_section.extracted: false`,
`extraction_owner: AMGT-rj-8`.

The section cut does not use card 1's "last heading match" rule, which takes a CROSS-REFERENCE on 2
of these 5 filings. Row W20-S4.

---

## 3. THE FIVE FILINGS -- analysis (INTERFACE F-1)

| security_key | passages | citations | resolved | items | cited | % | held | driver | USD |
|---|---|---|---|---|---|---|---|---|---|
| BA_US_Equity | 276 | 97 | 97 | 85 | 85 | 100.0 | 0 | BCA commercial aircraft deliveries (P0111) | 0.6416 |
| COST_US_Equity | 142 | 89 | 89 | 81 | 81 | 100.0 | 0 | Comparable sales ex-FX and gasoline (P0080) | 0.4501 |
| SAP_GY_Equity | 255 | 92 | 86 | 84 | 78 | 92.9 | 6 | Current cloud backlog growth at cc (P0091) | 0.5989 |
| HD_US_Equity | 146 | 81 | 81 | 79 | 79 | 100.0 | 0 | Comparable sales (P0101) | 0.5063 |
| BABA_US_Equity | 279 | 86 | 86 | 80 | 80 | 100.0 | 0 | Cloud Intelligence Group revenue (P0249) | 0.6779 |

409 items across five filings, 403 resolved to an exact passage (98.5%), 6 HELD. Every driver is
`resolution: cited` -- none needed the located fallback, none was held.

**The HOLD arm fired on live data**: SAP's six held items carry the tag they claimed and are absent
from `items`. Six of SAP's 92 citations quoted text the excerpt does not carry, so they resolved to
nothing -- which is the CRO's point ("a syntactically valid cite index string is not proof that the
passage can be located") measured on a real filing.

---

## 4. THE FIVE FILINGS -- drafting (INTERFACE D-1), read back from the pool

| security_key | sections | sentences | verbatim PASS | dropped | with a quoted span | evidence records | driver |
|---|---|---|---|---|---|---|---|
| BA_US_Equity | 5 | 38 | 38 | 2 | 14 | 88 | yes |
| COST_US_Equity | 5 | 35 | 35 | 3 | 11 | 71 | yes |
| SAP_GY_Equity | 5 | 36 | 36 | 0 | 13 | 70 | yes |
| HD_US_Equity | 5 | 38 | 38 | 2 | 18 | 61 | yes |
| BABA_US_Equity | 5 | 38 | 38 | 2 | 31 | 64 | yes |

185 sentences served, 185 verbatim-PASS, 9 DROPPED, 87 carrying the company's own words verbatim.
`ceo_bio` is empty and says so on every one of the five (`absent.owner: AMGT-rj-8`).

**The gate does real work on live data, and it did not at first.** The first BA draft reported
`quoted 0` across 40 of 40 sentences -- 1 of 85 analysis items carried a quotation mark, so the gate
ran 40 times and could not fail once. Row W20-S5.

---

## 5. THE POOL -- what was written, read back

`s3://opal-data-harvest`, through `lib.research.identity.crosswalk.write_pool` (put with
`Metadata {document-sha256, schema-version}`, then `head_object` compared on the digest AND the
content length; an object already carrying the same digest is not rewritten).

- `filings/v1/` -- **10 objects**: five `<accession>.source.json` and five `<accession>.analysis.json`.
- `drafting/v1/` -- **5 objects**: `BA_US_Equity.json`, `COST_US_Equity.json`, `SAP_GY_Equity.json`,
  `HD_US_Equity.json`, `BABA_US_Equity.json`.

Every upload printed `read-back=verified`. The BA drafting object's served digest is
`684197b8861424f99eec4c5a643668c2a7801cc9001ed223b54ff366053f7d81` and a LOCAL rebuild from the
persisted analysis reproduces it byte-for-byte (section 7).

---

## 6. THE BATCH AND THE SCHEDULE -- defined, disabled, never run over the universe

Dry run over U-1 (`s3://opal-data-harvest/universe/v1/2026-09-15.json`, as_of 2026-09-15):

    names 256   with_filing_identity 12   would_fetch 12   unresolved_source 244

which is the shape the issuer measured at the spawn. Nothing was fetched, no model call was made,
no pool write happened, and the task was not run.

Task, created then disabled in two commands:

    schtasks /Create /TN OpalResearch-FilingsAnalyzer /TR "<repo>\lib\research\filings\run_batch.cmd" /SC WEEKLY /D SUN /ST 06:00 /F
    schtasks /Change /TN OpalResearch-FilingsAnalyzer /DISABLE

both `SUCCESS`. Measured state (`/FO LIST /V`): `Scheduled Task State: Disabled`, `Schedule Type:
Weekly`, `Days: SUN`, `Task To Run: C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\
filings\run_batch.cmd`. The launcher derives the workspace root from its own location
(`%~dp0..\..\..`); no device path is baked into any file. Activation is Andrew's word.

**AC6's named invocation cannot show two of those fields** -- rows W20-S2 (MSYS rewrites `/Query` to
`C:/Program Files/Git/Query`, so the literal command emits nothing) and W20-S3 (`/FO LIST` without
`/V` carries neither `Scheduled Task State` nor `Schedule Type`). AC6 is recorded FAIL AS WRITTEN
and the order stays OPEN on it.

---

## 7. CONTROLS

**DETERMINISM.** The drafting document built TWICE from the same persisted analysis:

    run1 sha 684197b8861424f9 len 109540
    run2 sha 684197b8861424f9 len 109540  identical=True

and that digest IS the served object's `document-sha256`, so the deterministic half reproduces the
artifact exactly. The model passes are NOT deterministic by nature (no seed is offered); the pass-1
cache is what makes a re-run reproduce a given analysis rather than re-sample it, and every reuse is
disclosed.

**MUTANTS**, all four against the SERVED BA drafting document, positive control first:

| arm | expected | observed |
|---|---|---|
| positive control, unmutated | 38 pass, 0 refuse | 38 pass, 0 refuse |
| EXISTENCE: one sentence's id -> `P9999` | refuse | 37 pass, 1 refuse: `unknown evidence id 'P9999': it names no record on this document` |
| VERBATIM: one sentence quotes words the filing does not carry | refuse | 37 pass, 1 refuse: `verbatim gate: a quoted span is not in the passage it cites (P0111)` |
| SOURCE VERSION: one record's `document_sha256` -> superseded | refuse | 36 pass, 2 refuse: `source version: evidence id 'P0179' was drawn from document_sha256 'sha-of-a-SUPERSEDED-document', the served document is '5e6dd00...'` |

All three refusal paths FIRED, and the positive control passes, so the refusals are the mutation's
and not the gate's baseline.

**THE CRO'S THREE PROBES**, re-run as tests (`lib/research/drafting/tests/test_drafting.py`):

| probe | measured then | measured now |
|---|---|---|
| unknown evidence id, no quotation | 1 PASSED | REFUSE |
| valid id, the body passage quoted, absent from the title | 0 passed, 1 REFUSED | PASS |
| the same valid id, the TITLE quoted | 1 PASSED | REFUSE |

The middle row is the difference arm: the gate did not merely get stricter.

---

## 8. TESTS

    python -m unittest discover -s lib/research/filings/tests -p "test_*.py" -q   ->  Ran 20 tests ... OK
    python -m unittest lib.research.drafting.tests.test_drafting -q               ->  Ran 13 tests ... OK

33 of 33. Every filings test passes the model STUB into `analyze_source`, so no test can reach the
vendor.

---

## 9. ROWS FILED

`AMGT_RESAPP-Z-W20-S1` .. `-S8`, all `UNDER_INVESTIGATION`, all `INERT`, two `BLOCKING` (S2, S3 --
AC6's invocation) and six `OBSERVATION`. See
`org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` at
`8abfd829a7`.
