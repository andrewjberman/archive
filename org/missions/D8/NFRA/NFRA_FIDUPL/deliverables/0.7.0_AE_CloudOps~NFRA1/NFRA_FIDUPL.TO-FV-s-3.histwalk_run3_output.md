# NFRA_FIDUPL.TO-FV-s-3 -- Historical backfill walk, run 3 (the resume after the 504; stop: budget)

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. RESUME authorised by msg 9165 (17:05Z or later, same later-run command). Runs ledger nfra-fidupl-histwalk-runs-20261021 open before the run. Started only after `date -u` read 17:05:35Z, no unread message and no other automation in progress. No cookie or profile directory was touched.

run 3: SSM 58c97efc-92a8-484c-8179-737d0e86d755 on i-028e830f7226cc685, START 17:05:39Z, Success (transport) at 17:45:57Z
command: /opt/fidelity-uploader/venv/bin/python -u /opt/fidelity-uploader/hist_walk.py --config /opt/fidelity-uploader/config.json --max-days 60 --max-seconds 2400 (SSM executionTimeout 3000)
sign-in count: ONE sign-in in this run (SIGNIN ok secs=41). Trailing hour at 17:05Z: the issuer's 16:21Z session and my run 2 at 16:35Z, so run 3 was the third, at the cap. No 401, 403, lockout or 5xx line in the stdout that SSM returned.

## IMPORTANT: the SSM stdout is TRUNCATED

SSM returned 24,619 bytes of stdout and ends the output with the marker "--output truncated--" (SSM caps StandardOutputContent). The 618 lines that came back cover the sign-in and the days 2026-08-26 back to 2026-06-30; the final STOP, CLOSE and `exit=` lines are NOT in what SSM returned. The authoritative source for the end of this run is the S3 walk record below (finished_at 17:45:42Z, run_error null, stop budget). The stdout below is the truncated text, verbatim.

## stdout as returned by SSM, verbatim (618 lines, truncated)

