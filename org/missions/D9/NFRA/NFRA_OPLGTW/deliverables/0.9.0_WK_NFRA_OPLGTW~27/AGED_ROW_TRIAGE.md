# NFRA_OPLGTW -- aged OPEN remediation rows, triaged (OG-ar-1, 0.9.0_WK_NFRA_OPLGTW~27)

Population: the 41 rows whose latest state is OPEN across `remediations/REMEDIATION_v1-v3.md` at the pin 565223dd62 (66 rows; v1 25, v2 11, v3 5). Machine record: `AGED_ROW_TRIAGE.json` (every entry: id, round_graduated, owner, mechanism_one_line, exactly one of the three kinds). No remediation row was edited; `3.0.0_SA_CVO~O` advances them.

**Counts: 28 remediated_by, 11 moves_when, 2 close_reason (41 of 41).** `measured_how` per entry: RE-MEASURED here, PROOF-CITED (a proof instance read, not re-run), RECORD-CITED.

**CLOUD has moved since the pin.** The CVO's own triage (CLOUD @d99813522e) flipped 16 of these rows in place. This file is independent and a superset. It differs from that triage on five rows, measured here, and says so in each entry's `note`: W2-S8, S4, S5, W4-S12, S57 (row Z-W27-S1).

## 1. remediated_by (28) -- a shipped change whose measured result remediates the row

