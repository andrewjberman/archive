# NFRA_TRNSPT round 5 -- close record (2.0.0_SA_COO~T2, dell2, 2026-10-08)

Issuance `904370fa25` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R5.md`, CTO round-4 analysis @856673477a). Orders 2 of 2
complete; `round-close-check.py --round 5`: `verdict=MAY-CLOSE` (proofs 2 of 2 OK, 0 judgment criteria).

| cell | order | merge | criteria |
|---|---|---|---|
| TR-a-5 (E1) | NFRA_TRNSPT.TO-TR-a5 | `426f5751e9` | AC1 R5-A5-FILE-OK rows=4 first=monday_meeting; AC2 R5-A5-TEST-OK passed=5 |
| TR-c-5 (E2) | NFRA_TRNSPT.TO-TR-c5 | `f1e2990e05` | AC1 R5-C5-RECORD-OK deployed=aa75078e1b verdict=SAME-AS-HEAD; AC2 R5-C5-CENSUS-OK passed=4 |

Drain checks on the merged tree: the three transcripts mail/allowlist test files 39 passed; `commit-gate.sh` clean on both new modules.

## E1 -- the meeting allowlist (FWD-1, FWD-2)

- One real run: `meeting_allowlist.load()` -> 4 rows, first `monday_meeting`; `as_env_value()` -> 4 space-separated ids (595 chars).
- Criterion (3), the handoff: msg **1356** to `0.0.0_AB_MSTR~DELL2` (2026-10-08T17:54:48Z; SENT at the close read), asking the relay to the
  NFRA_OPLGTW gateway owner. Loading `TRANSCRIPT_MEETING_ALLOWLIST` is the owner's act; until then `/hx/transcripts` stays 403
  `meeting_not_allowed` and FWD-1's hop 2 is open.

## E2 -- D2-S2, truncation or classification (FWD-7 residue)

- Criterion (1): the deployed `mail_route.py` is SAME-AS-HEAD, resolved by CONTENT from the release artifact
  (`org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R5_DEPLOYED_ARTIFACT_READ.md`); the manifest's `aa75078e1b` is a never-merged
  local release branch (row NFRA_TRNSPT-D2-W2-S1; amendment `14289f79b2`). The Lambda's build-input `gateway_mail.py` is SAME as source.
- Criterion (2), the one live counts-only listing, by the issuer from dell2, over the 2026-10-07T23:30:13Z fire's own 60-day window with
  the pull's own sender table: `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R5_E2_LIVE_CENSUS.json`.
  - total listed 100 = sender#1 13 + sender#2 87.
  - sender#1: 2 spans, 1 page each (5, 8), no continuation token.
  - sender#2: 2 spans, 2 pages each (25+19, 25+18); a token on page 1 of each span, none on the last page.
  - **VERDICT: NOT truncation.** Every span paged to its end; `100 = 4 x 25` was a coincidence (13 + 87). The 2026-08-11 message was
    either outside the has-attachment listing for the table senders or listed and classified out. D2-S2 moves to classification;
    the next read is the fire's own run record for that message's admission flags (store read, laptop fenced path).
- The listing ran TWICE: the first run's output write failed on a path error and its result was not kept; the second, identical, is the
  recorded one. Both were GET-only reads on the gateway's listing route.
- First read of a credential by a Dell seat: secret `gateway/mail/bearer`, by name, read in-process only, at the two census runs
  (second run at 2026-10-08T18:06:07Z, the first minutes before). Reported to the laptop through `0.0.0_AB_MSTR~DELL2` per CTO relay msg 1232 rule (2).

## Drain incidents (recorded, repaired)

- Slot ~2 was re-seated twice (a finished worker cannot be resumed). The second seat rewrote `PENDING-THIS-COMMIT` pins in the closed
  TR-r4 and TR-t5 instances to a false hash; restored to base bytes by the third seat at `b751542ad6` before the merge.
