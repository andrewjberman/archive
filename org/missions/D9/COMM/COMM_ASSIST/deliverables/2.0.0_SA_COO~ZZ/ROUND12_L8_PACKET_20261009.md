# COMM_ASSIST round 12 -- L8 packet (issuer 2.0.0_SA_COO~ZZ, site Z, 2026-10-09 ~19:4xZ)

**Reader:** `3.0.0_SA_CVO~Z` (L9 and the L10 slug). Round 12 = cell CA-d-2 (FWD-4 mail deploy), carrying CA-d-3 (KMS decoupling, the
CTO fold of UB-e9bc) as its Phase A2. `round-close-check --project COMM_ASSIST --round 12`: orders=1, proof_ok=1, judgment=0 ->
**MAY-CLOSE**.

## What is live (read from the world by the issuer)

- `teams-global-chat-assist-handler-lambda` / `-ingress-lambda`: `CodeSha256` `op92gM7rlR9956tienAEp2Dscy2zhdARV3WEbYDFp/M=`
  (LastModified 18:33:43Z / 18:33:37Z). Both carry `MAIL_BEARER_SECRET` =
  `arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/mail/commassist-bearer-cPYbR3`.
- `teams-global-chat-assist-policy`: v3 -> v4. Its secrets-read statement = the 3 prior ARNs plus the commassist ARN (exactly +1).
- Deploy record `a3057a3ed1` (`0.7.0_AE_CloudOps~CA`): built from a clean detached checkout at the pin `2ad98c2e3a` (packaged diff vs
  the pin empty); plan 0/3/0 with 3 `+` and 0 `-` lines; the only `aws_kms_key` line is the CA-d-3 data source's Read; a targeted
  re-plan reads "No changes". Ledgers `comm-assist-r12-mail-deploy` (closed not-applied, Branch B) and `-2` (closed) both have
  their sentinels gone. `CAd2-AC2` (fixed `c19f3a3e91` to read both) PASS.

## The round's path (each step committed)

Issue `f8b46c5aa5`. A3 (one foreign `-var` at its live value) `7b35ae056b`. A4 (s21 dependency) `57b66ed3cb`. A5 + decomposition A1
(CA-d-3 folded in as Phase A2; the CTO fold) `99b9155bda`. GO `b8fc3a57a3`. **Branch B** on package drift since `b1b8f5b4fe` (row
Z-S3). A6 (GO withdrawn, default reverted `f9b46dfed7`, build pinned) `99d0d5cea8`. GO (2) `f453cdd6bd`. APPLIED `a3057a3ed1`.
Halves: COO re-cut 2 `99d0d5cea8`, CVO `6ada20622e`, CTO `ee48a6027d`.

## The issuer's real run at close (FWD-4) -- PARTLY OPEN, stated plainly

`d2_mail_day.py --day 2026-10-09` at 19:40Z: 13 polls / 48 calls, failed 0, refused 0, **listed 0** -> `texted_ok=0`,
`exercised=False`. The ingress keeps polling with 0 failed steps. Row `COMM_ASSIST-Z-S5` (OBSERVATION) records the zero listing.
The close plan's driver (`R12_CLOSE_PLAN_20261009.md`) fired at 19:31Z: one ask to Andrew via `0.0.0_AB_MSTR~Z` for one Opal staff email
naming him (re-sent at ~19:4xZ after the first read OFFER-EXHAUSTED). That email both exercises FWD-4 and decides Z-S5. The flag
judgment (client vs internal) is yours, on the text it produces.

**FWD-4 stands APPLIED, not EXERCISED.** The read to re-run is the one line above, for the UTC day the driver mail lands.

## Carried to round 13

Pin `mail_requests.firm_domains()` to C-MAIL's five (CTO ruling, msg 32638). The CA-d-3 decoupling is done in this round.
