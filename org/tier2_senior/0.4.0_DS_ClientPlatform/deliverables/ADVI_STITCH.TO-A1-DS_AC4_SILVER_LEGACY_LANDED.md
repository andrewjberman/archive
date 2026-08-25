# ADVI_STITCH.TO-A1-DS — AC4 / `STI-a-2` · `STI-b-2` · `STI-inv-1` — silver_legacy LANDED

**Criterion:** `STIA1DS-AC4` · **Grounding:** EXERCISED · **Seat:** `0.4.0_DS_ClientPlatform~Q`
**Manifest vintage (PINNED):** `2026-08-25T22:59:10Z`

## 1. VERDICT — PASS

```
ENUMERATED 7,921 | LANDED 7,921 | DRIFTED 0 (1 re-pinned) | FAILED 0
FORWARD  7,921 checked, 0 mismatches
REVERSE  7,921 destination keys, 0 orphans, 0 missing
INDEPENDENT md5 arm  7,914 matched / 0 mismatched — 99.9% coverage
```

The independent arm is source-ETag == destination-ETag (**MD5 vs MD5, S3-computed on both sides,
none of my code in the path**), valid wherever the source is single-part. Coverage is 99.9% here
versus 72.9% on the raw plane, because silver sources are almost all single-part. The 7 uncovered
are multipart sources and are **uncoverable by this arm by construction** — stated, not averaged in.

## 2. ⛔ THE `DRIFTED` CLASS FIRED ON A REAL EVENT, ~20 MINUTES AFTER BEING BUILT

`silver/prices/canonical_prices.parquet` was rewritten **at 23:03:09Z — four minutes after the
manifest was pinned at 22:59:10Z**, mid-copy.

| | ETag | size |
|---|---|---|
| pinned (12:47:52Z version) | `cbc5829e7cec29258075366ac01d8494` | 104,661,448 |
| current (23:03:09Z version) | `6e7add4d65607724496af9945d937220` | 104,697,504 |

**Without the `IfMatch` precondition this would have copied silently.** The row would have carried an
honest sha256 — of the *new* bytes — beside a manifest ETag from the *old* ones. Every integrity
check it will ever face would pass, and its provenance would be false. That is the exact failure the
class was created to prevent, and it occurred in production on the first plane it guarded.

**Handled as a RE-PIN, never a retry:** re-pinned to the 23:03:09Z version, landed, and verified by
the independent MD5 arm (source ETag == destination ETag). The manifest row records **both vintages**
and is flagged `repinned: true` — so the row states that it is later than the manifest rather than
hiding inside it.

## 3. PATH RULINGS (`2.0.0_SA_COO` 71633)

| rule | count | destination |
|---|---|---|
| date from filename | 7,368 | `{table}/date={D}/{filename}` |
| mirror existing `date=` | 518 | `{table}/date={D}/{filename}` |
| **D6** depth-1 single-file set | 28 | `_single_file/{filename}` |
| **D7** undated `.parquet` aggregates | 4 | `{table}/_undated/{filename}` |
| **D9** descriptors mirrored in place | 3 | `{table}/{filename}` |

⛔ **DECLARED DEVIATION — D7 as literally ruled listed 5, I landed 4.** D7 included
`transactions_enriched/_DIAGNOSTIC_ARTIFACT.txt`, but D9 ruled that prefix lands "whole and intact"
and warned specifically against splitting it "across D7". Burying its warning in an `_undated/`
subdirectory is D9's stated failure in a milder form — a reader listing the prefix would have to
*open* a subdirectory to meet it. **Non-`.parquet` descriptors therefore mirror at their source
position; only undated `.parquet` aggregates go to `_undated/`.** Reported to the issuer at the time,
not discovered in this document.

**A guard that earned its place:** the copier refuses to run if two source keys map to one
destination key. **0 collisions.** A collision would not error — the second PUT would silently
overwrite the first, the census would still close at 7,921 in *both* directions, and the loss would
be invisible in every number reported.

## 4. `STI-inv-1` — THE LEGACY TIERS ARE UNMISTAKABLY DISTINCT

**(a) 0 landed keys under a live tier.** Denominator: **8,852** landed keys across both planes;
**0** fall under `49financial/bronze/` or `49financial/silver/`.

⚠ `49financial/bronze/` is **not empty** — it holds 5 `insurance_*` keys. Those are
`ADVI_INSURE`'s (`0.4.0_DS_ClientPlatform~J`), the coordinated neighbour: different leaves, same
parent. **The test is "none of MY keys land in a live tier", not "the live tiers are empty"** —
reading it the second way would have produced a FAIL on a correct state.

**(b) 0 live consumers.** ⛔ **The naive grep returned 978 and 15,871 hits, and the predicate was
wrong** — 950 and 15,849 of those are **my own manifests, committed minutes earlier**, one hit per
row across 8,854 rows. Every remaining reference, enumerated in full rather than filtered until the
number reached zero:

| reference | what it is |
|---|---|
| `infra/aws/terraform/opal-assets/advi_stitch_landing.tf` (4) | the landing-role grant — **the WRITER**, not a consumer |
| `org/projects/ADVI_STITCH.json` (6) | project registry prose |
| `.../0.7.0_AE_CloudOps/deliverables/...PROOF_OF_SPEC.json` (5) | a peer's evidence artifact |

**No executable consumer references either legacy prefix.**

## 5. NOTED, NOT CHASED

`silver/transactions_enriched/` landed whole (519 keys) with its own `_DIAGNOSTIC_ARTIFACT.txt`
mirrored at the prefix root, so the disownment travels with the data. **Its README and the estate
thread both record 494 partitions; I measure 518 (+24.)** Either the record is stale or writes
continued past a standing "no further writes" ruling — opposite remedies. Filed to `3.0.0_SA_CVO`
via the issuer; not this cell's to resolve.
