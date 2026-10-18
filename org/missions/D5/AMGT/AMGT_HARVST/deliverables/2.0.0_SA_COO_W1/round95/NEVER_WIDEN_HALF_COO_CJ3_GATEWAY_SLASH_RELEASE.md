# NEVER-WIDEN -- COO HALF: the `opal-gateway` reads a slash key from its one stored form in the research, filing, peers, fundamentals, bestdata and coverage tools (`HVST-cj-3`, round 95, workstream SLASH-RELEASE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~08:5xZ UTC. **Authority:** the CTO's round-94 analysis (`ledger/ROUND_ANALYSIS.round94.md` @428b762698, msg 7946) item 1 (the gateway's harvest tools normalize the requested key; `BP/ LN` and `NG/ LN` return the full record whichever form is requested) and his rule for the release (msg 7978, which supersedes his msg 7975 cut line: "cut on `aa2efa2cf3`, the live base, plus exactly the 7 cj-2 and cj-6 files, the way `cg-3` did; `DEPLOY_BASE_REF=aa2efa2cf3`; the pair lists those 7 with the md5 proof for the 3 modified files; push the release ref to the shared lineage and tell site Z first"). **Measurement:** `HVST-cj-1` (merged `bc1f5233ec`), `HVST-cj-2` (`c692c5dfbb`), `HVST-cj-6` (`34fb405b29`), each re-run by the issuer: offline tests, and read-only replays of the changed code against the stored objects.

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, AFTER its ledger `harvst-cj4-dossiers-nonslash` is CLOSED and COMMITTED: cut a release branch `rel-amgt-harvst-cj3` FROM THE LIVE DEPLOYED COMMIT of `opal-gateway` (read three ways: `services.opal-gateway.deployed_commit` in `infra/aws/ec2/EC2_MANIFEST.json`, the commit the instance runs, and `/opt/opal-gateway/.deployed_commit`; all must read the same; the last report is `aa2efa2cf3dee82030c00f85425f686132adcf4a`, site Z's batch 8 closed 07:01:17Z, scratch ref `origin/rel-nfra-og-live-aa2efa2cf3`; any other value: STOP). Carry onto it ONLY these seven paths, taken from `34fb405b29`:

| path (under `infra/aws/ec2/opal-gateway/`) | status vs live | md5 at `34fb405b29` | md5 at live and at the pre-change base `845b69a8cc` |
|---|---|---|---|
| `app/harvest_research.py` | M | `bae82b93332988673a8f2eeaa0d62ab9` | `596c299597067fe5a8afb8e3493a0ed9` |
| `app/harvest_figures.py` | M | `ff7ec861c59320c64ba3eac21898d452` | `610eb6862918d2c6695c10d2de58734f` |
| `app/harvest_identity.py` | M | `bca2e8d8ee91d5ea862522b8eef3f0fd` | `9c8d1fd69ffe0594968b4acd2751fba9` |
| `app/harvest_keys.py` | A (new) | `9c9e46822d213fb10517eeb12132c7a4` | absent |
| `tests/test_cj2_slash_key_one_form.py` | A | `0ba8b830e816da844f7ec9fc4f9020d7` | absent |
| `tests/test_cj6_slash_key_other_tools.py` | A | `ac6c6d1a90ff02c8a2daf98fded45a00` | absent |
| `tests/fixtures/cj2_continuation_keys.txt` | A | `7a8fe09fbb0648435d76b01cd06a22c0` | absent |

(The issuer read the md5s from `git show` at the stated commits; the three modified files are byte-equal at live and at `845b69a8cc`, so the carried files apply clean on the live commit.) Prove `git diff --name-status <live> rel-amgt-harvst-cj3` lists exactly those seven paths (3 `M`, 4 `A`) and that each carried file's md5 equals the table; run the gateway tests on the release branch; deploy with `infra/aws/ec2/safe-ec2-deploy.sh opal-gateway` (`AGENT_NAME` set to the seat's serial, `DEPLOY_BASE_REF=<the live commit>` under the stale-base guard); read the served tools before and after.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is what the gateway's harvest tools serve for a key that contains a slash, and the key the tools print. **N = 1 resolver of a slash key in the gateway app after this release:** `app/harvest_keys.py::canonical_security_key` (with `slash_safe_key`), imported by `harvest_research.py`, `harvest_figures.py` and `harvest_identity.py`; before this release the gateway had none (every tool built prefixes from the raw key). The rule is the module rule of `lib/research/identity/crosswalk.py` (the deployed artifact cannot import it: `deploy-to-ec2.sh` ships only `lib/trading_calendar.py` and `lib/opal_naming.py`), carried as a copy guarded by the equality arm of `test_cj2_slash_key_one_form.py` over 105 keys (row `D1-W171-S3`, ARMED, the CTO decides whether the module moves). I read the diff (`git diff --stat 845b69a8cc 34fb405b29 -- infra/aws/ec2/opal-gateway`: 7 files, 919 insertions, 51 deletions).

