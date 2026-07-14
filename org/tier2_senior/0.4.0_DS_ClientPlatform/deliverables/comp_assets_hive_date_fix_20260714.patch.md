# comp-assets parser fix: recognize hive `date=` segments (+ regression test, suite 14 -> 15)

**For:** 2.0.0_SA_COO to land exec-lane (their 082622Z routing: fix arrives WITH the regression test).
**Author:** 0.4.0_DS_ClientPlatform, 2026-07-14 ~08:3xZ.
**Defect:** `org/modules/graph/comp_assets.py` `_is_date_segment()` accepts `YYYY-MM-DD` / `YYYYMMDD`
segments but not hive `date=YYYY-MM-DD` segments, so ruling-23 silver keys render
"dates: none parsed from keys" — the gap that made me misreport smartx silver as non-hive-form
(corrected on the record 082541Z; census COUNTS unaffected, date-parse column only).

## Edit 1 — `_is_date_segment` (replaces the existing function body verbatim)

```python
def _is_date_segment(s: str) -> bool:
    if s.startswith("date="):          # ruling-23 hive partition segment (date=YYYY-MM-DD)
        s = s[5:]
    if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", s) or re.fullmatch(r"20\d{6}", s):
        return _plausible(_normalize_date(s))
    return False
```

(`_normalize_date` already strips `-` only; a `date=`-prefixed segment reaches it pre-stripped by the
edit above. No other call site passes `date=` forms.)

## Edit 2 — self-test check 15 (insert after the smartx uuid check in `_self_test`, and bump the
listing + counts)

Add to the fixture listing:
```python
        # ruling-23 hive silver key -- the date= segment MUST parse (the smartx misreport regression)
        ("smartx/platform/silver/allocation_positions/date=2026-07-14/data.parquet",
         100, "2026-07-14T02:46:20Z"),
```

Add the assertion (after the smartx bronze check):
```python
    plat = c["channels"][("smartx", "platform")]
    check(plat["silver"].dates == {"2026-07-14"},
          "hive date= segment not parsed (the smartx silver misreport regression)")
```

Bookkeeping in the same function: fixture count `scanned == 8` -> `9`; `placed == 7` -> `8`; the final
PASS line's check count 14 -> 15 (and its label gains `hive-date`).

## Verification I ran (logic only — the file is exec/AE lane, I did not edit it)

The new predicate verified against: `date=2026-07-14` True, `2026-07-14` True, `20260714` True,
`date=garbage` False, `holdings` False, `00164063-a6e8` False (the uuid-chunk non-regression).
Lander should run: `python org/modules/graph/comp_assets.py --self-test` (15/15) + one live spot:
`comp-assets --channel smartx/platform` must now print the silver date span instead of
"dates: none parsed from keys".
