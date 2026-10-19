# ADDENDUM 4 to the never-widen packet for the synthetic commentary end-to-end run -- run 4 re-posts with the portal fix's backoff for up to four minutes and deletes nothing until after its last read (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-19. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` and its ADDENDUMS 1 to 3 (ADDENDUM 3: blob `f2baabd809e756324538352641b8ce1530c124da`, CTO half signed msg 10760). **Ledger:** `irpt-commentary-e2e-4-20261019`. **Authority:** CTO msg 10793 ("Write pair ADDENDUM 4: run 4 re-posts with backoff for up to 4 minutes, the same rule as the portal fix you are cutting, and deletes nothing until after its last read").

## 1. Why (IB2 `A_RESOLVE_LIVE.txt` and `A_RESOLVE_LIVE_NOTES.txt`, read by the issuer)

Run 3's five identical posts over 20 s all answered `RESOLVING`, but the door WAS invoked (5 invocations in the 14:30Z bucket: IB2's reading; my earlier "not invoked" was a UTC-4 mislabel, corrected to the CTO). IB2's step 11 deleted run 3's rows at 14:31:39Z, and the resident tried the resolve at 14:32:08Z and refused it `NORMALIZATION_TRANSITION_UNAVAILABLE` because the rows were gone. So run 3 could not show whether a fresh upload resolves: the test's own cleanup raced the resident. The portal has the same shape of limit (five posts over about 15 s) against live resolves of 0 to 13 s and two of 181 s (the issuer's reads of the `NORMALIZATION#` rows); `TO-AR-y-410` (worker 300) replaces it with a backoff.

## 2. The change to the pair (everything else in the packet and ADDENDUMS 1 to 3 stands)

| step | change |
|---|---|
| U | the re-post rule of ADDENDUM 2 (five posts, 3 s apart) is REPLACED by the portal fix's rule: while the answer is `RESOLVING`, re-post the IDENTICAL request (same body, same upload token, same `advisor_email`) after waits of 3, 3, 6, 6, 12, 12, 24, 24 s and then 30 s each, the waits summing to at most 240 s (the last one truncated); stop at the first answer that is not `RESOLVING`. A still-`RESOLVING` answer after the full 240 s is a STOP at U with the elapsed time (measured from the first post to the last answer) and the count of resident-journal `IRPT_RESIDENT_RESOLVE` lines since the first post; IB2 prints the row state of the `NORMALIZATION#` row (state and `dispatched_at` age only) before it stops. The upload token is fresh and the holdings bytes distinct (ADDENDUM 3) |
| P | the poll budget of 30 minutes starts after step S; unchanged |
| D | NOTHING is deleted before the LAST read of the run: step D starts only after (a) step R has run, or (b) the run has stopped at a hop and every read the stop requires has been made (including the journal count and the row state of U's stop, the dead-letter depth after, and the packager line). The resident's resolve of this run's own upload must have been observed (an `IRPT_RESIDENT_RESOLVE state=` line for it) or 5 minutes must have passed since the last post, whichever is first, before the upload's rows or blobs are touched. The receipt line `D` states the UTC time of the first delete and the UTC time of the last read, and the first delete must be later |

## 3. Blast radius delta

None: the same one upload re-posted for longer (a re-post of a `RESOLVING` row answers `RESOLVING` and creates no second object, `intake/uploads.py:526-533`; a redrive occurs only at or after `REDRIVE_SECONDS`, 960 s, which a 240 s wait never reaches), and the synthetic objects live a few minutes longer. The generation queue may hold this run's resolve message until the resident handles it.

## 4. Not claimed

- That the resident resolves a fresh upload within 240 s (the stop rule says what happens if not).
- That the staff user can read the commentary route for the advisor-owned request (ADDENDUM 1 section 4).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-19, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 to 3. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
