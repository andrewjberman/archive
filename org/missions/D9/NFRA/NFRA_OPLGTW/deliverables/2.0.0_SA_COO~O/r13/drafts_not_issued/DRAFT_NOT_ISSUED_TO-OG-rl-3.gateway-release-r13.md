# NFRA_OPLGTW task order -- `OG-rl-3` -- the next opal-gateway release on live 3a7d6a7dc8: audit fields, .env shape, roster count, Tax identity host-side, contract pinned

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md</decomp_doc>
<owned_cells>OG-rl-3</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_NFRA_OPLGTW~15</issued_to>
<issued_by>2.0.0_SA_COO~O</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a one-shot deploy; no cron, alarm, monitor or cadence.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change: the host role already reads gateway/principals/rosters (gateway-read-secrets.tf, OG-pr-1).
comp-adversary: DECLARED-NOT-APPLICABLE -- the payload is the CTO's enrichment list (analysis round 12 s.5 item 2).
EGRESS CLASS, declared: NONE beyond Opal's own AWS (S3 upload, SSM, Secrets Manager) and the public gateway URL.
</preflight>

## 1. THE CELL -- `OG-rl-3` (decomposition addendum R3-T.5, item 2)

Handed only after `OG-au-1` is drained to CLOUD. Pattern: your OG-tr-1 records (`ANNOUNCE_OG-tr-1.md`) for every step.
STANDING RULE (row Z-S32): nobody sources `/opt/opal-gateway/.env` in a shell; key names only, or the base64-shipped
parsers under `deliverables/2.0.0_SA_COO~O/{trnspt,r13}/checks/`, never a value echoed.

### PHASE A (pre-GO): read-only on the host; no upload, no secret written

1. **Live ref.** The manifest at HEAD names `3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7`; confirm by host md5 of every
   shipped file. A mismatch STOPS. Release tree `/c/tmp/og-rel7`, branch `rel-nfra-oplgtw-r13`, at that commit
   (CLOUD's gateway tree differs from live by 18 files: never cut from CLOUD). Audited
   `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15` for release-branch commits only.
2. **Audit (row Z-W15-S23).** Merge ONLY `OG-au-1`'s lines (its commits by `0.9.0_WK_NFRA_OPLGTW~19` on CLOUD) onto the
   live `app/audit.py` and `app/tools.py`, plus `tests/test_audit_bytes_principal.py`.
3. **`.env` shape (row Z-S32).** In the live `deploy-to-ec2.sh` `.env` render (one `printf`, ~:388), render every value
   that can hold whitespace double-quoted so a systemd `EnvironmentFile` and a bash parse read the SAME value (today 4:
   `OTP_BEARER`, `OTP_BEARER_LABELS`, `ENABLED_INTEGRATIONS`, `FIRM_ROLE_ARNS`). Key names unchanged (48). Prove on a
   rendered sample with masked values that `_env_shape_host.py`'s parse reads `disagreeing 0`.
4. **Roster log count (row Z-S34).** ~:251 counts `printf '%s' ... | wc -l` (pairs minus 1) and hard-codes
   `master_admin 1 pair`: compute both counts from the parsed roster JSON.
5. **Tax identity host-side.** Replace the deploying-shell input `OG_TAXSMA_WORKBOOK_IDENTITY` (~:173-182, :261) with a
   host-side read of a NEW key `taxsma_workbook_identity` (one `<tid>/<oid>` pair, the pair regex the template already
   has) in the existing secret `gateway/principals/rosters` (the role already reads it; :247-250 validate it -- extend
   that validator to admit the one new key and refuse a malformed value, rc 3, before any `.env` write). The value never
   rides the SSM command text again. The shell variable is no longer read at all.
6. **Contract single source (row NFRA_MCPINDEX-Z-W19-S13).** The shipped `deploy/NFRA_OPLGTW_CONTRACT.json` equals
   `org/standards/NFRA_OPLGTW_CONTRACT.json` at CLOUD HEAD (today both `a86f7e667cfc...`); extend
   `tests/test_schwab_host_inputs.py` so the release suite ALSO fails when the grant-writer's `build_package.py` stages
   the contract from any source other than `org/standards/NFRA_OPLGTW_CONTRACT.json`. Planted-mutant control for both.
7. **Z-S41 bytes (conditional).** If MDPF_TAXSMA's corrected `app/taxsma_workbook.py` has landed by now (register
   `org/tier0_exec/0.0.0_AB_MSTR/parked/TOOL_OWNER_ROUTING_REGISTER_SITEZ.md` row for Z-S41 CLOSED with a commit), ship
   those bytes verified by sha256 against their spec; otherwise do NOT touch that file.
8. **Tests** on the release tree, `AUDIT_PATH` isolated: `test_audit_bytes_principal.py`, `test_schwab_host_inputs.py`,
   `test_taxsma_workbook.py`, `test_mail_route.py`, `test_mail_listing.py`, `test_entitlement_admin.py::test_ogz2_ac08`.