## WHAT THIS CHANGES IN THE WORLD (named)

- **The tools changed (their entry computes the canonical key):** `harvest_get_research`, `harvest_get_filing_analysis`, `harvest_get_peers_and_scores` (research module), `harvest_get_fundamentals` (the kinds consensus, reference, valuation_history, segments and price), the bestdata query, and `harvest_security_coverage`. `harvest_press.py` and `harvest_published.py` are unchanged.
- **For a key with NO slash (every security but two): nothing changes** (an arm asserts every prefix and every body byte-equal; the controls below read it live).
- **For the two slash keys `BP/_LN_Equity` and `NG/_LN_Equity`, in either spelling:** `harvest_get_research` returns the dossier, continuation, ai_fill, reports and exec_officers (today the raw spelling returns the reports and nothing else, the encoded one everything but the reports: the replay reproduces both halves); the fundamentals kinds, the bestdata query and coverage read the partition form (the raw request, which reached 0 objects, now reaches the same objects as the encoded one; `price` reached 0 in BOTH spellings and now reaches 1). **The key a tool prints is the canonical raw key** (`BP/_LN_Equity`) whichever spelling was requested.
- **NOT changed, by design:** the path-component prefixes (`peers/v1`, `posture/v1`, `scores/v1`, `filings/v1`, `drafting/v1`, `management/v1`, `derived/model_block`, `publication-links/v1`) keep the caller's spelling: they hold BOTH spellings and the CTO decides (rows `D1-W171-S4` and `-S6`); so `harvest_get_peers_and_scores` and the filing and coverage path reads of the two keys behave as today.
- **The service restarts:** `opal-gateway` serves every MCP tool for every principal on every box, about a minute; the seat states the window (start and end UTC) in the deploy ledger entry. **Not touched:** any S3 object, `tools.py`, `server.py`, any other app file, the mcportal bundle, Terraform, IAM, a scheduled task, the harvest runner.

## THE RISK AND ITS CONTROL

The live gateway moves under other fabrics' releases (it moved to `aa2efa2cf3` on 2026-10-18 07:01Z). **The equality guard:** for each of the three modified files `git show <live>:<path>` must have the md5 of the last column; if any differs STOP, carry nothing, tell the issuer. **The CLOUD tip is NOT the cut** (the CTO's msg 7978): `git diff --name-status aa2efa2cf3 origin/CLOUD -- infra/aws/ec2/opal-gateway` lists 35 files of which 28 are other workstreams' (`server.py`, `destructive_ops.py`, `family_depth.py`, `probe_listener.py`, `admin_people_access.py`, `refs/*.json`, routing and test files) and a CLOUD-tip cut would ship them under this pair. A second control: the stale-base guard (`DEPLOY_BASE_REF` equal to the live commit).

## BOTH BRANCHES (the half is not signed unless it covers both)

- **Branch D (the diff, the tests, the reads and the counts PASS):** the deploy stands; the manifest records the new `deployed_commit` with the previous in `previous_deployed_commit`.
- **Branch F (the diff lists a path outside the seven or a md5 differs, a test fails, a control read differs, a slash-key read does not return the whole record, `/health` fails or the tool-name count differs):** if the cause is the deploy, roll back at once by redeploying `previous_deployed_commit` (read at the start, printed in `cj3_before.out`), read `/health` 200 and the tool-name count equal to the count before; the order stays `pending`; otherwise report the failure with the read. A read of a slash key that returns LESS than before is a Branch F.

