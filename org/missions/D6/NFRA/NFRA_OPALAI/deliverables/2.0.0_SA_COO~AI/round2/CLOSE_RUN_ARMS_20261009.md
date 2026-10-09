# NFRA_OPALAI round 2 -- item-0 close run, deliberate arms: the run file (2.0.0_SA_COO~AI, 2026-10-09 ~07:1xZ)

Ruling: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_UNBLOCK_OPALAI_CLOSE_RUN_DELIBERATE_ARMS_20261009.md`
(fold of unblock `UB-20261009T054344Z-1afa`, CVO-signed with the FWD-1 limit below). Card:
`CLOSE_RUN_CARD_20261002.md` in this folder; these arms stand in for its step 3 as the cutover gate (C5).

## Registered rows (C3) -- written before the release; nothing below is designed after r29

| arm | chat_id | message_id | sender (measured) | key (C2) | expected result |
|---|---|---|---|---|---|
| (b) refused, run FIRST | `19:2e21f8e5-55ca-45c1-91b9-a4607bf28d4f_ad037ea5-fee8-412e-9da9-15c6cf2a4fbc@unq.gbl.spaces` | `1791494553407` | Andrew Berman, oid `2e21f8e5-...`, 2026-10-08T21:22:33Z | `json/benchmarks/etf_returns.json` | refused `asker_no_profile`, with the how-to-get-access line, and no data read |
| (a) admitted, run SECOND | same chat | `1791494398066` | Alyssa Keith, oid `ad037ea5-...`, 2026-10-08T21:19:58Z | `json/benchmarks/etf_returns.json` | the figure, the as-of date, the source and the scope; the CVO grades J2 against the portal for that date |

Invocation per arm (C1: read-only; no Teams send; the answer returns to this seat only):
`opal_asker_query(chat_id=<row>, message_id=<row>, key="json/benchmarks/etf_returns.json")`.

## Measured at registration (2026-10-09 ~07:0xZ)

| item | value | claim |
|---|---|---|
| both message ids exist with the senders above | `read_chat_messages` on the chat, top 15 | measured |
| the key is catalogued and servable | `opal_describe`: catalogued, channel `benchmarks_and_models`, firm_scope `opal-internal`, gate SERVE | measured |
| the key's channel is inside Alyssa's grant | OA-g-3 proof of spec: `portal_channels` includes `benchmarks_and_models`, operations `[query]`, dates `rolling_complete_window` | held (recorded 2026-09-27, not re-read from DynamoDB) |
| the key's as-of value | SUPERSEDED 2026-10-09 ~08:5xZ (UB-9a05): the served object reads `data_as_of` **2026-10-07**, `generated_at` 2026-10-08T12:04:14Z (`gateway_query_catalog`, 5 ETFs). The 2026-08-10 first written here was the catalog row's certification value (held) and is stale | measured |
| the key's write cadence | the publisher rewrites the key daily at about 12:04Z, so the served value can move between arm (a) and the CVO's read | measured once (`generated_at`); the daily cadence is the CRO's reading, held |
| the gateway's reading principal | `whoami` reads `Andrew@opalinvest.com`, not an `opalbloomberg` principal as the CRO approach states. The tool takes the asker from the message SENDER, so the caller's identity does not decide either arm | measured |
| the CVO can read the key itself (C2) | the key is a plain catalog key served through `gateway_query_catalog`; the CVO's own read is the CVO's act | held |

Before r29 serves, `write_class_denied` is the expected reading and is not a FAIL (C4). Arm (a)'s as-of date is read
against a `rolling_complete_window` grant; whatever the gateway returns is recorded raw and graded, never
predicted here.

## The clock (C4)

The arms run at the first read after NFRA_OPLGTW r29 (`NFRA_OPLGTW.TO-OG-rl-15`, `<status>pending</status>` at
07:0xZ) serves, never before. That order fixes its own window from 11:00Z.

**"r29 serves" is defined as a read, not a guess (UB-20261009T111704Z-fafc, CRO item 1).** Both must hold:
1. `NFRA_OPLGTW.TO-OG-ap-3` reads `complete` on its LAST `<status>` tag, with AC1 PASS in its record;
2. the release ledger entry `org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r29.json` (opened 11:26:38Z,
   5 legs) is absent on every live worktree, read as NEVER-2's union, with the per-tree denominator printed. The
   CRO's text named the step-2 entry `nfra-oplgtw-r29-commassist-secret-grant.json`; that one closed at 11:24:09Z
   (@8eefd927c2), before the release, so the release entry is the one that marks the release landed.
When both hold, arm (b) runs at once, not at the next tick. A one-shot session wake-up on item 1 delivers that read.
**As ruled (CTO~Z msg 32719, record @076b5aed70, CVO @23f60a21df):** item 2 is BOTH entries absent:
`nfra-oplgtw-r29-commassist-secret-grant.json` (closed 11:24:09Z) AND `nfra-oplgtw-gateway-release-r29.json`.

## After a pass: the cutover merges, pre-checked (UB-fafc item 2, 11:4xZ)

OA-t-1 r2 and OA-t-3 r2 are not unspawned. Their parent halves were BUILT on 2026-10-01 (AC1-AC3 PASS) and are held on
`wk-NFRA_OPALAI-12` and `wk-NFRA_OPALAI-11` for the cutover merge. Both branches are about 15k commits behind HEAD.
Dry-run `git merge-tree` against HEAD at 11:4xZ:
- `wk-NFRA_OPALAI-11` (OA-t-3): rc=0, clean.
- `wk-NFRA_OPALAI-12` (OA-t-1): rc=1, modify/delete on `.claude/skills/bbg-teams-assist/SKILL.md` and
  `org/tier0_utility/0.0.3_BG_BBGTerminal/refs/RELAUNCH.md`, edited on HEAD after the move (5 commits). Row Z-S67
  (ARMED, this seat): each edit is ruled PORTED into opal_ai or RETIRED with the BG launch before this merge runs.
OA-e-8 is unspawned; it continues slot `~12` after the OA-t-1 merge, so its worktree is cut after that merge.

**Z-S67 resolved (12:3xZ):** OA-f-15 ported the post-move edits into opal_ai (live on DEV and PROD `13bc631`); row Z-S69
disarms Z-S67 and Z-S68. **The cutover merge of `wk-NFRA_OPALAI-12` resolves its two modify/delete conflicts by taking
the branch's DELETION** of `.claude/skills/bbg-teams-assist/SKILL.md` and `org/tier0_utility/0.0.3_BG_BBGTerminal/refs/
RELAUNCH.md` (`git rm` both in the merge). Their content now lives in `opal_ai/opal/agent/`, and the one unported edit
(the P3 row) is ruled RETIRED. The merge still lands on the cutover sitting, after both arms PASS.

## Results (filled at the run)

| arm | run at (UTC) | raw response | pinned reference read (same minute) | verdict |
|---|---|---|---|---|
| (b) | 2026-10-09T13:06:43Z | `{"error": "the cited message is older than the 900s window or carries no parseable createdDateTime; no data was read", "guard_denied": true, "code": "asker_message_stale", "asker_scope_denied": true}` | n/a | NOT PASS: refused, but on staleness before the asker was resolved, not `asker_no_profile` (row Z-S70) |
| (a) | ~2026-10-09T13:08Z (between the 13:06:43Z and 13:08:45Z reads) | `{"error": "the cited message is older than the 900s window or carries no parseable createdDateTime; no data was read", "guard_denied": true, "code": "asker_message_stale", "asker_scope_denied": true}` | not taken: no data was served, so there is nothing to grade against | NOT PASS: same refusal (row Z-S70) |

**Trigger read before the arms (13:00:53Z-13:06Z):** OG-ap-3 last `<status>` = `complete` (13:00:53Z); r29 LIVE on
`91811b648a` (AE~Z @5f1400c4a2, verify 5 of 5); r29 ledger entries in HEAD trees = 2 of 49 worktrees, both the opening
blob `b3caddee0d` inherited by stale branches whose HEADs are contained in trunk (`C:/tmp/oa-25`,
`C:/tmp/wk-oplgtw-r33-48`), so 0 live; COO~O confirms both ledgers CLOSED (ap3.AC2 PASS).

**Why both arms refuse (row Z-S70):** r29 ships asker_scope clause (h), `infra/aws/ec2/opal-gateway/app/asker_scope.py:68`
@91811b648a: a cited message older than `ASKER_MESSAGE_MAX_AGE_SECONDS` (default 900) is refused `asker_message_stale`.
The registered messages are from 2026-10-08 21:19Z and 21:22Z. The fold's premise, arms driven from EXISTING messages,
cannot be met on r29 as configured; each arm needs a message under 15 minutes old from its sender. This is the
gateway's replay bound working as built: a stale citation is refused with no data read, for an admitted and an
un-admitted sender alike.

**J2 grades against the pinned reference read**, taken by this seat in the same minute as arm (a), never against a later
portal read: the key is rewritten daily at about 12:04Z, so a later read can differ from a correct answer.
The pinned reference is the RAW `gateway_query_catalog` output (`data_as_of` and `generated_at` verbatim, plus its UTC
read time), committed in this file beside arm (a)'s result; a restatement is not a reference (CVO sign-off condition,
UB-20261009T083749Z-9a05, 3.0.0_SA_CVO~Z 09:07:24Z). If arm (a) and the CVO's grade fall in the same publication
window, the CVO also takes its own read as a second instrument.

## Step 4 (Analyst relaunch), before r29

Ruled run-as-built by `1.0.0_SA_CTO~Z` (msg 32603): the launcher's first prompt is fixed at `launcher.ps1:172` (PROD
`8cdc7b9`); `0.0.0_AB_MSTR~Z` reads the fast-forward line, the gate line, the Analyst's whoami and any sign-in prompt, then
closes the Analyst before it serves Teams (the BG concierge serves the same account). Measured 09:09Z on site Z: the runtime
checkout `C:\opal_runtime\opal_ai` reads `8cdc7b9`; a `claude.exe` (pid 8212) started 09:09:06Z under a `powershell.exe`
started 09:09:04Z. MSTR~Z's four readings: pending.

**Result, run 1 (09:09Z-09:18Z, PROD `8cdc7b9`; MSTR~Z msg 32612):** fast-forward OK; GATE: PASS (two launches); whoami
NOT READ, because the first prompt never ran (empty input); no sign-in. Closed 09:18Z, no Teams message served. Cause: row
Z-S64 (claude 2.1.295's variadic `--add-dir` swallowed the prompt). Repair: OA-f-9 AMENDMENT 3, opal_ai `c9983bd`.

**Result, run 2 (10:0xZ, PROD `c9983bd`; MSTR~Z msg 32654):** opal_ai DEV and PROD `c9983bd` (ls-remote); runtime checkout
fast-forwarded before launch; GATE: PASS; the command line carries `--add-dir ...\refs -- "Run your On launch steps ..."`;
**whoami ran unattended and returned Opal Bloomberg (opalbloomberg@opalinvest.com)**, then the Analyst moved on to step 2;
no sign-in prompt. Closed 10:06:51Z with no Teams message served. Z-S63 and Z-S64 are disarmed by row Z-S65. Step 4's
launch path is clear; what remains for it is the post-r29 run, with the two arm message ids as the Analyst's next prompt.

**The post-r29 step-4 prompt (registered now, so nothing is composed after the release).** After the arms run, and only
when the BG concierge is not serving the same account at that time (CTO~Z 32603), `0.0.0_AB_MSTR~Z` relaunches as before
and, once the identity gate reads Opal Bloomberg, types into the Analyst window exactly:

> Answer two existing Teams messages in chat 19:2e21f8e5-55ca-45c1-91b9-a4607bf28d4f_ad037ea5-fee8-412e-9da9-15c6cf2a4fbc@unq.gbl.spaces through opal_asker_query with key json/benchmarks/etf_returns.json: message 1791494398066, then message 1791494553407. Report each tool result verbatim to this window and do not post to Teams.

Expected: message `1791494398066` (Alyssa) returns the figure, `data_as_of`, source and scope; message `1791494553407`
(Andrew) returns `asker_no_profile`. The Analyst's window transcript is captured into this folder; the CVO grades it
for FWD-1. Whether the post goes to Teams is not in this run (C1 holds); the organic Teams reply stays the confirming case.

## What a pass does and does not prove

On PASS of both arms the card's "After a pass" acts follow: OA-t-1 r2 and OA-t-3 r2 merge, the BG launch retires (PRD
C11), OA-e-8 measures speed. Per the CVO's sign-off limit, the arms prove the gateway's entitlement mechanism only.
FWD-1 stays NOT_REALIZED until step 4's released Analyst answers a real portal-figure question on its own and the CVO
grades it. Step 4 (the Analyst relaunch) is `0.0.0_AB_MSTR~Z`'s PROCEED act under /govern.
