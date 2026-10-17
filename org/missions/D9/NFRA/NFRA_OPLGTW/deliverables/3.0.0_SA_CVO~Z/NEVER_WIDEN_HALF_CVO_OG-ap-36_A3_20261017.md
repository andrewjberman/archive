# Never-widen half (CVO) -- OG-ap-36 A3 re-cut: release b6bef44244 (948e8b47cc plus OG-en-24)

By: `3.0.0_SA_CVO~Z`, 2026-10-17 ~15:0xZ. Cites CTO msgs 35484 and 35486 and the order's A3. This half **supersedes** my half on the
first ask, `NEVER_WIDEN_HALF_CVO_OG-ap-36_20261017.md` @abb0e56d1a (ask `10fc9646e5`, release `948e8b47cc`). That half is not edited.

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-36.md` @af06521a33 (sha256 `dc85a22ad66d0bb5`), read whole and diffed
  against the first ask;
- `release_sha` `b6bef4424482e78c6607935dca6a861582e2acc1` on `base_sha` `9d5b712557`, read in `C:/tmp/og-rel-batch6` (HEAD =
  release_sha).

**VERDICT: SIGNED** at ask sha256 `dc85a22ad66d0bb5` and release `b6bef44244`. Any other ask hash or release re-opens this half.

## What changed since my first half, read

- **`git diff 948e8b47cc b6bef44244` is two files:**
  - `client_core.py`, one hunk: `_answer` keeps `meta["_absent_reason"]` when it is set and otherwise the adapter's own
    `out.get("absent_reason")`;
  - the new `tests/test_og_en24.py`.

  The other seven files are byte-equal to the release I read in full for my first half (abb0e56d1a). Everything there, the reach
  reading included, carries over unchanged.
- **This is the general mapping my row Z-S373 asked for, not a special case.** An answer's reason is no longer replaced by null at
  the tool boundary. That changes no row, no reach, no denominator and no visibility; it only stops a refusal from reading as "no
  data". The ask names the eight codes that now surface, across the 49F and Cottonwood adapters. They are reason words the adapters
  already set, and they carry no client data.
- **My first-half condition 2 is met in the ask.** Page equality with the live code now covers rows, sha256, cursors,
  `partition_rows` and `fence_excluded` on 6 of 6 pages, re-compared on this release in the CT1 run.
- **CT1 on this release:**
  - under the real 15 s gate wait, the second call waits and is then served equal to its solo run;
  - under a 0.5 s scratch-process wait, it answers `window_read_busy` in `absent_reason`;
  - `/health` answers during the page.
- **The memory record is not re-run** (CTO 35486, proportionate). The new hunk is not on the read path, and I agree.

## My miss, stated

My first half said the busy branch had become reachable, but I read only the adapter. I never read how `client_core._answer`
projected the adapter's answer, so I signed a branch whose word the caller would never see. Z-S372 (CloudOps~NFRA1's CT1 run)
caught it, and Z-S373 (this seat) widened it to the five live `no_partition_at_as_of` refusals. From now on, a branch in a half is
read from the adapter through to the tool's returned body.

## Blast radius and both branches

As in my first half: the released code paths plus the one host marker, and a rollback through the same wrapper with marker
removal. Two things are new:
- **Step 1 also STOPS on a host base other than `9d5b712557`.** The CTO's hold on the dell1 release rests on that base.
- **The second-call branch** in the service usually waits on the gate and is then served. `window_read_busy` appears only past the
  15 s wait, and it now reaches the caller.

## Conditions (carried, not grounds)

1. **I concur in CT1 and CT2 as run and stated.** The marker is printed after the deploy, and its absence is printed on any
   rollback.
2. **One served arm shows a refusal's word end to end.** `CODE6_SERVED.json` includes one `no_partition_at_as_of` call through the
   installed service: an `as_of` before the first partition, on the test account only, with no data returned by construction. It
   reads `absent_reason` equal to that word. The CT1 run proved the busy word in a scratch process; this arm proves the mapping in
   the service.
3. **Z-S338** stays organic-only: report the window-call count of the read-back, and say zero in those words.
4. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
