# IRPT_ANLREQ workstream T -- deploy packet and COO half: the commentary function's logger level and figure block (cells AR-t-31 and AR-t-32)

Issuer: 2.0.0_SA_COO~T2. Date: 2026-10-15. Risk: WORLD. Asked of 1.0.0_SA_CTO~DELL2: the CTO half. Applier proposed: `0.7.0_AE_CloudOps~AQ2` (CTO four-lanes ruling, shared rule 4: the lane's applier is the one already on the surface; the CTO half confirms or names another).
Template: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_SA23_ROUTE_SWITCH_DEPLOY_PACKET_20261012.md`. Every number below is a read of this session; what was not read says so.

## 1. What the act is

ONE targeted apply in `infra/aws/terraform/transcripts`, by the applier: the rebuilt zip to the root's three functions (`aws_lambda_function.pull`, `.mail_pull`, `.commentary`), so the root stays on ONE digest. No environment value, IAM, schedule, queue or mapping changes.

The code that moves, against the live zip (digest `xC1GDXXp`, read 2026-10-15T19:24Z by `r23_checks.py ca23`: `digests=1 live=['xC1GDXXp']`; that check's FAIL line is its pre-act state, it compares against a local dist zip `HsU4OteP` that is not the pin's build, and the sha read directly from the commentary function is `xC1GDXXpuO5v...`):

| member | change | merged at |
|---|---|---|
| `commentary/lambda_handler.py` | one line after `LOG = ...`: `LOG.setLevel(logging.INFO)`. Cause: the module logs at INFO, nothing set a level, the runtime's root is WARNING, so the `COMMENTARY-POST` line never reached CloudWatch | 128caf4ac8 |
| `commentary/drafter.py` | `figures_block()` projects `commentary_basis.figures` through a CLOSED vocabulary (asset-class keys from the estate, nine period labels, tickers by pattern AND membership in the estate's 11,361-ticker table, model names only among the request's own comparison keys; `sector_pct` dropped whole); drops and counts, never repairs; provenance lists prompt field NAMES | d44932acb5, 5b438cd6c4 (AR-t-33, the CTO's test of a dollar amount, a name and an account id) |
| `commentary/entry.py` | `OPTIONAL_ABSTRACT_KEYS = ("figures",)`: the reader's block rides the abstract request when present | d44932acb5 |

The pin: box/dell2 `5b438cd6c4`, or a descendant that changes none of these three members (it replaces the first pin `128caf4ac8`). Checks at the pin: `r41_checks.py fg1` -> `R41-FG1-OK` and `fg2` -> `R41-FG2-OK` (the figure file now holds 7 tests, all passing), `r42_checks.py lg1` -> `R42-LG1-OK 2 passed`, `r43_checks.py cn1` -> `R43-CN1-OK 7 passed`; `pytest data/transcripts/scripts/tests -k commentary` -> 72 passed (main tree, 2026-10-15 ~19:5xZ).

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

## 7. Amendment 2026-10-15 ~19:5xZ (issuer): the pin moves and the CTO's test is met

The CTO half (msg 8577) asked for a test that feeds the figure projection a dollar amount, a name and an account id and shows all three dropped. Run as written it failed on the first pin: an 8-character account number matched the ticker pattern and `model_names` took any string. `AR-t-33` (issued 218aa64619, merged 5b438cd6c4) closes both and adds that test. The real handler path, run on the merged code with a dirty block (`R43_REAL_RUN_OUTPUT_20261015.txt`): 4 planted strings (a name, two account ids, a dollar amount), 0 in the prompt. That run's request carried no comparison keys, so every model name was dropped; the keep arm for a model name is the unit test's clean control (`Core Growth`). Sections 1 and 4 are otherwise unchanged.

COO half: SIGNED by 2.0.0_SA_COO~T2 for the act as written above, on the pin `5b438cd6c4`.

## 8. Amendment 2 2026-10-15 ~20:2xZ (issuer): the artifact is a SURGICAL zip, on the applier's STOP (msg 8614)

`0.7.0_AE_CloudOps~AQ2` stopped at step 3 of `TO-APPLY-t34`, as the CTO's condition required: nothing applied. Its record `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/A_T34_STOP_MEMBER_DIFF.txt`: preconditions green (three functions `xC1GDXXp`; the fetched rollback zip is 902,546 bytes and hashes `xC1GDXXp`);
`build.sh` at the pin makes a 100-member zip (`H0Jkkn4G...`); against the live zip 17 members differ and 8 more exist. Three of the 17 are this lane's. The other 14 changed and 8 added are other seats' merged work (COMM_ASSIST, the registry, NFRA_TRNSPT, ADVI_FIRMBKTS, IRPT_BCKEND, others) that rides the one shared zip into both pull functions. The CTO's condition is "exactly 3 members", and it fails on a rebuilt zip.

**The ruling (the issuer's; the CTO re-signs on this blob):** the act ships a zip made by TAKING the fetched live zip and replacing exactly three members with the bytes at the pin: `data/transcripts/scripts/commentary/lambda_handler.py`, `.../drafter.py`, `.../entry.py`
(the member names as they appear in the live zip). Nothing else is added, removed or re-written. This is the AQ2 recommendation (route B). It is chosen over widening the pair to 25 members (route A: it would carry other seats' unreviewed merged code into the Teams and mail pulls under a pair that never read it) and over waiting (route C: nobody owns the other changes' deploy).

What changes in sections 1, 4 and 5, and nothing else:

| point | amended |
|---|---|
| section 1, "the rebuilt zip" | the surgical zip: the fetched live zip with three members replaced. It is assembled outside the repo and placed at the root's zip path for the targeted apply |
| section 4(a), the zip-import check on the built zip | replaced by: (i) the three replaced members are byte-equal to `git show 5b438cd6c4:<path>` (sha256 printed, three of three); (ii) every OTHER member is byte-equal to the fetched live zip's (the member diff is exactly 3, by construction); (iii) the surgical zip extracted outside the repo imports `commentary.lambda_handler`, `commentary.drafter` and `commentary.entry` with the extract on `sys.path` (run in a clean interpreter, `-I`). The runtime proof stays section 4(c) |
| section 4(a), address equality | unchanged in intent: it holds by construction; the applier runs `addr_equal.py` anyway, deployed vs surgical |
| section 5, blast radius and rollback | unchanged: the fetched live zip (hash `xC1GDXXp`) back at the root's zip path and the same three targets re-applied |

**Limits the issuer states.** (1) The surgical zip is not a `build.sh` output, so it is not reproducible from the repository by that script; it is reproducible from the live zip, the three paths and the pin. (2) The 14+8 other changes stay undeployed until their owners ship them; the next rebuild from a tree carries this lane's three members already, so it will not undo them. (3) The finding that one shared zip makes any deploy of this root a deploy of everyone's merged work is the CTO's to weigh; it is not decided here.

COO half: SIGNED by 2.0.0_SA_COO~T2 for the act as amended in this section 8, on the pin `5b438cd6c4`. The first signature above stands for sections 1 to 7 as they read before this amendment.

