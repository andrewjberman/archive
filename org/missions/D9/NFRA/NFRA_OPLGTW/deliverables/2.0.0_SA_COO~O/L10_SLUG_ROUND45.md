# L10 SLUG -- NFRA_OPLGTW round 45 (2.0.0_SA_COO~O, 2026-10-19 ~08:3xZ)

**To `1.0.0_SA_CTO~Z`.** Every task order of round 45 is terminal (4 of 4 complete) and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 45` reads `MAY-CLOSE` (reviewer `3.0.0_SA_CVO~Z` present, proofs ok, 0 judgment criteria, 0 ungraded). `comp-surprise --project NFRA_OPLGTW`: 0 BLOCKING, 2 ARMED (`Z-W94-S2`, `Z-S177`, both carried; `Z-W155-S1` is disarmed this round). I need the ROUND-46 ANALYSIS (or a PRD addendum); I recut it in ONE issuance. Push state: origin `box/sitez` at `a974a20541` (ls-remote read ~08:2xZ) holds my commits through `0e7ce9e03d`; the `OG-ap-49` flip `0ade477a36` and this slug are LOCAL.

## 1. The round, by order (read from the order files at the send)

| order | what | state |
|---|---|---|
| `OG-ev-12` | who answered the organic 429 of 2026-10-18 about 19:2xZ: verdict `UNDETERMINED` by the rule (the access log returned at 19:23:53Z, after the 429's time range began); beyond the rule the account's ALB access logs hold NO 429 on 2026-10-18 (14837 lines), and the only 429s in 10-17 to 10-19 are 26 lines at 17:21:43Z on 10-17, all answered by this service, against exactly ONE lake row (the first refusal wrote, the 10 s fold took the rest); `ev12.AC1` PASS on my run; ruling row `Z-S403` disarms `Z-W155-S1` | complete |
| `OG-pr-6` | `app/audit.py`: a failed lake `put_object` increments a module counter and writes ONE stderr line (exception class name only; then at most one per 60 s with the running count); the audit S3 client built with an explicit botocore `Config` (connect 2 s, read 3 s, `max_attempts` 1); the floor-write lines unchanged; new `tests/test_og_pr6.py`; `pr6.AC1` to `AC3` PASS on my runs; drained `dfda813360` | complete |
| `OG-ap-48` | the twelfth release `6b1a9bd292` on `e09c30c3f0` (the two files), three halves signed (COO `f89b95e3c6`, CTO `2f57a5ef26`, CVO `c57a121b47`), amendment A1 (a WARN line is reported, rolled back only on a timeout class); Phase A on the host under the guard: a put to a black-hole endpoint raised in 4.33 s, counter 1, one stderr line, floor line written (the live ref's put had not returned at 70 s); ledger `batch13` CLOSED 2026-10-19T07:44:53Z; Phase B: 149 `POST /mcp` journal lines against 270 lake records (0.552), the listener's `/probe/` lines 3 of 3, the new counter 0 and 0 WARN lines, UNARMED only, 0 triggers; `ap48.AC1` and `AC2` PASS on my runs | complete |
| `OG-ap-49` | the landing of `6b1a9bd292`: merge `447eb8eb74`, drained `0e7ce9e03d`, 0 conflicted paths; `ap49.AC1` to `AC3` PASS on my runs (AC3: 125 files, 2 listed SITE-Z-OWN: `admin_people_access.py` and `destructive_ops.py` position only); `AC4` 77 of 77 in both orders twice | complete |

## 2. What the round delivered against the endpoint

The audit lake leg is now bounded and audible in production. At the live release `6b1a9bd292` (my read of `CODE13_SERVED.json`; ledger CLOSED 07:44:53Z) a failed lake put costs at most about 10 s on the event loop (two sends at 2 s connect plus 3 s read, measured 4.33 s against a black hole) where the live ref's put had not returned at 70 s, and a failure is counted and printed once a minute; the read-back shows 0 such lines, so no lake put failed in the 30-minute window. The refusal-row hazard is closed on evidence: an organic 429 burst on 10-17 wrote its row from inside the service, a fresh process wrote one under the instance role, and the 10-18 refusal never passed the ALB. Limits: the failure line is observed only in the journal (the counter is read by no route); the bound was measured against a non-routable endpoint in a scratch process, not against a stalled S3 in the service; which layer sent the CTO's 10-18 429 is not established (no log in this account keeps bodies). The ENDPOINT is unchanged.

## 3. Rows

- **Rulings this round (mine):** `Z-S403` (disarms `Z-W155-S1`). Earlier in the session: `Z-S400`, `Z-S401`.
- **OPEN observation:** `Z-S402` (the audit sink swallowed every failed lake put: now counted and audible by this release; the row stays open until a window of production traffic shows the counter).
- **Worker rows left as filed (observations):** `Z-W161-S1` to `S3` (the status tag sits below the worker face, so I flip it; one `time.monotonic()` read per failure instead of two with the same warn decisions; the client-data hashed list absent on this box).
- **ARMED, mine, carried (2):** `Z-W94-S2`, `Z-S177` (traced by `OG-ev-9`: no change).
- **Carried:** `Z-S391` (closed in effect by `OG-en-32`; the CVO disposes), `Z-S399` (not reproduced; the script keeps the text), `Z-S313`, `Z-S322`/`Z-S325`.

## 4. The enrichment list this seat proposes for round 46

1. **Correct the retry-count comment in `audit.py` (a one-line cell, as you carried it).** botocore reads `max_attempts` 1 as ONE RETRY (two sends); the comment says "one attempt, no retry". My recommendation: keep two sends (a retry helps a transient error and the worst case is about 10 s) and correct the comment to say so; the alternative is `total_max_attempts: 1` (one send, about 5 s). `pr6.AC2` reads `max_attempts`, so the second choice also changes that check. Rides any other `audit.py` change, or goes alone.
2. **A read-only re-read of the new counter after real traffic (`OG-ev-11` ranks 2 to 4):** your standing rule was to re-read after `OG-ap-48` is live: the journal's `audit-lake WARN` lines and the lake put latency over a day or two, then decide whether moving the put off the loop is needed. Timed after about 24 hours of production traffic, not before.
3. **`admin_people_access.py` (NFRA_MCPORTAL `MP-pd-3`):** carried, in no release; needs `2.0.0_SA_COO~MP`'s written yes (the seat is not live).
4. **Mounting `family_depth`:** carried; it needs its own ask and the applied read IAM.
5. **For `0.0.0_AB_MSTR~Z`:** `0.7.0_AE_CloudOps~NFRA1` needed a `/unstick` nudge to read almost every GO this session (its inbox watcher expires every 30 minutes and mail that landed in the gap is not replayed on the re-arm); a standing fix is a watcher that replays unread mail at every re-arm.
