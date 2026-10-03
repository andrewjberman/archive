# AMGT_RESAPP round 66 -- `AMGT-ap-4` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-03 ~23:1xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at build commit `b642e313f9`, or a descendant whose CONTENT-DIFF equals the list
below. Build and upload ONE artifact, then ONE code-only `safe-apply`. `memory_size` stays 1769.
- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-ap-4.the-code-redeploy.md`.
- It carries:
  - `c20fd8cc98`: the chatter `tone_reason` text, on Andrew's ~18:xxZ deletion order;
  - ap-1, drained `2674ac7ba8`: FWD-39 word cloud;
  - ap-2's route read, drained `8f10187a78`: FWD-36 price 90/365.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `lPTMo20TWOn9GxEyMPa4EausVvWKpvyGQTeZcVFZlW0=` (ao-2, LastModified 2026-10-03T19:47:12Z) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `5xO0vR9UWlx.XI59G0KNLJyAsjMKOes4` (ao-2's upload) |

## THE FILE LIST (`--build-only` at `b642e313f9`)

The build read rc=0, cold-start FATAL [], request-time break [], and isolated 3 of 3. Against `lPTMo20T...`:
`CONTENT-DIFF SUMMARY: files 355, IDENTICAL 350, CHANGED 5, ADDED 0, REMOVED 0`. The package is 253,736,960 B (96.8%, 8,407,040 B
spare).

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/rolling_windows.py` | CHANGED | `c20fd8cc98` + ap-2 | chatter `tone_reason` reads "window tone is not served on this route yet" (c19); `price_window_axis` names the 90/365 axes |
| `lib/research/api/scoped_amgt.py` | CHANGED | ap-1 + ap-2 | the range route serves `word_cloud` (c18); `?days=90|365` serves the latest 90/365 generation with `window_end`, and a `window_note` where it is earlier than the last trading day (c22) |
| `lib/research/harvest/timeline_api.py` | CHANGED | ap-1 | `get_timeline` accepts an optional `word_cloud_builder`; no other field moves |
| `lib/opal_naming.py` | CHANGED | 4.0.0_SA_CRO `b77e2af4d5` (IRPT_DASHBD-S12) | NONE through this function. See below |
| `infra/logic/registry/reporting_policies.json` | CHANGED | same commit | NONE through this function. See below |

**Why the two naming files have no served effect through this function:**
- The diff touches only the reporting-family validator (`_validate_reporting_policies`) and `_reporting_destination`.
- The comp-find census over `lib` and `infra/aws/lambda` finds them called only by investor-reporting and the mdpf builders, and
  by opal_naming itself.
- The validator also runs at registry load (`opal_naming.py:364`), so it executes in this function. The registry load was proved
  in-process at `b642e313f9`:
  - `import lib.opal_naming` succeeds;
  - c9, c11-c14, c17, c18 and c19 all read YES locally;
  - the 6-suite union was 1092 passed at the ap-2 drain, which already carried `b77e2af4d5`.

Any other changed file at build time is a STOP.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `5xO0vR9UWlx.XI59G0KNLJyAsjMKOes4` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `lPTMo20T...` |

## EXPECTED OUTCOME -- both branches

| check | base (deployed lPTMo20T) | after (local at b642e313f9) |
|---|---|---|
| r66 c19 | NO: the terms-card wording on all 4 chatter windows | YES |
| r66 c18 | NO: no `word_cloud` | YES: BA 40, AMD 40, VLO 22 terms; empty window with its reason |
| r66 c22 | NO: 0 rows, "not produced yet" (re-read ~23:1xZ, after ap-3) | YES (~23:1xZ, after ap-3 `444ad788f4`): trending and breakout x 90 / 365 serve 94 / 95 rows, `window_end` 2026-10-02 = the last trading day |
| r64 c9, c11-c14; r65 c17 | YES | YES |
| r64 c10 (30-day clauses) | YES | YES |
| r64 c15 (cold read; the DAY route) | YES, 1.9-2.3 s at round 64 | read on deployed; the range route's local cold read rose ~1.5 s from the headline read, and c15 grades the day route |

**Failure branch:** any of the following is a ROLLBACK per the table:
- c18, c19 or c22 is not YES;
- any other check moves;
- c15 reads over 5 s;
- a non-200 on a covered key's overlay, thesis, peers, timeline or collected/chatter.

## WHAT THIS HALF DOES NOT COVER

Any of the following in the plan is a STOP:
- a memory change;
- a store write or an S3 delete;
- a vendor call;
- an IAM, route or gateway change;
- a data-engineering operation.
