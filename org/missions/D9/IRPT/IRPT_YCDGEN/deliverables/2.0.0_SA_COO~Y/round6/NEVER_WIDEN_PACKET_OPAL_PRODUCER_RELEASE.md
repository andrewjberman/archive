# IRPT_YCDGEN round 6 -- never-widen packet: the Opal producer's release through IRPT_BCKEND's path

**Author:** `2.0.0_SA_COO~Y`, 2026-10-06 ~00:4xZ. **For:** `1.0.0_SA_CTO` (the CTO half) and `2.0.0_SA_COO~P` / the IRPT_BCKEND release path (the installer).
**State:** every cell is merged on local `CLOUD` (LOCAL, not pushed; push state UNREAD at writing). **Nothing is deployed.** The portal cells (e-6, j-6) are a separate review.
**Conditions answered:** RULINGS batch 269 (msg 105429), items 1-6; YCD-g-6 condition 2 (msg 105423).

## 1. What moves, by merge (all under `infra/aws/lambda/investor-reporting/` unless noted)

| cell | merge | files it wrote | what it does |
|---|---|---|---|
| s-6 | 24bbe559eb (+9f56c40993) | `_contracts/AnalysisReport.v2.schema.json`, four fixtures, `_contracts/tests/test_analysisreport_v2.py` | the v2 form of AnalysisReport (provider discriminator); v1 untouched |
| b-6 | 9cbfbf2215 | `ycharts/research/layout_overview.py` (+ test) | classification through the one client; weights from amounts; no pricing |
| a-6 | 7e31aaa7b1 | `ycharts/research/opal_producer.py` (+ test) | reads accepted holdings, renders, writes run.json v2 and the v2 document |
| h-6 | f2b8972f9b | `layout_overview.py` (+ test) | the Opal page names no vendor under pricing off |
| c-6 | e30b93afa8 | `ops/owned_report.py` (+ test) | the server reads the Opal form; v1 still refused without its vendor members |
| g-6 | a9c65fa1b3 | `reports/resident_installed.py`, `ycharts/generate/publisher.py`, `publication_worker.py` (+ tests) | persists the Opal form and reaches READY; the vendor path unchanged |
| d-6 | 3b16f00db3 | `ycharts/generate/resident_worker.py` (+ test) | the producer switch by principal against an allow list (C-SWITCH) |
| i-6 | 14eb4d115d | registry, `lib/tests/test_irpt_destination.py`, producer, publisher, worker | retained PDF; the Opal document spills out of the checkpoint |
| l-6 | 6e4e325b5d | registry, `lib/tests/test_irpt_destination.py`, `reports/retention.py`, `repository.py`, `composition.py` (+ tests), producer, publisher | the batch-269 rework: v1 policy bytes restored; retention resolves the policy from the reference's `policy_revision` |
| k-6 | d2b625e697 | `reports/resident_installed.py`, `resident_worker.py` (+ tests), `ycharts/generate/tests/test_opal_thread_integration.py` | the installer supplies the Opal stores; the whole path proved with fakes |
| e-6, j-6 | workspace 2b01d10976, 1785e50b03 | portal commits `81bbeba2`, `cd3924d5` on portal branches, **not landed** | the Analysis tab reads the Opal form (separate CTO review) |

## 2. BLAST RADIUS (what the act may touch) and what it may not

**The act:** build one package of the files above, install it on the dedicated resident host (`i-0167fd745ad906a66`) through `ycharts/generate/install-resident.sh` after a controlled drain
of `irpt-analysis-resident.service`, and add one pinned binding `opal_map` (the Overview element map, `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json`, with its sha256).

**It may touch:** the resident package's code; the resident bindings file (one new optional key); retention-reference validation code used by every report read (`reports/retention.py`, `repository.py`).
**It may not touch, and the diff shows it does not:** the queue, the jobs table, the requests table, IAM, any schedule, the deployed registry (the `irpt-x10-v1` policy reads byte-identical, section 4), any stored retention row, any existing report, any stored document of any firm, the YCharts producer's code path.

