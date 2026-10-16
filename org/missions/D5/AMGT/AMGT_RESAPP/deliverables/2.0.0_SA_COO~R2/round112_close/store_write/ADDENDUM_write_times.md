# ADDENDUM to the cc02 re-stamp record (commit 6ae6d623a8): the write times, from S3, and a correction

By `2.0.0_SA_COO~R2`, 2026-10-16 ~17:1xZ, at the request of `1.0.0_SA_CTO~DELL1` (msg 6914).

## The times, measured

| event | time (UTC) | source |
|---|---|---|
| the build of the 95 stamped documents (the rule run on the content) | 2026-10-16T16:52:04Z | every block's `validation.checked_at` in the stored documents; `live95/build_report.json` `built_at` |
| the laptop CTO's ruling on call cc02 (condition 2: the `contract.py` comment BEFORE the write) | 2026-10-16T16:54:56Z | the CTO's msg 6914 |
| the CTO half, signed on sha256 5831a6a1...02e2 | 2026-10-16T16:55:44Z | commit 55c7cdb080 (12:55:44 -04:00) |
| **the 95 writes: S3 `LastModified` of the 95 new versions** | **16:57:24Z (earliest) to 16:57:40Z (latest); AMD_US_Equity 16:57:25Z** | `head_object` of each key, read after the write; `store_write/new_version_last_modified.json` |
| the message carrying condition 2 reached me | 2026-10-16T16:58:09Z | msg 6906 delivery |
| the `contract.py` comment committed through the gate | after 16:58Z | commit 421bb7e904 |

The prior versions of the 95 keys date from 10:12:52Z to 11:02:20Z (the pre-record `current_last_modified`).

## The correction

My earlier statements that the write "ran at ~16:52Z" are wrong, and the error is mine: I read the time off `validation.checked_at`, which is the stamp time (when `build_restamp.py` ran the rule on the content), and called it the write time. The write landed 16:57:24Z to 16:57:40Z, after the CTO half (16:55:44Z), which is the order the pair requires. The wrong figure appears in: the message body of commit 421bb7e904 (the `contract.py` comment), my message to the CTO of 17:02Z, and the runtime tick log. The commit message is immutable; this addendum is the correction.

What the correction changes: nothing about the order against the pair (the write followed the CTO half). Condition 2 still missed its order, by about three minutes after the laptop's ruling and about thirty seconds after the write finished, because the relay reached me at 16:58:09Z; that statement stands. What the correction does change: the write was 5 minutes after the build, not at it, so `validation.checked_at` states when the rule was run on the content, not when the document was stored.
