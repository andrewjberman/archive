# REVIEW -- INF_D_02c.client_directory.py

- script: `data/inf/scripts/gold/INF_D_02c.client_directory.py`
- verdict: **issues-found**
- runs_in_incremental: True
- findings: 1

## Finding 1 -- [low/unguarded-read/both]
- **Location:** `data/inf/scripts/gold/INF_D_02c.client_directory.py:91 (_read_book)`
- **Mechanism:** get_object is wrapped in try/except that catches ONLY s3.exceptions.NoSuchKey and returns None (graceful skip -> advisor recorded in advisors_missing, loop continues). But `json.loads(obj['Body'].read().decode('utf-8'))` on line 91 is OUTSIDE the try block. The script's explicit design intent (per docstring + the NoSuchKey handling) is to tolerate an absent/bad book.json and keep going, but that tolerance is not extended to (a) a present-but-malformed/empty book.json body, or (b) a transient non-NoSuchKey read error (S3 5xx/throttle, or an AccessDenied on IAM drift). Any of those raises an uncaught exception. Because INF_D_02c runs in the no-timeout, hard-fail gold D-chain (orion-gold-dispatch runs every INF_D_* with no timeout and aborts the whole chain on any nonzero exit), one uncaught exception here aborts the entire nightly D-chain rather than degrading gracefully.
- **Failure scenario:** One of the 4 book.json objects exists but is empty (0 bytes) or truncated/invalid JSON (e.g., a partially-written prior object), OR a transient S3 500/throttle hits one of the 4 GET calls -> json.loads (or the body read) raises JSONDecodeError/ClientError -> INF_D_02c exits nonzero -> orion-gold-dispatch hard-fails the chain -> all downstream gold (INF_D_04, INF_D_09, etc.) never run and served platinum goes stale for the night with no client_directory refresh. Contrast: a fully-absent book.json (NoSuchKey) is handled gracefully and the run still succeeds, so the failure mode is inconsistent with the script's own intent.
- **Proposed fix:** Move json.loads inside the try and broaden the except to also catch json.JSONDecodeError and botocore.exceptions.ClientError, logging WARN and returning None so the malformed/transient case degrades the same way an absent book does (advisor recorded in advisors_missing, _meta reflects the gap), optionally with a short retry on transient ClientError. This preserves the intended graceful-skip semantics and prevents a single bad/transient book from aborting the whole nightly D-chain.