**Both branches of the allow list.**
- **Branch A (ships this way): the allow list holds the inert placeholder** `PRINCIPAL_ID_TO_BE_SET_BY_ISSUER`. No real principal is on it, so the Opal path is unreachable. Behaviour for every request equals today's, except the retention-resolution and publisher/validator code now run on every read and write; section 4 is the evidence those are unchanged for v1.
- **Branch B (a separate act, on Andrew's word):** a one-line edit sets Andrew's sign-in principal id in `OPAL_PRODUCER_PRINCIPALS`, and the resident is restarted. Then only his requests are served by the Opal producer, which writes retained artifacts under `irpt-ycdgen-research-v1` and the firm bucket and reads `etf-classifications`. The list changes only on his word (C-SWITCH).

**Rollback per key.**
| what | rollback |
|---|---|
| resident package | `systemctl disable --now irpt-analysis-resident.service`, reinstall the previous package (retain its path and SHA256SUMS before the drain); the queue, accepted inputs and intents persist (the script's own header) |
| allow list | set it back to the placeholder and restart |
| `opal_map` binding | remove the key; the Opal path then refuses with `OPAL_STORES_REQUIRED`, never serving a YCharts request wrongly |
| retained Opal artifacts / Opal documents written during branch B | additive; the family is unreferenced-expiring (30 days); no existing row is rewritten, so nothing needs undoing |
| registry | nothing deployed: the v1 policy is byte-identical and `irpt-ycdgen-research-v1` stays PENDING_ENFORCEMENT until the CTO accepts it |

## 3. Writers of the named properties (N printed)

The property "a retained reference validates" is written by ONE rule, `reports/retention.py` (`_registered`, `require_live`); `~P`'s lane; one writer this round (a scan of 4,241 task-order files found no other non-terminal order naming it).
The property "a persisted report document is shaped" is written by TWO rules, the vendor key set and the Opal key set in `publisher.py`/`publication_worker.py` (`metadata_kind`), which refuses a request carrying both. N = 2, both read at signing.

## 4. Evidence the YCHARTS path is unchanged (batch 269 item 4; g-6 condition 2)

- `infra/logic/registry/reporting_policies.json`: `git diff e923e0f463^ HEAD` over the file is 0 lines (byte-identical to before i-6); `opal_naming.reporting_policy('irpt-x10-v1')['policy_sha256']` = `e0046398e23951451498c0fcfec29154db5b26d4c70d80c4121f50fd3dfc8c85`, the value the CTO's ruling names, printed from the built registry at HEAD.
- Existing retention tests: 18 pass untouched (`reports/tests/test_retention.py`, 21 passed with 3 new). A v1 reference validates exactly as before (`-k v1_reference_validates_unchanged`); an unregistered or non-ACTIVE revision is refused.
- v1 document persistence: g-6 AC2 and AC6 and i-6 AC5 (`-k v1_document_persists_byte_equal`) pass; the pinned digest also passes against an unmodified copy of the pre-change publisher (g-6 worker).
- Whole directories on the merged tree: `ycharts/research/tests`, `ycharts/generate/tests` (resident worker 53 passed, 8 skipped, the 8 pre-existing), `reports/tests`, `ops/tests`, `_contracts/tests` all pass; `lib/tests/test_irpt_destination.py` 73 passed.
- **NOT DONE, owed before the release (item 4, first limb):** one stored v1 retention row read from the LIVE index validating under the new code (a read, no write). I have not made that read; the live index and its principal need the resident host's role or a read grant. It is named here, not claimed.

## 5. Open items that gate or ride with the release

1. **Row IRPT_YCDGEN-W1-S13:** the installed home of the Overview element map (the `opal_map` binding above) and one real exercise of the two default openers (`layout_overview._default_classifier`, `runner.research_s3`) at the close run.
2. **Item 5:** `irpt-ycdgen-research-v1` goes ACTIVE only on the CTO's acceptance. The row, as it stands: policy `irpt-ycdgen-research`, firm `cottonwood`, families `YCHARTS_RESPONSE`, `YCHARTS_RUN`, `YCHARTS_OPAL_REPORT`; `enforcement_ref` is null today. Proposed enforcement revision: `d2b625e697` (the merge that completes the code resolving a reference's own revision: `reports/retention.py` at `6e4e325b5d` and the installer wiring at `d2b625e697`). Branch A does not need it ACTIVE (no Opal reference exists); branch B does.
3. **The resident host's IAM** (read `etf-classifications`; write the retained families and the firm bucket) is proved only by one real run under branch B; `comp-iam` cannot see a non-Lambda role.
4. **Row W3-S16 and W2-S13 and W4-S7/S8:** inert contract and portal items carried to the CTO (the analysis-report response schema needs a v2 sibling; the endpoints client path; a zero-section Opal report renders v1 wording).
5. The portal cells land on DEV after the CTO's review, as a separate act.

-- `2.0.0_SA_COO~Y`
