# ADHOC.canon-r11-orion-reader-trail -- second window read (0.7.0_AE_CloudOps~DELL1, 2026-10-18 16:31Z to 16:33Z)

Claim words: `measured` = read this session by `orion_logread.py` with `ORION_START=2026-10-17T16:00:00Z`; summary `ORION_READ_SUMMARY_20261018.json`. Event hours below are the request time in the log line, not the delivery hour.

## Denominators (measured)
- 7,263 log objects delivered between 2026-10-17 16:11:31Z and 2026-10-18 16:31:39Z (per delivery hour in the summary; 06Z..16Z today: 202, 18, 9, 18, 14, 26, 33, 356, 3817, 18, 2). 77,960 log lines read, 77,960 parsed (0 unparsed). Operations: REST.GET.OBJECT 43,199; REST.HEAD.OBJECT 13,469; REST.PUT.OBJECT 10,916; REST.GET.BUCKET 10,324.
- The last delivered object is 16:27:29Z at the first listing (16:31:39Z at the read), so requests up to about 16:00Z are covered with the usual delivery lag.

## The `orion/` GETs in those objects: 1,479 lines, all HTTP 200, 1,486,252,028 bytes
- Requesters: `assumed-role/mdpf-gold-lambda-role/mdpf-gold-lambda` 1,467 (99.2%); `assumed-role/opal-assets-silver-orion-role/opal-assets-silver-orion` 11; `assumed-role/opal-assets-daily-emitter-role/opal-assets-daily-emitter` 1. Key prefix to the second level: `orion/inflection/` for all. User agent: Boto3 on Linux for all 1,479.
- Event hours (UTC): 10-17 15Z 978 (the two D4 invokes of the CN-s-6 deploy, 489 GETs each), 10-17 16Z 3, 10-17 17Z 1; 10-18 13Z 497 (489 the gold lambda's scheduled fire, 8 the silver orion role).
- Size: mean 1.0 MB; 329 GETs at or above 1 MB; 1 at or above 10 MB (42.5 MB).

## The 06Z-16Z window of 2026-10-18 (the order's window)
497 `orion/` GETs, 529,438,245 bytes (all in 13Z). **The E4 burst did NOT recur.**

## Sum against E4 (order condition 3)
- Bytes seen in the logs: 0.53 GB in today's 06Z..16Z window; 1.64 GB in yesterday's (first read); 1.49 GB in the 24 hours read here.
- Bytes E4 counted: 122.10 GB over 26 hours, 99.4% in 2026-10-16 06Z..16Z, before the logging went live (2026-10-16 18:40Z).
- Two consecutive logged windows (10-17, 10-18) carry 1.64 GB and 0.53 GB against the E4 window's 122 GB. The logs cover none of the burst's window, so the difference is a coverage difference, not a measurement disagreement.

## Verdict
**The reader of the 2026-10-16 burst is still NOT NAMED**, and no requester is inferred. The one daily recurring reader of `orion/` in the logs is the gold lambda role at its scheduled fire (489 GETs, about 0.53 GB per fire).

## Open
Default under the issuer's msg 7670: remove the logging by 2026-10-19T18:39Z. A third window (10-19 06Z..16Z, readable after 16:30Z on 10-19) still fits before that deadline; proposed to the issuer.
