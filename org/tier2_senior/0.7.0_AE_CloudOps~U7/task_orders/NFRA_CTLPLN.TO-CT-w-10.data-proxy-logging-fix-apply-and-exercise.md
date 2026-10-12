<task_order id="NFRA_CTLPLN.TO-CT-w-10.data-proxy-logging-fix-apply-and-exercise">
<to_id>NFRA_CTLPLN.TO-CT-w-10.data-proxy-logging-fix-apply-and-exercise</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-12</date>
<status>complete</status>
<status_reason>Closed by the issuer 2.0.0_SA_COO~C after its own reads: proof instance VALID (CTw10-AC1, CTw10-AC2); live CodeSha256 zoCWZxmn6nwzFEEIEIl4NoVP2rojFGntQaLSxy8lLSU= (was aWwkzuxR...), last modified 2026-10-12T11:58:21Z; the deployed package holds exactly three members and their sha256 EQUAL the pin 5a0dfc9af8 (lambda_function.py a9c7a403..., session_tracker.py 00f8c6a3..., firm_page_access.py 7365de94...); the issuer read the 27 log events written after the apply: Bearer 0, eyJ 0, cookie or refresh 0, and three Request lines carrying method, path and request id only. Ledger nfra-ctlpln-ctw10-data-proxy-logging-fix-20261012 CLOSED. The STOP of step 2 was recorded MET and lifted for the apply only by the CTO (msg 108528). NOT done and NOT this order's: the PURGE of the group's 14 days of events and the INVALIDATION of the refresh tokens in the 16 recent lines (two identities by digest, both internal staff, one active and one disabled) are Andrew's; row S9112 stays ARMED on those two until he answers.</status_reason>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>1</round>
<workstream>LOGFIX</workstream>

<title>NFRA_CTLPLN LOGFIX CT-w-10: measure what the data proxy's log group holds, apply the no-credential logging fix by Terraform under a third signed pair, and read the new log lines</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round8.md</decomp_doc>
<owned_cells>CT-w-10</owned_cells>
<decomp_context>Row NFRA_CTLPLN-S9110, ruled ARMED by the CTO (msg 108509): the data proxy prints each caller's bearer token into /aws/lambda/opal-portal-data-proxy. CT-w-9 removes the print and proves it on fake events. This order puts it live and reads the result. Your own seat found the row during CT-w-3; the first two pairs (CT-u-7, CT-w-3) are closed.</decomp_context>
</decomp_ref>

<amendment>
AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~11:3xZ; gate limb: none graded this modification) -- THE GO. Status staged -> pending. The THIRD pair is SIGNED on both halves: COO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-w-10_PAIR_20261012.md` @f716ffd301, CTO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/1.0.0_SA_CTO/NEVER_WIDEN_CT_W10_S9110_LOG_REDACTION_CTO_HALF.md` (msg 108521). THE PIN is `5a0dfc9af8` (CT-w-9 merged @bc07b57d76, CT-w-8 merged @2a978fab00); the three build members and their sha256 are in the pair's section 1. READ BOTH HALVES WHOLE before any act. Conditions the halves carry: (1) the PRE measure counts by KEY NAME only and a long-lived credential found is a STOP plus one line to Andrew for a purge; (2) the CTO's added condition on the mark-only change: diff the DEPLOYED `firm_page_access.py` against the BUILT member with the single GENERATED header line excluded and print the diff; it must be EMPTY (the differing-line count expected 1, the header); non-empty is Branch B; (3) the built zip has exactly three members, hashed against the pin; (4) the callers are the second pair's (the dell walker account; the existing seed test row, armed and restored in the same ledger entry); (5) the log group and its retention are not changed. The 10 workspace tests that read the portal checkout's firmAccess.ts are NOT a Branch-B signal (the checkout is behind; the landed portal file passes).
</amendment>

<amendment>
AMENDMENT 2 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~11:5xZ; gate limb: none graded this modification) -- THE CTO'S RULING on your row NFRA_CTLPLN-S9112 (msg 108528): the STOP of step 2 is LIFTED FOR THE APPLY ONLY. Its purpose was to surface a long-lived credential before anything else, and you surfaced it (refresh_token cookie in 38 lines, 16 within 7 days; device_trust in 29; JWT-shaped in 49). The apply reduces exposure every minute it is live (no new refresh cookie is written), so LAND K1 now under the signed third pair, with the STOP recorded in your ledger entry as MET on the PRE measure. Every other condition of the half stands: P0 (the deployed members equal the second pair's pin), the three-member zip and its hashes, the empty header-excluded diff of `firm_page_access.py`, plan 0/1/0, R1-R3. Two things stay Andrew's and are NOT yours: (a) the PURGE of the group's events (a delete; the CTO has asked him with the counts); (b) the INVALIDATION of the refresh tokens in the 16 recent lines. ADDED STEP 6 (read-only, after the apply): prepare, for Andrew's yes to be one act, the list of the identities behind the 16 recent refresh_token lines BY DIGEST ONLY (a sha256 of each identity string, never the identity, never a cookie or token value, printed as a count and the digests), write it to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-10.affected-identities-digests.txt`, and state how an operator would map a digest back to an account without the log (for example by hashing the users table's emails the same way, read-only). Report it with the rest. Row S9112 keeps your name as the apply's disarm owner and Andrew's as the purge's.
</amendment>

