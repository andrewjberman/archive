# NEVER-WIDEN -- COO HALF: the `opal-gateway` reads the path-component prefixes of a slash key as the UNION of the canonical and the legacy raw prefix (`HVST-ck-3`, round 96, workstream PATHKEY-RELEASE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~13:0xZ UTC. **Authority:** the CTO's round-95 analysis (`ledger/ROUND_ANALYSIS.round95.md` @031ac46589, msg 8025) section 3 item 2 and enrichment items 2 and 4 (readers on the path-component tools resolve to the canonical spelling and read the union of both prefixes, the canonical winning a same-name collision; each object served carries which spelling it came from; no rename, no delete; "ships as a gateway release on the live base plus the changed files only, the cj-3 shape, under its own pair, with site Z told first"). **Measurement:** `HVST-ck-1` (the census, re-run by me, byte-identical), `HVST-ck-2` (merged `5e026fa7f4`; AC1 `7 passed` and AC2 `75 passed` re-run by me; the read-only replay re-run by me, unchanged: `REPLAY-UNION-WHOLE cells=12 equal=12`).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`: cut a release branch `rel-amgt-harvst-ck3` FROM THE LIVE DEPLOYED COMMIT of `opal-gateway` (read three ways: `services.opal-gateway.deployed_commit` in `infra/aws/ec2/EC2_MANIFEST.json`, the commit the instance runs, and `/opt/opal-gateway/.deployed_commit`; all must read the same; the last report is `6575999df5d22c0123abfc0c88cd1c6f1efe8c96` (this seat's `HVST-cj-3`, deployed 2026-10-18 10:52:49Z; the ref `origin/rel-amgt-harvst-cj3`, which site Z lands in its round 43); any other value: STOP and tell the issuer, who writes a re-base addendum as for ap-40). Carry onto it ONLY these six paths, taken from `5e026fa7f4` (the merge of worker `~172`'s `ck-2`):

