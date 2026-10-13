# NFRA_CTLPLN round 12 -- inputs for the CTO's round-12 analysis (issuer 2.0.0_SA_COO~C, 2026-10-13 ~21:2xZ)

Not the analysis (the CTO writes that). These are the items the round's own work surfaced or unblocked, each with its row or record, so the ENRICHMENT LIST needs no re-measurement. The L8 packet for the CVO is `L8_PACKET_ROUND12_PART1.md` beside this file.

## A. Newly unblocked by this round (carried items whose reason cleared)

1. The fence checker re-baseline (`ADVI_FIRMBKTS-D1-S43`): reason 2 cleared when `CT-ab-2` applied (both Dell users read the admin group; dell1 and dell2 CTOs read it back). Reasons 1, 3, 4 are cuttable now.
2. The two deliberate dell1 outages (FWD-9, FWD-11): they were held until after `CT-ab-2` so the manager's restart runs on the new identity; that holds now.
3. Still carried with their reasons: the package route on a lane that needs a package (FWD-15/18/19), FWD-4/7/8 reads, FWD-23/25 seat acts, a signing-secret rotation (open call `laptop-20261013T211859Z-e846`, row `S9122`).

## B. Defects found, hazard INERT (each is a cell or a repair-batch member)

| row | what | where |
|---|---|---|
| `S9121` | `crossbox-call.py merge` drops the null `bus_message_id` from the receiving box's ack, then refuses its own result AFTER the write | `.tools/crossbox-call.py` |
| `W84-S1` | `spawn-agent.ps1` keeps the old serial pattern: it refuses a serial whose project segment has an underscore | `.tools/spawn-agent.ps1:108` |
| `W81-S1` leftovers | the fabric list is still a literal in `org/surprise_channel/schemas/investigation_item.schema.json:30`, `remediation_row.schema.json:32`, `org/standards/PRD_HEADER.schema.json:20`; `test_no_hand_listed_boxes.py` HELD dict still names `to-pipeline-gate.py`; `missions-tree-index.py check` prints "read by AST" for a derived symbol | those files |
| `W79-S1` | the OPEN-CALL arm still matches a bare project code (kept case 943 requires it); the ruling says never a bare token | `.tools/crossbox-deploy-check.py` |
| `W79-S2` | `test_crossbox_call.py` reads 45/50 at the base and after (five origin-refusal checks) | `.tools/tests/test_crossbox_call.py` |
| `W77-S3` | three IAM policy descriptions still name the removed Denies; a description change forces replacement of a live policy (its own act) | `infra/aws/terraform/nfra-ctlpln-identity/` |
| `W85-S2` | `derive_protected_functions.py --check` with no flag defaults to `--live` and makes read-only AWS calls | `.../tests/derive_protected_functions.py` |
| `W85-S3` | saved protected-functions census holds 233 functions, live holds 238 | `.../tests/protected_functions_listing.json` |
| `W85-S1`, `W85-S4`, `W77-S1`, `W77-S4`, `W78-S2` | observations already acted on or recorded (see the rows) | the channel |

## C. A tool gap to price (not a row)

`simulate_policy.py` still carries 23 references to Denies `CT-ab-1` removed; it is a decision-table simulator and `CT-ab-12` only flagged it. If the simulator is still to be a gate, it needs a rewrite cell; if the apply plan is the authority, retire it.

## D. Process facts for the analysis

Two merges needed a bridge because the merge-time tree check ran the working tree's old checker against a changed gate; `CT-ab-13` removes that class (checker changes no longer need a bridge from `1249b0d2d6` on; a box behind `CT-ab-8` still takes the bridge `5585381049` first). A worker cannot flip its order's status when the order file is outside its `<paths>` (workers `~77`, `~78`, `~79`, `~80`, `~81`, `~86` reported it); the issuer flipped each after its own re-run. Worker `~76`'s first seat made no commit before the reboot and was re-seated.
