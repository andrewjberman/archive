# COMM_ASSIST round 19 -- the issuer's rulings on what surfaced (2.0.0_SA_COO~CA, laptop, 2026-10-15)

Each ruling cites the commit or read that carries it. A worker row is the worker's: the issuer rules inside its own decomposition and the CVO grades at the compile.

## Rows from the round's workers

| row | what | ruling | carried by |
|---|---|---|---|
| W27-S1 | `test_inbound_mail_draft.py` already failed its `client_no_request` arm at the base (11 of 12); the CA-k-1 order said only `test_inbound_mail.py` fails at the base | INERT, and the ISSUER's order-text defect (the issuer measured `test_inbound_mail.py` and not the sibling). CA-k-3 repaired the arm; the file now reads 17 of 17 | CA-k-3 `8454482177`, merged `93a3f55d25` |
| W28-S1 | the commit naming gate refused the hand-typed `transcripts` path in the gate script; no registry row gives a Terraform path, so the script's `--tf` became REQUIRED (the order wrote it optional) | INERT: `safe-apply.sh` always passes `--tf`, the issuer's check pins that call and reads 13 of 13; a default path would be a typed name the gate rightly refuses | CA-k-2 `935a400f14`, merged `d128627a96` |
| W28-S2 | the worker's commit carries the Haiku attribution, not the order's Sonnet line | INERT: the order text said Sonnet 5.5; the attribution rule in force names the model that wrote the commit | worker's report |
| W28-S3 | a refused `safe-commit` left `safe-apply.sh` staged | INERT: the worker re-committed and the final diff is the one inserted block (56 lines, no removed line), read by the issuer | worker's report |
| W29-S1 | naming the source in the scan log line took a `scan_table` signature change and two call sites, not two text lines | INERT: behaviour unchanged (`refresh_same` and `K2-READER` 7 of 7 read it) | CA-k-3 `8454482177` |
| W29-S2 (ARMED, owner `0.0.0_AB_MSTR`) | the commit gate's client-data check reported the hashed account-id list absent, so the CA-k-3 commits were not checked for client account ids | the same condition as `COMM_ASSIST-W21-S1`, which the CTO's round-18 analysis ADDENDUM 1 (`16e5520ca8`) closed AS BY DESIGN on Andrew's 2026-10-09 word (the check stays WARN-only; the list is deliberately not built). Not a hazard of this round; the issuer measured the CA-k-3 diff by hand: tests and two reader text lines, no client identifier. Named for the CVO's compile so the row closes with W21-S1 | this file |

## Defects of the issuer's own this round

1. The CA-k-1 order text said only `test_inbound_mail.py` fails at the base; `test_inbound_mail_draft.py` failed one arm too (W27-S1). Cost: none (INERT, repaired in CA-k-3). Remedy: the issuer runs every test file an order names against the base, not only the one it expects to fail.
2. The three round-19 issuer checks were first committed with lint errors the commit gate found (unused variables, an ambiguous name); fixed and re-measured at the base before the issuance. Cost: one refused commit.
3. The first CA-k-3 worktree failed on a full disk (`No space left on device` at 2.3 GB free): the issuer force-removed the merged worktrees per the standing rule and re-created it. The disk (`C:` at 97 to 98 percent used) is the box manager's; the CA-k-4 order carries a 5 GB free-space precondition.
4. Both first worker sessions (~27, ~28) ended on an API monthly spend limit (HTTP 429). Close-out sessions continued each lane; the issuer measured each worktree before respawning and re-ran every criterion on the merged trunk.
