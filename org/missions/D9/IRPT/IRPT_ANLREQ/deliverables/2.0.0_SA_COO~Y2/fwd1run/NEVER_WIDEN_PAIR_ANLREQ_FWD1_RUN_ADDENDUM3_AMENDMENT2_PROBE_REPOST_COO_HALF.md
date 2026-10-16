# IRPT_ANLREQ FWD-1 run, ADDENDUM 3 AMENDMENT 2 -- the probe's rule "each candidate once" reads RESOLVING on a fresh upload token, so the probe may re-post the SAME upload once -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No run-3 order is started until the CTO half of THIS amendment is signed on this file's blob (it rides with addendum 3, blob `64884b3338965c79a962c3f40cdb5cde44ad5811`, and amendment 1, blob `7a4e8735155f871b8f8573d0d4d0f3cc63704bec`).**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: addendum 3 section 3 (W8), the sentence "Probes, each ONCE ... The probe never sends a correction, never calls the analysis route, never posts a second time for one candidate." and nothing else.

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); INFERRED = said so.

## 1. What the record shows (RECORD)

The release-33 sitting (AQ2, `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r33/DOOR_TRACE_R33.txt`, AQ2's note "every fresh upload token answers RESOLVING first") sent each upload and read its answer: D1 first answered `RESOLVING` (status 200) at 03:40:43Z and, on a re-post of the same upload 16 s later, `NORMALIZED`; the internal viewer's P2 did the same (`RESOLVING` at 03:42:03Z, `NORMALIZED` 03:42:19Z); P1 and P1M were sent once and ended at `RESOLVING` (their final state was never read). So a single post of a probe candidate's CSV would record `RESOLVING`, not a finding, and the probe would say nothing about whether the candidate is unknown, whether it carries a suggestion, or what its actions are.

## 2. The change (what a person or a system meets)

Addendum 3 section 3 reads: probes "each ONCE, at least 15 s apart ... never posts a second time for one candidate". That rule is amended to exactly this: **for each candidate the applier posts the synthetic CSV once; if and only if the answer is `RESOLVING`, it waits at least 15 s and posts the SAME upload (the same upload token and file) ONCE more and keeps that second answer. At most two posts per candidate, at most ten probe posts in all; a second answer that is again `RESOLVING` is recorded as `RESOLVING` and the candidate does not qualify.** The probe still sends no correction, never calls the analysis route, and posts to the upload route only.
- **What it adds:** at most five more posts of the same synthetic one-row-plus-SPY files to the same route by the same transient internal-viewer identity, inside the same minutes. No new reach, no new principal, no new route.
- **What the door stores (INFERRED, listed by the same before/after rule):** a re-post of an unchanged upload to the same token resolves the state of the first post; an answer that asks for a correction stores nothing; the applier lists the intake store's prefixes before and after the probe and every new object by key and VersionId, none deleted in the window (the CTO's STOP condition, msg 9089, unchanged).

## 3. Limits named

NOT read: whether a RESOLVING first answer for an unknown ticker converts to NEEDS_CORRECTION on the re-post (the R33 record shows the conversion for known-ticker files only); the number of seconds the resolution takes (16 s in the record). If the second answer is still RESOLVING the candidate is recorded as such and the U-row stays UNEXERCISED when no candidate qualifies; no third post is made and no candidate is improvised.

## 4. Owed

The CTO half on this file's blob. The staged run order `IRPT_ANLREQ.TO-RUN-FWD1.fwd1-staff-filing-window3-aq2` (status HELD) already carries this rule in its step 5 and cites this blob; it stays HELD until the R34D install has closed and this amendment is signed.
