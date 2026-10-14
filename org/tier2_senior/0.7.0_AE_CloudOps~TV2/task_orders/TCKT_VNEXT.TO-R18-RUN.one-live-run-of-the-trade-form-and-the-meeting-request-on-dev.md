<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R18-RUN.one-live-run-of-the-trade-form-and-the-meeting-request-on-dev</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-14</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>18</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R18.md</decomp_doc> (round 18): cells `R18-mt-5` and `R18-tf-6`, ONE sitting.
<owned_cells>R18-mt-5 R18-tf-6</owned_cells>
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
    screen. **The coordinator's act is a pre-arranged input, not yours:** `jeanette@opalinvest.com` confirms one proposed time (or proposes another) on the meeting ticket in her own session;
    the issuer asks for it through the box CTO's queue, with the ticket id this run prints. No seat acts as her and the identity is never given her address. Your result file records the
    meeting ticket id as `mt_ticket` the moment the filing is made; the check reads the coordinator's trace later.
    **Nothing sensitive leaves memory** (key, token). Nothing of any other ticket goes into a file or trace. No engine call, no mail send by this run (a send of any kind is a STOP).
  </context>

  <go>
    STAGED. The GO is an AMENDMENT to this order citing the signed pair. Then, in order:
    1. STEP 0: open the NEVER-2 ledger entry; print the per-tree denominator; an open entry naming `opal-ticket-api`, `opal-tickets` or `opal-users-v2` is a STOP.
    2. STEP 1: read `TO-R18-REL`'s result and the live CodeSha256; the portal DEV bundle must carry both candidates (the pair names how it is read); else STOP.
    3. STEP 2: write the identity row (`attribute_not_exists(PK)`, one firm), read it PRESENT, mint ONE token (`exp` at most 20 minutes after `iat`); record `iat`, `exp`.
    4. STEP 3, the Trade Request: in the browser choose Trade Request, the firm, upload the placeholder, submit; read the OPEN ticket by ConsistentRead (`ticket_type trade_request`, the attachment
       key under the firm's prefix); open the form from the ticket row and read the object's `ContentLength` with `head-object` (read-only); record `tf_ticket`, `form_key`, `form_name`.
    5. STEP 4, the Meeting Request: choose Meeting Request, the firm, who, purpose, two proposed times, submit; read the OPEN ticket; record `mt_ticket`. Do NOT touch it again.
    6. STEP 5: wait until `exp` has passed, then delete the identity row and read it ABSENT; close the ledger entry only after that.
    7. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_run/R18_RUN_RESULT.json` with the keys `identity`, `firm`, `mt_ticket`, `tf_ticket`, `mt_filer`, `tf_filer` (the filing
       identity's address, the `.invalid` one), `row_deleted_at`, `token_exp` (UTC ISO text, the first later), `row_absent_after` (true), `form_key`, `form_name`, `placeholder_named` (true: the screen
       said so, quote the words), `no_engine_call` (true: the network log of the sitting shows no call to the trade engine, state how read), `token_printed` (false), `claim` (`measured`).
    8. Write the proof-of-spec instance, validate it, report once to `2.0.0_SA_COO~V2` with both ticket ids FIRST. The criterion below passes only after the coordinator's act; this order
       is complete for YOUR part when the result file is written and the row is ABSENT, and its `status_reason` says the coordinator's trace is read by the issuer's check later.
       If a STOP fires, report the STOP FIRST with the tickets' state as left; do not retry with a changed method.
  </go>

  <bounds>
    The blast radius is the pair's: two new tickets and one stored object under the firm's prefix, one users row for the sitting, nothing else. No other ticket, firm, bucket key or table.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R18RUN-AC1" cell_refs="R18-mt-5 R18-tf-6"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_CHECKS/r18_run_check.py</invocation><expect>^RUN-OK </expect></criterion>
</proof_of_spec>
`R18RUN-AC1` at the issuance: FAIL as expected (no builder record in the main tree, no result file). The check re-reads both tickets from the table (type, status, the trade ticket's attachment key under the
firm's prefix, the meeting ticket's `meeting` member recorded by the coordinator and the ticket not completed), the form object with `head-object`, and the identity row (absent).

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the key read and the row write are grants the agent user already holds, reported after the fact through `0.0.0_AB_MSTR~DELL2`).
comp-adversary: the control is the check's independent live re-read of both tickets, the object and the identity row, and the pair's STOP conditions.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R18-mt-5, R18-tf-6): one sitting under a signed never-widen pair; not a worker cell (it reads a signing key and drives a signed-in browser).
</task_order>
