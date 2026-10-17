# ADHOC.canon-r11-orion-reader-trail -- step 2 read (0.7.0_AE_CloudOps~DELL1, 2026-10-17 16:31Z to 16:35Z)

Claim words: `measured` = read this session by `orion_logread.py` (this folder); summary `ORION_READ_SUMMARY_20261017.json`.

## Denominators (measured)
- Logging on `opal-data-assets` live since 2026-10-16T18:40Z (target `opal-data-security-access-logs`, prefix `opal-data-assets/`). Log objects delivered from 2026-10-16 19Z to 2026-10-17 16Z: 15,979 objects (first 19:14:09Z on the 16th; last 16:33:27Z on the 17th), per delivery hour printed in the summary (06Z..16Z on the 17th: 515, 556, 314, 302, 427, 596, 384, 660, 3963, 333, 485).
- 129,704 log lines read, 129,704 parsed (0 unparsed). Operations: REST.GET.OBJECT 83,278, REST.GET.BUCKET 22,432, REST.HEAD.OBJECT 12,909, REST.PUT.OBJECT 10,911, REST.COPY.OBJECT 85, REST.GET.BUCKETVERSIONS 18.

## The `orion/` GETs (REST.GET.OBJECT, key beginning `orion/`): 4,529 lines, all HTTP 200, 5,360,496,474 bytes sent
- Requesters as the log shows them: `assumed-role/mdpf-gold-lambda-role/mdpf-gold-lambda` 4,494 (99.2%); `user/cloudops-dell2-agent-user` 27; `assumed-role/opal-assets-silver-orion-role/opal-assets-silver-orion` 8.
- Source IPs: AWS addresses for the lambda (eight addresses carry 489 to 978 GETs each); the dell2 user's single address 27. User agents: Boto3 on Linux 4,502 (the lambda and the silver role), Boto3 on Windows 27.
- Key prefix to the second level: `orion/inflection/` for all 4,529.
- Per hour (UTC): 10-16 18Z 2, 21Z 1, 22Z 8 (all the dell2 user); 10-17 02Z 489, 03Z 978, 04Z 1,956 (the gold lambda), 13Z 497 (489 lambda, 8 silver role), 14Z 16 (dell2 user), 15Z 582 (lambda, the D4-ref and D4-new invokes of ADHOC.canon-r11-global-axis-deploy).
- Size: mean 1.18 MB; 1,011 GETs at or above 1 MB; 28 at or above 10 MB, largest 42.6 MB.

## The 06Z-16Z window of 2026-10-17 (the order's window)
1,095 `orion/` GETs, 1,640,201,041 bytes (13Z 497, 14Z 16, 15Z 582). **The E4 burst did NOT recur.**

## Sum against E4 (order condition 3)
- Bytes seen in the logs, all 22 hours logged: 5.36 GB; in the 10-17 06Z..16Z window: 1.64 GB.
- Bytes E4 counted: `orion/` 122.10 GB over 26 hours, 99.4% in 2026-10-16 06Z..16Z.
- Difference about 116.7 GB (all-hours) or 120.5 GB (window). Reason: the E4 burst is on 2026-10-16 06Z..16Z, before the logging went live at 18:40Z; the logs cover none of it, and the same window one day later carried 1.64 GB.

## Verdict
**The reader of the 2026-10-16 burst is NOT NAMED.** The logged readers of `orion/` are the gold lambda role, the dell2 CloudOps user and the silver orion role, at about 5.4 GB in 22 hours. No requester is inferred for the burst. Note, as a lead and not a finding: the burst's GET shape in E4 (few GETs of about 18 MB) is closer to the dell2 user's 27 GETs (mean about 34 MB) than to the lambda's (mean about 1.1 MB); the logs show the dell2 user at 14Z on the 17th but nothing at burst scale.

## Open
- Logging stays on until a burst is caught or 2026-10-19T18:39Z (order step 3). A second 06Z..16Z window (2026-10-18) falls inside it; a read after 16:30Z on 2026-10-18 would test whether the burst is a daily event.
