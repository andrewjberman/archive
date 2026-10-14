# COMM_ASSIST round 18 -- the issuer's rulings on what surfaced (2.0.0_SA_COO~CA, laptop, 2026-10-14)

Each ruling cites the commit or read that carries it. A worker row is the worker's: the issuer rules inside its own decomposition and the CVO grades at the compile.

## The ARMED row this round closes

- **`COMM_ASSIST-W10-S2` (a forged `sms.reply` put on the queue is acted on as Andrew's text): DISARMED by evidence, R-12.** The mark is live and enforcing (CA-j-5 applied 15:07:01Z, ledger `comm-assist-r18-enforce-deploy` CLOSED @4dddae3aad). The disarm condition the CTO set is read twice, both by the issuer: (a) `check_j5_forged.py` put ONE unmarked `sms.reply` on a dummy `probe:ca-j-5-forged-20261014T150942Z` object: refused and recorded (`no-mark`, kind `sms.reply`, `unmarked_seen` 1, no other state key, no `tenant` result, no text sent); (b) Andrew's real tagged reply at 15:32:43Z was accepted under `enforce` and acted on (marks accepted 8 to 9, 0 unmarked, 0 refusals). The key that mints a mark is readable only by the assistant's execution role (CA-j-8: the Dell users read `explicitDeny`, simulated against the LIVE policy). The residual stands in PRD v0.8: an administrator can rewrite the key's policy and then read the key, a recorded management write. The row's channel closure is the CVO's at the compile.

## Worker and seat rows, with the ruling

| row | what | ruling | carried by |
|---|---|---|---|
| W19-S1 | the order placed two handler re-sends in `on_owner_text`; one is there and the other is in `on_owner_reply` | INERT; all four producer sites are stamped (`check_j1_mark`, read by AST) | `0ca94ce0b6` |
| W19-S2 (BLOCKING) | `test_teams_chat_natural.py` compared the handler's re-sends as exact payloads and was outside the grant | RESOLVED: the file joined the order's paths (AMENDMENT 1, `53be82a3cd`), updated in `b1b0e1c6a0`; the whole flow set 544 of 544 | `0ca94ce0b6` |
| W19-S3 | a mode value other than off, record or enforce raises for a text-driven event | INERT and kept: a typo fails loud and does not act (the served-code probe asserts it) | `check_j3_live` |
| W19-S4 | the flow-test harness seeds the secret cache because a patch of `a.secret` inside it was overwritten by the check's own | INERT | worker's report |
| W19-S5, W19-S6 | the natural test fails alone from the repo root (a bare sibling import, pre-existing); `CAj1-AC2`'s command runs only the tenant file | INERT; the whole set was run and read | worker's report |
| W20-S1 | `forward()` with `parents=True` also creates an absent reader root when called directly | INERT: the CLI refuses a missing `--root` first and `forward()` has one caller in its file | `0f09e35281` |
| W21-S1 (ARMED, owner UNMEASURED) | the commit gate's client-data check could not run: the hashed account-id list is absent on this box | the issuer measured the CA-j-2 commits by hand (130 added lines, the one 12-digit number is Opal's own account); the box-level absence is pre-existing and affects EVERY commit from this box, so it stands with the box manager, named for the CVO and CTO, never repaired by a seat | this file (the hand measurement was made in-session; the commit that carried the edit is `6cfb79f314`) |
| W23-S1, W23-S2 | an unreadable `at` in a held mark is re-dated to now; a sixth test was added | INERT: failing closed holds the mark longer; the extra test is welcome | `afa8752f44` |
| W24-S1, W24-S2, W24-S3 | `test_inbound_mail_draft.py` fails one arm at the base (a stale assertion about the tail of the text, 6 of 7); `test_inbound_mail.py` is 11 of 15 at the base; pytest does not collect those plain scripts | INERT, each verified by running both scripts on the trunk BEFORE the change; carried to a named repair cell CA-j-18 (stale mail test assertions, LOCAL), not cut | `ca76b8b225` |
| W25-S1 (BLOCKING) | `check_h1_failure_shape` required exactly four sources, contradicting the CA-j-13 contract | RESOLVED, and the defect was the ISSUER's: the order said the existing reader controls pass against the patched reader, and the issuer's own test ran the check by absolute path (it imports the trunk's reader), so it tested the unpatched reader. The check was amended (`628f55311d`) and proved against the worker's reader | `0ea947e32d` |
| W25-S2, W25-S3 | a null or unparsable timestamp is kept with a null age; the CLI help text says "the four files" and every scan logs "READ drafts" | INERT, cosmetic, kept | `0ea947e32d` |
| W26-S1 | the one-line commit exceeded the tool's time bound and ran in the background | INERT | worker's report |
| the seats' rows (CloudOps, five deploys) | none filed | | |

## Defects of the issuer's own this round (so the CVO sees them in one place)

1. The H1 check test by absolute path (above). Cost: one blocked worker and one respawn. Remedy: any issuer check that imports repository code is run from the worktree under test, by relative path, before the order says a control "passes against the patched file".
2. My first CA-j-17 pin was built on a trunk that already carried another project's registry file, so its package would have differed from the live one; the pin was rebuilt on the live pin and measured equal byte for byte. Cost: none in AWS.
3. My phrase "one multi-reply text" for the 13:01Z evidence was imprecise (it was one text routed as `natural`, plus the handler's seven re-sends); the half was refined before the CVO signed (`32eeb51891`).
4. Two ack slips, no effect (message 109098 acked in error before 109101).
