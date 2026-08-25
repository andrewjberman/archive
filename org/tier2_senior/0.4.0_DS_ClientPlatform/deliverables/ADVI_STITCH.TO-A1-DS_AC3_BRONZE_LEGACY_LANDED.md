# ADVI_STITCH.TO-A1-DS — AC3 / `STI-a-1` · `STI-b-1` · `STI-inv-2` — bronze_legacy LANDED

**Criterion:** `STIA1DS-AC3` · **Grounding class:** EXERCISED
**Seat:** `0.4.0_DS_ClientPlatform~Q` · **Issuer:** `2.0.0_SA_COO`
**Manifest vintage (PINNED):** `2026-08-25T22:33:48Z`

## 1. VERDICT — PASS

```
ENUMERATED : 932
LANDED     : 931
EXCLUDED   :   1   EXCLUDED-NOT-VENDOR-DATA (D5)
DRIFTED    :   0
FAILED     :   0
MECE       : 931 + 1 + 0 + 0 = 932  vs 932  -> CLOSES
```

Both directions against the pinned manifest, never a live source re-list:

| direction | check | result |
|---|---|---|
| FORWARD | every manifest row present + correct at destination | **931 checked, 0 mismatches** |
| REVERSE | every destination key traces to a listed source prefix | **931 dest keys, 0 orphans, 0 missing** |

## 2. THE METHOD, AND WHAT EACH ORACLE ACTUALLY PROVES

Streaming download + upload, in-flight sha256 both sides, **pinned by an `IfMatch` precondition**
carrying the manifest ETag — S3 refuses the read with `412` unless the object still carries exactly
the pinned bytes. Server-enforced, on `s3:GetObject` alone.

⛔ **BE PRECISE ABOUT THE CHAIN, BECAUSE IT IS NOT SELF-EVIDENT WHAT IT COVERS.** The sha256 was
computed by *my own copier*. S3 recomputes it on receipt and refuses a mismatched PUT — so the chain
proves *the bytes S3 stored are the bytes the copier hashed*. It does **not**, by itself, exclude a
copier that corrupted bytes in memory and then hashed the corrupted version: that failure is
self-consistent and would pass every layer above.

**So an INDEPENDENT oracle was run, using a different digest and no code of mine:**

| | |
|---|---|
| oracle | source ETag == destination ETag (**MD5 vs MD5**, S3-computed on both sides) |
| valid because | single-part source ETag *is* the MD5; every destination is single-part by construction |
| coverage | **679 of 931 landed (72.9%)** |
| result | **679 matched, 0 mismatched** |
| not covered | the 252 multipart sources — their ETag is a digest-of-digests, by construction |

This is corroboration by a *different instrument*, not a repetition: it never touches the sha256 path.
It cannot cover the multipart set, and that limit is stated rather than averaged away.

## 3. PATH RULINGS APPLIED (`2.0.0_SA_COO` 71609)

| id | population | destination | note |
|---|---|---|---|
| D1 | 3 undated | `transactions/_undated/` | **no date synthesised** — a fabricated partition date in an immutable tier is indistinguishable from a real one forever |
| D2 | 282 depth-1 `TXN_` | `transactions/{date}/` | family **DERIVED**, not source truth: `TXN_` appears in `transactions/` (97) and in **zero** other families |
| D3 | 62 date-range | `{family}/{START}/` | a **CONVENTION**; both endpoints survive in the preserved filename |
| D4 | 119 `_complete` markers | `{family}/_complete/{date}.json` | land — dropping them fails "census equals source census" by construction |
| D5 | 1 `_perm_probe` | — | **EXCLUDED**, declared and counted, not silently dropped |

⚠ **THE MARKERS ARE NOT A COMPLETENESS ORACLE.** Marker-date coverage of file-dates: allocations
8/125 (6.4%), assets 0/48 (0.0%), realized 47/110 (42.7%), transactions 56/160 (35.0%), unrealized
8/69 (11.6%); `backfill_v2` has **zero** markers. A landed `_complete/` tree *looks* like an
attestation of completeness and is not one — and a future reader will reach for it exactly when they
need a completeness check most.

## 4. RUN 1 FAILED TOTALLY. RECORDED, BECAUSE THE FAILURE MODE IS THE LESSON

Run 1: **0 landed, 931 AccessDenied on `s3:GetObjectVersion`.** Cause: passing `VersionId` to
`get_object` authorizes against `s3:GetObjectVersion`, which the landing role does not hold —
**a fact `0.7.0_AE_CloudOps~J` had stated in plain text in 71587, which I read and then wrote the
copier anyway.**

Three things worth keeping:
- **The failure was TOTAL, not partial.** Into a Rule 25 immutable tier that is the good direction:
  nothing to unpick, no half-landed set, no provenance to reconstruct.
- **The fix was not the grant.** 931 real AccessDenied failures are the most persuasive possible case
  for widening a least-privilege role — and it was still the wrong fix, because the defect was in the
  CALL. `IfMatch` removed the need entirely. **A widening justified by a real failure is
  indistinguishable at review from one that was actually needed.**
- **Run 1 reported `exit 0`.** It was piped through `| tail`, so the shell returned *tail's* rc.
  Caught from the `LANDED=0` line in the body, not the exit code — which is why the estate's
  discriminator for this class is a positive MARKER rather than an rc. Run 2 captured to a file and
  read the real rc.

## 5. `DRIFTED` — A STATUS CLASS, NOT A FLAG

A `412` means the source **changed since the manifest vintage** — real and expected on a live plane
(three of four still are). It is **never retried**. Retrying a 412 would either spin or **eventually
succeed against different bytes than the manifest records, landing a row whose sha256 is honest and
whose provenance is a lie.** Drift is a re-pin, not a retry. Retry-on-404 stands unchanged for the
genuinely transient class: `404` is *the read failed*, `412` is *the world moved*.

This run: **0 DRIFTED, 0 retried.**

## 6. `STI-a-4` / AC6 — THE SERVED SERIES IS UNTOUCHED

`gold/timeseries/account_performance.parquet` baseline pinned **before** any work at
`2026-08-25T21:17:31Z`: `VersionId=dqCah5NzuhEqJW8UqK0UEjBQIrytzwpz`, size 229,138,778.
Unreachable from the scope set by construction — `gold/timeseries/` is not a declared source prefix.
⚠ Its ETag ends `-28`, i.e. **MULTIPART — not a content digest.** `VersionId` is the sound oracle.

## 7. RULE 17a — THE GUARD DOES NOT REACH `bronze_legacy`. EXERCISED.

| arm | result |
|---|---|
| `.parquet` under a literal `/bronze/` segment | **DENIED** — `DenyParquetUnderBronze17a` fires |
| `.parquet` under `/bronze_legacy/` | **ALLOWED** — the guard does **not** reach |
| `.xlsx` under `/bronze_legacy/` (control) | ALLOWED — so the allow is not about the extension |

Tested via `create-multipart-upload`, which authorizes against `s3:PutObject` on the exact key
**without creating an object**; every upload aborted, 0 objects and 0 incomplete uploads left behind.

⛔ **So the no-parquet property under `bronze_legacy` rests on `STI-inv-2` ALONE — on discipline, not
on a bucket control.** The TO predicted this; it is now measured rather than assumed.
