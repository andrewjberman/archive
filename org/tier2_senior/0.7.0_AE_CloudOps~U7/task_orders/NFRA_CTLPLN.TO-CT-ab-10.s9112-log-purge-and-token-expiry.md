<task_order id="NFRA_CTLPLN.TO-CT-ab-10.s9112-log-purge-and-token-expiry">
<to_id>NFRA_CTLPLN.TO-CT-ab-10.s9112-log-purge-and-token-expiry</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-13</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>2</round>
<workstream>LOGFIX</workstream>

<title>NFRA_CTLPLN LOGFIX CT-ab-10 (row S9112): delete the data proxy's pre-fix log streams that carry credential material, print when the leaked tokens expire, and read whether the signing secret can be rotated -- no account is disabled</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round12.md</decomp_doc>
<owned_cells>CT-ab-10</owned_cells>
<decomp_context>Row NFRA_CTLPLN-S9112: before the CT-w-10 apply (2026-10-12T11:58:21Z, the function's LastModified) the data proxy printed whole events, so `/aws/lambda/opal-portal-data-proxy` holds 38 lines with refresh_token cookie material (16 within 7 days, two identities by digest, both internal staff, one active, one disabled) and 29 with device_trust. Andrew delegated it: "Row S9112 this can be done programmatically, i shouldnt need to be involved directly" (record org/tier1_exec/2.0.0_SA_COO~C/deliverables/ANDREW_DIRECT_20261013_143xZ_NFRA_CTLPLN_ROUND12_CALLS_ANSWERED.md, his confirmation of the deletion). The CTO's ruling sets the shape: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL_ADMIN_GROUP_SUPERSEDES_GRANTS_AND_S9112_PURGE_ROTATE_IF_EXISTS_NO_ACCOUNT_DISABLE_20261013.md section 2 (read it whole). Refresh tokens here are stateless RS256 JWTs (no per-token revocation: infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts about :232-245, :272 accepts the current or previous key).</decomp_context>
</decomp_ref>

<the_act>
1. Load `/cloud-ops`. Open ONE NEVER-2 ledger entry naming the log group, the cut time (2026-10-12T11:58:21Z), the streams to delete (by count and time span, before any delete), and the statement that the deletion is not recoverable and is confirmed by Andrew's sentence above.
2. **PURGE (the only write):** list every log stream of `/aws/lambda/opal-portal-data-proxy` (auto-paginated, count client-side, print the denominator). Delete exactly the streams whose `lastEventTimestamp` is BEFORE the cut time. A stream whose events span the cut time is NOT deleted; print it. Then re-count: the post-purge census of the 14-day group by KEY NAME only (refresh_token, device_trust, JWT-shaped, Bearer) must read 0 for lines before the cut; print the counts. Do not change the group, its retention or any other group.
3. **EXPIRY (read only):** for the token lines counted before the purge (count them in step 2 before deleting, by key name only), print the latest possible expiry of each set from the token TTLs the auth handler configures (read the TTL from code or configuration; never decode or print a token value): `refresh_latest_expiry=<UTC>`, `device_trust_latest_expiry=<UTC>`.
4. **ROTATION PATH (read only):** read where the signing secret lives (`opal/auth/jwt-private-key` per the code; confirm by a describe, never a get-secret-value) and whether a rotation path exists at HEAD (a rotation Lambda, a runbook, a script). Print `rotation_path=<path or NONE>`. Do NOT rotate: a rotation signs every user out and is its own order under its own pair, cut by the issuer if a path exists.
5. Write all of it to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-10.s9112-purge-record.txt` with these final lines, exact form: `PURGE streams_listed=<n> streams_deleted=<k> spanning_kept=<m>`, `POST-PURGE pre_cut_refresh=<k> pre_cut_device_trust=<k> pre_cut_jwt=<k> pre_cut_bearer=<k>`, `refresh_latest_expiry=<UTC>`, `rotation_path=<path or NONE>`. Close the ledger entry. Report to 2.0.0_SA_COO~C.
</the_act>

<bounds>
- Deletes ONLY log streams of the one group whose last event is before the cut. No other delete. No account disabled or edited; no secret read, rotated or written; no token or cookie VALUE printed or stored anywhere (key names and counts only).
</bounds>

<proof_of_spec>
<criterion id="CTab10-AC1" cell_refs="CT-ab-10"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-10.s9112-purge-record.txt</invocation><expect>pre_cut_refresh=0 pre_cut_device_trust=0 pre_cut_jwt=0 pre_cut_bearer=0</expect></criterion>
<criterion id="CTab10-AC2" cell_refs="CT-ab-10"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-10.s9112-purge-record.txt</invocation><expect>rotation_path=</expect></criterion>
</proof_of_spec>
<expected_criteria>CTab10-AC1,CTab10-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-10.s9112-log-purge-and-token-expiry.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTab10-AC1,CTab10-AC2`, and leave the status flip to the issuer. Row S9112's disarm_owner is this seat (CTO ruling section 2); append its disposition row when done.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~U7/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one purge.
comp-iam: RUN at step 1 -- denominator one log group; the laptop identity's delete grant on it; BLIND to the readers of the group (NFRA_IAMROLES202609's).
comp-adversary: RUN -- a post-fix stream deleted (only streams ending before the cut); a spanning stream deleted (kept and printed); a token value copied into the record (key names and counts only); a rotation performed by this order (forbidden, its own pair); BLIND: copies of the log lines outside this group (exports, subscriptions) -- list any subscription filter on the group and print it.
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, and the surprise channel.
</preflight>

Source: row S9112; Andrew's delegation @a7d5d7955c; CTO ruling @53acd6fe5f section 2.
</task_order>
