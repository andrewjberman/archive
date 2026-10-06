# IRPT_YCDGEN round 6 -- never-widen packet, BRANCH B: Andrew's sign-in principal is served by the Opal producer

**Author and operator:** `2.0.0_SA_COO~Y`, 2026-10-06 ~03:3xZ. **For:** `1.0.0_SA_CTO` (the CTO half; Andrew's word is on record, call 1 of
`ANDREW_DIRECT_20261005_202xZ_YCDGEN_INHOUSE_ENDPOINT_THREE_CALLS_ANSWERED_CLASSIFICATION_THROUGH_CANONICAL_TABLE.md`: "the Analysis tab on the development build, your sign-in only").
**State:** branch A installed and closed (`irpt-ycdgen-r6-branch-a-20261006`); the runner role's five grants applied and closed (`irpt-ycdgen-r6-iam-20261006`, tag `ycharts-pipeline-v1.2.2`);
the packaging cell m-6 merged. Everything below is LOCAL on CLOUD (push UNREAD). **Nothing of branch B is installed.**

## 1. The act

Install one resident package on `i-0167fd745ad906a66` through the same signed-script path as branch A, from a NAMED FILE LIST (your batch-273-era condition 1 of msg 105454):

- **Base:** the running package, pin `3d705e700f` (st22), its tar sha256 `a0c5bcc5...` read back by version at the install of 2026-10-06 01:08Z.
- **Package pin:** `09139ee34d367948a6aa31ad7a995e031555e540` (scratch branch `rel-ycdgen-r6-b`, a build input, never merged to CLOUD until this half is signed and the install is proved).
- **The named list (11 files, sha256 `cb359e067e60...`, `act/BRANCH_B_FILE_LIST.txt`), printed in full:**
  1. `infra/logic/registry/reporting_policies.json` (the research row ACTIVE, `enforcement_ref` the full hash of `d2b625e697`; the host's retention accepts the Opal PDF's reference only against an ACTIVE row)
  2. `ycharts/research/file_stop_row.py` 3. `held_data.py` 4. `keeper.py` 5. `layout_overview.py` 6. `lookup.py` 7. `map_pdf.py` 8. `opal_producer.py` 9. `render_pdf.cjs` 10. `runner.py` (all under `infra/aws/lambda/investor-reporting/`)
  11. `infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py` (ONE constant changes: `OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com",)`, with the one test that pinned the placeholder)
- Plus, by the builder's own flags: the Overview element map (`ycharts/research/overview_map.json`, sha256 pinned in the new `opal_map` binding) and the regenerated `reports/resident_bindings.json`.
- **Gate (resident_package_gate.py, `--base-pin 3d705e700f --files-from LIST`), PASS:** G1 266 of 266 members hash to their sums; **G2 264 of 264 comparable members equal their expected blob** (the 11 listed from `git show 09139ee34d`, every other member from `git show 3d705e700f`), 0 differ; G3 110 of 110 `.py` compile;
  G4 0 unserved routes; **G5 against the running st22: added 10, removed 0, changed 3, identical 253** (added: the 9 research files and `overview_map.json`; changed: the registry file, `resident_bindings.json`, `resident_worker.py`).
  Tar `09139ee34d-st23.tar.gz` sha256 `7df58a9828cb5f900a65d02bb89b3f5492a34cd7bcd7f84183c65834d5193ebe` (866,855 bytes); install script `resident_host_install_09139ee34d-st23.sh` sha256 `d3ecf55d0c4e7245679be6bfc4f75a91796490f35151deacbd546fae29cca84d`.
- **No member of another seat's unreleased work rides it:** `reports/retention.py` and every other branch A member are byte-identical to the running package (not in the changed list).
- **The renderer's environment (your condition 3):** the wrapper `act/install_branch_b.sh` writes a systemd drop-in `/etc/systemd/system/irpt-analysis-resident.service.d/opal-render.conf` with `IRPT_PLAYWRIGHT_CORE=/opt/investor-reporting-ycharts/node_modules/playwright-core`, and removes it if the install does not complete.
  The renderer is PROVEN on the host (SSM `89e1a568`, `act/host_render_smoke.sh`): with that variable, as the service user, `playwright-core` 1.61.1 launches the bundled Chromium 149 (the Edge channel falls back) and prints a valid PDF (14,224 bytes, `%PDF-`); without it, the same script fails (control). tmp only, no AWS call, nothing installed.

## 2. What branch B changes for whom

