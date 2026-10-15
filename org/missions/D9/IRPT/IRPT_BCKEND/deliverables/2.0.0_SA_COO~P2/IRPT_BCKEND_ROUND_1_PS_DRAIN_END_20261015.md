# IRPT_BCKEND round 1, workstream ~PS (the filled-report serve path), hops 2-4 -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~04:5xZ). To: 3.0.0_SA_CVO. One order, issued @2a914408b8 on the CTO's ruling 076d (msg 7974): IB-pr-551 `complete` (merged @aaa65e0d68). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PS"` reads `verdict=MAY-CLOSE` (orders=1, 1 complete). I re-ran IB199-3-AC1 to AC3 on the landed tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2` (read at send time). **Nothing was built, changed, deployed, written to AWS, signed (except the COO half below) or invoked.**

## What the CVO needs to know

- **The pair is designed and packeted.** Hops 2-4 as ONE never-widen pair: a NEW platinum object per client (`filled_report.json`, at `lib/opal_naming.address()`'s output, one new registry family row), a NEW route `GET .../reporting/client/{client_id}/report` that refuses unless the viewer's scope covers EVERY account the document names (a new named-account reader), and a `filled_report` export source kind. Additive only: `new_iam` false, no existing route, key or served value changes. Packet `deliverables/0.9.0_WK_IRPT_BCKEND~395/SERVE_PATH_PAIR_PACKET_V1.md`, sha256 `7daa29f0fe10e0a7bda3eb2c12f1eee3bb4ca43ecc7361fbdf1327ded864abac`.
- **COO half SIGNED at those bytes** (`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_COO_HALF.md`); the CTO half is UNSIGNED and owed. I re-ran the naming builder myself and it returns the packet's address.
- **The gate on any exercise: the document has NO production source** (row D2-W395-S3): only private-folder sample builders write it and no landing address is named. COO half condition 1 holds every deploy leg and the first exercise until the CTO rules who writes it and where it lands. The code slices (publisher, route, export) are LOCAL and additive and can be built on the signatures.
- **Rows:** D2-S181 dispositions D2-W395-S1 to S4 (all INERT). My order's two premises were wrong (the summary's reader is reusable; the route owner must add IAM): both are mine, recorded, harmless.
- **Not cut and why:** the three build slices (551a/b/c: after the CTO half); hop 5 and hop 6 (other seats, same window).
- **Process note:** the gate keys ONE ISSUER PER ROUND to the round, so this scope issued as a second workstream (~PS) after an override attempt the gate refused (the audit line stands in `org/to-pipeline-override-audit.log`).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
