# Round-81 PREP, R1's store half (row AMGT_RESAPP-D1-S3): grounding notes (2.0.0_SA_COO~R1 fork, 2026-10-09 ~04:2xZ)

Not cut, not issued: the decomposition waits on the CTO's round-80 analysis. Read only: no SEC fetch, no model call, no store
write. Base: box/dell1 after @34c8ad8144 (dd-1's cutter merged @6e44bfec4a).

## 1. The invocations (one named company)

1. **Fetch + silver write:** `python -m lib.research.filings.fetch --security-key ASML_NA_Equity --form 20-F --cik 937966 --write-pool`
   (`fetch.py:535-577`; `--universe newest` instead of `--cik/--form` reads `filing_identity`). `build_source_object` (EDGAR-by-CIK,
   SEC GET, no Terminal) cuts with the merged `document.cut`; `persist(..., write_pool=True)` (`:486-532`) appends ONE silver part via
   `harvest.filings.write_filing_source_silver` -> `store.silver_append` (`store.py:431-480`, put-if-absent `IfNoneMatch="*"`).
   CIK 937966 and form 20-F are MEASURED from the stored row's `filing_identity` (`{'cik': 937966, 'form_expected': '20-F', 'source': 'edgar'}`).
2. **Analyze + drafting:** `python -m lib.research.filings.analyze --security-key ASML_NA_Equity --source-json <the fresh source.json> --write-pool`
   (`analyze.py:1658-1781`). Pass `--source-json` (or `--cache-dir` naming the fresh copy): `resolve_source` (`:1565-1603`) prefers a
   LOCAL cache at `.scratch/filings_cache/ASML_NA_Equity.source.json` (`DEFAULT_CACHE_DIR`, `:1606`) over a live fetch, so a stale
   cached parser-1.0.0 object would be re-analyzed. `write_outputs` (`:1609-1655`) writes the analysis and the drafting document only.
3. **Drafting splices:** the served `drafting/v1/ASML_NA_Equity.json` was last written 2026-10-05T23:43:38Z, after the 09-30 analysis,
   so a `drafting_build.py` splice (`--splice-driver` / `--hold-unspanned`, `:815-876`) has run on it. analyze's write REPLACES that
   document; whether the splice must be re-run after it is OPEN (read `drafting_build.py` `:540-810` before the cut).
4. **Credentials:** `analyze.py:34-37,321-334` -- the key reaches the process ONLY as `ANTHROPIC_API_KEY`, exported in the same call from
   `comp-secrets get anthropic-api-key --reveal`. On dell1 (`cloudops-dell1-agent-user`) the secret's metadata reads (sha8 19cd49c3,
   len 108), so GetSecretValue works. Model `claude-opus-5` (`:60`), `messages.stream(output_config={"effort": ...})`.

## 2. THE BLOCKER ON DELL1 (measured)

`import lib.research.filings.fetch` and `...analyze` both FAIL here: Python 3.14 `ModuleNotFoundError: No module named 'fitz'`;
Python 3.12 `ImportError: DLL load failed while importing _extra`. `fetch.py:56` imports `document`, which imports `fitz` at module top
(`document.py:56`). The EDGAR .htm path never calls `fitz` (only `pdf_to_text` and friends, `:165-249`), but the import fails first.
Also: the default Python's `anthropic` SDK is 0.45.0 (3.12 has 0.84.0); whether 0.45.0 accepts `output_config` is UNREAD.
So the act cannot run on dell1 as the tree stands: either PyMuPDF is made importable on dell1 (pip egress is now open; the 3.12 DLL
failure suggests a missing runtime), or the run goes to a box where it imports (site Z ran every prior analysis).

## 3. Keys written -- all three SERVED by opal-amgt-scoped-api

| key | written by | served by | prior state (read 04:1xZ) | rollback |
|---|---|---|---|---|
| `s3://opal-data-harvest/sec/harvest/silver/filing_source/date=<run date>/part-<stamp>.parquet` (builder: `store.address_of` -> `opal_naming.address`) | NEW part, put-if-absent | `scoped_amgt._read_filing_source_object` (`:3552`), passage coverage | ONE part today, `date=2026-09-22/part-20260922T033157Z.parquet` (808,344 B, 13 sec rows); ASML's row parser 1.0.0, items `['Item 3.D. Risk Factors']` | delete the ONE new part (versioned bucket: a delete marker), so `silver_latest` falls back to the 09-22 row. **An S3 delete is on CLAUDE.md's human-confirmation list.** |
| `filings/v1/ASML_NA_Equity/000162828026011378.analysis.json` | overwrite (versioned) | segment rows, passage map (`FILINGS_ANALYSIS_PREFIX`, `:3765`) | latest VersionId `WIU.oSeIh8NKMhy2DfqsJmRwGOusYTxs` (2026-09-30T05:27:33Z, 93,121 B) | copy that VersionId back over the key |
| `drafting/v1/ASML_NA_Equity.json` | overwrite (versioned) | `/thesis` drafted sections, driver chart (`DRAFTING_PREFIX`, `:2654`) | latest VersionId `FWeloN5.zr6pvN1NWUXScK5RakjwF1qV` (2026-10-05T23:43:38Z, 13,503 B) | copy that VersionId back over the key |

Risk class: **WORLD** (an SEC GET, a model call, three served writes). It needs a never-widen pair (CTO~DELL1 + COO) and a NEVER-2 entry.

## 4. Writer census (N per key, every rule read)

- silver `filing_source` (sec): `fetch.persist` (from `fetch.main`, `batch.run_group` `:377-435`, and `battery.py`'s EDGAR leg); appends
  only; `silver_latest` (`store.py:373`) picks the newest `fetched_at` per (security_key, accession). N = 3 callers of one writer.
- `filings/v1/*.analysis.json`: `analyze.write_outputs` (from `analyze.main`, `batch.run_group`) and `analyze.reverify_stored_thesis_driver`
  (`--reverify-stored`). N = 2 writers.
- `drafting/v1/*.json`: `analyze.write_outputs` and `drafting_build` (`--rebuild-pool` `:552`, `--splice-driver` `:681`,
  `--hold-unspanned` `:809`). N = 2 modules, 4 entry points. No scheduled task runs any of them (FilingsAnalyzer disabled, census row 29).

## 5. Site Z

Census @6a308cd424 row 28 names `filings/battery.py:507-519` (its Terminal leg) as a site-Z hand-run; `fetch.py`/`analyze.py` RUNS are not
listed, and this path makes no Bloomberg call. CTO~DELL1 msgs 1267/1394 rule CHANGES to producer paths (a code merge is a site-Z deploy);
they say nothing of RUNNING the EDGAR path from dell1. A dell1 run writes the same shared keys a site-Z run would, so the pair names the
box. Open for 1.0.0_SA_CTO~DELL1: whether a dell1 RUN of these modules needs 1.0.0_SA_CTO~Z's half (the fork reads: no, it is not a
change to a producer path; but it moves the same served keys a site-Z hand-run moves).

## 6. Checks -- `round81_prep/checks/r81_store.py`, dry-run at the base

- AC1 base: FAIL as expected -- S1, S2, S3 FAIL (latest row parser 1.0.0, items `['Item 3.D. Risk Factors']`); `R81 STORE AC1 SERVED: NO`, exit 1.
- AC2 base (`--where deployed`, live `OUOsYXa`): FAIL as expected -- T1 PASS (200); T2 FAIL (refusal sentence x2); T3 FAIL (0 of 3 served
  locations cite Item 4.B); `R81 STORE AC2 SERVED: NO`, exit 1.