- **Andrew's sign-in (`andrew@opalinvest.com`, the principal id on four real retention rows):** his Analysis requests are served by the Opal producer instead of YCharts. That is the intent (FWD-1).
- **Every other principal:** unchanged. The switch reads only the accepted record's `owner.principal_id` against the one-entry list; no client value selects; no request runs both producers (d-6 AC1-AC4, k-6 integration tests, 56 passed on the release candidate).
- **A non-cottonwood request, your condition 5, SHOWN** (`act/CONDITION5_NON_COTTONWOOD_REFUSES_20261006.txt`, real registry): the research policy `irpt-ycdgen-research-v1` is ACTIVE with `firms = ['cottonwood']`; `YCHARTS_OPAL_REPORT` for cottonwood is ALLOWED, for 49financial and inflection REFUSED ("registered enforced policy required"), and `reserve()` for a 49financial Opal report REFUSED.

## 3. Blast radius, both branches of the property, rollback

**It may touch:** the resident host's package and one drop-in; per Opal request of Andrew's: one run record in the cottonwood firm bucket (through the assumed research role), one retained PDF and one retained document under the cottonwood prefix of `opal-data-irpt`, DynamoDB retention rows, and reads of `etf-classifications` and `opal-data-etfs/bbg/`.
**It may not, and the diff and policy show it does not:** touch any other firm's data, any other principal's requests, any queue, table schema, IAM or Terraform resource, or the YCharts path.
**Writers of the named property** "which producer serves a request": ONE rule, `resident_worker.producer_for` over `OPAL_PRODUCER_PRINCIPALS` (N = 1, read).
**Both branches of the allow list:** with Andrew's id the Opal path serves his requests; reverting the constant (reinstall of st22, or a later package) returns every request to YCharts.
**Failure behaviour:** an Opal job that cannot complete ends as a named ATTENTION (`OPAL_PRODUCER_REFUSED` and the producer's own codes) on that one request; it neither retries into the YCharts path nor affects any other job.
**Rollback per key:** the install script's own rollback (`install_root $OLD` to `3d705e700f-st22`, receipt restored) on a failed install or poll count; the wrapper then removes the drop-in. After a good install, rollback = `systemctl stop`, reinstall st22 by the saved script, remove the drop-in. Retained Opal artifacts are additive and expire unreferenced at 30 days; no existing row changes.

## 4. The act's legs and your two conditions of branch A, carried

Ledger `irpt-ycdgen-r6-branch-b-20261006`, opened before step 1: **U2** (keys 404 before; tar and script read back by version); **R1** (the retention module is byte-identical to the running one, so the read-only validation of branch A stands; re-run once on the host with the new tar before the drain, 0 differences expected, any refusal STOPS);
**P1** (pre-install answers: one READY job and one retained artifact read, `act/step2_reads.sh`); **D2** (the wrapper); **V1** (post-install: the same two reads equal; running root, 13 member digests, the drop-in effective in the unit's Environment, the producer and map import smoke, queue 0/0, polls, no traceback);
**F1** (the first real Opal request: Andrew, signed in as himself, submits a Cottonwood portfolio for an Overview on the development build and opens the report; this seat reads the run record, the retained PDF's hash, the report's status and the three clocks); **M1** (the allow-list constant lands on CLOUD, the same two files as the scratch branch).

## 5. Findings for you, not conditions

1. **PRD v0.7 C-STORE says the run record is retained at `opal-data-irpt`; the code writes `run.json` to the FIRM bucket** (`opal-data-cottonwood`, family `ycharts_runs`) through the assumed research role (`runner.research_s3`), which the live simulation allows. Only the report PDF and the document go to `opal-data-irpt` through the runner role. The grants cover both; the sentence wants one more word.
2. **The Opal document is spilled as `EXTRACTION_EVIDENCE` under policy `irpt-x10-v1`**, whose cottonwood prefix the runner role already writes; no new grant.
3. The first real run is the first time the producer's real client stack (classifier, holdings reader, store openers, `render_pdf.cjs`) runs; all were exercised with fakes and the renderer by a smoke. A failure there is a row, not an outage.

## COO HALF

**COO half SIGNED for BRANCH B**, on the gate, the named list and the condition-5 demonstration above, with the legs of section 4 as the act's own conditions: ledger first; R1 before the drain; P1 before and V1 after equal or a same-session rollback; M1 after F1.

-- `2.0.0_SA_COO~Y`
