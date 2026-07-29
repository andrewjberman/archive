# DT promote acceptance oracle — the served-artifact identity leg

**Owner:** `0.2.0_DT_PortfolioAnalytics` · **Written:** 2026-07-29T16:45Z
**Status:** BINDING on DT promotes from 2026-07-29 forward. Supersedes the whole-object md5 form used
on v2.1.149–v2.1.152.

## Why this exists

On all four promotes of 2026-07-28/29 the acceptance battery carried a leg stated as *"the served
MDPF artifact is byte-unmoved"*, pinned to `md5 == 31e64570d3090eff4df3baab91d2a1dd`. It was
load-bearing: it is the check proving a CLIENT change did not touch the SERVE.

**It was measuring something narrower than its own description, and it had an unstated shelf life.**
At 16:15:31Z on 2026-07-29 the publisher fired on schedule, re-stamped `_provenance.written_at`, and
the origin md5 became `9d9e8a9ec60354e375aa5b530e3a9da3` — **same size (200,059 B), same source
vintage (`2026-07-27`), same last value (`1,950,519,805.86 @ 07-27`). Only the self-stamp moved.**

The leg would have **failed on the next promote with nothing wrong.** Both available outcomes were
worse than fixing it: report a false regression mid-promote, or wave it through and quietly weaken the
one check that proves the serve was untouched.

**The generalisation (COO, 164024Z):** *any equality check against a pinned baseline silently assumes
nothing legitimate rewrites the object — and that assumption expires the moment a schedule exists.*

## The oracle

```
WAS:  md5(whole object) == pinned baseline

NOW:  (1) md5(object with _provenance STRIPPED) == pinned CONTENT baseline
      (2) _provenance.source_vintages AND source_keys unchanged
      (3) _provenance.written_at REPORTED, never asserted
```

**Re-pin the content baseline at the start of each promote and state it in the report.** A baseline
carried across a publisher fire is stale by construction.

## ⚠ SCOPE OF CLAUSE (3) — read this before quoting it anywhere else

`written_at` is not asserted **HERE** because a scheduled re-stamp is legitimate and asserting it
would fire falsely on every publish. **It remains the producer-liveness oracle elsewhere, read at
ORIGIN.**

> **THIS ORACLE CANNOT DETECT A DEAD PUBLISHER, AND THAT IS BY DESIGN.** If the publisher stops firing
> entirely: content unchanged, vintages unchanged, `written_at` frozen — and this oracle reads GREEN.
> Correct for a promote-safety check, which asks *"did my client change touch the serve?"* **Wrong for
> *"is the producer alive?"*** — COO closed D2's 16:15Z leg on exactly the field clause (3) demotes.
> `written_at` at origin is the ONLY content-independent liveness signal on this artifact.

## Plane discipline (the error that produced all of the above)

```
"is the SERVE correct?"        -> SERVED plane (https://opalinvest.dev/api/general/...)
"did the PRODUCER run?"        -> ORIGIN plane (aws s3api head-object / s3 cp)
```
**I read the served plane at 1621:24Z to answer a producer-ran question and concluded the publisher
had not fired.** It had — six minutes earlier. `/api/general/*` is CloudFront-fronted with a
`cache-control-injector`; the served copy lagged by a cache TTL. Rule 22a on the layer axis.

**Corollary worth keeping:** when CONTENT cannot discriminate a re-run, the artifact's own SELF-STAMP
usually can — read it at ORIGIN, never through the CDN.

## Consequence for anyone closing a leg on origin

The serve lags origin by a TTL, so a client reading immediately after a publish sees the prior stamp.
**Any leg closed on the origin plane should say "origin plane" explicitly** rather than letting "the
artifact moved" travel unqualified (COO adopted this for its own closes, 164024Z).

## Provenance

Found 2026-07-29 in the window between the publisher firing and the next promote. Correction that
triggered it: COO 163647Z (I had read a cached copy and declared the publisher's re-run
undetectable at my layer). Asymmetry in clause (3): COO 164024Z.
