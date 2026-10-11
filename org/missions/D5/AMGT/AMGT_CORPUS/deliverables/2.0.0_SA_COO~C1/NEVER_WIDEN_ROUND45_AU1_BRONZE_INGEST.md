# AMGT_CORPUS round 45 -- never-widen pair for `CRPS-au-1`: the site-Z bronze ingest of the resolved-folder files the store lacks

**Authority:** `1.0.0_SA_CTO~DELL1` round-44 analysis `ledger/ROUND_ANALYSIS.round44.md` @599a7cee43 s.2 item 1 (msg 3693). PRD FWD-1
(`prd/AMGT_CORPUS_PRD.md:190-200`). **Issuer / COO half:** `2.0.0_SA_COO~C1`. **CTO half:** owed by `1.0.0_SA_CTO~DELL1`
at `ledger/NEVER_WIDEN_ROUND45_AU1_CTO_HALF.md`. The executor is `0.7.0_AE_CloudOps~ZC` under the order
`task-orders/AMGT_CORPUS.TO-WRITE-R45-au1.bronze-ingest-and-four-count-sitez.md`, which names STOP 0 on both halves.

**What this half signs, and what it does not.** ONE act: `python -m lib.research.corpus.ingest --write`, run once at site Z, then
`--verify`, and the read-only `backlog --coverage-dry-run` and `library --census` before and after. It does not touch any dossier,
any model block, any page, any schedule or any other firm, and it makes no vendor call.

## THE BYTES (read at dell1 HEAD `1759d5fc6a`, and on `origin/box/sitez` @910098a565 after a fetch: equal)

| path | blob | role |
|---|---|---|
| `lib/research/corpus/ingest.py` | `d726b31065f3` | the writer; `ingest()` at :89-208, `_run_write` :262 |
| `lib/research/harvest/store.py` | `34b344de8ed1` | `bronze_put` :223 -- one conditional put, write-once |
| `lib/research/corpus/backlog.py` | `ec6830f630f3` | the fresh resolution (RESOLVED / AMBIGUOUS / UNRESOLVED) |
| `lib/research/corpus/library.py` | `b37fb1452556` | the census; the library root resolves at site Z only |

A site-Z tree whose bytes for any of the four differ from these is a STOP for this half.

## THE RULES READ AT SIGNING (producer's own, not predicted from shape)

- **Writers of the property "an object under `store.address_of("amgt", "bronze", "research-report", <security partition>)`": 1 in the closure of this act.**
  `ingest.py:173` `store.bronze_put(SOURCE, REQUEST, ...)`. Other `bronze_put` callers in `lib/research` write other requests
  (`research-report-extract`, `serp`, `filings`, `bloomberg`) or are test or stub callers (`substrate.py:486` takes a stub client).
- **Write rule: write-once.** `bronze_put` is one conditional put with `IfNoneMatch="*"`. A key that exists with the same sha256 is a
  no-op (`existed True`); a key that exists with a different sha256 raises `BronzeImmutableError`. The key is
  `form_b_object(sha256[:16], safe name)`, so a changed file lands under a NEW key and the prior object stays. Nothing is overwritten.
- **What it stores: RESOLVED-folder files only** (`ingest.py:124-132`). A file in an UNRESOLVED or AMBIGUOUS folder, or a loose root
  file, is printed with its reason and never stored: no key is guessed. So the count of objects can equal the count of files in
  RESOLVED folders; it can equal the drive's file count only if no folder is unresolved. The 2026-10-11 read printed 6
  unresolved-with-reason folders of 102 (`evidence/r44_at4_fence14_store_match_sitez.txt`). The order prints all three numbers.
- **Placeholders:** a OneDrive placeholder is opened `"rb"` and so hydrated on read (11 of 378 at the last census); a file that
  cannot be read is `read_failed`, counted and printed, not stored.
- **Dossier readers of this partition:** `team_sheet.py` (`BRONZE_REQUEST`), `extract.py`, `typed.py`. They read bronze at a DOSSIER
  WRITE (`dossier.write_one` via `continuation.write_one`); the served page reads the stored gold dossier. Whether any schedule calls a
  dossier write is NOT read here; the CTO half confirms it. This act writes no dossier.

## EXPECTED OUTCOME (every branch)

- **Branch A:** `files_in_resolved R`, `stored R`, `read_failed 0`; `put_performed P` new keys (the files the store lacked in resolved
  folders) and `existed R-P`; `unresolved_files K in J folders` with each reason named; `census F = R + K`; `--verify` prints
  `objects R files R match R mismatch 0`. The accounting script prints `identity OK`.
- **Branch B:** `K > 0`. Expected, since the fence14 line read 6 unresolved folders. Those files stay out of the store with their
  reasons; FWD-1 is then graded on the resolved-folder reading of the PRD's DONE WHEN, with `K` and the drive total printed beside it.
  The unresolved folders are an identity-resolution matter (`crosswalk/v1`), not an ingest defect, and ride a later round.
- **Branch C:** `read_failed > 0`, or `BronzeImmutableError`, or `--verify` mismatch > 0, or an `AccessDenied` on the put: STOP,
  copy the whole output, change nothing further. New keys already put stay (additive); the CTO decides.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the `research-report` bronze partitions of the RESOLVED securities, in the harvest bucket (`store.HARVEST_BUCKET`) | NEW keys only, one per previously unstored resolved-folder file (`put_performed P`) | none needed: additive, write-once, unread by the served page until a dossier write (its own pair). A delete of a new key needs a human word (CLAUDE.md, S3 deletes) |
| the library (OneDrive) | read only (`"rb"`); placeholders hydrate | not applicable |
| `ingest_run.json` under `deliverables/0.9.0_WK_AMGT_CORPUS~1/` | rewritten by the module on every `--write` (hard-coded path) | the executor commits it as run evidence, named in the order's `<paths>` |

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~09:27Z, for the act above, branches A to C.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