```
SIGNIN ok secs=41
REQ POST status.json status=200 secs=2
REQ GET profileList.json status=200 secs=11
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29278383 secs=11
FILE position bytes=29278383
FILE unknown status=200 bytes=630079 secs=1
FILE prices bytes=630079
FILE unknown status=200 bytes=12042996 secs=2
FILE psn bytes=12042996
DAY 2026-08-26 position=LANDED prices=LANDED psn=LANDED secs=125
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29159568 secs=9
FILE position bytes=29159568
FILE unknown status=200 bytes=630238 secs=1
FILE prices bytes=630238
FILE unknown status=200 bytes=11997800 secs=0
FILE psn bytes=11997800
DAY 2026-08-25 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29233274 secs=1
FILE position bytes=29233274
FILE unknown status=200 bytes=629939 secs=0
FILE prices bytes=629939
FILE unknown status=200 bytes=12027330 secs=0
FILE psn bytes=12027330
DAY 2026-08-24 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=12017000 secs=0
FILE psn bytes=12017000
DAY 2026-08-21 position=SKIPPED prices=SKIPPED psn=LANDED secs=18
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29205410 secs=2
FILE position bytes=29205410
FILE unknown status=200 bytes=632136 secs=0
FILE prices bytes=632136
FILE unknown status=200 bytes=12015272 secs=0
FILE psn bytes=12015272
DAY 2026-08-20 position=LANDED prices=LANDED psn=LANDED secs=49
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=29199188 secs=1
FILE position bytes=29199188
FILE unknown status=200 bytes=632673 secs=0
FILE prices bytes=632673
FILE unknown status=200 bytes=12013660 secs=0
FILE psn bytes=12013660
DAY 2026-08-19 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29086175 secs=2
FILE position bytes=29086175
FILE unknown status=200 bytes=609134 secs=0
FILE prices bytes=609134
FILE unknown status=200 bytes=12006306 secs=3
FILE psn bytes=12006306
DAY 2026-08-18 position=LANDED prices=LANDED psn=LANDED secs=50
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28617575 secs=10
FILE position bytes=28617575
FILE unknown status=200 bytes=608718 secs=1
FILE prices bytes=608718
FILE unknown status=200 bytes=11812882 secs=3
FILE psn bytes=11812882
DAY 2026-08-17 position=LANDED prices=LANDED psn=LANDED secs=61
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28635849 secs=9
FILE position bytes=28635849
FILE unknown status=200 bytes=611246 secs=0
FILE prices bytes=611246
FILE unknown status=200 bytes=11822962 secs=2
FILE psn bytes=11822962
DAY 2026-08-14 position=LANDED prices=LANDED psn=LANDED secs=56
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28641422 secs=9
FILE position bytes=28641422
FILE unknown status=200 bytes=612665 secs=0
FILE prices bytes=612665
FILE unknown status=200 bytes=11821408 secs=2
FILE psn bytes=11821408
DAY 2026-08-13 position=LANDED prices=LANDED psn=LANDED secs=56
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28649255 secs=9
FILE position bytes=28649255
FILE unknown status=200 bytes=613373 secs=0
FILE prices bytes=613373
FILE unknown status=200 bytes=11822476 secs=2
FILE psn bytes=11822476
DAY 2026-08-12 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28648218 secs=9
FILE position bytes=28648218
FILE unknown status=200 bytes=612190 secs=0
FILE prices bytes=612190
FILE unknown status=200 bytes=11827390 secs=0
FILE psn bytes=11827390
DAY 2026-08-11 position=LANDED prices=LANDED psn=LANDED secs=54
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28600374 secs=2
FILE position bytes=28600374
FILE unknown status=200 bytes=611638 secs=0
FILE prices bytes=611638
FILE unknown status=200 bytes=11806320 secs=0
FILE psn bytes=11806320
DAY 2026-08-10 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28630052 secs=12
FILE position bytes=28630052
FILE unknown status=200 bytes=610837 secs=0
FILE prices bytes=610837
FILE unknown status=200 bytes=11819246 secs=3
FILE psn bytes=11819246
DAY 2026-08-07 position=LANDED prices=LANDED psn=LANDED secs=60
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28584593 secs=2
FILE position bytes=28584593
FILE unknown status=200 bytes=610461 secs=0
FILE prices bytes=610461
FILE unknown status=200 bytes=11802102 secs=0
FILE psn bytes=11802102
DAY 2026-08-06 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28559480 secs=2
FILE position bytes=28559480
FILE unknown status=200 bytes=610029 secs=0
FILE prices bytes=610029
FILE unknown status=200 bytes=11795272 secs=0
FILE psn bytes=11795272
DAY 2026-08-05 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=29235323 secs=1
FILE position bytes=29235323
FILE unknown status=200 bytes=609725 secs=0
FILE prices bytes=609725
FILE unknown status=200 bytes=12092520 secs=0
FILE psn bytes=12092520
DAY 2026-08-04 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28538021 secs=9
FILE position bytes=28538021
FILE unknown status=200 bytes=611609 secs=0
FILE prices bytes=611609
FILE unknown status=200 bytes=11797374 secs=2
FILE psn bytes=11797374
DAY 2026-08-03 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28543856 secs=10
FILE position bytes=28543856
FILE unknown status=200 bytes=611576 secs=0
FILE prices bytes=611576
FILE unknown status=200 bytes=11804504 secs=2
FILE psn bytes=11804504
DAY 2026-07-31 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28493581 secs=9
FILE position bytes=28493581
FILE unknown status=200 bytes=612620 secs=0
FILE prices bytes=612620
FILE unknown status=200 bytes=11768934 secs=2
FILE psn bytes=11768934
DAY 2026-07-30 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
FILE unknown status=200 bytes=28570594 secs=9
FILE position bytes=28570594
FILE unknown status=200 bytes=613212 secs=0
FILE prices bytes=613212
FILE unknown status=200 bytes=11803268 secs=2
FILE psn bytes=11803268
DAY 2026-07-29 position=LANDED prices=LANDED psn=LANDED secs=56
REQ POST status.json status=200 secs=1
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28623984 secs=1
FILE position bytes=28623984
FILE unknown status=200 bytes=616027 secs=0
FILE prices bytes=616027
FILE unknown status=200 bytes=11826108 secs=1
FILE psn bytes=11826108
DAY 2026-07-28 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28537295 secs=11
FILE position bytes=28537295
FILE unknown status=200 bytes=614767 secs=0
FILE prices bytes=614767
FILE unknown status=200 bytes=11779130 secs=2
FILE psn bytes=11779130
DAY 2026-07-27 position=LANDED prices=LANDED psn=LANDED secs=60
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28530247 secs=11
FILE position bytes=28530247
FILE unknown status=200 bytes=614324 secs=0
FILE prices bytes=614324
FILE unknown status=200 bytes=11776244 secs=0
FILE psn bytes=11776244
DAY 2026-07-24 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28522671 secs=1
FILE position bytes=28522671
FILE unknown status=200 bytes=615711 secs=0
FILE prices bytes=615711
FILE unknown status=200 bytes=11772476 secs=0
FILE psn bytes=11772476
DAY 2026-07-23 position=LANDED prices=LANDED psn=LANDED secs=46
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28552034 secs=9
FILE position bytes=28552034
FILE unknown status=200 bytes=615060 secs=1
FILE prices bytes=615060
FILE unknown status=200 bytes=11782850 secs=2
FILE psn bytes=11782850
DAY 2026-07-22 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=1
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28420059 secs=9
FILE position bytes=28420059
FILE unknown status=200 bytes=616345 secs=0
FILE prices bytes=616345
FILE unknown status=200 bytes=11736524 secs=2
FILE psn bytes=11736524
DAY 2026-07-21 position=LANDED prices=LANDED psn=LANDED secs=58
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=3
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28269833 secs=10
FILE position bytes=28269833
FILE unknown status=200 bytes=612365 secs=0
FILE prices bytes=612365
FILE unknown status=200 bytes=11674558 secs=2
FILE psn bytes=11674558
DAY 2026-07-20 position=LANDED prices=LANDED psn=LANDED secs=60
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28194593 secs=9
FILE position bytes=28194593
FILE unknown status=200 bytes=610824 secs=0
FILE prices bytes=610824
FILE unknown status=200 bytes=11644244 secs=2
FILE psn bytes=11644244
DAY 2026-07-17 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=28084738 secs=1
FILE position bytes=28084738
FILE unknown status=200 bytes=603919 secs=0
FILE prices bytes=603919
FILE unknown status=200 bytes=11599152 secs=0
FILE psn bytes=11599152
DAY 2026-07-16 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=27948186 secs=11
FILE position bytes=27948186
FILE unknown status=200 bytes=597212 secs=1
FILE prices bytes=597212
FILE unknown status=200 bytes=11542044 secs=2
FILE psn bytes=11542044
DAY 2026-07-15 position=LANDED prices=LANDED psn=LANDED secs=59
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=29495523 secs=2
FILE position bytes=29495523
FILE unknown status=200 bytes=594621 secs=0
FILE prices bytes=594621
FILE unknown status=200 bytes=12111788 secs=0
FILE psn bytes=12111788
DAY 2026-07-14 position=LANDED prices=LANDED psn=LANDED secs=50
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=27705345 secs=1
FILE position bytes=27705345
FILE unknown status=200 bytes=582402 secs=0
FILE prices bytes=582402
FILE unknown status=200 bytes=11448778 secs=0
FILE psn bytes=11448778
DAY 2026-07-13 position=LANDED prices=LANDED psn=LANDED secs=46
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=27233659 secs=2
FILE position bytes=27233659
FILE unknown status=200 bytes=581160 secs=0
FILE prices bytes=581160
FILE unknown status=200 bytes=11278230 secs=0
FILE psn bytes=11278230
DAY 2026-07-10 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=27023410 secs=11
FILE position bytes=27023410
FILE unknown status=200 bytes=565902 secs=0
FILE prices bytes=565902
FILE unknown status=200 bytes=11207424 secs=3
FILE psn bytes=11207424
DAY 2026-07-09 position=LANDED prices=LANDED psn=LANDED secs=59
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=26924269 secs=9
FILE position bytes=26924269
FILE unknown status=200 bytes=540100 secs=0
FILE prices bytes=540100
FILE unknown status=200 bytes=11192434 secs=2
FILE psn bytes=11192434
DAY 2026-07-08 position=LANDED prices=LANDED psn=LANDED secs=57
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=26809056 secs=9
FILE position bytes=26809056
FILE unknown status=200 bytes=522627 secs=0
FILE prices bytes=522627
FILE unknown status=200 bytes=11127040 secs=3
FILE psn bytes=11127040
DAY 2026-07-07 position=LANDED prices=LANDED psn=LANDED secs=56
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=26816149 secs=9
FILE position bytes=26816149
FILE unknown status=200 bytes=523400 secs=0
FILE prices bytes=523400
FILE unknown status=200 bytes=11111220 secs=2
FILE psn bytes=11111220
DAY 2026-07-06 position=LANDED prices=LANDED psn=LANDED secs=55
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=26800736 secs=2
FILE position bytes=26800736
FILE unknown status=200 bytes=523928 secs=0
FILE prices bytes=523928
FILE unknown status=200 bytes=11108928 secs=0
FILE psn bytes=11108928
DAY 2026-07-02 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=26813618 secs=1
FILE position bytes=26813618
FILE unknown status=200 bytes=525236 secs=0
FILE prices bytes=525236
FILE unknown status=200 bytes=11126156 secs=0
FILE psn bytes=11126156
DAY 2026-07-01 position=LANDED prices=LANDED psn=LANDED secs=45
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
REQ POST status.json status=200 secs=2
FILE unknown status=200 bytes=26771799 secs=2
FILE position bytes=26771799
FILE unknown status=200 bytes=524706 secs=0
FILE prices bytes=524706
FILE unknown status=200 bytes=11101598 secs=1
FILE psn bytes=11101598
DAY 2026-06-30 position=LANDED prices=LANDED psn=LANDED secs=47
REQ POST status.json status=200 secs=2
REQ POST historicalExport.json status=200 secs=1
REQ custom status=200 S
REQ POST historicalExport.json status=200 secs=1
REQ standard status=200 S
REQ POST status.json status=200 sec--output truncated--
```

