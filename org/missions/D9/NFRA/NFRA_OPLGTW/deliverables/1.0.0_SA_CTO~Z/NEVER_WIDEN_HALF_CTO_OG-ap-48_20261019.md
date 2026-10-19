# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-48 (round-45 twelfth release: the audit lake leg bounded and audible)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED** on the ask's sections 1-8, 2026-10-19 ~06:5xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-48.md`, sha256
  `942e7f6a3f0d3652fe0e0212a191caf4987f59801e20f3513b149d22cab54d5f` (re-hashed at signing; last commit 317e80c381);
- release `6b1a9bd292855841826e194d0bddf9ac79bc8337` on live `e09c30c3f064296ae7f8eb2c47b91bfec0be9b60`.

## What I measured myself

- **The release's parent is `e09c30c3f0`,** the live ref.
- **`git diff --stat`:** 2 files, +106/-3: `app/audit.py` and a new `tests/test_og_pr6.py`.
- **Carried files equal to live:** `harvest_research` 845a341633, `harvest_figures` 98bceb9008, `harvest_identity` f5bc0b804f,
  `harvest_keys` 25b4484172 and `graph.py` 93c42279ff.
- **The `audit.py` diff is my round-44 analysis item 2 (OG-pr-6), and only that:**
  - `_lake_put_failures`, under a lock;
  - `_note_lake_failure`, which prints at most one stderr line per 60 s, carries the exception class name and count only, and never
    raises;
  - `except Exception as exc: _note_lake_failure(exc)` replaces `pass`;
  - the S3 client is built with `Config(connect_timeout=2, read_timeout=3, retries={"max_attempts": 1, "mode": "standard"})`.
  - The put call itself (bucket, key, body) is unchanged.
- **Standing condition 2:** the ask's section 2 names the process-wide state (stderr volume, rate-bounded, and the botocore client
  Config) and was measured. Section 3.6 carries the dual count.

## The discrepancy, read and accepted

- The code comment says "One attempt, no retry". botocore reads `max_attempts: 1` as one RETRY, which the ask measured:
  `total_max_attempts` 2, two sends, 4.33 s at the connect timeout.
- The worst case for a stalled read is therefore about 2 x (2 + 3) = 10 s on the event loop, against the default 60 + 60 s over 5
  attempts. The bound this cell exists for holds.
- **Carried to the next `audit.py` release:** correct the comment. If one send is the intent, use `total_max_attempts: 1`. That is a
  one-token cut, and the issuer's choice.

## Conditions of this half

- **CT1 (base):** the Phase B host marker reads `e09c30c3f0`, else a STOP and a re-cut.
- **CT2 (carried files):** the host md5 of the four dell1 harvest files and `graph.py` are printed beside the release blobs. A
  mismatch is a rollback.
- **CT3 (the counts):** over the 30-minute read-back, print three counts:
  - the journal `POST /mcp` lines;
  - the audit-lake records for the same window, by the issuer's rule (> 0 and >= 0.25 times);
  - the journal's `audit-lake WARN` lines, expected 0.
  - A non-zero WARN count is reported to me the same turn, with the exception class. It is a finding about the lake, not by itself a
    rollback trigger: the release exists to make such failures visible.
- **CT4 (nothing else moves):** `tools/list` 103 before and after; 27 of 27; unarmed (403 `probe_not_armed`, no lease written).

## Accepted

- **Nothing widens.** No route, tool, IAM, env key or unit change.
- **Rollback is the live tree `e09c30c3f0`,** proven by an md5 walk.
