# FB-p-2 step 5: the S3 diff and the BOUNDS 2 grade

2.0.0_SA_COO~B1, 2026-10-19 ~14:58Z. Claim: measured by this seat, read-only, from the versioned object (not from FB1's report).
Closes the CTO's ask in his msg 8303 ("have FB1 diff the prior S3 version against 9495cd56 and confirm only its change moved"); FB1 had not read the ask (5 messages OFFER-EXHAUSTED at 14:55Z), so the issuer read it.

## The diff

Object `s3://opal-data-inf/code/gold/orion-gold-dispatch.sh` (bucket versioning on). Denominator: 6 or more versions listed, two fetched by VersionId.

| | VersionId | LastModified | bytes | sha256 (8) |
|---|---|---|---|---|
| prior | JjTLNaZeRRAQn342RRa7qEHSR0AUf1FV | 2026-10-17T13:29:03Z | 113445 | e9aef66b |
| live | hK5vY2H31oT3NHmoiArlZ00ra8gkuDaO | 2026-10-19T14:22:09Z | 113054 | 9495cd56 |

`diff prior live` = ONE hunk, `1903,1912c1903,1905`: 13 changed lines in all. Ten lines (the `_sent_json` build, the `aws s3 cp -` write of `gold/meta/pipeline-complete.json` and its OK/WARN echoes) are replaced by two comment lines and one echo. 113445 - 113054 = 391 bytes, equal to FB1's recorded 778 -> 387. Nothing else in the object moved, including the failure branch.

## The BOUNDS 2 grade (deploy only through `safe-deploy.sh`)

FB1 used `s3api put-object`: `safe-deploy.sh` handles `.py` only and no-ops on a `.sh` (FB1 msg 8297, flag 1).
Grade: **DEVIATION, ACCEPTED.** The bound's purpose (a deploy that is verified and reversible) was met: the ledger entry was open before the write, the prior VersionId is the recorded rollback, the sha read back equal, and the diff above shows one named hunk. The bound could not be met as written for this file type. No amendment to the order's text; this record is the grade. Not a precedent for a `.py`.

## Left open (not this record's to close)

- FB1 files surprise rows 1 and 3 under the order (asked at 14:27Z and 14:44Z, unread).
- The write path to this object is closed to FB-p-2 (CTO msg 8317) and XA-20261019T143617Z-d9a9 is ruled (a): IB2 on dell2 is the one uploader.
- Step 6 (the marker's version history after a chain day past 14:22Z, i.e. 2026-10-20) is a read this seat owns.