## CONDITIONS

- **C-1.** The cut is on the live deployed commit, with the seven-path diff, the md5 table and the equality guard printed; no CLOUD-tip commit is carried.
- **C-2.** A deploy ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2; `org/critical_paths/.open_deploys/harvst-cj3-gateway-slash-release.json` and `change_management/`), naming the one service, the restart window and `previous_deployed_commit` as the rollback.
- **C-3.** The tests pass on the release branch before the deploy: the nine files of `HVST-cj-6`'s AC2 (`test_ce3_parts_absent_wording`, `test_cd1_dossier_misfiled`, `test_cc1_model_basis`, `test_cc2_research_misfiled`, `test_cc3_ticker_shaped_never_exact_on_name`, `test_og_gt1`, `test_og_gt3`, `test_og_gt4`, `test_cg4_report_fund_relation`) plus `test_cj2_slash_key_one_form` and `test_cj6_slash_key_other_tools`: 75 tests expected (48 + 8 + 19). `test_og_gt8` fails before and after any change here (row `D1-W171-S8`: it reads `deploy-to-ec2.sh`); it is NOT a gate; the seat prints its result before and after as a no-change control.
- **C-4.** No Terminal, queue or Bloomberg use; NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`); no model call.
- **C-5.** The served reads run through the gateway as an Opal principal and are recorded verbatim with `as_of` and `source_keys`.
- **C-6.** The MCP tool-name count and `/health` are read BEFORE and AFTER, on both branches, and are equal.
- **C-7 (controls: nothing moves for a key without a slash).** `harvest_get_research` for `UNH_US_Equity`, `CPA_US_Equity`, `KMB_US_Equity` and `MNST_US_Equity` with `fields` `["fund_of_record","last_stated_position"]`, and `harvest_get_fundamentals` for `UNH_US_Equity` (kinds consensus, reference, valuation_history, segments, price), read BEFORE and AFTER: every returned entry, key, `content_sha256`, `as_of` and `source_keys` EQUAL. (They are read after `HVST-cj-4`'s ledger closed; nothing writes these objects during the act.)
- **C-8 (the proof, CTO msg 7946 item 1).** After the deploy, `BP/_LN_Equity`, `BP-SLASH-_LN_Equity`, `NG/_LN_Equity` and `NG-SLASH-_LN_Equity` through `harvest_get_research` each return the dossier (a `dossier_key`), the continuation (a `continuation_key`), the ai_fill (`ai_fill_key`), at least one `research_reports[]` entry and the exec-officer roster, recorded verbatim; the BEFORE reads of the same four (step 0) show the two halves. `harvest_get_fundamentals` (kind consensus) for `BP/_LN_Equity` returns the same object as for `BP-SLASH-_LN_Equity`. Anything less: Branch F.
- **C-9 (host owner told first).** After the cut and before the deploy the seat writes `cj3_hostowner_note.out` (release commit, the seven paths, the intended window start and end UTC, the rollback) and tells the issuer; the issuer sends it to site Z through `0.0.0_AB_MSTR~DELL1` and sends GO; the deploy waits for that GO and for the host owner's answer; an in-flight release on the host in the window is a STOP.
- **C-10 (the commit reaches the shared lineage).** Right after the deploy the issuer asks `0.0.0_AB_MSTR~DELL1` to push the release ref and tells site Z to land it on its gateway lineage.

## ROLLBACK

Redeploy `previous_deployed_commit` from `EC2_MANIFEST.json` through the same script; no data is written by the act.

## WHAT THIS DOES NOT COVER

The path-component tools (peers, posture, scores, filings, drafting, management, model block, publication links); whether the module moves where the deployed artifact ships it; any slash key other than the two; the `tools.py` notes (site Z's); the standing red `test_og_gt8`.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
