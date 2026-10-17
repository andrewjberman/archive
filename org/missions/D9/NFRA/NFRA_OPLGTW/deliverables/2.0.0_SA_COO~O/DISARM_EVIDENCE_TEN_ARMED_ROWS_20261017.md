# NFRA_OPLGTW -- disarm evidence for ten ARMED rows (2.0.0_SA_COO~O, 2026-10-17 ~01:5xZ)

The disarm owner of each row below is `2.0.0_SA_COO~O`. Each row was dismissed by one of the issuer's adjudicating rows (`Z-S178` to `Z-S187`, all in `surprise-channel/investigations/INVESTIGATION_v1.md`) and graduated by the CVO (`Z-C-S55`, `Z-C-S62`, `Z-C-S65`, `Z-C-S69`). The hazard each row armed has ended; the evidence is the adjudicating row's `dismissal_reason`, which names the order that ended it. The CVO writes the disarm clock (`.tools/surprise-row-gate.py`, R-15); this file is the owner's evidence and word.

| armed row | hazard that ended | ended by (cited in the adjudicating row) | adjudicating row | CVO graduation |
|---|---|---|---|---|
| `Z-S67` | a deploy restart revoking a client's token family | remedy R50 live; the r29 release read 0 concierge families revoked (the row's own disarm condition) | `Z-S178` | `Z-C-S55` |
| `Z-W35-S1` | the 503-while-rotation-commits route | `OG-rf-1` complete, send-gate code in live release `3d5c9c8bf1`; `OG-dr-1` closed superseded | `Z-S179` | `Z-C-S62` |
| `Z-W42-S1` | grant-writer Lambda refusing 13-month grants | Lambda rebuilt and redeployed by `OG-ap-9` (complete, proof valid) | `Z-S180` | `Z-C-S62` |
| `Z-W39-S5` | two unrelated unapplied Terraform changes | applied by `OG-ap-9` (gateway root) and `MDPF_HEALGAP` `HG-t-5` (assets root) | `Z-S181` | `Z-C-S62` |
| `Z-W43-S7` | a cold 13-month read past the ALB limit | `OG-wr-1` primed 274 of 274 dates on 8 pairs; warm read at most 12.1 s | `Z-S182` | `Z-C-S62` |
| `Z-W49-S1` | KMS policy blocking the .pptx pair write | `GatewayWritesTranscripts` statement (`NFRA_TRNSPT` apply ka21); the pair has written | `Z-S183` | `Z-C-S62` |
| `Z-W49-S3` | two writers with different object-name rules | one content-addressed key rule (`deck_<sha16>.pptx`); pair live, `OG-ap-10` complete | `Z-S184` | `Z-C-S62` |
| `Z-W49-S4` | the PutObject grant not added (naming gate) | registry row first, then the grant; `OG-ap-8` complete | `Z-S185` | `Z-C-S62` |
| `Z-S85` | a trunk-cut release revoking the transcript allowlist | allowlist hunk drained onto trunk by `OG-db-1` (5 references where there were 0) | `Z-S186` | `Z-C-S65` |
| `Z-W57-S2` | denying `blackdiamond_list_fees` ending two callers' access | Andrew answered yes; tier rule ruled; `OG-bd-2`, `OG-bd-3` complete and live | `Z-S187` | `Z-C-S69` |

**Not in this list, and why.** `Z-S312` disarms only on Andrew's real browser run (owner `2.0.0_SA_COO~O`; MC Portal relays). `Z-S177` needs a real 429 in the audit. `Z-W94-S2` is carried to the CTO's reading. Those three stay ARMED.

**Denominator.** `comp-surprise --project NFRA_OPLGTW --json` read 13 ARMED rows at 2026-10-17 ~01:5xZ; 10 are in this table, 3 are named above.