| path (under `infra/aws/ec2/opal-gateway/`) | status vs live | md5 at `5e026fa7f4` | md5 at live `6575999df5` |
|---|---|---|---|
| `app/harvest_research.py` | M | `42296ce22d5f5b811cf57019e07432a5` | `bae82b93332988673a8f2eeaa0d62ab9` |
| `app/harvest_figures.py` | M | `6fa6d895186fe313955a7cf948326000` | `ff7ec861c59320c64ba3eac21898d452` |
| `app/harvest_identity.py` | M | `cff484f5376f91b4255778d4d7b4a035` | `bca2e8d8ee91d5ea862522b8eef3f0fd` |
| `app/harvest_keys.py` | M | `72dc6f676f16982f39f56a3521877729` | `9c9e46822d213fb10517eeb12132c7a4` |
| `tests/test_cj6_slash_key_other_tools.py` | M (one test's two assertions) | `694921dc52fb240d32cfc22be34e51ab` | `ac6c6d1a90ff02c8a2daf98fded45a00` |
| `tests/test_ck2_path_component_union_read.py` | A (new) | `056e720f2cbe9694edf2761322ab8c43` | absent |

(The issuer read these md5s from `git show` at the stated commits; the five modified files at the pre-change base equal the live commit's, so the carried files apply clean on the live commit. Stat against live: 6 files, 573 insertions, 30 deletions.) Prove `git diff --name-status <live> rel-amgt-harvst-ck3` lists exactly those six paths (5 `M`, 1 `A`) and that each carried file's md5 equals the table; run the gateway tests on the release branch; deploy with `infra/aws/ec2/safe-ec2-deploy.sh opal-gateway` (`AGENT_NAME` set to the seat's serial, `DEPLOY_BASE_REF=<the live commit>` under the stale-base guard); read the served tools before and after.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is what the gateway's path-component tools serve for a key that contains a slash. **N = 1 resolver of the path-component prefixes of a slash key in the gateway app after this release:** `app/harvest_keys.py::path_component_reads` (with `union_rows` and `object_pick`), imported by `harvest_research.py`, `harvest_figures.py` and `harvest_identity.py`; before, each tool built its prefix from the caller's spelling. The rule that picks which prefix wins is the ruling: the canonical object wins a same-name collision; nothing is written. I read the full gateway diff (`git diff --stat 4b4d28e837 5e026fa7f4 -- infra/aws/ec2/opal-gateway/app`: 4 files).

## WHAT THIS CHANGES IN THE WORLD (named)

- **The tools changed (their path-component reads):** `harvest_get_research` (the management roster), `harvest_get_filing_analysis` (filings, drafting), `harvest_get_peers_and_scores` (peers, scores, posture), `harvest_get_fundamentals` and `harvest_query_columns` (the model block and its FYE form), and `harvest_security_coverage` (the keyed datasets and the packs ledger). Not changed: `publication-links/v1/<root>/` and `raw/seekingalpha/<cc>/` (derived from a key component; 0 objects under both spellings), the `security_key=` partition reads (round 95), `harvest_press.py`, `harvest_published.py`, `tools.py`.
- **For a key with NO slash (every security but two): nothing changes** (an arm of the new test asserts the same S3 calls and a byte-equal body; no `stored_spelling` field; the controls below read it live).
- **For the two slash keys `BP/_LN_Equity` and `NG/_LN_Equity`, in either spelling:** the tools read the canonical prefix and the legacy raw prefix and serve their union by name, the canonical object winning; the response gains a `stored_spelling` map saying which spelling each served object came from. **What the stored data shows (census `ck1_census.out`, re-run by me):** the raw spelling holds only names that the canonical spelling also holds (`raw_only=0` in every cell), so the SET of objects served does not grow; what changes is that a request in EITHER spelling now reaches the whole canonical set (before: `peers/v1/BP/_LN_Equity/` 7 objects against 10 under the canonical prefix; the model block 6 against 24; the coverage tool read the caller's spelling), and that four same-name pairs differ in bytes (peers `2026-09-24T2252Z.json`, `packs/<key>/input_ledger.json`, for BP and NG): **the canonical object, the newer one in all four, is now served in both spellings** (the legacy raw object is no longer reachable by name where a canonical one exists; it is not moved or deleted).
- **The service restarts:** `opal-gateway` serves every MCP tool for every principal on every box, about a minute; the seat states the window (start and end UTC) in the deploy ledger entry. **Not touched:** any S3 object, `tools.py`, `server.py`, any other app file, the mcportal bundle, Terraform, IAM, a scheduled task, the harvest runner.

## THE RISK AND ITS CONTROL

The live gateway moves under other fabrics' releases (site Z lands its round 43 `OG-ap-43`, which carries the live commit's parent and this seat's `6575999df5`). **The equality guard:** for each of the five modified files `git show <live>:<path>` must have the md5 of the last column; if any differs STOP, carry nothing, tell the issuer. **The CLOUD tip is NOT the cut** (the cj-3 rule stands: it carries other workstreams' gateway files). A second control: the stale-base guard (`DEPLOY_BASE_REF` equal to the live commit). A third: a slash-key request must return no LESS than before (Branch F).

## BOTH BRANCHES (the half is not signed unless it covers both)

- **Branch D (the diff, the tests, the reads and the counts PASS):** the deploy stands; the manifest records the new `deployed_commit` with the previous in `previous_deployed_commit`.
- **Branch F (the diff lists a path outside the six or a md5 differs, a test fails, a control read differs, a slash-key path-component read serves FEWER objects or a different canonical object than the stored canonical one, `/health` fails or the tool-name count differs):** if the cause is the deploy, roll back at once by redeploying `previous_deployed_commit` (read at the start, printed in `ck3_before.out`), read `/health` 200 and the tool-name count equal to the count before; the order stays `pending`; otherwise report the failure with the read.

## CONDITIONS

- **C-1.** The cut is on the live deployed commit, with the six-path diff, the md5 table and the equality guard printed; no CLOUD-tip commit is carried.
- **C-2.** A deploy ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2; `org/critical_paths/.open_deploys/harvst-ck3-gateway-union-read-release.json` and `change_management/`), naming the one service, the restart window and `previous_deployed_commit` as the rollback.
- **C-3.** The tests pass on the release branch before the deploy: the eleven files of `HVST-ck-2`'s AC2 (75 tests) plus `test_ck2_path_component_union_read` (7): 82 tests expected. `test_og_gt8` fails before and after (row `D1-W171-S8`); it is NOT a gate; the seat prints its result before and after as a no-change control.
- **C-4.** No Terminal, queue or Bloomberg use; NO call of `etfs_compare_peers` on the gateway; no model call.
- **C-5.** The served reads run through the gateway as an Opal principal and are recorded verbatim with `as_of` and `source_keys`.
- **C-6.** The MCP tool-name count and `/health` are read BEFORE and AFTER, on both branches, and are equal.
- **C-7 (controls: nothing moves for a key without a slash).** `harvest_get_research` for `UNH_US_Equity`, `CPA_US_Equity`, `KMB_US_Equity` and `MNST_US_Equity` with `fields` `["fund_of_record","last_stated_position"]`, `harvest_get_peers_and_scores` and `harvest_get_filing_analysis` and `harvest_security_coverage` for `UNH_US_Equity`, and `harvest_get_fundamentals` for `UNH_US_Equity` (kinds consensus, reference, valuation_history, segments, price), read BEFORE and AFTER: every returned entry, key, `content_sha256`, `as_of` and `source_keys` EQUAL, and no `stored_spelling` field in any of them.
- **C-8 (the proof, CTO analysis section 3).** After the deploy, for `BP/_LN_Equity`, `BP-SLASH-_LN_Equity`, `NG/_LN_Equity` and `NG-SLASH-_LN_Equity`: (i) `harvest_get_peers_and_scores` returns the SAME peers object for the raw and the encoded request (same `object_key`, same `member_count`; 10 canonical objects exist, the newest is served), with `stored_spelling` naming the spelling of each part; (ii) `harvest_security_coverage` returns the SAME `objects` count per dataset for the raw and the encoded request (row `D1-W171-S6` closes when they are equal: the replay reads BP 41 and 41, NG 39 and 39); (iii) `harvest_get_filing_analysis` and `harvest_get_fundamentals` (kind model) return the same record for both spellings; (iv) the research record of round 95 (dossier, continuation, ai_fill, reports, roster) is STILL whole. Anything less: Branch F.
- **C-9 (host owner told first).** After the cut and before the deploy the seat writes `ck3_hostowner_note.out` (release commit, the six paths, the intended window start and end UTC, the rollback) and tells the issuer; the issuer sends it to site Z through `0.0.0_AB_MSTR~DELL1` and sends GO; the deploy waits for that GO and for the host owner's answer; an in-flight release on the host in the window (including site Z's round 43) is a STOP.
- **C-10 (the commit reaches the shared lineage).** Right after the deploy the issuer asks `0.0.0_AB_MSTR~DELL1` to push the release ref and tells site Z to land it with the round-43 batch.

## ROLLBACK

Redeploy `previous_deployed_commit` from `EC2_MANIFEST.json` through the same script; no data is written by the act.

## WHAT THIS DOES NOT COVER

The writer of the raw spelling found by `HVST-ck-4` (the `pull_enqueue` Lambda; a Terraform act of its own); a migration of the legacy objects to one stored form (the CTO proposes it only after a census shows it would lose nothing); `publication-links/v1` and `raw/seekingalpha`; any slash key other than the two; the standing red `test_og_gt8`; the stale comments left in `test_cj6` arm 3 (`D1-W172-S8`).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
