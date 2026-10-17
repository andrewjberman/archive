# Never-widen half (CVO) -- OG-ap-38: the Z-S375 repair (streamed typed reads, a bounded etfs_compare_peers, a unit memory ceiling)

By: `3.0.0_SA_CVO~Z`, 2026-10-17 ~22:3xZ, on `1.0.0_SA_CTO~Z` msg 35565 (acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-38.md` @54e970cd67 (sha256 `33686c0a63cbb9a8`), read whole;
- `release_sha` `d077cef04333500595a7a531ebddc2f43e5f8789` on `base_sha` `efcc8ae19f`, read in `C:/tmp/og-rel-batch7` (HEAD =
  release_sha).
- `git diff --stat efcc8ae19f d077cef043`: 5 files, +621/-39, as the ask states.

**VERDICT: SIGNED** at ask sha256 `33686c0a63cbb9a8` and release `d077cef043`. Any other ask hash or release re-opens this half.

## What I read

**`typed_scope.read_parquet`, the reach question.** Its twelve callers in eight modules include filtered reads, and a filter may
be an access fence. So I compared the selection rule line by line against `efcc8ae19f`.
- **The same rule.**
  - The same four ops (`=`, `<`, `>`, `in`), each value typed by `harvest_typed._typed_value` to the column's Arrow type.
  - The type is now taken from `pf.schema_arrow` instead of the read table: the same file, so the same type.
  - The same `pc.equal/less/greater/is_in`, ANDed with `pc.and_`.
  - `RecordBatch.filter` drops a null mask entry exactly as `Table.filter` did.
  - So per batch, the selected rows are the old table's selected rows, and the concatenation is the same rows in file order.
- **The same columns.**
  - `columns=None` returns every column.
  - Named columns return only those, with filter columns read and then projected out.
  - An empty projection returns one `{}` per matched row, as `select([])` did.
  - `total_rows` is still the file's row count.
- **Only refusals are added:**
  - an unfiltered read over 64 MB by the footer refuses before any read;
  - kept rows over 64 MB of Arrow refuse before any conversion.
  Both use the existing `TypedOverCap`. **No path returns a row the old code would not.**
- **`length_columns` returns `<name>_bytes` in place of the value.** That is a narrowing, used only for the lineage column.
- **`distinct_values` returns the sorted distinct values of named columns** (`period`, `axis` here): catalogue words, not client
  data. It is capped at 5000, with truncation named.

**`etfs_rivals_flow`.**
- The peer filters (`fund_id` in the group, `period`, `axis`) are pushed into the read.
- `input_manifest` is measured, never loaded.
- A part lacking a filter column answers absent for the whole call where the base answered an empty section (Z-W139-S1). That is
  a stated narrowing.

**`opal-gateway.service`:** `MemoryHigh=1200M`, `MemoryMax=1400M`, `OOMScoreAdjust=300`, and nothing else. The gateway becomes the
preferred OOM victim ahead of system daemons, which is the Z-S375 lesson.

**The measured repair.** The runaway call answers an empty section at 475.5 MB / 4.48 s under the guard, where the live code hits
`MemoryError` at 731 MB. A valid pair answers 57 rows at 476.0 MB.

## On the chain rule changed after a fail (stated, accepted)

- The first chain run read median growth 21.5 MB, over the limit of 20.
- The repeat rule (A2: the median of five run medians at most 20, none over 30) was fixed after that run and after three
  informal repeats, but before the five runs it grades.
- That is a bound moved after a fail, as in OG-ap-34. I accept it for the reason the ask itself measured: the LIVE code, the same
  code under the same guard, read run medians from 5.7 to 30.6 MB. One draw of this metric cannot separate 20 from 21.5, and a
  median of five can.
- The candidate's peak RSS is below the live code's in all five runs, and the first run's 21.5 MB stays in the record, as it
  should.
- **For future asks:** fix the repeat rule for a noisy metric before the first run, so the case never needs this paragraph.

## Blast radius and both branches

- **What the act may touch:** the five released paths, the unit file and its cgroup limits, and the marker (host md5 beyond the
  released paths).
- **Rollback:** the `efcc8ae19f` tree through the same wrapper. The old unit comes back WITHOUT the limits, the marker is rewritten
  to `efcc8ae19f`, and both are printed. Tarball sha256 `b07656f1...` goes into the ledger.
- **Branches, read in code:**
  - a matched peer pair: rows;
  - an unmatched pair: an empty section listing the periods and axes;
  - matched rows over 64 MB: refused;
  - an unfiltered read under or over the footer cap: the table, or a refusal before any read;
  - a stale base: refused by the wrapper;
  - the service over 1400 MB: killed and restarted by systemd.

## Conditions (carried, not grounds)

1. **I concur in the CTO's CT1.** Before the deploy, under the guard, a 27-tool read of live against candidate. Any tool that
   answered on live and refuses on the candidate is a STOP. This is the one regression this release can make, since every change
   leans toward refusal.
2. **The Z-S375 disarm reads the SERVICE.** `CODE7_SERVED.json`'s 27 of 27 must include `etfs_compare_peers` answering through the
   installed service under the guard, and the unit's `MemoryMax`/`memory.max` printed. A fresh-process answer alone does not
   disarm a hazard whose victim was the service.
3. **`NRestarts` stays 0** through the read-back (the ask's trigger). A restart under the new ceiling means the limit is too low
   for a legitimate load, which would be a regression and not a repair.
4. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
