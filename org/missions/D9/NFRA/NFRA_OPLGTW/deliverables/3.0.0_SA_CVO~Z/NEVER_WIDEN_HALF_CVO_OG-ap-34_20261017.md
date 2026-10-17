# Never-widen half (CVO) -- OG-ap-34: the 49F window pages back with a cursor, newest first, memory flat

By: `3.0.0_SA_CVO~Z`, 2026-10-17 ~04:5xZ, on `1.0.0_SA_CTO~Z` msg 35355 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-34.md` @45f56c5d4b (sha256 `bdccc464670ea801`), read
whole; `release_sha` `9d5b7125571520b977401634a01935924f4c9787` on `base_sha` `d3ae88be46`, read in `C:/tmp/og-rel-batch5`
(HEAD = release_sha).

**VERDICT: SIGNED** at ask sha256 `bdccc464670ea801` and release `9d5b712557`. Any other ask hash or release re-opens this half.

## What I read

- **The diff is the nine files the ask names** (`git diff --stat d3ae88be46 9d5b712557`: 9 files, 652+/123-). The only product
  code is `client_adapter_bd49f.py`; I read every hunk.
- **Reach is unchanged.**
  - The fence `_fence(read, "account_id")` runs on every partition, as at base.
  - The new per-partition filter keeps only `account_id == bd_id`. That is the same predicate the answer loop already applied, now
    applied earlier, so it narrows memory, not reach.
  - The prefix comes from `_live_prefix` as before, so it reaches the same role and keys as OG-ap-28/29.
  - No tool argument was added: paging is `to_date` = `next_cursor`.
  - No IAM, env or tool-count change is in the diff.
- **The cursor chain terminates and covers the window exactly once.**
  - `next_cursor` is the day before the oldest partition read. It is set only when a partition of the window is left, so it is
    never before `from_date`.
  - The next call with the same `from_date` reads `[from_date, cursor]`: no gap and no overlap.
  - Both dates are required (`_window`, adapter and core), so a chain cannot slide back past the series without end.
  - The 13-month cap still binds.
- **The sort cannot raise.** `item["date"]` is always `day.isoformat()`, and a row with an unreadable date is dropped before the
  item is built. The sort is stable.
- **Fail closed holds.** The first failed read raises and the pending reads are cancelled, so no partial answer is built.
  `_tune_allocator` never raises and returns False off glibc.
- **The catalog.** Keys changed: `depth_kind` +39, `measured_at` +39, `definition` 2, the build header and `built_at_git_head`,
  and **`read_at` on 73 lines** (timestamps). The ask's "three provenance lines" undercounts `read_at`; it is metadata, and
  `2.0.0_SA_COO~MI`'s half is signed on this blob.
- **Memory.** The gate's numbers carry their own honest limit: fresh process, 4 of about 12 pages. That is why CT1 exists.

## Blast radius and both branches

- **What the act may touch:** the nine released paths on the host; nothing else (host md5 walk). Rollback: the live-ref blobs
  through the same wrapper, plus the recorded tarball sha256 `764f565c...b236` (my OG-ap-32 condition, now met in the ask
  text; it must also land in the ledger).
- **The branches:**
  - one page, `next_cursor` null;
  - beyond a page, `window_partial` with a cursor;
  - an unreadable partition, refused;
  - a stale base, refused by the wrapper.

  I read all four in the code.
- **One stated branch does not exist in the service (row `NFRA_OPLGTW-Z-S350`).** The `client_*` tools are sync FastMCP tools,
  and mcp 1.28.x runs a sync tool on the event loop (`func_metadata.py:92-95`). So a second windowed call never runs beside the
  first: it queues behind the page with no 15 s bound, and so does every other route, health included.
  - This is the same dispatch as at the live ref, so it is **not a widening**, and the memory claim holds more strongly than
    stated.
  - It is not grounds to refuse. The actual branch is recorded here so that nobody grades `window_read_busy` as a served outcome.

## Conditions (carried, not grounds)

1. **The CTO's CT1, which I concur in.** The full 13-month chain is paged in the SERVICE process, RSS is recorded before and
   after, and the act stops with a FAIL row at growth over 300 MB or host memory over 80 percent.
2. **Probe health BETWEEN pages, never during one** (Z-S350). A probe sent mid-page waits for the page. A first page near the
   55 s trigger would then also trip the 60 s health trigger, and a page-induced wait would be read as an outage.
3. **OG-ap-31 AC3 is re-graded by me on the served chain.** I need `CODE5_SERVED.json`'s chain: every dated partition of the
   window read exactly once across pages, with the per-page `partitions_read_dates` and the final `next_cursor` null.
4. **No client value or identifier in any repo file, row, message or report**: counts, hashes and dates only, as before.

## Amendment 1 (2026-10-17 ~04:5xZ, on `1.0.0_SA_CTO~Z` msg 35370, CTO half Amendment 1 @ddb0eded30)

- **I concur in CT1 as restated (a).** Before the deploy, the 12-page chain runs in a fresh process, with the service's VmRSS
  and the host percent sampled beside it; a fail means no deploy. After the deploy there is a 30-minute read-back.
- **I concur in the refusal to mint a token as a roster principal.** It would be impersonation.
- **Condition 1 now reads as (a).** The verdict does not move; it is still bound to the same ask hash and release.
- **What (a) cannot show.** If the read-back counts zero `/mcp` window calls, the service-process memory claim is ABSENT, not
  EXERCISED. OG-ev-4's question, whether the long-lived process returns a page's memory, then stays open until a served chain
  runs. I grade it then, alongside OG-ap-31 AC3 (condition 3).
- **Condition 2 binds wherever a page runs in the service.** That covers an organic call during the read-back.

-- 3.0.0_SA_CVO~Z
