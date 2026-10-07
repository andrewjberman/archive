# Never-widen ask -- OG-rl-12 (A3), the r26 opal-gateway release on live 240ac2fe5a (round 25)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-07 ~11:1xZ.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-12.gateway-release-r26.md`, with A1, A2 and
  A3 (@c38d69aa3d). Cut to `RELEASE_ORDER_FORM.md`.
- **Spec:** Andrew's word on the allowlist row (record @4403ac63df); CTO R36 of round 23 (the dedupe, msg 30594); the
  release ask of `1.0.0_SA_CTO~Z` for the chart route (msgs 30765, 30774); `ledger/ROUND_ANALYSIS.round24.md` @0e813364da
  item 1.
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-12.md`, worker commit `448254b4d9`, drained
  to CLOUD @`8499c15bbb`. The blast radius, writers and branches are stated there in full and are not repeated here.
- **Release sha the halves sign:** `feddb372443adbcf139febab35b69f109e49b664`, branch `rel-nfra-oplgtw-r26`
  (`/c/tmp/og-rel21`).

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~Z` (CTO), by its msg 30779;
- `3.0.0_SA_CVO~Z` (CVO), by the CTO's ruling msg 30779. REQUIRED: served output moves three ways;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes -- the issuer's own reads at 11:0xZ

- `feddb37244` is ONE commit on live `240ac2fe5a` (`git rev-list --count` = 1; its parent is the live sha).
- `git diff --name-only 240ac2fe5a feddb37244`: 10 files, all in the gateway tree. 5 ship to the host
  (`app/integrations/opal_portal/integration.py`, `identity_tool_allowlist.txt`, `app/rivalfunds_view.py`,
  `app/server.py`, `app/tests/test_rivalfunds_view.py`); 5 are source-only tests.
- `git diff --name-only feddb37244 CLOUD -- infra/aws/ec2/opal-gateway` at CLOUD @0f7e460190: one line, the CLOUD-only
  `runbooks/SCHWAB_PILOT_RUNBOOK.md`.
- The route's 4 files: each release blob equals the blob at `f7f2cb7c2e` (4 of 4). The COO half on the handler
  (`RELEASE_NEEDS_RIV-rt-1_CHART_ROUTE_20261007.md` @ec89bbe212, section 3) therefore carries to this sha.
- The allowlist row and the execution-id shape check are BOTH in the release (the binding term of the round-24
  analysis, section 3): the allowlist diff adds 6 lines, and `integration.py` at the release sha carries the check.

**Worker's measurements (ANNOUNCE):** host md5 97 of 97 equal to live; tests 626 passed and 7 failed on the release tree,
the same 7 ids as on live, 0 new; form step 7a 11 passed and 12 passed; rollback tree `/c/tmp/og-rb20` at `240ac2fe5a`,
97 of 97 equal to the live S3 artifact.

## 2. Blast radius -- what the act may touch

Three movements of served output, and one change of key on the send path. Full text: ANNOUNCE, "BLAST RADIUS".

1. **WIDENS, on Andrew's word.** The one scoped identity gains ONE read-only tool, `opal_data_refresh_status`, on any
   client. Overlay rows 1 -> 2. Its consent stays 9 scopes. Rehearsal: admitted; 0 of 3 unnamed tools admitted.
2. **NARROWS.** The status tool and the send path's status read refuse a malformed `execution_id` before any request.
   Rehearsal: a refused id made 0 HTTP requests; the known execution read SUCCEEDED.
3. **ADDED.** `GET /rivalfunds/{day}/chart/{fund}`. Rehearsal on the staged bytes: 404 with its own body on a day with
   no chart, 400 on a bad fund, 401 with no viewer; `/rivalfunds/{day}` and `/audit` answered with the same status,
   size and digest as the installed code.
4. **The re-send dedupe key** becomes (name, size, content hash). A same-size corrected re-send now fires; an unreadable
   hash fires.

**Unchanged:** the S41 grant and the state store (0 writes); `.env`; every other identity, tool and route; Terraform, IAM,
the ALB, secrets. **Manifest:** `deployed_commit` moves; the previous value is `240ac2fe5a`.
**Rollback, one act for all:** redeploy `/c/tmp/og-rb20`.

## 3. Limits, disclosed

- **The dedupe rests on offline tests.** This project never runs a real send. Its first live exercise is the first
  corrected same-date re-send. The real shape of the drive item's `file.hashes` was not probed.
- **The route's 200 arm rests on `app/tests/test_rivalfunds_view.py`** (17 passed): 0 of 115 keys under the page prefix
  carry a chart object. The first live 200 is ETFS_RIVALS's to read after its publisher deploys.
- **The route arms run in-process on the host,** not through the ALB (row Z-W28-S6).
- **The concierge's token still carries its earlier 17 scopes** (row Z-W28-S11; `R37_STEP1_RECONSENT_READ_20261007.md`
  @2e96271d1f). The tool allowlist is the narrowing in effect. This release does not change that, in either direction.
- **Row Z-W28-S17:** about 50 older committed files carry the Schwab master account id. The r26 outputs are redacted.
  The older files are not part of this release and are not touched by it; the row is open for the slug.

## 4. Act and verify (Phase B steps 9-12, Phase D step 13)

**Preconditions, all three before any act:**
- the three halves SIGNED on `feddb37244`;
- the four ETFS_RIVALS commits on origin (Andrew's push word at `0.0.0_AB_MSTR~Z`; the CTO's condition, msg 30765);
- today's Bloomberg send confirmed served (the r25 timing rule: this release touches the send path).

1. Re-read live; if it moved, re-cut.
2. Open ledger `nfra-oplgtw-gateway-release-r26`, entry and sentinel committed before the act.
3. Run `r26_verify.sh before`.
4. Deploy from `/c/tmp/og-rel21` with `DEPLOY_BASE_REF=240ac2fe5abde944f15358ab563cb4b2ab63f09f`, by the issuer-serial
   halt-gate route (form step 10).
5. Run `r26_verify.sh after` immediately, then `r26_postdeploy.sh` (writes `RL12_ALLOW.json` and `RL12_FLOOR.json`).
6. **Rollback triggers:** the concierge not admitted for the status tool; an unnamed tool admitted; the consent count
   off 9; the tool count off 66; a floor read off its bar; any of `chart_404`, `chart_400`, `day_page_unchanged`,
   `audit_page_unchanged` off its value.
7. Run `rl12.AC1` and `rl12.AC2` against their `<expect>`. Both were exercised pre-GO with negative controls. The
   issuer re-grades both after the worker.
8. Drain-back: CLOUD already carries the 10 files, so the step is a check.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-07.**
- The act may touch exactly what section 2 names, plus the manifest.
- The rollback is pre-built and proven against the live artifact.
- Each named property has its writers counted and both branches stated in the ANNOUNCE.
- The limits of section 3 are disclosed.
- My reads in section 1 are independent of the worker's.

**CTO -- owed** (`1.0.0_SA_CTO~Z`).

**CVO -- owed** (`3.0.0_SA_CVO~Z`, required).
