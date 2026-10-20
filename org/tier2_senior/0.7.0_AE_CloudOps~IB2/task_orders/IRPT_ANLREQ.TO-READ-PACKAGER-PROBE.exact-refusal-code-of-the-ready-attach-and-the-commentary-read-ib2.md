<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-PACKAGER-PROBE.exact-refusal-code-of-the-ready-attach-and-the-commentary-read-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- two diagnostics run once on the resident host in the service's own environment: (A) ONE authenticated package POST as the packager principal to a ticket id that does not exist (the ticket service answers not-found and writes nothing); (B) ONE head and ONE one-byte ranged get of a synthetic leftover object of run 6 by the host's role. No other write, no deploy, no delete, no queue action. The only writes are the record file and one private temp file you create and remove. No ledger.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; probe B reads under the host role as it is.
comp-adversary: RUN -- by reading your read A_PACKAGER_CLIENTERROR.txt (R1L: the READY attach printed `retained_for_retry PackagerRefused` at 08:02:53 and the ticket service log holds NO /package request in the window; the commentary attach printed `class=ClientError`; R3: the role is DENIED s3:GetObject on the analysis_commentaries prefix) and the code (`opal_packager.live_ticket_ports`: every refusal message is a closed code; `resident_installed._packager_http`, `_read_secret_string`) against this cell; the lens: a printed secret, token, header, URL or email (forbidden: print only the exception class and the closed code), a real ticket id (use the bogus id below only), a second POST, a read of the commentary text (probe B asks for ONE BYTE and prints no byte). NOT seen (blind): the unit's exact environment variables; denominator: two probes and one closing line.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 43, workstream ZZ103: the exact refusal code of run 6's READY attach and the exact error of its commentary read (cell AR-y-444).
<owned_cells>AR-y-444</owned_cells>
</decomp_ref>

  <objective>
    Print (A) the exact closed refusal of the packager's ticket port (`attach`) as the resident builds it, for a package POST to a ticket id that does not exist, and (B) the exact error code of a read of run 6's leftover commentary draft object by the host's role. Report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2 with the file path and the lines. GO NOW.
  </objective>

  <context>
    Load /cloud-ops first. Run 6 (receipt A_E2E6.txt, state file `state_e2e6.json` in the same folder). The READY attach (`handle_ready` -> `_attach` -> `ports["attach"]`) raised a `PackagerRefused` BEFORE any request reached the ticket service; the closed code is not in the journal. Candidates: `PACKAGER_TOKEN_UNREADABLE` (the secret `opal/ticketing/svc-irpt-packager` unreadable or without a non-empty `token` member), `<step>:TRANSPORT` (the https call to the packager api_base failed), a refusal word from a 4xx the port converts, or `PACKAGER_PRINCIPAL_UNSET` (the binding is malformed). The commentary attach raised `ClientError` where the code reads the commentary draft (`live_read_artifact` -> the repository -> an S3 get under `irpt/49financial/state/analysis_commentaries/`); your simulation shows the role denied there.
  </context>

  <the_act>
    GO now. The two probes are independent. Never print a secret, token, header, URL or email.
    1. PROBE A. Send a small python3 script to the resident host by Systems Manager AS ROOT, run with the service's own environment and interpreter in the way your V2 script enters it (the transient unit or `systemd-run` with the service unit's Environment and User), with the install root `/opt/irpt-resident/0485393f3a-r34m`:
```
import json, sys, boto3
root = "/opt/irpt-resident/0485393f3a-r34m"
sys.path[:0] = [root + "/ycharts/research", root + "/reports", root + "/ycharts/generate", root + "/intake", root]
import opal_packager
import resident_installed as ri
cfg = json.load(open(root + "/reports/resident_bindings.json"))["packager"]
sm = boto3.client("secretsmanager", region_name="us-east-1")
ports = opal_packager.live_ticket_ports(cfg, read_secret=ri._read_secret_string(sm), http=ri._packager_http)
payload = {"report_ref": "x", "pdf_ref": None, "original_ref": "x", "commentary_ref": None,
           "firm": "49financial", "request_id": "REQ-" + "0" * 24, "request_revision": 1}
try:
    print("A_RETURNED", type(ports["attach"]("TCK-20261020-00000000", payload)).__name__)
except Exception as exc:
    print("A_EXC", type(exc).__name__, str(exc)[:80])
```
    (Adjust only the import path lines if the install tree needs them; the `packager` binding is read from the host file and printed nowhere.) Line: `A <A_RETURNED type|A_EXC class closed-message>`. If the script cannot run, write `A NOT-RUN <why>`.
    2. PROBE B. In the same environment, with boto3 `s3`: `head_object` and `get_object(Range="bytes=0-0")` of the run-6 leftover object under `irpt/49financial/state/analysis_commentaries/` (its key is in `state_e2e6.json`, `leftover_blob_keys`; bucket `opal-data-irpt`); print only `ok` or the botocore error `Code` for each, never the byte. Line: `B head=<ok|CODE> get=<ok|CODE>`.
    3. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_probe/A_PACKAGER_PROBE.txt with the lines A and B (each answered or `NOT-RUN <why>`) and a closing line `PROBES-DONE <n> of 2 answered`. Commit it. Report ONCE as in the objective. Remove the private temp file.
  </the_act>

  <bounds>
    Exactly one package POST (to the bogus ticket id) and one head plus one ranged get. No other call, no purge, redrive or send, no delete, no `get-secret-value` by you (the probe reads the secret in memory through the service's own code and prints nothing of it), no IAM or Terraform change, no deploy. Nothing about Andrew's ticket TCK-20261017-5af976ff is read.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_probe/IRPT_ANLREQ.TO-READ-PACKAGER-PROBE.exact-refusal-code-of-the-ready-attach-and-the-commentary-read-ib2.proof_of_spec.json`.
    <criterion id="PKGPR-AC1" cell_refs="AR-y-444">The record holds the two answer lines and the closing line.<invocation>grep -c -E '^(A |B |PROBES-DONE [0-9]+ of 2 answered)' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_probe/A_PACKAGER_PROBE.txt</invocation><expect>^3$</expect></criterion>
    <criterion id="PKGPR-AC2" cell_refs="AR-y-444">No line holds a token, a URL, a signature or an email address (the leak control).<invocation>grep -c -E 'eyJ[A-Za-z0-9_-]{10,}|https?://|Bearer |X-Amz-|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_packager_probe/A_PACKAGER_PROBE.txt</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-y-444 is the issuer's, as for TO-READ-PACKAGER-CLIENTERROR.
