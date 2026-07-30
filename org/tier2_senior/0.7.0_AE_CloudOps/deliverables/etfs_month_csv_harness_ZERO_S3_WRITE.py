#!/usr/bin/env python3
"""ZERO-S3-WRITE exercise harness for render_month_end.write_month_csvs().

Owner: 0.7.0_AE_CloudOps~A (2026-07-30). Shared to 0.4.0_DE_ClientPlatform on request
(COO 064748Z: reuse this, do not stand up a second harness) for the Aug-1 per-partner
carried-forward disclosure work.

  python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/etfs_month_csv_harness_ZERO_S3_WRITE.py
  python ...py 2026-07                 # single month
  python ...py 2026-07 2026-06         # target + positive control (the DEFAULT, and do not skip it)

=============================================================================
ZERO-WRITE PROPERTY -- WHAT IS EXERCISED vs WHAT IS INFERRED. Read this.
=============================================================================
S3 **IS** TOUCHED. Reads only. "Zero S3 writes" is NOT "does not touch S3", and
conflating the two is how someone concludes this needs no credentials.
  READS  (required): load_universe -> GetObject config/etf_universe.json
                     load_all_daily -> ListObjectsV2 daily/{partner}/ + GetObject per date-key
  WRITES (none)     : write_month_csvs' body only ever does open(path,"w") into out_dir and
                      returns the local paths.

EXERCISED (0.7.0_AE_CloudOps~A, 2026-07-30, both months):
  s3://opal-data-etfs/platinum/reports/ listed BEFORE and AFTER the run.
    BEFORE 4 keys, 0 .csv, 2026-07/ absent
    AFTER  4 keys, 0 .csv, 2026-07/ absent -- and the 4 LastModified values are UNCHANGED
           (2026-06-25 19:28:53 x2, 2026-07-01 10:00:48 x2). An overwrite would move them.
  The 3 produced July CSVs existed ONLY under a local tempfile.mkdtemp() dir.
INFERRED, NOT EXERCISED (stated so nobody upgrades it):
  Bucket-WIDE absence of writes. The before/after control covers platinum/reports/ -- the
  prefix that matters, because that is what the real Aug-1 run enumerates and attaches.
  It does not prove nothing was written to some other prefix.

WHY THIS MATTERS MORE THAN USUAL: the real run enumerates platinum/reports/{month}/ and
attaches whatever it finds. An ad-hoc artifact written there becomes PRODUCTION EVIDENCE on
a partner-payment basis. That is why this harness calls write_month_csvs DIRECTLY and never
main() -- every S3 put_object for the CSVs lives in main(), which is never invoked here.
=============================================================================

GOTCHAS that are not visible from reading render_month_end.py:

1. NATIVE-WINDOWS PATH. This runs under native python, which CANNOT resolve an MSYS
   /cygdrive/c/... path -- that spelling ModuleNotFoundError'd on the first attempt. The
   sys.path entry below uses the native drive-letter form deliberately (a raw string). Do not
   "tidy" it to a posix path.
2. PASS THE MONTH EXPLICITLY. Never rely on a default. The orchestrator's _last_month()
   uses a FIXED -5 (EST) offset, not ET-with-DST: at the scheduled 14:00Z fire it resolves
   2026-07 correctly, but any invoke between 00:00Z-05:00Z on Aug-1 resolves 2026-06 and
   would silently rehearse THE WRONG MONTH and pass. render_month_end._resolve_month() is a
   different function again. Passing a literal sidesteps both.
3. RUN THE POSITIVE CONTROL. A month with known data (2026-06) must be run alongside the
   target, or a zero/short result for the target is uninterpretable -- you cannot tell
   "no data yet" from "the function is broken". June is a COMPLETE month and returns a
   uniform 3 x 31-column result; that is also the exercised proof of _month_cap's
   complete-month branch.
4. IN-PROGRESS MONTHS ARE RAGGED BY DESIGN, NOT BROKEN. Run against 2026-07 before Aug-1
   and you get per-partner column counts (e.g. 28/29/27 of a 31-day July) because
   _month_cap MTD-caps an in-progress month (:164-175). On Aug-1 the same code returns
   m_end unconditionally and all three become 31 days. Do not "fix" this.
5. DO NOT TOUCH _month_cap. It implements Andrew-ruled full-calendar-month billing with a
   CVO verification behind it (+$790,884 on May 49F, 2026-07-07).
6. Needs credentials with READ on opal-data-etfs. Runtime is a few seconds per month; it
   does a GetObject per date-key (60-71 keys/partner), so it is call-count-bound, not
   CPU-bound. No local data required -- it pulls everything.
"""
from __future__ import annotations

import os
import sys
import tempfile
import traceback

sys.path.insert(0, os.path.join(
    r"C:\Users\AndrewBerman\Desktop\ajb_workspace",
    "data", "etfs", "scripts", "presentation"))

import render_month_end as R  # noqa: E402


def exercise(month: str, label: str) -> list[str]:
    print(f"\n=== {label}: write_month_csvs({month!r}) ===")
    out_dir = tempfile.mkdtemp(prefix=f"etfsqa-{month}-")
    print(f"    local out_dir: {out_dir}")
    try:
        paths = R.write_month_csvs(month, out_dir)
    except Exception as e:
        print(f"RAISED: {type(e).__name__}: {e}")
        traceback.print_exc()
        print(f"VERDICT {label}: THROWS. Note the blast radius -- render_month_end.py:644 calls "
              f"this UNCONDITIONALLY with no try/except, UPSTREAM of every S3 upload, under "
              f"`set -e`. A throw here costs the PDF too: total non-delivery, not degraded.")
        return []
    print(f"RETURNED {len(paths)} path(s)  (CANONICAL_PARTNERS={R.CANONICAL_PARTNERS} -> "
          f"{len(R.CANONICAL_PARTNERS)} is the structural max)")
    for p in paths:
        with open(p, encoding="utf-8") as f:
            head = f.readline().rstrip("\n")
            row2 = f.readline().rstrip("\n")
        cols = head.split(",")
        print(f"  {os.path.basename(p)}  {os.path.getsize(p)} B  days={len(cols)-1}  "
              f"first={cols[1] if len(cols) > 1 else '-'}  LAST={cols[-1]}")
        print(f"    row2: {row2[:110]}")
    print(f"VERDICT {label}: NO EXCEPTION, {len(paths)} CSV(s) -> attach set would be "
          f"{len(paths)} CSV(s) + 1 PDF")
    return paths


if __name__ == "__main__":
    months = sys.argv[1:] or ["2026-07", "2026-06"]
    print(f"universe = {R.load_universe()}")
    for i, m in enumerate(months):
        exercise(m, "TARGET" if i == 0 else f"POSITIVE CONTROL ({m})")
    print("\nREMINDER: verify zero-write yourself -- list s3://opal-data-etfs/platinum/reports/")
    print("before and after and compare BOTH the key count AND the LastModified values.")