9. **Rollback** `/c/tmp/og-rb7` at `3a7d6a7dc8`, built without uploading, equal file by file to the live S3 artifact.
   Its template still reads the identity from the shell: record that the rollback deploy needs
   `OG_TAXSMA_WORKBOOK_IDENTITY` exported (the issuer supplies it off-repo on request).
10. Write a verify script now (row W15-S18): host `/health` 200, shipped md5 = release bytes, tool list unchanged,
    then `r13/checks/rl3.AC1.sh` and `trnspt/checks/tr.AC1.sh`.
11. `ANNOUNCE_OG-rl-3.md` (steps 1-10 numbers; no value, no identifier). Commit and report. Do NOT upload.

### PHASE B (GO): only after the issuer says GO (CTO + COO halves SIGNED; the gateway queue told)

12. Re-read live; if it moved, re-cut and re-run 1-11. NEVER-2 ledger `nfra-oplgtw-gateway-release-r13` (legs: secret key,
    upload, install + verify, manifest, rollback-proven), entry AND sentinel committed BEFORE the act.
13. **Secret key.** Read `gateway/principals/rosters` IN MEMORY; add `taxsma_workbook_identity` with the value whose
    sha256 equals the host's current `TAXSMA_WORKBOOK_IDENTITY` (read the hash host-side; the issuer supplies the value
    off-repo); `put-secret-value`; prove every pre-existing key's value hash is unchanged. Never print a value.
14. Act from `/c/tmp/og-rel7` with `OG_TAXSMA_WORKBOOK_IDENTITY` UNSET, `DEPLOY_BASE_REF=<live full sha> HALT_ACK=1
    AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15` through `infra/aws/ec2/safe-ec2-deploy.sh`. Capture its result lines literally.
15. Run the verify script immediately. Any failure: roll back, re-verify, close ROLLED BACK. Then STOP and report: the
    issuer makes one live transcript read so `rl3.AC2` has a record to grade; you are continued after it.
16. Record `EC2_MANIFEST.json` `services.opal-gateway` by hand on the CLOUD base; close every leg with proof; commit.

## 2. BOUNDS

Terraform, IAM, the ALB, the instance, the identity allowlist and `app/taxsma_workbook.py` (except step 7) untouched.
`safe-ec2-deploy.sh` READ only. No secret written except step 13's one key. No transcript text. Never push, `git stash`,
rebase, `checkout --` or `clean`; never override a gate; no vendor call. REFUSE a criterion you cannot meet as written.

## 3. SURFACES

<paths>
infra/aws/ec2/EC2_MANIFEST.json
org/critical_paths/change_management/
org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r13.json
org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/
org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

Release-branch only, never merged to CLOUD by this cell: the gateway files of steps 2-8. Rows: id
`NFRA_OPLGTW-Z-W15-S<k>`, fabric `site-z`, disarm_owner `2.0.0_SA_COO~O`.

## 4. PROOF OF SPEC (literal; run from your worktree root after the ledger close is committed)

<proof_of_spec>
  <criterion id="AC1" cell_refs="OG-rl-3"><invocation>bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r13/checks/rl3.AC1.sh; echo "exit=$?"</invocation><expect>(?s)RELEASE READ-BACK ARMS 4 of 4.*RESULT: PASS.*exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="OG-rl-3"><invocation>bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r13/checks/rl3.AC2.sh; echo "exit=$?"</invocation><expect>(?s)bytes integer \S+ 0 True; principal is a \S+ pair True.*RESULT: PASS.*exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="OG-rl-3"><invocation>bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r13/checks/rl3.AC3.sh; echo "exit=$?"</invocation><expect>(?s)sentinel at HEAD=no;.*descends from 3a7d6a7dc8=yes;.*outside the release set 0; ms_ingest.py shipped 0.*RESULT: PASS.*exit=0</expect></criterion>
</proof_of_spec>

- `AC1`: on the served host, `.env` keys unchanged (48), every value parses the same under systemd and bash, the
  contract copy equals `org/standards`, the Tax keys non-empty.
- `AC2`: a post-release transcript read's audit record carries `bytes` and `principal`.
- `AC3`: NEVER-2 closed; the release ships only the named files.

## 5. WHEN YOU ARE DONE

Instance at `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/NFRA_OPLGTW.TO-OG-rl-3.gateway-release-r13.proof_of_spec.json`,
validated with `python .tools/proof-of-spec-check.py <instance>`. Report once per phase.

<!-- ===================== RECORD FACE ===================== -->

**ISSUER NOTES:**
- Round label 13 (addendum R3-T.5, item 2), chained after `OG-au-1`. Halves: CTO + COO (no capability change), never-widen
  ask written at PHASE A. Pre-cut: `rl3.AC1` 3 of 4 (4 parse disagreements), `rl3.AC2` FAIL, `rl3.AC3` FAIL.
- The `.env` key-name before-set is `deliverables/2.0.0_SA_COO~O/r13/RL3_ENV_KEYS_BEFORE.txt` (48 names, SSM
  635a885e-ac82-429c-8035-400c818672c7 era).

<status>pending</status>
<round>13</round>
<slot>~15</slot>
<fabric>site-z</fabric>
<risk>WORLD</risk>
<worker_class>worker</worker_class>
