# ADVI_STITCH.TO-A1-DS — AC5 / `STI-a-3` · `STI-b-3` · `STI-inv-5` — the three BD series FROZEN

**Criterion:** `STIA1DS-AC5` · **Grounding:** EXERCISED (mutant) · **Seat:** `0.4.0_DS_ClientPlatform~Q`
**Manifest vintage (PINNED):** `2026-08-25T23:37:05Z`

## 1. VERDICT — PASS

```
ENUMERATED 7,273 | LANDED 7,273 | DRIFTED 0 | FAILED 0
FORWARD  7,273 checked, 0 mismatches
REVERSE  7,273 dest keys, 0 orphans, 0 missing
INDEPENDENT md5 arm  7,273 matched / 0 mismatched — 100.0% coverage
```

Destination `s3://opal-data-49financial/gold/advi/reference/bd_legacy_{series}/date={D}/data.parquet`.
Grammar is **Rule 17b** ("GOLD IS PARQUET, `{table}/date={D}/`") and matches the existing sibling in
that exact prefix (`ref_txn_classification/date={D}/data.parquet`) — derived from law and local
convention, not chosen. **Neighbour untouched: `ref_txn_classification` still 10 keys.**
**`STI-a-3` count of what stays put: 73,563 − 7,273 = 66,290.**

## 2. ⛔ TWO VINTAGE KINDS, LABELLED PER SERIES — NOT ONE REMEDY FOR THREE VALUES

| series | keys | label |
|---|---|---|
| `bd_legacy_holdings` | 2,425 | **CLOSED-PERIOD-IMMUTABLE** — write-once at source (1 version, 1 ETag) |
| `bd_legacy_performance` | 2,424 | **SNAPSHOT-AT-VINTAGE** |
| `bd_legacy_nna` | 2,424 | **SNAPSHOT-AT-VINTAGE** |

`performance` and `nna` are **restated by BD** — measured, stratified 28 of 2,424 keys: mean distinct
ETags 2.5 (2020) rising to 12.0 (2025), **no year content-stable**; counts are a FLOOR because the
retained version window caps at 29. Labelling them "the closed period" would tell a future reader
this equals BD's current answer. It does not, and it will diverge. The label is written **per row in
the manifest**, not only in this document.

## 3. ⛔ MY IDEMPOTENCE GATE WAS BROKEN, AND IT FAILED AS THE THING I HAD WARNED AGAINST

The first implementation ran the gate **before** the source was read, so `source_sha256` was always
`None`, the equality branch could never fire, and every existing key took the refusal path:
**7,273 of 7,273 `REFUSED_CONTENT_DIFFERS` on a re-run of byte-identical data.**

The refusal was in the **safe** direction — it never overwrote anything — but it is **not `inv-5`**.
"A re-run is a NO-OP on existing keys and REFUSES on a content difference" requires the gate to
**discriminate**, and one that only ever refuses does not. **A refusal that fires on healthy input is
the alarm-indistinguishable-from-healthy-operation failure this TO's AC5 was amended to avoid — I
argued that case to the issuer hours earlier and then built it.**

**THE ORDER IS THE MECHANISM.** A content-keyed no-op must cost a source **READ**; it must never cost
a **WRITE**. Fixed by hashing the source first, then gating. Re-run after the fix:
**7,273 SKIPPED_NOOP, 0 refusals, 0 writes.**

⚠ **Second error, recorded because it cost evidence:** that broken re-run **overwrote the run-1
landed manifest**, replacing 7,273 rows carrying `source_sha256` with refusal rows carrying none.
Recoverable — every destination object holds an S3-computed `ChecksumSHA256` — and rebuilt by the
corrected run. **A "no-op test" that clobbers the artifact it is testing is not a no-op.**

## 4. `STI-inv-5` — THE MUTANT, AND BOTH ARMS ARE REACHABLE FROM DIFFERENT TRUTHS

Subject `bd_legacy_holdings/date=2020-01-01/data.parquet`, one hex digit changed in the **expected**
hash:

| arm | expected sha256 | result |
|---|---|---|
| CONTROL | `5eb3e7b2…a119` (true) | **SKIPPED_NOOP** |
| MUTANT | `0eb3e7b2…a119` (one digit) | **REFUSED_CONTENT_DIFFERS** |

**The gate discriminates.** Both arms run the same code against the same live object and differ only
in the field under test — a control set is sound only when both halves can fail there.
⛔ **No bytes were written on either arm: the mutation is in the EXPECTATION, never in the immutable
tier.** Planting a corrupted object to test a guard would have meant writing corruption into a
closed-period store to prove it was protected.

## 5. NEVER#3 / AC6 STILL HOLDS

`gold/timeseries/account_performance.parquet` remains unreachable from this cell — the moved set is
exactly `gold/canonical/{performance,nna,holdings}/` and nothing else in `opal-data-bd/gold` was read
or written. Baseline `VersionId=dqCah5NzuhEqJW8UqK0UEjBQIrytzwpz` pinned before any work.
