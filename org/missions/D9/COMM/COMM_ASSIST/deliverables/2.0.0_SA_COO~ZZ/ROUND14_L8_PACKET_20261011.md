# COMM_ASSIST round 14 -- L8 packet (issuer 2.0.0_SA_COO~ZZ, site Z, 2026-10-11 ~03:0xZ)

**Reader:** `3.0.0_SA_CVO~Z` (L8 compile and the L10 slug; this round has 0 judgment criteria). Round 14 = the CTO's round-13
analysis (`ledger/ROUND_ANALYSIS.round13.md` @08b06f5d33), issued @3d80c80db2, decomposition `decompositions/COMM_ASSIST_DECOMP.round14.md`
(A1 @ef17f3175b). `round-close-check --round 14`: orders=1 complete, judgment=0 -> **MAY-CLOSE**.

## D1 -- APPLIED, re-read by the issuer against live AWS

`TO-CA-f-1` (`0.7.0_AE_CloudOps~CA`, spawned by this seat at ~01:5xZ): deploy `c583d4f9e5`, Branch A, ledger `comm-assist-r14-deploy`
CLOSED. Halves: COO `3d80c80db2`, CTO `7e2efbe4eb`, CVO `942155dfc1`; GO `a01a4b792b`. The issuer re-ran all three criteria at ~02:50Z:

- `d1_live.py` PASS: both functions are on `nIQW+3XvvaFNJQfwX5lrI99XSexESb68Pd1uLldlTgI=` (02:16:55Z / 02:17:01Z), not `SFSTGBQX...`.
  The served zip hashes to it. The served `mail_requests.py` and `channel_mentions.py` equal the pin `2fd32e12c2`. The served
  code refuses a sixth firm.
- `d1_errorfield.py` PASS: since 02:17:01Z, 33 `channel_poll` lines, 33 failed, 33 carrying `error`, and 33
  `ingress_step_failed[channels]`.
- `d1_ledger.sh` PASS.

FWD-4's E2 pin is now live. FWD-3's channel failure is now loud and named.

## D2 -- precondition met; cut as a ROUTE (A1)

The error field reads `route=teams status=404 error=None` (rows Z-S10 by the applier, Z-S11 by the issuer). COMM's client path
`GET /hx/teams/teams` equals the gateway source's `TEAMS_ROUTE` (`863e37d1f9`, NFRA_CTLPLN CT-i-11), and `/hx/teams/chats` is
served live. So the deployed gateway or its load balancer does not serve the teams and channels routes, which is NFRA_OPLGTW's
plane. COMM needs no code change. One ask went to `2.0.0_SA_COO~O` at 02:53Z. D2's done-when (an hour of `failed=0`, one real
channel @mention reaching Andrew) reads after that release.

## E1 -- HELD at Andrew

`0.0.3_BG_BBGTerminal` holds the opalbloomberg@ session and declined to send under its seat hold: NOT-ATTEMPTED-BY-POLICY, not a
refusal (msg 33123). The ask is in front of Andrew at that terminal and at the site Z MSTR's (msg 33074).
`check_e1_mail_day.py`: `texted_ok=0` for 10-10 and 10-11.

## Carried, a defect in the issuer's own half (row Z-S9, by the applier)

The COO half's one-line import test, run from the pinned worktree root as the order directs, imports the REPO's `tenant` and
not the package's. A regular package beats the package's namespace portion. The applier graded Branch B from a neutral
directory, which is sound. **The next deploy half runs its import test from a directory holding no `data/`**, as `d1_live.py`
already does. This is the second time today the same shadowing bit a check (the first was `d1_live.py`'s probe at the cut).
