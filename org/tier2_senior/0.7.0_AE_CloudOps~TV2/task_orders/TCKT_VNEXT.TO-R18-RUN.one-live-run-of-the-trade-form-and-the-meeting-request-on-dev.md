<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R18-RUN.one-live-run-of-the-trade-form-and-the-meeting-request-on-dev</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-14</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>18</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R18.md</decomp_doc> (round 18): cells `R18-mt-5` and `R18-tf-6`, ONE sitting.
<owned_cells>R18-mt-5</owned_cells>
</decomp_ref>

  <objective>
    Run each of the two journeys ONCE, for real, on portal DEV in one sitting under one synthetic internal identity: FWD-10, a Trade Request filed by choosing a firm and
    uploading the placeholder form, the OPEN ticket's form opened from its row; FWD-11, a Meeting Request filed with proposed times, then read after the coordinator's own
    act on the ticket. STAGED: it starts only on the issuer's GO, which names a signed never-widen pair and records that the portal candidates are landed on DEV and the release is live.
  </objective>

  <context>
    **The pair is your whole procedure.** The issuer writes it after `TO-R18-REL` reads REL-OK and the two portal candidates (`cand/dell2/tckt-meeting-request`,
    `cand/dell2/tckt-trade-form-upload`) are landed on portal DEV by `.tools/portal-merge-forward.sh` on Andrew's approval rows, at
    `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`; the CTO signs its half. Its model is the R16 crawl:
    `deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_CW1_CRAWL_PAIR.md` and your own `r16_cw2_crawl.py` (one synthetic `.invalid` identity, ONE token of at most 20 minutes,
    the key and the token in memory only, the row removed after `exp` and read ABSENT, a NEVER-2 ledger entry open until then).
    The identity's firm list is exactly one served firm, the one the pair names (`firm`). The two writes the identity makes are the filings; it files with the Ticket Center's own controls
    in the signed-in browser, never by a direct table write. The trade form is the PLACEHOLDER (a one-page synthetic PDF the pair names, containing no client data), named as such on the
    screen. **The coordinator step is DRIVEN by a second synthetic identity (AMENDMENT 1, CTO ruling msg 7832, ruled (b)):** a minted INTERNAL `@opal.invalid` coordinator is the SOLE
    `ROUTING_MATRIX.meeting_request.primary` for ONE run window, confirms one proposed time on the meeting ticket in the browser, and is deleted. Jeanette's address is never given to a seat and
    is restored as the primary after the window. Jeanette's first real confirm later grades it again as the organic arm, never the gate.
    **Nothing sensitive leaves memory** (key, token). Nothing of any other ticket goes into a file or trace. No engine call, no mail send by this run (a send of any kind is a STOP).
  </context>

  <go>
    AMENDMENT 4 (issuer 2.0.0_SA_COO~V2, 2026-10-16 ~18:2xZ; gate limb: none graded this modification; it names the GO and fixes the run's date stamp, no placeholder, no path widened). CONDITIONAL GO. THE PAIR IS SIGNED BY BOTH HALVES at the file's current blob: COO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md` (git blob `66453198ec9cfbaed19700f3db1097b50f8763ff`, sha256 `2e76b1445ee9e3cc6194ea3b98ec0d589a62e07e5d4ff1ebe235c4ebb07392bc`, @8f17f7b84b); CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R18_RUN_PAIR_CTO_HALF.md` (git blob `0eaaf3299982e2b0a5d56b34b952b7775e6bbb53`, the routing window, mail none, the firm `cottonwood`, the object left in place, the key read) and its AMENDMENT 1 half `.../R18_RUN_PAIR_AMENDMENT_1_CTO_HALF.md` (git blob `cf7c856072d14b70122bb53afbc9259156702d66`, the origin `http://localhost:5174`, plus the added condition: the start gate PRINTS the page origin it opened and the PUT's `Origin` header). Measure those three blobs and the criterion `R18_CHECKS/r18_run_check.py` (`1cc5c4e4ca4047919068b6ac85afeac8e63568b6`) with `git hash-object` BEFORE section 1's start gate; any difference is a STOP and no GO. THE RUN'S DATE STAMP: `20261016`: the identities are `tckt-r18-filer-20261016@opal.invalid` and `tckt-r18-coord-20261016@opal.invalid`, each written with `allowedFirmIds` the LIST `["cottonwood"]` (never `scope_all_firms`; the combined release is LIVE, so a row with neither is refused, 403). START GATE, read by the issuer just now and to be re-read by you (any failing item is a STOP before anything is minted): (1) `TO-R18-REL` is `complete` (TV2's report msg 9736) and `r18_rel_check.py` prints REL-OK (the issuer ran it: REL-OK); (2) the portal DEV checkout carries BOTH forms: `c05e3dda` and `12c164a0` are ancestors of origin/DEV (the issuer read: yes); (3) the live `ROUTING_MATRIX` reads `meeting_request.primary` = `["jeanette@opalinvest.com"]` exactly (the issuer read: yes); (4) no open ledger names `opal-ticket-api`, `opal-tickets` or `opal-users-v2` in any live worktree (print the denominator). THE CTO'S CONDITIONS carried by the combined pair's after-read: the release's apply-end timestamp is 2026-10-16T17:57:19Z (the issuer's after-read of `/aws/lambda/opal-ticket-api` starts there: zero `WE_CLIENT_SENT` and at least one `WE_CLIENT_NO_CONTACT`, which the two CREATEs exercise); record each CREATE's `WE_*` token in your trace. THE S3 OBJECT: the 643-byte placeholder object is left in place by this run (the CTO half, item 4); Andrew's word of ~13:4xZ on 2026-10-16 (recorded at c2b2f1e950) lets a fabric-made synthetic object be deleted by listed key and VersionId without a call, and the issuer does that as its own leg AFTER the CVO's grade, not in this order: print the object's key and VersionId in your result file. Report once to the issuer when `r18_run_check.py` prints RUN-OK and the ledger is closed.
    AMENDMENT 5 (issuer 2.0.0_SA_COO~V2, 2026-10-16 ~18:5xZ, on your STOP msg 9764 and the CTO's msg 9769; gate limb: none graded this modification; it NARROWS, no placeholder, no path widened). THIS ORDER NOW RUNS PART 1 ONLY (FWD-11, the Meeting Request). Trade Request is hidden in the DEV type list by Andrew's word of 2026-10-13 (hide 4d601023), so STEP 3 (the Trade Request, the presign, the PUT, the trade ticket) and every object, form-key and placeholder claim are SKIPPED in this run; FWD-10 is PART 2 under its own later amendment. The pair's AMENDMENT 2 is SIGNED by both halves: COO half `R18_RUN/R18_RUN_PAIR.md` (git blob `000c3467f53fb1bbec6c8660a5eafec7796b32bd`, sha256 `3e0f93494f15ac33f4964bd647d349e4338e2f97cbe0d5dd365421c01e53cd32`, @38415448a5); CTO half `1.0.0_SA_CTO~DELL2/R18_RUN_PAIR_CTO_HALF.md` (git blob `5e89bca0c200adec31f6b6e4377abbca4d460f6c`, @510daa4f60, msg 9769). Measure these two blobs and the criterion `R18_CHECKS/r18_run_check_meeting.py` (`d4a45af2d521704f79605018aad57569971ea141`) BEFORE the start gate; the earlier blobs of AMENDMENT 4 that name the old pair blob and the old criterion are SUPERSEDED by these (the CTO half's AMENDMENT 1 half `cf7c856072d1` still stands for the origin condition: measure it too). THE CHANGES TO THE START GATE: item (2) now reads "the portal DEV checkout carries the MEETING form" (`c05e3dda` and `12c164a0` are ancestors of origin/DEV: yes, read by the issuer), and does NOT require Trade Request in the type list; items (1), (3) and (4) are unchanged and you re-read all of them. THE RESULT FILE `R18_RUN_RESULT.json` carries the MEETING subset of the keys: `browser_origin`, `identity`, `coordinator_identity`, `mt_confirmed_time`, `routing_before`, `routing_during`, `routing_after`, `firm`, `mt_ticket`, `mt_filer`, `row_deleted_at`, `token_exp`, `row_absent_after`, `no_engine_call`, `token_printed` (the new criterion reads exactly these); no `tf_*`, `form_*`, `put_origin_header` or `placeholder_named` key. The filer files ONE ticket (the Meeting Request) and the coordinator makes ONE `POST .../{meeting_ticket}/meeting`; no S3 object is written, so the object-key and VersionId note of AMENDMENT 4 does not apply to this part. The identities (date stamp 20261016, `allowedFirmIds ["cottonwood"]`), the routing window (steps 4 and 6), the removal (step 7), the printed page origin, the mail statement and the CTO's conditions are unchanged. Report once to the issuer when `r18_run_check_meeting.py` prints `RUN-OK (meeting only)` and the ledger is closed.
    AMENDMENT 6 (issuer 2.0.0_SA_COO~V2, 2026-10-16 ~19:1xZ, on the CTO's msg 9780; gate limb: none graded this modification; it narrows, no placeholder, no path widened). THE SERVER ON 5174 IS ANDREW'S SMOKE COPY. `http://localhost:5174` is served now by Andrew's smoke checkout (`C:/dev/smoke-template-5174`, HEAD `1779d676`, which the issuer read: `c05e3dda`, `12c164a0` and `dc057891b086` are ancestors of its HEAD, so it carries the meeting form). This run REUSES it: do NOT start a dev server, do NOT stop or restart the one on 5174 (any step of this order, AMENDMENT 2 or the pair that says "start", "stop" or "bun run dev" is VOID for this part), open the Playwright browser on `http://localhost:5174` and print the page's origin as before, read the server's checkout HEAD read-only (`git -C <that checkout> log -1`, `merge-base --is-ancestor` for the two candidates; any failing is a STOP and you ask the issuer, never edit or restart anything), record `server_reused` true in a NOTE. 5174 is the only dev port (Andrew-direct 2026-09-24).
    The GO's steps are unchanged:
    1. STEP 0: open the NEVER-2 ledger entry; print the per-tree denominator; an open entry naming `opal-ticket-api`, `opal-tickets` or `opal-users-v2` is a STOP.
    2. STEP 1: read `TO-R18-REL`'s result and the live CodeSha256; the portal DEV bundle must carry both candidates (the pair names how it is read); else STOP.
    3. STEP 2: write the identity row (`attribute_not_exists(PK)`, one firm), read it PRESENT, mint ONE token (`exp` at most 20 minutes after `iat`); record `iat`, `exp`.
    4. STEP 3, the Trade Request: in the browser choose Trade Request, the firm, upload the placeholder, submit; read the OPEN ticket by ConsistentRead (`ticket_type trade_request`, the attachment
       key under the firm's prefix); open the form from the ticket row and read the object's `ContentLength` with `head-object` (read-only); record `tf_ticket`, `form_key`, `form_name`.
    5. STEP 4, the Meeting Request, in the window the pair names (AMENDMENT 1): (a) READ `ROUTING_MATRIX` from the live function and record `routing_before` (it must read `meeting_request.primary` = jeanette only,
       else STOP); (b) mint the second identity (the coordinator, `@opal.invalid`, INTERNAL, one firm list as the first, its own row and ONE token of at most 20 minutes) and set `meeting_request.primary` to
       it ALONE by the pair's method (a Terraform apply under `safe-apply`, never a hand edit), READ it back and record `routing_during`; if the create path would mail the routing primary, the pair says how you
       prove it mails nothing to Jeanette (she is not in the list, which is the point of SOLE); (c) as the filing identity choose Meeting Request, the firm, who, purpose, two proposed times, submit; read the OPEN
       ticket and its `routing.primary`; record `mt_ticket`; (d) as the coordinator identity confirm ONE of the two times on that ticket in the browser; read the ticket by ConsistentRead (`meeting.status`
       `confirmed`, `meeting.time` the clicked one, `meeting.by` the coordinator identity, status still `open`); record `coordinator_identity`, `mt_confirmed_time`; (e) restore `meeting_request.primary` to jeanette
       alone by the same method, READ it back and record `routing_after`; the window ends only when that read passes.
    6. STEP 5: wait until BOTH tokens' `exp` have passed, then delete both identity rows and read each ABSENT; close the ledger entry only after that.
    7. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_run/R18_RUN_RESULT.json` with the keys `identity`, `firm`, `mt_ticket`, `tf_ticket`, `mt_filer`, `tf_filer` (the filing
       identity's address, the `.invalid` one), `coordinator_identity` (the second `.invalid` address), `mt_confirmed_time`, `routing_before`, `routing_during`, `routing_after` (each the
       `meeting_request` routing object as read), `row_deleted_at`, `token_exp` (UTC ISO text, the first later, for the LATER of the two tokens), `row_absent_after` (true, both rows), `form_key`, `form_name`, `placeholder_named` (true: the screen
       said so, quote the words), `no_engine_call` (true: the network log of the sitting shows no call to the trade engine, state how read), `token_printed` (false), `claim` (`measured`).
    8. Write the proof-of-spec instance, validate it, report once to `2.0.0_SA_COO~V2` with both ticket ids FIRST. If a STOP fires, report the STOP FIRST with the tickets' state as left; do not retry with a changed method.
  </go>

  <bounds>
    The blast radius is the pair's: two new tickets and one stored object under the firm's prefix, two users rows for the sitting, and the ONE routing window (the `meeting_request` primary changed
    to the synthetic coordinator for the window and restored to jeanette@opalinvest.com, read back after each change). Nothing else. No other ticket, firm, bucket key, table or routing entry.
  </bounds>

  <amendment id="1" date="2026-10-14" by="2.0.0_SA_COO~V2">
    AMENDMENT 1 (issuer; gate limb: none graded this modification; CTO ruling msg 7832, call (b)). Andrew's L2 law (no FWD is a wait when a seat can drive it) turns the coordinator step into a DRIVEN arm:
    a second synthetic internal identity is the SOLE `meeting_request` routing primary for one window, so the test never mails Jeanette and her real address is untouched. The window is the routing widening and
    the pair must cover BOTH directions (set and restore), the read-back after each, and the deletion of both identities read ABSENT. Jeanette's first real confirm later grades it again as the organic arm, never
    the gate. STEP 4, the result keys and the check are amended accordingly.
  </amendment>

  <amendment id="2" date="2026-10-14" by="2.0.0_SA_COO~V2">
    AMENDMENT 2 (issuer; gate limb: none graded this modification; it narrows, adds no placeholder). "Portal DEV" is the DEV branch's dev server on `http://localhost:5174` (its `/api/*` proxies to the one hosted distribution, which serves PROD), never a hosted site: the pair's COO-half AMENDMENT 1 states the reads and the three consequences. In STEP 1 the readiness item reads the dev checkout's HEAD (it carries `cand/dell2/tckt-meeting-and-trade-form`), STEPS 3 and 5 drive a Playwright browser opened on `http://localhost:5174`, and a run that opens `d2n2nzpeqf34ge.cloudfront.net` or any other origin is a STOP: the laptop's CORS list admits `http://localhost:5174`, `https://opalinvest.dev` and `https://www.opalinvest.dev` only. Start the dev server yourself (`bun run dev --port 5174`), stop it at the end, record in the result file how the origin was read (`browser_origin`).
  </amendment>
  <amendment id="3" date="2026-10-15" by="2.0.0_SA_COO~V2">
    AMENDMENT 3 (issuer; gate limb: none graded this modification; carries the CTO's added condition, msg 8757, blob 66453198ec). Before the trade form's first PUT, print the page's origin (`window.location.origin`) and the `Origin` header of the PUT request as the browser sent it. Anything other than `http://localhost:5174` aborts the run BEFORE the PUT (a STOP reported first). Record both in the result file as `browser_origin` and `put_origin_header`; the issuer's check requires both to equal `http://localhost:5174`.
  </amendment>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R18RUN-AC1" cell_refs="R18-mt-5"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_CHECKS/r18_run_check_meeting.py</invocation><expect>^RUN-OK </expect></criterion>
</proof_of_spec>
`R18RUN-AC1` at the issuance: FAIL as expected (no builder record in the main tree, no result file). The check re-reads both tickets from the table (type, status, the trade ticket's attachment key under the
firm's prefix, the meeting ticket's `meeting` member recorded by the recorded coordinator identity and the ticket not completed), the form object with `head-object`, BOTH identity rows (absent) and the live
`ROUTING_MATRIX` (the `meeting_request` primary restored to exactly jeanette@opalinvest.com).

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the key read and the row write are grants the agent user already holds, reported after the fact through `0.0.0_AB_MSTR~DELL2`).
comp-adversary: the control is the check's independent live re-read of both tickets, the object and the identity row, and the pair's STOP conditions.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R18-mt-5, R18-tf-6): one sitting under a signed never-widen pair; not a worker cell (it reads a signing key and drives a signed-in browser).
</task_order>