<context>
STAGED. The issuer's GO (a task-order flip to pending with an amendment, as for CT-w-3) arrives when `CT-w-9` and `CT-w-8` are merged AND the THIRD signed pair is on the record: COO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-w-10_PAIR_*.md`, CTO half under `deliverables/1.0.0_SA_CTO/`. It names the PIN (the merge commit carrying the fixed handler and the final `firm_page_access.py`). Do nothing before both. READ BOTH HALVES WHOLE.
The change removes a log line; it narrows what the function writes. Lambda code changes by Terraform only (`safe-apply`, root `infra/aws/terraform/market-overview/`, `aws_lambda_function.portal_data_proxy`); never `aws lambda update-function-code`.
</context>

<the_act>
1. Load `/cloud-ops`. Open ONE NEVER-2 ledger entry naming the function, the pin, the previous artifact version id (rollback = re-apply it) and the consumers (none). `comp-iam` and the graph query with their denominators.
2. **MEASURE the log group BEFORE the apply (read-only, counts only, never a value, bounded by timeout):** over the whole 14-day retention of `/aws/lambda/opal-portal-data-proxy`, count (a) lines containing a JWT-shaped string, (b) lines containing `Cookie` or `cookie` or `refresh`, (c) lines containing `Set-Cookie`. If (b) or (c) is non-zero, look at the KEY NAMES only (not values) and say whether any is a long-lived credential (a refresh token, a session cookie). A long-lived credential present is a STOP: write the one-line ask to Andrew for a log purge in your report and apply nothing. With 15-minute access tokens only, no purge is owed and the retention stays.
3. P0: download the DEPLOYED package and hash its three members; they must equal the CT-w-3 pin's (`17b122b0...`, `00f8c6a3...`, `80590106...`) or STOP. Build the code-only zip per the source map at the pin; read back its member list (exactly three) and hash all three against the pin; `safe-apply` on the one root, plan 0 add / 1 change / 0 destroy or STOP; read back the live `CodeSha256`; close the entry only when it equals the built file's.
4. **EXERCISE and read the NEW lines:** with the callers of the first two pairs (the dell walker account for the INTERNAL caller; the existing seed test row on a partner firm for the PARTNER caller, armed and restored in the same ledger entry), make: one internal call to `GET /aum/metrics` (expect 200), one partner call to `GET /aum/metrics` (expect 200), one partner call to a class-(ii) route (expect 403). Then read ONLY the log events written after the apply time: print the count of events, the count containing a JWT-shaped string (expect 0), the count containing `Bearer` (expect 0), and one example line with every value other than the method and the path replaced by `<redacted>`. Write all of it to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-10.logging-fix-exercise.txt`. Final lines, exact form: `class-i admitted-firm=<code> internal=<code>`, `class-ii partner=<code>`, `POST-APPLY events=<n> jwt_shaped=<k> bearer=<k>`.
5. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR: the pin, CodeSha256 before and after, the plan counts, the step-2 counts, the ledger entry, the codes and the post-apply counts.
</the_act>

<bounds>
- One Lambda's code only. No IAM, API Gateway, authorizer, log-group, retention or table change; the log group is NOT purged by this order. No `update-function-code`. No `terraform apply` except through `safe-apply`. A plan that moves anything but the one resource is a STOP. No credential minted; no token or cookie VALUE printed or stored, anywhere.
</bounds>

<proof_of_spec>
<criterion id="CTw10-AC1" cell_refs="CT-w-10"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-10.logging-fix-exercise.txt</invocation><expect>jwt_shaped=0 bearer=0</expect></criterion>
<criterion id="CTw10-AC2" cell_refs="CT-w-10"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-10.logging-fix-exercise.txt</invocation><expect>class-ii partner=403</expect></criterion>
</proof_of_spec>
<expected_criteria>CTw10-AC1,CTw10-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-10.data-proxy-logging-fix-apply-and-exercise.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTw10-AC1,CTw10-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~U7/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/terraform/market-overview/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one-time apply.
comp-iam: RUN at step 1 -- denominator one function; the seat's own apply grant on the one root; BLIND to the readers of the log group (NFRA_IAMROLES202609 owns that, ruling c404 s.4).
comp-adversary: RUN -- a long-lived credential in 14 days of logs (step 2 STOPs and asks Andrew for a purge); a token value copied into a report or file (counts and key names only, never values); a fix that changes an answer (the codes of step 4 and the 965 fence tests); BLIND: log lines written before the apply, which stay until retention expires (15-minute tokens).
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, the one Terraform root and the surprise channel.
</preflight>

Source: CTO ruling msg 108509 (record CTO_RULING_NFRA_CTLPLN_S9110_DATA_PROXY_LOGS_BEARER_TOKENS_20261012.md).
</task_order>
