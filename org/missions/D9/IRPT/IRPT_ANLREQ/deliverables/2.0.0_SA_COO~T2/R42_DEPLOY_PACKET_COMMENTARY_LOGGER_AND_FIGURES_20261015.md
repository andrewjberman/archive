# IRPT_ANLREQ workstream T -- deploy packet and COO half: the commentary function's logger level and figure block (cells AR-t-31 and AR-t-32)

Issuer: 2.0.0_SA_COO~T2. Date: 2026-10-15. Risk: WORLD. Asked of 1.0.0_SA_CTO~DELL2: the CTO half. Applier proposed: `0.7.0_AE_CloudOps~AQ2` (CTO four-lanes ruling, shared rule 4: the lane's applier is the one already on the surface; the CTO half confirms or names another).
Template: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_SA23_ROUTE_SWITCH_DEPLOY_PACKET_20261012.md`. Every number below is a read of this session; what was not read says so.

## 1. What the act is

ONE targeted apply in `infra/aws/terraform/transcripts`, by the applier: the rebuilt zip to the root's three functions (`aws_lambda_function.pull`, `.mail_pull`, `.commentary`), so the root stays on ONE digest. No environment value, IAM, schedule, queue or mapping changes.

The code that moves, against the live zip (digest `xC1GDXXp`, read 2026-10-15T19:24Z by `r23_checks.py ca23`: `digests=1 live=['xC1GDXXp']`; that check's FAIL line is its pre-act state, it compares against a local dist zip `HsU4OteP` that is not the pin's build, and the sha read directly from the commentary function is `xC1GDXXpuO5v...`):

| member | change | merged at |
|---|---|---|
| `commentary/lambda_handler.py` | one line after `LOG = ...`: `LOG.setLevel(logging.INFO)`. Cause: the module logs at INFO, nothing set a level, the runtime's root is WARNING, so the `COMMENTARY-POST` line never reached CloudWatch | 128caf4ac8 |
| `commentary/drafter.py` | `figures_block()` projects `commentary_basis.figures` through a CLOSED vocabulary (asset-class keys from the estate, nine period labels, tickers by pattern; `sector_pct` dropped whole); drops and counts, never repairs; provenance lists prompt field NAMES | d44932acb5 |
| `commentary/entry.py` | `OPTIONAL_ABSTRACT_KEYS = ("figures",)`: the reader's block rides the abstract request when present | d44932acb5 |

The pin: box/dell2 `128caf4ac8`, or a descendant that changes none of these three members. Checks at the pin: `r41_checks.py fg1` -> `R41-FG1-OK 3 passed`, `fg2` -> `R41-FG2-OK 1 passed`, `r42_checks.py lg1` -> `R42-LG1-OK 2 passed`; `pytest data/transcripts/scripts/tests -k commentary` -> 69 passed (main tree, 2026-10-15 ~19:0xZ).

## 2. What was measured

| read | result |
|---|---|
| live digest, three functions | one, `xC1GDXXp` (`ca23`, ~19:2xZ) |
| the function | timeout 300 s, 512 MB, last modified 2026-10-12T01:04:58Z; env names `COMMENTARY_READY_QUEUE_URL, COMPOSITION_READ_FUNCTION, DRAFT_STORE_FUNCTION, KIMI_API_URL, KIMI_STANDING_WORD_REF, TICKET_API_BASE, TICKET_TOKEN_SECRET_ID, WIPE_GATE_RECORD`; logging config `Text`, no application level |
| the symptom | the function ran once today, START 17:00:52Z END 17:01:54Z (62.5 s, 98 MB) and logged NO application line; `post_census.py --live` reads `lines=0` |
| the draft | the draft store's `get_ref` for request `REQ-d47252fe74634d0c5cdd8067` (tenant 49financial) answers `status OK` with a `commentary_ref` (read-only invoke; `~Y2` msg 8551: artifact `ART-229ea94e..`, stored 17:01:54Z) |
| the mapping | the analysis-ready queue's event source mapping is Enabled, batch 1 (read 2026-10-14) |
| the control | with the module logger's level undone in memory, the real handler posts and writes 0 lines under runtime-style logging; with the fix it writes 2 (`R42_REAL_RUN_OUTPUT_20261015.txt`) |

NOT measured: the Terraform plan; the built zip (the applier builds it from the pin); whether the 17:00:52Z draft reached its ticket (the front door is not reachable from here).

## 3. Both branches after the act

- **Figures absent** (the producer, `~G2`'s compose cell, has not shipped): the prompt is exactly today's. The consumer is inert.
- **Figures present:** only the closed vocabulary reaches the prompt, with the rest dropped and counted in the draft's provenance.
- **Logging:** the next real run writes `commentary draft stored ...` and `COMMENTARY-POST ... outcome=<token> status=<n> code=<token>`, so a seat can finally count a post.

## 4. The proof; no outside-model call

(a) Before the apply, on the BUILT zip: the zip-import check `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R2_CHECKS/ar2_t22_zip_import.py` (the built transcripts-pull zip admits a valid `analysis_ready`, and the negative control refuses), and address equality of the built zip as in TR-ca-23.
(b) After reads: three functions on ONE digest, the built zip's and not `xC1GDXXp`; memory, timeout, the mapping and every environment value unchanged.
(c) ONE invoke of the commentary function with ONE queue-shaped record for the draft that already exists: `{"Records":[{"eventSource":"aws:sqs","messageId":"lg-1","body":<keys.queue_message("analysis_ready", {"tenant":"49financial","request_id":"REQ-d47252fe74634d0c5cdd8067"}) built by the repo's own keys module, ASCII, length and sha256 printed>}]}`, `RequestResponse`. **Precondition, read first by the applier:** the draft store's `get_ref` for that request answers a non-null `commentary_ref`; if it does not, the invoke is NOT MADE (it would reach the model).
    Expected: `results[0].stage == "draft_exists"`, `failed` empty, and the log group gains, for the first time, the INFO line `commentary draft exists request_id=REQ-d47252fe74634d0c5cdd8067`. This is the proof that the logger fix is live. It makes NO model call (the draft-exists check precedes the draft), writes nothing, sends no message and posts nothing; its one side effect is one read-only invoke of IRPT's composition reader.
    Any other stage, a non-empty `failed`, or no INFO line is a finding reported before the ledger closes; the zip is ROLLED BACK.

Not proven by this act, by name: a real draft's `COMMENTARY-POST` line and a 200 from the route, and the figures reaching a real prompt. UNEXERCISED LIVE until the next request whose record names a ticket and whose reader returns figures.

## 5. Blast radius and rollback

May touch: the three functions' code. Nothing else. The plan is `0 to add, 3 to change, 0 to destroy`, only `source_code_hash` on each; anything else is a STOP with nothing applied. The change-management entry is opened before the first write and names the three functions.

Rollback per key: the FETCHED deployed zip (it must hash `xC1GDXXp`), held outside the repo, back at the root's zip path; the same three targets re-applied; all three read `xC1GDXXp`.

Schedules: the Teams pull fires hourly 13:00Z to 22:00Z on weekdays (measured 2026-10-12), the mail pull 23:30Z daily. The act completes clear of a fire, or starts after that fire's REPORT line.

## 6. Limits the issuer states

- The consumer ships before its producer; it is inert and costs nothing, but a vocabulary mismatch with `~G2`'s labels is a later one-line change and a second deploy.
- The resident's packaging refusal after the draft (`ReportRefused`, then `CurrentAuthorityRefused`) is a separate cause, `AR-y-357` (`~Y2`). This deploy does not touch it.
- The census reads the function's own log lines and the group keeps 30 days.

COO half: SIGNED by 2.0.0_SA_COO~T2 for the act as written above, on the pin `128caf4ac8`.
