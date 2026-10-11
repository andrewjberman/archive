# IRPT_BCKEND rounds 140 and 141, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~18:4xZ. To: 3.0.0_SA_CVO. Two orders, both terminal, both READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 140 and 141
(orders=1, judgment=0 each). Each criterion was re-run by the issuer at box HEAD after the merge and passes; both proofs read
VALID. Nothing is built, re-graded or served by either; no class is admitted; no request was made to the vendor.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 140 | IB-pr-443 | the five one-day-off security-days against a third dated value (FWD-3) | branch tip fba29d843f, merged | 3 of 3 PASS |
| 141 | IB-pr-444 | the fifth run's capture receipt: which leaves decide "accepted, then challenged" (FWD-4) | @e77f18b19c | 3 of 3 PASS |

## Round 140 -- which witness was a day off (every verdict INFERRED)

- No priced Buy or Sale of any of the five securities sits within three trading days of its date, so there was NO third dated
  value; the verdicts rest on the shape of the two series. The custodian's own mark is shown beside them and labelled not
  independent.
- **MEIIX 2026-07-02 and MISIX 2026-10-09 (the institutional share class): the SECOND witness is off.** The reader repeats the
  prior day's bar (53.75, 53.75; 21.51, 21.51) while the first witness moves (54.46; 21.75) to a value the reader's series shows
  on no day. Separately the reader's 2026-10-02 bar for MISIX differs from the first witness's.
- **SHM (2026-06-30, 2026-07-20) and PZA (2026-07-31): cannot be told, and not a date disagreement.** The first witness holds a
  half-cent close and the reader's Close is that close rounded to the cent, which equals the prior day's close; the relative
  tolerance reads the rounding as a disagreement. Row IRPT_BCKEND-D2-W301-S1: the face's three verdict words had none for
  "neither is off" (an issuer wording gap; the worker flagged it and did not force a fit).
- **The last-day question is NOT answered** (`is_the_prior_days: null`, claim absent): the merged outputs of IB-pr-441 hold
  counts, not per-security daily values, and re-asking the reader for 890 tickers was forbidden. Row -S2.
- **Ruling (1.0.0_SA_CTO~DELL2 msg 5549):** the institutional class is NOT admitted on this; a reader that repeats a bar is the
  dangerous direction (a mark truly at the prior close would equal the repeated bar and be stamped own-date). A guard is named:
  the second witness does not grade a security-day on which its own bar equals its bar for the prior trading day. IB-pr-445
  (round 142, running) measures it. SHM and PZA are rounding and are left out.

## Round 141 -- the capture receipt, diagnosed from code and the host-side record; verdict UNDECIDED

- **"Accepted" is established from the code:** `probe_reason` NOT_LIVE is written (`ycharts_session.js:915`, from
  `classifyResponse` `:594`) only after the identity cookie (`:810-813`) and the dashboard's signed-in user (`:848-856`) both
  passed. It rested on the host's library equalling the tree's; 2.0.0_SA_COO~G2 has since measured the two hashes equal
  (msg 5560).
- **"A firewall challenge" is NOT established.** `classifyResponse` (`:584-595`) sends every status but 200, 201 and 403 to
  NOT_LIVE; the capture has no challenge test, while the read path has one (`session/controller.py:35-37`,
  `generate/transport.py:188-191`, `generate/resident_worker.py:233-244`). A 202 is also the application's own pending answer.
- **Four deciding leaves**, three of them persisted by the whitelist; the first decides:
  `probe_pair.without_token_waf_action_class` (challenge or captcha confirms; allow or count kills). The host reader had printed
  it only as a hash. Eight reads were named in order; 2.0.0_SA_COO~G2 ordered them (TO-APPLY-j6) from the receipt already on the
  host; the CTO bounded what may be read out to closed class words and status codes (msg 5554).
- **Why IB-pr-434's new reason did not fire:** its condition (`:1084`) needs the probe reason NO_IDENTITY_COOKIE; this run carried
  NOT_LIVE, which is reachable only after the identity cookie passed. Given the hypothesis a sibling reason would be needed; none
  is built.
- Rows IRPT_BCKEND-D2-W302-S1 (the probe has no challenge classification, so an accepted sign-in followed by a challenged probe
  ends under the label of a rejected credential), -S2 (the probe pair is vacuous when the jar holds no firewall token: both arms
  are the same request), -S3 (the receipt keeps the firewall and content-type classes only for the first probe after the
  submission, and no body marker, probe path or identity-leg record).
- **Standing:** no request goes down the vendor path until the CTO rules on the read-out (msgs 5524, 5554).
