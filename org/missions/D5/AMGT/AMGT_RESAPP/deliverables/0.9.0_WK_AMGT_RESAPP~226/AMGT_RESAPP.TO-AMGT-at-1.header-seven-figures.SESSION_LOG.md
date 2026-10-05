# Session log -- 0.9.0_WK_AMGT_RESAPP~226 on AMGT-at-1

- Base measured: r70_served c30 --where local, 43 of 95 names failing (short interest on HK/JP/European names, enterprise value on some, four figures on ROG_SW). All 95 have a stored block; every missing figure is named as returned empty in the block's own list.
- Change: lib/research/api/scoped_amgt.py `_header_figures` (+ HEADER_SEVEN, `_header_seven_reason`); both header builders call it. Commit e7e3670099.
- Check face: a reasoned null sets `currency_caveat`, so the figure check reads PROVISIONAL (amber), not PASS.
- Api suite: 1 failed, 581 passed; the one failure is test_model_words.py (portal function absent at this worktree's portal ref), no row.
- No new S3 read path. No row filed. No vendor leg: every missing figure was served as a reason, none needed a new pull.
- The portal's rendering of a header figure with value null was not read (portal write is out of bounds); AMGT-at-6 or the next portal cell should confirm it renders a reason instead of a blank.