| row | graded in round | owner | by what / measured |
|---|---|---|---|
| S19 | 1 | 2.0.0_SA_COO~O | 72897184fd (halt-gate-check.sh derives HALT_GATE_SHARED_ROOT from git --git-common-dir). Re-measured at the pin from this worktree: the common-dir parent differs from the worktree root; org/mcp/inbox is PRESENT in the shared root ... |
| S4 | 1 | 2.0.0_SA_COO~O | OG-m-2a (c064389bab, live dispatcher advi-49f-gold-dispatch): the S3 accelerator dispatches only on a qualified marker version. Re-measured from the dispatcher's log group, all 382 events since 2026-09-29T03:00Z, no nextToken: 57 ... |
| S45 | 1 | 1.0.0_SA_CTO | OG-n-1 (062e036d54; ledger nfra-oplgtw-gateway-eip closed 473217c119). Re-ran the order's check eip.AC1.sh at the pin: rc=0, 'addresses associated with the instance=1', the association exists and the EIP equals the instance ... |
| S48 | 1 | 2.0.0_SA_COO~O | OG-r-3 change 1 (1efe069571): _cap_respected reads peak_child_rss_bytes on every path and an unread RSS is not respected; test_ogr3_ac01 PASS in that order's proof. Confirmed on the served release: CAPACITY_R4.json (OG-r-4, ... |
| S49 | 1 | 2.0.0_SA_COO~O | OG-r-3 change 3 (1efe069571 lineage; deliverables 0.9.0_WK_NFRA_OPLGTW~11/onhost-capacity-recut.result.md): AC4 grades the ruled windows. Baseline 2026-09-11..09-17: 7 of 7 day-buckets with HTTPCode_Target_5XX_Count 0, 19,473 ... |
| S5 | 1 | 2.0.0_SA_COO~O | OG-m-2a (c064389bab): the dispatch is gated on a qualified closure marker. Re-measured (same read as S4): of 52 s3-triggered invocations since 2026-09-29, 46 SKIPPED on a non-qualified marker and 6 dispatched, each on a qualified ... |
| S57 | 1 | 2.0.0_SA_COO~O | OG-x-2/OG-x-3 (streaming producer, released in 4248b70b39, in the live lineage) and the served-release measurement OG-r-4 (587d79e64e, CAPACITY_R4.json, release 4231bd2ddc, verdict SUFFICIENT; AC1 PASS): a 250,000 x 11 export ... |
| S61 | 1 | 2.0.0_SA_COO~O | OG-t-1 + OG-t-2 (tier released in d61fde4693, live lineage; OG-t-2 proof AC2: tier.py 141 lines, 0 email-roster reads; OG-t-1 AC1 email-keyed resolve_tier call sites 0). Re-measured at the live ref af2d762970: resolve_tier( is ... |
| W2-S10 | 1 | 2.0.0_SA_COO~O | OG-r-3 change 3: AC4 grades R-OG-23A's window 2026-09-11..09-17 (19,473 requests, 0 5xx in 7 of 7 buckets, window p95 0.4960 s, -10.4 % against OG-p-1's 0.5535 s, cap +20 %); OG-r-3 AC4 PASS. OG-r-4 then re-measured capacity on ... |
| W2-S8 | 1 | 2.0.0_SA_COO~O | fd841cd02b (OG-h-1 amendment A1): .gitattributes gains infra/aws/ec2/opal-gateway/**/*.{service,txt,yaml,json,md,html,jsonl} text eol=lf, plus the one exception DATA_CATALOG.yaml -text. Re-measured at the pin (the same 7 lines ... |
| W3-S11 | 1 | 2.0.0_SA_COO~O | OG-u-1 (c4d2274c6d, live lineage): server.py ms_site_children calls _ms_guard before it reads site_id (read at af2d762970 :803-812). Re-ran test_auth_hardening.py + test_ratelimit.py at the pin: 11 passed, 0 failed. |
| W3-S18 | 1 | 2.0.0_SA_COO~O | OG-u-1 (c4d2274c6d): ratelimit.py AUTH_PATHS carries /callback, /schwab/download/login and /schwab/download/callback at af2d762970:44-45, and test_auth_hardening asserts browser_oidc.LOGIN_PATH and CALLBACK_PATH are in it (lines ... |
| W3-S2 | 1 | 2.0.0_SA_COO~O | OG-h-1 (82824d829f): tests/conftest.py points AUDIT_PATH at a private temp file (honouring an environment value) before any app import, and a session fixture patches the cached Config. Re-measured: after 4 pytest invocations ... |
| W3-S5 | 1 | 2.0.0_SA_COO~O | OG-u-2 (0906bf01e5; C1 addendum R-5, 30-day idle lifetime): live at af2d762970 oauth_as.py :535-575 (CLIENT_IDLE_LIFETIME_SECONDS 2592000, expires_at written on the record, get_client returns None once expired, TTL deletion is ... |
| W3-S6 | 1 | 2.0.0_SA_COO~O | OG-h-1 (82824d829f): an autouse fixture uses monkeypatch.setattr(rl.time, 'monotonic', ...), restored per test (test_ratelimit.py:25-29). Re-ran test_ratelimit.py with test_auth_hardening.py in ONE process at the pin: 11 passed, ... |
| W3-S9 | 1 | 2.0.0_SA_COO~O | OG-t-1 + OG-t-2 (the principal tier, released in d61fde4693; OG-t-2 AC2 PASS, 15 of 15 shipped files inside the set, tier.py 0 email-roster reads; AC3 on the host: 0 email roster reads). Re-measured at af2d762970: resolve_tier ... |
| W4-S10 | 1 | 2.0.0_SA_COO~O | bf938bcf39 (IRPT_BCKEND-S122 fix): the manifest probe's code is read as MANIFEST_DECL=0 with '// MANIFEST_DECL=$?', so all three branches are reachable. Re-measured at the pin: infra/aws/lambda/ci/build-and-upload.sh :470-489 ... |
| W4-S12 | 1 | 2.0.0_SA_COO~O | OG-m-3 (4e14699746): the dispatcher grades the chain log, not stdout. Re-measured: the live Lambda's CodeSha256 equals OG-m-3's proof AC2 value (built-artifact sha), and of 11 chain dispatches since 2026-09-29, 10 logged 'OK: ... |
| W5-S6 | 1 | 2.0.0_SA_COO~O | OG-o-4 (877339606f): envelope.py rows counted once, and test_ogo4_ac02 pins a 500-row narrow page. Re-ran test_ogo4_ac02 at the pin: 1 passed, 26 deselected; OG-o-4 proof AC2 1 of 1. |
| W6-S9 | 1 | 2.0.0_SA_COO~O | OG-h-1 (82824d829f): the constant child_lag < 0.25 became a relative bound (loop_lag > 1.0, child_lag < loop_lag / 2). Re-ran test_ogq1_ac02 at the pin: 1 passed, 13 deselected. |
| Z-S23 | 12 | 1.0.0_SA_CTO~O | 490526897d (0.0.0_AB_MSTR~Z): the drain commits from a private index snapshot, so a peer's later staging cannot enter the merge. Re-read at the pin: safe-merge.sh :448-475 takes the snapshot (GIT_INDEX_FILE=$_PRIV_IDX git ... |
| Z-S34 | 12 | 2.0.0_SA_COO~O | OG-rl-4 (release af2d762970, live since 2026-10-03T16:55:49Z): the log line's counts come from the parsed roster JSON (deploy-to-ec2.sh:248 at af2d762970, ROSTER_COUNTS). rl4 AC1 release read-back 4 of 4 arms on the served host ... |
| Z-S41 | 12 | 2.0.0_SA_COO~O | db92656c72, shipped in 4231bd2ddc (OG-rl-3) and carried into live af2d762970. Re-read at af2d762970: taxsma_workbook.py:118-119 _OTHER_ROUTE_BEARERS = (OTP_BEARER, MS_INGEST_BEARER, GRAPH_READ_BEARER, TRANSCRIPT_BEARER, ... |
| Z-S46 | 15 | 1.0.0_SA_CTO~O | bee7c817d7 (the surprise-gate branch checks and reports REMAIN STAGED) corrected by f2c150d420 (Z-S50: it unstages and post-checks everything THIS call staged), both on CLOUD. Re-read on CLOUD: safe-commit.sh :878-899 prints ... |
| Z-W10-S1 | 12 | 1.0.0_SA_CTO~O | CTO round-15 R9 (b56208fd64), ADOPT the measured grain (dim_position + quantity_settled_unsettled and quantity_cash_settled; dim_asset + security_description_line_1) on the evidence of GRAIN_R15.json (OG-gr-2, drain 4b6afce2d2): ... |
| Z-W12-S8 | 12 | 2.0.0_SA_COO~O | OG-wp-1 (DENY_RECORD_ORIGIN.json, 0.9.0_WK_NFRA_OPLGTW~20): a strong full scan (366 items) with the deny record's origin fields all ABSENT, disposition KEEP_WITH_REASON (CTO R2-k call 1) and the synthetic partitions ... |
| Z-W15-S23 | 12 | 1.0.0_SA_CTO~O | OG-au-1 shipped by OG-rl-4 (live af2d762970). OG-rl-4 proof AC2 (b9d98d0f4c): 37 audit records after deployed_at 2026-10-03T16:55:49Z, 1 read_meeting_transcript ok record; the newest: bytes is an integer > 0, principal is a ... |
| Z-W26-S4 | 15 | 2.0.0_SA_COO~O | OG-ts-1 (a9a30299ac; drain 685d7f8489 on CLOUD, issuer re-grade ts1.AC1 PASS): conftest.py loads the pinned staged closure and test_closure_under_test.py pins it; proof AC1 'suite rc=0; test_ogts1_ac01 passed 1 of 1; 24 passed in ... |

## 2. moves_when (11) -- the condition that moves it, and who acts

| row | graded in round | owner | condition and actor |
|---|---|---|---|
| S36 | 1 | 1.0.0_SA_CTO | Andrew's word to delete the 8 probe items on CARD_W2-S6_PROBE_FIXTURES.md (a production-store delete needs it); 1.0.0_SA_CTO~O relays the word, a CloudOps lane runs the per-key deletes. Same act as W2-S6: the 3 PROFILE records ... |
| S63 | 12 | 2.0.0_SA_COO~O | The pilot-walkthrough grading cell re-enters (CTO round-14 R6: as a NEW cell in the round where G-E stands, i.e. after Menachem's tid/oid grant). At that cut 2.0.0_SA_COO~O records which seal is of record and marks the AC8 probe ... |
| W1-S9 | 1 | 2.0.0_SA_COO~O | A registry row (infra/logic/registry) or an R20 register entry that Andrew acknowledges, for opal-mcp-schwab-catalog-read, opal-mcp-emp-menachem-schwab-read and opal-gateway-assume-schwab-readers, owned by 1.0.0_SA_CTO~O with the ... |
| W2-S6 | 1 | 2.0.0_SA_COO~O | Same act as S36: Andrew's word to delete the 8 items on CARD_W2-S6_PROBE_FIXTURES.md (per-key delete commands are prepared, none run), plus a TTL for future probes. Re-measured 2026-10-03: the same 8 items are present (373 of 373 ... |
| W6-S2 | 1 | 1.0.0_SA_CTO | OG-gr-3 (R9's grain into query.py DATASET_GRAINS and datasets.json, with the grain notes) merged, then OG-rl-5 (the gateway release carrying it on af2d762970, under CTO, COO and CVO halves) live; acceptance there: a rows-mode ... |
| Z-S43 | 12 | 1.0.0_SA_CTO~O | An invitation of the delegated identity to the Research Team Meeting series (Andrew's act or the series organizer's; no application route, ruling 28043). Then the 4th meeting re-runs as a NEW cell (OG-tx-2 is cancelled with its ... |
| Z-W12-S7 | 12 | 2.0.0_SA_COO~O | Andrew's interactive authorization-code exchange re-authorizing that client, due before 2026-10-15 (3-day margin; hard stop about 2026-10-18); 2.0.0_SA_COO~O names the session and records the new expiry. No record of the exchange ... |
| Z-W13-S2 | 12 | 1.0.0_SA_CTO~O | The 49F ADVI chain's owner (DT/AE lane, placed through 0.0.0_AB_MSTR~Z's tool-owner routing register, round-12 3a) classifies a dispatch with no chain log as ABORT, or proves the bootstrap order makes it impossible. OG-m-3's ... |
| Z-W13-S5 | 12 | 2.0.0_SA_COO~O | MDPF_CANON's remediation of the 16 out-of-pattern S3 key lines in DATA_CATALOG.yaml lands (the naming limb refuses the line-ending-only diff until then), after which one commit runs git add --renormalize on that one path. The ... |
| Z-W15-S31 | 15 | 2.0.0_SA_COO~O | The next order that touches trnspt/checks/tr.AC1.sh rewrites arm 4 to the live 50-key count (CTO round-14 R4, 'yes with stale arm'); 2.0.0_SA_COO~O owns the check. Re-measured: 2 '48 keys' hits remain (lines 7 and 32) at the pin ... |
| Z-W16-S5 | 15 | 2.0.0_SA_COO~O | The first full trading day on live af2d762970 (live since 2026-10-03T16:55:49Z; 10-03 is a Saturday, so Monday 2026-10-05) elapses; 2.0.0_SA_COO~O re-measures p95 against 0.5535 s with the +20 % cap (0.6642 s) and grades it; a ... |

## 3. close_reason (2) -- no condition moves it

| row | graded in round | owner | reason |
|---|---|---|---|
| S43 | 1 | 2.0.0_SA_COO~O | No condition moves it. OG-h-1 item B registered every citation (OUT_OF_REPO_CITATIONS.md: 36 citing lines in 12 files; 35 ABSENT-ON-SITE-Z, 1 DURABLE). The seal inputs are now durable (7 SSM SecureStrings under the reseal path, ... |
| Z-W17-S4 | 15 | 1.0.0_SA_CTO~O | Ruled KEPT and closed as design by the CTO (round-15 analysis R10, b56208fd64): deleting its block plans a DESTROY of live layer v1 and removed/moved blocks are barred; it stays build-free with its hash read from the deployed ... |

Full text of every measurement, with the commands behind it, is in the JSON entry; the 2026-10-03 live reads were: one consistent DynamoDB scan (373 of 373 items), the dispatcher log group since 2026-09-29 (382 events), `describe` of the dispatcher Lambda, the order's own `eip.AC1.sh`, ALB daily p95, and pytest on the named gateway tests at the pin.
