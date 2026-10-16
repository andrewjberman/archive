# IRPT_DASHBD round 128, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-16 ~00:0xZ; written late at the CTO's request, msg 8779)

**One direct-act order (a one-line data edit), drained and graded on the LANDED tree; no vendor call, no S3 read or write, nothing deployed, no client data.** Issued @d5d026244d (merged @38e0e24b8a), drained: `DB-i-15` (~315, merged @b421b07328). On the merged tree `DBI126-1-AC1` (the round-126 check, which now also requires the new key) PASSES, the order's own criterion `DBI128-1-AC1` is that command, and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 128 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. Cut on the CTO's round-126 analysis (msg 8730).

## What changed

The round-126 series-ended read record `SERIES_ENDED_CAUSE_R126.json` gained ONE key: `"cause_claim": "inferred"` (the account is absent from a complete positions partition; its own status was not read). `git diff` shows one added line and no other byte moved. The round-126 check was amended in the same issuance to require the key, so a consumer can reject on the field; between that issuance and the worker's merge `DBI126-1-AC1` read FAIL on trunk (named in decomposition section 14, not a regression).

## Why an order for one line

My own commit of the line was REFUSED by commit lane TREE_DELIVERABLES, which grants a worker's deliverables folder only to a worker holding a non-terminal order that names the path. I did not use the audited lane override. The record face needs a worker; the direct-act path is the cheapest lawful one.

## What the issuer read for itself

Re-ran the check on the landed tree (PASS), confirmed the diff is one added line against the pre-edit record, and ran `round-close-check`. **Not a grade.** No packet was written at the time (a direct act runs no L8); the CTO asked for one, and this is it.

## Rows

None filed by the worker. No ARMED row.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