## stderr, verbatim

```
WARN: trading_calendar: pandas_market_calendars absent; answering from the hardcoded NYSE fallback NYSE/hardcoded-fallback-2010-2027 (covers 2010-2027; regenerate with lib/tests/gen_nyse_closures.py --write before 2028)
```

## The walk record (s3://opal-data-assets/fidelity/alongside/bronze/_runs/20261021/histwalk-20261021T170538Z.json, 8454 bytes)

```
keys: ['caps', 'days', 'finished_at', 'histwalk', 'partial', 'per_type', 'run_error', 'run_id', 'scope', 'sign_ins', 'started_at', 'stop']
histwalk = true
sign_ins = 1
run_error = null
stop = {"evidence": "wall budget reached before 2026-06-24", "reason": "budget"}
run_id = "20261021T170538Z"
started_at = "2026-10-21T17:05:38Z"
finished_at = "2026-10-21T17:45:42Z"
caps = {"max_days": 60, "max_seconds": 2400}
partial = false
per_type = {"position": {"bytes_landed": 1212319781, "earliest_landed": "20260625", "empty_days": 0, "landed_days": 43, "skipped_days": 1, "stop_reason": null, "stopped": false}, "prices": {"bytes_landed": 25502100, "earliest_landed": "20260625", "empty_days": 0, "landed_days": 43, "skipped_days": 1, "stop_reason": null, "stopped": false}, "psn": {"bytes_landed": 512865310, "earliest_landed": "20260625", "empty_days": 0, "landed_days": 44, "skipped_days": 0, "stop_reason": null, "stopped": false}}
days: 44
first: {"date": "2026-08-26", "results": {"position": "LANDED", "prices": "LANDED", "psn": "LANDED"}, "secs": 125}
last 2: [{"date": "2026-06-26", "results": {"position": "LANDED", "prices": "LANDED", "psn": "LANDED"}, "secs": 56}, {"date": "2026-06-25", "results": {"position": "LANDED", "prices": "LANDED", "psn": "LANDED"}, "secs": 57}]
```

## What the record shows

- Stop: budget, "wall budget reached before 2026-06-24"; run_error null; sign_ins 1; started 17:05:38Z, finished 17:45:42Z.
- Days walked in run 3: 44 trading days, 2026-08-26 back to 2026-06-25, 47 to 125 s per day; every day position, prices and psn LANDED, apart from one skipped position and prices (already landed).
- Run 3 totals: position 43 days landed, 1212319781 bytes; prices 43 days, 25502100 bytes; psn 44 days, 512865310 bytes; earliest landed 20260625 for each. No type has stopped (stop_reason null, empty_days 0).
